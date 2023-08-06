"""
dimod-cache is a python package to transparently store output from dimod Sampler objects

The central entrypoint is the :class:`~HoardingSampler`-class.

(C) janus@insignificancegalore.net (2023)
"""
from __future__ import annotations
import base64
import dataclasses
from datetime import datetime
from functools import cached_property
import hashlib
import json
from pathlib import Path
import pickle
import typing

import numpy as np
import dimod
from dimod import SampleSet, Sampler
from dimod.typing import Variable, Bias


def sampleset_write(s: SampleSet, p: Path):
    """
    Store SampleSet object to file in binary efficient form
    """
    with p.open("wb") as f:
        pickle.dump(s.to_serializable(use_bytes=True), f)


def sampleset_read(p: Path) -> SampleSet:
    """
    Read SampleSet object from file created by `sampleset_write`
    """
    with p.open("rb") as f:
        s = pickle.load(f)
    return SampleSet.from_serializable(s)


def sampleset_count(s: SampleSet) -> int:
    """
    Return total number of samples stored

    If the samples are aggregated, this will in general not match number of rows in dataset.
    """
    return s.record["num_occurrences"].sum()


def sampleset_split(s: SampleSet, n: int) -> tuple[SampleSet, SampleSet]:
    """
    Split a sampleset into two parts (a, b) s.t.
    - s = concat(a,b)
    - sampleset_count(a)>=n
    """
    a = s.record["num_occurrences"].cumsum()
    idx = np.searchsorted(a, n, side="left") + 1 if n > 0 else 0
    return (s.slice(None, idx, sorted_by=None), s.slice(idx, None, sorted_by=None))


def _cache_key_save(p: Path, key):
    with p.open("w") as f:
        json.dump(key, f, sort_keys=True)


def _cache_key_load(p: Path):
    with p.open() as f:
        return json.load(f)


def _cache_key_hash(key) -> str:
    ss = json.dumps(key, sort_keys=True)
    dg = hashlib.md5(ss.encode("utf-8")).digest()
    # base64 is 6 bits/char, md5 is 128bits=6*21.33
    ret = base64.urlsafe_b64encode(dg)[:22].decode()
    return ret


class FileBasedCacheEntry:
    """
    Proxy object for the cache value pertaining to one specific key

    Key is specified via `base_path`, which must include input hash.
    The value of `base_path.name` must be glob-safe, i.e. it cannot contain
    square brackets, asterisks, or question marks.

    Replay functionality is tied to lifetime of object.
    - Once a new sampleset has been added, no replay is available
      (internal state: `_replay_available=0`)
    - Once all existing samples have been consumed via `replay_consume`,
      no further replay is possible

    Results related to one key is stored in multiple files.
    - `<base_path>.input.json`: Input cache_key
    - `<base_path>-<iso datetime>-<count>.record`: Stored sample-set with `count` records
    """

    _glob_chars = frozenset({"[", "]", "?", "*"})

    def __init__(self, base_path: Path, cache_key=None):
        base_path = Path(base_path)
        if any(c in self._glob_chars for c in base_path.name):
            raise ValueError(
                "Base path name part must be glob-safe. "
                f"Not satisfied for {base_path.name}"
            )
        self.base_path = base_path
        if cache_key is None:
            # Will fail if no key is provided and the key has not been stored
            cache_key = _cache_key_load(self.cache_key_path)
        elif not self.cache_key_path.exists():
            _cache_key_save(self.cache_key_path, cache_key)
        self.cache_key = cache_key
        self._read_cache: None | SampleSet = None
        self._replay_available: None | int = None

    @property
    def cache_key_path(self) -> Path:
        return self.base_path.with_suffix(".input.json")

    def _load_cache_key(self) -> str:
        with self.cache_key_path.open() as f:
            return json.load(f)

    def add_sampleset(self, res: SampleSet):
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")
        count = sampleset_count(res)
        dst = (
            self.base_path.parent / f"{self.base_path.name}-{timestamp}-{count}.record"
        )
        sampleset_write(res, dst)
        self._read_cache = None
        self._replay_available = 0

    @property
    def replay_available(self) -> int:
        if self._replay_available is None:
            sa = self.replay_sampleset
            self._replay_available = 0 if sa is None else sampleset_count(sa)
        return self._replay_available

    def get_sampleset_files(self) -> list[Path]:
        return sorted(self.base_path.parent.glob(self.base_path.name + "*.record"))

    def read_sampleset(self) -> None | SampleSet:
        input_paths = self.get_sampleset_files()
        if input_paths:
            return dimod.concatenate(sampleset_read(p) for p in input_paths)
        return None

    @property
    def replay_sampleset(self) -> None | SampleSet:
        if self._read_cache is None:
            self._read_cache = self.read_sampleset()
        return self._read_cache

    def replay_consume(self, n_min) -> None | SampleSet:
        """
        Replay of (partially) aggregated samples:
        - When collecting aggregated samplesets, the resulting overall set is partially
          aggregated
        - Replay will use as many rows as needed to get at least the requested number of
          samples
        - If the final row returned is an aggregate, returned sample count may be higher
          than requested
        """
        if self.replay_available == 0:
            return None
        # accessing .replay_available has ensured that ._read_cache is populated
        if self._read_cache:
            res, self._read_cache = sampleset_split(self._read_cache, n_min)
            self._replay_available = sampleset_count(self._read_cache)
            return res
        return None

    def __repr__(self) -> str:
        return f"FileBasedCacheEntry<base_path={repr(self.base_path)}>"


QUBO = typing.Mapping[typing.Tuple[Variable, Variable], Bias]


class KeyPolicy(typing.Protocol):
    ignored_input_fields: frozenset[str] = frozenset(
        {"num_reads", "time_limit", "max_num_samples", "max_answers"}
    )

    def cache_key(
        self,
        *,
        input_parameters: typing.Any,
        sampler_properties: dict,
        sampler_parameters: dict,
    ) -> dict:
        """
        Return a json-compatible dict to be used as cache key

        All three input parameters are provided as json-compatible data.
        The input parameters have already been filtered to exclude `num_reads`, etc.
        as listed in `KeyPolicy.ignored_input_fields`
        """
        pass


@dataclasses.dataclass(frozen=True)
class SampleSetCache:
    """
    Implements storage/cache functionality for HoardingSampler
    """

    sampler: Sampler
    storage_path: Path
    key_policy: KeyPolicy
    prefix: str
    enable_replay: bool
    enable_sample: bool
    _entries: dict[str, FileBasedCacheEntry] = dataclasses.field(
        init=False, default_factory=dict
    )

    @cached_property
    def sampler_properties(self):
        return self.sampler.properties

    @cached_property
    def sampler_parameters(self):
        return self.sampler.parameters

    def get(
        self, cache_key, create_if_missing: bool = False
    ) -> FileBasedCacheEntry | None:
        hash = _cache_key_hash(cache_key)
        if entry := self._entries.get(hash):
            return entry
        if not create_if_missing:
            return None
        # Create an entry for this key and make sure the storage folder exists
        self.storage_path.mkdir(parents=True, exist_ok=True)
        base_name = f"{self.prefix}-{hash}"
        base_path = self.storage_path / base_name
        entry = FileBasedCacheEntry(base_path=base_path, cache_key=cache_key)
        self._entries[hash] = entry
        return entry

    def get_or_insert(self, cache_key) -> FileBasedCacheEntry:
        res = self.get(cache_key, create_if_missing=True)
        assert res is not None
        return res

    def get_cache_key(self, **parameters):
        return self.key_policy.cache_key(
            sampler_parameters=self.sampler_parameters,
            sampler_properties=self.sampler_properties,
            input_parameters={
                k: v
                for k, v in parameters.items()
                if k not in KeyPolicy.ignored_input_fields
            },
        )

    def sample_qubo(self, Q: QUBO, **parameters) -> SampleSet:
        # QUBO as provided is not json-compatible -- store as list of items
        cache_key = self.get_cache_key(qubo_safe=list(Q.items()), **parameters)
        entry = self.get_or_insert(cache_key)

        num_reads = parameters.get("num_reads")
        res_replay = None
        if self.enable_replay and num_reads is not None and entry.replay_available > 0:
            res_replay = entry.replay_consume(num_reads)
            assert res_replay is not None  # is safe because replay_available>0
            num_reads -= sampleset_count(res_replay)
            parameters["num_reads"] = num_reads
        res_sample = None
        if self.enable_sample and (num_reads is None or num_reads > 0):
            res_sample = self.sampler.sample_qubo(Q, **parameters)
            entry.add_sampleset(res_sample)

        if res_replay is None:
            if res_sample is None:
                raise ValueError("No sample available")
            res = res_sample
        elif res_sample is None:
            res = res_replay
        else:
            res = dimod.concatenate(res_replay, res_sample)
        return res

    def entries(self) -> typing.Iterator[FileBasedCacheEntry]:
        return iter(self._entries.values())


@dataclasses.dataclass
class ManualKey(KeyPolicy):
    """
    A KeyPolicy implementation based on combining input parameters (qubo) with a manual key

    This approach can lead to false caching if the manual key is not sufficiently detailed.

    Args:
        manual_key: Value of `manual_key` and input parameters are combined as cache key.
    """

    key: dict

    def cache_key(
        self, *, sampler_parameters, sampler_properties, input_parameters
    ) -> dict:
        return {"manual_key": self.key, "input_parameters": input_parameters}


def print_key_tree(d: dict[str, typing.Any], indent=0):
    """
    Print a tree of keys for a nested hierarchy of dicts
    """
    for k, v in d.items():
        print(f"{' '*indent}{k}")
        if hasattr(v, "items"):
            print_key_tree(v, indent + 4)


def dict_partial_clone(d: dict[str, typing.Any], skip: typing.AbstractSet[str]) -> dict:
    """
    Recurse into child dicts, clone except for keys in skip set.

    Not intended for use outside SamplerCache
    """
    sf = frozenset(skip)

    def inner_clone(d):
        return (
            {k: inner_clone(v) for k, v in d.items() if k not in sf}
            if hasattr(d, "items")
            else d
        )

    return inner_clone(d)


class DefaultKey(KeyPolicy):
    """
    A KeyPolicy implementation that keeps the maximum amount of key information
    """

    def cache_key(self, **kwargs) -> dict:
        return kwargs


class PartialKey(KeyPolicy):
    """
    A KeyPolicy implementation that ignores a specific set of terms in the cache key

    Args:
        extra_skip: Skip terms to be added to default
        skip: The terms in the skip set are removed from any level of the full cache key value.
    """

    default_skip_set = frozenset({"anneal_offset_ranges", "couplers", "qubits"})

    def __init__(
        self,
        extra_skip: None | set[str] = None,
        skip: None | set[str] = None,
    ):
        some_skip: typing.AbstractSet[str] = (
            self.default_skip_set if skip is None else skip
        )
        if extra_skip is not None:
            some_skip = extra_skip.union(some_skip)
        self.skip = frozenset(some_skip)

    def cache_key(self, **kwargs) -> dict:
        return dict_partial_clone(DefaultKey().cache_key(**kwargs), skip=self.skip)


# todo: implement "replay"-functionality for `HoardingSampler``
class HoardingSampler(Sampler):
    """
    A sampler implementation that wraps a dwave sampler instance to store return values

    Results are stored as multiple files, with names of the form
    - "{prefix}-{hash}.input.json": Contains cache-key specific for input in json
      encoding. Hash value is derived from cache-key
    - "{prefix}-{hash}-{datetime}-{count}.record": Contains output SampleSet
      corresponding to a sampler run.

    When `replay` is active, existing results for a given input will be returned before
    the sampler is queried. The replay state follows the life-cycle of the Sampler
    object. To start replay over, create a new sampler object with same inputs.

    Args:
        key_policy: A KeyPolicy instance that specifies how to compute a cache-key that
                    uniquely identifies the inputs. Included implementations
                        - :class:`DefaultKey`
                        - :class:`ManualKey`
                        - :class:`PartialKey`
                    Default value: DefaultKey
        storage_path: The path to the folder to use for storing results.
        prefix: A prefix string to make it simpler to identify cache files
        replay: [False] Whether to replay previous results for same input before calling
                sampler
        replay_only: [False] If true, sampler will not be called even if replay is
                     exhausted. Implies replay.

    Simplest use:
    >>> sampler = HoardingSampler(EmbeddingComposite(DWaveSampler())
    >>> sampler.sample_qubo(qubo, num_reads=100)

    More advanced use:
    >>> sampler = HoardingSampler(EmbeddingComposite(DWaveSampler()),
    >>>               key_policy=ManualKey({'anneal_speed': 27.0, 'hardware': 'server2'}),
    >>>               storage_path='./day-02',
    >>>               prefix='dwave-server2',
    >>>           )
    """

    def __init__(
        self,
        sampler: Sampler,
        *,
        key_policy: None | KeyPolicy = None,
        storage_path: None | Path = None,
        prefix: str = "dwave",
        replay: bool = False,
        replay_only: bool = False,
    ):
        super().__init__()

        if key_policy is None:
            key_policy = DefaultKey()
        storage_path = Path(".") if storage_path is None else Path(storage_path)
        self.cache = SampleSetCache(
            sampler=sampler,
            key_policy=key_policy,
            storage_path=storage_path,
            prefix=prefix,
            enable_replay=replay or replay_only,
            enable_sample=not replay_only,
        )

    @property
    def sampler(self) -> Sampler:
        return self.cache.sampler

    def sample_qubo(self, Q: QUBO, **parameters) -> SampleSet:
        return self.cache.sample_qubo(Q, **parameters)

    @property
    def parameters(self) -> typing.Dict[str, typing.Any]:
        return self.cache.sampler_parameters

    @property
    def properties(self) -> typing.Dict[str, typing.Any]:
        return self.cache.sampler_properties

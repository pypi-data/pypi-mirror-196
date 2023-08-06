from dimod import SampleSet
from dimod_cache import sampleset_split, sampleset_count, dict_partial_clone


def test_sampleset_split():
    ss = SampleSet.from_samples(
        [[int(c) for c in f"{v:03b}"] for v in range(8)],
        vartype="BINARY",
        energy=[1, 2, 3, 4, 4, 3, 2, 1],
        num_occurrences=[1, 2, 3, 4, 4, 3, 2, 1],
    )
    assert sampleset_count(ss) == 20
    ab = sampleset_split(ss, 0)
    assert [sampleset_count(s) for s in ab] == [0, 20]

    ab = sampleset_split(ss, 1)
    assert [sampleset_count(s) for s in ab] == [1, 19]

    ab = sampleset_split(ss, 6)
    assert ab[0].record.energy.tolist() == [1, 2, 3]
    assert [sampleset_count(s) for s in ab] == [6, 14]

    ab = sampleset_split(ss, 7)
    assert [sampleset_count(s) for s in ab] == [10, 10]

    ab = sampleset_split(ss, 20)
    assert [sampleset_count(s) for s in ab] == [20, 0]


def test_dict_partial_clone():
    dd = {"a": 1, "x": "a", "b": {"y": "n", "c": 3, "d": [1, 2, 3]}}
    ddf = dict_partial_clone(dd, {"x", "y"})
    assert set(ddf.keys()) == {"a", "b"}
    assert set(ddf["b"].keys()) == {"c", "d"}
    assert ddf["b"]["d"] == [1, 2, 3]

`dimod-cache` is a hoarding proxy framework for `dimod.Sampler`-objects.

Example use:

```
import dimod
import dwave.samplers

qubo = dimod.generators.gnp_random_bqm(10, .5, 'BINARY').to_qubo()[0]

sampler = HoardingSampler(dwave.samplers.SimulatedAnnealingSampler(), replay=True)
res_1 = sampler.sample_qubo(qubo, num_reads=10)

sampler = HoardingSampler(dwave.samplers.SimulatedAnnealingSampler(), replay=True)
res_2 = sampler.sample_qubo(qubo, num_reads=10)

assert res_1==res_2
```
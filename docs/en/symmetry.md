# Diagram symmetry

`myqcd.symmetry` counts vertex automorphisms and parallel-edge exchanges of
a finite diagram. It deliberately does **not** assign a physics symmetry
factor: that requires the identical-particle and vertex-exchange
conventions.

## Automorphisms

A vertex permutation is an automorphism when it preserves the edge multiset,
including particle labels and external endpoints ($-1$).

| Diagram | Vertex automorphisms | Edge exchanges |
|---|---|---|
| chain with four vertices | 2 | 1 |
| triangle | 6 | 1 |
| self-energy | 2 | 1 |
| sunset | 2 | 6 |

The sunset has three identical internal gluons, hence the $3!=6$ edge
exchange factor. Swapping the two vertices is an automorphism because both
external legs are quark stubs.

## Reproduce

```python
from myqcd import symmetry, topology

assert symmetry.automorphism_count(topology.build_cycle(3)) == 6
assert symmetry.automorphism_count(topology.build_chain(4)) == 2
assert symmetry.edge_exchange_count(topology.build_sunset()) == 6
print(symmetry.symmetry_table(topology.build_self_energy()))
```

## Why the physics factor is separate

A physics symmetry factor also depends on whether external legs are
distinguishable, how identical vertices are grouped and which Wick
contractions are counted. Those conventions are not encoded in the graph
alone, so the table above is a combinatorial input, not a final factor.

# Diagram topology

`myqcd.topology` works on the combinatorial graph only: vertices, internal
edges, external-leg edges and particle labels. It computes invariants and,
for small graphs, decides isomorphism by explicit vertex permutations.

## Invariants

For a diagram with $V$ vertices, $E_{\mathrm{int}}$ internal edges and $C$
connected components,

$$
L=E_{\mathrm{int}}-V+C,
\qquad
\text{tree}\iff E_{\mathrm{int}}=V-C.
$$

A single cycle has $V\ge3$, $E_{\mathrm{int}}=V$ and every degree equal to
two. External-leg edges (endpoint $-1$) are excluded from
$E_{\mathrm{int}}$.

## Isomorphism and enumeration

`canonical_signature` takes the lexicographically smallest edge signature
over vertex relabelings. `is_isomorphic` compares the edge multiset under
all permutations up to eight vertices. For larger graphs only the canonical
signature is used and the limitation is explicit.

The small-graph enumerator gives:

| Vertices | Internal edges | Connected isomorphism classes |
|---|---|---|
| 3 | 3 | 1 (triangle) |
| 4 | 3 | 2 (path, star) |
| 4 | 4 | 2 (cycle, triangle with pendant) |

## Reproduce

```python
from myqcd import topology

triangle = topology.build_cycle(3)
chain = topology.build_chain(3)
assert triangle.loop_count == 1
assert topology.is_cycle(triangle)
assert topology.is_tree(chain)
assert not topology.is_isomorphic(triangle, chain)

trees = topology.enumerate_connected_topologies(4, 3)
assert len(trees) == 2
print(topology.topology_table(triangle))
```

## Comparison with standard graph theory

| Quantity | MyQCD | Standard |
|---|---|---|
| Loop number | $E_{\mathrm{int}}-V+C$ | cycle rank |
| Tree criterion | $E_{\mathrm{int}}=V-C$ | forest |
| Cycle criterion | all degrees 2, $E_{\mathrm{int}}=V$ | simple cycle |
| Isomorphism | exact for $V\le8$ | graph isomorphism |

Symmetry factors are deliberately not assigned here: they require the
particle-content and vertex-exchange conventions of a specific diagram.

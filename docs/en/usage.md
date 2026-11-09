# Usage

## Audit the operator and diagram layers

```bash
python -m myqcd.operator_audit --root .
```

The command writes `logs/data/operator_audit/operator_feynman_audit.json` and
returns a non-zero exit code if any check fails.

It verifies the Clifford algebra, the rank of the 16 Dirac structures, the
Dirac trace theorem against explicit matrices, the SU(3) Fierz identity,
bilinear decomposition round trips, Wick pairing graphs, loop counting and the
exporters.

## Use the algebra layers

```python
import sympy as sp

from myqcd import color, gamma, operators

assert gamma.gamma_basis_rank() == 16
assert gamma.trace_gamma_product((1, 1)) == 4
assert color.casimir_fundamental() == sp.Rational(4, 3)

operator = operators.BilinearOperator(
    name="O_V4", left_flavor="u", right_flavor="d", structure="V4"
)
assert operator.pyqcd_gamma_index == 4
assert operator.mass_dimension == 3
```

## Build and export a diagram

```python
from myqcd import diagram_export, feynman

triangle = feynman.Diagram(
    vertices=("a", "b", "c"),
    edges=(
        feynman.Edge(0, 1, "gluon"),
        feynman.Edge(1, 2, "gluon"),
        feynman.Edge(2, 0, "gluon"),
    ),
)
assert triangle.loop_count == 1
assert diagram_export.to_tikz(triangle).startswith("%")
assert diagram_export.to_dot(triangle).startswith("digraph")
assert diagram_export.to_svg(triangle).startswith("<?xml")
```

## Wick pairings

```python
from myqcd import wick

fields = wick.fermion_fields(["u"], ["u"])
pairings = wick.enumerate_wick_pairings(fields)
assert len(pairings) == 1
assert pairings[0].sign in (-1, 1)
```

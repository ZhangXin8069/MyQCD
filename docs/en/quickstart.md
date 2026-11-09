# Quickstart

## Install

```bash
pip install myqcd
```

Python 3.10+ and SymPy 1.12+; the full suite is exercised on Python 3.12.

## First audit

```bash
python -m myqcd.operator_audit
```

The command prints a JSON summary and writes
`logs/data/operator_audit/operator_feynman_audit.json` under the current
directory.

## First operator

```python
import sympy as sp

from myqcd import gamma, operators

pion = operators.BilinearOperator("O_pi", "u", "d", "P")
assert pion.mass_dimension == 3
assert pion.parity_sign == -1
assert pion.charge_conjugation_sign == 1
assert pion.pyqcd_gamma_index == 5
assert gamma.trace_gamma_product((1, 1)) == 4
print(pion.latex())
```

## First Fierz check

```python
import sympy as sp

from myqcd import fierz

coefficients = fierz.fierz_transform("S", "S")
assert coefficients[("S", "S")] == sp.Rational(1, 4)
assert coefficients[("A1", "A1")] == -sp.Rational(1, 4)
print(len(coefficients))
```

## First diagram

```python
from myqcd import diagram_export, topology

triangle = topology.build_cycle(3)
assert triangle.loop_count == 1
assert diagram_export.to_mermaid(triangle).startswith("flowchart LR")
print(diagram_export.export_audit(triangle)["formats"])
```

## Where to go next

| Goal | Page |
|---|---|
| Learn the full workflow | `tutorial` |
| See worked checks | `worked-examples` |
| Look up a quantity | `reference-values` |
| Understand conventions | `conventions` |
| Check API names | `api-reference` |

## Boundaries

The quickstart checks exact algebra and structure. It does not install or
read a lattice ensemble, compute loop integrals or perform a continuum
extrapolation.

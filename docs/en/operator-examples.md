# Operator examples

A compact catalog of physically motivated bilinears. The signs are computed
by `myqcd.operators`; the names are labels, not full interpolating fields
with smearing or gauge links.

| Operator | Structure | Derivatives | Parity | C | dim | PyQCD |
|---|---|---|---|---|---|---|
| $\bar q\gamma_5q$ | `P` | 0 | $-1$ | $+1$ | 3 | 5 |
| $\bar q\gamma_4q$ | `V4` | 0 | $+1$ | $-1$ | 3 | 4 |
| $\bar q\gamma_4\gamma_5q$ | `A4` | 0 | $-1$ | $-1$ | 3 | 15 |
| $\bar q q$ | `S` | 0 | $+1$ | $+1$ | 3 | 0 |
| $\bar q\sigma_{12}q$ | `T12` | 0 | $+1$ | $-1$ | 3 | 8 |
| $\bar q\gamma_3D_\mu q$ | `V3` | 1 | $-1$ | $+1$ | 4 | 3 |
| $\bar q\gamma_4D_\mu D_\nu q$ | `V4` | 2 | $+1$ | $-1$ | 5 | 4 |
| $\bar q\gamma_5D_\mu q$ | `P` | 1 | $-1$ | $+1$ | 4 | 5 |

## Checks

```python
from myqcd import operators

for structure in ("S", "P", "V4", "A4", "T12"):
    operator = operators.BilinearOperator(
        name=f"O_{structure}",
        left_flavor="u",
        right_flavor="d",
        structure=structure,
    )
    assert operator.mass_dimension == 3
    assert operator.pyqcd_gamma_index is not None or structure == "T13"
print("operator examples OK")
```

## What the table does not mean

- The labels do not include smearing, Wilson lines or source conjugation.
- Derivative operators are not automatically symmetrized or made traceless.
- The PyQCD index is an exact matrix match; `T13` has no exact entry.
- A physical interpolating field may mix several structures.

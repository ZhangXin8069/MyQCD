# Operators

`myqcd.operators` implements the 16 Dirac bilinears in the PyQCD
DeGrand--Rossi basis. A bilinear is written as `bar q_u Gamma q_d`.

## Dirac basis

| Structure | Class | Parity | C | dim | PyQCD index |
|---|---|---|---|---|---|
| `S` | S | +1 | +1 | 3 | 0 |
| `P` | P | -1 | +1 | 3 | 5 |
| `V1` | V | -1 | +1 | 3 | 1 |
| `V2` | V | -1 | -1 | 3 | 2 |
| `V3` | V | -1 | +1 | 3 | 3 |
| `V4` | V | +1 | -1 | 3 | 4 |
| `A1` | A | +1 | +1 | 3 | 12 |
| `A2` | A | +1 | -1 | 3 | 13 |
| `A3` | A | +1 | +1 | 3 | 14 |
| `A4` | A | -1 | -1 | 3 | 15 |
| `T12` | T | +1 | -1 | 3 | 8 |
| `T13` | T | +1 | +1 | 3 | — |
| `T14` | T | -1 | -1 | 3 | 9 |
| `T23` | T | +1 | -1 | 3 | 6 |
| `T24` | T | -1 | +1 | 3 | 10 |
| `T34` | T | -1 | -1 | 3 | 11 |

Notes:

- Parity is computed from `gamma4 Gamma gamma4 = s Gamma`.
- Charge conjugation is computed from `C^-1 Gamma C = s Gamma` with
  `C = gamma4 gamma2`.
- Mass dimension at zero derivatives is 3.
- The PyQCD index is the exact `gamma(i)` index. `T13` has no exact entry
  because `gamma(7) = gamma3 gamma1 = -sigma13`.

## Reproduce the decomposition

```python
import sympy as sp
from myqcd import operators

matrix = operators.structure_matrix("V4")
coefficients = operators.decompose_dirac_bilinear(matrix)
assert sp.simplify(coefficients["V4"] - 1) == 0
assert all(
    sp.simplify(value) == 0
    for name, value in coefficients.items()
    if name != "V4"
)
print(coefficients["V4"])
```

## Comparison with standard values

The numbers below are exact SymPy results. "Standard" means the conventional
SU(3)/Dirac values in four Euclidean dimensions, not a fit to an ensemble.

### Dirac algebra

| Identity | MyQCD | Standard |
|---|---|---|
| `Tr[1]` | 4 | 4 |
| `Tr[gamma_mu gamma_nu]` | `4 delta_mu_nu` | `4 delta_mu_nu` |
| `Tr[gamma1 gamma1]` | 4 | 4 |
| `Tr[gamma1 gamma2]` | 0 | 0 |
| `Tr[gamma1 gamma2 gamma3 gamma4]` | 0 | 0 |
| `Tr[gamma5 gamma1 gamma2 gamma3 gamma4]` | 4 | `4 epsilon_1234 = 4` |
| `gamma5^2` | 1 | 1 |
| `{gamma5, gamma_mu}` | 0 | 0 |
| `C gamma_mu C^-1` | `-gamma_mu^T` | `-gamma_mu^T` |

### SU(3) color algebra

| Quantity | MyQCD | Standard |
|---|---|---|
| `C_F` | `4/3` | `4/3` |
| `C_A` | `3` | `3` |
| `f_123` | `1` | `1` |
| `f_147` | `1/2` | `1/2` |
| `f_458` | `sqrt(3)/2` | `sqrt(3)/2` |
| `d_118` | `1/sqrt(3)` | `1/sqrt(3)` |
| `d_146` | `1/2` | `1/2` |
| `sum f^2` | `24` | `24` |
| `sum d^2` | `40/3` | `40/3` |
| `Tr[T^a T^b]` | `delta_ab/2` | `delta_ab/2` |

The historical SU(3) derivations in `myqcd.derivations` use the anti-Hermitian
normalization `-delta_ab/2`; the values above belong to the Hermitian
`myqcd.color` layer and must not be mixed with the historical convention.

## Command

```bash
python -m myqcd.operator_audit
```

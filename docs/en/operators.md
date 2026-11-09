# Operators

`myqcd.operators` implements the 16 Dirac bilinears in the PyQCD
DeGrand--Rossi basis. A bilinear is written as $\bar q_u \Gamma q_d$.

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

- Parity is computed from $\gamma_4 \Gamma \gamma_4 = s\,\Gamma$.
- Charge conjugation is computed from $C^{-1}\Gamma C = s\,\Gamma$ with
  $C = \gamma_4\gamma_2$.
- Mass dimension at zero derivatives is $3$.
- The PyQCD index is the exact $\gamma(i)$ index. `T13` has no exact entry
  because $\gamma(7) = \gamma_3\gamma_1 = -\sigma_{13}$.

## Worked examples

### Non-trivial decomposition

```python
import sympy as sp

from myqcd import gamma, operators

matrix = (
    gamma.gamma(1) * gamma.gamma(2)
    + 2 * gamma.gamma(3) * gamma.gamma5()
    + gamma.gamma5()
)
coefficients = operators.decompose_dirac_bilinear(matrix)
assert sp.simplify(coefficients["T12"] - 1) == 0
assert sp.simplify(coefficients["A3"] - 2) == 0
assert sp.simplify(coefficients["P"] - 1) == 0
assert (
    operators.reconstruct_dirac_bilinear(coefficients) - matrix
).is_zero_matrix
print(
    {
        name: value
        for name, value in coefficients.items()
        if value != 0
    }
)
```

### Meson interpolating operators

```python
from myqcd import operators

pion = operators.BilinearOperator("O_pi", "u", "d", "P")
rho = operators.BilinearOperator("O_rho", "u", "d", "V4")
a1 = operators.BilinearOperator("O_a1", "u", "d", "A4")

assert [pion.parity_sign, rho.parity_sign, a1.parity_sign] == [-1, 1, -1]
assert [
    pion.charge_conjugation_sign,
    rho.charge_conjugation_sign,
    a1.charge_conjugation_sign,
] == [1, -1, -1]
print(pion.latex(), rho.latex(), a1.latex())
```

| Operator | Structure | Parity | C | PyQCD index |
|---|---|---|---|---|
| $\pi$ | `P` | $-1$ | $+1$ | 5 |
| $\rho$ (temporal) | `V4` | $+1$ | $-1$ | 4 |
| $a_1$ (temporal) | `A4` | $-1$ | $-1$ | 15 |

These are quantum-number labels; smearing, gauge links and source conjugation
are separate layers.

### Derivative operators

```python
from myqcd import operators

twist2 = operators.BilinearOperator(
    "O_twist2", "u", "u", "V3", derivatives=1
)
twist3 = operators.BilinearOperator(
    "O_twist3", "u", "u", "V3", derivatives=2
)
assert (twist2.mass_dimension, twist3.mass_dimension) == (4, 5)
print(twist2.mass_dimension, twist3.mass_dimension)
```

For example, $\mathcal{O}_{\mu\nu} = \bar q\,\gamma_\mu D_\nu q$ has mass
dimension $4$, and two derivatives give dimension $5$. The class does not
model symmetrization, tracelessness or equation-of-motion reduction.

### Explicit matrix identities

```python
import sympy as sp

from myqcd import gamma

assert gamma.gamma5() == sp.diag(1, 1, -1, -1)
assert gamma.charge_conjugation_matrix() == gamma.gamma(4) * gamma.gamma(2)
assert (
    gamma.dirac_trace(
        gamma.gamma5()
        * gamma.gamma(1)
        * gamma.gamma(2)
        * gamma.gamma(3)
        * gamma.gamma(4)
    )
    == 4
)
```

## Comparison with standard values

The numbers below are exact SymPy results. "Standard" means the conventional
SU(3)/Dirac values in four Euclidean dimensions, not a fit to an ensemble.

### Dirac algebra

| Identity | MyQCD | Standard |
|---|---|---|
| $\mathrm{Tr}[1]$ | $4$ | $4$ |
| $\mathrm{Tr}[\gamma_\mu\gamma_\nu]$ | $4\delta_{\mu\nu}$ | $4\delta_{\mu\nu}$ |
| $\mathrm{Tr}[\gamma_1\gamma_1]$ | $4$ | $4$ |
| $\mathrm{Tr}[\gamma_1\gamma_2]$ | $0$ | $0$ |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_3\gamma_4]$ | $0$ | $0$ |
| $\mathrm{Tr}[\gamma_5\gamma_1\gamma_2\gamma_3\gamma_4]$ | $4$ | $4\epsilon_{1234}=4$ |
| $\gamma_5^2$ | $1$ | $1$ |
| $\{\gamma_5,\gamma_\mu\}$ | $0$ | $0$ |
| $C\gamma_\mu C^{-1}$ | $-\gamma_\mu^{T}$ | $-\gamma_\mu^{T}$ |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_1\gamma_2]$ | $-4$ | $-4$ |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_2\gamma_1]$ | $4$ | $4$ |

### SU(3) color algebra

| Quantity | MyQCD | Standard |
|---|---|---|
| $C_F$ | $4/3$ | $4/3$ |
| $C_A$ | $3$ | $3$ |
| $T_F$ | $1/2$ | $1/2$ |
| $f_{123}$ | $1$ | $1$ |
| $f_{147}$ | $1/2$ | $1/2$ |
| $f_{458}$ | $\sqrt{3}/2$ | $\sqrt{3}/2$ |
| $d_{118}$ | $1/\sqrt{3}$ | $1/\sqrt{3}$ |
| $d_{146}$ | $1/2$ | $1/2$ |
| $\sum f^2$ | $24$ | $24$ |
| $\sum d^2$ | $40/3$ | $40/3$ |
| $\mathrm{Tr}[T^aT^b]$ | $\frac{1}{2}\delta^{ab}$ | $\frac{1}{2}\delta^{ab}$ |

The historical SU(3) derivations in `myqcd.derivations` use the anti-Hermitian
normalization $-\frac{1}{2}\delta^{ab}$; the values above belong to the
Hermitian `myqcd.color` layer and must not be mixed with the historical
convention.

### Reference conventions

- PyQCD DeGrand--Rossi basis:
  `refer/git-rep/PyQCD/pyqcd/lattice/_gamma.py`.
- Standard SU(3) trace and $f/d$ conventions:
  `refer/git-rep/feyncalc/FeynCalc/SUN/SUNTrace.m` (reference only).

## Command

```bash
python -m myqcd.operator_audit
```

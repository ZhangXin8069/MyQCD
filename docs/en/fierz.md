# Fierz transformations

`myqcd.fierz` implements the general Dirac Fierz rearrangement in the 16
bilinear basis. With $\Gamma_A$ from `myqcd.operators`,

$$
\left(\bar\psi_1\Gamma_A\psi_2\right)
\left(\bar\psi_3\Gamma_B\psi_4\right)
=
\sum_{C,D}F_{AB}^{CD}
\left(\bar\psi_1\Gamma_C\psi_4\right)
\left(\bar\psi_3\Gamma_D\psi_2\right).
$$

The coefficients are computed exactly by projecting onto the dual basis
$\Gamma^A=\Gamma_A/g_A$, where
$g_A=\mathrm{Tr}[\Gamma_A\Gamma_A]/4\in\{+1,-1\}$ in the Euclidean basis.
The engine is checked against both the component-level matrix identity and
random complex spinors.

## Scalar–scalar example

For $A=B=S$ the only non-zero terms have $C=D$:

| $C=D$ | Coefficient |
|---|---|
| `S`, `P`, `V1`–`V4` | $+1/4$ |
| `A1`–`A4`, `T12`–`T34` | $-1/4$ |

The signs follow the Euclidean basis; they are not an arbitrary convention.
For mixed structures, e.g. $A=S$, $B=V_1$, the non-zero partners include
$(C,D)=(S,V_1),(P,A_1),(V_1,S)$ and tensor/axial combinations.

## Reproduce

```python
import sympy as sp

from myqcd import fierz

scalar = fierz.fierz_transform("S", "S")
assert scalar[("S", "S")] == sp.Rational(1, 4)
assert scalar[("A1", "A1")] == -sp.Rational(1, 4)

mixed = fierz.fierz_transform("S", "V1")
assert mixed[("S", "V1")] == sp.Rational(1, 4)
assert mixed[("V1", "S")] == sp.Rational(1, 4)
assert len(mixed) == 16

spinors = [
    [1.0 + 0.5j, 0.0, 0.0, 0.0],
    [0.0, 1.0 - 0.5j, 0.0, 0.0],
    [0.0, 0.0, 1.0 + 0.5j, 0.0],
    [0.0, 0.0, 0.0, 1.0 - 0.5j],
]
assert abs(fierz.fierz_residual("S", "V1", spinors)) < 1e-9
print(len(fierz.common_identities()))
```

## Comparison with standard identities

| Check | Result |
|---|---|
| Dual completeness $\sum_A\Gamma_A^{ij}\Gamma^{A,kl}=4\delta^{il}\delta^{kj}$ | exact |
| Matrix identity for tested $(A,B)$ | exact |
| Random-spinor residual | $<10^{-9}$ |
| Number of non-zero terms for $S$–$S$ | 16 |
| Number of non-zero terms for $S$–$V_1$ | 16 |

The overall sign of a Fierz rearrangement depends on the Grassmann
convention used when moving $\psi_2$ past $\bar\psi_3$; this package checks
the commuting-component matrix identity and states the convention explicitly.

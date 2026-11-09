# Lattice operators

Lattice operator construction combines Dirac structure, color, gauge links
and displacement. `myqcd` provides the exact algebraic pieces; the gauge
field arrays and tensor contractions belong to the numerical PyQCD layer.

## Wilson line

A straight Wilson line from $x$ to $y$ is

$$
W(x,y)=\prod_{s\in\text{path}}U_\mu(s),
$$

with $U_\mu(x)\mapsto G(x)U_\mu(x)G^\dagger(x+\hat\mu)$. A bilinear with a
Wilson line is

$$
\mathcal{O}_{\Gamma}(x;z)
=\bar q(x)\,\Gamma\,W(x,x+z)\,q(x+z).
$$

## Clover and staple

The clover field strength is

$$
F_{\mu\nu}(x)=\frac{-i}{8}\sum_{\pm}
\left(P_{\mu\nu}(x)-P_{\mu\nu}^\dagger(x)\right),
$$

and a staple operator uses a three-segment path
$-L\hat z\to b\hat b\to(L+z)\hat z$. These are the structures used by the
gluon OPE and TMD layers of PyQCD.

## Quantum numbers

| Operator | Structure | Derivatives | Parity | C | PyQCD index |
|---|---|---|---|---|---|
| $\bar q\gamma_5q$ | `P` | 0 | $-1$ | $+1$ | 5 |
| $\bar q\gamma_4q$ | `V4` | 0 | $+1$ | $-1$ | 4 |
| $\bar q\gamma_4\gamma_5q$ | `A4` | 0 | $-1$ | $-1$ | 15 |
| $\bar q\gamma_3D_\mu q$ | `V3` | 1 | $-1$ | $+1$ | 3 |

## Reproduce

```python
import sympy as sp

from myqcd import gamma, operator_basis, operators

pion = operators.BilinearOperator("O_pi", "u", "d", "P")
assert pion.parity_sign == -1
assert pion.charge_conjugation_sign == 1
assert pion.pyqcd_gamma_index == 5

twist = operator_basis.DerivativeOperator(
    "O_twist", "V3", derivatives=1, color="octet"
)
assert twist.mass_dimension == 4
assert twist.pyqcd_gamma_index == 3
assert all(operator_basis.chiral_projector_identities().values())
print(pion.latex(), twist.latex())
```

## Boundary

The algebraic checks do not prove gauge invariance of a particular lattice
discretization. Path ordering, link smearing, clover improvement and
gradient-flow renormalization require the numerical implementation and its
own tests.

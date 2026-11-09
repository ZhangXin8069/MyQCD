# Lorentz algebra

`myqcd.lorentz` provides four-dimensional Euclidean tensor algebra: the
metric, the Levi-Civita tensor, contractions, the Schouten identity and
transverse/spin-2 projectors. All identities are exact SymPy expressions.

## Metric and epsilon

$$
\delta_{\mu\nu}=\mathrm{diag}(1,1,1,1),\qquad
\varepsilon_{0123}=+1.
$$

The basic contractions are

$$
\sum_{\mu\nu\rho\sigma}\varepsilon_{\mu\nu\rho\sigma}^2=24,
$$

$$
\sum_{\rho\sigma}\varepsilon_{\mu\nu\rho\sigma}
\varepsilon_{\alpha\beta\rho\sigma}
=2\left(\delta_{\mu\alpha}\delta_{\nu\beta}
-\delta_{\mu\beta}\delta_{\nu\alpha}\right),
$$

and the full contraction is the determinant of Kronecker deltas. The
four-dimensional Schouten identity vanishes identically:

$$
\varepsilon_{abcd}p_e+\varepsilon_{bcde}p_a
+\varepsilon_{cdea}p_b+\varepsilon_{deab}p_c
+\varepsilon_{eabc}p_d=0.
$$

## Projectors

For $p^2\neq0$ the transverse and longitudinal projectors are

$$
T_{\mu\nu}=\delta_{\mu\nu}-\frac{p_\mu p_\nu}{p^2},
\qquad
L_{\mu\nu}=\frac{p_\mu p_\nu}{p^2},
\qquad
T_{\mu\nu}+L_{\mu\nu}=\delta_{\mu\nu}.
$$

The transverse traceless spin-2 projector is

$$
P^{(2)}_{\mu\nu\rho\sigma}
=\frac12\left(T_{\mu\rho}T_{\nu\sigma}+T_{\mu\sigma}T_{\nu\rho}\right)
-\frac13 T_{\mu\nu}T_{\rho\sigma}.
$$

In four dimensions it projects onto the five transverse traceless
polarizations; its one-pair trace vanishes.

## Reproduce

```python
import sympy as sp

from myqcd import lorentz

p = lorentz.vector_components("p")

assert lorentz.epsilon_square() == 24
assert lorentz.epsilon_two_contract_residual() == 0
assert lorentz.schouten_residual(p) == 0
assert lorentz.spin2_dimension(p) == 5
assert lorentz.spin2_traceless_check(p) == 0

def projector(mu, nu):
    return lorentz.transverse_projector(p, mu, nu)

assert sp.simplify(
    sum(projector(0, nu) * projector(nu, 2) for nu in range(4))
    - projector(0, 2)
) == 0
print(lorentz.epsilon_two_contract(0, 1, 0, 1))
```

## Comparison with standard values

| Quantity | MyQCD | Standard |
|---|---|---|
| $\sum\varepsilon^2$ | $24$ | $4!$ |
| $\varepsilon_{\mu\nu\rho\sigma}\varepsilon_{\alpha\beta\rho\sigma}$ | $2(\delta_{\mu\alpha}\delta_{\nu\beta}-\delta_{\mu\beta}\delta_{\nu\alpha})$ | same |
| $\delta_{\mu\nu}T_{\mu\nu}$ | $3$ | $D-1$ |
| $\sum_{\mu\nu}P^{(2)}_{\mu\nu\mu\nu}$ | $5$ | $(D-1)D/2-1$ |

The dimension count is the transverse traceless symmetric rank-2 dimension
in $D-1=3$ spatial dimensions.

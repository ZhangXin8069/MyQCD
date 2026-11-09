# QCD Lagrangian

The Euclidean QCD Lagrangian with gauge fixing and ghosts is

$$
\mathcal{L}
=-\frac14 F^a_{\mu\nu}F^a_{\mu\nu}
+\bar\psi\left(\gamma_\mu D_\mu+m\right)\psi
+\frac{1}{2\xi}\left(\partial_\mu A^a_\mu\right)^2
+\bar c^a\left(-\partial_\mu D^{ab}_\mu\right)c^b,
$$

with

$$
D_\mu=\partial_\mu-igT^aA^a_\mu,
\qquad
F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu
+gf^{abc}A^b_\mu A^c_\nu.
$$

## Vertices from the expansion

| Term | Vertex | Coupling |
|---|---|---|
| $\bar\psi\gamma_\mu T^aA^a_\mu\psi$ | q-qbar-g | $g$ |
| $gf^{abc}(\partial A)AA$ | g-g-g | $g$ |
| $g^2f^{abe}f^{cde}A A A A$ | g-g-g-g | $g^2$ |
| $\bar c\,\partial_\mu( gT^aA^a_\mu)c$ | c-cbar-g | $g$ |

The vertex factors and mass dimensions are exposed by `myqcd.qcd_rules`.

## Reproduce the algebraic check

```python
import sympy as sp

from myqcd import qcd_rules

p = (sp.Symbol("p0"), sp.Symbol("p1"), sp.Symbol("p2"), sp.Symbol("p3"))
assert qcd_rules.ward_identity_residual(p).is_zero_matrix
assert qcd_rules.rule_audit()["vertex_count"] == 4
print(qcd_rules.propagator_mass_dimensions())
```

## Boundary

The Lagrangian above fixes the Euclidean sign conventions. A different
Minkowski convention changes overall signs; loop integrals, gauge-fixing
dependence and BRST cohomology are outside this page.

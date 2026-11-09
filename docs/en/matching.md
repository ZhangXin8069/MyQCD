# Matching

`myqcd.matching` collects tree-level matching coefficients, the Fourier
prefactor and the hybrid switch used by TMD matching.

## Tree level

For the bilinear basis the tree-level matching is

$$
C_\Gamma^{(0)}=1,
\qquad
\mathcal{O}_\Gamma^{\mathrm{MS}}=
\mathcal{O}_\Gamma^{\mathrm{lattice}}+\cdots
$$

The package checks the coefficient and the convolution prefactor; it does
not derive loop matching kernels.

## Hybrid switch

A smooth switch is

$$
f(x;x_0,w)=\frac{1}{1+e^{-(x-x_0)/w}},
\qquad
f(x_0)=\frac12.
$$

The residual at the midpoint is checked exactly.

## Reproduce

```python
import sympy as sp

from myqcd import matching

assert matching.tree_level_matching("S") == 1
assert matching.hybrid_continuity_residual() == 0
assert matching.matching_residual(2, 4, sp.Rational(1, 2)) == 0
assert matching.fourier_prefactor() == 1 / sp.pi
print(matching.matching_table(("S", "V")))
```

## Boundary

The tree-level coefficient is a convention, not a one-loop result. The
hybrid switch is a smoothing function; its implementation in a matching
formula requires a separate derivation.

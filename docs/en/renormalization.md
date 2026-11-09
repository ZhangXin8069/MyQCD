# Renormalization

`myqcd` provides the algebraic ingredients of bilinear renormalization:
Dirac projectors, color traces, operator dimensions and mixing matrices. It
does not compute loop integrals or fit Z factors to an ensemble.

## RI/MOM condition

For an amputated vertex $\Lambda_\Gamma(p)$ and a projector $P_\Gamma$, the
RI/MOM condition at $p^2=\mu^2$ is schematically

$$
Z_\Gamma\,
\mathrm{Tr}\left[P_\Gamma\Lambda_\Gamma(p)\right]_{p^2=\mu^2}
=
\mathrm{Tr}\left[P_\Gamma\Lambda_\Gamma^{(0)}(p)\right]_{p^2=\mu^2}.
$$

The tree-level vertex is the Dirac matrix itself. The projectors used here
are the 16 bilinears $S,P,V_\mu,A_\mu,T_{\mu\nu}$.

## Projector normalization

| Structure | Matrix | Tree trace |
|---|---|---|
| $S$ | $1$ | $4$ |
| $P$ | $\gamma_5$ | $4$ |
| $V_\mu$ | $\gamma_\mu$ | $4$ |
| $A_\mu$ | $\gamma_\mu\gamma_5$ | $4$ |
| $T_{\mu\nu}$ | $\sigma_{\mu\nu}$ | $4$ |

For the tensor basis the Euclidean Gram sign is negative; the projector
normalization must use the corresponding $g_A$ factor rather than assuming
all traces are $+4$.

## Mixing matrix

A set of operators $\mathcal{O}_i$ renormalizes as

$$
\mathcal{O}_i^{R}
=\sum_j Z_{ij}\mathcal{O}_j .
$$

The algebraic layer can test that a supplied $Z$ matrix is invertible and
that tree-level $Z^{(0)}=1$; it does not derive the loop coefficients.

## Reproduce

```python
import sympy as sp

from myqcd import gamma, operators

assert gamma.dirac_trace(gamma.identity()) == 4
assert gamma.dirac_trace(gamma.gamma5()) == 0
assert gamma.dirac_trace(gamma.gamma(4)) == 0
assert gamma.dirac_trace(gamma.gamma(4) * gamma.gamma(4)) == 4

values = [
    operators.BilinearOperator("O", "u", "u", structure).charge_conjugation_sign
    for structure in ("S", "P", "V4", "A4")
]
assert values == [1, 1, -1, -1]
print(values)
```

## Projector algebra

```python
import sympy as sp

from myqcd import renormalization

for name in renormalization.bilinear_projectors():
    assert sp.simplify(
        renormalization.tree_level_projection(name) - 1
    ) == 0

assert renormalization.z_factor(sp.Integer(2), sp.Integer(4)) == sp.Rational(1, 2)
assert renormalization.mixing_matrix_is_invertible(sp.eye(3))
print(renormalization.projector_table()[:2])
```

## Boundary

The package does not claim a complete RI/MOM analysis: loop integrals,
trace projectors with external spinors, perturbative matching kernels and
continuum extrapolation are separate tasks.

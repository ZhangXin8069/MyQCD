# QCD Feynman rules

`myqcd.qcd_rules` provides symbolic QCD propagators, Ward identities, the
three-gluon Lorentz tensor and a vertex/dimension catalog in four Euclidean
dimensions.

## Propagators

$$
S_q(p)=\frac{m-i p\!\!/}{p^2+m^2},
$$

$$
D^{ab}_{\mu\nu}(p)
=\delta^{ab}\left[
\frac{\delta_{\mu\nu}}{p^2}
-(1-\xi)\frac{p_\mu p_\nu}{p^4}
\right],
\qquad
D^{ab}_{c}(p)=\frac{\delta^{ab}}{p^2}.
$$

The quark propagator satisfies
$(m+i p\!\!/)S_q(p)=1$. The massless Ward identity is
$p\!\!/\,p\!\!/=p^2$. The gluon is transverse only in Landau gauge
($\xi=0$):

$$
p_\mu D^{\mu\nu}(p)=\xi\,\frac{p^\nu}{p^2}.
$$

## Vertices

| Vertex | Particles | Color | Lorentz | Coupling | Mass dimension |
|---|---|---|---|---|---|
| q-qbar-g | $q,\bar q,g$ | $T^a_{ij}$ | $\gamma_\mu$ | $g$ | 0 |
| g-g-g | $g,g,g$ | $f^{abc}$ | $(k_1-k_2)_\rho\delta_{\mu\nu}+\cdots$ | $g$ | 1 |
| g-g-g-g | four gluons | $f^{abe}f^{cde}+\cdots$ | $\delta\delta$ permutations | $g^2$ | 0 |
| c-cbar-g | $c,\bar c,g$ | $f^{abc}$ | $k_\mu$ | $g$ | 1 |

The three-gluon tensor is

$$
V_{\mu\nu\rho}(k_1,k_2,k_3)
=(k_1-k_2)_\rho\delta_{\mu\nu}
+(k_2-k_3)_\mu\delta_{\nu\rho}
+(k_3-k_1)_\nu\delta_{\rho\mu}.
$$

## Reproduce

```python
import sympy as sp

from myqcd import lorentz, qcd_rules

p = lorentz.vector_components("p")
m = sp.Symbol("m", positive=True)

assert qcd_rules.quark_propagator_residual(p, m).is_zero_matrix
assert qcd_rules.ward_identity_residual(p).is_zero_matrix
assert all(
    qcd_rules.gluon_transversality(p, nu, gauge_parameter=0) == 0
    for nu in range(4)
)
assert qcd_rules.rule_audit()["vertex_count"] == 4
print(qcd_rules.propagator_mass_dimensions())
```

## Comparison with standard dimensions

| Object | MyQCD | Standard |
|---|---|---|
| Quark propagator dimension | $-1$ | $-1$ |
| Gluon/ghost propagator dimension | $-2$ | $-2$ |
| q-qbar-g vertex dimension | $0$ | $0$ |
| Three-gluon vertex dimension | $1$ | $1$ |
| Four-gluon vertex dimension | $0$ | $0$ |

These are mass dimensions in four dimensions. The catalog is structural:
it does not compute loop integrals or symmetry factors.

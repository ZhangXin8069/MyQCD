# Conventions

## Gamma matrices

| Index | Meaning |
|---|---|
| `gamma(0)` | identity sentinel |
| `gamma(1..4)` | x, y, z, t in the DR basis |
| `gamma(5)` | $\gamma_5=\mathrm{diag}(1,1,-1,-1)$ |
| `gamma(6..15)` | products used by PyQCD |
| `gamma(16,17)` | $\gamma_3\gamma_1(1\pm\gamma_4)/2$ |

Clifford: $\{\gamma_\mu,\gamma_\nu\}=2\delta_{\mu\nu}$.
Charge conjugation: $C=\gamma_4\gamma_2$.

## Color

Hermitian generators $T^a=\lambda^a/2$,

$$
\mathrm{Tr}[T^aT^b]=\frac12\delta^{ab},
\qquad
[T^a,T^b]=if^{abc}T^c.
$$

The historical derivations in `myqcd.derivations` use the anti-Hermitian
normalization $-\frac12\delta^{ab}$; do not mix the two layers.

## Metric and epsilon

Euclidean $\delta_{\mu\nu}$, $\varepsilon_{0123}=+1$,
$\sum\varepsilon^2=24$.

## Operators

$$
\dim(\bar q\Gamma q)=3,\qquad
\dim(\bar q\Gamma D^nq)=3+n.
$$

Parity is $\gamma_4\Gamma\gamma_4=s\Gamma$; charge conjugation is
$C^{-1}\Gamma C=s\Gamma$.

## Diagrams

$L=E_{\mathrm{int}}-V+C$; external-leg edges (endpoint $-1$) are excluded
from $E_{\mathrm{int}}$.

## Lattice

Momenta $p_\mu=2\pi n_\mu/L_\mu$; dispersion
$\hat p^2=4a^{-2}\sum\sin^2(p_\mu a/2)$.

## Evidence boundary

All statements above are exact algebraic conventions. Loop integrals,
ensembles and continuum limits are separate.

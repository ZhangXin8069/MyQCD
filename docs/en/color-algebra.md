# Color algebra

`myqcd.color_traces` collects the SU(3) trace, contraction and Casimir
identities used by the operator and diagram layers.

## Generator traces

With $T^a=\lambda^a/2$ and $\mathrm{Tr}[T^aT^b]=\delta^{ab}/2$,

$$
\mathrm{Tr}[T^aT^bT^c]
=\frac14\left(d^{abc}+i f^{abc}\right),
$$

$$
\mathrm{Tr}[T^aT^bT^cT^d]
=\frac{1}{4N}\left(\delta^{ab}\delta^{cd}
-\delta^{ac}\delta^{bd}+\delta^{ad}\delta^{bc}\right)
+\cdots
$$

The four-generator trace is evaluated exactly from the explicit Gell-Mann
matrices, so no convention-dependent closed form is assumed.

## f/d contractions and Casimirs

$$
\sum_e f^{abe}f^{cde},\qquad
\sum_e d^{abe}d^{cde},\qquad
\sum_e f^{abe}d^{cde}
$$

are exposed directly. For SU($N$),

$$
C_F=\frac{N^2-1}{2N},\qquad C_A=N,\qquad T_F=\frac12.
$$

| Quantity | SU(3) value |
|---|---|
| $C_F$ | $4/3$ |
| $C_A$ | $3$ |
| $T_F$ | $1/2$ |
| $f_{123}$ | $1$ |
| $f_{147}$ | $1/2$ |
| $f_{458}$ | $\sqrt3/2$ |
| $d_{118}$ | $1/\sqrt3$ |
| $\sum f^2$ | $24$ |
| $\sum d^2$ | $40/3$ |

## Reproduce

```python
import sympy as sp

from myqcd import color_traces

assert color_traces.trace_two(1, 1) == sp.Rational(1, 2)
assert color_traces.trace_three(1, 2, 3) == sp.I / 4
assert color_traces.f_contract(1, 2, 1, 2) == 1
assert color_traces.jacobi_residual(1, 2, 3, 4) == 0
assert color_traces.casimir_generic(3)["C_F"] == sp.Rational(4, 3)
assert color_traces.su3_casimirs()["C_A"] == 3
print(color_traces.trace_table()[0])
```

## Comparison

The trace and contraction values agree with the standard Hermitian Gell-Mann
conventions. The historical SU(3) derivations in `myqcd.derivations` use the
anti-Hermitian normalization $-\delta^{ab}/2$ and must not be mixed with this
module.

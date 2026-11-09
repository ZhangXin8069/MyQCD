# Gamma traces

`myqcd.gamma_traces` provides $\gamma_5$ traces, chiral projector traces and
the epsilon correspondence in the PyQCD DeGrand--Rossi basis.

## Four-gamma gamma5 trace

With $\gamma_5=\gamma_1\gamma_2\gamma_3\gamma_4$,

$$
\mathrm{Tr}\left[\gamma_5\gamma_\mu\gamma_\nu
\gamma_\rho\gamma_\sigma\right]
=4\,\varepsilon_{\mu\nu\rho\sigma},
$$

where the indices are mapped from $1,\dots,4$ to $0,\dots,3$. Traces with
fewer than four gamma matrices vanish; longer chains are evaluated from the
explicit $4\times4$ matrices.

## Chiral projectors

$$
P_{L,R}=\frac{1\mp\gamma_5}{2},
\qquad
\mathrm{Tr}[P_L]=\mathrm{Tr}[P_R]=2,
\qquad
\mathrm{Tr}[P_LP_R]=0.
$$

## Reproduce

```python
from myqcd import gamma_traces

assert gamma_traces.trace_gamma5((1, 2, 3, 4)) == 4
assert gamma_traces.trace_gamma5((2, 1, 3, 4)) == -4
assert gamma_traces.trace_gamma5((1, 2, 3)) == 0
assert gamma_traces.trace_gamma5_four_residual() == 0
assert gamma_traces.trace_projector_orthogonality()["Tr[P_L]"] == 2
assert gamma_traces.trace_left_projector() == 2
assert gamma_traces.trace_right_projector() == 2
print(gamma_traces.trace_gamma5_table())
```

## Comparison

| Identity | MyQCD | Standard |
|---|---|---|
| $\mathrm{Tr}[\gamma_5\gamma_1\gamma_2\gamma_3\gamma_4]$ | $4$ | $4\varepsilon_{1234}$ |
| $\mathrm{Tr}[\gamma_5\gamma_\mu\gamma_\nu]$ | $0$ | $0$ |
| $\mathrm{Tr}[P_L]$ | $2$ | $D/2$ |
| $\mathrm{Tr}[P_R]$ | $2$ | $D/2$ |
| $\{ \gamma_5,\gamma_\mu\}$ | $0$ | $0$ |

The overall sign of the epsilon trace is tied to the Euclidean convention
$\varepsilon_{0123}=+1$ and the DR basis; it is not a scheme-independent
Minkowski statement.

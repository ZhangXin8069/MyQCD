# Reference values

All values below are exact results or standard conventions used by the
package.

## Dirac

| Quantity | Value |
|---|---|
| $\mathrm{Tr}[1]$ | 4 |
| $\mathrm{Tr}[\gamma_\mu\gamma_\nu]$ | $4\delta_{\mu\nu}$ |
| $\mathrm{Tr}[\gamma_1\gamma_1]$ | 4 |
| $\mathrm{Tr}[\gamma_1\gamma_2]$ | 0 |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_3\gamma_4]$ | 0 |
| $\mathrm{Tr}[\gamma_5\gamma_1\gamma_2\gamma_3\gamma_4]$ | 4 |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_1\gamma_2]$ | $-4$ |
| $\mathrm{Tr}[\gamma_1\gamma_2\gamma_2\gamma_1]$ | 4 |
| $\gamma_5^2$ | 1 |
| $\{\gamma_5,\gamma_\mu\}$ | 0 |
| $C\gamma_\mu C^{-1}$ | $-\gamma_\mu^T$ |

## SU(3)

| Quantity | Value |
|---|---|
| $C_F$ | $4/3$ |
| $C_A$ | 3 |
| $T_F$ | $1/2$ |
| $f_{123}$ | 1 |
| $f_{147}$ | $1/2$ |
| $f_{458}$ | $\sqrt3/2$ |
| $d_{118}$ | $1/\sqrt3$ |
| $d_{146}$ | $1/2$ |
| $\sum f^2$ | 24 |
| $\sum d^2$ | $40/3$ |
| $\mathrm{Tr}[T^aT^b]$ | $\frac12\delta^{ab}$ |

## Lorentz

| Quantity | Value |
|---|---|
| $\sum\varepsilon^2$ | 24 |
| $\varepsilon_{\mu\nu\rho\sigma}\varepsilon_{\alpha\beta\rho\sigma}$ | $2(\delta_{\mu\alpha}\delta_{\nu\beta}-\delta_{\mu\beta}\delta_{\nu\alpha})$ |
| $T_{\mu\nu}$ trace | 3 |
| $P^{(2)}$ dimension | 5 |

## QCD dimensions

| Object | Dimension |
|---|---|
| Quark propagator | $-1$ |
| Gluon/ghost propagator | $-2$ |
| q-qbar-g vertex | 0 |
| Three-gluon vertex | 1 |
| Four-gluon vertex | 0 |

## Operator dimensions

| Derivatives | Dimension |
|---|---|
| 0 | 3 |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

## Diagram loop numbers

| Diagram | $V$ | $E_{\mathrm{int}}$ | $C$ | $L$ |
|---|---|---|---|---|
| chain | 3 | 2 | 1 | 0 |
| triangle | 3 | 3 | 1 | 1 |
| self-energy | 2 | 2 | 1 | 1 |
| sunset | 2 | 3 | 1 | 2 |

These values are checked by `python -m myqcd.operator_audit`.

# 参考值

以下都是精确结果或本包使用的标准约定。

## Dirac

| 量 | 值 |
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

| 量 | 值 |
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

| 量 | 值 |
|---|---|
| $\sum\varepsilon^2$ | 24 |
| $\varepsilon_{\mu\nu\rho\sigma}\varepsilon_{\alpha\beta\rho\sigma}$ | $2(\delta_{\mu\alpha}\delta_{\nu\beta}-\delta_{\mu\beta}\delta_{\nu\alpha})$ |
| $T_{\mu\nu}$ 的迹 | 3 |
| $P^{(2)}$ 维数 | 5 |

## QCD 量纲

| 对象 | 量纲 |
|---|---|
| 夸克传播子 | $-1$ |
| 胶子/鬼传播子 | $-2$ |
| q-qbar-g 顶点 | 0 |
| 三胶子顶点 | 1 |
| 四胶子顶点 | 0 |

## 算符量纲

| 导数 | 量纲 |
|---|---|
| 0 | 3 |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

## 图圈数

| 图 | $V$ | $E_{\mathrm{int}}$ | $C$ | $L$ |
|---|---|---|---|---|
| 链 | 3 | 2 | 1 | 0 |
| 三角 | 3 | 3 | 1 | 1 |
| 自能 | 2 | 2 | 1 | 1 |
| sunset | 2 | 3 | 1 | 2 |

这些值由 `python -m myqcd.operator_audit` 检查。

# Gamma 迹

`myqcd.gamma_traces` 提供 PyQCD DeGrand--Rossi 基中的 $\gamma_5$ 迹、
手征投影迹与 epsilon 对应关系。

## 四个 gamma 的 γ5 迹

取 $\gamma_5=\gamma_1\gamma_2\gamma_3\gamma_4$，

$$
\mathrm{Tr}\left[\gamma_5\gamma_\mu\gamma_\nu
\gamma_\rho\gamma_\sigma\right]
=4\,\varepsilon_{\mu\nu\rho\sigma},
$$

指标从 $1,\dots,4$ 映射到 $0,\dots,3$。少于四个 gamma 的迹为零；更长
的链由显式 $4\times4$ 矩阵计算。

## 手征投影

$$
P_{L,R}=\frac{1\mp\gamma_5}{2},
\qquad
\mathrm{Tr}[P_L]=\mathrm{Tr}[P_R]=2,
\qquad
\mathrm{Tr}[P_LP_R]=0.
$$

## 复现

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

## 比对

| 恒等式 | MyQCD | 标准 |
|---|---|---|
| $\mathrm{Tr}[\gamma_5\gamma_1\gamma_2\gamma_3\gamma_4]$ | $4$ | $4\varepsilon_{1234}$ |
| $\mathrm{Tr}[\gamma_5\gamma_\mu\gamma_\nu]$ | $0$ | $0$ |
| $\mathrm{Tr}[P_L]$ | $2$ | $D/2$ |
| $\mathrm{Tr}[P_R]$ | $2$ | $D/2$ |
| $\{ \gamma_5,\gamma_\mu\}$ | $0$ | $0$ |

epsilon 迹的整体符号绑定 Euclidean 约定 $\varepsilon_{0123}=+1$ 与
DR 基；它不是与方案无关的 Minkowski 陈述。

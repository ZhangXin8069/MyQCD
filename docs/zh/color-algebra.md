# 颜色代数

`myqcd.color_traces` 汇总算符层与图层使用的 SU(3) 迹、缩并与 Casimir
恒等式。

## 生成元迹

取 $T^a=\lambda^a/2$、$\mathrm{Tr}[T^aT^b]=\delta^{ab}/2$，

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

四生成元迹由显式 Gell-Mann 矩阵精确计算，不依赖某个约定相关的闭式。

## f/d 缩并与 Casimir

$$
\sum_e f^{abe}f^{cde},\qquad
\sum_e d^{abe}d^{cde},\qquad
\sum_e f^{abe}d^{cde}
$$

直接提供。对 SU($N$)，

$$
C_F=\frac{N^2-1}{2N},\qquad C_A=N,\qquad T_F=\frac12.
$$

| 量 | SU(3) 值 |
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

## 复现

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

## 比对

迹与缩并值采用标准厄米 Gell-Mann 约定。`myqcd.derivations` 中的历史
SU(3) 推导使用反厄米归一化 $-\delta^{ab}/2$，不可与本模块混用。

# 匹配

`myqcd.matching` 汇总树级匹配系数、Fourier 前因子与 TMD 匹配使用的
hybrid 开关。

## 树级

对双线性基，树级匹配为

$$
C_\Gamma^{(0)}=1,
\qquad
\mathcal{O}_\Gamma^{\mathrm{MS}}=
\mathcal{O}_\Gamma^{\mathrm{lattice}}+\cdots
$$

本包检查系数与卷积前因子；不推导圈阶匹配核。

## Hybrid 开关

光滑开关为

$$
f(x;x_0,w)=\frac{1}{1+e^{-(x-x_0)/w}},
\qquad
f(x_0)=\frac12.
$$

中点残差被精确检查。

## 复现

```python
import sympy as sp

from myqcd import matching

assert matching.tree_level_matching("S") == 1
assert matching.hybrid_continuity_residual() == 0
assert matching.matching_residual(2, 4, sp.Rational(1, 2)) == 0
assert matching.fourier_prefactor() == 1 / sp.pi
print(matching.matching_table(("S", "V")))
```

## 边界

树级系数是约定，不是一圈结果。Hybrid 开关是平滑函数；它在匹配公式中的
实现需要独立推导。

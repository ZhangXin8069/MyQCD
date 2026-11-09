# 重正化

`myqcd` 提供双线性重正化的代数部件：Dirac 投影器、颜色迹、算符量纲与
混合矩阵。它不计算圈积分，也不对真实系综拟合 Z 因子。

## RI/MOM 条件

对截肢顶点 $\Lambda_\Gamma(p)$ 与投影器 $P_\Gamma$，在 $p^2=\mu^2$ 处的
RI/MOM 条件示意为

$$
Z_\Gamma\,
\mathrm{Tr}\left[P_\Gamma\Lambda_\Gamma(p)\right]_{p^2=\mu^2}
=
\mathrm{Tr}\left[P_\Gamma\Lambda_\Gamma^{(0)}(p)\right]_{p^2=\mu^2}.
$$

树级顶点就是 Dirac 矩阵本身。这里使用的投影器是 16 个双线性
$S,P,V_\mu,A_\mu,T_{\mu\nu}$。

## 投影器归一化

| 结构 | 矩阵 | 树级迹 |
|---|---|---|
| $S$ | $1$ | $4$ |
| $P$ | $\gamma_5$ | $4$ |
| $V_\mu$ | $\gamma_\mu$ | $4$ |
| $A_\mu$ | $\gamma_\mu\gamma_5$ | $4$ |
| $T_{\mu\nu}$ | $\sigma_{\mu\nu}$ | $4$ |

在 Euclidean 基中张量基的 Gram 符号为负；投影器归一化必须使用对应的
$g_A$ 因子，不能假定所有迹都是 $+4$。

## 混合矩阵

一组算符 $\mathcal{O}_i$ 的重正化为

$$
\mathcal{O}_i^{R}
=\sum_j Z_{ij}\mathcal{O}_j .
$$

代数层可以检查给定 $Z$ 矩阵可逆、树级 $Z^{(0)}=1$；它不推导圈阶系数。

## 复现

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

## 边界

本包不声称完成完整 RI/MOM 分析：圈积分、带外线旋量的投影器、微扰匹配核
与连续极限外推属于独立任务。

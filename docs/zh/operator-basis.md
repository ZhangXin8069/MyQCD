# 算符基

`myqcd.operator_basis` 在 16 个 Dirac 双线性上增加导数计数、颜色表示、
手征组合与 Fierz 重排。结构为

$$
\mathcal{O}_{\Gamma}^{(n)}
=\bar q\,\Gamma\,D^{(n)}q,
\qquad
\dim\mathcal{O}=3+n.
$$

## 导数算符

`DerivativeOperator` 保存 Dirac 结构、导数阶数、颜色表示与味标签。
`mass_dimension` 为 $3+n$；`parity_sign` 与
`charge_conjugation_sign` 继承零导数双线性。该类型不建模对称化、
无迹化或运动方程约化。

| 导数 $n$ | 质量量纲 |
|---|---|
| 0 | 3 |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

## 手征组合

取 $P_{L,R}=(1\mp\gamma_5)/2$，

$$
V_\mu\pm A_\mu
=\gamma_\mu(1\pm\gamma_5)
=2\gamma_\mu P_{R,L}.
$$

投影恒等式 $P_L^2=P_L$、$P_R^2=P_R$、$P_LP_R=0$ 与
$P_L+P_R=1$ 都被精确检查。

## 颜色表示

单态双线性的颜色因子为 $1$；八重态为 $T^a$（$a=1,\dots,8$）。
指标显式保留，便于单独审计颜色缩并。

## 复现

```python
import sympy as sp

from myqcd import operator_basis

operators_list = operator_basis.enumerate_derivative_operators(
    ("u", "d"), max_derivatives=2, colors=("singlet", "octet")
)
assert len(operators_list) == 384

operator = operator_basis.DerivativeOperator(
    "O_twist2", "V3", derivatives=2, color="octet"
)
assert operator.mass_dimension == 5
assert operator.pyqcd_gamma_index == 3
assert operator.label == "V"

assert all(operator_basis.chiral_projector_identities().values())
assert operator_basis.color_factor("octet", 3) == "T^3"

terms = operator_basis.fierz_rearrangement("S", "V1")
assert terms
print(len(terms), operator_basis.color_factor("singlet"))
```

## 与标准计数比对

| 项 | MyQCD | 标准 |
|---|---|---|
| Dirac 双线性数 | 16 | $1+1+4+4+6$ |
| 结构 × 导数 × 味 × 颜色 | $16\times(n+1)\times N_f^2\times2$ | 相同 |
| $n=2$、$N_f=2$、两种颜色 | 384 | 384 |
| $n$ 阶导数的质量量纲 | $3+n$ | $3+n$ |

这是组合计数；不声称所有算符在运动方程或 Fierz 恒等式之后仍然独立。

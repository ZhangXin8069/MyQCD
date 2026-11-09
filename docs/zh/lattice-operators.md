# 格点算符

格点算符构建组合 Dirac 结构、颜色、规范链接与位移。`myqcd` 提供精确的
代数部件；规范场数组与张量收缩属于 PyQCD 的数值层。

## Wilson 线

从 $x$ 到 $y$ 的直线 Wilson 线为

$$
W(x,y)=\prod_{s\in\text{path}}U_\mu(s),
$$

变换为 $U_\mu(x)\mapsto G(x)U_\mu(x)G^\dagger(x+\hat\mu)$。带 Wilson 线的
双线性为

$$
\mathcal{O}_{\Gamma}(x;z)
=\bar q(x)\,\Gamma\,W(x,x+z)\,q(x+z).
$$

## Clover 与 staple

Clover 场强为

$$
F_{\mu\nu}(x)=\frac{-i}{8}\sum_{\pm}
\left(P_{\mu\nu}(x)-P_{\mu\nu}^\dagger(x)\right),
$$

staple 算符使用三段路径
$-L\hat z\to b\hat b\to(L+z)\hat z$。这些是 PyQCD 胶子 OPE 与 TMD 层使用
的结构。

## 量子数

| 算符 | 结构 | 导数 | 宇称 | C | PyQCD 索引 |
|---|---|---|---|---|---|
| $\bar q\gamma_5q$ | `P` | 0 | $-1$ | $+1$ | 5 |
| $\bar q\gamma_4q$ | `V4` | 0 | $+1$ | $-1$ | 4 |
| $\bar q\gamma_4\gamma_5q$ | `A4` | 0 | $-1$ | $-1$ | 15 |
| $\bar q\gamma_3D_\mu q$ | `V3` | 1 | $-1$ | $+1$ | 3 |

## 复现

```python
import sympy as sp

from myqcd import gamma, operator_basis, operators

pion = operators.BilinearOperator("O_pi", "u", "d", "P")
assert pion.parity_sign == -1
assert pion.charge_conjugation_sign == 1
assert pion.pyqcd_gamma_index == 5

twist = operator_basis.DerivativeOperator(
    "O_twist", "V3", derivatives=1, color="octet"
)
assert twist.mass_dimension == 4
assert twist.pyqcd_gamma_index == 3
assert all(operator_basis.chiral_projector_identities().values())
print(pion.latex(), twist.latex())
```

## 边界

代数检查不证明某个格点离散化的规范不变性。路径排序、链接涂抹、Clover
改进与梯度流重正化需要数值实现及其独立测试。

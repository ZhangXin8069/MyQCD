# QCD 拉氏量

带规范固定与鬼场的 Euclidean QCD 拉氏量为

$$
\mathcal{L}
=-\frac14 F^a_{\mu\nu}F^a_{\mu\nu}
+\bar\psi\left(\gamma_\mu D_\mu+m\right)\psi
+\frac{1}{2\xi}\left(\partial_\mu A^a_\mu\right)^2
+\bar c^a\left(-\partial_\mu D^{ab}_\mu\right)c^b,
$$

其中

$$
D_\mu=\partial_\mu-igT^aA^a_\mu,
\qquad
F^a_{\mu\nu}=\partial_\mu A^a_\nu-\partial_\nu A^a_\mu
+gf^{abc}A^b_\mu A^c_\nu.
$$

## 展开得到的顶点

| 项 | 顶点 | 耦合 |
|---|---|---|
| $\bar\psi\gamma_\mu T^aA^a_\mu\psi$ | q-qbar-g | $g$ |
| $gf^{abc}(\partial A)AA$ | g-g-g | $g$ |
| $g^2f^{abe}f^{cde}A A A A$ | g-g-g-g | $g^2$ |
| $\bar c\,\partial_\mu( gT^aA^a_\mu)c$ | c-cbar-g | $g$ |

顶点因子与质量量纲由 `myqcd.qcd_rules` 提供。

## 复现代数检查

```python
import sympy as sp

from myqcd import qcd_rules

p = (sp.Symbol("p0"), sp.Symbol("p1"), sp.Symbol("p2"), sp.Symbol("p3"))
assert qcd_rules.ward_identity_residual(p).is_zero_matrix
assert qcd_rules.rule_audit()["vertex_count"] == 4
print(qcd_rules.propagator_mass_dimensions())
```

## 边界

以上拉氏量固定 Euclidean 符号约定。不同 Minkowski 约定会改变整体符号；
圈积分、规范依赖与 BRST 上同调不在本页范围。

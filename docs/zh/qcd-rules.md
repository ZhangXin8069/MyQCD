# QCD 费曼规则

`myqcd.qcd_rules` 提供四维 Euclidean 约定下的符号 QCD 传播子、Ward 恒等式、
三胶子 Lorentz 张量以及顶点/量纲清单。

## 传播子

$$
S_q(p)=\frac{m-i p\!\!/}{p^2+m^2},
$$

$$
D^{ab}_{\mu\nu}(p)
=\delta^{ab}\left[
\frac{\delta_{\mu\nu}}{p^2}
-(1-\xi)\frac{p_\mu p_\nu}{p^4}
\right],
\qquad
D^{ab}_{c}(p)=\frac{\delta^{ab}}{p^2}.
$$

夸克传播子满足 $(m+i p\!\!/)S_q(p)=1$。无质量 Ward 恒等式为
$p\!\!/\,p\!\!/=p^2$。胶子只在 Landau 规范（$\xi=0$）横向：

$$
p_\mu D^{\mu\nu}(p)=\xi\,\frac{p^\nu}{p^2}.
$$

## 顶点

| 顶点 | 粒子 | 颜色 | Lorentz | 耦合 | 质量量纲 |
|---|---|---|---|---|---|
| q-qbar-g | $q,\bar q,g$ | $T^a_{ij}$ | $\gamma_\mu$ | $g$ | 0 |
| g-g-g | $g,g,g$ | $f^{abc}$ | $(k_1-k_2)_\rho\delta_{\mu\nu}+\cdots$ | $g$ | 1 |
| g-g-g-g | 四胶子 | $f^{abe}f^{cde}+\cdots$ | $\delta\delta$ 置换 | $g^2$ | 0 |
| c-cbar-g | $c,\bar c,g$ | $f^{abc}$ | $k_\mu$ | $g$ | 1 |

三胶子张量为

$$
V_{\mu\nu\rho}(k_1,k_2,k_3)
=(k_1-k_2)_\rho\delta_{\mu\nu}
+(k_2-k_3)_\mu\delta_{\nu\rho}
+(k_3-k_1)_\nu\delta_{\rho\mu}.
$$

## 复现

```python
import sympy as sp

from myqcd import lorentz, qcd_rules

p = lorentz.vector_components("p")
m = sp.Symbol("m", positive=True)

assert qcd_rules.quark_propagator_residual(p, m).is_zero_matrix
assert qcd_rules.ward_identity_residual(p).is_zero_matrix
assert all(
    qcd_rules.gluon_transversality(p, nu, gauge_parameter=0) == 0
    for nu in range(4)
)
assert qcd_rules.rule_audit()["vertex_count"] == 4
print(qcd_rules.propagator_mass_dimensions())
```

## 与标准量纲比对

| 对象 | MyQCD | 标准 |
|---|---|---|
| 夸克传播子量纲 | $-1$ | $-1$ |
| 胶子/鬼传播子量纲 | $-2$ | $-2$ |
| q-qbar-g 顶点量纲 | $0$ | $0$ |
| 三胶子顶点量纲 | $1$ | $1$ |
| 四胶子顶点量纲 | $0$ | $0$ |

以上是四维质量量纲。该清单是结构性的：不做圈积分或对称因子推导。

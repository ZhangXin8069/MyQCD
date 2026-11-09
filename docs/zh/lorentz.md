# Lorentz 代数

`myqcd.lorentz` 提供四维 Euclidean 张量代数：度规、Levi-Civita 张量、缩并、
Schouten 恒等式以及横向/spin-2 投影。所有恒等式都是 SymPy 精确表达式。

## 度规与 epsilon

$$
\delta_{\mu\nu}=\mathrm{diag}(1,1,1,1),\qquad
\varepsilon_{0123}=+1.
$$

基本缩并：

$$
\sum_{\mu\nu\rho\sigma}\varepsilon_{\mu\nu\rho\sigma}^2=24,
$$

$$
\sum_{\rho\sigma}\varepsilon_{\mu\nu\rho\sigma}
\varepsilon_{\alpha\beta\rho\sigma}
=2\left(\delta_{\mu\alpha}\delta_{\nu\beta}
-\delta_{\mu\beta}\delta_{\nu\alpha}\right),
$$

全缩并等于 Kronecker delta 的行列式。四维 Schouten 恒等式恒为零：

$$
\varepsilon_{abcd}p_e+\varepsilon_{bcde}p_a
+\varepsilon_{cdea}p_b+\varepsilon_{deab}p_c
+\varepsilon_{eabc}p_d=0.
$$

## 投影算子

当 $p^2\neq0$ 时，横向与纵向投影为

$$
T_{\mu\nu}=\delta_{\mu\nu}-\frac{p_\mu p_\nu}{p^2},
\qquad
L_{\mu\nu}=\frac{p_\mu p_\nu}{p^2},
\qquad
T_{\mu\nu}+L_{\mu\nu}=\delta_{\mu\nu}.
$$

横向无迹 spin-2 投影为

$$
P^{(2)}_{\mu\nu\rho\sigma}
=\frac12\left(T_{\mu\rho}T_{\nu\sigma}+T_{\mu\sigma}T_{\nu\rho}\right)
-\frac13 T_{\mu\nu}T_{\rho\sigma}.
$$

在四维中它投影到五个横向无迹极化；单对指标的迹为零。

## 复现

```python
import sympy as sp

from myqcd import lorentz

p = lorentz.vector_components("p")

assert lorentz.epsilon_square() == 24
assert lorentz.epsilon_two_contract_residual() == 0
assert lorentz.schouten_residual(p) == 0
assert lorentz.spin2_dimension(p) == 5
assert lorentz.spin2_traceless_check(p) == 0

def projector(mu, nu):
    return lorentz.transverse_projector(p, mu, nu)

assert sp.simplify(
    sum(projector(0, nu) * projector(nu, 2) for nu in range(4))
    - projector(0, 2)
) == 0
print(lorentz.epsilon_two_contract(0, 1, 0, 1))
```

## 与标准值比对

| 量 | MyQCD | 标准值 |
|---|---|---|
| $\sum\varepsilon^2$ | $24$ | $4!$ |
| $\varepsilon_{\mu\nu\rho\sigma}\varepsilon_{\alpha\beta\rho\sigma}$ | $2(\delta_{\mu\alpha}\delta_{\nu\beta}-\delta_{\mu\beta}\delta_{\nu\alpha})$ | 相同 |
| $\delta_{\mu\nu}T_{\mu\nu}$ | $3$ | $D-1$ |
| $\sum_{\mu\nu}P^{(2)}_{\mu\nu\mu\nu}$ | $5$ | $(D-1)D/2-1$ |

维数对应 $D-1=3$ 维空间中的对称无迹二阶张量。

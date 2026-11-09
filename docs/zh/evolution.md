# 演化

`myqcd.evolution` 实现单指数 RGE 解

$$
Z(\mu)=\left(\frac{\mu}{\mu_0}\right)^{-\gamma},
\qquad
\gamma=-\frac{d\log Z}{d\log\mu}.
$$

对对角反常维度矩阵，演化矩阵是对角的；非对角混合需要矩阵指数，不在本
辅助层内。

## 复现

```python
import sympy as sp

from myqcd import evolution

mu = sp.Symbol("mu", positive=True)
mu0 = sp.Symbol("mu0", positive=True)

z = evolution.solve_z(mu, mu0, 1)
assert sp.simplify(z - mu0 / mu) == 0
assert evolution.evolution_residual(3, 1, mu0, mu) == 0
assert sp.simplify(
    evolution.anomalous_dimension_from_z(z, mu) - 1
) == 0
print(evolution.evolution_table())
```

## 比对

| 输入 | 演化因子 |
|---|---|
| $\gamma=0$ | 1 |
| $\gamma=1$ | $\mu_0/\mu$ |
| $\gamma=-1$ | $\mu/\mu_0$ |

符号约定由上式计算固定；换约定会改变指数符号。

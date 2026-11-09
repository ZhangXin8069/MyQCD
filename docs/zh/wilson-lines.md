# Wilson 线

`myqcd.wilson` 提供符号 Wilson 路径乘积与 3x3 链接的规范协变检查。它存储
矩阵，不存储规范场数组。

## 路径乘积

$$
W(x,y)=U_0U_1\cdots U_{n-1}.
$$

规范变换下，

$$
U_i\mapsto G_iU_iG_{i+1}^\dagger,
\qquad
W\mapsto G_0WG_n^\dagger.
$$

dagger 路径反转链接并对每个链接取厄米共轭：
$W^\dagger=U_{n-1}^\dagger\cdots U_0^\dagger$。

## Staple

三段 staple 描述为

$$
(-L\hat z,\; b\hat b,\; (L+z)\hat z).
$$

`staple_descriptors(z,b,L)` 返回这些方向/长度对。

## 复现

```python
import sympy as sp

from myqcd import wilson

links = (sp.diag(1, 1, -1), sp.diag(-1, 1, 1))
path = wilson.straight_path(links)
assert path.product() == links[0] * links[1]
assert path.dagger().product() == path.product().H

angles = (sp.Rational(1, 5), sp.Rational(2, 5), sp.Rational(3, 5))
gauges = tuple(
    wilson.unitary_phases(
        (sp.Rational(index, 7), sp.Rational(index + 1, 7), sp.Rational(index + 2, 7))
    )
    for index in range(4)
)
assert wilson.covariance_residual(links, gauges[:3]).is_zero_matrix
print(wilson.staple_descriptors(2, 1, 5))
```

## 边界

本模块检查代数路径乘积与协变性；不读取 ILDG 组态、不涂抹链接、不做
格点收缩。

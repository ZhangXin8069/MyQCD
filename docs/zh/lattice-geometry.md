# 格点几何

`myqcd.lattice` 提供整数指标动量、Fourier 相位、格点色散与小规模动量枚举。

## 动量与相位

对格点尺寸 $L_\mu$ 与整数指标 $n_\mu$，

$$
p_\mu=\frac{2\pi n_\mu}{L_\mu},
\qquad
e^{-ip\cdot x}.
$$

格距为 $a$ 的格点色散为

$$
\hat p^2=\frac{4}{a^2}\sum_\mu\sin^2\left(\frac{p_\mu a}{2}\right),
$$

当 $p_\mu a\ll1$ 时退化为 $\sum_\mu p_\mu^2$。

## 复现

```python
import math

from myqcd import lattice

p = lattice.momentum_from_indices((1, 0, 0, 0), (4, 4, 4, 8))
assert p[0] == math.pi / 2
phase = lattice.fourier_phase((math.pi / 2, 0, 0, 0), (1, 0, 0, 0))
assert abs(phase - (-1j)) < 1e-12
assert lattice.lattice_dispersion((0.1, 0.2)) > 0
assert lattice.lattice_dispersion((0.0, 0.0)) == 0
momenta = lattice.spatial_momenta((4, 4), max_index=1)
assert len(momenta) == 9
print(lattice.momentum_permutations((1.0, 0.0, 0.0)))
```

## 与连续极限比对

| 量 | 格点 | 连续极限 |
|---|---|---|
| 动量 | $2\pi n_\mu/L_\mu$ | 相同 |
| 色散 | $4a^{-2}\sum\sin^2(p_\mu a/2)$ | $\sum p_\mu^2$ |
| 相位 | $e^{-ip\cdot x}$ | 相同 |

色散对照在有限 $a$ 下是精确的；连续表达式只是 $a\to0$ 极限，不是有限格距
下的恒等式。

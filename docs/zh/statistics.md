# 统计

`myqcd.statistics` 仅用标准库实现 jackknife 重采样、确定性 bootstrap 与
有效质量估计。

## Jackknife

对 $N$ 个样本 $x_i$，leave-one-out 估计与均值协方差为

$$
\bar x_{(-i)}=\frac{\sum_j x_j-x_i}{N-1},
\qquad
\widehat{\mathrm{Cov}}
=\frac{N-1}{N}\sum_i
\left(\bar x_{(-i)}-\bar x\right)
\left(\bar x_{(-i)}-\bar x\right)^T.
$$

## Bootstrap 与有效质量

Bootstrap 指标由带种子的 `random.Random` 生成，结果可复现。关联函数的
有效质量为

$$
m_{\mathrm{eff}}(t)=\log\frac{C(t)}{C(t+1)}.
$$

## 复现

```python
import math

from myqcd import statistics

samples = [(1.0, 2.0), (2.0, 4.0), (3.0, 6.0), (4.0, 8.0)]
assert statistics.jackknife_mean(samples) == (2.5, 5.0)
covariance = statistics.jackknife_covariance(samples)
assert covariance[0][0] > 0
assert statistics.bootstrap_indices(4, 5, seed=7) == statistics.bootstrap_indices(4, 5, seed=7)
result = statistics.bootstrap_mean([1.0, 2.0, 3.0, 4.0], 50, seed=3)
assert result["stderr"] >= 0
masses = statistics.effective_mass([math.exp(-t) for t in range(4)])
assert all(abs(mass - 1.0) < 1e-12 for mass in masses)
print(result)
```

## 比对

| 量 | MyQCD | 标准 |
|---|---|---|
| Jackknife 均值 | leave-one-out 均值 | 相同 |
| 协方差因子 | $(N-1)/N$ | 相同 |
| Bootstrap | 带种子重采样 | 相同 |
| 有效质量 | $\log(C_t/C_{t+1})$ | 相同 |

Jackknife 协方差是**均值**的协方差，不是单个组态的协方差。Bootstrap
不能替代真实系综或连续极限外推。

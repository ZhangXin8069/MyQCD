# 图对称性

`myqcd.symmetry` 统计有限图的顶点自同构与平行边交换。它**不**分配物理
对称因子：后者需要全同粒子与顶点交换约定。

## 自同构

若顶点置换保持边多重集（含粒子标签与外部端点 $-1$），则它是自同构。

| 图 | 顶点自同构 | 边交换 |
|---|---|---|
| 四顶点链 | 2 | 1 |
| 三角 | 6 | 1 |
| 自能 | 2 | 1 |
| sunset | 2 | 6 |

sunset 有三条全同内部胶子，因此有 $3!=6$ 的边交换因子。交换两个顶点
也是自同构，因为两条外部腿都是夸克短桩。

## 复现

```python
from myqcd import symmetry, topology

assert symmetry.automorphism_count(topology.build_cycle(3)) == 6
assert symmetry.automorphism_count(topology.build_chain(4)) == 2
assert symmetry.edge_exchange_count(topology.build_sunset()) == 6
print(symmetry.symmetry_table(topology.build_self_energy()))
```

## 为什么物理因子单列

物理对称因子还依赖外线是否可区分、全同顶点如何分组、计数哪些 Wick
收缩。这些约定不在图中，因此上表是组合输入，不是最终因子。

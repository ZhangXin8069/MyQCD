# 图拓扑

`myqcd.topology` 只处理组合图：顶点、内部边、外部腿边与粒子标签。它计算
不变量，并对小图用显式顶点置换判定同构。

## 不变量

对有 $V$ 个顶点、$E_{\mathrm{int}}$ 条内部边、$C$ 个连通分量的图，

$$
L=E_{\mathrm{int}}-V+C,
\qquad
\text{树}\iff E_{\mathrm{int}}=V-C.
$$

单环满足 $V\ge3$、$E_{\mathrm{int}}=V$，且每个顶点度数都是 2。外部腿边
（端点 $-1$）不计入 $E_{\mathrm{int}}$。

## 同构与枚举

`canonical_signature` 在所有顶点重标号下取字典序最小的边签名。
`is_isomorphic` 对不超过 8 个顶点的图穷举置换比较边多重集；更大的图只
使用规范签名，并明确标注限制。

小图枚举结果：

| 顶点数 | 内部边数 | 连通同构类 |
|---|---|---|
| 3 | 3 | 1（三角） |
| 4 | 3 | 2（路径、星形） |
| 4 | 4 | 2（四环、三角带悬挂边） |

## 复现

```python
from myqcd import topology

triangle = topology.build_cycle(3)
chain = topology.build_chain(3)
assert triangle.loop_count == 1
assert topology.is_cycle(triangle)
assert topology.is_tree(chain)
assert not topology.is_isomorphic(triangle, chain)

trees = topology.enumerate_connected_topologies(4, 3)
assert len(trees) == 2
print(topology.topology_table(triangle))
```

## 与标准图论比对

| 量 | MyQCD | 标准 |
|---|---|---|
| 圈数 | $E_{\mathrm{int}}-V+C$ | cycle rank |
| 树判据 | $E_{\mathrm{int}}=V-C$ | forest |
| 环判据 | 度数全为 2，$E_{\mathrm{int}}=V$ | simple cycle |
| 同构 | $V\le8$ 精确 | graph isomorphism |

本模块故意不分配对称因子：它依赖具体图的粒子内容和顶点交换约定。

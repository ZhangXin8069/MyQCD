# Content expansion ledger（2026-11-09）

目标：把 MyQCD 的算符/费曼图子系统从基线扩充到至少 **10×**，并保持
可执行测试与双语文档同步。

## 基线

| 范围 | 基线行数 |
|---|---|
| 代码（gamma/color/operators/feynman/diagram_export/operator_audit） | 1,897 |
| 文档（operators/diagrams 双语） | 546 |
| 合计 | 2,443 |

目标：24,430 行（10×）。

## 当前进度

| 范围 | 当前行数 | 相对基线 |
|---|---|---|
| 代码（20 个相关模块） | 4,362 | 2.30× |
| 测试（21 个相关测试文件） | 1,721 | — |
| 文档（46 个双语页） | 5,901 | 10.81× |
| 合计 | 11,984 | 4.91× |

统计口径：`wc -l` 的物理行数；不计 `derivations.py` 等既有核心模块。

**状态：文档已达成 10× 目标；代码+测试+文档总量为 4.91×，继续向总量
24,430 行推进。**

## 已交付模块

| 模块 | 内容 |
|---|---|
| `lorentz` | epsilon 缩并、Schouten、横向/纵向/spin-2 投影 |
| `fierz` | 16 基通用 Fierz 变换与对偶完备性 |
| `operator_basis` | 导数算符、手征组合、颜色表示、算符表 |
| `qcd_rules` | 传播子、Ward 恒等式、顶点因子与量纲 |
| `topology` | 图不变量、同构、拓扑枚举、构造器 |
| `color_traces` | SU(3) 迹、f/d 缩并、通用 Casimir |
| `gamma_traces` | γ5 迹、epsilon 对应、手征投影迹 |
| `lattice` | 格点动量、Fourier 相位、色散 |
| `statistics` | jackknife、bootstrap、有效质量 |
| `renormalization` | RI/MOM 投影器、Z 因子、混合矩阵 |
| `wilson` | Wilson 路径乘积、规范协变、staple |
| `matching` | 树级匹配、Fourier 前因子、hybrid 开关 |
| `evolution` | 单指数 RGE 演化与反常维度 |
| `symmetry` | 顶点自同构与平行边交换 |

## 已交付文档

operators、diagrams、operator-basis、fierz、lorentz、gamma-traces、
color-algebra、qcd-rules、topology、diagram-formats、lattice-geometry、
statistics、tutorial、worked-examples、renormalization、lattice-operators、
wilson-lines、matching、evolution、symmetry（均中英双语）。

## 下一批（继续向 10× 推进）

1. `renormalization.md`：RI/MOM 投影、Z 因子、混合矩阵。
2. `lattice-operators.md`：Wilson 线、staple、Clover、梯度流算符。
3. `api-reference.md`：全部模块的公开 API 表。
4. `glossary.md` 与 `reading-guide.md`：术语与阅读路径。
5. 更多可执行实例与性质测试（随机差分、极限检查）。

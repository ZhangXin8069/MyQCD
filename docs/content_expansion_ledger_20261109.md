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
| 代码（新增 lorentz/fierz/operator_basis/qcd_rules/topology/color_traces/gamma_traces/lattice/statistics 等） | 3,835 | 2.02× |
| 测试（14 个相关测试文件） | 1,450 | — |
| 文档（14 个双语页） | 2,389 | 4.38× |
| 合计 | 7,674 | 3.14× |

统计口径：`wc -l` 的物理行数；不计 `derivations.py` 等既有核心模块。

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

## 已交付文档

operators、diagrams、operator-basis、fierz、lorentz、gamma-traces、
color-algebra、qcd-rules、topology、diagram-formats、lattice-geometry、
statistics、tutorial、worked-examples（均中英双语）。

## 下一批（继续向 10× 推进）

1. `renormalization.md`：RI/MOM 投影、Z 因子、混合矩阵。
2. `lattice-operators.md`：Wilson 线、staple、Clover、梯度流算符。
3. `api-reference.md`：全部模块的公开 API 表。
4. `glossary.md` 与 `reading-guide.md`：术语与阅读路径。
5. 更多可执行实例与性质测试（随机差分、极限检查）。

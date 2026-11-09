# 概览

`myqcd` 为 MyQCD 使用的格点 QCD 公式提供可执行证据。它把物理报告拆成三层：

- 带明确假设与通过/失败检查的 SymPy 推导；
- 把公式绑定到报告行号的来源注册表；
- 独立的算符构建与费曼图层。

本包不复制 GPL-3.0 或无许可证的上游源码。参考库以只读 Git 子模块引入；
每个实现的恒等式都在测试套件中独立断言。

## 模块表

| 模块 | 作用 |
|---|---|
| `myqcd.audit` | 核心公式检查与论文公式索引 |
| `myqcd.pyqcd_theory_audit` | gamma、顶点、Wilson 线、Clover、ratio 与 TMD 边界审计 |
| `myqcd.derivations` | 格点规范场、梯度流、LaMET、PDF/TMD 与统计的 SymPy 推导 |
| `myqcd.formula_registry` | 公式到来源与推导入口的注册表 |
| `myqcd.latex_inventory` | 论文源文件的显示公式清单 |
| `myqcd.wick` | 精确味道 Wick 配对与 Grassmann 符号 |
| `myqcd.gamma` | DeGrand--Rossi gamma 基、迹定理与 16 个 Dirac 结构 |
| `myqcd.color` | SU(3) 生成元、结构常数、Casimir 与颜色 Fierz 恒等式 |
| `myqcd.operators` | Dirac 双线性分解、宇称/C 分类与 PyQCD 索引映射 |
| `myqcd.feynman` | 图数据结构、QCD 规则清单与 Wick 配对图 |
| `myqcd.diagram_export` | 零依赖 TikZ-Feynman、DOT 与 SVG 导出 |

## 证据边界

`verified` 只覆盖实际检查过的代数、量纲、有限维代理与组合恒等式。
它不声称完成圈积分、非微扰矩阵元、真实系综、GPU 数值、soft/rapidity 闭环
或连续极限。

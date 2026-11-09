# 总览

`myqcd` 是格点 QCD 的精确代数审计层。当前检查点加入算符构建、费曼图结构、
Lorentz 与颜色代数、QCD 规则、格点运动学与统计，并提供双语文档与
PyPI/RTD 交付。

## 模块地图

| 层 | 模块 |
|---|---|
| 表示 | `gamma`、`gamma_traces`、`color`、`color_traces`、`lorentz` |
| 算符 | `operators`、`operator_basis`、`fierz` |
| 图 | `feynman`、`topology`、`diagram_export`、`qcd_rules` |
| 格点 | `lattice`、`statistics`、`wick` |
| 审计 | `operator_audit`、`pyqcd_theory_audit` |
| 核心审计 | `audit`、`derivations`、`formula_registry`、`latex_inventory` |

## 文档地图

| 目标 | 页面 |
|---|---|
| 通过代码学习 | `tutorial`、`worked-examples`、`case-studies` |
| 算符基 | `operators`、`operator-basis`、`operator-catalog`、`lattice-operators` |
| 代数 | `lorentz`、`fierz`、`gamma-traces`、`gamma-catalog`、`color-algebra`、`color-catalog` |
| 规则与图 | `qcd-rules`、`vertex-catalog`、`diagrams`、`diagram-catalog`、`diagram-formats`、`topology` |
| 格点与统计 | `lattice-geometry`、`statistics` |
| 参考 | `api-reference`、`glossary`、`notation`、`conventions`、`reference-values` |
| 运维 | `validation`、`release-checklist`、`troubleshooting`、`migration`、`comparison`、`limitations`、`roadmap` |

## 证据等级

- `verified`：本次会话执行的精确 SymPy 代数或组合。
- `structural`：在声明假设下的代数闭合。
- `inferred`：由显式约定推导。
- `unverified`：需要圈图、系综或连续极限。

## 指标

| 范围 | 行数 |
|---|---|
| 基线算符/图子系统 | 2,443 |
| 当前代码（20 个模块） | 4,362 |
| 当前测试（21 个文件） | 1,721 |
| 当前双语文档（46 页） | 5,901 |
| 文档相对 546 行基线 | 10.81× |
| 代码+测试+文档总量 | 11,984（基线 4.91×） |

行数是 `wc -l` 物理行数，衡量覆盖而非正确性；正确性由测试套件与
48 项算符审计保证。

## 命令

```bash
python -m myqcd.operator_audit
python -m myqcd.pyqcd_theory_audit --root .
python -m pytest
python -m sphinx -b html -W docs/en <output>
python -m sphinx -b html -W docs/zh <output>
```

## 边界

本包不计算圈积分、不拟合系综、不分配对称因子、不做连续极限外推。这些是
独立的数值与唯象任务。

## 下一步

继续补重正化投影器、Wilson 路径代数、显式对称因子约定、匹配核与随机
差分测试。内容台账跟踪目标。

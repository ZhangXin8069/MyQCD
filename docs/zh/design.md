# 设计

`myqcd` 是精确代数审计层。设计显式区分四类边界：表示、算符结构、图组合
与数值系综。

## 分层

| 层 | 模块 | 职责 |
|---|---|---|
| 表示 | `gamma`、`gamma_traces`、`color`、`color_traces`、`lorentz` | 精确矩阵、迹与张量恒等式 |
| 算符 | `operators`、`operator_basis`、`fierz` | 双线性、导数、手征/颜色结构与 Fierz |
| 图 | `feynman`、`topology`、`diagram_export`、`qcd_rules` | 图不变量、规则与导出 |
| 格点 | `lattice`、`statistics`、`wick` | 运动学、重采样与配对 |
| 审计 | `operator_audit`、`pyqcd_theory_audit` | 机器可读检查 |

## 不变量

1. **精确性：** 所有代数结果是 SymPy 表达式，不是浮点近似。
2. **约定固定：** DR gamma 索引、Euclidean 度规、$+1/2$ 颜色归一化与
   $C=\gamma_4\gamma_2$ 都写在公开 docstring 中。
3. **证据边界：** `verified` 只覆盖实际执行的检查；圈积分、系综与连续
   极限是独立任务。
4. **无隐藏依赖：** 算符/图层只依赖 SymPy 与标准库；导出格式是字符串。

## 数据流

```
算符定义
  -> Dirac/颜色/Lorentz 代数
  -> Wick 配对或图
  -> 圈数/拓扑不变量
  -> JSON/Mermaid/LaTeX/TikZ/DOT/SVG
```

审计入口 `python -m myqcd.operator_audit` 覆盖四个阶段并写出 JSON 报告，
不运行外部代码，也不读取系综。

## 非目标

本包不是数值收缩引擎、Mathematica 替代品、圈积分库或拟合框架。这些职责
属于 PyQCD、FeynCalc 或专门数值包。

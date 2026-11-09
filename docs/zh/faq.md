# 常见问题

## `myqcd` 能替代 PyQCD 吗？

不能。PyQCD 是格点 QCD 数值包；`myqcd` 是精确代数审计与算符/图层，引用
PyQCD 作为约定来源。

## 会计算圈积分吗？

不会。它提供传播子、顶点、投影器与代数恒等式；圈积分与系综拟合不在包内。

## 为什么用 Euclidean 约定？

目标是格点 QCD：$\delta_{\mu\nu}$、厄米 gamma 矩阵与
$\varepsilon_{0123}=+1$。Minkowski 符号不同，必须显式转换。

## 为什么某些 Fierz 系数带负号？

Euclidean 下 16 基的 Gram 矩阵并非全正；实现使用对偶基
$\Gamma^A=\Gamma_A/g_A$。符号由分量矩阵恒等式与随机旋量双重检查。

## 为什么 `gamma(0)` 是单位矩阵？

PyQCD 的 DeGrand–Rossi API 把索引 0 当作单位哨兵；时间矩阵是
`gamma(4)`，不是 `gamma(0)`。

## 为什么 `T13` 没有 PyQCD 索引？

PyQCD 中 `gamma(7)=gamma3 gamma1=-sigma13`，没有精确的 `sigma13`
项。映射返回 `None`，不会静默改号。

## 为什么 CLI 会跳过论文清单？

`python -m myqcd` 需要 `refer/papers/INDEX.md`。缺失时核心检查仍运行，
报告 `verified_core_without_inventory`。指定 paper id 或 inventory JSON
时以退出码 2 报错。

## 为什么不自动分配对称因子？

对称因子依赖全同粒子内容与顶点交换约定。`myqcd.topology` 只暴露图
不变量。

## 如何新增算符？

使用 `operators.BilinearOperator` 或
`operator_basis.DerivativeOperator`，并校验 `structure`、`derivatives`、
`color` 与味标签。

## 如何导出图？

用 `diagram_export` 输出 JSON、Mermaid、LaTeX、TikZ、DOT 或 SVG。这些
是结构格式，不调用外部进程。

## 哪些内容不在范围内？

圈积分、非微扰矩阵元、真实系综、GPU 数值、soft/rapidity 重求和、连续
极限外推和完整重正化拟合。

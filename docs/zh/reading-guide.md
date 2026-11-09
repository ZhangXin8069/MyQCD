# 阅读指南

按目标选择路径。

| 目标 | 页面 |
|---|---|
| 构建双线性算符 | `operators`、`operator-basis`、`lattice-operators` |
| 理解 gamma/颜色约定 | `gamma-traces`、`color-algebra`、`lorentz` |
| 复现 Fierz 恒等式 | `fierz`、`worked-examples` |
| 写 QCD 费曼规则 | `qcd-rules`、`diagrams` |
| 画图或导出 | `diagrams`、`diagram-formats`、`topology` |
| 检查格点运动学 | `lattice-geometry`、`statistics` |
| 通过代码学习 | `tutorial`、`worked-examples` |
| 查 API 名称 | `api-reference`、`glossary` |

## 三种阅读顺序

1. **物理优先：** `overview` → `operators` → `operator-basis` → `fierz`
   → `qcd-rules` → `diagrams`。
2. **代码优先：** `tutorial` → `worked-examples` → `api-reference`。
3. **审计优先：** `usage` → `operator_audit` 命令 → `topology` →
   `diagram-formats`。

## 记号

- Euclidean 度规 $\delta_{\mu\nu}$；$\varepsilon_{0123}=+1$。
- DR gamma 索引：$0=I$，$1$–$4$ 为空间/时间，$5=\gamma_5$。
- 双线性质量量纲为 $3$；每个导数加 $1$。
- $L=E_{\mathrm{int}}-V+C$ 为圈数。

## 边界

本库是**精确代数审计层**，不是数值格点系综、圈积分包或连续极限外推
工具。各页面分别声明证据边界；术语表给出共享定义。

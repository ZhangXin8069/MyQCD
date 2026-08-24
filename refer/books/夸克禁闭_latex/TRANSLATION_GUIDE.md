# 翻译指南：夸克禁闭（中文版）

本文档记录中文版 LaTeX 的生成方式。

## 来源

- **英文版 LaTeX**：`../Confinement_of_quarks_latex/`（本中文版逐节翻译自该英文版）。
- **原著**：K. G. Wilson, "Confinement of quarks", Phys. Rev. D **10**, 2445 (1974)。
- **插图**：`images/` 中的 10 张图复制自英文版的 `images/`（同名 `figN.png`）。

## 约定

- 使用 `ctexart`（XeLaTeX），中文字体为 AR PL UMing CN / Droid Sans Fallback。
- 章节编号为罗马数字（I、II、……），小节为 A、B；公式编号为
  `(节号.序号)`（如 `(3.1)`、`(5.6)`），与原文一致。
- 图编号为全局 Fig. 1–10，用 `\refstepcounter{figure}` +
  `\caption*{图 N. ...}`（带星号）保持与原文一致；正文中引用写作``图~1``。
- 人名、机构名一般保留英文原名（或中文常用译名，首次出现时给出），
  例如 Schwinger（施温格）、Wilson、Kogut、Susskind。
- 参考文献列表保留英文原文（第 1–20 条）。

## 编译

```bash
cd 夸克禁闭_latex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # ×2 遍
```

输出：`build/main.pdf`（约 24 页）；根目录另有一份 `夸克禁闭.pdf`。

# AGENTS.md — 格点量子色动力学_latex

Gattringer & Lang《Quantum Chromodynamics on the Lattice》中文版 LaTeX 译本（以英文版 `../Quantum_Chromodynamics_on_the_Lattice_latex/` 为底稿逐章翻译）。

## 结构

`main.tex`（ctexbook + XeLaTeX，前言 + 12 章 + 附录）；`preamble.tex`；`chapters/`（中文章节文件，与英文版同名）；`images/figXY.png`（34 图，与英文版共用）；`build/main.pdf`（~392 页）；`TRANSLATION_GUIDE.md`；`figures_map.md`；`overfull_fixes_zh.txt`。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # 两遍
```

## 翻译约定

- 正文/标题/图题/表题译中文；**公式、`\label`、`\eqref`、图片**保留英文原样（数学必须与英文版逐字节一致）
- 章节文件名、编号、`\label` 与英文版完全一致，可逐章对照；英文版修改需同步本目录

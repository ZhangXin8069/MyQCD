# AGENTS.md — INTRODUCTION_TO_LATTICE_QCD_latex

R. Gupta《Introduction to Lattice QCD》(arXiv:hep-lat/9807028v1) 英文 LaTeX 转排——150 页学校讲义综述，格点 QCD 标准参考。

## 结构

`main.tex` + `chapters/secNN_name.tex`（每节一章，sec01–20 + sec00_references 参考文献 198 条）；`images/figN.png`（35 图）；`extract/secNN.txt`（原始提取，只读）；`extract_figures.py`；`CONVERSION_GUIDE.md`；`build/`。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # 需 3 遍（TOC/引用）
```

## 编号模型（忠实原文）

- 每节→章，公式按章编号（如 (5.1)、§14.2.3）；图表强制**全局**编号（Fig. 1–35 / Table 1–8，`\counterwithout`）
- 原文未编号的表（sec02/03/20）用 `\caption*{}` 不占用表号
- 原书笔误按原样保留；§18.6 "Mass Inequalities" 从 sec19 提取补入 sec18（跨页丢失）
- 中文译本：`../格点QCD导论_latex/`

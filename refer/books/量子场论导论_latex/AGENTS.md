# AGENTS.md — 量子场论导论_latex

Peskin & Schroeder《An Introduction to Quantum Field Theory》中文版 LaTeX 转排（英文原版在 `../An_Introduction_to_Quantum_Field_Theory_latex/`）。

## 结构

`main.tex`（ctexbook，`\input` 各章）；`chapters/`（frontmatter + ch01–ch22 + appendix，**已全部译毕**）；`images/`（与英文版共享同一套图）；`build/main.pdf`（419 页）。

## 编译

```bash
cd build; xelatex -interaction=nonstopmode -halt-on-error ../main.tex   # 两遍
```

## 转换约定

- 正文译规范学术中文；**公式、`\label`、`\eqref`、图片**保留英文原样
- 人名保留英文原名；`\problems` 由 `main.tex` 定义为「习题」
- undefined 引用（eq:4.48 等）与原书一致，属忠实转排现象

# AGENTS.md — 格点QCD导论_latex

R. Gupta《Introduction to Lattice QCD》中文版 LaTeX 译本（以英文版 `../INTRODUCTION_TO_LATTICE_QCD_latex/` 为底稿逐章翻译）。

## 结构

`main.tex`（ctexbook + XeLaTeX，20 章 + 参考文献）；`chapters/secNN_name.tex`（21 个中文章节文件）；`images/figN.png`（35 图，与英文版共用）；`build/main.pdf`（126 页）；`TRANSLATION_GUIDE.md`（翻译指南与术语表）。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # 需 3 遍
```

依赖中文字体（`AR PL UMing CN` 正文、`Droid Sans Fallback` 无衬线/等宽，`\setCJKmainfont` 显式指定）。

## 中文排版注意事项

- 正文中希腊字母必须用数学模式（`$\pi$`、`$\alpha_s$`）：中文字体缺 U+03C0 等字形，字面 `π` 产生 "Missing character" 警告
- 数学环境中的 `\mathrm{}` 不放中文（数学字体无 CJK 字形），保留英文

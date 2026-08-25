# CONVERSION_GUIDE.md — Quasi_PDF_Gradient_Flow_latex

## 底稿来源
- arXiv 官方 LaTeX 源（`https://arxiv.org/e-print/1612.01584`，gzip tar）：
  `qpdf.tex` + `qpdf.bbl`，jheppub 文档类；无图源文件（论文无插图）。
- 库内本地 PDF 仅用于核对（/root/PyQCD/refer/papers/…Monahan_Orginos_2017.pdf），未参与排版。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(a4paper,2.5cm)；统一宏包 amsmath/amssymb/
  mathtools/graphicx/microtype/enumitem/url/bigints/xcolor/hyperref(hidelinks)。
- jheppub 私有宏（`\affiliation`、`\emailAdd`、`\abstract{}`、`\keywords`、`\arxivnumber`）
  改为标准 title/author/thanks + abstract 环境；keywords 移至摘要下方一行；
  源内占位 `\arxivnumber{1234.5678}` 弃用，题记行写 JHEP 03 (2017) 116 与 arXiv:1612.01584。
- 正文五个 section 用 sed 按行区间从 qpdf.tex 原样切出（逐字保留，含脚注式致谢），
  未手工重打公式。
- 参考文献：qpdf.bbl 原样嵌入 chapters/backmatter.tex（未运行 bibtex，未删改条目）；
  bbl 内两处 Latin-1 字节已转 UTF-8（Schäfer）。

## 图来源
- arXiv 源不含任何图文件；正文亦无 \includegraphics，无占位妥协。

## 已知妥协点
- 保留源未使用的 `cjm` 环境与 `\trace` 宏定义（需 xcolor）。
- bigints 宏包（系统已有）保留 `\bigintsss` 大积分号原貌。

# CONVERSION_GUIDE — Diffusion Models as Stochastic Quantization in Lattice Field Theory

## 底稿来源
- arXiv:2309.17082v2 [hep-lat]（2024-05-09），Accepted at JHEP。
- 官方 e-print 源 `arxiv.org/e-print/2309.17082`（gzip tar），主文件 `dm4lqft_v2.tex`，
  含 `dm4lqft_v2.bbl`（85 条参考文献）与 `figures/`、`app_figures/` 共 15 个图。
- 库内本地 PDF 仅用于首页核对标题/作者/摘要。

## 归一化说明
- 原 `\documentclass[a4paper,11pt]{article}` + 私有宏包 `jheppub.sty`（及 lineno、
  subcaption、dcolumn、bm、tabularx、xcolor、cleveref）→ 统一为 SPEC §2.2 标准序言；
  正文未实际使用被删宏包的构造。
- JHEP 式 title/author/affiliation 块 → 标准 article 标题块（作者上标单位 +
  date 区放单位/邮箱/arXiv 行）；keywords 并入摘要块末尾。
- `\acknowledgments`（jheppub 宏）→ `\section*{Acknowledgments}`。
- 两处 `\cref{a,b}` → 自定义 `\Eqsref{}{}`；其余交叉引用用原生 `\ref/\eqref`。
- 参考文献直接采用源包内 `.bbl` 原文（含其自带 \providecommand{\href} 与
  \raggedright 分组），未增删改条目。

## 图来源
- 全部 15 幅图取自 arXiv 源包，复制到 `images/`，路径改为 `images/...`；
  无占位图。

## 已知妥协点
- 原文行号（lineno）与超链接配色（colorlinks=blue/red）未保留（hidelinks 规范化）。
- 源中若干成对花括号分组（修订痕迹）原样保留，不影响输出。

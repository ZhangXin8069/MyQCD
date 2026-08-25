# CONVERSION_GUIDE — Locally_Smeared_OPE_latex

## 底稿来源
- arXiv:1501.05348v2 [hep-lat]（2015-04-21），官方 e-print 源码 `wflow_ope.tex` + 9 张图 PDF。
- 期刊版本：Phys. Rev. D 91, 074513 (2015)，DOI 10.1103/PhysRevD.91.074513。
- 库内 PDF（/root/PyQCD/refer/papers/...Monahan_Orginos_2015.pdf）仅用于核对首页书目信息。

## 归一化说明
- revtex4-1 (aps,prd,twocolumn) → `\documentclass[11pt]{article}` 单栏 a4/margin2.5cm；
  宏包统一为 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
- 标题块重排：title/author/affiliation 手工重建；期刊卷页、DOI、arXiv 号以脚注形式置于标题。
- `\pacs{...}` → 正文 PACS numbers 行；`\begin{acknowledgments}` → `\section*{Acknowledgments}`。
- 正文散文、全部公式、图注逐字保留；节文件切分为 section01..07，编号沿用 article 默认。

## 参考文献
- REVTeX 生成的 `thebibliography` 连同其 \providecommand 辅助宏整块原样放入 backmatter.tex；
  条目未删改。导言区补 `\providecommand{\http}{http}` 以修复原源中一处笔误
  （\bibitem{Braun:2008ur} 的 URL 写作 `\http://arxiv.org/...`）。

## 图来源
- arXiv 源内附 9 张矢量 PDF 图，原样复制到 `images/`，相对路径引用，无占位图。

## 已知妥协点
- 双栏→单栏导致分页/图表位置与原刊不同；正文引用 "Eq.~(58)" 为原文硬编码编号，因公式
  环境逐一保序复刻，编号与本文档一致，故保留原样。
- 图 minipage/includegraphics 宽度按单栏版面等比放大（0.24→0.49 等），仅为排版适配。

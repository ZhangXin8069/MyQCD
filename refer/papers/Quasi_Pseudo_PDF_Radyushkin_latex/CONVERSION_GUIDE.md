# Conversion Guide — Quasi_Pseudo_PDF_Radyushkin_latex

- 论文: A. V. Radyushkin, "Quasi-parton distribution functions, momentum
  distributions, and pseudo-PDFs", Phys. Rev. D 96, 034025 (2017).
- 底稿来源: arXiv 官方源 `arxiv.org/e-print/1705.01488`（v2, 2017-08-03），
  单文件 REVTeX 源码 `pseudo0801.tex`，全部正文逐字保留。
- 归一化: `\documentclass[11pt]{article}` + geometry/a4paper margin 2.5cm；
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
  移除 revtex4-1 及未在正文中使用的 dcolumn/slashed/calligra/bm 宏包；
  保留源文件自定义宏 `\nn` 等。PACS 码并入标题脚注。
- 标题采用 PRD 发表版标题；脚注含 DOI/arXiv/预印本号。
- 图: 三幅图 PDF 直接取自 arXiv 源包（RkP1_10_50keyn, QyP1_10_50key, MBMkey），
  复制到 `images/`，无占位图。
- 参考文献: 源内嵌 thebibliography 原样保留于 chapters/backmatter.tex，
  仅去除 INSPIRE 引用计数注释行，条目内容未删改。
- 已知妥协点:
  - 原文两处公式使用同一标签 `newVDFxzQ`（revtex 下重复定义），转排时保留首个、
    第二处不再标注，正文引用未受影响。
  - 原 `\vspace` 微调值照抄，单栏排版下留白与原刊略有差异。

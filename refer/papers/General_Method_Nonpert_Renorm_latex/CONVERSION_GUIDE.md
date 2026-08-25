# CONVERSION_GUIDE

- 来源底稿: arXiv 官方 LaTeX 源 hep-lat/9411010（1994-11-07 单文件 `9411010.tex`，
  `\documentstyle[12pt,epsf]{article}` 老式源）。
- 归一化: `\documentclass[11pt]{article}` + geometry/a4paper/margin=2.5cm；
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)；
  移除 epsf、`\centerline{\bf...}` 手工标题、`\vfill\eject` 等旧式排版。
- 标题块按 SPEC 重排；期刊卷页、preprint 号与 arXiv id 以首页脚注给出。
- 图: 源内 9 幅 PostScript（feynman1-3/file/zvl/zs/za/zp/zsszp.ps）经 ghostscript
  `-dEPSCrop` 转 PDF 置于 `images/`（z*.ps 原缺 %%BoundingBox，已先计算紧致 bbox 再裁剪）。
  `\epsffile` 与 `\special{picture}` 统一改为 `\includegraphics`，宽度近似原尺寸。
- 正文逐字保留（含原文拼写如 denisties/Traslational/whithin/stastistics/continous，
  以及 fig:zvl caption 中重复的 "see sec. \ref{sec:per}"），未作任何更正或改写。
- 表格保留原 LaTeX 码；仅 `\rm`→`\textrm`、`\it`→`\itshape`、figure `[c]`→`[htbp]`。
- 参考文献原样移入 chapters/backmatter.tex（含 bibitem 内嵌注释文字）。
- 已知妥协点: 无。图全部取自官方源，无占位符。

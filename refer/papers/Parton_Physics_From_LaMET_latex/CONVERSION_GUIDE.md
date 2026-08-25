# CONVERSION_GUIDE.md — Parton_Physics_From_LaMET_latex

底稿来源：arXiv 官方源 1404.6680（e-print gzip，内含 newparton.tex 与
spacetime.pdf），未动用本地 PDF。调度方给出的库内 PDF 路径
（/root/PyQCD/...）在本机不存在，亦无需使用。

归一化说明：
- revtex4（aps,prd,preprint）→ article 11pt + geometry(a4paper,2.5cm)；
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hidelinks。
- 移除 epsfig/psfrag/slashed/bm/colordvi/enumerate 及全部作者私有
  \newcommand（经核对正文均未使用）；figure* → figure（单栏）。
- 正文、摘要、图注、致谢、thebibliography 逐字保留，含原稿笔误
  （"renormaliation"、"couner-part"、"obervables"、"plan wave"、
  "C.~-P.~Yuan and ," 等）与注释掉的 bibitem；未删条目、未改写。
- 原文无 \section 分节，全文置 section01.tex；致谢+参考文献在 backmatter.tex。
- 标题块重排：title/author/affiliations + \thanks 脚注式期刊卷页与
  arXiv 行；编号用 article 默认。

图：images/spacetime.pdf 直接取自 arXiv 源包，无占位。

已知妥协点：无。两次 xelatex 通过，无 undefined references/citations。

# CONVERSION_GUIDE.md

## 来源
- 底稿：arXiv 官方源 `arxiv.org/e-print/1305.1539`（gzip tar，`newparton.tex` + `pdf.eps`）。
- 原稿为 REVTeX4（prd preprint 单栏）；本版按统一规范归一化为
  `\documentclass[11pt]{article}` + geometry/amsmath/amssymb/mathtools/graphicx/
  microtype/enumitem/url/hidelinks-hyperref。

## 归一化说明
- 正文、摘要、脚注式致谢与参考文献**逐字保留**（含原文拼写疏漏，如
  "renormaliazation"、"anistropic"、"This late quantity" 等）。
- 标题块重排为 article 式 title/author/affiliation，发表信息以脚注给出
  （PRL 110, 262002 (2013)；DOI 10.1103/PhysRevLett.110.262002；arXiv:1305.1539）。
- 删除 REVTeX 私有宏包（epsfig/psfrag/colordvi/enumerate/slashed/bm 等）；
  `slashed` 以手写 `\providecommand{\slashed}` 等价替代（原稿未实际使用）；
  原自定义宏保留。
- 公式编号沿用 article 默认顺序编号，与正文引用的 Eq. (1)/(3)/(7)/(11) 一致。

## 图来源
- Fig. 1 = 原源码 `pdf.eps`（单圈修正示意），复制至 `images/pdf.eps`，
  XeLaTeX 经 xdvipdfmx 直接内嵌，无占位。

## 已知妥协点
- 原预印本文中 `\cite{jizhangzhao}` 在其文献表中无对应条目（原作者疏漏）。
  转排时依正式出版版（INSPIRE recid 1232221 的参考文献表）补入该条：
  X. Ji, J.-H. Zhang, Y. Zhao, PRL 111, 112002 (2013) [arXiv:1304.6708]，
  在 backmatter.tex 中以注释标明系转排者所加。其余条目未作任何增删改写。
- 库内本地 PDF 未使用（arXiv 源完整可用）。

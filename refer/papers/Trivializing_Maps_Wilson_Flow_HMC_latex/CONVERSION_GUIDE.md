# CONVERSION_GUIDE

## 底稿来源
- arXiv 官方源 `arxiv.org/e-print/0907.5491`（v2，2009-12-03 打包），plain TeX
  （作者自定义 format/macros/sectN 文件结构），逐字转录为 LaTeX。
- 书目信息与库内 PDF（Trivializing_maps_the_Wilson_flow_and_the_HMC_algorithm_Luscher_2010.pdf）
  及 arXiv abs 页交叉核对；DOI 10.1007/s00220-009-0953-7 取自 arXiv 元数据。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(2.5cm)；amsmath/amssymb/mathtools/
  graphicx/microtype/enumitem/url/hyperref(hidelinks)。
- 原文自定义宏（\trans、\Lop、\du、\rmd 等）在导言区以 \newcommand 等价移植；
  plain-TeX `\cases`→amsmath `cases`；`\equation/\enum/\noenum` 手工映射为
  equation/align（每行一号）/multline/split。
- 公式编号用 \numberwithin{equation}{section}，与原文 (2.1)…(E.12) 完全一致
  （已核对正文全部硬编码引用：(2.9)(4.5)(4.14)(4.15)(5.11)(5.14)(A.5)(A.13)
  (B.3)(B.5)(B.9)(C.1)(D.1)(D.5)(D.10)(D.11)(D.14)(E.3)(3.9) 等）。
- 参考文献：原 biblio 文件 13 条原样转入 thebibliography（顺序=原文编号顺序），
  正文 [\ref{…}] → \cite{…}。

## 图来源
- 源包 plots/cycle.eps、loops.eps、trj.eps 经 epstopdf 转为 images/*.pdf，
  caption 原文保留。

## 已知妥协点
- 致谢段从 sect7 末尾移至 backmatter（\section*{Acknowledgements}），文字未动。
- 多行公式的行间距微调（\nexteq 跳距以 \\[..ex] 近似）；无内容改动。
- 原文页眉页脚/CERN 预印本排版样式不复制；CERN-PH-TH/2009-118 保留于首页右上。

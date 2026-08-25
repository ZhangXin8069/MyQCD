# CONVERSION_GUIDE — TMD_Soft_Function_LaMET_latex

## 底稿来源
- arXiv:2005.14572（v2, hep-lat），官方源 `arxiv.org/e-print/2005.14572`，
  单文件 `soft_function_v06.tex` + 22 个 PDF 图，完整解包使用。
- 发表信息（经 inspirehep.net API 核实）：Phys. Rev. Lett. 125, 192001 (2020)，
  DOI 10.1103/PhysRevLett.125.192001。

## 归一化说明
- revtex4-1 (prl, twocolumn) → `\documentclass[11pt]{article}` + geometry/a4paper margin 2.5cm；
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hidelinks-hyperref。
- 移除 REVTeX 私有构造：`\collaboration`/`\affiliation`/`\email` 改为标题块上标编号 +
  机构列表；`\date{\today}` 按发表版写为 October 9, 2020；删除未使用的
  color/slashed/epsfig/subfigure/diagbox/ulem 及作者草稿宏 \Red/\Blue/\rsout/\bsout。
- 正文散文、全部公式、表格、图注、致谢、参考文献逐字保留；
  PRL 式斜体行内小节名（{\it Introduction.} 等）转为编号 \section{...}。
- Supplemental Materials 原位于参考文献之后，按本仓库规范移入 backmatter.tex
  （致谢 → 补充材料 → 参考文献）；\section*{Supplemental Materials} 转为编号节。

## 图来源
- 全部 22 幅图为 arXiv 源自带 PDF 矢量图，复制至 images/；
  文件名中 `=` 已删除（09a_HeatMap_b=0.pdf → 09a_HeatMap_b0.pdf）并同步改写引用。无占位图。

## 已知妥协点（微小、已声明）
1. 原文硬编码交叉引用改为 \ref 动态引用以适配 article 编号：
   "Eq.(2)/Eq.(4)/Table I/Fig. 2" → 对应 label 引用（文字其余部分未动）；
   补充材料正文 "Sec. C and F" → \ref{subsec:mixing} and \ref{subsec:imagpart}。
2. 补充材料中重复出现的 `\label{eq:S_ratio}` 重命名为 `eq:S_ratio_app`（无引用指向它），
   以消除 multiply-defined 警告。
3. 参考文献条目原样保留（含 INSPIRE 统计注释行）；\bibitem{supplemental}
   为原文自引补充材料的占位条目，照原文保留。

# CONVERSION_GUIDE — Accessing_Gluon_PDF_LaMET_latex

## 底稿来源
- arXiv:1808.10824 官方 LaTeX 源（v2, `gluon_quasi-PDF_prl_revised2.tex`，2019-03-21），
  经 `https://arxiv.org/e-print/1808.10824` 获取（gzip 单文件，无图无表）。
- 与发表版 PRL 122, 142001 (2019) 对应。

## 归一化说明
- 原稿为 REVTeX 4.1 双栏 Letter；改为 `\documentclass[11pt]{article}` +
  geometry/a4paper/2.5cm，统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/
  enumitem/url/hidelinks-hyperref。
- 原 run-in 粗体段首标题（Introduction: 等 7 个）改排为编号 \section（1–7），
  文字逐字保留；摘要逐字保留。
- 标题块重排：title + 上标作者/单位；DOI/arXiv/通讯作者以首页脚注给出
  （原稿 \email{wei.wang@sjtu.edu.cn} 保留于此脚注）。
- `\begin{acknowledgments}` → `\section*{Acknowledgments}`。
- 数学环境（eqnarray/align、pmatrix、matrix 下标）原样照抄；
  仅保留正文实际使用的源宏 \beq/\eeq/\non。
- 参考文献为源文件 thebibliography 逐条原样转录（含 INSPIRE 计数注释行，
  未删任何活动条目；原稿中被注释掉的备用条目一并保留为注释）。

## 图表
- 该文无图、无表，无需 images/。

## 已知妥协点
- 无。正文与公式逐字对应 arXiv v2 源（含原文 Eq.(15) 第二式中 `M^2,` 的
  原样逗号排版瑕疵，忠实保留）。

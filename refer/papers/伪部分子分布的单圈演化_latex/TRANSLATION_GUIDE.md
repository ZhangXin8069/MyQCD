# Translation Guide — 伪部分子分布的单圈演化_latex

## 来源
- 原文：A. Radyushkin, "One-loop evolution of parton pseudo-distribution
  functions on the lattice", arXiv:1801.02427v3 [hep-ph]；
  Phys. Rev. D 98, 014019 (2018), DOI: 10.1103/PhysRevD.98.014019。
- 底稿为英文转排版 `../One_Loop_Evolution_Pseudo_PDF_latex/`
  （arXiv 官方 TeX 源逐节转排），本目录为其逐节忠实中文译本。

## 约定
- `\documentclass[11pt]{ctexart}`；字体 AR PL UMing CN（正文）/
  Droid Sans Fallback（无衬线/等宽）；行距 1.05、emergencystretch 3em。
- 全部散文逐节翻译：摘要、小节名、图注、脚注、致谢；
  数学公式、人名、机构、参考文献列表保留英文原文，公式照抄不改。
- 术语：quasi-PDF→准部分子分布；pseudo-PDF→伪部分子分布（伪 PDF）；
  ITD→Ioffe 时间分布；reduced→约化；LLA→领头对数近似；
  evolution→演化；matching→匹配；renormalization→重正化；
  gauge link→规范连接；higher-twist→高扭度；global fits→全局拟合。
- 图直接复制英文目录 `images/`（11 张 PDF）；章节/公式/图表编号与英文版一一对应。

## 妥协点
- 无占位图；编译两遍通过，交叉引用全部解析（build/main.pdf，14 页）。

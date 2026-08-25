# TRANSLATION_GUIDE — 准PDF完整非微扰重正化方案_latex

## 来源
- 底稿为英文转排目录 `../Complete_NP_Renorm_QuasiPDF_latex/`
  （其底稿为 arXiv:1706.00265 官方源 tex+bbl+18 幅 EPS 图）。
- 逐节忠实翻译全部散文：摘要、标题、小节名、图注、表注、脚注、致谢；
  数学公式一律照抄英文版未改动；人名/机构/参考文献列表保留英文。

## 约定（术语采用物理学界通用译名）
- quasi-PDF → 准部分子分布（准 PDF）；light-front PDF → 光前部分子分布；
  pseudo-PDF → 赝部分子分布；transversity → 横向性；helicity → 螺旋度。
- smearing → 涂抹（HYP smearing → HYP 涂抹）；matching → 匹配；
  renormalization → 重正化；lattice artifacts → 格点伪影；
  discretization effects → 离散化效应；truncation → 截断；
  twisted mass fermions → 扭转质量费米子；vertex function → 顶点函数。

## 结构与编号
- 章节/公式/图表编号与英文版一一对应（含表 1、表 2 与全部 10 个 figure 环境）。
- 图直接复制自英文目录 `images/*.eps`，引用路径一致。
- 参考文献保留英文，逐条照录 arXiv 源 `.bbl`（与英文版完全相同）。
- 原文重复标签 `sub3.2`（两处小节同名 label）按原文保留，仅产生编译警告。

## 排版设置
- `\documentclass[11pt]{ctexart}` + a4paper/2.5cm 边距；
  字体：AR PL UMing CN / Droid Sans Fallback（SPEC 固定）；
  行距 1.05、emergencystretch 3em（参照 夸克禁闭_latex/main.tex）。

## 已知妥协点
- 无内容删减。AR PL UMing 无真实粗体/斜体字形，编译日志中的 font-shape
  替换警告为正常回退行为。

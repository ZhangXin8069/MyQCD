# TRANSLATION_GUIDE.md

## 来源
- 译自同库英文转排版 `../Novel_Quark_Field_Creation_Operator_latex/`
  （底稿为 arXiv:0905.2160 官方 LaTeX 源）。
- 原文：M. Peardon et al. (Hadron Spectrum Collaboration),
  Phys. Rev. D 80, 054506 (2009)。

## 约定
- `\documentclass[11pt]{ctexart}`；字体 AR PL UMing CN /
  Droid Sans Fallback（与 books 目录中文版一致）。
- 全部散文逐节忠实翻译：摘要、标题、小节名、图注、表注、脚注、致谢。
- 数学公式、标签（\label/\ref）、引用键一律照抄英文版；
  章节/公式/图表编号与英文版一一对应。
- 人名、机构、参考文献列表保留英文（backmatter 中 thebibliography
  原样复用，拆分出 `chapters/bibitems.tex` 共享条目）。
- 术语：smearing→涂抹，distillation→蒸馏，perambulator→保留英文
  （首现加注“遍历矩阵”），disconnected→不连通，
  generalized perambulator→广义 perambulator，
  point-to-all→point-to-all，stout-smeared→stout 涂抹。

## 图
- images/*.pdf 直接复制自英文目录（EPS 经 Ghostscript 转换的同一批文件）。

## 妥协点
- 无占位图；无删减。个别原文笔误按忠实原则随译文自然表述，公式未改动。

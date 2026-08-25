# TRANSLATION_GUIDE.md

## 来源
- 译自本库英文转排版 `../Analytic_Smearing_of_SU3_Link_Variables_latex/`
  （底稿：arXiv:hep-lat/0311018 官方 LaTeX 源）。
- 任务单所给 hep-lat/0307022 为另一论文（Adams & Bietenholz），已改用
  本文正确 id。

## 约定
- `\documentclass[11pt]{ctexart}`；字体 AR PL UMing CN /
  Droid Sans Fallback；\linespread{1.05}、\emergencystretch{3em} 等设置
  参照 `books/夸克禁闭_latex/main.tex`。
- 逐节忠实翻译全部散文（摘要、标题、小节名、图注、致谢）；数学公式一律
  照抄不改；人名/机构/参考文献列表保留英文；章节、公式、图表编号与英文版
  一一对应。
- 术语：smearing→涂抹，stout links→stout 链接，fuzzing→fuzz 涂抹，
  fat links→胖链接，staple→staple 组合，plaquette→方格，
  tadpole→蝌蚪图，matching/renormalization→匹配/重正化，
  molecular dynamics→分子动力学，force term→力项，
  effective energy→有效能量，unquenched→非 quenched（含海夸克）。
- 图 4 幅直接复制英文目录 `images/*.pdf`；参考文献 22 条原样保留英文
  （与英文版逐字相同）。

## 妥协点
- UMing 字体无真粗体/斜体，编译有良性 font-shape 警告（ctex 自动替代）。
- 文献条目 pub 的幽默注释按原文保留英文，未译。

# TRANSLATION_GUIDE — 规范等变的流采样_latex

## 来源
- 底稿：英文规范化转排版 `../Equivariant_Flow_Sampling_latex/`
  （其底稿为 arXiv:2003.06413 官方 LaTeX 源，revtex4-1 → article 归一化）。
- 本目录逐节忠实翻译其全部散文（标题、摘要、小节名、图注、脚注、致谢）。

## 约定
- `\documentclass[11pt]{ctexart}`；字体固定为 AR PL UMing CN /
  Droid Sans Fallback（XeLaTeX）；行距 1.05，\emergencystretch=3em。
- 数学公式一律照抄英文版不改；人名、机构、参考文献（72 条 bbl 原样附加）
  保留英文。
- 术语译法：gauge-equivariant→规范等变；critical slowing down→临界慢化；
  coupling layer→耦合层；kernel→核；topological susceptibility→拓扑磁化率；
  plaquette/Wilson 圈/sweep/Haar 测度/trivializing map（平凡化映射，首现注英）
  等按格点与机器学习界通行用法。
- 章节、公式、图表编号与英文版一一对应（节 1–5 + 致谢 + 参考文献）。
- 图 4 幅直接复制自英文目录 images/。

## 妥协点
- AR PL UMing CN 无粗体/斜体字形，编译时回退为常规体（仅字体形状警告，
  不影响内容）；摘要标题由 ctex 自动作"摘要"。

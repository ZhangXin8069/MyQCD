# TRANSLATION_GUIDE

## 来源
- 底稿为本库英文转排版 `../Multiplicative_Renorm_Quasi_Operators_latex/`（arXiv:1809.01836 官方源）。
- 摘要、标题、节名、图注、脚注式作者信息、致谢与补记均逐节忠实翻译；数学公式原样照抄。

## 约定
- 文档类 `ctexart` + 固定字体 AR PL UMing CN / Droid Sans Fallback；行距 1.05、emergencystretch 3em。
- 人名、机构名保留原文（作者中文名附罗马拼写）；参考文献列表整体保留英文，未删改条目。
- 术语：quasi-PDF→准部分子分布；quasi-parton operator→准部分子算符；gauge link→规范链；
  multiplicative renormalizability→乘法可重正性；dimensional regularization (DR)→维数正规化；
  lattice cross sections (LCSs)→格点截面；matching→匹配；collinear factorization→共线因子化；
  Ward identity→Ward 恒等式；one-particle-(ir)reducible→单粒子不可约/可约。
- 章节、公式、图表编号与英文版一一对应；图直接复制自英文目录 `images/`。

## 妥协点
- 无占位内容。旧式字体命令 `\it` 在 ctex 下对紧随的中文字符会误吞分词，已改用 `\textit{}`。

# TRANSLATION_GUIDE.md — 任意阶部分子分布矩_latex

## 来源
- 英文转排目录 `../PDF_Moments_Any_Order_latex/`（底稿 arXiv:2311.18704v2 官方 TeX 源）。
- 逐节忠实翻译全部散文（标题、摘要、正文、图注、表注、脚注、致谢、补充材料）；
  数学公式照抄不改；人名/机构/参考文献列表保留英文（55 条 bbl 原样复制）。

## 约定
- 文档类 ctexart 11pt；字体 AR PL UMing CN / Droid Sans Fallback；
  `\linespread{1.05}` + `\emergencystretch=3em`。
- 章节/公式/图表编号与英文版一一对应；图片直接复制自英文目录 `images/`。
- 术语：gradient flow→梯度流；quasi-PDF→准部分子分布；pseudo-PDF→赝 PDF；
  matching→匹配；renormalization→重正化；twist-2→扭度2（保留英文 twist-2）；
  ringed fields→环场；SFTX→短流时间展开；hypercubic group→超立方群；
  irreducible representation→不可约表示；traceless→无迹；anomalous dimension→反常量纲；
  signal-to-noise ratio→信噪比；lattice spacing→格距；continuum limit→连续极限。

## 妥协点
- 与英文版相同：匹配节中重复标签 eq:flowed_t2 改为 eq:flowed_t2_ringed。
- 原文 "the energy-momentum tensor" 译作“能量—动量张量”；"beta function" 保留
  “beta 函数”写法以避免正文字体缺希腊字符。

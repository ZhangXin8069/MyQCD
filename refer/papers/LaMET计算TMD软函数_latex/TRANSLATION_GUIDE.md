# TRANSLATION_GUIDE — LaMET计算TMD软函数_latex

## 来源
- 原文：Qi-An Zhang et al. (Lattice Parton Collaboration), "Lattice-QCD Calculations
  of TMD Soft Function Through Large-Momentum Effective Theory"，
  arXiv:2005.14572 [hep-lat]，发表于 Phys. Rev. Lett. 125, 192001 (2020)。
- 底稿为本库英文转排版 `../TMD_Soft_Function_LaMET_latex/`（arXiv 官方源），
  本目录为其逐节忠实中文翻译。

## 约定
- `\documentclass[11pt]{ctexart}`；字体：AR PL UMing CN（正文）/
  Droid Sans Fallback（无衬线/等宽）；\linespread{1.05} + emergencystretch 3em。
- 摘要、标题、小节名、图注、表注、脚注、致谢全部翻译；
  数学公式一律照抄英文版不改；人名、机构、参考文献列表保留英文。
- 术语采用物理学界通用译名：soft function→软函数，quasi-TMD wave function→
  准 TMD 波函数，Collins-Soper kernel→Collins-Soper 核，rapidity→快度，
  form factor→形状因子，matching→匹配，renormalization→重正化，
  ensemble→系综，wall source→墙源，boost factor→增强因子，
  intrinsic→内禀，operator mixing→算符混合，pinch-pole→pinch-pole 奇异性。
- 章节/公式/图表编号与英文版一一对应；图片直接复制自英文目录 images/。

## 妥协点
1. 与英文版相同的 \ref 动态引用修正（原硬编码 Eq.(2)/Eq.(4)/Table I/Fig. 2 →
   对应 label 引用；补充材料 Sec. C and F → subsec 引用）。
2. 补充材料中重复的 eq:S_ratio 标签重命名为 eq:S_ratio_app（与英文版一致）。
3. 致谢中的中文人名（徐峰、袁立）依原文拼音 Xu Feng, Yuan Li 回译，如与本人
   用字有出入以原文为准。

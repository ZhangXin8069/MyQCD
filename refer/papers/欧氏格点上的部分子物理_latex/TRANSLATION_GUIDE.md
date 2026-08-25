# TRANSLATION_GUIDE.md

## 来源
- 底稿为同任务生成的英文归一化转排版
  `../Parton_Physics_on_Euclidean_Lattice_latex/`（其底稿来自 arXiv:1305.1539 官方源）。
- 文档类 `\documentclass[11pt]{ctexart}`；中文字体固定为
  AR PL UMing CN / Droid Sans Fallback；行距 1.05、emergencystretch=3em。

## 约定
- 散文逐节忠实翻译：标题、摘要、正文、图注、致谢；数学公式一律照抄未改；
  人名与机构保留英文；参考文献列表保留英文原文。
- 章节结构、公式编号 (1)–(16)、图号 Fig. 1 与英文版一一对应；
  正文中的 Eq. 引用相应译作"式~(n)"。
- 术语采用物理学界通用译名：light-cone→光锥，leading-twist→领头扭度，
  twist-two→扭度2，boost→助推，matching→匹配，renormalization→重正化，
  GPD→广义部分子分布，TMD→横动量依赖部分子分布，Wigner→维格纳分布，
  exclusive→遍举，jet quenching→喷注淬灭，gauge link→规范链，
  staple→U 形（staple）路径，anisotropic lattice→各向异性点阵。

## 图
- Fig. 1 直接复制英文目录 `images/pdf.eps`（XeLaTeX 内嵌）。

## 妥协点
- 原预印本文中 `\cite{jizhangzhao}` 缺少文献条目（原作者疏漏），中英文版均依
  正式出版版补入 X. Ji, J.-H. Zhang, Y. Zhao, PRL 111, 112002 (2013)
  [arXiv:1304.6708]，并在 backmatter.tex 注明系转排者所加。
- 英文原文的个别拼写疏漏（renormaliazation、anistropic 等）仅存在于英文版；
  中文版按其本意翻译。

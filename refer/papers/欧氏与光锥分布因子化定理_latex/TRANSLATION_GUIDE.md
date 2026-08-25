# Translation Guide — 欧氏与光锥分布因子化定理_latex

## 来源
- 底稿：同任务生成的英文转排版 `../Factorization_Euclidean_LightCone_latex/`
  （其底稿为 arXiv:1801.03917 官方 LaTeX 源）。
- 逐节忠实翻译全部散文：摘要、标题、小节名、图表注、脚注、致谢；
  数学公式一律照抄英文版；人名/机构/参考文献列表保留英文
  （`chapters/bbl.tex` 与英文版完全相同）。

## 约定
- `\documentclass[11pt]{ctexart}`；字体 AR PL UMing CN / Droid Sans Fallback；
  行距 1.08 + emergencystretch 3em（参照 refer/books/夸克禁闭_latex 设置）。
- 章节/公式/图表编号规则与英文版一致（article 默认），交叉引用一一对应。
- 引用简写宏中文化：`\eq`→式(…)、`\sec`→第…节、`\fig`→图…、`\app`→附录…；
  `\spcorr` 宏译为"空间关联函数"。
- 术语：quasi-PDF→准 PDF；pseudo-PDF→赝 PDF；matching→匹配；
  renormalization→重正化；twist-2→扭度-2；plus function→plus 函数；
  Ioffe time→Ioffe 时间；LaMET→大动量有效理论；smeared→涂抹；
  vertex/sail/tadpole→顶点图/帆图/蝌蚪图。
- 图像直接复制自英文目录 `images/`（arXiv 源图，共 8 幅 PDF）。

## 妥协点
- 与英文版相同的三处排版级修正（跨行 \left/\right 定界符改行内定界符、
  标签行 \nonumber 移位、弯引号替换）已同步应用于中文版，公式内容未变。

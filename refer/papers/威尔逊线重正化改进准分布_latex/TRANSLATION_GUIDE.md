# TRANSLATION_GUIDE

- 来源：英文转排版 `../Wilson_Line_Renorm_Improved_QPD_latex/`（底稿为 arXiv:1609.08102 官方源，正文逐字转排）；本目录为其逐节忠实中文译本。
- 约定：`\documentclass[11pt]{ctexart}` + a4paper/2.5cm；中文字体固定 AR PL UMing CN / Droid Sans Fallback；`\linespread{1.05}` + `\emergencystretch{3em}`。
- 全部散文（标题、摘要、小节名、图注、致谢、"补记"、附录）逐段翻译；数学公式、标签（qUnpolDef/WLrenorm/WLcoordspace/eq8/im 等）与交叉引用一律照抄，章节/公式/图表编号与英文版一一对应。
- 人名（Jiunn-Wei Chen 等）、机构地址、参考文献列表保留英文原样（bibliography 直接取自英文目录 backmatter.tex，未删改条目）。
- 术语采用物理学界通用译名：quasi(-)parton distribution→准部分子分布/准 PDF，Wilson line→威尔逊线，matching→匹配，renormalization→重正化，counterterm→反项，power divergence→幂次发散，lattice spacing→格点间距，large momentum effective theory→大动量有效理论。
- 图：9 张 PDF 图直接复制自英文目录 `images/`，路径引用一致。
- 妥协点：① 题注脚注中的 DOI 联网未能核实，按规范标 `[?]`；② 编译日志仅有 UMing 无粗体/斜体形状的字体替换警告（非错误），两遍 xelatex 通过、无未定义引用。

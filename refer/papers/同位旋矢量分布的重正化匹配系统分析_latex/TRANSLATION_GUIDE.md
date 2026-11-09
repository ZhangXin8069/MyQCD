# TRANSLATION_GUIDE

- 来源：英文转排目录 `../Isovector_Systematic_Renorm_Matching_latex/`（arXiv:1807.06566v2 [hep-lat] 官方源）。
- 文档类：`\documentclass[11pt]{ctexart}`；中文字体固定为
  AR PL UMing CN / Droid Sans Fallback；行距 1.08、emergencystretch=3em 参照书目模板设置。
- 翻译范围：标题、摘要、五个章节全部散文、表题/图注、致谢、附录导语与结语；
  数学公式、表格数值、图一律照抄英文版不改。
- 人名、作者名单、机构地址、资助项目编号与参考文献列表（87 条 thebibliography）保留英文原样。
- 术语约定：quasi-PDF→准 PDF；LaMET→大动量有效理论；RI/MOM→正规化无关动量减除；
  smearing→涂抹；matching→匹配；renormalization→重正化；counterterm→反项；
  excited state→激发态；source-sink separation→源—汇分离；operator mixing→算符混合。
- 图直接复制英文目录 `images/`（33 个 PDF），路径 `images/`，编号与英文版一一对应。
- 结构与英文版一一对应：section01–05 + backmatter（致谢+附录A/B+参考文献）；
  附录 A/B 标题译出，正文公式原样；交叉引用标签与英文版相同（app:one-loop 等）。
- 妥协点：AR PL UMing CN 无粗体/斜体字形，回退默认（编译日志中的 font shape 警告无害）；
  原文重复标签 eq:fit 的第二处已改为 eq:fit2（同英文版处理）。

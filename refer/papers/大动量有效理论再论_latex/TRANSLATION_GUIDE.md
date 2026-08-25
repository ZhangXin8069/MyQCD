# TRANSLATION_GUIDE.md

## 来源
- 译自本库英文转排版 `../More_On_LaMET_Parton_Physics_latex/`（底稿为 arXiv:1706.07416
  官方 LaTeX 源 `mk_eu_new.tex`）。原文：Nucl. Phys. B 924, 366--376 (2017)。

## 约定
- 文档类 `ctexart`(11pt)；字体固定 AR PL UMing CN / Droid Sans Fallback；
  行距与 emergencystretch 设置参照 `refer/books/夸克禁闭_latex/main.tex`。
- 全部散文逐节忠实翻译：摘要、标题、小节名、脚注、致谢；数学公式一律照抄不改；
  人名/机构/参考文献列表保留英文；作者中文名（季向东/张建辉/赵勇）按学界通行写法附注。
- 术语采用通用译名：quasi-distribution→准分布，pseudo-distribution→赝分布，
  Ioffe-time distribution→Ioffe 时间分布，matching→匹配，renormalization→重正化，
  power divergence→幂次发散，collinear divergence→共线发散，gauge link→规范连接，
  Wilson line→威尔逊线，boost→助推，infinite momentum frame→无限动量系，
  light-front quantization→光前量子化，higher-twist→高扭度，support→支撑域。
- 章节、公式、引文编号与英文版一一对应（同一套 label）。

## 妥协点
1. §4 中 "the quality of Eq.(11) and (12)"（quality 为 equality 之笔误）译为
   "等同性"，并用 \ref 动态引用两个 h 公式（英文版同此处理）。
2. 原文笔误（Eulidean、distribtutions、guage 等）在中文版中以"（原文如此）"
   或保留英文原词方式注明，不擅自更正物理内容。
3. 引用 Rossi–Testa 文中式 (19)、(35) 的编号指其原文编号，保持字面直录。

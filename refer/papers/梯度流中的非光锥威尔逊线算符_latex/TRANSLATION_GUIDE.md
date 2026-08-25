# TRANSLATION_GUIDE

## 来源
- 英文转排目录 `../Off_LightCone_Wilson_Line_Flow_latex/`（底稿 arXiv:2312.05032 官方源，
  JHEP 06 (2024) 210）。中文版逐节忠实翻译其 main + chapters/section01–05 + backmatter
  （致谢、附录A、参考文献）。

## 约定
- 文档类 ctexart；CJK 字体按规范固定（AR PL UMing CN / Droid Sans Fallback）。
- 全部数学公式、\label/\ref/\cite 键与英文版逐字一致，编号一一对应。
- 人名、机构地址、参考文献列表保留英文/原文。
- 术语：quasi-PDF→准PDF（首现"准分布函数"）、gradient flow→梯度流、Wilson line→威尔逊线、
  matching→匹配、renormalization→重正化、ringed (fermion) field→带圈费米子场、
  auxiliary field→辅助场、small flow-time expansion→小流时展开、anomalous dimension→反常量纲、
  background field method→背景场方法、eikonal→类晶、quarkonium→夸克偶素、
  chromoelectric/chromomagnetic→色电/色磁、flow radius→流半径、linear divergence→线性发散。
- 图 7 幅直接复制自英文目录 images/，路径相同。

## 妥协点
- 原文个别笔误性表述（如 "we have obtained eq.~(...)" 缺介词、"the continue limit"、
  eq.(677) 中 O_{∥⊥}^R 与 C_{∥⊥} 的下标写法）按原文照译照抄，未代为更正。
- 编译：xelatex ×2 于 build/main.pdf；无 error、无 undefined reference。

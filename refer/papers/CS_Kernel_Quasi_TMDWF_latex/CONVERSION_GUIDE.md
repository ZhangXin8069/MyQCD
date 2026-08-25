# CONVERSION_GUIDE — CS_Kernel_Quasi_TMDWF_latex

## 底稿来源
- arXiv:2204.00200 官方 e-print 源码（`https://arxiv.org/e-print/2204.00200`，gzip tar），
  含 main.tex / main.bbl / plots/*.eps。
- 发表信息经 inspirehep.net API 核实：Phys. Rev. D 106, 034509 (2022),
  DOI 10.1103/PhysRevD.106.034509。

## 归一化说明
- revtex4-1（twocolumn, prd）→ `article`(11pt) 单栏 + geometry(2.5cm)；
  宏包统一为 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
- 标题块重排：合作组名 LPC + 13 位作者按上标编号对应 15 个单位；通讯作者以 *、† 标注；
  arXiv id / DOI 以脚注行置于单位列表之后。
- 正文（含摘要、脚注式通讯邮箱、致谢、附录）逐字保留，未改动任何句子；
  原文中的笔误（如 "arge P^z"、"teh form"）照原样保留。
- 参考文献：main.bbl（unsrt，54 条）原样放入 chapters/backmatter.tex，未增删改写。

## 图来源
- 全部 39 张图取自 arXiv 源码 plots/ 中预转换的 `*-eps-converted-to.pdf`，
  复制到 images/<原名>.pdf；无占位图。
- `\includegraphics` 统一改为 width=0.62\textwidth（双图示意类 0.5\textwidth），
  多面板堆叠布局保持原顺序。

## 已知妥协点
- 删除了源码中 `\begin{comment}...\end{comment}` 内一段被作者废弃的草稿文字
  （原刊版本亦不含该内容）；删除 widetext/newpage 双栏排版指令。
- 原文 Fig.(fig:K_b) caption 后有一句游离于 caption 花括号外的正文
  （"The horizontal shaded band shows ..."），按源码原样保留为正文文本。

# CONVERSION_GUIDE.md — PDF_Moments_Any_Order_latex

## 底稿来源
- arXiv:2311.18704v2 [hep-lat]（官方 TeX 源，`https://arxiv.org/e-print/2311.18704`）
- 作者：Andrea Shindler；TTK-23-31；发表于 Phys. Rev. D 110, L051503 (2024)，
  DOI: 10.1103/PhysRevD.110.L051503。
- 库内本地 PDF（3 页 Letter 版）用于交叉核对首页书目信息。

## 归一化说明
- 原 REVTeX4-2 (`twist2_gf.tex` + intro/t2/gf/matching/applications/conclusions/supplemental.tex)
  → `article` 11pt + geometry(2.5cm)；正文文字逐字保留（含摘要、脚注、致谢、补充材料）。
- 原 run-in 小节标题（*Introduction.* 等）改为编号 `\section`；
  gf 节内 *O(a) improvement.* 与补充材料的三个小标题改为 `\subsection`。
- `macros.sty` 仅收录正文实际使用的宏；`\slashed{D}` 用 `\not D` 等价替代（原 slashed 宏包弃用）。
- intro.tex 中两段 `\begin{comment}` 废弃草稿按原样排除（原编译亦不出现）。

## 图来源
- 全部 10 张图取自 arXiv 源包（8 个费曼图 PDF + 2 个 jpg），复制于 `images/`，
  `\includegraphics` 加相对路径与扩展名；图 1 八张小图宽度由 0.16→0.11\textwidth 以适配单栏 A4。

## 已知妥协点
- 源中 `matching.tex` 与 `gf.tex` 重复使用标签 `eq:flowed_t2`（原稿缺陷）；为消除
  multiply-defined 警告，将匹配节中的环化算符定义式改标为 `eq:flowed_t2_ringed`，
  其余引用目标不变。
- 参考文献直接采用源包自带 `twist2_gf.bbl`（55 条，apsrev4-2 格式，自含宏定义），逐条保留未改动。
- 编号采用 article 默认：节 1–7、公式 (1) 起，与原刊 Letter 双栏编号不一一对应。

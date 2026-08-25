# CONVERSION_GUIDE.md

## 底稿来源
- arXiv 官方源 `e-print/1912.10053`（v2, 2020-11-16, REVTeX 4.1），解包完整可编译。
- 库内 PDF（116 页）仅作核对，未用于提取。

## 归一化说明
- `revtex4-1` → `article`(11pt) + geometry/a4paper/2.5cm；统一宏包 amsmath/amssymb/
  mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)，另保留内容必需的
  标准宏包 bm、xcolor(table)、multirow、dcolumn、subfig。
- REVTeX 专有构造改写：`\affiliation/\email/\preprint/\pacs` → 文首脚注块；
  `\begin{acknowledgments}` → `\section*{Acknowledgments}`；
  `widetext` 环境与 `\squeezetable` 命令删除（单栏排版无意义）；
  占位图文件名中 `_` 转义为 `\_`。
- 参考文献：源 `main.bbl`（apsrev4-1，205 条）逐字放入 `chapters/backmatter.tex`。
- Supplemental Material 按原文顺序置于参考文献之后（同在 backmatter.tex）。

## 图来源与妥协点（已声明）
- 源共 88 个 figure 环境 / 234 个独立图片文件（全部为 PDF 位图化矢量图）。
- 按调度方策略仅收录每章前 4 个 figure 环境（共 36 个环境，76 个图片文件，
  复制于 `images/`，路径 `images/<原文件名>`）；其余 145 处
  `\includegraphics` 以占位框替换（保留原 caption 与 label，框内注明
  "[figure unavailable -- see original paper]" 及原文件名）。
- 表格全部保留 LaTeX 原码；公式、脚注、附录逐字保留。

## 已知问题
- 编号采用 article 默认（节 1,2,…；公式 (1)…），与原刊编号不完全一致，
  交叉引用均经 \label/\ref 自动解析，两遍编译无 undefined references。

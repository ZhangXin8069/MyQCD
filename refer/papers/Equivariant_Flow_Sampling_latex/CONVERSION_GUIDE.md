# CONVERSION_GUIDE — Equivariant_Flow_Sampling_latex

## 底稿来源
- arXiv 官方 LaTeX 源：`https://arxiv.org/e-print/2003.06413`（v1, 2020-03-13，gzip/tar）。
- 含 `main.tex`（revtex4-1）、`main.bbl`（apsrev4-1，72 条）、4 个图 PDF。
- 本地库内 PDF 仅用于核对，未参与文本提取。

## 归一化说明
- 文档类 revtex4-1 → `article`（11pt, a4, margin 2.5cm）；宏包统一为
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
- 原文 PRL 式无编号斜体小节 `\ssection{...}` 改为编号 `\section{...}`（节 1–5）；
  引言部分原文无标题，保持无标题段落置于摘要之后（section01）。
- 原文宏命令（\tint, \obs, \Uone 等）原样保留于导言区。
- 正文文字逐字保留；仅改动：`\citep`→`\cite`、图路径加 `images/` 前缀、
  `\columnwidth`→`\linewidth`（单栏等价）。
- 标题块重排：作者上标对应 3 个单位；首页脚注给出期刊卷页/DOI/arXiv 行
  （原 revtex 由刊方生成，转排后手工补齐）。

## 图来源
- 4 个图 PDF 直接复制自 arXiv 源 → `images/`，无占位图。

## 参考文献
- `chapters/backmatter.tex` 中致谢后原样附加 `main.bbl` 全部 72 条
  （bbl 自带 \providecommand 序幕，与 article+hyperref 兼容），未删改条目。

## 已知妥协点
- 单栏排版，节/公式编号与 PRL 双栏原刊不同（原稿源码本身即无固定编号差异，
  编号由文档类决定）。
- 原文第 2 页脚注 1（Reweighted observables…）保留为正文脚注。

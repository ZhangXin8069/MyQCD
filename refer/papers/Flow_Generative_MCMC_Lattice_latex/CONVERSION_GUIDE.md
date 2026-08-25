# CONVERSION_GUIDE — Flow_Generative_MCMC_Lattice_latex

## 底稿来源
- arXiv 官方源：`https://arxiv.org/e-print/1904.12072`（gzip tar，2019-09-10 版）。
- 解包得 `main.tex`（revtex4）、`main.bbl`、13 个图 PDF。
- 原文：Phys. Rev. D 100, 034515 (2019)，MIT-CTP/5114。

## 归一化说明（覆盖原样式）
- `revtex4` → `article`（11pt, a4paper, margin=2.5cm）；统一宏包
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/cancel/hyperref(hidelinks)。
- 标题块手排（title/author/affiliation），首页脚注给出 DOI/arXiv/预印本号。
- 正文文字逐字保留；公式、编号顺序不变（article 默认节 1,2,… 公式 (1)…）。

## REVTeX 私有构造的替换
- `\begin{ruledtabular}` → 普通 tabular + `\hline\hline`（表 I）。
- `\begin{widetext}` → 移除（单栏排版无需）。
- `subfig` 的 `\subfloat`/`\subref` → 自写计数器版宏（导言区），输出 (a)(b)(c)。
- `bbm` 的 `\mathbbm{1}` → `\providecommand` 映射为 `\mathbf{1}`。
- `\preprint`（MIT-CTP/5114）并入标题脚注。

## 图来源
- 全部 13 张图直接取自 arXiv 源 PDF，复制到 `images/`，`\includegraphics{images/...}`
  相对路径引用；无占位图。个别图在原 twocolumn 版并排，本版改用 minipage 布局。

## 参考文献
- `main.bbl`（h-apsrev 样式产物）原样放入 `chapters/references.tex`，
  由 `backmatter.tex` `\input`；58 条无一删改。

## 已知妥协点
- 双栏转单栏，图表位置随排版浮动（原码中 "Better float placement" 注释保留）。
- 附录 A 中多行 align 因单栏变宽，为保持公式内容原样未再拆分。

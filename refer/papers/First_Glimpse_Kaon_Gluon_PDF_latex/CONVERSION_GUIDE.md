# CONVERSION_GUIDE — First_Glimpse_Kaon_Gluon_PDF_latex

- 底稿来源：arXiv:2112.03124v2 官方源（`https://arxiv.org/e-print/2112.03124v2`，
  gzip tar 包），含 `main.tex` + `main.bbl` + `Figs/`（19 个 PDF 图）。
- 归一化：revtex4 (prd,aps,twocolumn) → article 11pt 单栏；统一宏包
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref[hidelinks]；
  另加 mathrsfs（正文大量使用 `\mathscr{M}`，必需）。
- 标题块：重排为 article 式 title/author/affiliation；DOI 与 arXiv 号以脚注形式
  附于标题（DOI:10.1103/PhysRevD.106.094510，经 arXiv API 确认）。
- 参考文献：`main.bbl`（apsrev4-1 输出，89 条）原样放入
  `chapters/bibliography.tex` 并由 backmatter 引入；条目未删改；
  编号在单栏布局下按出现顺序呈现。
- 图：源包内 19 个 PDF 图复制到 `images/`，`\includegraphics{images/...}` 引用；
  原 `figure*` 双栏浮动改为单栏 `figure*`/`figure`（article 下等价通栏），
  两张三联图行间加 `\\` 换行以适配单栏宽度。
- `\begin{widetext}`（revtex 私有）已去除包裹；`\preprint`、`\email` 分别并入
  标题脚注与作者 `\thanks`。
- 正文文字、公式、表格逐字保留；未删任何章节或条目。
- 已知妥协点：无。编译两遍+第三遍复核均通过（0 error / 0 undefined ref）。

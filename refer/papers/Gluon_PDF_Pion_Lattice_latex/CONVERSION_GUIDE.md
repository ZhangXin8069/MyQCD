# CONVERSION_GUIDE.md

- 底稿来源：arXiv:2104.06372（v1, 2021-04-13）官方 LaTeX 源 `arxiv.org/e-print/2104.06372`，本地库内 PDF（/root/PyQCD/refer/papers/）仅用于首页书目核对。
- 归一化：revtex4-1（twocolumn、superscriptaddress 等）→ `\documentclass[11pt]{article}` + geometry 2.5cm；宏包统一为 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hidelinks-hyperref。`mathrsfs`（\mathscr）存在则加载，否则回退 \mathcal。
- 正文逐字保留（摘要、脚注、致谢、附录无）；参考文献 = 源 `output.bbl`（apsrev4-1）原样并入 backmatter.tex，未删改条目。
- 图：源包内 11 个 PDF 图全部复制到 `images/`，路径 `figs/`→`images/`；`figure*`（跨栏）改为单栏 `figure`。
- 标题块手工重排：作者上标单位 + 脚注式 MSUHEP-21-004 / arXiv 行。
- 已知妥协点：
  - 双栏排版改为单栏（SPEC 要求），图表宽度沿用原相对宽度；
  - 原文个别笔误按原样保留（如 "an first-principles"、"finial"、"The analysis done Ref.~[15]"、"y^3" 应为 d^3y 等），忠实转录不代改。

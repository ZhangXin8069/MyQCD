# CONVERSION_GUIDE.md

- **底稿来源**: arXiv 官方 LaTeX 源 `arxiv.org/e-print/1602.05525`
  （`smear_moda.tex` + `smear_moda.bbl` + 12 个图 PDF），非库内 PDF
  （调度方提示的库内 PDF 经核对实为 Allton et al., PRD 47, 5153 (1993)，与本论文无关）。
- **归一化**: REVTeX4-1 → article 11pt + geometry(a4, 2.5cm)；宏包统一为
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hidelinks-hyperref。
  去除 `\widetext`（单栏无需）、`figure*`→`figure`、`\pacs`/`\email`/`\affiliation`
  并入文首标题块（DOI/arXiv/PACS 以脚注式行给出）。
- **正文**: 六节 + 致谢 + 附录逐字保留，未改动任何文字、公式、脚注；
  节文件按 `\section` 切分于 `chapters/section01–06.tex`，
  `backmatter.tex` = 致谢 + 附录 + 原 `.bbl`（58 条，原样保留）。
- **图**: 11 张被引用的源图 PDF 全部复制到 `images/`，经 `\graphicspath{{images/}}`
  引用；源内未被引用的 `extra_diff_dir_nuc.pdf` 实际被引用（共 12 张中 11 张入目录）。
- **妥协点**: `dsfont.sty` 本机缺失 → `\providecommand{\mathds}{\mathbb}` 等价替换
  （仅影响 \mathds{1} 字体风格）；`slashed` 包在正文中未使用故移除；
  编号保持 article 默认连续编号，与原文一致。

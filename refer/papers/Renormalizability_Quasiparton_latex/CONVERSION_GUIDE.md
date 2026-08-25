# CONVERSION_GUIDE — Renormalizability_Quasiparton_latex

- 底稿来源：arXiv:1707.03107 官方 LaTeX 源 v2（`arxiv.org/e-print/1707.03107`，
  gzip tar 包），非库内 PDF。原文件 `quasipdf-renormalization.tex`（revtex4）+
  `bbl.tex` + `figures/*.eps`（9 张）。
- 归一化说明：按统一规范改为 `\documentclass[11pt]{article}` +
  geometry(a4,2.5cm)，宏包 amsmath/amssymb/mathtools/graphicx/microtype/
  enumitem/url/hidelinks-hyperref；去除 revtex4、epsfig、epstopdf、bm、slashed
  等私有/未用宏包与全部自定义宏（源中定义的 \ben/\een/\tq/\td 等正文均未使用，
  已删除）。`slashed` 宏包以手写宏 `\newcommand{\slashed}[1]{/\!\!\!#1}` 替代。
  正文内容逐字保留（含摘要、脚注、致谢、附录性内容与原文笔误）。
- 标题块：采用期刊发表题名（调度方给定）；arXiv 源标题为 ``On the
  Renormalizability of Quasi Parton Distribution Functions''，已在标题脚注注明；
  DOI/arXiv 行置于脚注。PACS 行保留为普通文本行。
- 图来源：9 张 EPS 经 epstopdf 转为 PDF 复制到 `images/`（无缺失图），
  `\graphicspath{{images/}}` 相对路径引用，尺寸沿用原文设置。
- 参考文献：bbl 内容原样放入 `chapters/backmatter.tex`（仅修正一处转录笔误：
  Nam:2017gzm 的 InSPIRE 记录号恢复为源文件中的 1591333），条目未删改。
- 编号保持 article 默认（节 1–6、公式顺序编号），单栏排版；因环境与分栏
  与原刊不同，公式编号可能与原刊略有差异，但内部 \eqref 交叉引用一致。
- 已知妥协点：原文正文硬编码的 "Eq. (9)" 引用照原样保留（其指向由原文
  编号体系决定）；原文个别笔误（如 "Renormalizaiton"、"Based these"）
  按“逐字保留”原则未作修改。

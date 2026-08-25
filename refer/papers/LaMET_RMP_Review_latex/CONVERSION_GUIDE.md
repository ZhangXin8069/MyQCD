# CONVERSION_GUIDE — Large-Momentum Effective Theory (LaMET review)

- 底稿来源: arXiv 官方源 `arxiv.org/e-print/2004.03543`（gzip tar），单文件 `lamet_main.tex`
  + `lamet_main.bbl`（apsrmp4-1 自包含） + `lamet.bib` + 31 幅 EPS 图。
- 归一化: REVTeX4-1 → `article` 11pt + geometry/a4、统一宏包；正文逐字保留，
  仅 `\includegraphics` 路径改为 `images/xxx.pdf`。
- 宏处理: 源文件全部 newcommand/DeclareRobustCommand 原样保留（含对 `\sec` 的
  重定义为 Sec.~\ref）；`\beq/\eeq` 等 eqnarray 简写保留。
- 图来源: 源包 EPS 经 Ghostscript `-dEPSCrop` 批量转 PDF 存入 `images/`（31/31 全部成功）。
- 参考文献: `.bbl` 原样嵌入 `chapters/backmatter.tex`；preamble 用
  `[numbers,sort&compress]{natbib}` 解析 author-year 可选参数 → 数字引用。
- 结构: main.tex + chapters/section01–07（按 \section 切分）+ backmatter.tex
  （致谢 + 附录A 缩略语表 + 附录B 约定 + 参考文献，均逐字保留）。
- 标题块: 重排 title/authors/affiliations；邮箱与期刊信息为脚注
  （Rev. Mod. Phys. 93, 035005 (2021); DOI: 10.1103/RevModPhys.93.035005; arXiv:2004.03543）。
- 已知妥协点:
  - 无表格类浮动体（原文亦无 table 环境）；
  - 单栏排版使总页数（~121 pp）多于原刊双栏版式，内容无删减；
  - 附录A 中 `\begin{array}{L@{\qquad}L}` 列格式依赖 array 包的 `>$l<$`，已保留。

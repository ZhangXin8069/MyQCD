# CONVERSION_GUIDE

- 底稿来源：arXiv 官方源 `arxiv.org/e-print/1609.08102`（gzip tar，主文件 `WL_renorm_LPT_v3.tex` + 10 张 EPS 图），逐字转排；正文（含摘要、致谢、Note added、附录）未做任何改写。
- 归一化：`\documentclass[11pt]{article}` + geometry(2.5cm)；宏包统一为 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。移除 revtex4、epsfig、psfrag、colordvi、enumerate、slashed、bm 等原私有依赖。
- 宏处理：`\beq/\eeq/\non` 保留为等价宏；颜色强调命令 `\B/\R` 改为恒等输出（去色）；`\slashed` 以 `\not` 手写等价宏兜底（正文未用）。EPS 图全部经 GhostScript 转成 PDF，置于 `images/`，`\includegraphics` 相对路径引用。
- 结构：`main.tex` + `chapters/section01–04.tex` + `chapters/backmatter.tex`（致谢 + Note added + 附录 + thebibliography 原样保留，含注释性 INSPIRE 行）。源中注释掉的 `%\appendix` 已启用，使附录按 article 默认编为 A 节。
- 标题块：title/author/affiliation 重排为 article 样式，题注脚注给出 NPB 915, 1--9 (2017) 与 arXiv id；DOI 字段未能联网核实，按规范标 `[?]`。
- 编号保持 article 默认（节 1,2,…；公式 (1)…）；单栏排版。
- 已知妥协点：无。两遍 xelatex 编译零错误、零未定义引用。

# CONVERSION_GUIDE.md

- 来源：arXiv:1808.09837v4 官方 LaTeX 源（`arxiv.org/e-print/1808.09837`，2025-05-07 打包）。
  本地库内 PDF（TTK-18-32, v4）仅用于首页书目核对；期刊信息经
  inspirehep.net API 核实：Eur. Phys. J. C 78 (2018) 944,
  DOI:10.1140/epjc/s10052-018-6415-7。
- 归一化：scrartcl→article + geometry(a4,2.5cm)；统一宏包 amsmath/amssymb/
  mathtools/graphicx/microtype/enumitem/url/ifthen/hyperref(hidelinks)。
  正文、脚注、致谢、附录、参考文献逐字保留。
- 私有依赖替换：
  - `slashed` 宏包 → 手写 `\slashed{#1}:=\not{#1}`；
  - `scalefnt/showlabels/fancyhdr/color/cite/ulem/filemod/authblk/epsf/rotating`
    均为版式辅助，删除或以普通字号替代（`\abbrev`→`\small`）；
  - `multirow` → 投影符定义处改为三行数组；
  - 标题块手工重排，作者/单位 + 脚注式 DOI/arXiv 行。
- 图：全部取自 arXiv 源包（dias/O1.pdf、O3.pdf 与 figs/c{1..4}_{3,130}.pdf），
  复制到 `images/`，`\includegraphics` 路径相应改写；bb 选项照抄原文。
- 参考文献：源 `_ref.tex`（sortref 生成）37 条 bibitem 原样并入 backmatter.tex，
  未删改；期刊缩写宏块从原文件保留于 main.tex 序言。
- 已知妥协点：无占位图；公式编号沿用 article 默认 (1)(2)…，与原刊编号一致；
  原 v4 源中 `\label{eq:}`（空名标签，未被引用）按原样保留。

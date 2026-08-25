# Conversion Guide

- **底稿来源**: arXiv:1101.0963 官方源 (`arxiv.org/e-print/1101.0963`, plain-TeX
  多文件工程 main/title/macros/format/sect1–9/appa–c/biblio + 13 幅 EPS 图)。
- **归一化**: plain TeX → `article` 11pt + geometry/a4, margin=2.5cm；统一宏包
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
  原 `\equation/\enum/\nexteq` 手工编号体系改写为标准 `equation/align` +
  `\numberwithin{equation}{section}`，公式号 (2.4)、(A.1)… 与原文完全一致；
  正文中的公式/节/图引用全部改为 `\eqref`/`\ref` 自动交叉引用。
  原 macros 中仍被使用的宏（\rmd,\rz,\SUn,\vbulk,\cbar…）在 main.tex 重定义。
- **图**: 源包 plots/*.eps 经 Ghostscript `-dEPSCrop` 转为 PDF 放入 `images/`，
  以 `\includegraphics` 引用；行内费曼规则图保留原尺寸参数与基线偏移。
- **参考文献**: 原 biblio 的 7 个 \bibitem 原文照录进 thebibliography，
  键名不变，正文 [\ref{...}] → \cite{...}。
- **编号差异**: 无。节 1–9、附录 A–C、图 1–5、公式均与原文一致。
- **已知妥协点**:
  - 正文个别原文笔误按"逐字保留"原则未改动（如 sect.2.3 "As far the momenta"、
    sect.5 "the integral small t"）。
  - 致谢段从第 9 节末移至 backmatter 开头（内容未动）。

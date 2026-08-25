# CONVERSION_GUIDE

- 底稿来源: arXiv:1807.06566v2 [hep-lat] 官方源 `https://arxiv.org/e-print/1807.06566`
  （单文件 `gt_quasi-PDF_v02.tex` + `figures/*.pdf`，REVTeX 4-1 双栏）。
- 归一化: `\documentclass[11pt]{article}` + geometry/a4paper/2.5cm；统一宏包
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref(hidelinks)。
  移除 revtex4-1 私有结构（`\preprint`、`\collaboration`、`\widetext`、`\email`、twocolumn）。
- 正文内容逐字保留：摘要、五个 section、致谢、两个附录、87 条 thebibliography 原样转录。
- 标题块重排：作者+上标编号、通讯作者脚注邮箱、机构列表 minipage、arXiv/MIT-CTP 行。
- 图来源: arXiv 源内全部 33 个 PDF 图复制到 `images/`，路径改 `images/`；
  `unpolarized_different_momentum(.pdf)` 与 `unpolarized_Pz=5_with_pheno(.pdf)` 源中无扩展名引用，保持原样。
- 已知妥协点:
  - 宏包 `slashed` 以 `\providecommand{\slashed}[1]{\ensuremath{\not{#1}}}` 等价替换。
  - 原文两处公式共用 `\label{eq:fit}`（源文件笔误），第二个改为 `eq:fit2` 以消除重复标签警告；正文无引用受影响。
  - 附录原为 `\section*{Appendix}` + 两个 `\subsection`，改为 `\appendix` 后两个 `\section`（编号 A/B），交叉引用 \ref{app:*} 相应指向 A/B。
  - 单栏排版，公式编号与节编号按 article 默认（与原刊双栏编号一致）。

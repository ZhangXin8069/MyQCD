# CONVERSION_GUIDE — Smeared_Quasidists_Perturbation_latex

## 底稿来源
- arXiv:1710.04607v3 [hep-lat]（官方源，`https://arxiv.org/e-print/1710.04607`）。
- 该 v3 为勘误后版本（Erratum Phys. Rev. D 110, 059902 (2024)），与库内本地 PDF
  `Smeared_quasidistributions_in_perturbation_theory_Monahan_2018.pdf`（首页标注
  arXiv:1710.04607v3，Dated: September 26, 2024）内容一致。
- 正式发表：Phys. Rev. D 97, 054507 (2018)。

## 归一化说明
- revtex4-1 (prd, twocolumn) → `\documentclass[11pt]{article}` + geometry(a4,2.5cm)，
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hidelinks-hyperref，
  另加 `[numbers]{natbib}` 以保持 apsrev4-1 .bbl 的数字式引用。
- 源内全部 `\newcommand`（slash 记号、Ei/erf、ε_UV/ε_IR、bar 记号等）原样保留。
- siunitx 用法 `\SI{0.1}{fm}` 等改写为 `$0.1\,\mathrm{fm}$` 等标准写法；
  bigints/booktabs/color/multirow/ulem/verbatim 在正文中未使用，随 revtex 一并移除。
- 标题块重排：title/author/affiliation + 脚注式 arXiv/DOI/INT-PUB 行；
  `\keywords` 改为摘要后的斜体行；`\date{\today}` 按定稿固定为 September 26, 2024。

## 结构
- main.tex + chapters/section01–05.tex + chapters/backmatter.tex（致谢 + 附录 A/B + 参考文献）。
- 参考文献为源 .bbl（apsrev4-1，54 条）原样拼接，未删改。

## 图来源
- 全部 11 张图取自 arXiv 源包，原样复制到 `images/`（tree/qmatch1/qmatch2/qmatch_zpsi 为 PDF，
  zmu/hfn_re/hfn_im/cutoff_test/ir_re_test/ir_im_test 为 PNG），无占位图。

## 已知妥协点
- 单栏排版，图 2 的三行组合图中原 revtex 的负 vspace 对齐改为 `\\[8pt]` 行距方案，
  标号 (a)–(j) 对齐良好（已渲染页面核验）。
- 公式编号为 article 默认全局连续编号（含附录），非原刊按节编号。

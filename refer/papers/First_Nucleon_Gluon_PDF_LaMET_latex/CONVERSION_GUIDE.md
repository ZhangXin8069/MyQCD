# CONVERSION_GUIDE — First Nucleon Gluon PDF from Large Momentum Effective Theory

## 底稿来源
- arXiv:2505.13321v3 [hep-lat]（官方源 `https://arxiv.org/e-print/2505.13321`，gzip tar）
- 源文件：`main-PLB-v2.tex`（REVTeX4 双栏）+ `refs.bib` + `Figs/`（16 个 PDF 图）
- 本地库内 PDF（/root/PyQCD/refer/papers/…）用于核对首页书目信息；未走 PDF 重排路线。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(a4paper,margin=2.5cm)；统一宏包
  amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/[hidelinks]hyperref + float。
- 移除 REVTeX 私有构造：`twocolumn`、`\widetext`、`\preprint`、`\email`、`\affiliation`、
  `appendices` 环境（改用标准 `\appendix`）；标题块手工重排为 article 风格，
  保留 MSUHEP-25-024、日期与 arXiv 行（脚注式 email）。
- 未用到的原宏包（cases/slashed/physics/hhline/mathrsfs/ulem/multirow/tabularx/xcolor 等）删除；
  正文体未使用其任何宏。保留原自定义宏 `\slashp`、`\non`、`\UPDATE`（恒等透传）。
- 正文逐字保留（含摘要、致谢、附录、注释性文字中的引号样式微调除外）；
  `\UPDATE{...}` 为作者标记宏，按原文恒等展开。
- 图：16 个 Figs/*.pdf 原样复制到 `images/`，引用路径改为 `images/xxx`；无缺图。

## 参考文献
- 用 BibTeX(unsrt) 由官方 refs.bib 生成 .bbl（40 条），原样嵌入 chapters/backmatter.tex；
  编译不再需要 bibtex。条目未删改。

## 已知妥协点
- 双栏 → 单栏重排；figure*/widetext 宽环境在单栏下等价展开。
- 原文个别句子本身存在语法瑕疵（如 "with at two heavier"、"difference large-$\nu$"），
  忠实保留原文，未做修改。

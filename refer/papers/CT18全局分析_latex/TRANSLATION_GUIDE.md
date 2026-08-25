# TRANSLATION_GUIDE.md

## 来源
- 英文底稿：同目录姊妹目录 `../CT18_Global_Analysis_latex`（arXiv:1912.10053v2 转排），
  本目录为其全文中译：摘要、正文各节、图注、表注、脚注、致谢逐节翻译；
  数学公式照抄不改；人名、机构名、程序包名保留英文；参考文献列表保留英文原文。

## 约定
- 文档类 `ctexart`（11pt），字体 AR PL UMing CN / Droid Sans Fallback，
  `\emergencystretch=3em` 改善中西混排断行。
- 章节、公式、图表编号与英文版一一对应；`\label/\ref` 原样保留。
- 术语采用物理学界通用译名：parton distribution function→部分子分布函数、
  global fit→全球拟合、Hessian→Hessian 方法、profiling→剖析、nuisance parameter→讨厌参数、
  factorization scale→因子化标度、resummation→重求和、matching→匹配、smearing→涂抹、
  strangeness suppression→奇异性压低、intrinsic charm→内禀粲、standard candle→标准烛光。

## 图表与妥协点（继承英文版的已声明妥协）
- 图片直接复制自英文目录 `images/`（76 个文件）；每章仅收录前 4 个 figure 环境，
  其余图形位置保留占位框（"[figure unavailable -- see original paper]"），
  caption 已译出。表格全部保留原码，表头/表注已译。
- 补充材料按原文顺序置于参考文献之后（chapters/backmatter.tex）。

## 编译
`xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex`（两遍）。

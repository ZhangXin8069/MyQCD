# CONVERSION_GUIDE — Complete_NP_Renorm_QuasiPDF_latex

## 底稿来源
- arXiv 官方源 `https://arxiv.org/e-print/1706.00265`（gzip tar）：
  `PDFs_NPrenorm_v2.tex` + `PDFs_NPrenorm_v2.bbl` + 18 个 EPS 图。
- DOI 行（10.1016/j.nuclphysb.2017.08.012）转录自 arXiv abs 页面。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(a4paper,2.5cm)；去掉 REVTeX 残留选项、
  typearea/t1enc/arydshln/tikz/ulem/caption/multirow 等正文未实际使用的宏包。
- 原 `\abstract{...}` 命令改为标准 abstract 环境。
- 保留源文件自带宏：`\MSb`、`\Re/\Im` 重定义、`\be\ee\bea\eea\cl`；eqnarray 结构照旧。
- 正文逐字保留，包括原文拼写笔误（如 non-pertubative、transverity、"we have extend"、
  "does not dependent"）与重复标签 `sub3.2`（两处小节同名 label → 编译警告，
  非错误；为忠实原文未改动）。
- 标题块重排：title/author/affiliations + 脚注通讯作者行 + 文末期刊卷页 DOI/arXiv 行。

## 图来源
- `images/*.eps` 为 arXiv 源包原图原样复制；xelatex+ghostscript 自动转 EPS 内嵌。
- ETMC 合作组 logo（etmc.eps）保留在标题页。

## 参考文献
- `.bbl` 内容原样放入 `chapters/backmatter.tex`（elsarticle-num 排版格式），未删改条目。

## 已知妥协点
- 无。全部图、表、脚注、附录级内容（本文无附录）完整。

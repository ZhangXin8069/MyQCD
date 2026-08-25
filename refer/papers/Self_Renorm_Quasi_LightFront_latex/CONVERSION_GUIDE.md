# CONVERSION_GUIDE

- 来源：arXiv 官方 LaTeX 源 `arXiv:2103.02965`（e-print tar，2021-03-05 版），主文件
  `linear_divergence.tex` + `linear_divergence.bbl`（apsrev4-1 生成）+ `figures/`（117 个 PDF/PNG）。
- 归一化：`\documentclass[11pt]{article}` + geometry(a4,2.5cm)；统一宏包 amsmath/amssymb/mathtools/
  graphicx/microtype/enumitem/url/hidelinks-hyperref；另加 xcolor、bm、booktabs、array
  （正文表格 `\toprule`、`\multicolumn{...<{\centering}}` 与 `\bm` 向量所需，均为 TeX Live 标准件）。
- 结构：main.tex（序言+标题块+摘要+`\input`）+ chapters/section01–09.tex（每 `\section` 一文件）
  + chapters/backmatter.tex（致谢 + 原样内嵌的 thebibliography，71 条未删改）。
- 图片：全部源图复制到 `images/` 并以相对路径引用；无占位图。
- 已知妥协点：
  1. 删除作者自己用 `\iffalse…\fi` 屏弃的四段草稿文字与其中红字批注（正式版不含这些内容）；
     正文其余文字逐字保留。
  2. 废弃宏包 `subfigure` 的 `\subfigure[]{…}` 改写为自定义 `\panel{字母}{选项}{图}`（minipage 实现，
     双栏并排、图下标 (a)–(f)，与原图注引用一致）；revtex 的 title/collaboration/affiliation 重排为
     article 标题块，通讯邮箱以脚注保留。
  3. 单栏排版替代原 revtex 双栏预印本样式；编号沿用 article 默认。
  4. .bbl 中 apsrev4-1 辅助命令随 bbl 自带 providecommand，在 article 下可直接编译。

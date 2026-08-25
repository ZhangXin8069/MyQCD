# CONVERSION_GUIDE — Chiral_Symmetry_YM_Gradient_Flow_latex

## 底稿来源
- arXiv:1302.5246 官方 LaTeX 源（plain TeX 格式：main.tex + format/macros/title/sect1-10/appa-appe/biblio），
  `curl https://arxiv.org/e-print/1302.5246` 获取。
- 与库内 PDF（Luscher 2013, JHEP 04 (2013) 123）同源核对。

## 归一化说明
- `\documentclass[11pt]{article}` + geometry(a4paper,margin=2.5cm)；统一宏包按 SPEC §2.2。
- 原 plain TeX 机制以兼容层在 main.tex 序言中重建，正文逐字保留：
  - `\section N. Title \par` / `\subsection` / `\appendix` 定界宏改为 lussec/lussubsec/lusapp
    （改名避免与 LaTeX \section 冲突——thebibliography 内部调用 `\section*`）；
  - `\equation{...\enum}` + 自制 `\displaylines`（照抄 plain.tex）保持公式编号 (节.序)；
  - `\cases`、`\topinsert/\endinsert`（minipage 实现）、`\figurecaption`、`\tablecaption`、`\sfn`（双参脚注）。
  - 原宏包文件 macros -> luescher-macros.tex：`\Bbb->\mathbb`、`\frak->\mathfrak`、
    删除其 `\frac/\Im/\Re/\ring` 重定义（用 LaTeX 标准等价物）、新增 `\mib=\boldsymbol`；其余逐字保留。
- 引用：源内数字标签机制（biblist.tex + `\ref{Name}`）改写为标准 `thebibliography`
  + `\cite{Name}`，条目文本逐字未动、顺序不变（编号与原文一致）。
- 表 1、表 2 由原 plain TeX `\settabs\+` 对齐重排为 LaTeX tabular，数据逐字核对保留。

## 图来源
- Fig.1：源包 plots/wi.eps -> images/wi.pdf（epstopdf），caption 逐字保留。

## 已知妥协点
- 无。正文（含摘要、脚注 x5、致谢、附录 A-E、参考文献全部条目）逐字转排，无占位内容。
- 页面版式为统一 article 单栏，不模仿原刊；公式编号机制与原文一致。

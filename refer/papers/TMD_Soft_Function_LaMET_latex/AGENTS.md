# AGENTS.md

本目录为论文 "Lattice-QCD Calculations of TMD Soft Function Through Large-Momentum
Effective Theory" (arXiv:2005.14572, PRL 125, 192001) 的英文归一化 LaTeX 转排
（源：arXiv 官方 e-print，详见 CONVERSION_GUIDE.md）。

编译（两遍）：
```
cd TMD_Soft_Function_LaMET_latex && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```
成品：`build/main.pdf`。结构：`main.tex` + `chapters/section01–05.tex` +
`chapters/backmatter.tex`（致谢+补充材料+参考文献）+ `images/`。

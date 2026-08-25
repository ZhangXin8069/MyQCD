# Locally_Smeared_OPE_latex

Monahan & Orginos, "Locally smeared operator product expansions in scalar field theory",
Phys. Rev. D 91, 074513 (2015), arXiv:1501.05348 —— 英文原文归一化 LaTeX 转排（单栏 article）。

编译：
```bash
cd Locally_Smeared_OPE_latex && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # ×2
```

结构：`main.tex` + `chapters/section01..07.tex`（正文）+ `chapters/backmatter.tex`（致谢+参考文献，逐字保留）；图在 `images/`。详见 `CONVERSION_GUIDE.md`。

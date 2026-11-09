# 局域涂抹算符乘积展开_latex

Monahan & Orginos, "Locally smeared operator product expansions in scalar field theory"
（Phys. Rev. D 91, 074513 (2015); arXiv:1501.05348）的全文中文译本（ctexart 单栏排版）。

编译：
```bash
cd 局域涂抹算符乘积展开_latex && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # ×2
```

结构：`main.tex` + `chapters/section01..07.tex` + `chapters/backmatter.tex`（中文致谢+英文原参考文献）；图在 `images/`。约定见 `TRANSLATION_GUIDE.md`。

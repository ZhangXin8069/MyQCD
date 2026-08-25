# AGENTS.md

本目录是 Ji/Zhang/Zhao《More On Large-Momentum Effective Theory Approach to Parton Physics》(Nucl. Phys. B 924, 366 (2017), arXiv:1706.07416) 的 LaTeX 转排版。

编译（需两遍以生成交叉引用）：

```bash
cd More_On_LaMET_Parton_Physics_latex && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

成品：`build/main.pdf`。结构见 `CONVERSION_GUIDE.md`。

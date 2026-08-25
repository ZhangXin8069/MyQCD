# AGENTS.md

Large-Momentum Effective Theory (Rev. Mod. Phys. 93, 035005 (2021), arXiv:2004.03543)
的英文 LaTeX 转排目录（由 arXiv 源归一化重排）。

编译：
```bash
cd LaMET_RMP_Review_latex && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # ×2
```
成品: `build/main.pdf`。结构: `main.tex` + `chapters/*.tex` + `chapters/backmatter.tex` + `images/*.pdf`。

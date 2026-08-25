# AGENTS.md — 夸克禁闭_latex

K. G. Wilson《夸克禁闭》("Confinement of quarks", PRD 10, 2445 (1974)) 中文版 LaTeX——格点规范理论开创性论文，由英文版 `../Confinement_of_quarks_latex/` 逐节翻译。

## 结构

`main.tex`（ctexart，六节 + 致谢 + 参考文献）；`chapters/section01.tex`–`section06.tex`（I–VI）+ `backmatter.tex`；`images/figN.png`（10 图，从英文版复制）；`TRANSLATION_GUIDE.md`；`build/`。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # 两遍
```

输出 `build/main.pdf`（约 24 页）。节编号罗马数字；图 `\caption*{图 N. ...}` 保持全局 Fig. 1–10；规范场变量 $\theta_{\mu\nu}$、重定标方块场 $f_{\mu\nu}$。

# AGENTS.md — Confinement_of_quarks_latex

K. G. Wilson《Confinement of quarks》(Phys. Rev. D 10, 2445 (1974)) 英文 LaTeX 转排——格点规范理论开创性论文。

## 结构

`main.tex`（article 类）+ `preamble.tex`（宏包/物理宏 `\thl`/`\ev`/`\dd`/`\Tr`/`\order`）；`chapters/section01.tex`–`section06.tex`（每节一个文件，罗马数字 I–VI）+ `backmatter.tex`；`images/figN.png`（10 图）；`extract/pageNN.txt`（原始提取，只读）；`CONVERSION_GUIDE.md`；`build/`。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # 两遍
```

## 关键约定

- 公式自动编号 `(2.1)`、`(3.1)`…；图用 `\caption*{Fig. N. ...}` 保持全局 Fig. 1–10
- 规范场变量为 $\theta_{\mu\nu}$（扫描件常误读为 A/B/8）；重定标方块场 $f_{\mu\nu}$
- 使用 `preamble.tex` 宏而非自造记号
- 中文译本：`../夸克禁闭_latex/`

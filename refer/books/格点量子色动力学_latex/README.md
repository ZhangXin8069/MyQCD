# 格点量子色动力学——中文版 LaTeX

英文原书：

> **C. Gattringer 与 C. B. Lang, *Quantum Chromodynamics on the Lattice:
> An Introductory Presentation***, Lecture Notes in Physics **788**,
> Springer (2010), DOI 10.1007/978-3-642-01850-3

本目录是依据英文版 LaTeX 转写逐章翻译而成的**中文版**。正文已翻译为简体中文（采用标准粒子物理/格点场论术语），全部公式、编号、插图与原版一致，参考文献保留英文原文。

## 目录结构

```
格点量子色动力学_latex/
├── main.tex                  # 主文件（ctexbook）：标题页、目录、各章
├── preamble.tex              # 宏包、页面几何、物理宏（ctex 适配）
├── chapters/
│   ├── preface.tex           # 前言
│   ├── chapter01.tex … chapter12.tex
│   └── appendix.tex          # 附录
├── images/                   # 插图（与英文版共用，34 张 PNG）
├── build/                    # 编译输出（main.pdf）
├── TRANSLATION_GUIDE.md      # 翻译规则与中文术语对照
├── figures_map.md            # 图表号 → 文件 映射
└── README.md
```

## 编译

```bash
cd 格点量子色动力学_latex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # 跑两遍
```

编译产物为 `build/main.pdf`（约 392 页）。

要求：`xelatex`（TeX Live）+ `ctex` 宏包 + 中文字体（本机为 AR PL 文鼎字体，ctex 自动选用）。

## 说明

- **正文**由英文版 LaTeX 翻译而来；**公式**保持原样（语言无关），编号与原书一致。
- **插图**沿用英文版从原书 PDF 裁剪的 300 dpi PNG，见 `figures_map.md`。
- 与英文版相比页数略少（中文更紧凑）。
- 数学为从原书 PDF 重建的最佳努力结果；翻译亦为最佳努力，术语以中文格点 QCD 惯用表达为准。

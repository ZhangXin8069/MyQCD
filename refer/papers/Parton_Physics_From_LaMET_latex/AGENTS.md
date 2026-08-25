# Parton_Physics_From_LaMET_latex

Xiangdong Ji, "Parton Physics from Large-Momentum Effective Field Theory",
Sci. China Phys. Mech. Astron. 57, 1407–1412 (2014)（arXiv:1404.6680）
的归一化单栏 LaTeX 转排版；正文逐字保留，图与参考文献完整。

## 编译

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍
```

成品：`build/main.pdf`。底稿来源与妥协点见 `CONVERSION_GUIDE.md`；
中文译本见 `../大动量有效理论与部分子物理_latex/`。

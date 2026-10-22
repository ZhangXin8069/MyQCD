# 4150 对照报告 PDF 验收

报告：`docs/report_donghx_4150_reproduction_20260829.pdf`

## 编译

在仓库内隔离目录 `.pdfcheck.4FppeV/build-next/` 执行 XeLaTeX 两遍：

```
xelatex -interaction=nonstopmode -halt-on-error \
  -output-directory=../.pdfcheck.4FppeV/build-next \
  report_donghx_4150_reproduction_20260829.tex
xelatex -interaction=nonstopmode -halt-on-error \
  -output-directory=../.pdfcheck.4FppeV/build-next \
  report_donghx_4150_reproduction_20260829.tex
```

结果：

```
exit code: 0
pages: 23
page size: 453.54 x 255.12 pt (16:9)
Overfull: 0
Float too large: 0
Missing character: 0
LaTeX Warning: 0
```

## 渲染与目检

使用 `pdftoppm -png -r 120` 渲染得到 23/23 页；联系页为：

```
.pdfcheck.4FppeV/render-next/contact-01.png
.pdfcheck.4FppeV/render-next/contact-02.png
.pdfcheck.4FppeV/render-next/contact-03.png
```

23 页均已覆盖检查；新增的 momentum-smear 输出级页、结论页、smear 边界页和
验收页另以原尺寸复核，未见裁切、遮挡、越界或不可读表格。

## 2026-08-30 极化输出级更新

源文件：`docs/report_donghx_4150_reproduction_20260830.tex`。

在仓库临时目录 `.pdfcheck.20260830.GrEryJ/` 完成两遍 XeLaTeX：

```text
xelatex -interaction=nonstopmode -halt-on-error \
  -output-directory=.pdfcheck.20260830.GrEryJ \
  docs/report_donghx_4150_reproduction_20260830.tex
xelatex -interaction=nonstopmode -halt-on-error \
  -output-directory=.pdfcheck.20260830.GrEryJ \
  docs/report_donghx_4150_reproduction_20260830.tex
```

两遍退出码均为 `0`；`xelatex-1.log` 与 `xelatex-2.log` 中
`Overfull`、`Float too large`、`Missing character` 均为 0。最终 PDF 为 27 页，
页尺寸 `453.54 x 255.12 pt`（16:9）；`pdftoppm -png -r 120` 渲染得到 27/27 页。
联系页及新增极化页、边界页、验收页、映射页均以原尺寸检查，未见裁切、遮挡、越界或
不可读内容。

本次续验使用仓库内临时目录 `.pdfcheck.20260830.GrEryJ/fresh/` 重新编译两遍；两遍
退出码均为 `0`。第二遍日志中的交叉引用、`Overfull`、`Float too large`、
`Missing character`、`Underfull` 均为 `0`，并额外核对 `overfull_hbox=0`、
`overfull_vbox=0`；`frames_expected=27=pages_actual=pages_rendered`。使用
`pdftoppm -png -r 100` 生成 27 页渲染图，联系页分组为
`.pdfcheck.20260830.GrEryJ/contact-{1,2,3}.png`；27 页均已目检，记录
`occlusion_pairs=0`、`clipped_objects=0`、`outside_safe_area=0`。

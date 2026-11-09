# CONVERSION_GUIDE.md

## 底稿来源
- arXiv 官方源：`https://arxiv.org/e-print/1706.07416`（gzip 单文件 `mk_eu_new.tex`，2017-09-18 版），
  解包于 `/tmp/opencode/work/More_On_LaMET_Parton_Physics/src/`。
- 调度方提供的库内 PDF 路径（/root/PyQCD/...）不存在；未使用 PDF 兜底。
- 期刊信息 Nucl. Phys. B 924, 366–376 (2017) 来自调度方输入，转录于标题脚注。

## 归一化说明
- `revtex4` → `article` (11pt) + geometry/a4paper/margin=2.5cm；
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/hyperref[hidelinks]。
- 去掉的宏包：mathrsfs、amsfonts(并入amssymb)、slashed、array、verbatim、epsfig、color、bm
  （对应宏 `\x\y\z\n\U\tr\ttau\teta\Blue\TODO...` 在正文中均未使用，仅保留实际用到的
  `\ep \slashp \beq \eeq \nn` 与 `\Sec\App\Eq\Eqs\Ref` 等引用快捷命令）。
- 标题块重排：title/author/affiliation → `\thanks` 脚注式单位 + DOI/arXiv/preprint 行；
  `\preprint{MIT-CTP/4914}` 移入标题脚注。摘要按 article 惯例移至 `\maketitle` 之后。
- 正文散文逐字保留，含原文拼写笔误（Eulidean、renomalization、distribtutions、
  Minskowskian、guage、onshell、"quality of Eqs." 等），未作改动。

## 已声明的两处最小编辑（非散文内容）
1. §4 中 "the quality of Eq. (11) and (12)" 的硬编码编号指向原 preprint 排版的两个
   Ioffe 时间关联函数公式；本版为其添加 `\label{eq:covitd}`、`\label{eq:lccorrel}`
   并改用 `\ref` 动态引用（措辞未动）。
2. §2 首段 "as in Eq. (1)" 同样改为 `\Eq{eq:fact}`（本版中恰为式 (1)）。

## 图表
- 原文无图无表；无 images/ 目录。

## 其他
- 参考文献 thebibliography 30 条逐字保留（含 %%CITATION 注释）。
- 原 Eq.(13)（pseudo 分布定义）行内含一个全角空格 U+3000，已替换为普通空格（纯空白修正）。

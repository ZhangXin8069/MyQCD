# TRANSLATION_GUIDE — NNPDF17高精度数据部分子分布_latex

## 来源
- 译自本库英文转排目录 `../NNPDF17_High_Precision_Data_latex/`（arXiv:1706.00428 官方源）。
- 章节、公式、图表编号与英文版一一对应；数学公式与图代码逐字照抄。

## 约定
- 文档类 `\documentclass[11pt]{ctexart}`；中文字体 AR PL UMing CN / Droid Sans Fallback；
  行距 1.18，`\emergencystretch=3em`。microtype 与 XeLaTeX+CJK 冲突，中文版禁用。
- 术语：closure test→封闭性检验；Hessian→Hessian；Monte Carlo replicas→蒙特卡罗副本；
  matching→匹配；intrinsic charm→内禀粲；strangeness→奇异味；fixed-target→固定靶；
  rapidity→快度；luminosity→亮度；tolerance→容忍度；resummation→重求和；
  MHOU→缺失高阶不确定度；smearing/matching 等按学界通用译名。
- 人名、机构、程序名、PDF 集合名、URL 与参考文献列表保留英文。

## 妥协点（重要）
1. ~~五张共享大表以英文原表 PDF 嵌入~~ **已修复（2026-08-26）**：5 类大表（数据集总表×3、
   运动学切割、chi² 表×2）已整体移植原生 table 环境并保留中文 caption；根因为 ctexart/
   xeCJK 下数学上标内老式 `\rm` 组含 `\bar{\nu}` 触发 XeTeX「bad native font flag」内部
   错误，将该单元格改写为 `\sigma^{\mathrm{CC},\bar{\nu}}$` 等价形式后消除。原降级嵌入
   的 images/A1–D.pdf 已无引用（文件保留未删）。历史记录：初版因
   C/D.pdf=两张 chi² 表）。原因：ctexart/xeCJK 环境下这三类 tabular 触发 XeTeX
   "bad native font flag" 内部错误（英文原表同样复现，article 类正常），三轮排错未果，
   按 SPEC 降级处理。表中 label 移入中文 caption，交叉引用与编号保持一致；
   各表中文译文以中文 caption 完整给出。
2. DOI 具体后缀未能在允许域名内核实，标题脚注标 `[?]`（同英文版）。
3. 英文原文少量笔误（Ball:16neh→2016neh、"1.110"等）已按上下文更正并在 section06 注明；
   section02 中被注释的 $t_0$ 表格讨论段保持注释状态并以一行说明代替。
4. 参考文献列表为 .bbl 原文照录（chapters/bibliography.tex），不译。

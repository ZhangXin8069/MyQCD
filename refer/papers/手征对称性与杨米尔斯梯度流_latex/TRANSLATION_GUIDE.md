# TRANSLATION_GUIDE — 手征对称性与杨米尔斯梯度流_latex

## 来源
- 英文母本：同库 `Chiral_Symmetry_YM_Gradient_Flow_latex/`（arXiv:1302.5246 转排版）。
- 原文：M. Lüscher, JHEP 04 (2013) 123。

## 约定
- `\documentclass[11pt]{ctexart}`；中文字体按规范固定
  （AR PL UMing CN / Droid Sans Fallback）。
- **逐节忠实翻译全部散文**：摘要、各节及小节标题、图注、表注、脚注（×2 类 dagger 注 ×5）、致谢、附录 A–E。
- 数学公式、公式编号 (节.序)、章节/图表编号与英文版一一对应；
  公式块由构建脚本从英文版逐字抽取嵌入（`asm.py`，括号配平含 `\{` 处理），未作任何改动。
- 人名/机构保留原文；参考文献列表整体保留英文（thebibliography 原样复制）。
- 表 1、表 2 数据与英文版逐字相同，仅表题译为中文。
- Fig.1 图形文件直接复制自英文目录 `images/wi.pdf`。

## 术语表（主要）
gradient flow 梯度流 | flow time 流时间 | chiral condensate 手征凝聚 |
pseudo-scalar 赝标 | improvement 改善 | counterterm 抵消项 |
Lagrange multiplier 拉格朗日乘子 | Wick contraction Wick 收缩 |
smearing 涂抹/光滑化 | step scaling 步长标度 | Schrödinger functional 薛定谔泛函 |
random source 随机源 | jackknife jackknife 刀切法 | contact term 接触项

## 妥协点
- UMing 无粗体/斜体字形，标题处由 ctex 自动替换（编译警告，非错误）。
- 正文个别英文排版惯用语（如 "canonical normalization"）保留英文原词以避免歧义。

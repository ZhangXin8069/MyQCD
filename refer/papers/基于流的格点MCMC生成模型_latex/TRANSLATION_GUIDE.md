# TRANSLATION_GUIDE — 基于流的格点MCMC生成模型_latex

## 来源
- 译自本库英文转排目录 `../Flow_Generative_MCMC_Lattice_latex/`（其底稿为
  arXiv:1904.12072 官方源，PRD 100, 034515 (2019)）。
- 章节、公式、图表、脚注编号与英文版一一对应。

## 约定
- `\documentclass[11pt]{ctexart}`；字体 AR PL UMing CN / Droid Sans Fallback；
  行距 1.05，`\emergencystretch=3em`（参照 books/夸克禁闭_latex 设置）。
- 全部散文逐节忠实翻译：摘要、标题、小节名、图表注、脚注、致谢。
- 数学公式一律照抄不改；附录 A 公式中被划掉的期望值保留 \cancel 划线。
- 人名、机构、参考文献列表保留英文（58 条 bbl 与英文版同一文件）。
- 术语采用通用译名：normalizing flow→归一化流，coupling layer→耦合层，
  critical slowing down→临界慢化，integrated autocorrelation time→积分自相关时间，
  acceptance rate→接受率，proposal distribution→提议分布，ensemble→系综，
  pole mass→极点质量，susceptibility→磁化率，bootstrap resampling→bootstrap 重采样；
  Hybrid Monte Carlo 首译作"杂交蒙特卡洛（Hybrid Monte Carlo, HMC）"，其后沿用 HMC。

## 妥协点
- 附录 A 中两处条件竖线的英文条件文字（"all proposals ... rejected" 等）按原文
  保留英文以维持公式紧凑；其余公式内嵌文字均照抄原文。
- 图为原 arXiv 源 PDF 图（英文图内标注未重绘），图注已翻译。

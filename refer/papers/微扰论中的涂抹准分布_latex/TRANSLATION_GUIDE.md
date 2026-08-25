# TRANSLATION_GUIDE — 微扰论中的涂抹准分布_latex

## 来源
- 译自本库英文转排版 `../Smeared_Quasidists_Perturbation_latex/`，
  底稿为 arXiv:1710.04607v3（勘误后版本，对应 PRD 97, 054507 (2018) + Erratum 110, 059902）。

## 约定
- `\documentclass[11pt]{ctexart}`；字体 AR PL UMing CN / Droid Sans Fallback；
  行距 1.05、emergencystretch 3em（参照 夸克禁闭_latex 模板）。
- 逐节忠实翻译全部散文（标题、摘要、关键词、小节名、图注、脚注、致谢、附录）；
  数学公式、宏命令与英文版逐字一致；人名、机构、参考文献列表保留英文。
- 术语：quasidistribution→准分布；pseudodistribution→赝分布；smeared→涂抹；
  gradient flow→梯度流；flow time→流时；light-front→光前；
  matching→匹配；renormalization→重正化；power divergence→幂次发散；
  ringed fermions→环标费米子（首次出现附英文）；step-scaling→步标度。
- 章节/公式/图表编号与英文版一一对应（article 默认连续编号）；
  图直接复制英文目录 `images/`，标签（label）保持英文原样。

## 妥协点
- 参考文献为英文 .bbl 原样保留（54 条，natbib 数字模式）。
- 原文中个别笔误（如 3.5 节公式用 $a(\oz^2)$ 而正文称 $c(\oz^2)$、$\log(8\pi\mu^2t)$ 的 t）
  系 v3 定稿原样，翻译未作更动。

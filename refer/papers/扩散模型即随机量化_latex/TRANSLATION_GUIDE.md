# TRANSLATION_GUIDE — 扩散模型即格点场论中的随机量化

## 来源
- 由英文版 `../Diffusion_Stochastic_Quantization_latex/`（arXiv:2309.17082v2，
  Accepted at JHEP）逐节忠实翻译；章节/公式/图表编号一一对应。

## 约定
- `\documentclass[11pt]{ctexart}`；字体固定 AR PL UMing CN / Droid Sans Fallback，
  行距 1.08 + emergencystretch（参照 books/夸克禁闭_latex 惯例）。
- 数学公式、参考文献条目（.bbl 原文）、人名、机构地址保留英文；
  机构地址行给出中文意译并保留原文地名/邮编。
- 术语：diffusion model→扩散模型，score→分数（score），denoising→去噪，
  stochastic quantization→随机量化，critical slowing down→临界慢化，
  hopping parameter→跳跃参数，smearing→涂抹，integrated out→积掉，
  trivializing flow→平凡化流，accept/reject→接受/拒绝。
- 图 15 幅直接复制自英文目录 images/，路径相同。

## 妥协点
- 表 tab:observables 首列 data-set 标签按原文保留英文（Training/Testing/
  Generated (HMC/DM)）。
- 原文个别修订痕迹花括号分组未在译文中复现，不影响内容完整性。

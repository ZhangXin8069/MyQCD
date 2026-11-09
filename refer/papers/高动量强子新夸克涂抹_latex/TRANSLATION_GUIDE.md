# TRANSLATION_GUIDE.md

- **来源**: 英文转排版 `../Novel_Quark_Smearing_High_Momenta_latex/`
  （底稿 arXiv:1602.05525 官方 LaTeX 源）；逐节忠实翻译。
- **结构/编号**: 章节、公式、图表、脚注编号与英文版一一对应；
  数学公式照抄未改；标签（\label）与英文版相同。
- **术语约定**: smearing→涂抹；momentum smearing→动量涂抹；interpolator→内插算符；
  smeared-smeared/smeared-point→涂抹-涂抹/涂抹-点；boost(ed)→助推（boost 保留）；
  quasi-PDF→准部分子分布；TMD→横动量依赖部分子分布；covariant Laplacian→协变拉普拉斯算子；
  distillation→distillation（蒸馏）；perambulator 保留英文；lattice artefacts→格点人为效应；
  staples/staple 路径保留英文并加注。
- **保留英文**: 人名、机构名、Email、参考文献列表（58 条原样）、软件名
  （CHROMA、QPACE 等）。
- **字体**: 正文 AR PL UMing CN，黑体/等宽 Droid Sans Fallback（SPEC 指定）；
  编译时出现 UMing 粗体/斜体字形替换警告属正常回退，不影响输出。
- **妥协点**: 无占位图（11 张图全部来自 arXiv 源）；`\mathds` 因本机无 dsfont.sty
  以 `\mathbb` 等价替换（同英文版）。

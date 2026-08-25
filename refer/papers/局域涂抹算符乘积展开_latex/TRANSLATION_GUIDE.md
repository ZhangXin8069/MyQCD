# TRANSLATION_GUIDE — 局域涂抹算符乘积展开_latex

## 来源
- 英文底稿：本仓库 `Locally_Smeared_OPE_latex/`（arXiv:1501.05348v2 官方源转排），
  Phys. Rev. D 91, 074513 (2015)。
- 本目录为该文全文中文译本，章节/公式/图表编号与英文版一一对应。

## 约定
- 文档类 ctexart（xelatex）；中文字体：正文 AR PL UMing CN，无衬线/等宽 Droid Sans Fallback。
- 全部散文（标题、摘要、小节名、图注、致谢）逐节忠实翻译；数学公式、标签、引用键照抄英文版不改。
- 人名、机构、参考文献列表保留英文；参考文献块与英文版逐字节相同。
- 术语：smearing→涂抹；gradient flow→梯度流；flow time→流时间；
  Wilson coefficients→威尔逊系数；power-divergent mixing→幂次发散混合；
  small flow-time expansion→小流时间展开；step-scaling→步标度；
  renormalization group→重正化群；anomalous dimension→反常维数；
  connected/disconnected→连通/非连通；counterterm→反抵消项。
- 正文 "Eq.~(58)" 为原文硬编码编号，两版均按原样保留。

## 编译
```bash
cd 局域涂抹算符乘积展开_latex && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex   # ×2
```

## 妥协点
- 式 (eq:rhotau_mutau) 一行在原 arXiv 源中即存在花括号排版瑕疵（\widetilde 参数未闭合仍可编译），
  中文版已按式 eq:rhotau 的正确结构补全为 \widetilde{\phi}(p_1)，数学含义不变。

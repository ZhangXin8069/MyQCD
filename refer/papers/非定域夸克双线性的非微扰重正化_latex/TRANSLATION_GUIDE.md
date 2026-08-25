# TRANSLATION_GUIDE.md

## 来源
- 底稿：英文转排版 `../Nonpert_Renorm_Quark_Bilinears_latex/`（arXiv:1707.07152
  官方源归一化重排，PRL 121, 022004 (2018)）。
- 中文版逐段忠实翻译：摘要、标题、脚注、图注、致谢全部译出；数学公式照抄不改。

## 约定
- 文档类 `ctexart`（11pt）；中文字体 AR PL UMing CN / Droid Sans Fallback；
  行距与 emergencystretch 设置参照 `refer/books/夸克禁闭_latex/main.tex`。
- 图直接复制自英文目录 `images/`；Figure/公式编号与英文版一一对应
  （Fig.1=Eeff, Fig.2=Zphi_ratio_vs_both, Fig.3=Zphi_scatter,
  Fig.4=hel_comp+hel_comp_ren, Fig.5=hel_comp_ens, Fig.6=qpdf_hel_ren）。
- 人名、机构名保留英文；参考文献列表原样保留英文（`backmatter_bbl.tex`）。
- 术语：quasi-PDF→准部分子分布；smearing→涂抹；matching→匹配；
  renormalization→重正化；mixing→混合；twisted mass→扭转质量；
  static quark→静态夸克；ensemble→系综；lattice artifacts→格点人为效应；
  counterterm→抵消项；helicity→螺旋度。

## 委协点
- 主标题采用刊出版标题的直译《非定域夸克双线性算符的格点QCD非微扰重正化》，
  所据 arXiv 源早期标题已在标题脚注注明。
- 参考文献条目内的英文书名格式（utphys-noitalics 样式产物）未做汉化处理。

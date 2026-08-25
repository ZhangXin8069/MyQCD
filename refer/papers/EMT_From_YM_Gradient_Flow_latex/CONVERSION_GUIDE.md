# CONVERSION_GUIDE

- 论文: H. Suzuki, "Energy–momentum tensor from the Yang–Mills gradient flow",
  Prog. Theor. Exp. Phys. 2013, 083B03.
- 底稿来源: arXiv 官方源 `arXiv:1304.0533`（e-print tar，主文件
  `EM_extended_ptep_ver6.tex`，v3, 2015-06-17）。库内未找到该论文本地 PDF，
  未使用 PDF 重排路线。
- 归一化: 原 `ptephy.cls`（PTEP 期刊类，随源附带）替换为标准
  `\documentclass[11pt]{article}` + geometry(2.5cm)；
  统一宏包 amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/
  booktabs/hyperref(hidelinks)。`\subjectindex{...}` 以注释保留。
- 结构: `main.tex` + `chapters/section01..05.tex` + `chapters/backmatter.tex`
  （致谢 + 附录 A + 参考文献）。公式按节编号（与原文标签一致）。
  附录在 article 类下编号为 A（原文 PTEP 排版同为附录 A；原 .tex 标签作
  sec:5/eq:(5.x)，仅内部键名不同，显示编号 A.1… 与原刊一致程度见 PDF）。
- 图: 源附 17 幅 EPS（diagram_1..17.eps），已复制到 `images/` 并用
  ghostscript 预转换为同名 PDF（XeLaTeX 直接可用；`\includegraphics` 无扩
  展名引用，优先取 .pdf）。图注按原文保留为空 caption。
- 表: Table 1（booktabs 原码保留）；仅将 `\tabcolsep` 由 20pt 调为 12pt 以
  适配 A4 版心。带 * 的更正数值照原文。
- 参考文献条目逐条照抄（含 %%CITATION 注释行）；删除了各 bibitem 中被源文
  件自身注释掉的论文标题行与 INSPIRE 引用计数注释行（不影响正文引用）。
- 已知妥协点:
  1) 源文件中以大段 LaTeX 注释形式存在的图 3–12/14–17 的中间表达式未排入
     正文（原刊亦不显示），已在 backmatter.tex 相应位置以注释说明；
  2) 未使用的私有宏 \Slash（依赖 \ooalign）省略；\Bar 以 \providecommand
     兜底定义；
  3) 编译器为 XeLaTeX（SPEC 规定），与源 pdfTeX 排版细节或有微小差异。

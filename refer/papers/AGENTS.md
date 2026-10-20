# AGENTS.md — papers（原文转排库与导读文选）

`papers/` 下共 102 个目录，分两类：

- **原文转排库**：50 篇精华论文的双语全文（100 个目录，2026-08-26 由 agent 生成）；
- **导读文选**：2 套 38 篇论文的英文/中文评注导读（2 个目录，2026-08-25 生成）。

文选与原文库互补：文选是评注导读，原文库是全文。两套文选目录实际位于本目录下，
不是 `refer/` 根目录。

## 结构约定

- 原文每篇两个目录：`<Slug>_latex/`（英文转排）+ `<中文名>_latex/`（中文译本）。
- 英文版：`article` 类；`main.tex` + `chapters/sectionNN.tex`（每节一文件）+
  `chapters/backmatter.tex`（致谢/附录/参考文献）+ `images/`；由 arXiv 官方源
  归一化改造而成（去除 REVTeX/elsarticle 等期刊私有宏，统一标准宏包），正文逐字保留。
- 中文版：`ctexart`（XeLaTeX，字体 AR PL UMing CN / Droid Sans Fallback）；逐节忠实翻译；
  公式照抄不改；人名与参考文献列表保留英文；插图复用英文目录 `images/`。
- 每目录应附 `CONVERSION_GUIDE.md`（英文版来源与妥协点）或 `TRANSLATION_GUIDE.md`
  （中文版约定）及简版 `AGENTS.md`。
- 导读文选为 `book`/`ctexbook` 类，`main.tex` 使用 `\input{../chapters/...}`，须在
  `build/` 内编译。

## 编译

```bash
# 原文转排
cd <目录> && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍

# 导读文选
cd <选集目录>/build && xelatex -interaction=nonstopmode -halt-on-error ../main.tex  # 两遍
```

当前工作区未保留任何 `build/main.pdf`；除 2026-10-21 复验的两套文选外，历史页数尚未复验。

## 索引与质量

- 总索引：`INDEX.md`，覆盖 50 篇原文（目录对 / 实测页数 / arXiv 底稿 / 备注）；
  两套导读文选单列在该文件的“导读文选”一节。
- 原文 100 个目录历史上 xelatex 两遍编译通过、日志零错误，合计 2460 页；
  该结论来自 2026-08-26 的历史记录，当前工作区无 PDF 可复核。
- 两套导读文选于 2026-10-21 复验：两遍编译零错误，英文 36 页、中文 35 页。
- 原 PARTIAL 2 处已于 2026-08-26 收尾修复：CT18 中英版补齐全量 234 图
  （arXiv:1912.10053 源、原始参数还原，EN 143→146 页 / ZH 140→143 页）；
  NNPDF17 中文版 5 类大表原生还原（xeCJK「bad native font flag」根因=数学上标内
  老式 `\rm` 组含 `\bar{希腊}`，改写为 `\mathrm{CC},\bar{\nu}` 等价形式后消除）。

## 已知缺口

- 20 个原文转排目录缺简版 `AGENTS.md`：19 个中文译本（`LaMET计算TMD软函数_latex`、
  `任意阶部分子分布矩_latex`、`伪部分子分布的单圈演化_latex`、`准PDF完整非微扰重正化方案_latex`、
  `准光前关联函数的自重正化_latex`、`准部分子分布的可重正性_latex`、
  `同位旋矢量分布的重正化匹配系统分析_latex`、`大动量有效理论再论_latex`、
  `微扰论中的涂抹准分布_latex`、`手征对称性与杨米尔斯梯度流_latex`、
  `扩散模型即随机量化_latex`、`格点算符非微扰重正化一般方法_latex`、
  `梯度流中的非光锥威尔逊线算符_latex`、`梯度流形式的双圈能动量张量_latex`、
  `梯度流高阶计算的技术与结果_latex`、`欧氏与光锥分布因子化定理_latex`、
  `胶子伪分布的短距行为_latex`、`规范等变的流采样_latex`、
  `高动量强子新夸克涂抹_latex`）和 1 个英文转排（`Parton_Physics_on_Euclidean_Lattice_latex`）。
  它们均已有所需的 `CONVERSION_GUIDE.md` 或 `TRANSLATION_GUIDE.md`。
- 两套导读文选目录（`Essential_Papers_on_Lattice_QCD_Parton_Physics_latex`、
  `格点QCD部分子物理精华论文选_latex`）缺 `AGENTS.md` 与 GUIDE；其结构由本文件与
  `../AGENTS.md` 约束。
- `anomalpap5.tex` 为 0 字节遗留文件，未被任何索引或 LaTeX 入口引用，待确认后删除。
- 未收录 5 篇前印本经典（无开放获取底稿）：Gross–Wilczek/Politzer 1973、
  Altarelli–Parisi 1977、Duane et al. 1987(HMC)、Collins–Soper 1981、Parisi–Wu 1981。
- 书目勘误：文选卡片中 Morningstar–Peardon 的 arXiv id 应为 hep-lat/0311018（非 0307022）。
- 生产日志：`.make.2026-08-25-08-59-10.log`；用户输入清单 `.agent.*.list`（均不入库）。

# 中文版翻译指南 — 格点QCD导论

中文版由英文版 LaTeX（`../INTRODUCTION_TO_LATTICE_QCD_latex/chapters/`）逐章翻译而来。
译文必须**保留全部 LaTeX 结构**，只翻译文字内容。

## 硬性规则

1. **保留结构**：`\chapter`/`\section`/`\subsection` 标题翻译成中文；方程环境、
   数学公式、`\label`、`\ref`/`\eqref`、图表环境、`\includegraphics{images/figN.png}`、
   编号一律**原样保留，不得改动**。
2. **翻译范围**：正文散文、小节标题、图题（caption）、表题与表格单元内容 → 中文；
   数学、符号、人名、文献编号、数值单位 → 保留。
3. **公式中的文字**：`\text{...}` 内的说明性文字可译成中文；数学符号不译。
4. **术语统一**：严格使用下表术语，全篇一致。
5. **语气**：忠实直译，不增删内容，不添加注释。
6. **人名**：国际通用人名保留原文（Wilson、Lüscher、Weingarten、Nielsen、Ninomiya、
   Schrodinger 等）；中文文献中常见译名可附注。
7. **输出**：写到 `格点QCD导论_latex/chapters/secNN_name.tex`（与英文版同名）。
8. 中文引号用 ``「」``，但 LaTeX 中建议直接使用中文引号字符或 `` `` '' `` 均可。

## 物理术语对照表（必须统一）

| 英文 | 中文 |
|------|------|
| lattice QCD / LQCD | 格点QCD |
| quark / antiquark | 夸克 / 反夸克 |
| gluon | 胶子 |
| action | 作用量 |
| gauge theory / gauge invariance / gauge field | 规范理论 / 规范不变性 / 规范场 |
| gauge fixing / gauge fixed | 规范固定 |
| local gauge symmetry | 定域规范对称性 |
| continuum limit | 连续极限 |
| Euclidean / Minkowski | 欧几里得 / 闵可夫斯基 |
| path integral | 路径积分 |
| partition function | 配分函数 |
| transfer matrix | 传递矩阵 |
| correlation function | 关联函数 |
| two-point / three-point correlation | 两点 / 三点关联函数 |
| effective mass | 有效质量 |
| Wilson fermions | 威尔逊费米子 |
| staggered fermions | 交错费米子 |
| naive fermion action | 朴素费米子作用量 |
| chiral symmetry / chiral limit | 手征对称性 / 手征极限 |
| spontaneous symmetry breaking | 自发对称性破缺 |
| fermion doubling problem | 费米子加倍问题 |
| plaquette | 方格 |
| Wilson loop | 威尔逊圈 |
| Wilson / Polyakov line | 威尔逊线 / 波利亚科夫线 |
| confinement / asymptotic freedom | 禁闭 / 渐近自由 |
| strong coupling expansion | 强耦合展开 |
| string tension | 弦张力 |
| renormalization / renormalized | 重整化 / 重整化的 |
| renormalized trajectory / fixed point | 重整化轨迹 / 不动点 |
| critical exponent / critical surface | 临界指数 / 临界超曲面 |
| lattice spacing | 格距 |
| hopping parameter | 跳跃参数 |
| clover action | 三叶草作用量 |
| tadpole / mean-field improvement | 蝌蚪图 / 平均场改进 |
| improved action | 改进作用量 |
| hadron spectrum / hadron | 强子谱 / 强子 |
| meson / baryon | 介子 / 重子 |
| glueball | 胶球 |
| quarkonium | 夸克偶素 |
| decay constant | 衰变常数 |
| interpolating operator | 插值算符 |
| operator / matrix element | 算符 / 矩阵元 |
| Ward identity | 沃德恒等式 |
| quark mass | 夸克质量 |
| quenched approximation | 淬火近似 |
| dynamical fermions | 动力学费米子 |
| phase transition | 相变 |
| deconfinement / chiral transition | 退禁闭 / 手征相变 |
| standard model | 标准模型 |
| coupling constant | 耦合常数 |
| Higgs / CKM matrix | 希格斯 / CKM 矩阵 |
| Haar measure | Haar 测度 |
| Gribov copies | Gribov 拷贝 |
| Monte Carlo | 蒙特卡洛 |
| gauge configuration | 规范组态 |
| renormalization constant | 重整化常数 |
| operator mixing | 算符混合 |
| mass inequality | 质量不等式 |
| strong coupling constant αs | 强耦合常数 αs |
| Schrodinger functional | 薛定谔泛函 |
| CP violation | CP 破坏 |
| quark masses m_u, m_d, ... | 夸克质量 m_u, m_d, ... |

## 译例

- "The goal of the lectures is ..." → "本讲义的目的是……"
- "as shown in Fig. 5" → "如图~\ref{fig:5} 所示"
- "i.e." / "e.g." / "etc." → 即 / 例如 / 等
- "Eq. (5.1)" → "式~\eqref{eq:5.1}"（保留 `\eqref` 结构）
- 英文双引号 "..." → 中文引号「...」

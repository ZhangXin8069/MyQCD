# PyQCD 参考索引

本文件只索引 PyQCD 子模块中的只读资料，不复制、不转排、不修改上游内容。

## 路径与来源

- 源码根：`refer/git-rep/PyQCD/`
- 上游参考根：`refer/git-rep/PyQCD/refer/`
- 上游 URL：<https://gitee.com/zhangxin8069/PyQCD.git>
- 当前检出：`0a2f85d30881fc8ead60972c0afb9c028abc348f`
- 已吸收文档入口：`docs/pyqcd_reference/README.md`

## 一级入口

| 路径 | 内容 | 主要用途 |
|---|---|---|
| `refer/git-rep/PyQCD/refer/books/` | 4 部著作的英/中 LaTeX 与 PDF，共 670 个文件 | 格点 QCD、量子场论、禁闭与谱学 |
| `refer/git-rep/PyQCD/refer/papers/` | 91 个原始论文 PDF | 梯度流、OPE、LaMET、重整化、PDF/TMD 与数值结果 |
| `refer/git-rep/PyQCD/refer/donghx/` | 质子两点函数、OPE、梯度流胶子 PDF 历史代码 | flow-to-quasi、算符与关联函数对照 |
| `refer/git-rep/PyQCD/refer/zhangxin/` | 胶子 PDF 全流程、输入输出与分析框架 | 从场强到 Fourier、matching 和统计 |
| `refer/git-rep/PyQCD/refer/huangcl/` | Chroma 多步流水线、RK3、ratio、matching、拟合 | 流程和数值实现交叉核验 |
| `refer/git-rep/PyQCD/refer/sush/` | 蒸馏、Wick 收缩、重采样和谱学分析 | 收缩拓扑与统计基元 |
| `refer/git-rep/PyQCD/refer/git-rep/` | 外部软件来源与二手分析文档 | 仅作来源导航；未初始化子模块不视为已验证源码 |

## 主题映射

下表中的 `refer/...` 路径均相对于上游参考根
`refer/git-rep/PyQCD/`。

| 主题 | 优先资料 |
|---|---|
| 格点 QCD 基础 | `refer/books/INTRODUCTION_TO_LATTICE_QCD_latex/`、`refer/books/Quantum_Chromodynamics_on_the_Lattice_latex/` |
| Wilson/gradient flow | `refer/papers/Properties_and_uses_of_the_Wilson_flow_in_lattice_QCD_Luscher_2010.pdf`、`refer/papers/Perturbative_analysis_of_the_gradient_flow_in_non-abelian_gauge_theories_Luscher_Weisz_2011.pdf` |
| 胶子 OPE 与非定域算符 | `refer/papers/Accessing gluon parton distributions in large momentum effective theory.pdf`、`refer/zhangxin/gluon_pdf_full_workflow.py` |
| 准 PDF/LaMET | `refer/papers/Parton Physics on Euclidean Lattice.pdf`、`refer/papers/Parton Physics from Large-Momentum Effective Field Theory.pdf`、`refer/papers/Factorization Theorem Relating Euclidean and Light-Cone Parton Distributions.pdf` |
| 非局域算符重整化 | `refer/papers/A complete non-perturbative renormalization prescription for quasi-PDFs.pdf`、`refer/papers/A Hybrid Renormalization Scheme for Quasi Light-Front Correlations in Large-Momentum Effective Theory.pdf` |
| 胶子 TMD 与 CS 核 | `refer/papers/Nonperturbative Determination of Collins-Soper Kernel from Quasi Transverse-Momentum Dependent Wave Functions.pdf`、`refer/papers/Lattice-QCD Calculations of TMD Soft Function Through Large-Momentum Effective Theory.pdf` |
| 强子关联函数与谱学 | `refer/books/INTRODUCTION_TO_LATTICE_QCD_latex/chapters/sec17_correlators.tex`、`sec18_hadron_spectrum.tex` |
| Wick 收缩与蒸馏 | `refer/sush/_distillation/corr_wick.py`、`corr_contraction.py` |
| 统计与拟合 | `refer/zhangxin/lsq_tools.py`、`refer/huangcl/_0xxx/fit_tools.py`、`refer/sush/_distillation/analyse.py` |

## 使用边界

- 原始 PDF 和上游代码的版权、许可与可再分发条件以各地上游文件为准，未逐项核验的内容不得复制进主包。
- `refer/papers/` 没有项目级 `INDEX.md`；文件身份以上游路径和文件本身为准，不从文件名
  推断未经验证的版本。
- `refer/git-rep/` 中的子模块和部分符号链接可能指向仓库外路径。工具不得递归跟随链接。
- 历史代码中的集群绝对路径、旧轴序或一次性脚本只作为来源证据，不能直接当作可复现接口。

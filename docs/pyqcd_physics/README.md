# PyQCD 物理说明

本目录是 MyQCD 的第一入口。目标是用可追溯的中文材料解释
`refer/git-rep/PyQCD` 中的物理对象、公式和算法，而不是平行维护另一套格点 QCD
实现。

## 证据层级

| 层级 | 本库位置 | 作用 |
|---|---|---|
| PyQCD 源码与文档 | `refer/git-rep/PyQCD/` | 接口、轴序、实现和历史约定的唯一事实源 |
| PyQCD 自带参考 | `refer/git-rep/PyQCD/refer/` | 书籍、论文、历史代码、外部软件参考；只读 |
| 可执行公式审计 | `myqcd/` | SymPy 恒等式、量纲、极限、有限维模型和 Wick 配对 |
| PyQCD 物理论述 | 本目录三份 PDF/TeX | 代码—公式—物理对象—验证边界的系统解释 |
| PyQCD 文档吸收 | `docs/pyqcd_reference/` | 上游 163 个格点 QCD 文档与历史报告的原样快照 |
| 本地文献转排 | `refer/papers/`、`refer/books/` | 可检索、可编译的中英文公式与教材辅助 |

## 建议阅读顺序

1. [`report_gluon_tmd_lattice_qcd_review_20261023.pdf`](report_gluon_tmd_lattice_qcd_review_20261023.pdf)
   给出核子胶子 TMD-PDF 的定义、格点算符、Dirac/BiCGSTAB 求逆、软/rapidity、重正化、梯度流、匹配、关键公式卡片，以及图形化的尺度窗口、误差预算与分级验收链。
2. [`report_pyqcd_lattice_qcd_theory_20260906.pdf`](report_pyqcd_lattice_qcd_theory_20260906.pdf)
   给出全链物理结构和源码入口。
3. [`report_gluon_tmd_gradient_flow_20260828.pdf`](report_gluon_tmd_gradient_flow_20260828.pdf)
   聚焦核子胶子 `f_1^g` 的 finite-staple 方案、soft/rapidity、匹配和停止门。
4. [`../pyqcd_reference/README.md`](../pyqcd_reference/README.md)
   查阅从 PyQCD 吸收的完整物理笔记、推导和历史报告。
5. [`../../refer/git-rep/docs/pyqcd-physics-reference.md`](../../refer/git-rep/docs/pyqcd-physics-reference.md)
   用于从主题跳转到 PyQCD 自带书籍、论文和原始代码。
6. [`../../myqcd/README.md`](../../myqcd/README.md) 用于运行公式审计和读取可执行证据。

## 物理链与代码入口

表中路径均相对仓库根目录。

| 物理环节 | PyQCD 源码入口 | 参考与原论文入口 | MyQCD 解释 |
|---|---|---|---|
| 格点规范场、SU(3) 链接、plaquette | `refer/git-rep/PyQCD/pyqcd/lattice/`、`pyqcd/smear/` | `refer/git-rep/PyQCD/refer/books/` | 理论报告“规范组态与场强”章节 |
| 蒸馏、传播子、顶点与 Wick 收缩 | `pyqcd/vertex/`、`pyqcd/contraction/` | `refer/git-rep/PyQCD/refer/sush/` | `myqcd/wick.py`; 理论报告“蒸馏与 Wick 收缩”章节 |
| 强子两点/三点关联函数与谱学 | `pyqcd/analysis/` | `refer/git-rep/PyQCD/refer/books/INTRODUCTION_TO_LATTICE_QCD_latex/` | 理论报告“关联函数与谱学”章节 |
| 断连图、比值、重采样与拟合 | `pyqcd/analysis/_disconnected.py`、`_ratio2pt.py` | `refer/git-rep/PyQCD/refer/zhangxin/`、`huangcl/` | 理论报告“统计与裸矩阵元”章节 |
| Clover 场强、Wilson line 与胶子 OPE | `pyqcd/operator/_gluon_ope.py`、`_tmd.py` | `refer/git-rep/PyQCD/refer/donghx/`、`zhangxin/` | 理论报告“胶子算符”章节 |
| Wilson/gradient flow 与 RK3 | `pyqcd/renorm/_gradient_flow.py` | `refer/git-rep/PyQCD/refer/huangcl/_0xxx/Wilson_Flow_RK3.py` | 理论报告“梯度流”章节 |
| `Z_R`、hybrid/self-renormalization | `pyqcd/renorm/_zr.py`、`_hybrid.py` | `refer/git-rep/PyQCD/refer/papers/` | 理论报告“重整化方案”章节 |
| NLO matching、Fourier 与 CS 核 | `pyqcd/renorm/_matching.py`、`_tmdextract.py` | `refer/git-rep/PyQCD/refer/papers/` | TMD 报告 |
| 核子胶子 TMD-PDF | `pyqcd/renorm/_tmd.py`、`pyqcd/pipeline/` | `refer/git-rep/PyQCD/refer/papers/` | TMD 报告 |

## 结果判定

一个物理结论只有在以下条件同时满足时才能升级：

1. 算符、投影、link class、轴序、归一化和单位均已固定。
2. 代数或算法检查通过，且失败边界可重现。
3. 梯度流、Wilson line、soft/rapidity、zero-bin 和 matching 属于同一方案。
4. `a`、`L`、`P_z`、`tau`、`ell`、`b_T` 等尺度窗口闭合。
5. 真实系综、统计误差、系统误差和连续极限均有机器可查证据。

缺少任一项时，只报告对应层级的原型或接口，不使用“完整 TMD-PDF 结果”这一表述。

"""课程的非论文来源注册表；论文 P01--P50 从 INDEX.md 单源解析。"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Source:
    title: str
    locator: str
    role: str


def _internal(title: str, role: str) -> Source:
    return Source(
        title=title,
        locator="docs/lattice_qcd_gluon_tmd_course/content/",
        role=role,
    )


SOURCES: Dict[str, Source] = {
    "BOOK-MATH": _internal("数学预备课（课程自编）", "补足高中到微积分、Fourier 和量纲分析的完整推导。"),
    "BOOK-NUMERICS": _internal("数值分析预备课（课程自编）", "差分、求积、收敛阶、线性求解和误差账本。"),
    "BOOK-LINALG": _internal("线性代数预备课（课程自编）", "向量、谱分解、张量指标和矩阵数值检查。"),
    "BOOK-GROUP": _internal("连续群与生成元预备课（课程自编）", "从旋转群过渡到 SU(2)/SU(3)。"),
    "BOOK-MECHANICS": _internal("作用量与经典力学预备课（课程自编）", "变分、Euler--Lagrange 与 Noether 思想。"),
    "BOOK-EM": _internal("规范势与经典场预备课（课程自编）", "Abelian 场强与规范冗余。"),
    "BOOK-QM": _internal("量子力学预备课（课程自编）", "态、算符、测量、谱与不确定关系。"),
    "BOOK-STAT": _internal("Monte Carlo 统计与拟合讲义（课程自编）", "协方差、重采样、覆盖率和模型系统学。"),
    "BOOK-QFT": Source(
        "An Introduction to Quantum Field Theory（仓库转排本）",
        "../PyQCD/refer/books/An_Introduction_to_Quantum_Field_Theory_latex/",
        "量子场论、规范理论、QCD 和重整化的主教材交叉核验。",
    ),
    "BOOK-LQCD": Source(
        "Introduction to Lattice QCD / 格点 QCD 导论（仓库转排本）",
        "../PyQCD/refer/books/INTRODUCTION_TO_LATTICE_QCD_latex/；../PyQCD/refer/books/格点QCD导论_latex/",
        "欧氏化、规范链接、费米子、连续极限和关联函数。",
    ),
    "BOOK-QCD-LATTICE": Source(
        "Quantum Chromodynamics on the Lattice（仓库转排本）",
        "../PyQCD/refer/books/Quantum_Chromodynamics_on_the_Lattice_latex/",
        "格点 QCD 形式体系、算法和系统误差的深入交叉核验。",
    ),
    "REPORT-TMD": Source(
        "梯度流核子胶子 TMD 项目报告",
        "docs/report_gluon_tmd_gradient_flow_20260828.pdf；docs/report_gluon_tmd_gradient_flow_20260828_2.pdf",
        "本课程终点定义、实现现状、证据分级和关键物理边界。",
    ),
    "MYQCD-FORMULAS": Source(
        "MyQCD 可执行公式注册表",
        "myqcd/formula_registry.py；myqcd/derivations.py；tests/test_myqcd_sympy.py",
        "复杂公式的 SymPy 精确代理与证据边界。",
    ),
    "MYQCD-COURSE-EXAMPLES": Source(
        "课程配套 SymPy 代码参考",
        "docs/lattice_qcd_gluon_tmd_course/myqcd/",
        "群论/QFT、格点谱学、重整化与 TMD 的 26 个可运行教学例题。",
    ),
    "DOC-3PT": Source("格点 QCD 中的三点函数构造", "../PyQCD/docs/格点QCD中的3pt构造.tex", "核子三点函数、谱分解和代码接口。"),
    "DOC-DGLAP": Source("格点 QCD 中的 DGLAP 演化", "../PyQCD/docs/格点QCD中的DGLAP演化方程.tex", "部分子演化与卷积。"),
    "DOC-DISCONNECTED": Source("连通图与非连通图", "../PyQCD/docs/格点QCD中的连通图与非连通图.tex", "断连拓扑与真空扣除。"),
    "DOC-EXTRAPOLATION": Source("格点 QCD 中的外推", "../PyQCD/docs/格点QCD中的外推.tex", "连续、有限体积和物理点外推。"),
    "DOC-FERMIONS": Source("格点费米子方案", "../PyQCD/docs/格点QCD中的费米子方案.tex", "倍增、Wilson/Clover 与方案比较。"),
    "DOC-FIELD-STRENGTH": Source("格点场强张量", "../PyQCD/docs/格点QCD中的场强张量.tex", "plaquette/clover 场强和约定。"),
    "DOC-GLUON-POLARIZATION": Source("胶子极化", "../PyQCD/docs/格点QCD中的胶子极化.tex", "胶子张量投影。"),
    "DOC-OPE": Source("格点 QCD 中的 OPE 算符", "../PyQCD/docs/格点QCD中的OPE算符.tex", "局域矩、twist 与算符基底。"),
    "DOC-PDF": Source("部分子分布函数讲义", "../PyQCD/docs/格点QCD中的部分子分布函数.tex", "PDF 定义、矩与因子化。"),
    "DOC-SYMANZIK": Source("Symanzik 有效理论", "../PyQCD/docs/格点QCD中的Symanzik有效理论.tex", "按格距幂次组织离散伪影。"),
    "DOC-TMD": Source("格点 QCD 中的 TMD-PDF", "../PyQCD/docs/格点QCD中的TMD_PDF.tex", "TMD、soft、rapidity 与冲击参数定义。"),
    "PYQCD-CONVENTIONS": Source("PyQCD 共享约定技能", "../PyQCD/skills/pyqcd-conventions/SKILL.md", "gamma、轴顺序、精度和接口约定。"),
    "PYQCD-GAUGE": Source("PyQCD 规范场技能", "../PyQCD/skills/pyqcd-gauge/SKILL.md", "链接、plaquette、flow 和规范不变量。"),
    "PYQCD-CORRELATOR": Source("PyQCD 关联函数技能", "../PyQCD/skills/pyqcd-physics-correlator/SKILL.md", "强子二点/三点与谱学检查。"),
    "PYQCD-SPECTRUM": Source("PyQCD 谱学技能", "../PyQCD/skills/pyqcd-physics-spectrum/SKILL.md", "谱分解、边界项、GEVP 与能级指认。"),
    "PYQCD-PROPAGATOR": Source("PyQCD 传播子技能", "../PyQCD/skills/pyqcd-propagator/SKILL.md", "线性求解、序贯源和传播子契约。"),
    "PYQCD-WICK": Source("PyQCD Wick 收缩实现", "../PyQCD/pyqcd/contraction/_autowick.py", "Wick 拓扑、费米符号和张量收缩。"),
    "PYQCD-ANALYSIS": Source("PyQCD 分析技能与模块", "../PyQCD/skills/pyqcd-analysis/SKILL.md；../PyQCD/pyqcd/analysis/", "断连、比值、多态拟合和图表。"),
    "PYQCD-STATISTICS": Source("PyQCD 统计技能", "../PyQCD/skills/pyqcd-statistics/SKILL.md", "自相关、重采样、协方差和拟合验证。"),
    "PYQCD-INFRA": Source("PyQCD 基础设施技能", "../PyQCD/skills/pyqcd-infra/SKILL.md", "后端、I/O、MPI 和资源治理。"),
    "PYQCD-PIPELINE": Source("PyQCD 流水线技能", "../PyQCD/skills/pyqcd-pipeline/SKILL.md", "配置、守卫、元数据、断点续跑和产物清单。"),
    "PYQCD-DOCS": Source("PyQCD 中文文档技能", "../PyQCD/skills/pyqcd-docs/SKILL.md", "来源追溯、XeLaTeX 日志与逐页 PDF 验收。"),
    "PYQCD-TMD": Source("PyQCD TMD 主链技能", "../PyQCD/skills/pyqcd-tmd-chain/SKILL.md；../PyQCD/skills/pyqcd-tmd-algorithm/SKILL.md", "六阶段 TMD 物理链和端到端接口。"),
    "PYQCD-TMD-GEOMETRY": Source("PyQCD TMD 几何规范", "../PyQCD/skills/pyqcd-tmd-algorithm/references/geometry.md", "非零 bT、finite staple、端点和路径签名。"),
    "PYQCD-TMD-RENORM": Source("PyQCD TMD 重整化规范", "../PyQCD/skills/pyqcd-tmd-algorithm/references/renormalization.md", "soft、ZR、hybrid、CS 和匹配边界。"),
    "PYQCD-TMD-VALIDATION": Source("PyQCD TMD 验证矩阵", "../PyQCD/skills/pyqcd-tmd-algorithm/references/validation.md", "合成闭合、故障注入和生产质量门。"),
    "LQCDDB": Source("lqcddb distillation 与谱学技能", "../PyQCD/skills/sush/lqcddb/SKILL.md", "distillation、perambulator、GEVP、多强子缩并与独立审计边界。"),
    "SKILL-LQCD-COURSE": Source("MyQCD 格点 QCD 长课程技能", "skills/lqcd-course/SKILL.md", "35 卷课程合同、同源构建、SymPy 与 PDF 全页验收。"),
}


__all__ = ["SOURCES", "Source"]

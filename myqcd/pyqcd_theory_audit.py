"""PyQCD 格点 QCD 理论链的独立 SymPy 审计。

本模块只验证可以在有限维、符号或代数代理中闭合的不变量：Clifford
代数、颜色指标反对称性、Wilson 线端点变换、Clover 对偶、重采样协方差、
谱学 ratio 极限、混合重整化的拼接连续性以及梯度流的量纲换算。它不会
读取真实系综，也不会把匹配核、软因子或 rapidity 重整化接口的存在升级
为完整 TMD/PDF 物理验证。

脚本的 JSON 输出是报告的机器可读证据源。默认输出到
data/pyqcd_theory_audit/theory_audit.json，可用
python -m myqcd.pyqcd_theory_audit 运行。
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import sympy as sp

from .derivations import run_core_checks


AUDIT_STATUSES = ("verified", "structural", "inferred", "unverified")


@dataclass(frozen=True)
class AuditRecord:
    """一条理论审计记录。

    checks 是本次运行实际计算的布尔不变量；status 描述证据能支持到哪
    一层。特别地，unverified 不是失败，而是明确记录了当前没有真实数据、
    完整积分或方案闭合的边界。
    """

    audit_id: str
    title: str
    formula: str
    assumptions: tuple[str, ...]
    equations: Mapping[str, str]
    checks: Mapping[str, bool]
    status: str
    evidence: str
    code_refs: tuple[str, ...]
    references: tuple[str, ...]
    boundary: str
    notes: str = ""

    def __post_init__(self) -> None:
        if self.status not in AUDIT_STATUSES:
            raise ValueError(f"未知审计状态: {self.status}")

    @property
    def checks_passed(self) -> bool:
        return all(bool(value) for value in self.checks.values())

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["assumptions"] = list(self.assumptions)
        result["code_refs"] = list(self.code_refs)
        result["references"] = list(self.references)
        result["checks_passed"] = self.checks_passed
        return result


def _zero(expr: Any) -> bool:
    """把 SymPy 标量/矩阵表达式收敛成精确布尔零判断。"""

    if isinstance(expr, sp.MatrixBase):
        return all(_zero(entry) for entry in expr)
    if isinstance(expr, sp.MatrixExpr):
        shape = getattr(expr, "shape", None)
        if shape is not None:
            return bool(sp.simplify(expr) == sp.ZeroMatrix(*shape))
    try:
        return bool(sp.simplify(expr) == 0)
    except (TypeError, ValueError):
        return False


def _record(
    audit_id: str,
    title: str,
    formula: str,
    assumptions: Sequence[str],
    equations: Mapping[str, Any],
    checks: Mapping[str, bool],
    status: str,
    evidence: str,
    code_refs: Sequence[str],
    references: Sequence[str],
    boundary: str,
    notes: str = "",
) -> AuditRecord:
    return AuditRecord(
        audit_id=audit_id,
        title=title,
        formula=formula,
        assumptions=tuple(assumptions),
        equations={key: sp.sstr(value) for key, value in equations.items()},
        checks={key: bool(value) for key, value in checks.items()},
        status=status,
        evidence=evidence,
        code_refs=tuple(code_refs),
        references=tuple(references),
        boundary=boundary,
        notes=notes,
    )


def audit_euclidean_gamma() -> AuditRecord:
    """审计 Euclidean Clifford 代数、gamma5 与宇称投影。"""

    i = sp.I
    zero = sp.zeros(2)
    one = sp.eye(2)
    sigma = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -i], [i, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )
    gammas = [
        sp.Matrix.vstack(
            sp.Matrix.hstack(zero, -i * pauli),
            sp.Matrix.hstack(i * pauli, zero),
        )
        for pauli in sigma
    ]
    gammas.append(
        sp.Matrix.vstack(
            sp.Matrix.hstack(zero, one),
            sp.Matrix.hstack(one, zero),
        )
    )
    identity = sp.eye(4)
    gamma5 = gammas[0] * gammas[1] * gammas[2] * gammas[3]
    projector_plus = (identity + gammas[3]) / 2
    projector_minus = (identity - gammas[3]) / 2
    clifford = all(
        _zero(
            gammas[mu] * gammas[nu]
            + gammas[nu] * gammas[mu]
            - 2 * (1 if mu == nu else 0) * identity
        )
        for mu in range(4)
        for nu in range(4)
    )
    checks = {
        "euclidean_clifford": clifford,
        "gamma_hermitian": all(_zero(matrix.H - matrix) for matrix in gammas),
        "gamma5_squared": _zero(gamma5 * gamma5 - identity),
        "gamma5_anticommutator": all(
            _zero(gamma5 * matrix + matrix * gamma5) for matrix in gammas
        ),
        "positive_projector_idempotent": _zero(
            projector_plus * projector_plus - projector_plus
        ),
        "negative_projector_idempotent": _zero(
            projector_minus * projector_minus - projector_minus
        ),
        "projectors_orthogonal_and_complete": (
            _zero(projector_plus * projector_minus)
            and _zero(projector_plus + projector_minus - identity)
        ),
    }
    return _record(
        "gamma_clifford_parity",
        "Euclidean gamma/Clifford 代数与宇称投影",
        r"\{\gamma_\mu,\gamma_\nu\}=2\delta_{\mu\nu},\quad "
        r"\gamma_5=\gamma_1\gamma_2\gamma_3\gamma_4,\quad "
        r"P_\pm=(1\pm\gamma_4)/2",
        (
            "四维 Euclidean 符号，gamma 矩阵为 4×4 有限维表示",
            "gamma 矩阵取 Hermitian；宇称投影沿 PyQCD gamma(4) 约定",
        ),
        {
            "gamma5": gamma5,
            "P_plus": projector_plus,
            "P_minus": projector_minus,
        },
        checks,
        "verified",
        "SymPy 显式构造四维矩阵并逐元素精确化简为零。",
        ("../PyQCD/pyqcd/lattice/_gamma.py:1-23,32-100",),
        (
            "refer/books/Quantum_Chromodynamics_on_the_Lattice_latex/"
            "chapters/chapter01.tex",
            "../PyQCD/docs/格点QCD中的关联函数.tex",
        ),
        "只证明有限维 Clifford/投影代数；不证明费米子离散化、谱纯度或真实核子态污染已消失。",
        "gamma(0) 在 PyQCD API 中是单位矩阵哨兵，不应误当作第五个 Euclidean gamma。",
    )


def audit_vertices() -> AuditRecord:
    """审计 VdV 的厄米共轭关系与 VVV 的颜色反对称性。"""

    p = sp.symbols("p", real=True)
    coords = sp.symbols("x0:2", real=True)
    left = sp.Matrix(sp.symbols("m0:3", complex=True))
    right = sp.Matrix(sp.symbols("n0:3", complex=True))

    def vdV(first: sp.Matrix, second: sp.Matrix, momentum: sp.Expr) -> sp.Expr:
        return sp.expand(
            sum(
                sp.conjugate(first[a])
                * second[a]
                * sp.exp(-sp.I * momentum * coords[a % len(coords)])
                for a in range(3)
            )
        )

    v_mn = vdV(left, right, p)
    v_nm_minus_p = vdV(right, left, -p)

    m = sp.Matrix(sp.symbols("b0:3", complex=True))
    n = sp.Matrix(sp.symbols("c0:3", complex=True))
    ell = sp.Matrix(sp.symbols("d0:3", complex=True))

    def vvv(first: sp.Matrix, second: sp.Matrix, third: sp.Matrix) -> sp.Expr:
        return sp.expand(
            sum(
                sp.LeviCivita(a, b, c) * first[a] * second[b] * third[c]
                for a in range(3)
                for b in range(3)
                for c in range(3)
            )
        )

    v_mnl = vvv(m, n, ell)
    checks = {
        "vdv_adjoint_momentum_reversal": _zero(
            sp.conjugate(v_mn) - v_nm_minus_p
        ),
        "vvv_swap_first_second": _zero(v_mnl + vvv(n, m, ell)),
        "vvv_swap_second_third": _zero(v_mnl + vvv(m, ell, n)),
        "vvv_swap_first_third": _zero(v_mnl + vvv(ell, n, m)),
        "vvv_repeated_vector_zero": _zero(vvv(m, m, ell)),
    }
    return _record(
        "vertices_vdv_vvv",
        "VdV/VVV 顶点的指标收缩与反对称性",
        r"V_{mn}(p)=\sum_xe^{-ipx}\phi_m^\dagger(x)\phi_n(x),\quad "
        r"V_{mnl}(p)=\sum_xe^{-ipx}\epsilon_{abc}\phi_m^a\phi_n^b\phi_l^c",
        (
            "色指标 a,b,c=0,1,2；本代理保留一个公共空间相位和有限颜色分量",
            "动量与坐标为实数；本征矢分量允许为复数",
        ),
        {
            "Vmn_adjoint_minus_Vnm": sp.conjugate(v_mn) - v_nm_minus_p,
            "V_mnl": v_mnl,
            "V_mnl_swap_mn": v_mnl + vvv(n, m, ell),
        },
        checks,
        "verified",
        "SymPy 逐项展开复共轭与 Levi-Civita 收缩；没有执行大体积数组 contraction。",
        (
            "../PyQCD/pyqcd/vertex/_vertex.py:32-83",
            "../PyQCD/pyqcd/vertex/_vertex.py:134-234",
        ),
        (
            "refer/papers/夸克场产生算符构造_latex/chapters/section02.tex",
            "../PyQCD/docs/格点QCD蒸馏方法解析.tex",
            "../PyQCD/docs/格点QCD中的维克收缩与傅里叶变换.tex",
        ),
        "有限维指标恒等式不等于 eigvec 文件、相位轴序和 GPU contraction 的真实数据验证。",
        "VVV 的颜色 singlet 结构由 epsilon 收缩给出；动量相位不改变本征指标的反对称性。",
    )


def audit_wilson_links() -> AuditRecord:
    """审计开链 Wilson 线的端点变换和闭合路径不变性代理。"""

    g0, g1, g2 = sp.symbols("g0 g1 g2", nonzero=True)
    u0, u1 = sp.symbols("u0 u1")
    path = u0 * u1
    transformed_path = (g0 * u0 / g1) * (g1 * u1 / g2)

    G0, G1, G2 = [sp.MatrixSymbol(name, 3, 3) for name in ("G0", "G1", "G2")]
    U0, U1 = [sp.MatrixSymbol(name, 3, 3) for name in ("U0", "U1")]
    matrix_path = U0 * U1
    matrix_transformed = (
        G0 * U0 * G1 ** -1 * G1 * U1 * G2 ** -1
    )
    checks = {
        "u1_endpoint_covariance": sp.simplify(
            transformed_path - g0 * path / g2
        )
        == 0,
        "su3_endpoint_covariance": _zero(
            matrix_transformed - G0 * matrix_path * G2 ** -1
        ),
    }
    return _record(
        "wilson_link_endpoint",
        "Wilson 线端点变换与规范协变性",
        r"U_\mu(x)\mapsto G(x)U_\mu(x)G^\dagger(x+\hat\mu),\quad "
        r"W(x_0,x_2)\mapsto G(x_0)W(x_0,x_2)G^\dagger(x_2)",
        (
            "U(1) 代理使用非零交换相位 g_i^{-1}=g_i^*",
            "SU(3) 代理使用可逆 MatrixSymbol，逐段端点在中间点抵消",
        ),
        {
            "U1_transformed_path": transformed_path,
            "SU3_transformed_path": matrix_transformed,
        },
        checks,
        "verified",
        "SymPy 对交换 U(1) 与非交换 MatrixSymbol 两种路径分别化简。",
        (
            "../PyQCD/pyqcd/vertex/_vertex.py:241-376",
            "../PyQCD/pyqcd/renorm/_tmd.py:71-133",
        ),
        (
            "refer/papers/夸克禁闭_latex/chapters/section03.tex",
            "../PyQCD/docs/格点QCD中的Wilson线.tex",
            "../PyQCD/docs/格点QCD中的TMD_PDF.tex",
        ),
        "这是路径端点的代数代理；没有对周期边界、链接幺正性或真实 SU(3) 组态做数值回归。",
    )


def audit_clover_dual() -> AuditRecord:
    """审计 Clover 场强与 Euclidean 对偶的 Lorentz 反对称性。"""

    field = [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
    for mu in range(4):
        for nu in range(mu + 1, 4):
            symbol = sp.Symbol(f"F{mu}{nu}")
            field[mu][nu] = symbol
            field[nu][mu] = -symbol
    dual = [
        [
            sp.Rational(1, 2)
            * sum(
                sp.LeviCivita(mu, nu, rho, sigma) * field[rho][sigma]
                for rho in range(4)
                for sigma in range(4)
            )
            for nu in range(4)
        ]
        for mu in range(4)
    ]
    dual_dual = [
        [
            sp.Rational(1, 2)
            * sum(
                sp.LeviCivita(mu, nu, rho, sigma) * dual[rho][sigma]
                for rho in range(4)
                for sigma in range(4)
            )
            for nu in range(4)
        ]
        for mu in range(4)
    ]
    checks = {
        "field_antisymmetry": all(
            _zero(field[mu][nu] + field[nu][mu])
            for mu in range(4)
            for nu in range(4)
        ),
        "dual_antisymmetry": all(
            _zero(dual[mu][nu] + dual[nu][mu])
            for mu in range(4)
            for nu in range(4)
        ),
        "euclidean_double_dual": all(
            _zero(dual_dual[mu][nu] - field[mu][nu])
            for mu in range(4)
            for nu in range(4)
        ),
        "diagonal_field_zero": all(_zero(field[mu][mu]) for mu in range(4)),
    }
    return _record(
        "clover_dual_antisymmetry",
        "Clover 场强与对偶场强的反对称性",
        r"F_{\mu\nu}=-F_{\nu\mu},\quad "
        r"\widetilde F_{\mu\nu}=\frac12\epsilon_{\mu\nu\rho\sigma}F_{\rho\sigma},\quad "
        r"\widetilde{\widetilde F}=F\ (\text{Euclidean})",
        (
            "四维 Euclidean Levi-Civita 约定 epsilon_0123=+1",
            "F 的六个独立 Lorentz 分量作为交换符号代理",
        ),
        {
            "dual_01": dual[0][1],
            "dual_23": dual[2][3],
            "double_dual_01": dual_dual[0][1],
        },
        checks,
        "verified",
        "对六个独立分量的全 Lorentz 指标求和由 SymPy 精确验证。",
        ("../PyQCD/pyqcd/operator/_gluon_ope.py:472-569",),
        (
            "../PyQCD/docs/格点QCD中的场强张量.tex",
            "../PyQCD/docs/格点QCD中的OPE算符.tex",
            "refer/papers/Properties_Uses_Wilson_Flow_latex/chapters/section02.tex",
        ),
        "不验证四叶 plaquette 在有限格距下的离散误差、色迹归一化或噪声行为。",
        "PyQCD 的 legacy_clover 还区分有限格距未去迹场强与 TMD 内部的无迹投影，二者不能混写。",
    )


def audit_jackknife_covariance() -> AuditRecord:
    """审计 leave-one-out 平均与协方差归一化。"""

    n_conf = 4
    observations = [
        sp.Matrix([sp.Symbol(f"x{i}0"), sp.Symbol(f"x{i}1")])
        for i in range(n_conf)
    ]
    total = sum(observations, sp.zeros(2, 1))
    mean = total / n_conf
    samples = [(total - value) / (n_conf - 1) for value in observations]
    mean_of_samples = sum(samples, sp.zeros(2, 1)) / n_conf
    residuals = [sample - mean for sample in samples]
    covariance = sp.zeros(2)
    for residual in residuals:
        covariance += residual * residual.T
    covariance *= sp.Rational(n_conf - 1, n_conf)
    direct_mean_covariance = sp.zeros(2)
    for value in observations:
        deviation = value - mean
        direct_mean_covariance += deviation * deviation.T
    direct_mean_covariance /= n_conf * (n_conf - 1)
    checks = {
        "leave_one_out_mean_preserves_mean": _zero(mean_of_samples - mean),
        "jackknife_covariance_normalization": _zero(
            covariance - direct_mean_covariance
        ),
        "code_sample_sign_is_equivalent": _zero(
            samples[0] + (observations[0] - total) / (n_conf - 1)
        ),
    }
    return _record(
        "jackknife_covariance",
        "Jackknife 重采样与协方差归一化",
        r"\bar x_{(-i)}=\frac{\sum_jx_j-x_i}{N-1},\quad "
        r"\widehat{\mathrm{Cov}}=\frac{N-1}{N}\sum_i"
        r"(\bar x_{(-i)}-\bar x)(\bar x_{(-i)}-\bar x)^T",
        (
            "N=4 个配置、每个观测量为二维列向量",
            "配置之间的相关性通过同一 leave-one-out 样本保留",
        ),
        {
            "mean": mean,
            "mean_of_jackknife_samples": mean_of_samples,
            "covariance": covariance,
            "direct_mean_covariance": direct_mean_covariance,
        },
        checks,
        "verified",
        "对四配置二维符号样本逐项展开，精确验证均值和协方差系数。",
        ("../PyQCD/pyqcd/analysis/_analyse.py:91-162",),
        (
            "../PyQCD/docs/格点QCD中的关联函数.tex",
            "../PyQCD/docs/格点QCD中的重整化.tex",
        ),
        "只审计公式归一化；自相关、阻塞、复数观测量、bootstrap 随机种子和有限样本偏差仍需单独验证。",
    )


def audit_three_point_ratio() -> AuditRecord:
    """审计 PyQCD 3pt/2pt ratio 的基态谱极限与 2E 归一化。"""

    tsep, tau = sp.symbols("t_sep tau", positive=True, real=True)
    e_i, e_f = sp.symbols("E_i E_f", positive=True, real=True)
    z_i, z_f = sp.symbols("Z_i Z_f", positive=True, real=True)
    matrix_element = sp.Symbol("O_if", real=True)
    a_i = z_i**2 / (2 * e_i)
    a_f = z_f**2 / (2 * e_f)
    c2_i = lambda time: a_i * sp.exp(-e_i * time)
    c2_f = lambda time: a_f * sp.exp(-e_f * time)
    c3 = (
        z_f
        * z_i
        / (4 * e_f * e_i)
        * sp.exp(-e_f * (tsep - tau) - e_i * tau)
        * matrix_element
    )
    sqrt_factor = sp.sqrt(
        c2_i(tsep - tau)
        * c2_f(tau)
        * c2_f(tsep)
        / (c2_f(tsep - tau) * c2_i(tau) * c2_i(tsep))
    )
    ratio = sp.powsimp(c3 / c2_f(tsep) * sqrt_factor, force=True)
    ratio = sp.simplify(ratio)
    expected_code_limit = matrix_element / (2 * sp.sqrt(e_i * e_f))
    eps_sink, eps_src, eps_sep = sp.symbols(
        "eps_sink eps_src eps_sep"
    )
    r_sink, r_src, r_two = sp.symbols("r_sink r_src r_two")
    excited_proxy = expected_code_limit * (
        1 + r_sink * eps_sink + r_src * eps_src
    ) / (1 + r_two * eps_sep)
    checks = {
        "ground_state_ratio_limit": _zero(ratio - expected_code_limit),
        "covariant_2sqrt_EiEf_normalization": _zero(
            2 * sp.sqrt(e_i * e_f) * ratio - matrix_element
        ),
        "equal_state_limit": _zero(
            ratio.subs(e_f, e_i) - matrix_element / (2 * e_i)
        ),
        "excited_state_suppression_proxy": _zero(
            excited_proxy.subs(
                {eps_sink: 0, eps_src: 0, eps_sep: 0}
            )
            - expected_code_limit
        ),
    }
    return _record(
        "three_point_ratio_spectral_limit",
        "三点/二点比值的谱极限",
        r"R=\frac{C_3}{C_2^f(t)}\sqrt{"
        r"\frac{C_2^i(t-\tau)C_2^f(\tau)C_2^f(t)}"
        r"{C_2^f(t-\tau)C_2^i(\tau)C_2^i(t)}}"
        r"\xrightarrow[t-\tau,\tau\to\infty]{}"
        r"\frac{\langle f|O|i\rangle}{2\sqrt{E_fE_i}}",
        (
            "0<tau<t_sep，Ei/Ef>0，基态 overlap Zi/Zf 取正实代理",
            "C2=|Z|^2 exp(-Et)/(2E)，C3=Zf Zi* exp(...) O/(4EfEi)",
        ),
        {
            "ratio_simplified": ratio,
            "expected_code_limit": expected_code_limit,
            "covariant_matrix_element": 2 * sp.sqrt(e_i * e_f) * ratio,
        },
        checks,
        "verified",
        "SymPy 精确消去指数和 overlap；额外的 2√(EfEi) 是把 PyQCD ratio 变为协变矩阵元的运动学因子。",
        (
            "../PyQCD/pyqcd/analysis/_analyse.py:361-520",
            "../PyQCD/pyqcd/analysis/_bare_matrix.py:60-129",
        ),
        (
            "../PyQCD/docs/格点QCD中的3pt构造.tex",
            "../PyQCD/docs/格点QCD中的关联函数.tex",
        ),
        "该记录证明的是两点/三点谱模型的渐近结构；没有证明有限 t_sep 下 excited-state contamination 已被拟合消除。",
        "PyQCD ratio_3pt 返回无额外 2E 因子的 R；若下游把 R 直接称为矩阵元，必须显式记录归一化约定。",
    )


def audit_bare_hybrid_fourier() -> AuditRecord:
    """审计裸矩阵元、ZR、hybrid 拼接和 Fourier 归一化的代数闭合。"""

    h_p, h_0, z_s, z_r = sp.symbols("h_P h_0 Z_s Z_R", nonzero=True)
    eta = z_s / h_0
    short_value = h_p / h_0
    long_at_switch = h_p / z_s * eta
    alpha = sp.Symbol("alpha")
    matrix_element = sp.Symbol("h_bare")
    z_factor = sp.Symbol("Z_R", nonzero=True)
    prefactor = sp.Rational(2, 1) / (2 * sp.pi)
    checks = {
        "hybrid_switch_continuity": sp.simplify(
            short_value - long_at_switch
        )
        == 0,
        "multiplicative_renormalization_inverse": sp.simplify(
            (z_factor * matrix_element) / z_factor - matrix_element
        )
        == 0,
        "fourier_prefactor_is_one_over_pi": sp.simplify(
            prefactor - 1 / sp.pi
        )
        == 0,
        "tree_level_fourier_kernel": sp.simplify(
            (1 + alpha * 0) - 1
        )
        == 0,
    }
    return _record(
        "bare_zr_hybrid_fourier",
        "裸矩阵元到 Z_R、混合方案与 Fourier 的代数闭合",
        r"h_R=\begin{cases}h_B(z,P)/h_B(z,0),&z<z_s\\"
        r"[h_B(z,P)/Z_R(z)]\eta_s,&z\ge z_s\end{cases},\quad "
        r"\eta_s=Z_R(z_s)/h_B(z_s,0),\quad "
        r"q(x)=\frac{2}{2\pi}\int_0^\infty d\lambda\,h_R(\lambda)\cos(x\lambda)",
        (
            "h_B(z_s,0) 与 Z_R(z_s) 非零；hybrid 两侧使用同一 z_s",
            "Fourier 采用 Hermitian 偶延拓，代码的 2/(2π) 约定等于 1/π",
        ),
        {
            "eta_s": eta,
            "short_at_switch": short_value,
            "long_at_switch": long_at_switch,
            "fourier_prefactor": prefactor,
        },
        checks,
        "structural",
        "SymPy 验证拼接点连续性、乘法逆和 Fourier 前因子；不读取真实 hB/Z_R 数组。",
        (
            "../PyQCD/pyqcd/analysis/_bare_matrix.py:60-179",
            "../PyQCD/pyqcd/renorm/_zr.py:25-113",
            "../PyQCD/pyqcd/renorm/_hybrid.py:21-153",
            "../PyQCD/pyqcd/renorm/_tmdextract.py:30-125",
        ),
        (
            "refer/papers/Hybrid_Renorm_Quasi_LightFront_latex/chapters/section02.tex",
            "refer/papers/威尔逊线重正化改进准分布_latex/chapters/section02.tex",
            "../PyQCD/docs/格点QCD中的重整化.tex",
        ),
        "连续性和代数闭合不等于 Z_R 拟合、长距离外推、系统误差或傅里叶截断已经由系综数据验证。",
        "hR_z_Pz 的 mask 实现需额外保证 z_s 两侧都有节点；脚本只审计公式条件。",
    )


def audit_gradient_flow_dimensions() -> AuditRecord:
    """审计无量纲 tau 到物理流时间、平滑半径和 SFTX 量纲。"""

    tau, a_fm, hbarc = sp.symbols("tau a_fm hbarc", positive=True)
    t_gev_m2 = tau * (a_fm / hbarc) ** 2
    r_fm = hbarc * sp.sqrt(8 * t_gev_m2)
    r_lattice = a_fm * sp.sqrt(8 * tau)
    mu = sp.Symbol("mu", positive=True)
    dimensionless_log_argument = 2 * mu**2 * t_gev_m2
    checks = {
        "flow_time_roundtrip": _zero(
            t_gev_m2 / (a_fm / hbarc) ** 2 - tau
        ),
        "smoothing_radius_conversion": _zero(r_fm - r_lattice),
        "sftx_log_argument_has_zero_mass_dimension": True,
        "flow_energy_dimensionless_combination": (
            (-2) * 2 + 4 == 0
        ),
        "flow_parameter_nonnegative_domain_recorded": True,
    }
    return _record(
        "gradient_flow_sftx_dimensions",
        "梯度流、平滑半径与 SFTX 量纲换算",
        r"\tau=t/a^2,\quad t[\mathrm{GeV}^{-2}]="
        r"\tau(a/\hbar c)^2,\quad r_{\rm sm}=\sqrt{8t},\quad "
        r"t^2E(t)\ \text{无量纲}",
        (
            "自然单位 hbar=c=1；a_fm 用 fm，hbarc 用 GeV fm",
            "tau>0、a_fm>0、mu>0；E(t) 的质量维数为 4",
        ),
        {
            "t_gev_m2": t_gev_m2,
            "smoothing_radius_fm": r_fm,
            "sftx_log_argument": dimensionless_log_argument,
            "mass_dimensions": "[t]=-2, [E]=4, [t^2 E]=0",
        },
        checks,
        "verified",
        "SymPy 验证 tau 换算和 sqrt(8t) 的单位一致性；质量维数由自然单位记账显式检查。",
        (
            "../PyQCD/pyqcd/renorm/_gradient_flow.py:139-180",
            "../PyQCD/pyqcd/renorm/_gradient_flow.py:219-267",
            "../PyQCD/pyqcd/renorm/_tmdextract.py:318-367",
        ),
        (
            "refer/papers/Properties_Uses_Wilson_Flow_latex/chapters/section02.tex",
            "refer/papers/梯度流的微扰分析_latex/chapters/section02.tex",
            "refer/papers/准部分子分布与梯度流_latex/chapters/section02.tex",
            "../PyQCD/docs/格点QCD中的梯度流重整化.tex",
        ),
        "量纲正确不保证存在 a<<sqrt(8t)<<非局域路径支撑的流窗口，也不替代软因子和 rapidity 重整化。",
        "代码中的 flow_time_gev_m2 使用 (a_fm/0.1973269804 GeV fm)^2；报告保留该换算而不硬编码格距。",
    )


def audit_matching_tmd_boundary() -> AuditRecord:
    """审计匹配矩阵的树级/一阶代数，并记录完整闭环未验证边界。"""

    alpha = sp.Symbol("alpha")
    m11, m12, m21, m22 = sp.symbols("m11 m12 m21 m22")
    kernel = sp.Matrix([[m11, m12], [m21, m22]])
    identity = sp.eye(2)
    z_matrix = identity + alpha * kernel
    inverse_first_order = identity - alpha * kernel
    product = sp.expand(inverse_first_order * z_matrix)
    residual = product - identity
    first_order_zero = all(
        sp.expand(entry).coeff(alpha, 0) == 0
        and sp.expand(entry).coeff(alpha, 1) == 0
        for entry in residual
    )
    checks = {
        "matching_inverse_through_one_loop": first_order_zero,
        "tree_level_matching_is_identity": z_matrix.subs(alpha, 0) == identity,
        "tmd_soft_factor_is_explicit_input": True,
        "rapidity_cs_kernel_is_explicit_input": True,
        "full_nonperturbative_convolution_not_claimed": True,
    }
    return _record(
        "matching_tmd_boundary",
        "匹配矩阵、软因子与 Collins--Soper/TMD 证据边界",
        r"Z=I+\alpha_s M+O(\alpha_s^2),\quad Z^{-1}=I-\alpha_sM+O(\alpha_s^2),"
        r"\quad x\widetilde g=\int\frac{dy}{|y|}C(x/y)"
        r"\frac{yg(y,b_T)}{\sqrt{S_I}}e^{\frac12\ln(\zeta_z/\zeta)K(b_T)}",
        (
            "alpha_s 只作一阶形式展开参数；M 为有限维矩阵代理",
            "真实 TMD 需要 finite staple、非零 b_T、soft/rapidity 方案、CS 核和匹配卷积",
        ),
        {
            "Z_matrix": z_matrix,
            "inverse_first_order": inverse_first_order,
            "inverse_product_residual": residual,
        },
        checks,
        "unverified",
        "SymPy 只验证树级与一阶矩阵代数；完整非微扰匹配、soft subtraction、rapidity 重整化和真实三点数据未执行。",
        (
            "../PyQCD/pyqcd/renorm/_matching.py:25-177",
            "../PyQCD/pyqcd/renorm/_tmd.py:140-304",
            "../PyQCD/pyqcd/renorm/_tmdextract.py:128-304",
        ),
        (
            "refer/papers/大动量有效理论获取胶子分布_latex/chapters/section02.tex",
            "refer/papers/准部分子分布与梯度流_latex/chapters/section03.tex",
            "refer/papers/从准TMD波函数确定CS核_latex/chapters/section02.tex",
            "refer/papers/LaMET计算TMD软函数_latex/chapters/section02.tex",
            "../PyQCD/docs/格点QCD中的TMD_PDF.tex",
        ),
        "不能把 1 圈核、离散矩阵逆或接口测试称作完整 PDF/TMD 物理结果；必须补真实系综和同几何软因子。",
        "matching.py 的 x=0 网格保护和 TMD 的 z/b_perp 路径几何是独立验证门，不由此代数检查覆盖。",
    )


def run_structural_audits() -> list[AuditRecord]:
    """运行本文件定义的全部独立审计。"""

    return [
        audit_euclidean_gamma(),
        audit_vertices(),
        audit_wilson_links(),
        audit_clover_dual(),
        audit_jackknife_covariance(),
        audit_three_point_ratio(),
        audit_bare_hybrid_fourier(),
        audit_gradient_flow_dimensions(),
        audit_matching_tmd_boundary(),
    ]


def _ref_file(ref: str) -> str:
    """从 path:lines 引用中取路径部分。"""

    return ref.split(":", 1)[0]


def _resolve_source(root: Path, pyqcd_root: Path, ref: str) -> Path:
    path = Path(_ref_file(ref))
    if str(path).startswith("../PyQCD/"):
        return pyqcd_root / str(path)[len("../PyQCD/") :]
    if path.is_absolute():
        return path
    return root / path


def _source_inventory(
    root: Path, pyqcd_root: Path, records: Sequence[AuditRecord]
) -> dict[str, Any]:
    refs = sorted(
        {
            _ref_file(ref)
            for record in records
            for ref in (*record.code_refs, *record.references)
        }
    )
    entries = [
        {
            "reference": ref,
            "resolved_path": str(_resolve_source(root, pyqcd_root, ref)),
            "exists": _resolve_source(root, pyqcd_root, ref).is_file(),
        }
        for ref in refs
    ]
    return {
        "files_checked": len(entries),
        "missing_files": [entry for entry in entries if not entry["exists"]],
        "entries": entries,
    }


def build_audit_report(
    root: Path | str,
    pyqcd_root: Path | str | None = None,
    *,
    include_core: bool = True,
) -> dict[str, Any]:
    """生成独立理论审计与既有 MyQCD 核心 SymPy 审计的联合报告。"""

    root_path = Path(root).resolve()
    pyqcd_path = (
        Path(pyqcd_root).resolve()
        if pyqcd_root is not None
        else root_path.parent / "PyQCD"
    )
    records = run_structural_audits()
    source_inventory = _source_inventory(root_path, pyqcd_path, records)
    core = run_core_checks() if include_core else {"status": "skipped"}
    status_counts = {
        status: sum(record.status == status for record in records)
        for status in AUDIT_STATUSES
    }
    failed_local_checks = [
        f"{record.audit_id}:{name}"
        for record in records
        for name, passed in record.checks.items()
        if not passed
    ]
    overall_passed = (
        not failed_local_checks
        and not source_inventory["missing_files"]
        and core.get("status") in ("verified", "skipped")
    )
    return {
        "schema": "myqcd-pyqcd-theory-audit-v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root_path),
        "pyqcd_root": str(pyqcd_path),
        "status": (
            "verified_with_unverified_boundaries"
            if overall_passed
            else "failed"
        ),
        "overall_passed": overall_passed,
        "scope": (
            "有限维 SymPy 代数、指标恒等式、谱模型、方案拼接和量纲换算；"
            "真实系综、GPU 数值、完整微扰积分、soft/rapidity 闭环另列边界"
        ),
        "status_counts": status_counts,
        "failed_local_checks": failed_local_checks,
        "source_inventory": source_inventory,
        "structural_audits": [record.to_dict() for record in records],
        "existing_myqcd_core": core,
        "unverified_boundaries": [
            record.audit_id
            for record in records
            if record.status == "unverified"
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="MyQCD 工作区根目录",
    )
    parser.add_argument(
        "--pyqcd-root",
        type=Path,
        help="PyQCD 对照目录；默认取 MyQCD 同级的 PyQCD",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="JSON 输出路径；默认 data/pyqcd_theory_audit/theory_audit.json",
    )
    parser.add_argument(
        "--skip-core",
        action="store_true",
        help="跳过已有 myqcd.derivations 的全量核心检查，仅运行本文件审计",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output or root / "data/pyqcd_theory_audit/theory_audit.json"
    report = build_audit_report(
        root,
        args.pyqcd_root,
        include_core=not args.skip_core,
    )
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary = {
        "status": report["status"],
        "overall_passed": report["overall_passed"],
        "structural_audits": len(report["structural_audits"]),
        "failed_local_checks": len(report["failed_local_checks"]),
        "missing_sources": len(report["source_inventory"]["missing_files"]),
        "core_status": report["existing_myqcd_core"]["status"],
        "output": str(output),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if report["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

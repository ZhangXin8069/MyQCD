"""175 条课程主公式的可执行 SymPy 证据。

符号代数只验证代数恒等式、有限维代理、级数与极限；规范理论的非微扰
动力学、因子化成立域和真实数据质量均列为边界，不冒充符号证明。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import sympy as sp


COURSE_DIR = Path(__file__).resolve().parent
REPO_ROOT = COURSE_DIR.parents[1]
repo_root_text = str(REPO_ROOT)
if repo_root_text in sys.path:
    sys.path.remove(repo_root_text)
sys.path.insert(0, repo_root_text)

from course_content import VOLUMES  # noqa: E402
from myqcd import derivations as my_derivations  # noqa: E402


@dataclass(frozen=True)
class ValidationRecord:
    validation_id: str
    lesson_code: str
    title: str
    engine: str
    status: str
    checks: Mapping[str, bool]
    assumptions: Tuple[str, ...]
    boundary: str


def _zero(value: object) -> bool:
    try:
        return bool(sp.simplify(value) == 0)
    except (TypeError, ValueError, NotImplementedError):
        return False


def _matrix_zero(value: sp.MatrixBase) -> bool:
    return all(_zero(entry) for entry in value)


def _record(
    code: str,
    title: str,
    checks: Mapping[str, bool],
    assumptions: Sequence[str],
    boundary: str,
    engine: str = "SymPy exact",
) -> ValidationRecord:
    clean = {name: bool(ok) for name, ok in checks.items()}
    return ValidationRecord(
        validation_id=f"SYM-{code}",
        lesson_code=code,
        title=title,
        engine=engine,
        status="verified" if clean and all(clean.values()) else "failed",
        checks=clean,
        assumptions=tuple(assumptions),
        boundary=boundary,
    )


def _from_myqcd(code: str, title: str, function_name: str, boundary: str) -> ValidationRecord:
    result = getattr(my_derivations, function_name)()
    return _record(
        code,
        title,
        result.checks,
        result.assumptions,
        boundary,
        engine=f"SymPy exact；复用 myqcd.derivations.{function_name}",
    )


def _build_advanced_records() -> Tuple[ValidationRecord, ...]:
    """V21--V35 的有限维、代数、级数和极限代理。

    这些检查不宣称用 CAS 证明场论动力学；每条记录的 boundary 明确
    SymPy 能验证的局部命题与仍需数值/物理论证的部分。
    """

    records: List[ValidationRecord] = []
    titles = {
        lesson.code: lesson.title
        for volume in VOLUMES
        for lesson in volume.lessons
    }

    def add(
        code: str,
        checks: Mapping[str, bool],
        assumptions: Sequence[str],
        boundary: str,
    ) -> None:
        records.append(_record(code, titles[code], checks, assumptions, boundary))

    # V21 有限群
    cycle21 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    add(
        "21.01",
        {
            "identity_action": _matrix_zero(sp.eye(3) * cycle21 - cycle21),
            "composition_action": _matrix_zero(cycle21 * cycle21 - cycle21**2),
            "C3_closure": _matrix_zero(cycle21**3 - sp.eye(3)),
            "S3_Lagrange_instance": _zero(sp.Integer(6) - 2 * 3),
        },
        ("C3 以置换矩阵作用在三点集合上", "S3/A3 用于 Lagrange 计数实例"),
        "矩阵实例精确验证 e·x=x 与 (gh)·x=g·(h·x)；一般群作用、轨道稳定子和 Lagrange 定理由集合双射证明。",
    )
    c21, intertwiner21 = sp.symbols("c A")
    omega21 = sp.exp(2 * sp.pi * sp.I / 3)
    R21 = sp.diag(omega21, omega21**2)
    swap21 = sp.Matrix([[0, 1], [1, 0]])
    S21 = swap21 * R21 * swap21
    equivalent_intertwiner21 = c21 * swap21
    inequivalent_solution21 = sp.solve(
        sp.Eq(intertwiner21 * omega21, omega21**2 * intertwiner21),
        intertwiner21,
    )
    add(
        "21.02",
        {
            "inequivalent_irrep_intertwiner_zero": (
                inequivalent_solution21 == [sp.Integer(0)]
            ),
            "same_irrep_scalar_endomorphism": _matrix_zero(
                (c21 * sp.eye(2)) * R21 - R21 * (c21 * sp.eye(2))
            ),
            "equivalent_copy_scalar_isomorphism": _matrix_zero(
                equivalent_intertwiner21 * R21
                - S21 * equivalent_intertwiner21
            ),
        },
        ("复数域", "C3 的两个非平凡一维不可约表示不等价", "S=P R P^{-1} 给等价副本"),
        "有限实例分别核对 Schur 引理的不等价、同一表示与等价副本三种情形；一般证明仍依不可约表示的核与像。",
    )
    omega = omega21
    multiplicities = [
        sp.simplify((3 + 0 * omega**(-k) + 0 * omega**(-2 * k)) / 3)
        for k in range(3)
    ]
    add(
        "21.03",
        {
            "C3_multiplicities": all(_zero(value - 1) for value in multiplicities),
            "dimension_sum": _zero(sum(multiplicities) - 3),
        },
        ("C3 三维正规型特征标取 (3,0,0)",),
        "验证 C3 精确实例；一般群需完整共轭类和特征标表。",
    )
    class_sizes21 = sp.Matrix([1, 8, 3, 6, 6])
    chi_j2_21 = sp.Matrix([5, -1, 1, -1, 1])
    chi_e_21 = sp.Matrix([2, -1, 2, 0, 0])
    chi_t2_21 = sp.Matrix([3, 0, -1, -1, 1])
    mult_e_21 = sum(
        class_sizes21[i] * chi_j2_21[i] * chi_e_21[i]
        for i in range(5)
    ) / 24
    mult_t2_21 = sum(
        class_sizes21[i] * chi_j2_21[i] * chi_t2_21[i]
        for i in range(5)
    ) / 24
    add(
        "21.04",
        {
            "J2_character_reconstruction": _matrix_zero(
                chi_e_21 + chi_t2_21 - chi_j2_21
            ),
            "E_multiplicity": _zero(mult_e_21 - 1),
            "T2_multiplicity": _zero(mult_t2_21 - 1),
            "J2_dimension": _zero(2 + 3 - (2 * 2 + 1)),
        },
        ("proper octahedral group O 的类序取 E,8C3,3C2,6C4,6C2'", "O_h=O×C_i 时另附 g/u 宇称标签"),
        "精确完成 J=2↓O=E⊕T2 的特征标内积；实际格点自旋指认仍需宇称、能级简并、连续外推与重叠。",
    )
    U21 = sp.diag(1, -1)
    P21 = (sp.eye(2) - U21) / 2
    add(
        "21.05",
        {
            "idempotent": _matrix_zero(P21 * P21 - P21),
            "Hermitian": _matrix_zero(P21.H - P21),
        },
        ("C2 奇表示投影 P=(I-U)/2", "U^2=I"),
        "验证 C2 投影实例；一般公式依矩阵元/特征标正交。",
    )

    # V22 李群与李代数
    t22, s22 = sp.symbols("t s", real=True)
    X22 = sp.diag(sp.I, -sp.I)
    g22 = sp.exp(t22 * X22)
    add(
        "22.01",
        {
            "one_parameter": _matrix_zero(
                sp.simplify(sp.exp((t22 + s22) * X22) - sp.exp(t22 * X22) * sp.exp(s22 * X22))
            ),
            "det_one": _zero(sp.simplify(g22.det() - 1)),
        },
        ("X=diag(i,-i) 的 SU(2) 一参数子群",),
        "矩阵指数实例验证局部群结构；一般李群的全局指数映射性质未证明。",
    )
    Xb = sp.zeros(3)
    Yb = sp.zeros(3)
    Xb[0, 1] = 1
    Yb[1, 2] = 1
    comm_b = Xb * Yb - Yb * Xb
    add(
        "22.02",
        {
            "central_commutator": _matrix_zero(comm_b * Xb - Xb * comm_b)
            and _matrix_zero(comm_b * Yb - Yb * comm_b),
            "BCH_exact": _matrix_zero(
                sp.exp(Xb) * sp.exp(Yb) - sp.exp(Xb + Yb + comm_b / 2)
            ),
        },
        ("三阶 Heisenberg 幂零矩阵", "二重交换子为零"),
        "验证 BCH 在中心交换子实例上精确截断；一般级数收敛域另论。",
    )
    sqrt2 = sp.sqrt(2)
    Jp = sp.Matrix([[0, sqrt2, 0], [0, 0, sqrt2], [0, 0, 0]])
    Jm = Jp.T
    J3 = sp.diag(1, 0, -1)
    J1 = (Jp + Jm) / 2
    J2 = (Jp - Jm) / (2 * sp.I)
    Casimir = sp.simplify(J1 * J1 + J2 * J2 + J3 * J3)
    add(
        "22.03",
        {
            "su2_commutator": _matrix_zero(sp.simplify(J1 * J2 - J2 * J1 - sp.I * J3)),
            "j1_Casimir": _matrix_zero(Casimir - 2 * sp.eye(3)),
        },
        ("j=1、ℏ=1 的显式矩阵表示",),
        "验证一个不可约表示；半整数表示与群全局性质需另查。",
    )
    alpha1_22 = sp.Matrix([1, 0])
    alpha2_22 = sp.Matrix([-sp.Rational(1, 2), sp.sqrt(3) / 2])
    omega1_22 = sp.Matrix([sp.Rational(1, 2), 1 / (2 * sp.sqrt(3))])
    omega2_22 = sp.Matrix([0, 1 / sp.sqrt(3)])
    cartan22 = sp.Matrix(
        [
            [2 * alpha1_22.dot(alpha1_22), 2 * alpha1_22.dot(alpha2_22)],
            [2 * alpha2_22.dot(alpha1_22), 2 * alpha2_22.dot(alpha2_22)],
        ]
    )
    weight_pairing22 = sp.Matrix(
        [
            [2 * omega1_22.dot(alpha1_22), 2 * omega1_22.dot(alpha2_22)],
            [2 * omega2_22.dot(alpha1_22), 2 * omega2_22.dot(alpha2_22)],
        ]
    )
    p22, q22 = sp.symbols("p q", integer=True, nonnegative=True)
    dim_pq22 = (p22 + 1) * (q22 + 1) * (p22 + q22 + 2) / 2
    casimir_pq22 = (
        p22**2 + q22**2 + p22 * q22 + 3 * p22 + 3 * q22
    ) / 3
    add(
        "22.04",
        {
            "A2_Cartan_matrix": _matrix_zero(
                cartan22 - sp.Matrix([[2, -1], [-1, 2]])
            ),
            "fundamental_weight_duality": _matrix_zero(
                weight_pairing22 - sp.eye(2)
            ),
            "fundamental_dimension_Casimir": _zero(
                dim_pq22.subs({p22: 1, q22: 0}) - 3
            )
            and _zero(
                casimir_pq22.subs({p22: 1, q22: 0})
                - sp.Rational(4, 3)
            ),
            "adjoint_dimension_Casimir": _zero(
                dim_pq22.subs({p22: 1, q22: 1}) - 8
            )
            and _zero(casimir_pq22.subs({p22: 1, q22: 1}) - 3),
            "three_times_antithree": _zero(3 * 3 - 1 - 8),
        },
        ("SU(3) 根系采用 |alpha_i|^2=1 的二维归一化", "Dynkin 标号 (p,q) 为非负整数", "厄米生成元约定 [t^a,t^b]=if^{abc}t^c"),
        "精确验证 A2 简单根、基本权、维数与二次 Casimir 公式的 3 和 8 表示；权重 multiplicity 与一般张量积分解仍需表示论算法。",
    )
    N22, C22 = sp.symbols("N C", positive=True)
    haar_solution = sp.solve(sp.Eq(C22 * N22**2, N22), C22)[0]
    add(
        "22.05",
        {"normalization_constant": _zero(haar_solution - 1 / N22)},
        ("左右不变性已把二点积分限制为 C δ_il δ_jk", "∫dU=1"),
        "SymPy 只解归一化常数；Haar 存在唯一性和不变量张量由群论证明。",
    )

    # V23 粒子物理
    add(
        "23.01",
        {
            "up_charge": _zero(sp.Rational(1, 2) + sp.Rational(1, 6) - sp.Rational(2, 3)),
            "down_charge": _zero(-sp.Rational(1, 2) + sp.Rational(1, 6) + sp.Rational(1, 3)),
        },
        ("采用 Q=T3+Y、左手夸克双重态 Y=1/6",),
        "只核对电荷归一化；规范反常与完整粒子谱另验。",
    )
    add(
        "23.02",
        {"flavor_dimension": _zero(3**3 - (10 + 8 + 8 + 1))},
        ("三夸克 flavor SU(3) 张量积",),
        "维数相等是必要检查，不单独证明不可约分解。",
    )
    L23, S23 = sp.symbols("L S", integer=True, nonnegative=True)
    parity23 = (-1) ** (L23 + 1)
    charge23 = (-1) ** (L23 + S23)
    add(
        "23.03",
        {
            "pseudoscalar_0minusplus": _zero(parity23.subs(L23, 0) + 1)
            and _zero(charge23.subs({L23: 0, S23: 0}) - 1),
            "eigenvalues_square_to_one": _zero(parity23**2 - 1)
            and _zero(charge23**2 - 1),
        },
        ("中性 q qbar、L 与 S 为非负整数",),
        "不验证 flavor 相位和非自共轭强子的 C 标签。",
    )
    Gamma23, M23, s23, amplitude23 = sp.symbols(
        "Gamma M s amplitude", positive=True
    )
    tau23 = 1 / Gamma23
    dsigma23 = amplitude23**2 / (64 * sp.pi**2 * s23)
    sigma23 = 4 * sp.pi * dsigma23
    add(
        "23.04",
        {
            "lifetime_width": _zero(Gamma23 * tau23 - 1),
            "massless_2to2_solid_angle_integral": _zero(
                sigma23 - amplitude23**2 / (16 * sp.pi * s23)
            ),
            "phase_space_prefactor_dimension": _zero(
                (1 / (2 * M23)) * 2 * M23 - 1
            ),
        },
        ("自然单位 hbar=c=1", "质心系无质量 2->2 且末态可区分", "amplitude 与角度无关的教学模型"),
        "验证通量/两体相空间给出的 dσ/dΩ 与积分；自旋颜色平均、相同粒子因子、质量阈值和真实振幅需逐过程处理。",
    )
    Q23, Lam23, p23 = sp.symbols("Q Lambda p", positive=True)
    xconv23, yconv23 = sp.symbols("x y", positive=True)
    convolution23 = sp.integrate(xconv23 / yconv23, (yconv23, xconv23, 1))
    add(
        "23.05",
        {
            "power_suppression": _zero(sp.limit((Lam23 / Q23) ** p23, Q23, sp.oo)),
            "explicit_Mellin_convolution": _zero(
                convolution23 - xconv23 * sp.log(1 / xconv23)
            ),
        },
        ("p>0 且固定 Lambda", "0<x<1", "教学卷积取 f(y)=y、C(x/y)=x/y"),
        "只验证一个显式卷积和高尺度幂修正；QCD 因子化的区域分离、Glauber 条件与核的微扰计算不是 CAS 命题。",
    )

    # V24 量子场论深化
    x24 = sp.symbols("x", real=True)
    f24 = x24**5 + 2 * x24
    p_on_f = -sp.I * sp.diff(f24, x24)
    comm_xp = x24 * p_on_f - (-sp.I * sp.diff(x24 * f24, x24))
    add(
        "24.01",
        {"canonical_commutator_on_polynomial": _zero(comm_xp - sp.I * f24)},
        ("Schrödinger 表示 p=-i d/dx", "以多项式测试函数作精确代理"),
        "验证单自由度 [x,p]=i；场的分布 δ 与真空发散未由 SymPy 处理。",
    )
    psq24, msq24 = sp.symbols("p2 m2")
    propagator24 = sp.I / (psq24 - msq24)
    add(
        "24.02",
        {"inverse_kernel": _zero((psq24 - msq24) * propagator24 - sp.I)},
        ("远离极点 p²=m²", "iε 在纯代数代理中省略"),
        "不验证 Fourier 轮廓、因果边界和分布意义。",
    )
    J24 = sp.symbols("J")
    Z024 = sp.exp(J24**2 / 2)
    add(
        "24.03",
        {
            "Gaussian_fourth_derivative": _zero(
                sp.diff(Z024, J24, 4).subs(J24, 0) - 3
            )
        },
        ("零维 Gaussian 生成泛函代理",),
        "只验证四点 Wick 配对数 3；真实时空图、对称因子和正规化另算。",
    )
    s24, m24, Z24 = sp.symbols("s m Z", positive=True)
    pole24 = Z24 / (s24 - m24**2)
    add(
        "24.04",
        {"pole_residue": _zero(sp.limit((s24 - m24**2) * pole24, s24, m24**2) - Z24)},
        ("孤立单粒子简单极点",),
        "验证 LSZ 截肢的极点代数；渐近态存在和多粒子支切另论。",
    )
    mu24, masssq24, eps24, lambda24 = sp.symbols(
        "mu m2 epsilon lambda", positive=True
    )
    loop24 = (
        mu24**eps24
        * sp.gamma(eps24 / 2)
        * masssq24 ** (-eps24 / 2)
        / (4 * sp.pi) ** (2 - eps24 / 2)
    )
    loop_pole_residue24 = sp.limit(eps24 * loop24, eps24, 0, dir="+")
    beta_coefficient24 = sp.Rational(3, 1) / (16 * sp.pi**2)
    delta_lambda24 = 3 * lambda24**2 / (16 * sp.pi**2 * eps24)
    delta_from_channels24 = (
        sp.Rational(3, 2) * lambda24**2 * loop_pole_residue24 / eps24
    )
    reduced_bare24 = lambda24 + beta_coefficient24 * lambda24**2 / eps24
    beta_dimreg24 = -eps24 * lambda24 + beta_coefficient24 * lambda24**2
    fixed_bare_residual24 = sp.series(
        eps24 * reduced_bare24
        + sp.diff(reduced_bare24, lambda24) * beta_dimreg24,
        lambda24,
        0,
        3,
    ).removeO()
    add(
        "24.05",
        {
            "bubble_pole_residue": _zero(
                loop_pole_residue24 - 1 / (8 * sp.pi**2)
            ),
            "three_channel_counterterm": _zero(
                delta_from_channels24 - delta_lambda24
            ),
            "fixed_bare_coupling_RGE": _zero(fixed_bare_residual24),
            "four_dimensional_beta": _zero(
                beta_dimreg24.subs(eps24, 0)
                - 3 * lambda24**2 / (16 * sp.pi**2)
            ),
        },
        ("lambda phi^4/4! 于 d=4-epsilon", "Euclidean massive bubble、MS 极点部分", "三个 s/t/u 通道各含 1/2 对称因子"),
        "完整验证一圈 bubble 的极点、delta_lambda 与 beta_lambda=3lambda^2/(16pi^2)；有限部分、二圈、阈值与非微扰 triviality 不在本检查中。",
    )

    # V25 规范量子化
    D25 = sp.Matrix([[-1, 1, 0], [0, -1, 1], [1, 0, -1]])
    add(
        "25.01",
        {"periodic_divergence_zero_mode": _matrix_zero(D25 * sp.ones(3, 1))},
        ("一维周期有限差分作为 Gauss 散度代理",),
        "只验证常场散度为零；非 Abelian 约束代数与物理 Hilbert 空间另论。",
    )
    a25, b25, c25, d25 = sp.symbols("a b c d")
    M25 = sp.Matrix([[a25, b25], [c25, d25]])
    add(
        "25.02",
        {"FP_Jacobian": _zero(M25.det() - (a25 * d25 - b25 * c25))},
        ("以二维规范条件 Jacobian 代理 functional determinant",),
        "不处理无限维行列式、Gribov copies 或正则化。",
    )
    e1 = sp.Matrix([1, 0, 0])
    e2 = sp.Matrix([0, 1, 0])
    e3 = sp.Matrix([0, 0, 1])
    bracket = lambda u, v: u.cross(v)
    jacobi25 = (
        bracket(e1, bracket(e2, e3))
        + bracket(e2, bracket(e3, e1))
        + bracket(e3, bracket(e1, e2))
    )
    lowering25 = sp.Matrix([[0, 0], [1, 0]])
    grading25 = sp.diag(1, -1)
    ghost1_25 = sp.kronecker_product(lowering25, sp.eye(2))
    ghost2_25 = sp.kronecker_product(grading25, lowering25)
    Baux25, gauge_condition25, xi25, antighost25, s_gauge25 = sp.symbols(
        "B G xi bar_c sG"
    )
    gauge_fermion_variation25 = (
        Baux25 * (gauge_condition25 + xi25 * Baux25 / 2)
        - antighost25 * s_gauge25
    )
    add(
        "25.03",
        {
            "su2_Jacobi": _matrix_zero(jacobi25),
            "Grassmann_generators_nilpotent": _matrix_zero(ghost1_25**2)
            and _matrix_zero(ghost2_25**2),
            "Grassmann_generators_anticommute": _matrix_zero(
                ghost1_25 * ghost2_25 + ghost2_25 * ghost1_25
            ),
            "graded_gauge_fermion_variation": _zero(
                gauge_fermion_variation25
                - (
                    Baux25 * gauge_condition25
                    + xi25 * Baux25**2 / 2
                    - antighost25 * s_gauge25
                )
            ),
        },
        ("SU(2) 结构常数用三维叉积表示", "s bar_c=B、sB=0", "s(XY)=(sX)Y+(-1)^|X|X(sY)"),
        "有限矩阵实现验证两个 Grassmann 生成元和分次符号，并核对 s[bar_c(G+xi B/2)]；完整时空作用量、测度与 Gribov 问题仍需场论处理。",
    )
    q0, q1, p0, p1 = sp.symbols("q0 q1 p0 p1")
    gamma0 = sp.Matrix([[0, 1], [1, 0]])
    gamma1 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    slash = lambda u0, u1: u0 * gamma0 + u1 * gamma1
    add(
        "25.04",
        {
            "tree_Ward": _matrix_zero(
                slash(q0, q1)
                - (slash(p0 + q0, p1 + q1) - slash(p0, p1))
            )
        },
        ("树级逆传播子 S^{-1}=slash(p)", "二维 gamma 代理"),
        "只验证树级纵向恒等式；圈级 Slavnov--Taylor 含鬼核与重整化。",
    )
    yQ25 = sp.Rational(1, 6)
    yuC25 = -sp.Rational(2, 3)
    ydC25 = sp.Rational(1, 3)
    yL25 = -sp.Rational(1, 2)
    yeC25 = sp.Integer(1)
    anomaly_su3_25 = 2 * yQ25 / 2 + yuC25 / 2 + ydC25 / 2
    anomaly_su2_25 = 3 * yQ25 / 2 + yL25 / 2
    anomaly_u1_25 = (
        6 * yQ25**3
        + 3 * yuC25**3
        + 3 * ydC25**3
        + 2 * yL25**3
        + yeC25**3
    )
    anomaly_gravity25 = (
        6 * yQ25 + 3 * yuC25 + 3 * ydC25 + 2 * yL25 + yeC25
    )
    g25, FdualF25, mferm25, pseudoscalar25, flavors25 = sp.symbols(
        "g FtildeF m P N_f"
    )
    topological_density25 = g25**2 * FdualF25 / (32 * sp.pi**2)
    axial_divergence25 = (
        2 * sp.I * mferm25 * pseudoscalar25
        + 2 * flavors25 * topological_density25
    )
    add(
        "25.05",
        {
            "SU3_squared_U1": _zero(anomaly_su3_25),
            "SU2_squared_U1": _zero(anomaly_su2_25),
            "U1_cubed": _zero(anomaly_u1_25),
            "gravity_squared_U1": _zero(anomaly_gravity25),
            "axial_anomaly_normalization": _zero(
                axial_divergence25
                - 2 * sp.I * mferm25 * pseudoscalar25
                - flavors25 * g25**2 * FdualF25 / (16 * sp.pi**2)
            ),
        },
        ("一代标准模型全部写成左手 Weyl 场 Q,u^c,d^c,L,e^c", "T(fundamental)=1/2", "q(x)=g^2 F^a tildeF^a/(32pi^2)"),
        "精确核对四类局域规范反常及课程轴 Ward 恒等式系数；全局反常、正则化推导和非微扰拓扑涨落不由电荷求和证明。",
    )

    # V26 非微扰场论
    phi1, phi2, v26, lam26 = sp.symbols("phi1 phi2 v lambda", positive=True)
    V26expr = lam26 * (phi1**2 + phi2**2 - v26**2) ** 2 / 4
    Hess26 = sp.hessian(V26expr, (phi1, phi2)).subs({phi1: v26, phi2: 0})
    add(
        "26.01",
        {
            "radial_mass": _zero(Hess26[0, 0] - 2 * lam26 * v26**2),
            "Goldstone_mass": _zero(Hess26[1, 1]),
        },
        ("O(2) Mexican-hat 势", "在真空 (v,0) 展开"),
        "有限体积自发破缺与量子修正未包含。",
    )
    g26, A26, h26 = sp.symbols("g A h")
    kinetic26 = sp.expand(g26**2 * A26**2 * (v26 + h26) ** 2 / 2)
    add(
        "26.02",
        {
            "gauge_mass_coefficient": _zero(
                kinetic26.coeff(A26, 2).subs(h26, 0) - g26**2 * v26**2 / 2
            )
        },
        ("Abelian Higgs unitary-gauge 二次项代理",),
        "不证明规范不变可观测谱或非 Abelian 混合。",
    )
    d26 = sp.symbols("d")
    add(
        "26.03",
        {"operator_term_dimension": _zero((4 - d26) + d26 - 4)},
        ("四维时空", "O_d 的工程量纲为 d"),
        "只验证 Λ^{4-d} 配平；Wilson 系数大小与 EFT 幂计数需物理输入。",
    )
    x0_26, x1_26, x2_26, x3_26 = sp.symbols(
        "x_0 x_1 x_2 x_3", real=True
    )
    pauli1_26 = sp.Matrix([[0, 1], [1, 0]])
    pauli2_26 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    pauli3_26 = sp.diag(1, -1)
    radius_squared26 = x0_26**2 + x1_26**2 + x2_26**2 + x3_26**2
    winding_map26 = (
        x0_26 * sp.eye(2)
        + sp.I
        * (x1_26 * pauli1_26 + x2_26 * pauli2_26 + x3_26 * pauli3_26)
    )
    add(
        "26.04",
        {
            "S3_map_unitarity": _matrix_zero(
                sp.simplify(winding_map26.H * winding_map26 - radius_squared26 * sp.eye(2))
            ),
            "S3_map_determinant": _zero(
                sp.simplify(winding_map26.det() - radius_squared26)
            ),
            "unit_sphere_lands_in_SU2": _zero(
                winding_map26.det().subs(x0_26**2, 1 - x1_26**2 - x2_26**2 - x3_26**2) - 1
            ),
        },
        ("S3_infinity 以 x0^2+x1^2+x2^2+x3^2=1 表示", "SU(2) 基本表示 U=x0 I+i x·sigma"),
        "精确验证紧化空间的显式映射落在 SU(2)；pi_3(SU(N))=Z、绕数积分整数性与 instanton 作用量界仍由拓扑和场论证明。",
    )
    R26, T26, sigma26, mu26 = sp.symbols("R T sigma mu", positive=True)
    W26 = sp.exp(-sigma26 * R26 * T26 - mu26 * (R26 + T26))
    Vstatic26 = sp.limit(-sp.log(W26) / T26, T26, sp.oo)
    zcenter26, polyakov26, plaquette26 = sp.symbols(
        "z_center L_P U_square", nonzero=True
    )
    transformed_polyakov26 = zcenter26 * polyakov26
    transformed_plaquette26 = zcenter26 * (1 / zcenter26) * plaquette26
    add(
        "26.05",
        {
            "static_potential": _zero(Vstatic26 - (sigma26 * R26 + mu26)),
            "string_tension_slope": _zero(sp.diff(Vstatic26, R26) - sigma26),
            "Polyakov_loop_center_charge": _zero(
                transformed_polyakov26 - zcenter26 * polyakov26
            ),
            "plaquette_center_invariance": _zero(
                transformed_plaquette26 - plaquette26
            ),
        },
        ("面积律加周长律模型", "R,T>0", "纯 SU(N) 规范理论中某时间片链接乘 z in Z_N"),
        "验证 Wilson 面积律代理及 L_P->zL_P、局域 plaquette 不变；动力学基本表示夸克显式破坏中心对称，弦断裂和 crossover 需有限温度数据。",
    )

    # V27 格点谱学
    E0, E1, t27, A0, A1 = sp.symbols("E0 E1 t A0 A1", positive=True)
    Delta27 = sp.symbols("Delta", positive=True)
    ratio27 = (A1 * sp.exp(-E1 * t27)) / (A0 * sp.exp(-E0 * t27))
    ratio_gap27 = sp.simplify(ratio27.subs(E1, E0 + Delta27))
    add(
        "27.01",
        {
            "excited_state_ratio": _zero(
                ratio_gap27 - (A1 / A0) * sp.exp(-Delta27 * t27)
            ),
            "large_time_suppression": _zero(
                sp.limit(ratio_gap27, t27, sp.oo)
            ),
        },
        ("E1>E0>0；SymPy 的极限用正符号并在物理解释中要求正能隙",),
        "只验证两态比值；真实谱权重、边界和噪声需数据拟合。",
    )
    E27, T27, a27 = sp.symbols("E T a", positive=True)
    C27 = lambda tt: sp.cosh(E27 * (T27 / 2 - tt))
    cosh_ratio27 = sp.trigsimp(
        (C27(t27 - a27) + C27(t27 + a27)) / (2 * C27(t27))
    )
    add(
        "27.02",
        {"cosh_identity": _zero(cosh_ratio27 - sp.cosh(E27 * a27))},
        ("单一周期 cosh", "E,a>0"),
        "arccosh 主支和含噪非线性偏差需数值处理。",
    )
    t0_27 = sp.symbols("t0", positive=True)
    Cdiag_t = sp.diag(sp.exp(-E0 * t27), 2 * sp.exp(-E1 * t27))
    Cdiag_t0 = sp.diag(sp.exp(-E0 * t0_27), 2 * sp.exp(-E1 * t0_27))
    gevp_matrix = sp.simplify(Cdiag_t0.inv() * Cdiag_t)
    add(
        "27.03",
        {
            "GEVP_eigenvalues": _matrix_zero(
                gevp_matrix
                - sp.diag(
                    sp.exp(-E0 * (t27 - t0_27)),
                    sp.exp(-E1 * (t27 - t0_27)),
                )
            )
        },
        ("两个正交算符各耦合一个能态",),
        "有限算符基修正、条件化和近简并态追踪不由对角代理覆盖。",
    )
    V27mat = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    Box27 = V27mat * V27mat.T
    add(
        "27.04",
        {
            "orthonormal_columns": _matrix_zero(V27mat.T * V27mat - sp.eye(2)),
            "projector": _matrix_zero(Box27 * Box27 - Box27),
            "rank_trace": _zero(sp.trace(Box27) - 2),
        },
        ("3×2 实正交低模基作为 distillation 代理",),
        "不验证协变 Laplacian、perambulator 求逆或规范协变性。",
    )
    S27 = sp.eye(5)
    add(
        "27.05",
        {
            "subduction_unitarity": _matrix_zero(S27.H * S27 - sp.eye(5)),
            "J2_dimension": _zero(2 + 3 - 5),
        },
        ("J=2 的五维空间，以酉基变换代理 subduction",),
        "立方群系数与连续自旋的物理指认仍需特征标和谱数据。",
    )

    # V28 多强子与 Lüscher
    m28, p28 = sp.symbols("m p", positive=True)
    Efree28 = 2 * sp.sqrt(m28**2 + p28**2)
    add(
        "28.01",
        {
            "equal_mass_CM": _zero(
                Efree28
                - (
                    sp.sqrt(m28**2 + p28**2)
                    + sp.sqrt(m28**2 + (-p28) ** 2)
                )
            )
        },
        ("P=0、两粒子等质量",),
        "只验证连续色散运动学；实际格点应使用实测/格点色散。",
    )
    phi28 = -sp.Rational(35, 100) * sp.pi
    delta28 = sp.Rational(35, 100) * sp.pi
    add(
        "28.02",
        {"quantization_branch": _zero(delta28 + phi28)},
        ("选择 n=0 的连续相移分支",),
        "不计算 Z00；一般 moving-frame/分波混合需矩阵条件。",
    )
    a0_28, k28 = sp.symbols("a0 k", positive=True)
    denominator28 = -1 / a0_28 - sp.I * k28
    add(
        "28.03",
        {"bound_state_pole": _zero(denominator28.subs(k28, sp.I / a0_28))},
        ("忽略有效程", "采用课程的散射长度符号约定"),
        "近阈值参数化的收敛和 Riemann 片层需物理论证。",
    )
    k1, k2, b1, b2 = sp.symbols("k1 k2 b1 b2")
    quant28 = sp.diag(k1, k2) - sp.diag(b1, b2)
    add(
        "28.04",
        {
            "determinant_factorization": _zero(
                quant28.det() - (k1 - b1) * (k2 - b2)
            ),
            "zero_when_channel_matches": _zero(quant28.det().subs(k1, b1)),
        },
        ("两分波无非对角混合的有限维代理",),
        "真实盒矩阵 B、little group 和 lmax 截断需数值实现。",
    )
    M28, Gamma28 = sp.symbols("M Gamma", positive=True)
    Ep28 = M28 - sp.I * Gamma28 / 2
    add(
        "28.05",
        {
            "pole_mass": _zero(sp.re(Ep28) - M28),
            "pole_width": _zero(-2 * sp.im(Ep28) - Gamma28),
        },
        ("M、Γ 为正实数",),
        "只验证极点参数定义；耦合道幺正、解析延拓和留数需完整振幅。",
    )

    # V29 有限体积
    alpha29, L29, mm29, pp29 = sp.symbols("alpha L m p", positive=True, real=True)
    gaussian_image = sp.integrate(
        sp.exp(-alpha29 * pp29**2) * sp.exp(sp.I * L29 * mm29 * pp29),
        (pp29, -sp.oo, sp.oo),
    ) / (2 * sp.pi)
    gaussian_expected = (
        sp.exp(-L29**2 * mm29**2 / (4 * alpha29))
        / (2 * sp.sqrt(sp.pi * alpha29))
    )
    add(
        "29.01",
        {"Gaussian_image_transform": _zero(gaussian_image - gaussian_expected)},
        ("一维 Gaussian f、α>0",),
        "验证 Poisson 公式中的单个 Fourier 像；无限格点求和收敛另论。",
    )
    x29 = sp.symbols("x", positive=True)
    fv29 = sp.exp(-x29) / x29 ** sp.Rational(3, 2)
    ratio29 = sp.simplify(fv29.subs(x29, 6) / fv29.subs(x29, 4))
    add(
        "29.02",
        {
            "mPiL_ratio": _zero(
                ratio29 - sp.exp(-2) * (sp.Rational(2, 3)) ** sp.Rational(3, 2)
            )
        },
        ("仅保留首个 e^{-x}/x^{3/2} 项",),
        "观测量系数、多绕行和更重态未验证。",
    )
    Lsym29, const29 = sp.symbols("L C", positive=True)
    leading_shift29 = const29 / Lsym29**3
    add(
        "29.03",
        {
            "doubling_volume": _zero(
                leading_shift29.subs(Lsym29, 2 * Lsym29) / leading_shift29
                - sp.Rational(1, 8)
            )
        },
        ("阈值能移仅保留 L^{-3} 首项",),
        "a0/L 高阶、有效程和完整 Lüscher 条件未包含。",
    )
    n29 = sp.symbols("n", integer=True)
    theta29 = sp.symbols("theta", real=True)
    phase29 = sp.exp(sp.I * (2 * sp.pi * n29 + theta29))
    add(
        "29.04",
        {"twisted_boundary_phase": _zero(sp.simplify(phase29 - sp.exp(sp.I * theta29)))},
        ("n 为整数",),
        "不验证 partial twisting 的海夸克和 annihilation 有限体积效应。",
    )
    Q29, alphaQ29, cQ29 = sp.symbols("Q alpha c", positive=True)
    qed29 = alphaQ29 * Q29**2 * cQ29
    add(
        "29.05",
        {
            "charge_squared_scaling": _zero(
                qed29.subs(Q29, 2) / qed29.subs(Q29, 1) - 4
            ),
            "neutral_limit": _zero(qed29.subs(Q29, 0)),
        },
        ("同一 QED 零模方案和盒长",),
        "不固定 QED_L/QED_TL 的普适系数或结构项。",
    )

    # V30 有限温度
    Nt30, at30 = sp.symbols("Nt at", positive=True)
    Temp30 = 1 / (Nt30 * at30)
    add(
        "30.01",
        {"thermal_circle": _zero(Temp30 * Nt30 * at30 - 1)},
        ("自然单位 kB=ℏ=c=1",),
        "不验证路径积分测度和费米反周期迹符号。",
    )
    z30 = sp.exp(2 * sp.pi * sp.I / 3)
    add(
        "30.02",
        {
            "Z3_center": _zero(sp.simplify(z30**3 - 1)),
            "plaquette_center_cancel": _zero(sp.simplify(z30 * sp.conjugate(z30) - 1)),
        },
        ("SU(3) 中心元 z=e^{2πi/3}",),
        "静态自由能重整化和动力学夸克显式破缺未验证。",
    )
    m30, A30, B30, C30, Tv30, Vol30 = sp.symbols(
        "m A B C T V", real=True
    )
    lnZ30 = A30 + B30 * m30 + C30 * m30**2
    condensate30 = Tv30 / Vol30 * sp.diff(lnZ30, m30)
    susceptibility30 = sp.diff(condensate30, m30)
    add(
        "30.03",
        {
            "condensate_derivative": _zero(
                condensate30 - Tv30 / Vol30 * (B30 + 2 * C30 * m30)
            ),
            "susceptibility": _zero(
                susceptibility30 - 2 * C30 * Tv30 / Vol30
            ),
        },
        ("ln Z 的二阶局部 Taylor 代理", "V非零"),
        "真实 stochastic trace、加性/乘性重整化和临界缩放未处理。",
    )
    T30 = sp.symbols("T", positive=True)
    pfun = sp.Function("p")
    identity30 = sp.simplify(
        T30**5 * sp.diff(pfun(T30) / T30**4, T30)
        - (T30 * sp.diff(pfun(T30), T30) - 4 * pfun(T30))
    )
    c30, T0_30 = sp.symbols("c T0", positive=True)
    integral30 = sp.integrate(c30 / T30, (T30, T0_30, sp.symbols("T1", positive=True)))
    T1_30 = sp.symbols("T1", positive=True)
    integral30 = sp.integrate(c30 / T30, (T30, T0_30, T1_30))
    add(
        "30.04",
        {
            "trace_identity": _zero(identity30),
            "constant_I_over_T4": _zero(
                integral30 - c30 * sp.log(T1_30 / T0_30)
            ),
        },
        ("p 可微", "第二项取 I/T⁴=c"),
        "格点 beta functions、零温扣除和积分常数需实测。",
    )
    tau30, beta30, omega30 = sp.symbols("tau beta omega", positive=True)
    kernel30 = sp.cosh(omega30 * (tau30 - beta30 / 2)) / sp.sinh(
        omega30 * beta30 / 2
    )
    add(
        "30.05",
        {
            "midpoint_kernel": _zero(
                kernel30.subs(tau30, beta30 / 2)
                - 1 / sp.sinh(omega30 * beta30 / 2)
            ),
            "finite_matrix_rank_bound": sp.Matrix([[1, 0, 1], [0, 1, 1]]).rank() <= 2,
        },
        ("ω,β>0", "2×3 矩阵作欠定离散核代理"),
        "不证明连续谱唯一性；先验偏差必须用 mock-data 覆盖。",
    )

    # V31 费米子方案
    a31, Delta31, mpi31 = sp.symbols("a Delta mpi", positive=True)
    mtaste31 = mpi31**2 + a31**2 * Delta31
    add(
        "31.01",
        {"taste_restoration": _zero(sp.limit(mtaste31, a31, 0) - mpi31**2)},
        ("taste 劈裂领先 O(a²)",),
        "rooting 的局域性和正确 universality 不能由质量极限单独证明。",
    )
    alpha31, Ls31, A31 = sp.symbols("alpha Ls A", positive=True)
    mres31 = A31 * sp.exp(-alpha31 * Ls31)
    add(
        "31.02",
        {
            "Ls_increment_ratio": _zero(
                sp.simplify(
                    mres31.subs(Ls31, Ls31 + 10) / mres31
                    - sp.exp(-10 * alpha31)
                )
            ),
            "infinite_Ls": _zero(sp.limit(mres31, Ls31, sp.oo)),
        },
        ("单一 mobility-gap 指数模型",),
        "dislocation 尾、M5 调谐和 Ward identity 需真实数据。",
    )
    gamma5_31 = sp.diag(1, -1)
    epsilon31 = sp.Matrix([[0, 1], [1, 0]])
    D31 = sp.eye(2) + gamma5_31 * epsilon31
    add(
        "31.03",
        {
            "sign_squared": _matrix_zero(epsilon31 * epsilon31 - sp.eye(2)),
            "Ginsparg_Wilson": _matrix_zero(
                gamma5_31 * D31
                + D31 * gamma5_31
                - D31 * gamma5_31 * D31
            ),
        },
        ("设 a=1 的 2×2 Hermitian-unitary sign kernel 代理",),
        "不验证 overlap 局域性、低模近似误差或 index theorem。",
    )
    O0_31, c2_31 = sp.symbols("O0 c2")
    O31 = O0_31 + c2_31 * a31**2
    add(
        "31.04",
        {
            "automatic_Oa_improvement": _zero(sp.diff(O31, a31).subs(a31, 0)),
            "continuum_limit": _zero(sp.limit(O31, a31, 0) - O0_31),
        },
        ("最大扭转已由对称性消去线性 a 项",),
        "不验证 PCAC 临界质量调谐和 flavor/parity O(a²) 劈裂。",
    )
    B0_31, mv31, ms31, Dmix31 = sp.symbols("B0 mv ms Dmix", positive=True)
    mixed31 = B0_31 * (mv31 + ms31) + a31**2 * Dmix31
    add(
        "31.05",
        {
            "mixed_action_continuum": _zero(
                sp.limit(mixed31, a31, 0) - B0_31 * (mv31 + ms31)
            )
        },
        ("mixed-action 特有项领先 O(a²)",),
        "partial-quenching double poles 与 EFT 高阶未验证。",
    )

    # V32 改进、边界与尺度
    c1_32 = sp.Rational(-1, 12)
    c0_32 = 1 - 8 * c1_32
    add(
        "32.01",
        {
            "normalization": _zero(c0_32 + 8 * c1_32 - 1),
            "tree_Symanzik_c0": _zero(c0_32 - sp.Rational(5, 3)),
        },
        ("采用 c0+8c1=1 的 loop 计数约定", "c1=-1/12"),
        "不验证 action 的 BCH 全展开、圈级改进或实际旋转破缺。",
    )
    xi32, asp32, c32 = sp.symbols("xi asp c", positive=True)
    momentum_term32 = c32**2 * asp32**2 / xi32**2
    add(
        "32.02",
        {
            "anisotropic_example": _zero(
                momentum_term32.subs(
                    {xi32: 4, asp32: sp.Rational(4, 5), c32: 1}
                )
                - sp.Rational(1, 25)
            ),
            "isotropic_limit": _zero(momentum_term32.subs(xi32, 1) - c32**2 * asp32**2),
        },
        ("连续色散乘 a_t² 的代数代理",),
        "重整化各向异性必须由实测色散调谐。",
    )
    r1_32, r2_32, sigma32, N32 = sp.symbols(
        "rho1 rho2 sigma N", positive=True
    )
    tauint32 = sp.Rational(1, 2) + r1_32 + r2_32
    variance32 = 2 * tauint32 * sigma32**2 / N32
    add(
        "32.03",
        {
            "variance_expansion": _zero(
                variance32
                - sigma32**2 / N32 * (1 + 2 * r1_32 + 2 * r2_32)
            ),
            "independent_limit": _zero(
                variance32.subs({r1_32: 0, r2_32: 0}) - sigma32**2 / N32
            ),
        },
        ("只保留两个滞后相关系数的平稳链代理",),
        "真实 τint 的窗口选择、慢尾和拓扑遍历需时间序列诊断。",
    )
    x32, T32, mgap32, Amp32 = sp.symbols("x T mgap A", positive=True)
    left32 = Amp32 * sp.exp(-mgap32 * x32)
    right32 = Amp32 * sp.exp(-mgap32 * (T32 - x32))
    add(
        "32.04",
        {
            "reflection_pair": _zero(
                left32.subs(x32, T32 - x32) - right32
            ),
            "deep_bulk_suppression": _zero(
                sp.limit(Amp32 * sp.exp(-mgap32 * x32), x32, sp.oo)
            ),
        },
        ("单一正质量隙边界态",),
        "有限 T 的 min 距离、边界反项和 bulk 平台需数据验证。",
    )
    tphys32, tlatt32, aM32, hbarc32 = sp.symbols(
        "tphys tlatt aM hbarc", positive=True
    )
    alattice32 = sp.sqrt(tphys32) / sp.sqrt(tlatt32)
    Mphys32 = aM32 / alattice32 * hbarc32
    add(
        "32.05",
        {
            "scale_identity": _zero(alattice32**2 * tlatt32 - tphys32),
            "mass_conversion": _zero(Mphys32 * alattice32 - aM32 * hbarc32),
        },
        ("tlatt=t0/a²、tphys=t0phys",),
        "不确定度相关传播和不同尺度间的连续一致性需重采样。",
    )

    # V33 局域重整化
    O33 = sp.Matrix([1, 2])
    Z33 = sp.diag(2, 3)
    C33 = sp.diag(sp.Rational(11, 10), sp.Rational(9, 10))
    add(
        "33.01",
        {
            "matrix_order": _matrix_zero(
                C33 * Z33 * O33
                - sp.Matrix([sp.Rational(11, 5), sp.Rational(27, 5)])
            )
        },
        ("二维对角 mixing/conversion 数值代理",),
        "实际算符基、power mixing 和 perturbative truncation 未验证。",
    )
    Zq33 = sp.Rational(4, 5)
    projected33 = sp.Rational(5, 4)
    ZO33 = Zq33 / projected33
    add(
        "33.02",
        {
            "RI_MOM_condition": _zero(ZO33 / Zq33 * projected33 - 1),
            "example_ZO": _zero(ZO33 - sp.Rational(16, 25)),
        },
        ("标量投影顶角代理",),
        "Landau 规范、Goldstone pole、H(4) 和窗口问题需格点数据。",
    )
    mu33 = sp.symbols("mu", positive=True)
    dot33 = (mu33**2 + mu33**2 - mu33**2) / 2
    add(
        "33.03",
        {"symmetric_dot_product": _zero(dot33 - mu33**2 / 2)},
        ("p1²=p2²=(p1-p2)²=μ²",),
        "只验证非例外运动学；projector 与 MSbar conversion 需具体方案。",
    )
    sigma1_33, sigma2_33 = sp.symbols("sigma1 sigma2")
    add(
        "33.04",
        {
            "two_step_composition": _zero(
                (sp.Rational(11, 10) * sp.Rational(21, 20))
                - sp.Rational(231, 200)
            ),
            "identity_step": _zero(sp.Integer(1) * sigma1_33 - sigma1_33),
        },
        ("连续 step factors 按尺度链相乘",),
        "每步的调谐、相关误差与 a/L 连续外推未验证。",
    )
    add(
        "33.05",
        {
            "discrete_beta_example": _zero(
                (sp.Rational(46, 10) - 4) / sp.log(4)
                - sp.Rational(3, 5) / sp.log(4)
            ),
            "no_running_limit": _zero((mu33 - mu33) / sp.log(4)),
        },
        ("s=2 且采用课程 beta_s 符号",),
        "不验证 flow coupling 的 tree normalization、scheme 或连续外推。",
    )

    # V34 非局域与 TMD 重整化
    dm34, z1_34, z2_34, a34 = sp.symbols(
        "dm z1 z2 a", positive=True
    )
    line34 = lambda zz: sp.exp(-dm34 * zz / a34)
    add(
        "34.01",
        {
            "line_exponent_additivity": _zero(
                sp.simplify(line34(z1_34 + z2_34) - line34(z1_34) * line34(z2_34))
            ),
            "zero_length": _zero(line34(0) - 1),
        },
        ("同一路径、同一 δm，z1,z2>0",),
        "端点/cusp 对数、mixing 与 flow scheme 仍需独立处理。",
    )
    Delta34, z34 = sp.symbols("Delta z", positive=True)
    add(
        "34.02",
        {
            "auxiliary_mass_shift": _zero(
                sp.exp(-(dm34 + Delta34) * z34)
                / sp.exp(-dm34 * z34)
                - sp.exp(-Delta34 * z34)
            )
        },
        ("辅助静态传播子使用单一质量移位",),
        "不验证路径有序、表示、cusp 或端点 current mixing。",
    )
    Z34, h34, h034 = sp.symbols("Z h h0", nonzero=True)
    ratio34 = (Z34 * h34) / (Z34 * h034)
    add(
        "34.03",
        {
            "common_Z_cancels": _zero(sp.simplify(ratio34 - h34 / h034)),
            "identity_ratio": _zero(ratio34.subs(h34, h034) - 1),
        },
        ("分子分母 UV 因子完全相同且分母非零",),
        "不同长度/几何的 Z 比、IR 参考依赖和绝对匹配未验证。",
    )
    hzs34, hbzs34 = sp.symbols("h_zs hb_zs", nonzero=True)
    zswitch34 = sp.symbols("zs", positive=True)
    long_branch34 = (
        hzs34
        * sp.exp(dm34 * (z34 - zswitch34) / a34)
        * (sp.symbols("hb_z") / hbzs34)
    )
    add(
        "34.04",
        {
            "hybrid_continuity": _zero(
                long_branch34.subs(
                    {z34: zswitch34, sp.symbols("hb_z"): hbzs34}
                )
                - hzs34
            )
        },
        ("在 z=zs 使用同一裸锚点",),
        "指数符号、zs 窗口、导数平滑和 Fourier 系统学需方案扫描。",
    )
    y34, K34 = sp.symbols("y K", positive=True)
    F34 = y34**K34
    add(
        "34.05",
        {
            "soft_example": _zero(
                sp.Rational(4, 5) / sp.sqrt(sp.Rational(16, 25)) - 1
            ),
            "CS_log_derivative": _zero(
                y34 * sp.diff(sp.log(F34), y34) - K34
            ),
        },
        ("y=sqrt(zeta)>0", "soft 数值只作代数代理"),
        "不证明 soft 几何匹配、rapidity 因子化、flow conversion 或胶子 matching。",
    )

    # V35 联合设计与资格考核
    a35, P35, tau35, ell35 = sp.symbols(
        "a P tau ell", positive=True
    )
    target35 = sp.symbols("target")
    surrogate35 = (
        target35 + a35**2 + 1 / P35**2 + tau35 + sp.exp(-ell35)
    )
    limit35 = sp.limit(
        sp.limit(
            sp.limit(sp.limit(surrogate35, a35, 0), P35, sp.oo),
            tau35,
            0,
        ),
        ell35,
        sp.oo,
    )
    add(
        "35.01",
        {"ordered_target_limit": _zero(limit35 - target35)},
        ("可分离领先修正代理", "按预注册顺序取极限"),
        "实际 estimand 还需 scheme、soft、匹配、交叉项和可识别性。",
    )
    sigA35, sigB35, rho35 = sp.symbols("sigA sigB rho", positive=True)
    total35 = sigA35**2 + sigB35**2 + 2 * rho35 * sigA35 * sigB35
    d35, ca35, ct35 = sp.symbols("d_Gamma c_at c_t", positive=True)
    converted_flow35 = (
        target35
        + ca35 * a35**2 / (8 * tau35)
        + ct35 * tau35 / d35**2
    )
    continuum_then_flow35 = sp.limit(
        sp.limit(converted_flow35, a35, 0), tau35, 0
    )
    b35, z35, ds35, df35, db35, iq35 = sp.symbols(
        "b_T z d_source d_sink d_boundary Lambda_inverse", positive=True
    )
    support_min35 = sp.Min(b35, z35, ell35, iq35, ds35, df35, db35)
    add(
        "35.02",
        {
            "independent_3_4": _zero(
                sp.sqrt(total35.subs({sigA35: 3, sigB35: 4, rho35: 0})) - 5
            ),
            "fully_correlated_3_4": _zero(
                sp.sqrt(total35.subs({sigA35: 3, sigB35: 4, rho35: 1})) - 7
            ),
            "continuum_before_flow_reaches_target": _zero(
                continuum_then_flow35 - target35
            ),
            "flow_before_continuum_is_singular": (
                sp.limit(converted_flow35, tau35, 0, dir="+") is sp.oo
            ),
            "source_distance_enters_window": _zero(
                support_min35.subs(
                    {b35: 5, z35: 6, ell35: 7, iq35: 8,
                     ds35: 2, df35: 9, db35: 10}
                ) - 2
            ),
            "sink_distance_enters_window": _zero(
                support_min35.subs(
                    {b35: 5, z35: 6, ell35: 7, iq35: 8,
                     ds35: 9, df35: 2, db35: 10}
                ) - 2
            ),
            "boundary_distance_enters_window": _zero(
                support_min35.subs(
                    {b35: 5, z35: 6, ell35: 7, iq35: 8,
                     ds35: 9, df35: 10, db35: 2}
                ) - 2
            ),
        },
        (
            "两项标准差取正、rho=0 或 1",
            "a,tau,d_Gamma>0，先在固定正 tau 取 a->0",
            "d_Gamma 取整条路径到源、汇、时间边界及非零几何尺度的最小值",
            "finite-staple 已完成完整 C_Gamma 转换",
        ),
        "精确验证协方差两极端、有序极限和三类安全距离都能主导 flow window；不证明非局域 C_Gamma 的路径、端点、cusp、mixing 或方案转换，缺核时仍须停止在 finite-flow prototype。",
    )
    lam35 = sp.symbols("lambda", positive=True)
    Kmat35 = sp.Matrix([[1, 0], [0, 1], [1, 1]])
    Lmat35 = sp.eye(2)
    hvec35 = sp.Matrix(sp.symbols("h0:3"))
    fsol35 = (
        Kmat35.T * Kmat35 + lam35 * Lmat35.T * Lmat35
    ).inv() * Kmat35.T * hvec35
    normal_residual35 = (
        (Kmat35.T * Kmat35 + lam35 * Lmat35.T * Lmat35) * fsol35
        - Kmat35.T * hvec35
    )
    add(
        "35.03",
        {
            "Tikhonov_normal_equation": _matrix_zero(
                sp.simplify(normal_residual35)
            ),
            "nullity_lower_bound": 80 - 20 >= 60,
        },
        ("单位协方差、L=I 的有限矩阵代理", "lambda>0"),
        "物理约束、分辨核、νmax 和正则化覆盖需 mock-data 实测。",
    )
    H35 = sp.Function("H")
    Hin35, Hcfg35, Hcode35, Henv35, Hcode2_35 = sp.symbols(
        "Hin Hcfg Hcode Henv Hcode2"
    )
    digest35 = H35(Hin35, Hcfg35, Hcode35, Henv35)
    add(
        "35.04",
        {
            "deterministic_digest": digest35
            == H35(Hin35, Hcfg35, Hcode35, Henv35),
            "code_dependency": digest35
            != H35(Hin35, Hcfg35, Hcode2_35, Henv35),
        },
        ("H 视为输入元组的确定性内容摘要构造",),
        "不证明密码学抗碰撞、规范化编码或并行 bitwise reproducibility。",
    )
    Csample35 = sp.Matrix([1, 3])
    Lsample35 = sp.Matrix([3, 1])
    mean_product35 = (
        sum(Csample35) / 2
    ) * (sum(Lsample35) / 2)
    mean_joint35 = sum(
        Csample35[i] * Lsample35[i] for i in range(2)
    ) / 2
    add(
        "35.05",
        {
            "joint_not_product_of_means": not _zero(mean_joint35 - mean_product35),
            "covariance_value": _zero(mean_joint35 - mean_product35 + 1),
        },
        ("两个逐组态样本的精确反例",),
        "只证明均值乘积不能恢复 connected covariance；完整生产链仍需真实数据全门验证。",
    )

    return tuple(records)


def build_records() -> Tuple[ValidationRecord, ...]:
    records: List[ValidationRecord] = []

    def add(
        code: str,
        title: str,
        checks: Mapping[str, bool],
        assumptions: Sequence[str],
        boundary: str,
    ) -> None:
        records.append(_record(code, title, checks, assumptions, boundary))

    def add_my(code: str, title: str, name: str, boundary: str) -> None:
        records.append(_from_myqcd(code, title, name, boundary))

    # V01 数学语言
    M, Ld, Tm = sp.symbols("M L T", positive=True)
    dim_m = sp.Matrix([1, 0, 0])
    dim_a = sp.Matrix([0, 1, -2])
    add(
        "01.01",
        "量纲指数相加",
        {"force_dimension": _matrix_zero(dim_m + dim_a - sp.Matrix([1, 1, -2]))},
        ("基本量取 M,L,T", "乘法对应量纲指数相加"),
        "量纲一致只是否定错误的必要条件，不证明动力学公式。",
    )
    x, b = sp.symbols("x b", positive=True)
    add(
        "01.02",
        "对数换底",
        {
            "base_e": _zero((sp.log(x) / sp.log(sp.E)) - sp.log(x)),
            "inverse_definition": _zero(
                sp.log(b ** (sp.log(x) / sp.log(b))) - sp.log(x)
            ),
        },
        ("x>0", "b>0 且 b≠1；第二项在实主值对数域"),
        "不验证数据是否真的服从幂律或指数律。",
    )
    theta = sp.symbols("theta", real=True)
    euler_residual = sp.expand_complex(sp.exp(sp.I * theta)) - (
        sp.cos(theta) + sp.I * sp.sin(theta)
    )
    add(
        "01.03",
        "Euler 公式与单位模",
        {
            "euler": _zero(euler_residual),
            "unit_modulus": _zero(
                (sp.cos(theta) + sp.I * sp.sin(theta))
                * (sp.cos(theta) - sp.I * sp.sin(theta))
                - 1
            ),
        },
        ("theta 为实数",),
        "复相位的物理可观测性还需具体算符和对称性。",
    )
    n = sp.symbols("n", integer=True, positive=True)
    add(
        "01.04",
        "幂函数求导",
        {"power_rule": _zero(sp.diff(x**n, x) - n * x ** (n - 1))},
        ("n 为正整数；一般实/复幂需指定分支",),
        "数值差分的舍入误差不在符号检查内。",
    )
    a0, a1 = sp.symbols("a_0 a_1", real=True)
    f = x**4 - 3 * x + 2
    add(
        "01.05",
        "微积分基本定理的多项式实例",
        {
            "endpoint_difference": _zero(
                sp.integrate(sp.diff(f, x), (x, a0, a1))
                - (f.subs(x, a1) - f.subs(x, a0))
            )
        },
        ("以四次多项式作精确代表", "积分端点为实数"),
        "一般函数需满足可积性和绝对连续等分析条件。",
    )

    # V02 线性代数与对称性
    c, s, vx, vy = sp.symbols("c s v_x v_y", real=True)
    rotation_angle = sp.symbols("rotation_angle", real=True)
    R = sp.Matrix(
        [
            [sp.cos(rotation_angle), -sp.sin(rotation_angle)],
            [sp.sin(rotation_angle), sp.cos(rotation_angle)],
        ]
    )
    v = sp.Matrix([vx, vy])
    rotated_norm = (R * v).dot(R * v) - v.dot(v)
    add(
        "02.01",
        "正交变换保持长度",
        {"norm": _zero(sp.trigsimp(rotated_norm))},
        ("二维实向量", "R 使用显式 sin/cos 参数化"),
        "有限维正交代理；Lorentz 变换使用不同度规。",
    )
    aa, bb, cc, dd = sp.symbols("a b c d")
    A2 = sp.Matrix([[aa, bb], [cc, dd]])
    inv_candidate = sp.Matrix([[dd, -bb], [-cc, aa]]) / (aa * dd - bb * cc)
    add(
        "02.02",
        "二阶矩阵逆",
        {
            "left_inverse": _matrix_zero(sp.simplify(A2 * inv_candidate - sp.eye(2))),
            "right_inverse": _matrix_zero(sp.simplify(inv_candidate * A2 - sp.eye(2))),
        },
        ("ad-bc 非零", "元素可交换"),
        "大稀疏矩阵的稳定求解和条件数需数值验证。",
    )
    lam_plus, lam_minus = aa + bb, aa - bb
    vp = sp.Matrix([1, 1]) / sp.sqrt(2)
    vm = sp.Matrix([1, -1]) / sp.sqrt(2)
    Asym = sp.Matrix([[aa, bb], [bb, aa]])
    reconstructed = lam_plus * (vp * vp.T) + lam_minus * (vm * vm.T)
    add(
        "02.03",
        "对称二阶矩阵谱分解",
        {
            "reconstruction": _matrix_zero(sp.simplify(reconstructed - Asym)),
            "orthonormal": _matrix_zero(
                sp.Matrix.hstack(vp, vm).T * sp.Matrix.hstack(vp, vm)
                - sp.eye(2)
            ),
        },
        ("a,b 为实数", "展示一个可完全解析的厄米实例"),
        "一般厄米谱定理由线性代数证明；近简并数值稳定性另测。",
    )
    eps = sp.Matrix([[0, 1], [-1, 0]])
    add(
        "02.04",
        "二维 Levi--Civita 缩并",
        {"epsilon_contraction": _matrix_zero(eps * eps.T - sp.eye(2))},
        ("epsilon_12=1",),
        "高维缩并的符号取决于指标位置和度规约定。",
    )
    sigma3 = sp.diag(1, -1)
    U2 = sp.diag(sp.exp(sp.I * theta / 2), sp.exp(-sp.I * theta / 2))
    add(
        "02.05",
        "SU(2) 一参数子群",
        {
            "unitary": _matrix_zero(sp.simplify(U2.conjugate().T * U2 - sp.eye(2))),
            "det_one": _zero(U2.det() - 1),
            "generator_derivative": _matrix_zero(
                sp.diff(U2, theta).subs(theta, 0) - sp.I * sigma3 / 2
            ),
        },
        ("theta 为实数",),
        "仅验证 SU(2) 对角子群，不代替一般 SU(3) 群算法。",
    )

    # V03 Fourier、概率与数值
    N4 = 4
    W = sp.Matrix(
        N4,
        N4,
        lambda k, j: sp.exp(-2 * sp.pi * sp.I * k * j / N4),
    )
    add(
        "03.01",
        "N=4 离散 Fourier 正交性",
        {"inverse": _matrix_zero(sp.simplify(W.conjugate().T * W / N4 - sp.eye(N4)))},
        ("采用正变换无 1/N、逆变换含 1/N", "N=4 精确代表"),
        "一般 N 的几何级数证明在课件中给出；FFT 轴与符号仍需实现测试。",
    )
    sigma, k = sp.symbols("sigma k", positive=True, real=True)
    gaussian_ft = sp.integrate(
        sp.exp(-x**2 / (2 * sigma**2)) * sp.exp(-sp.I * k * x),
        (x, -sp.oo, sp.oo),
    )
    add(
        "03.02",
        "高斯 Fourier 变换",
        {
            "gaussian_transform": _zero(
                gaussian_ft
                - sp.sqrt(2 * sp.pi) * sigma * sp.exp(-sigma**2 * k**2 / 2)
            )
        },
        ("sigma>0", "k 为实数"),
        "有限盒子、离散采样和混叠需数值收敛测试。",
    )
    xs = sp.symbols("x0:4", real=True)
    av, shift, scale = sp.symbols("mu b a", real=True)
    mean_x = sum(xs) / 4
    var_x = sum((q - mean_x) ** 2 for q in xs) / 4
    ys = [scale * q + shift for q in xs]
    mean_y = sum(ys) / 4
    var_y = sum((q - mean_y) ** 2 for q in ys) / 4
    add(
        "03.03",
        "有限样本总体方差的仿射变换",
        {"variance_scaling": _zero(sp.expand(var_y - scale**2 * var_x))},
        ("四个等权实样本作精确代理", "方差使用 1/N 定义"),
        "抽样方差、协方差估计和自相关另行处理。",
    )
    h = sp.symbols("h", positive=True)
    f_generic = sp.Function("f")
    poly = x**5 + 2 * x**3 - x
    central = (poly.subs(x, x + h) - poly.subs(x, x - h)) / (2 * h)
    expected = sp.diff(poly, x) + h**2 * sp.diff(poly, x, 3) / 6 + h**4 * sp.diff(poly, x, 5) / 120
    add(
        "03.04",
        "中心差分 Taylor 展开",
        {"through_h4": _zero(sp.expand(central - expected))},
        ("以五次多项式使展开精确终止",),
        "一般光滑函数余项为 O(h^6)（除以 h 后对应式中 O(h^6) 之后）。",
    )
    nn = sp.symbols("N", integer=True, positive=True)
    Lbox = sp.symbols("L", positive=True)
    hh = Lbox / nn
    j = sp.symbols("j", integer=True)
    trapezoid = hh * (
        sp.summation((j * hh) ** 2, (j, 1, nn - 1)) + Lbox**2 / 2
    )
    add(
        "03.05",
        "复合梯形法二次函数误差",
        {
            "exact_error": _zero(
                sp.simplify(trapezoid - Lbox**3 / 3 - Lbox * hh**2 / 6)
            )
        },
        ("N 为正整数", "h=L/N"),
        "浮点舍入、一般函数高阶导数界和自适应策略不在此恒等式内。",
    )

    # V04 时空与经典场
    beta, ct, xx = sp.symbols("beta ct x", real=True)
    gamma = 1 / sp.sqrt(1 - beta**2)
    ctp = gamma * (ct - beta * xx)
    xp = gamma * (xx - beta * ct)
    add(
        "04.01",
        "1+1 维 Lorentz 间隔",
        {"interval": _zero(sp.simplify(ctp**2 - xp**2 - (ct**2 - xx**2)))},
        ("|beta|<1", "度规号差 (+,-)"),
        "只验证标准 boost；一般四维协变由矩阵度规条件给出。",
    )
    E, p, m = sp.symbols("E p m", real=True)
    four_norm = E**2 - p**2
    add(
        "04.02",
        "四动量质壳",
        {"mass_shell_rearrangement": _zero((four_norm - m**2) - (E**2 - p**2 - m**2))},
        ("自然单位 c=1", "选择正能支需额外物理条件"),
        "格点色散伪影不由连续代数式给出。",
    )
    t, mass, spring = sp.symbols("t m k", positive=True, real=True)
    q = sp.Function("q")(t)
    qdot = sp.diff(q, t)
    lag = mass * qdot**2 / 2 - spring * q**2 / 2
    euler = sp.diff(sp.diff(lag, qdot), t) - sp.diff(lag, q)
    add(
        "04.03",
        "谐振子 Euler--Lagrange 方程",
        {"equation": _zero(euler - (mass * sp.diff(q, t, 2) + spring * q))},
        ("端点变分为零", "m,k 为正"),
        "只验证变分结果的代数形式；泛函分析条件在正文说明。",
    )
    amp, omega = sp.symbols("A omega", positive=True, real=True)
    qsol = amp * sp.cos(omega * t)
    energy = mass * sp.diff(qsol, t) ** 2 / 2 + spring * qsol**2 / 2
    add(
        "04.04",
        "谐振子能量守恒",
        {
            "on_shell_constant": _zero(
                sp.trigsimp(sp.diff(energy.subs(spring, mass * omega**2), t))
            )
        },
        ("omega^2=k/m", "解析谐振子解"),
        "Noether 定理的一般场论证明不由单一模型替代。",
    )
    tx, xy = sp.symbols("t x", real=True)
    alpha = sp.Function("alpha")(tx, xy)
    A0 = sp.Function("A0")(tx, xy)
    A1 = sp.Function("A1")(tx, xy)
    F01 = sp.diff(A1, tx) - sp.diff(A0, xy)
    transformed = sp.diff(A1 + sp.diff(alpha, xy), tx) - sp.diff(
        A0 + sp.diff(alpha, tx), xy
    )
    add(
        "04.05",
        "Abelian 场强反对称与规范不变",
        {
            "gauge_invariance": _zero(transformed - F01),
            "antisymmetry": _zero(
                (sp.diff(A0, xy) - sp.diff(A1, tx)) + F01
            ),
        },
        ("场与规范函数二阶连续，混合偏导可交换",),
        "非阿贝尔交换子项在 V07 单独验证。",
    )

    # V05 量子力学
    norm = (sp.pi * sigma**2) ** sp.Rational(-1, 4)
    psi = norm * sp.exp(-x**2 / (2 * sigma**2))
    add(
        "05.01",
        "高斯波函数归一化",
        {
            "normalization": _zero(
                sp.integrate(psi**2, (x, -sp.oo, sp.oo)) - 1
            )
        },
        ("sigma>0", "波函数取实高斯"),
        "有限盒子和离散积分需独立收敛检查。",
    )
    hbar = sp.symbols("hbar", positive=True, real=True)
    test_wave = x**4 - 2 * x + 3
    xp_wave = x * (-sp.I * hbar * sp.diff(test_wave, x))
    px_wave = -sp.I * hbar * sp.diff(x * test_wave, x)
    add(
        "05.02",
        "位置—动量对易子",
        {"commutator_on_test_space": _zero(xp_wave - px_wave - sp.I * hbar * test_wave)},
        ("以四次多项式代表可微测试函数", "p=-i hbar d/dx"),
        "无界算符的定义域问题需泛函分析；离散导数有边界残差。",
    )
    e1, e2 = sp.symbols("E1 E2", real=True)
    Ut = sp.diag(sp.exp(-sp.I * e1 * t / hbar), sp.exp(-sp.I * e2 * t / hbar))
    add(
        "05.03",
        "厄米二能级幺正演化",
        {"unitarity": _matrix_zero(sp.simplify(Ut.conjugate().T * Ut - sp.eye(2)))},
        ("E1,E2,t 为实数", "H 已在能量基对角化"),
        "时间依赖 Hamiltonian 需要时间有序指数。",
    )
    angle = sp.symbols("angle", real=True)
    probs = sp.cos(angle) ** 2 + sp.sin(angle) ** 2
    expectation = sp.cos(angle) ** 2 - sp.sin(angle) ** 2
    add(
        "05.04",
        "二能级 Born 概率与期望",
        {
            "probability_sum": _zero(probs - 1),
            "expectation": _zero(sp.trigsimp(expectation - sp.cos(2 * angle))),
        },
        ("态系数为实；一般复系数取模平方", "本征值为 +1,-1"),
        "Born 规则是量子理论公设，SymPy 只核对其代数后果。",
    )
    prob_density = psi**2
    x2 = sp.integrate(x**2 * prob_density, (x, -sp.oo, sp.oo))
    ppsi = -sp.I * hbar * sp.diff(psi, x)
    p2 = sp.integrate(sp.conjugate(ppsi) * ppsi, (x, -sp.oo, sp.oo))
    add(
        "05.05",
        "高斯最小不确定波包",
        {
            "x_variance": _zero(x2 - sigma**2 / 2),
            "p_variance": _zero(p2 - hbar**2 / (2 * sigma**2)),
            "saturation": _zero(sp.sqrt(x2 * p2) - hbar / 2),
        },
        ("sigma,hbar>0", "零均值、零平均动量实高斯"),
        "一般 Robertson 不确定关系的证明在课件正文；这里只验证饱和实例。",
    )

    # V06 量子场论
    px, py, pz = sp.symbols("p_x p_y p_z", real=True)
    plane = sp.exp(-sp.I * E * t + sp.I * (px * x + py * xy + pz * tx))
    kg = sp.diff(plane, t, 2) - (
        sp.diff(plane, x, 2)
        + sp.diff(plane, xy, 2)
        + sp.diff(plane, tx, 2)
    ) + m**2 * plane
    add(
        "06.01",
        "Klein--Gordon 平面波色散",
        {
            "dispersion_residual": _zero(
                sp.simplify(
                    kg.subs(E**2, px**2 + py**2 + pz**2 + m**2)
                )
            )
        },
        ("自然单位", "平面波坐标以三个独立实变量代表"),
        "自由场检查不证明相互作用 QCD 的谱。",
    )
    cutoff = 5
    annihilation = sp.zeros(cutoff)
    for idx in range(1, cutoff):
        annihilation[idx - 1, idx] = sp.sqrt(idx)
    creation = annihilation.T
    number = creation * annihilation
    number_comm = number * creation - creation * number
    inner_residual = number_comm - creation
    add(
        "06.02",
        "截断 Fock 空间的产生算符",
        {
            "inner_states": _matrix_zero(inner_residual[:, : cutoff - 1]),
            "number_spectrum": tuple(number.diagonal()) == tuple(range(cutoff)),
        },
        ("Fock 截断 n=0,...,4", "只在非最高截断态检查对易关系"),
        "有限维空间不可能在最高态满足完整 Heisenberg 代数；边界残差被显式排除。",
    )
    add_my(
        "06.03",
        "高斯生成泛函",
        "derive_generating_functional",
        "验证有限维高斯模型及源导数；一般相互作用路径积分不作形式评价。",
    )
    variance = sp.symbols("sigma2", positive=True)
    gauss_norm = 1 / sp.sqrt(2 * sp.pi * variance)
    moment2 = sp.integrate(
        x**2 * gauss_norm * sp.exp(-x**2 / (2 * variance)),
        (x, -sp.oo, sp.oo),
    )
    moment4 = sp.integrate(
        x**4 * gauss_norm * sp.exp(-x**2 / (2 * variance)),
        (x, -sp.oo, sp.oo),
    )
    add(
        "06.04",
        "零均值高斯四点 Wick 配对",
        {
            "second_moment": _zero(moment2 - variance),
            "fourth_moment": _zero(moment4 - 3 * moment2**2),
        },
        ("variance>0", "一维零均值高斯代理"),
        "多点自由场的三种配对结构由同一高斯定理给出；费米负号另需 Grassmann 代数。",
    )
    gap, ratio = sp.symbols("Delta r", positive=True)
    add(
        "06.05",
        "欧氏谱的基态投影",
        {
            "excited_suppression": _zero(
                sp.limit(ratio * sp.exp(-gap * t), t, sp.oo)
            )
        },
        ("能隙 Delta>0", "重叠比有限"),
        "若基态重叠为零或有限时间边界显著，主导态需重新判定。",
    )

    # V07 QCD
    add(
        "07.01",
        "质子与中子电荷计数",
        {
            "proton_charge": _zero(2 * sp.Rational(2, 3) - sp.Rational(1, 3) - 1),
            "neutron_charge": _zero(sp.Rational(2, 3) - 2 * sp.Rational(1, 3)),
        },
        ("夸克电荷单位取 |e|", "只做味量子数加法"),
        "颜色单态和强相互作用动力学不由电荷计数证明。",
    )
    add_my(
        "07.02",
        "SU(3) 生成元恒等式",
        "derive_su3_generator_identities",
        "用八个反厄米 Gell--Mann 生成元逐项验证李代数；约定转换在课件注明。",
    )
    coord = sp.symbols("s", real=True)
    psi_fun = sp.Function("psi")(coord)
    alpha_fun = sp.Function("alpha")(coord)
    gauge_fun = sp.Function("A")(coord)
    coupling = sp.symbols("g", nonzero=True, real=True)
    omega_fun = sp.exp(sp.I * alpha_fun)
    psi_prime = omega_fun * psi_fun
    gauge_prime = gauge_fun + sp.diff(alpha_fun, coord) / coupling
    cov_prime = sp.diff(psi_prime, coord) - sp.I * coupling * gauge_prime * psi_prime
    cov_original = sp.diff(psi_fun, coord) - sp.I * coupling * gauge_fun * psi_fun
    pauli1_703 = sp.Matrix([[0, 1], [1, 0]])
    theta_703 = sp.symbols("theta_703", real=True)
    omega_703 = sp.diag(
        sp.exp(sp.I * theta_703 * coord / 2),
        sp.exp(-sp.I * theta_703 * coord / 2),
    )
    psi_703 = sp.Matrix(
        [sp.Function("psi_1")(coord), sp.Function("psi_2")(coord)]
    )
    gauge_component_703 = sp.symbols("a_1", real=True)
    gauge_matrix_703 = gauge_component_703 * pauli1_703 / 2
    gauge_prime_703 = (
        omega_703 * gauge_matrix_703 * omega_703.conjugate().T
        - sp.I
        * sp.diff(omega_703, coord)
        * omega_703.conjugate().T
        / coupling
    )
    cov_prime_703 = (
        sp.diff(omega_703 * psi_703, coord)
        - sp.I * coupling * gauge_prime_703 * omega_703 * psi_703
    )
    cov_original_703 = (
        sp.diff(psi_703, coord)
        - sp.I * coupling * gauge_matrix_703 * psi_703
    )
    add(
        "07.03",
        "U(1) 与非对易 SU(2) 协变导数",
        {
            "U1_covariance": _zero(sp.expand(cov_prime - omega_fun * cov_original)),
            "SU2_covariance": _matrix_zero(
                sp.simplify(cov_prime_703 - omega_703 * cov_original_703)
            ),
        },
        (
            "D=d-igA、psi'=Omega psi、g 非零",
            "A'=Omega A Omega^dagger-(i/g)(d Omega)Omega^dagger",
            "SU(2) 代理中 Omega 沿 sigma3、A 沿不对易的 sigma1",
        ),
        "精确验证非阿贝尔矩阵次序和非齐次项符号；四维 SU(3) 离散实现仍需逐点测试。",
    )
    sigma1 = sp.Matrix([[0, 1], [1, 0]])
    sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma3 = sp.Matrix([[1, 0], [0, -1]])
    aval, bval, gval = sp.symbols("a b g", real=True)
    field1 = aval * sigma1 / 2
    field2 = bval * sigma2 / 2
    field_strength = -sp.I * gval * (field1 * field2 - field2 * field1)
    transformed_field_strength = (
        omega_703 * field_strength * omega_703.conjugate().T
    )
    qbar_entries = sp.symbols("qbar_1 qbar_2")
    dq_entries = sp.symbols("Dq_1 Dq_2")
    qbar_proxy = sp.Matrix([qbar_entries])
    dq_proxy = sp.Matrix(dq_entries)
    quark_bilinear = (qbar_proxy * dq_proxy)[0]
    transformed_quark_bilinear = (
        qbar_proxy
        * omega_703.conjugate().T
        * omega_703
        * dq_proxy
    )[0]
    add(
        "07.04",
        "非阿贝尔场强与 QCD 拉氏量不变量",
        {
            "commutator_term": _matrix_zero(
                sp.simplify(field_strength - gval * aval * bval * sigma3 / 2)
            ),
            "antisymmetry": _matrix_zero(
                field_strength
                + (-sp.I * gval * (field2 * field1 - field1 * field2))
            ),
            "gluon_trace_invariance": _zero(
                sp.simplify(
                    sp.trace(transformed_field_strength * transformed_field_strength)
                    - sp.trace(field_strength * field_strength)
                )
            ),
            "quark_bilinear_invariance": _zero(
                sp.simplify(transformed_quark_bilinear - quark_bilinear)
            ),
            "four_dimensional_mass_dimensions": (
                2 * 2 == 4 and 1 + sp.Rational(3, 2) + sp.Rational(3, 2) == 4
            ),
        },
        ("有限维 SU(2) 子群矩阵实例", "D=d-igA 约定", "四维自然单位"),
        "矩阵代理验证交换子、自旋无关颜色双线性与迹型胶子项的不变性；完整 SU(3) 味结构、旋量指标和量子反常仍需场论推导。",
    )
    u, beta0 = sp.symbols("u beta0", positive=True)
    alpha_s = 4 * sp.pi / (beta0 * u)
    add(
        "07.05",
        "一圈运行耦合方程",
        {
            "beta_equation": _zero(
                sp.diff(alpha_s, u) + beta0 * alpha_s**2 / (4 * sp.pi)
            ),
            "nf3": _zero((11 - sp.Rational(2, 3) * 3) - 9),
        },
        ("u=ln(mu^2/Lambda^2)>0", "一圈微扰"),
        "靠近 Lambda 的强耦合和禁闭不能由一圈公式证明。",
    )

    # V08 欧氏格点
    kk, NN = sp.symbols("k N", integer=True, positive=True)
    add(
        "08.01",
        "周期边界的动量量子化",
        {
            "periodic_phase": _zero(
                sp.expand_complex(sp.exp(2 * sp.pi * sp.I * kk)) - 1
            )
        },
        ("k,N 为整数", "p=2pi k/(Na), L=Na"),
        "有限格点还需识别 k 模 N 和 Brillouin 区。",
    )
    add_my(
        "08.02",
        "格点链接变量连续展开",
        "derive_lattice_link",
        "在可交换单色分量验证幺正性和 a^2 展开；非阿贝尔使用矩阵指数。",
    )
    ph = sp.symbols("alpha beta gamma delta", real=True)
    plaq = sp.prod(
        [
            sp.exp(sp.I * ph[0]),
            sp.exp(sp.I * ph[1]),
            sp.exp(-sp.I * ph[2]),
            sp.exp(-sp.I * ph[3]),
        ]
    )
    add(
        "08.03",
        "U(1) plaquette 的离散 curl",
        {
            "phase_sum": _zero(
                sp.simplify(
                    plaq
                    - sp.exp(sp.I * (ph[0] + ph[1] - ph[2] - ph[3]))
                )
            ),
            "reverse": _zero(
                sp.simplify(1 / plaq - sp.conjugate(plaq))
            ),
        },
        ("四个链接相位为实数",),
        "非阿贝尔 Baker--Campbell--Hausdorff 展开和路径基点另行验证。",
    )
    phi = sp.symbols("phi", real=True)
    action_piece = 1 - sp.cos(phi)
    add(
        "08.04",
        "Wilson plaquette 小场展开",
        {
            "quadratic_coefficient": _zero(
                sp.limit(action_piece / phi**2, phi, 0) - sp.Rational(1, 2)
            ),
            "nonnegative_proxy": bool(action_piece.subs(phi, sp.pi / 3) > 0),
        },
        ("U(1) 小相位代理",),
        "SU(3) 迹归一化和格点求和系数依赖生成元约定。",
    )
    avec, mass_gap = sp.symbols("a m_gap", positive=True)
    Linf = sp.symbols("Linf", positive=True)
    corr = sp.symbols("c_a c_L", real=True)
    finite_model = corr[0] * avec**2 + corr[1] * sp.exp(-mass_gap * Linf)
    add(
        "08.05",
        "连续与无限体积极限",
        {
            "joint_limit": _zero(
                sp.limit(
                    sp.limit(finite_model, avec, 0), Linf, sp.oo
                )
            )
        },
        ("mass gap>0", "O(a) 项已改进消去"),
        "具体系数、幂次和有限体积函数须由作用量、算符与数据决定。",
    )

    # V09 格点费米子
    paulis = (sigma1, sigma2, sigma3)
    clifford_checks: Dict[str, bool] = {}
    for i0 in range(2):
        for j0 in range(2):
            lhs = paulis[i0] * paulis[j0] + paulis[j0] * paulis[i0]
            rhs = 2 * (1 if i0 == j0 else 0) * sp.eye(2)
            clifford_checks[f"gamma_{i0+1}{j0+1}"] = _matrix_zero(lhs - rhs)
    add(
        "09.01",
        "Pauli 子代数的 Euclidean Clifford 关系",
        clifford_checks,
        ("以 gamma1=sigma1, gamma2=sigma2 作有限子代数",),
        "四维 gamma 表示和项目轴顺序由共享约定测试保证。",
    )
    ap = sp.symbols("ap", real=True)
    add(
        "09.02",
        "朴素费米子倍增零点",
        {
            "origin_zero": _zero(sp.sin(ap).subs(ap, 0)),
            "edge_zero": _zero(sp.sin(ap).subs(ap, sp.pi)),
            "continuum_slope": _zero(sp.limit(sp.sin(ap) / ap, ap, 0) - 1),
        },
        ("一维自由场动量符号",),
        "四维 16 重倍增由四方向笛卡尔组合得出。",
    )
    wilson_term = 1 - sp.cos(ap)
    add(
        "09.03",
        "Wilson 项的物理支与倍增支",
        {
            "physical_leading": _zero(
                sp.limit(wilson_term / ap**2, ap, 0) - sp.Rational(1, 2)
            ),
            "doubler_mass": _zero(wilson_term.subs(ap, sp.pi) - 2),
        },
        ("一维自由场、r=1",),
        "Wilson 项的手征破缺、临界质量和 Clover 改进需完整格点分析。",
    )
    Avec = sp.Matrix([[2, 1], [1, 2]])
    bvec = sp.Matrix([3, 0])
    sol = Avec.inv() * bvec
    add(
        "09.04",
        "传播子线性系统的小矩阵闭合",
        {
            "solution": _matrix_zero(sol - sp.Matrix([2, -1])),
            "residual": _matrix_zero(Avec * sol - bvec),
        },
        ("2x2 对称正定代理",),
        "巨大稀疏 Dirac 算符的条件数、预条件与浮点停止准则需数值测试。",
    )
    add_my(
        "09.05",
        "Jacobi 到 Gaussian 涂抹极限",
        "derive_quark_gaussian_smearing",
        "自由周期小格点验证 Laplacian 模、极限与投影；非阿贝尔协变性另测。",
    )

    # V10 Monte Carlo
    S0, S1 = sp.symbols("S0 S1", real=True)
    w0, w1 = sp.exp(-S0), sp.exp(-S1)
    p0, p1 = w0 / (w0 + w1), w1 / (w0 + w1)
    add(
        "10.01",
        "两态 Boltzmann 归一化",
        {
            "probability_sum": _zero(p0 + p1 - 1),
            "constant_observable": _zero(p0 + p1 - 1),
        },
        ("有限两态模型",),
        "Markov 链样本的无偏性还需平稳、遍历和热化条件。",
    )
    pi0, pi1, q01, q10 = sp.symbols("pi0 pi1 q01 q10", positive=True)
    r_mh = pi1 * q10 / (pi0 * q01)
    add(
        "10.02",
        "Metropolis--Hastings 两分支详细平衡",
        {
            "r_le_one_branch": _zero(pi0 * q01 * r_mh - pi1 * q10),
            "r_gt_one_reverse_branch": _zero(
                pi1 * q10 / r_mh - pi0 * q01
            ),
        },
        ("所有目标权重和提议概率为正", "分别验证 r<=1 与 r>1 的代数分支"),
        "遍历性和实际混合速度不由详细平衡单独保证。",
    )
    add_my(
        "10.03",
        "Markov 链自相关与有效样本数",
        "derive_mcmc_autocorrelation",
        "验证有限自回归代理的自相关和方差放大；真实链需窗口与误差分析。",
    )
    add_my(
        "10.04",
        "HMC 标量 leapfrog 与接受校正",
        "derive_hmc_scalar",
        "验证一维标量代理的可逆/保体积及 Hamiltonian 误差；SU(3) 力另测。",
    )
    Ns, Nt, lattice_a, mpi = sp.symbols("N_s N_t a m_pi", positive=True)
    spatial_extent = Ns * lattice_a
    temporal_extent = Nt * lattice_a
    add(
        "10.05",
        "系综物理尺寸与 m_pi L",
        {
            "spatial_extent": _zero(spatial_extent / lattice_a - Ns),
            "temporal_extent": _zero(temporal_extent / lattice_a - Nt),
            "dimensionless_product": _zero(
                (mpi / 2) * (2 * spatial_extent) - mpi * spatial_extent
            ),
        },
        ("各向同性格距", "m_pi 以逆长度单位表示"),
        "m_pi L 大于某经验值不构成有限体积误差证明。",
    )

    # V11 核子关联函数
    phase_a, phase_b = sp.symbols("alpha beta", real=True)
    color_u = sp.diag(
        sp.exp(sp.I * phase_a),
        sp.exp(sp.I * phase_b),
        sp.exp(-sp.I * (phase_a + phase_b)),
    )
    add(
        "11.01",
        "三夸克反对称颜色单态",
        {
            "su3_determinant": _zero(sp.simplify(color_u.det() - 1)),
            "epsilon_factor": _zero(
                sp.simplify(
                    color_u[0, 0] * color_u[1, 1] * color_u[2, 2] - 1
                )
            ),
        },
        ("以 SU(3) 对角子群显式检查 epsilon_123 分量",),
        "一般 SU(3) 结论依赖 epsilon U U U=det(U)epsilon；旋量/费米符号另测。",
    )
    amp0, amp1, energy0, delta_e = sp.symbols(
        "A0 A1 E0 Delta", positive=True
    )
    corr2 = amp0 * sp.exp(-energy0 * t) + amp1 * sp.exp(
        -(energy0 + delta_e) * t
    )
    relative_excited = corr2 / (amp0 * sp.exp(-energy0 * t)) - 1
    add(
        "11.02",
        "二点谱的基态投影",
        {
            "relative_pollution": _zero(
                sp.simplify(
                    relative_excited
                    - amp1 / amp0 * sp.exp(-delta_e * t)
                )
            ),
            "large_time": _zero(sp.limit(relative_excited, t, sp.oo)),
        },
        ("A0,A1,E0,Delta>0", "忽略有限 T 后向传播的双态代理"),
        "真实重叠可有投影与归一化因子；有限时间边界须加入拟合。",
    )
    single_c = amp0 * sp.exp(-energy0 * t)
    step = sp.symbols("a_t", positive=True)
    meff = sp.log(single_c / single_c.subs(t, t + step))
    add(
        "11.03",
        "单指数有效质量",
        {"am_eff": _zero(sp.expand_log(meff, force=True) - energy0 * step)},
        ("A0,E0,a_t>0", "纯单指数"),
        "多态、噪声导致的非正关联函数与后向项需相关拟合。",
    )
    tau, tsep = sp.symbols("tau t_sep", positive=True)
    coeff_a, coeff_b, matrix00 = sp.symbols("A B M00", finite=True)
    ratio3 = (
        matrix00
        + coeff_a * sp.exp(-delta_e * tau)
        + coeff_b * sp.exp(-delta_e * (tsep - tau))
    )
    symmetric_limit = ratio3.subs(tau, tsep / 2)
    energy11, projector_factor11, physical_matrix11 = sp.symbols(
        "E K_Pi M_phys", positive=True
    )
    ground_ratio11 = projector_factor11 * physical_matrix11 / (2 * energy11)
    add(
        "11.04",
        "三点中心插入的激发态抑制",
        {
            "center_form": _zero(
                sp.simplify(
                    symmetric_limit
                    - matrix00
                    - (coeff_a + coeff_b) * sp.exp(-delta_e * tsep / 2)
                )
            ),
            "large_separation": _zero(
                sp.limit(symmetric_limit - matrix00, tsep, sp.oo)
            ),
            "recover_2E_projector_normalization": _zero(
                2 * energy11 * ground_ratio11 / projector_factor11
                - physical_matrix11
            ),
        },
        ("Delta>0", "双态领先污染", "中心插入 tau=tsep/2", "K_Pi 非零且外态采用相对论 2E 归一化"),
        "A、B 的关系取决于算符与运动学，未强制对称；实际 K_Pi 来自 Euclidean 自旋和与目标 Lorentz 投影，不能由标量代理猜测。",
    )
    cvals = sp.symbols("c0:3", real=True)
    ovals = sp.symbols("o0:3", real=True)
    cmean = sum(cvals) / 3
    omean = sum(ovals) / 3
    cov_biased = sum(cvals[i] * ovals[i] for i in range(3)) / 3 - cmean * omean
    cov_unbiased = sum(
        (cvals[i] - cmean) * (ovals[i] - omean) for i in range(3)
    ) / 2
    shift_c = sp.symbols("shift", real=True)
    shifted_cov_unbiased = sum(
        (cvals[i] - cmean) * (ovals[i] + shift_c - (omean + shift_c))
        for i in range(3)
    ) / 2
    add(
        "11.05",
        "断连真空扣除的有限样本协方差结构",
        {
            "N_over_Nminus1_correction": _zero(
                sp.expand(cov_unbiased - sp.Rational(3, 2) * cov_biased)
            ),
            "constant_shift": _zero(
                sp.expand(shifted_cov_unbiased - cov_unbiased)
            ),
            "single_configuration_zero": _zero(cvals[0] * ovals[0] - cvals[0] * ovals[0]),
        },
        ("三个独立等权块作一般符号样本", "无偏形式采用 1/(N-1)"),
        "验证 1/N 均值差式须乘 N/(N-1)；非零物理信号需要真实系综配对，N<2 必须由接口拒绝。",
    )

    # V12 统计与拟合
    avecs = sp.symbols("a0:4", real=True)
    bvecs = sp.symbols("b0:4", real=True)
    amean = sum(avecs) / 4
    bmean = sum(bvecs) / 4
    cov_centered = sum(
        (avecs[i] - amean) * (bvecs[i] - bmean) for i in range(4)
    ) / 4
    cov_raw = sum(avecs[i] * bvecs[i] for i in range(4)) / 4 - amean * bmean
    add(
        "12.01",
        "协方差的中心与原始矩形式",
        {"identity": _zero(sp.expand(cov_centered - cov_raw))},
        ("四个等权实样本", "使用 1/N 总体矩定义"),
        "无偏样本协方差改用 1/(N-1)；自相关需块处理。",
    )
    jvals = sp.symbols("x0:3", real=True)
    jmean = sum(jvals) / 3
    leaves = tuple((sum(jvals) - val) / 2 for val in jvals)
    leave_mean = sum(leaves) / 3
    jk_var = sp.Rational(2, 3) * sum((val - leave_mean) ** 2 for val in leaves)
    sample_var_over_n = (
        sum((val - jmean) ** 2 for val in jvals) / 2 / 3
    )
    add(
        "12.02",
        "样本均值的删除一 jackknife 方差",
        {
            "leave_mean": _zero(sp.expand(leave_mean - jmean)),
            "variance": _zero(sp.expand(jk_var - sample_var_over_n)),
        },
        ("N=3 的一般符号样本", "目标估计量为线性样本均值"),
        "非线性估计量关系只在大样本下一阶成立；课程算法仍重跑完整链。",
    )
    bu, bv = sp.symbols("u v", real=True)
    boot_means = (bu, (bu + bv) / 2, (bv + bu) / 2, bv)
    boot_center = sum(boot_means) / 4
    boot_var = sum((qv - boot_center) ** 2 for qv in boot_means) / 4
    empirical_var = ((bu - (bu + bv) / 2) ** 2 + (bv - (bu + bv) / 2) ** 2) / 2
    add(
        "12.03",
        "N=2 bootstrap 均值的精确枚举",
        {
            "conditional_mean": _zero(boot_center - (bu + bv) / 2),
            "conditional_variance": _zero(
                sp.expand(boot_var - empirical_var / 2)
            ),
        },
        ("枚举两个样本的 2^2 个有序有放回重样本",),
        "真实分析的块 bootstrap 和分位数覆盖需重复模拟验证。",
    )
    add_my(
        "12.04",
        "相关 chi-square 与 nuisance profile",
        "derive_correlated_chi_square_profile",
        "在有限维精确模型验证驻点、Woodbury 形式和 profile；协方差估计误差另测。",
    )
    gaps = sp.symbols("d1:4", real=True)
    energies = [energy0]
    for gv in gaps:
        energies.append(energies[-1] + sp.exp(gv))
    add(
        "12.05",
        "正能隙参数化",
        {
            "gap_1": _zero(energies[1] - energies[0] - sp.exp(gaps[0])),
            "gap_2": _zero(energies[2] - energies[1] - sp.exp(gaps[1])),
            "gap_3": _zero(energies[3] - energies[2] - sp.exp(gaps[2])),
        },
        ("delta_j 为实数，因此 exp(delta_j)>0",),
        "参数有序不保证多态模型可由有限数据辨识。",
    )

    # V13 部分子分布
    Pdotq, Q2, xbj = sp.symbols("Pq Q2 x", positive=True)
    final_virtuality = 2 * xbj * Pdotq - Q2
    x_solution = sp.solve(sp.Eq(final_virtuality, 0), xbj)[0]
    add(
        "13.01",
        "质量可忽略部分子的 Bjorken x",
        {"solution": _zero(x_solution - Q2 / (2 * Pdotq))},
        ("p=xP 且 p^2 近似 0", "(p+q)^2=0", "Q^2=-q^2>0"),
        "靶质量、高 twist 和有限 Q^2 修正未由该运动学代理涵盖。",
    )
    nu = sp.symbols("nu", real=True, nonzero=True)
    direct_itd = sp.integrate(sp.exp(sp.I * x * nu) / 2, (x, -1, 1))
    add(
        "13.02",
        "有限支持均匀分布的 Ioffe-time 变换",
        {
            "fourier_pair": _zero(
                sp.simplify(
                    sp.expand_complex(direct_itd) - sp.sin(nu) / nu
                )
            ),
            "normalization_limit": _zero(
                sp.limit(sp.sin(nu) / nu, nu, 0) - 1
            ),
        },
        ("以 [-1,1] 上 q(x)=1/2 作规范化代理",),
        "光锥算符定义、Wilson 线和重整化由物理理论给出，非此积分证明。",
    )
    moment_proxy13 = my_derivations.derive_pdf_moment_relations()
    xmoment13 = sp.symbols("x_moment", nonnegative=True)
    gluon_model13 = 2 * xmoment13
    add(
        "13.03",
        "PDF Mellin 矩与局域算符系数",
        {
            **moment_proxy13.checks,
            "lowest_unpolarized_gluon_twist2_moment": _zero(
                sp.integrate(xmoment13 * gluon_model13, (xmoment13, 0, 1))
                - sp.Rational(2, 3)
            ),
        },
        (*moment_proxy13.assumptions, "非极化规范不变胶子 twist-2 塔从 n=2 开始，对应 int dx x g(x)"),
        "有限代理验证矩关系和最低胶子动量矩；不存在由本记录支持的 n=1 规范不变胶子数算符，真实 mixing/renormalization 另验。",
    )
    add_my(
        "13.04",
        "Mellin 卷积代数",
        "derive_mellin_convolution",
        "验证可积测试函数的卷积和矩性质；DGLAP plus 分布与截断阶另有边界。",
    )
    add_my(
        "13.05",
        "二维 TMD Fourier 归一化",
        "derive_tmd_fourier",
        "验证高斯/有限维代理的 bT--kT Fourier 关系；soft 与 rapidity 结构不由 Fourier 代数消除。",
    )

    # V14 LaMET 与 CS
    add_my(
        "14.01",
        "quasi/pseudo Fourier 反演",
        "derive_qpdf_ppdf_fourier_inversion",
        "验证受控测试函数的正反变换；有限 z 重建的病态性需数值覆盖测试。",
    )
    add_my(
        "14.02",
        "LaMET 匹配与幂计数",
        "derive_lamet_matching",
        "验证代理核的卷积、尺度和极限；修正系数一般依 x、bT、ell，且小 x/端点展开可能非一致，QCD 因子化定理本身不是 SymPy 结论。",
    )
    mix = sp.Matrix([[2, 1], [1, 3]])
    parton_vector = sp.Matrix([1, 2])
    add(
        "14.03",
        "两通道胶子—singlet 线性混合代理",
        {
            "forward": _matrix_zero(mix * parton_vector - sp.Matrix([4, 7])),
            "inverse": _matrix_zero(mix.inv() * (mix * parton_vector) - parton_vector),
        },
        ("用常数 2x2 矩阵代理每个矩阵元的 x 卷积", "det C 非零"),
        "真实匹配核含分布、尺度和卷积；这里只检查通道线性代数。",
    )
    add_my(
        "14.04",
        "pseudo-ITD Fourier 关系",
        "derive_pseudo_itd",
        "验证有限测试分布的 Ioffe-time 变换和归一化；短距因子化域另判。",
    )
    cs_proxy14 = my_derivations.derive_collins_soper_evolution()
    add(
        "14.05",
        "Collins--Soper 演化积分",
        cs_proxy14.checks,
        (
            *cs_proxy14.assumptions,
            "x 空间比较固定共同 x；坐标空间比较固定共同 Ioffe time nu=zP_z",
            "生产提取至少三个有效 P_z，以同时约束 K 与有限动量幂修正",
        ),
        "只验证固定 bT 的演化积分；相同 z、不同 P_z 不满足共同 nu，两点比值也不能辨认 K 与 1/P_z^2 污染。",
    )

    # V15 胶子 TMD 算符
    r1, r2, r3, r4 = sp.symbols("r1 r2 r3 r4", real=True)
    qmat = sp.Matrix(
        [[r1 + sp.I * r2, r3 + sp.I * r4], [-r3 + sp.I * r4, r1 - sp.I * r2]]
    )
    anti = qmat - qmat.conjugate().T
    fproxy = anti / sp.I
    ftr = fproxy - sp.trace(fproxy) * sp.eye(2) / 2
    add(
        "15.01",
        "clover 反厄米无迹投影代理",
        {
            "hermitian": _matrix_zero(sp.simplify(ftr.conjugate().T - ftr)),
            "traceless": _zero(sp.trace(ftr)),
        },
        ("2x2 显式复矩阵代理", "场强约定含 1/i"),
        "clover 的 8ga^2 系数和 O(a^2) 改进需小场格点展开验证。",
    )
    Ua = sp.diag(sp.exp(sp.I * phase_a), sp.exp(-sp.I * phase_a))
    Ub = sp.diag(sp.exp(sp.I * phase_b), sp.exp(-sp.I * phase_b))
    Wb0 = sp.Matrix([[1, 2], [3, 5]])
    W0b = sp.Matrix([[2, -1], [1, 1]])
    Fb = sigma1
    F0 = sigma2
    original_trace = sp.trace(Fb * Wb0 * F0 * W0b)
    transformed_trace = sp.trace(
        (Ub * Fb * Ub.conjugate().T)
        * (Ub * Wb0 * Ua.conjugate().T)
        * (Ua * F0 * Ua.conjugate().T)
        * (Ua * W0b * Ub.conjugate().T)
    )
    add(
        "15.02",
        "双场强闭合颜色迹的端点规范不变",
        {"endpoint_cancellation": _zero(sp.simplify(transformed_trace - original_trace))},
        ("SU(2) 对角局域变换显式代理", "两条 Wilson 线按两个端点协变", "目标过程类固定为 past-pointing [-,-]"),
        "一般 SU(3) 由相同矩阵消去和迹循环性证明；代数不区分 [-,-] 与其他 link class，过程标签和路径几何必须另测。",
    )
    ell, zlong, bx, by = sp.symbols("ell z b_x b_y", real=True)
    leg1 = sp.Matrix([0, 0, -ell])
    bridge = sp.Matrix([bx, by, 0])
    leg2 = sp.Matrix([0, 0, zlong + ell])
    add(
        "15.03",
        "三段 staple 的端点位移",
        {
            "endpoint": _matrix_zero(
                leg1 + bridge + leg2 - sp.Matrix([bx, by, zlong])
            ),
            "transverse": _zero(bridge.dot(sp.Matrix([0, 0, 1]))),
            "z_zero_b_nonzero_remains_bilocal": _matrix_zero(
                (leg1 + bridge + leg2).subs(zlong, 0) - sp.Matrix([bx, by, 0])
            ),
            "true_local_path_collapse": _matrix_zero(
                leg1.subs(ell, 0)
                + bridge.subs({bx: 0, by: 0})
                + leg2.subs({ell: 0, zlong: 0})
            ),
        },
        ("z 方向取第三轴", "bT 位于前两轴", "第一长腿沿 -z，代表主目标 [-,-] 的有限 quasi 代理"),
        "端点代数验证 z=0,bT!=0 仍双局域；真正局域还要求 ell=0 和 Wilson 路径收缩，非零守卫与周期边界由实现检查。",
    )
    T11, T12, T21, T22 = sp.symbols("T11 T12 T21 T22", real=True)
    tensor2 = sp.Matrix([[T11, T12], [T21, T22]])
    epsilon_t = sp.Matrix([[0, 1], [-1, 0]])
    symmetric_part = (tensor2 + tensor2.T) / 2
    antisymmetric_part = (tensor2 - tensor2.T) / 2
    trace_part = sp.trace(symmetric_part) * sp.eye(2) / 2
    traceless_part = symmetric_part - trace_part
    helicity_coefficient = sum(
        epsilon_t[i, j] * tensor2[i, j] for i in range(2) for j in range(2)
    ) / 2
    add(
        "15.04",
        "二维横向张量的非极化、螺旋度与线偏振分解",
        {
            "projector_trace": _zero(sp.trace(sp.eye(2)) - 2),
            "traceless": _zero(sp.trace(traceless_part)),
            "helicity_projection": _matrix_zero(
                antisymmetric_part - helicity_coefficient * epsilon_t
            ),
            "reconstruction": _matrix_zero(
                trace_part + traceless_part + antisymmetric_part - tensor2
            ),
        },
        ("二维 Euclidean 横向平面", "epsilon_T^{12}=+1", "张量元取实符号代理"),
        "这里只验证横向张量代数；light-front 指标、i 因子、核子自旋和 f1g[-,-] 归一化必须由选定算符约定固定。",
    )
    Zmix = sp.Matrix([[2, 0], [1, 1]])
    bare = sp.Matrix([3, 4])
    ren = Zmix * bare
    add(
        "15.05",
        "算符混合矩阵的正反映射",
        {
            "forward": _matrix_zero(ren - sp.Matrix([6, 7])),
            "inverse": _matrix_zero(Zmix.inv() * ren - bare),
            "nonsingular": _zero(Zmix.det() - 2),
        },
        ("两算符有限维代理",),
        "真实 Z 是尺度、方案和几何相关的卷积/混合对象。",
    )

    # V16 梯度流
    add_my(
        "16.01",
        "四维热核与半群",
        "derive_heat_kernel_semigroup",
        "验证归一化、卷积半群和扩散宽度代理；有限周期盒边界另测。",
    )
    add_my(
        "16.02",
        "Wilson 格点流的作用量单调性",
        "derive_wilson_lattice_flow_monotonicity",
        "在显式格点代理验证梯度平方结构；生产积分器还需步长收敛。",
    )
    flow_r, spacing, distance = sp.symbols("r_flow a d", positive=True)
    ratio_uv = flow_r / spacing
    ratio_phys = flow_r / distance
    scale_factor = sp.symbols("lambda", positive=True)
    add(
        "16.03",
        "流时窗口的无量纲尺度比",
        {
            "unit_invariance_uv": _zero(
                ratio_uv.subs(
                    {flow_r: scale_factor * flow_r, spacing: scale_factor * spacing}
                )
                - ratio_uv
            ),
            "unit_invariance_physical": _zero(
                ratio_phys.subs(
                    {flow_r: scale_factor * flow_r, distance: scale_factor * distance}
                )
                - ratio_phys
            ),
            "radius_definition": _zero(
                sp.sqrt(8 * (flow_r**2 / 8)) - flow_r
            ),
        },
        ("所有长度为正", "r_flow=sqrt(8 tau)"),
        "不等式是否有重叠窗口取决于实际 a、几何和数据稳定性。",
    )
    add_my(
        "16.04",
        "flowed 传播子的热核抑制",
        "derive_flowed_propagators",
        "验证微扰线性化传播子的指数抑制；rapidity subtraction 明确不在该检查中。",
    )
    tau_sfte, lambda_sfte, path_length = sp.symbols(
        "tau Lambda L_path", positive=True
    )
    local_target, local_coeff = sp.symbols("O_R c_tau", finite=True)
    local_sfte = local_target + local_coeff * tau_sfte * lambda_sfte**2
    flow_radius_sfte = sp.sqrt(8 * tau_sfte)
    perimeter_ratio = path_length / flow_radius_sfte
    add(
        "16.05",
        "局域小流时展开与非局域路径边界",
        {
            "local_limit": _zero(sp.limit(local_sfte, tau_sfte, 0) - local_target),
            "local_power_is_dimensionless": _zero(
                sp.diff(tau_sfte * lambda_sfte**2, tau_sfte)
                - lambda_sfte**2
            ),
            "finite_path_nonanalytic": (
                sp.limit(perimeter_ratio, tau_sfte, 0, dir="+") is sp.oo
            ),
            "log_flow_nonanalytic": (
                sp.limit(-sp.log(tau_sfte * lambda_sfte**2), tau_sfte, 0, dir="+")
                is sp.oo
            ),
        },
        (
            "tau,Lambda,L_path>0",
            "局域代理只保留 O(tau Lambda^2)",
            "finite-staple 的路径长度在 tau->0 时固定非零",
        ),
        "局域常数加 tau 模型不能验证非局域 TMD 的 flow-to-standard 转换；后者必须给出依赖 z、bT、ell、端点、cusp、mixing 与方案的 C_Gamma 核，否则保持 finite-flow prototype。",
    )

    # V17 实际测量链
    tau1, tau2, psq = sp.symbols("tau1 tau2 p2", positive=True)
    add(
        "17.01",
        "流轨迹检查点的半群复用",
        {
            "semigroup_mode": _zero(
                sp.exp(-tau2 * psq) * sp.exp(-tau1 * psq)
                - sp.exp(-(tau1 + tau2) * psq)
            ),
            "initial_condition": _zero(sp.exp(-tau1 * psq).subs(tau1, 0) - 1),
        },
        ("线性化单动量模", "tau1,tau2,p2>0"),
        "非线性群值 Wilson 流由数值积分器回归测试，不由单模代理替代。",
    )
    dims = sp.symbols("N_tau N_z N_b N_l N_proj N_orient", positive=True, integer=True)
    product_dims = sp.prod(dims)
    sample_subs = dict(zip(dims, (3, 7, 4, 5, 2, 2)))
    add(
        "17.02",
        "算符几何网格计数",
        {
            "sample_count": _zero(product_dims.subs(sample_subs) - 1680),
            "factorization": _zero(product_dims - sp.Mul(*dims)),
        },
        ("各轴为正整数", "朴素笛卡尔积、尚未对称约化"),
        "路径缓存可减计算量但不能改变逻辑数据项数。",
    )
    MN, Pz = sp.symbols("M_N P_z", positive=True)
    EN = sp.sqrt(MN**2 + Pz**2)
    add(
        "17.03",
        "boost 核子连续色散",
        {
            "mass_shell": _zero(EN**2 - MN**2 - Pz**2),
            "rest_limit": _zero(EN.subs(Pz, 0) - MN),
        },
        ("M_N>0", "取正能支"),
        "有限 a 的格点色散和信噪比须由多动量数据检查。",
    )
    cv = sp.symbols("c0:4", real=True)
    ov = sp.symbols("o0:4", real=True)
    sample_size = sp.Integer(4)
    cbar = sum(cv) / sample_size
    obar = sum(ov) / sample_size
    biased_covariance = (
        sum(cv[i] * ov[i] for i in range(sample_size)) / sample_size
        - cbar * obar
    )
    unbiased_covariance = sum(
        (cv[i] - cbar) * (ov[i] - obar) for i in range(sample_size)
    ) / (sample_size - 1)
    unbiased_from_means = sample_size * biased_covariance / (sample_size - 1)
    cshift = sp.symbols("c_shift", real=True)
    shifted_obar = obar + cshift
    shifted_unbiased = sum(
        (cv[i] - cbar) * (ov[i] + cshift - shifted_obar)
        for i in range(sample_size)
    ) / (sample_size - 1)
    covariance_count = sp.symbols("N_cov", integer=True, positive=True)
    add(
        "17.04",
        "构型级无偏断连协方差",
        {
            "centered_equals_corrected_means": _zero(
                sp.expand(unbiased_covariance - unbiased_from_means)
            ),
            "constant_shift": _zero(
                sp.expand(shifted_unbiased - unbiased_covariance)
            ),
            "N1_denominator_guard": _zero(
                (covariance_count - 1).subs(covariance_count, 1)
            ),
        },
        ("N=4 个独立块作为一般符号实例", "C2 与 O 使用相同索引配对", "生产接口要求 N>=2"),
        "SymPy 验证 1/(N-1) 中心化形式与 N/(N-1) 均值差式等价；N<2 必须由接口显式失败，构型错配仍需故障注入测试。",
    )
    nsep = sp.symbols("N", integer=True, positive=True)
    qexp = sp.symbols("q", positive=True)
    idx = sp.symbols("j", integer=True)
    M00, caa, cbb = sp.symbols("M00 A B")
    finite_sep = 6
    summed = sp.summation(
        M00 + caa * qexp**idx + cbb * qexp ** (finite_sep - idx),
        (idx, 1, finite_sep - 1),
    )
    closed_sum = (
        (finite_sep - 1) * M00
        + (caa + cbb)
        * qexp
        * (1 - qexp ** (finite_sep - 1))
        / (1 - qexp)
    )
    add(
        "17.05",
        "双态领先项的 summation 几何级数",
        {
            "closed_form_n6": _zero(
                sp.cancel((summed - closed_sum) * (1 - qexp))
            ),
            "constant_slope": _zero(
                ((nsep - 1) * M00).subs(nsep, nsep + 1)
                - (nsep - 1) * M00
                - M00
            ),
        },
        ("N>=2", "q=exp(-Delta E) 且 q!=1", "接触剔除取一格作代表"),
        "真实多态、相关噪声和有限 T 需共享 C2 参数的联合拟合。",
    )

    # V18 重整化与匹配
    add_my(
        "18.01",
        "Wilson 线线性反项指数化",
        "derive_wilson_line_linear_counterterm",
        "验证长度可加自能的指数形式；端点、cusp、flow-time 与方案依赖另列。",
    )
    soft_s, beam1, beam2, conversion_qs, zuv_mix = sp.symbols(
        "S_qsoft B1 B2 C_qsoft_to_S Z_UV_mix", positive=True
    )
    sub1 = conversion_qs * zuv_mix * beam1 / sp.sqrt(soft_s)
    sub2 = conversion_qs * zuv_mix * beam2 / sp.sqrt(soft_s)
    add(
        "18.02",
        "已声明方案中的对称 quasi-soft 平方根分配",
        {
            "two_beams": _zero(
                sub1 * sub2
                - conversion_qs**2 * zuv_mix**2 * beam1 * beam2 / soft_s
            ),
            "unit_factors": _zero(
                sub1.subs({soft_s: 1, conversion_qs: 1, zuv_mix: 1}) - beam1
            ),
        },
        (
            "固定 f1g[-,-] link class、Wilson 方向 v 与 vbar",
            "固定 rapidity regulator rho、zero-bin 和目标方案 S",
            "S_qsoft>0 的实正代理；复值情形需连续平方根分支",
        ),
        "只核对特定对称约定的代数。任意 Euclidean 真空 staple 不自动是标准 soft；缺 C_qsoft_to_S、方向、regulator 或 zero-bin 时必须保持 prototype。",
    )
    add_my(
        "18.03",
        "比值型非微扰重整化",
        "derive_ri_mom_ratio_renormalization",
        "验证共同乘法因子的消去与参考条件；参考态 IR 系统学不自动消失。",
    )
    z18, zs18, dm18 = sp.symbols("z z_s delta_m", positive=True)
    hs18, hl18 = sp.symbols("h_S h_L", nonzero=True)
    amplitude18 = hs18 / hl18
    straight_long18 = amplitude18 * sp.exp(dm18 * (z18 - zs18)) * hl18
    add(
        "18.04",
        "直线算符的 hybrid 重整化连续拼接",
        {
            "value_continuity": _zero(straight_long18.subs(z18, zs18) - hs18),
            "counterterm_at_switch": _zero(
                sp.exp(dm18 * (z18 - zs18)).subs(z18, zs18) - 1
            ),
            "normalization_ratio": _zero(amplitude18 * hl18 - hs18),
        },
        ("z,z_s>0 表示直线 Wilson 线的 |z|、|z_s|", "h_L 非零", "只要求拼接点函数值连续"),
        "该检查严格限定为 straight-line hybrid。finite-staple 必须以完整路径周长差 L_Gamma-L_Gamma,s 重新推导，并另处理端点、cusp 与 mixing；不得由本记录升级为已重整化 TMD。",
    )
    cs_proxy = my_derivations.derive_quasi_tmd_matching_and_cs_kernel()
    add(
        "18.05",
        "quasi-TMD 匹配与 CS 核",
        cs_proxy.checks,
        (
            *cs_proxy.assumptions,
            "CS 比较须位于共同 x，或坐标空间插值到共同 Ioffe time nu=zP_z",
            "生产提取至少使用三个有效 P_z 以区分 K 与 1/P_z^2 幂修正",
        ),
        "底层有限模型只验证 leading-power 两点比值代数，不是生产充分条件；完整 f1g[-,-] 胶子-singlet 匹配、共同运动学、三动量联合拟合与真实数据闭合仍须另验。",
    )

    # V19 联合极限
    c2, c4 = sp.symbols("c2 c4", real=True)
    cont_model = sp.symbols("F0") + c2 * avec**2 + c4 * avec**4
    add(
        "19.01",
        "a^2 连续外推截距",
        {"continuum_limit": _zero(sp.limit(cont_model, avec, 0) - sp.symbols("F0"))},
        ("a>0", "领先 O(a) 项已消去"),
        "实际幂次、尺度相关和 a^2/tau 交叉项由作用量与数据决定。",
    )
    pinf = sp.symbols("P", positive=True)
    x19, btrans19, ell19 = sp.symbols("x b_T ell", positive=True)
    Finf_fun = sp.Function("F_inf")
    d2_fun = sp.Function("d_2")
    d4_fun = sp.Function("d_4")
    Finf = Finf_fun(x19, btrans19)
    d2 = d2_fun(x19, btrans19, ell19)
    d4 = d4_fun(x19, btrans19, ell19)
    momentum_model = Finf + d2 / pinf**2 + d4 / pinf**4
    add(
        "19.02",
        "大动量倒幂外推",
        {
            "infinite_momentum": _zero(
                sp.limit(momentum_model, pinf, sp.oo) - Finf
            ),
            "evenness": _zero(momentum_model.subs(pinf, -pinf) - momentum_model),
        },
        ("固定 x、b_T、ell 与重整化/rapidity 方案", "P_z 非零", "所选标量通道在 P_z 反号下为偶"),
        "匹配对数须先统一；d_n 一般依赖 x、b_T、ell，且小 x 与端点的倒幂展开可能非一致；(aP)^2 与 1/P^2 需交叉数据区分。",
    )
    tau_flow, ca, ctau, ca2, Lam = sp.symbols(
        "tau a_coeff t_coeff a2_coeff Lambda", positive=True
    )
    local_flow_model = (
        Finf
        + ctau * tau_flow * Lam**2
        + ca * avec**2 / tau_flow
        + ca2 * (avec * Lam) ** 2
    )
    continuum_then_flow = sp.limit(
        sp.limit(local_flow_model, avec, 0), tau_flow, 0
    )
    nonlocal_path = sp.symbols("L_Gamma", positive=True) / sp.sqrt(8 * tau_flow)
    add(
        "19.03",
        "连续后零流时的有序极限",
        {
            "safe_order": _zero(continuum_then_flow - Finf),
            "fixed_a_divergence": (
                sp.limit(avec**2 / tau_flow, tau_flow, 0) is sp.oo
            ),
            "finite_staple_path_divergence": (
                sp.limit(nonlocal_path, tau_flow, 0, dir="+") is sp.oo
            ),
        },
        ("局域模型的系数和 Lambda 有限正", "先 a->0 后 tau->0", "finite-staple 路径在流时极限中保持非零"),
        "safe_order 只属于局域或已完成 C_Gamma 转换的对象；未消去 L_Gamma/sqrt(8tau)、ln tau、cusp 与 mixing 时，非局域 TMD 必须触发停止门。",
    )
    Delta, length, Acorr = sp.symbols("Delta ell A", positive=True)
    length_model = Finf + Acorr * sp.exp(-Delta * length)
    vlong, vtrans = sp.symbols("v_parallel v_perp", real=True)
    displacement = length * sp.Matrix([vlong, vtrans])
    tangent = displacement / length
    add(
        "19.04",
        "有限 staple 指数饱和",
        {
            "infinite_length": _zero(
                sp.limit(length_model, length, sp.oo) - Finf
            ),
            "two_length_ratio": _zero(
                sp.simplify(
                    (length_model.subs(length, length + 2) - Finf)
                    / (length_model - Finf)
                    - sp.exp(-2 * Delta)
                )
            ),
            "tangent_independent_of_length": _matrix_zero(
                sp.diff(tangent, length)
            ),
        },
        ("Delta>0", "单能隙指数模型", "Wilson 线切向量 v 固定，ell 只缩放位移"),
        "增大 ell 只测试有限长度饱和，不会把空间型方向变为光状或替代 rapidity 方案；幂尾、周期镜像和 soft 几何效应必须与替代模型比较。",
    )
    sig1, sig2, rho = sp.symbols("sigma1 sigma2 rho", real=True)
    covariance_matrix = sp.Matrix(
        [[sig1**2, rho * sig1 * sig2], [rho * sig1 * sig2, sig2**2]]
    )
    ones = sp.Matrix([1, 1])
    total_var = (ones.T * covariance_matrix * ones)[0]
    add(
        "19.05",
        "相关误差来源的总方差",
        {
            "quadratic_form": _zero(
                total_var
                - sig1**2
                - sig2**2
                - 2 * rho * sig1 * sig2
            ),
            "independent_limit": _zero(
                total_var.subs(rho, 0) - sig1**2 - sig2**2
            ),
        },
        ("两来源代理", "|rho|<=1 时协方差半正定"),
        "系统变体间相关性须由联合重采样或明确模型估计。",
    )

    # V20 自主实现
    axis_lengths = sp.symbols(
        "Ncfg Ntau NP Nz Nb Nell Ntins Nproj", positive=True, integer=True
    )
    logical_elements = sp.prod(axis_lengths)
    add(
        "20.01",
        "命名轴笛卡尔积的元素数",
        {
            "example_count": _zero(
                logical_elements.subs(
                    dict(zip(axis_lengths, (100, 2, 2, 2, 2, 2, 2, 2)))
                )
                - 12800
            )
        },
        ("所有逻辑轴长度为正整数",),
        "分块、压缩和稀疏布局只改变物理存储，不改变逻辑契约。",
    )
    Hin, Hcfg, Hcode, Hstage, Hcfg2 = sp.symbols(
        "H_inputs H_config H_code H_stage H_config_changed"
    )
    SHA = sp.Function("SHA256")
    digest = SHA(Hin, Hcfg, Hcode, Hstage)
    add(
        "20.02",
        "内容寻址依赖的符号结构",
        {
            "deterministic_expression": digest == SHA(Hin, Hcfg, Hcode, Hstage),
            "config_dependency": digest != SHA(Hin, Hcfg2, Hcode, Hstage),
        },
        ("把 SHA256 视为四元输入的确定性构造函数",),
        "碰撞抗性是密码学性质，不由 SymPy 证明；实际实现还需规范化字节编码和原子写入。",
    )
    coverage_exact = sp.erf(sp.sqrt(2))
    add(
        "20.03",
        "标准正态两倍标准差覆盖率",
        {
            "cdf_identity": _zero(
                (
                    sp.Rational(1, 2)
                    * (1 + sp.erf(2 / sp.sqrt(2)))
                    - sp.Rational(1, 2)
                    * (1 + sp.erf(-2 / sp.sqrt(2)))
                )
                - coverage_exact
            ),
            "numeric_range": 0.9544 < float(coverage_exact.evalf()) < 0.9546,
        },
        ("pull 服从标准正态的理想校准模型",),
        "真实覆盖率必须由重复合成实验测量，单次 |pull|<2 不证明正确。",
    )
    serial_fraction, procs = sp.symbols("f p", positive=True)
    speedup = 1 / (serial_fraction + (1 - serial_fraction) / procs)
    add(
        "20.04",
        "Amdahl 强标度",
        {
            "one_process": _zero(speedup.subs(procs, 1) - 1),
            "asymptotic_bound": _zero(
                sp.limit(speedup, procs, sp.oo) - 1 / serial_fraction
            ),
            "example": abs(
                float(speedup.subs({serial_fraction: sp.Rational(1, 20), procs: 16}))
                - 9.142857142857142
            )
            < 1e-12,
        },
        ("0<f<=1", "并行部分理想均分且忽略额外通信开销"),
        "真实性能必须 profile；模型不是 PyQCD 实测。",
    )
    joint_a, joint_p, joint_tau, joint_l = sp.symbols(
        "a P tau ell", positive=True
    )
    target = sp.symbols("F_target")
    joint_model = (
        target
        + joint_a**2
        + 1 / joint_p**2
        + joint_tau
        + sp.exp(-joint_l)
    )
    joint_limit = sp.limit(
        sp.limit(
            sp.limit(sp.limit(joint_model, joint_a, 0), joint_p, sp.oo),
            joint_tau,
            0,
        ),
        joint_l,
        sp.oo,
    )
    add(
        "20.05",
        "四类调节量的联合理想极限",
        {"joint_limit": _zero(joint_limit - target)},
        ("使用可分离的领先修正代理", "P,ell 为正"),
        "真实极限含交叉项、对数、混合和相关数据；该检查只验证终章流程骨架。",
    )

    records.extend(_build_advanced_records())

    expected_codes = tuple(
        lesson.code for volume in VOLUMES for lesson in volume.lessons
    )
    actual_codes = tuple(record.lesson_code for record in records)
    if len(records) != len(expected_codes):
        raise AssertionError(
            f"SymPy 记录应与课程单元数相等：expected={len(expected_codes)}, "
            f"actual={len(records)}"
        )
    if len(set(actual_codes)) != len(actual_codes):
        raise AssertionError("SymPy 记录编号重复")
    if set(actual_codes) != set(expected_codes):
        missing = sorted(set(expected_codes) - set(actual_codes))
        extra = sorted(set(actual_codes) - set(expected_codes))
        raise AssertionError(f"SymPy 编号不闭合：missing={missing}, extra={extra}")
    order = {code: idx for idx, code in enumerate(expected_codes)}
    records.sort(key=lambda item: order[item.lesson_code])
    return tuple(records)


def write_results(records: Sequence[ValidationRecord], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "lattice-qcd-course-sympy-v1",
        "total": len(records),
        "passed": sum(item.status == "verified" for item in records),
        "records": [asdict(item) for item in records],
    }
    (output_dir / "sympy_validation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines_out = [
        "% 由 sympy_validation.py 生成；不要手工编辑。",
        r"\begin{longtable}{p{0.12\linewidth}p{0.20\linewidth}p{0.13\linewidth}p{0.45\linewidth}}",
        r"\toprule",
        r"编号 & 检查对象 & 状态 & 证据边界\\",
        r"\midrule",
        r"\endhead",
    ]
    for item in records:
        boundary = (
            item.boundary.replace("\\", r"\textbackslash{}")
            .replace("&", r"\&")
            .replace("%", r"\%")
            .replace("_", r"\_")
            .replace("#", r"\#")
        )
        title = item.title.replace("&", r"\&").replace("_", r"\_")
        status = "通过" if item.status == "verified" else "失败"
        lines_out.append(
            f"{item.validation_id} & {title} & {status} & {boundary}\\\\"
        )
    lines_out.extend((r"\bottomrule", r"\end{longtable}", ""))
    (output_dir / "sympy_validation_table.tex").write_text(
        "\n".join(lines_out), encoding="utf-8"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=COURSE_DIR / "generated",
        help="验证 JSON/TeX 的输出目录",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="只执行，不写生成文件",
    )
    args = parser.parse_args(argv)
    records = build_records()
    failed = [item.validation_id for item in records if item.status != "verified"]
    if not args.check_only:
        write_results(records, args.output_dir)
    print(f"SymPy validations: {len(records) - len(failed)}/{len(records)} passed")
    if failed:
        print("failed:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

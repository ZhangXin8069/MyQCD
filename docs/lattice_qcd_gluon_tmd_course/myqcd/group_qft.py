"""群论、李代数与量子场论的有限维 SymPy 例题。"""

from __future__ import annotations

from typing import Tuple

import sympy as sp

from ._common import SymbolicExample, is_zero, make_example, matrix_is_zero


def su2_lie_algebra() -> SymbolicExample:
    """用 Pauli 矩阵验证 SU(2) 对易关系、归一化和 Casimir。"""

    sigma = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )
    generators = tuple(item / 2 for item in sigma)
    commutators_ok = True
    normalization_ok = True
    for a in range(3):
        for b in range(3):
            rhs = sp.zeros(2)
            for c in range(3):
                rhs += sp.I * sp.LeviCivita(a, b, c) * generators[c]
            commutators_ok &= matrix_is_zero(
                generators[a] * generators[b]
                - generators[b] * generators[a]
                - rhs
            )
            normalization_ok &= is_zero(
                sp.trace(generators[a] * generators[b])
                - sp.Rational(1, 2) * int(a == b)
            )
    casimir = sum((item * item for item in generators), sp.zeros(2))
    return make_example(
        "MYQCD-GQ-01",
        "SU(2) 生成元与二次 Casimir",
        ("22.03",),
        {"T1": generators[0], "T2": generators[1], "T3": generators[2], "C2": casimir},
        {
            "commutators": commutators_ok,
            "trace_normalization": normalization_ok,
            "fundamental_casimir": matrix_is_zero(
                casimir - sp.Rational(3, 4) * sp.eye(2)
            ),
        },
        ("T_a=sigma_a/2", "hbar=1", "二维基本表示"),
        "有限矩阵可验证一个表示；它不替代 SU(2) 全局拓扑与全部不可约表示的证明。",
        ("BOOK-GROUP", "BOOK-QFT"),
    )


def su3_fundamental_representation() -> SymbolicExample:
    """验证 Gell-Mann 基，并显式构造 A2 根、基本权和 Dynkin 数据。"""

    sqrt3 = sp.sqrt(3)
    lambdas = (
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, -sp.I, 0], [sp.I, 0, 0], [0, 0, 0]]),
        sp.Matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, -sp.I], [0, 0, 0], [sp.I, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -sp.I], [0, sp.I, 0]]),
        sp.diag(1, 1, -2) / sqrt3,
    )
    generators = tuple(item / 2 for item in lambdas)
    hermitian_traceless = all(
        matrix_is_zero(item.H - item) and is_zero(sp.trace(item))
        for item in generators
    )
    trace_normalization = all(
        is_zero(
            sp.trace(generators[a] * generators[b])
            - sp.Rational(1, 2) * int(a == b)
        )
        for a in range(8)
        for b in range(8)
    )
    casimir = sum((item * item for item in generators), sp.zeros(3))
    alpha1 = sp.Matrix([1, 0])
    alpha2 = sp.Matrix([-sp.Rational(1, 2), sqrt3 / 2])
    omega1 = sp.Matrix([sp.Rational(1, 2), 1 / (2 * sqrt3)])
    omega2 = sp.Matrix([0, 1 / sqrt3])
    cartan = sp.Matrix(
        [
            [2 * alpha1.dot(alpha1), 2 * alpha1.dot(alpha2)],
            [2 * alpha2.dot(alpha1), 2 * alpha2.dot(alpha2)],
        ]
    )
    weight_pairing = sp.Matrix(
        [
            [2 * omega1.dot(alpha1), 2 * omega1.dot(alpha2)],
            [2 * omega2.dot(alpha1), 2 * omega2.dot(alpha2)],
        ]
    )
    p, q = sp.symbols("p q", integer=True, nonnegative=True)
    dynkin_dimension = (p + 1) * (q + 1) * (p + q + 2) / 2
    dynkin_casimir = (p**2 + q**2 + p * q + 3 * p + 3 * q) / 3
    completeness = all(
        is_zero(
            sum(g[i, j] * g[k, ell] for g in generators)
            - sp.Rational(1, 2)
            * (
                int(i == ell) * int(j == k)
                - sp.Rational(1, 3) * int(i == j) * int(k == ell)
            )
        )
        for i in range(3)
        for j in range(3)
        for k in range(3)
        for ell in range(3)
    )
    return make_example(
        "MYQCD-GQ-02",
        "SU(3) 生成元、A2 根权与 Dynkin 表示数据",
        ("07.02", "22.04"),
        {
            "T3": generators[2],
            "T8": generators[7],
            "sum_Ta2": casimir,
            "simple_roots": sp.Matrix.hstack(alpha1, alpha2),
            "fundamental_weights": sp.Matrix.hstack(omega1, omega2),
            "Cartan": cartan,
            "dim(p,q)": dynkin_dimension,
            "C2(p,q)": dynkin_casimir,
        },
        {
            "Hermitian_and_traceless": hermitian_traceless,
            "trace_normalization": trace_normalization,
            "fundamental_casimir": matrix_is_zero(
                casimir - sp.Rational(4, 3) * sp.eye(3)
            ),
            "color_completeness": completeness,
            "A2_Cartan": matrix_is_zero(
                cartan - sp.Matrix([[2, -1], [-1, 2]])
            ),
            "fundamental_weight_duality": matrix_is_zero(
                weight_pairing - sp.eye(2)
            ),
            "Dynkin_3_and_8": is_zero(
                dynkin_dimension.subs({p: 1, q: 0}) - 3
            )
            and is_zero(dynkin_casimir.subs({p: 1, q: 0}) - sp.Rational(4, 3))
            and is_zero(dynkin_dimension.subs({p: 1, q: 1}) - 8)
            and is_zero(dynkin_casimir.subs({p: 1, q: 1}) - 3),
        },
        ("T_a=lambda_a/2 为厄米约定", "Tr(T_a T_b)=delta_ab/2", "根长归一化 |alpha_i|^2=1", "Dynkin (p,q)>=0"),
        "验证颜色代数、根权对偶以及 3/8 表示数据；不计算一般权 multiplicity、非阿贝尔路径排序、费曼图或强耦合动力学。",
        ("BOOK-QFT", "BOOK-QCD-LATTICE", "PYQCD-CONVENTIONS"),
    )


def bch_nilpotent_example() -> SymbolicExample:
    """在中心交换子的幂零代数中精确验证 BCH 截断。"""

    x = sp.zeros(3)
    y = sp.zeros(3)
    x[0, 1] = 1
    y[1, 2] = 1
    commutator = x * y - y * x
    lhs = x.exp() * y.exp()
    rhs = (x + y + commutator / 2).exp()
    return make_example(
        "MYQCD-GQ-03",
        "Baker--Campbell--Hausdorff 公式的精确截断",
        ("22.02",),
        {"X": x, "Y": y, "commutator": commutator, "expX_expY": lhs},
        {
            "central_commutator": matrix_is_zero(commutator * x - x * commutator)
            and matrix_is_zero(commutator * y - y * commutator),
            "BCH_identity": matrix_is_zero(lhs - rhs),
        },
        ("X、Y 为三阶 Heisenberg 幂零矩阵", "二重交换子为零"),
        "一般 BCH 是无穷级数；本例精确只因所有更高嵌套交换子消失。",
        ("BOOK-GROUP", "BOOK-QFT"),
    )


def u1_field_strength_gauge_invariance() -> SymbolicExample:
    """验证 Abelian 场强在 A_mu -> A_mu + partial_mu alpha 下不变。"""

    x, y = sp.symbols("x y", real=True)
    alpha = sp.Function("alpha")(x, y)
    ax = sp.Function("A_x")(x, y)
    ay = sp.Function("A_y")(x, y)
    field_strength = sp.diff(ay, x) - sp.diff(ax, y)
    transformed = sp.diff(ay + sp.diff(alpha, y), x) - sp.diff(
        ax + sp.diff(alpha, x), y
    )
    return make_example(
        "MYQCD-GQ-04",
        "U(1) 场强的规范不变性",
        ("04.04", "23.03"),
        {"F_xy": field_strength, "F_xy_prime": transformed},
        {
            "gauge_invariance": is_zero(transformed - field_strength),
            "pure_gauge_has_zero_field": is_zero(
                sp.diff(sp.diff(alpha, y), x) - sp.diff(sp.diff(alpha, x), y)
            ),
        },
        ("alpha、A_x、A_y 二阶连续可微", "偏导可交换", "Abelian U(1)"),
        "非阿贝尔场强还含 g[A_mu,A_nu]；本例不能验证 SU(3) 的自相互作用。",
        ("BOOK-EM", "BOOK-QFT"),
    )


def gaussian_generating_functional() -> SymbolicExample:
    """验证高斯生成泛函，并补一个 d=4-epsilon 的 phi4 一圈极点链。"""

    k = sp.Symbol("K", positive=True, real=True)
    source = sp.Symbol("J", real=True)
    field = sp.Symbol("phi", real=True)
    integrand = sp.exp(-k * field**2 / 2 + source * field)
    integral = sp.integrate(integrand, (field, -sp.oo, sp.oo))
    closed = sp.sqrt(2 * sp.pi / k) * sp.exp(source**2 / (2 * k))
    one_point = sp.diff(sp.log(closed), source)
    connected_two_point = sp.diff(sp.log(closed), source, 2)
    epsilon, mu, mass_squared, coupling = sp.symbols(
        "epsilon mu m2 lambda", positive=True, real=True
    )
    bubble = (
        mu**epsilon
        * sp.gamma(epsilon / 2)
        * mass_squared ** (-epsilon / 2)
        / (4 * sp.pi) ** (2 - epsilon / 2)
    )
    pole_residue = sp.limit(epsilon * bubble, epsilon, 0, dir="+")
    beta_coefficient = 3 / (16 * sp.pi**2)
    counterterm = 3 * coupling**2 / (16 * sp.pi**2 * epsilon)
    reduced_bare = coupling + beta_coefficient * coupling**2 / epsilon
    beta_dimreg = -epsilon * coupling + beta_coefficient * coupling**2
    fixed_bare_residual = sp.series(
        epsilon * reduced_bare
        + sp.diff(reduced_bare, coupling) * beta_dimreg,
        coupling,
        0,
        3,
    ).removeO()
    return make_example(
        "MYQCD-GQ-05",
        "高斯生成泛函与 phi4 一圈极点、反项和 beta 函数",
        ("24.03", "24.05"),
        {
            "integrand": integrand,
            "Z": closed,
            "dlogZ_dJ": one_point,
            "one_loop_bubble": bubble,
            "bubble_pole_residue": pole_residue,
            "delta_lambda": counterterm,
            "beta_lambda": beta_dimreg,
        },
        {
            "Gaussian_integral": is_zero(integral - closed),
            "one_point": is_zero(one_point - source / k),
            "connected_two_point": is_zero(connected_two_point - 1 / k),
            "bubble_pole": is_zero(pole_residue - 1 / (8 * sp.pi**2)),
            "three_channel_counterterm": is_zero(
                sp.Rational(3, 2) * coupling**2 * pole_residue / epsilon
                - counterterm
            ),
            "fixed_bare_RGE": is_zero(fixed_bare_residual),
        },
        ("K>0 且 J、phi 为实数", "lambda phi^4/4! 于 d=4-epsilon", "Euclidean massive bubble 与 MS 极点"),
        "高斯部分只代理自由场正规模；一圈部分只给 pole/counterterm/beta 链，有限项、二圈与非微扰测度不由此得到。",
        ("BOOK-QFT",),
    )


def transverse_projector() -> SymbolicExample:
    """验证二维 Euclidean 动量空间横向投影算符。"""

    q1, q2 = sp.symbols("q_1 q_2", real=True)
    q = sp.Matrix([q1, q2])
    q_squared = (q.T * q)[0]
    projector = sp.eye(2) - q * q.T / q_squared
    return make_example(
        "MYQCD-GQ-06",
        "Ward 恒等式中的横向投影",
        ("25.04",),
        {"q_squared": q_squared, "P_T": projector},
        {
            "transverse": matrix_is_zero(sp.simplify(q.T * projector)),
            "idempotent": matrix_is_zero(sp.simplify(projector * projector - projector)),
            "rank_trace": is_zero(sp.simplify(sp.trace(projector) - 1)),
        },
        ("q_1^2+q_2^2 != 0", "二维 Euclidean 代理"),
        "投影代数不证明规范固定后的量子 Ward/Slavnov--Taylor 恒等式无反常。",
        ("BOOK-QFT", "PYQCD-TMD-VALIDATION"),
    )


def build_examples() -> Tuple[SymbolicExample, ...]:
    """按稳定编号返回本章全部示例。"""

    return (
        su2_lie_algebra(),
        su3_fundamental_representation(),
        bch_nilpotent_example(),
        u1_field_strength_gauge_invariance(),
        gaussian_generating_functional(),
        transverse_projector(),
    )

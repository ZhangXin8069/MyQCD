"""格点色散、有限时间谱学、GEVP、有限体积与统计例题。"""

from __future__ import annotations

from typing import Tuple

import sympy as sp

from ._common import SymbolicExample, is_zero, make_example, matrix_is_zero


def lattice_dispersion_relation() -> SymbolicExample:
    """检查最近邻格点动量在连续极限恢复 p。"""

    p = sp.Symbol("p", real=True)
    mass = sp.Symbol("m", positive=True, real=True)
    p_hat_squared = 4 * sp.sin(p / 2) ** 2
    energy = sp.sqrt(mass**2 + p_hat_squared)
    expansion = sp.series(p_hat_squared, p, 0, 6).removeO().expand()
    return make_example(
        "MYQCD-SP-01",
        "自由格点色散关系与连续极限",
        ("27.01", "32.03"),
        {"p_hat_squared": p_hat_squared, "series": expansion, "E": energy},
        {
            "rest_energy": is_zero(energy.subs(p, 0) - mass),
            "continuum_momentum": is_zero(sp.limit(p_hat_squared / p**2, p, 0) - 1),
            "leading_cutoff_term": is_zero(
                expansion - p**2 + p**4 / 12
            ),
        },
        ("格距取 a=1", "m>0", "一维最近邻自由场代理"),
        "相互作用强子的色散关系和各向异性参数必须由格点数据拟合。",
        ("BOOK-LQCD", "PYQCD-SPECTRUM"),
    )


def finite_time_meson_correlator() -> SymbolicExample:
    """验证有限时间周期边界下单态介子关联函数的 cosh 形式。"""

    amplitude, energy, time, extent = sp.symbols(
        "A E t T", positive=True, real=True
    )
    correlator = amplitude * (
        sp.exp(-energy * time) + sp.exp(-energy * (extent - time))
    )
    cosh_form = (
        2
        * amplitude
        * sp.exp(-energy * extent / 2)
        * sp.cosh(energy * (extent / 2 - time))
    )
    return make_example(
        "MYQCD-SP-02",
        "介子关联函数的 forward/backward 与 cosh 等价",
        ("13.03", "27.02"),
        {"C(t)": correlator, "cosh_form": cosh_form},
        {
            "time_reflection": is_zero(correlator.subs(time, extent - time) - correlator),
            "cosh_identity": is_zero(
                correlator - sp.expand(cosh_form.rewrite(sp.exp))
            ),
            "midpoint_stationary": is_zero(
                sp.diff(correlator, time).subs(time, extent / 2)
            ),
        },
        ("A,E,T>0", "单态近似", "介子有效周期边界"),
        "多态、热绕回和开放边界需扩展模型；cosh 拟合本身不保证基态占优。",
        ("BOOK-LQCD", "PYQCD-CORRELATOR", "PYQCD-SPECTRUM"),
    )


def baryon_parity_boundary_relation() -> SymbolicExample:
    """保留重子投影关联函数中的 backward 反宇称伙伴。"""

    ap, am, ep, em, time, extent = sp.symbols(
        "A_plus A_minus E_plus E_minus t T", positive=True, real=True
    )
    c_plus = ap * sp.exp(-ep * time) - am * sp.exp(-em * (extent - time))
    c_minus = am * sp.exp(-em * time) - ap * sp.exp(-ep * (extent - time))
    return make_example(
        "MYQCD-SP-03",
        "重子反周期边界与反宇称 backward 态",
        ("27.03",),
        {"C_plus": c_plus, "C_minus": c_minus},
        {
            "parity_time_reflection": is_zero(
                c_plus.subs(time, extent - time) + c_minus
            ),
            "infinite_T_forward_limit": is_zero(
                sp.limit(c_plus, extent, sp.oo) - ap * sp.exp(-ep * time)
            ),
        },
        ("A_plus,A_minus,E_plus,E_minus,T>0", "固定 P+ 投影", "奇数夸克有效反周期边界"),
        "符号依赖算符、gamma 基和投影约定；真实拟合必须与 PyQCD 元数据逐项对齐。",
        ("PYQCD-CONVENTIONS", "PYQCD-SPECTRUM"),
    )


def two_state_effective_energy() -> SymbolicExample:
    """推导二态污染对连续有效能量的指数抑制。"""

    e0, gap, ratio, time = sp.symbols(
        "E_0 Delta r t", positive=True, real=True
    )
    correlator = sp.exp(-e0 * time) * (1 + ratio * sp.exp(-gap * time))
    effective = -sp.diff(sp.log(correlator), time)
    expected = e0 + gap * ratio * sp.exp(-gap * time) / (
        1 + ratio * sp.exp(-gap * time)
    )
    return make_example(
        "MYQCD-SP-04",
        "二态有效能量的基态极限",
        ("13.04", "27.04"),
        {"C(t)": correlator, "E_eff": effective, "gap_form": expected},
        {
            "effective_energy_formula": is_zero(effective - expected),
            "ground_state_limit": is_zero(sp.limit(effective, time, sp.oo) - e0),
            "positive_contamination": bool(
                (expected - e0).is_positive
            ),
        },
        ("E0,Delta,r,t>0", "无限时间方向", "两态截断"),
        "有限 T 的 backward 态、振幅相位和多态拟合系统误差未包含。",
        ("BOOK-LQCD", "PYQCD-SPECTRUM", "PYQCD-STATISTICS"),
    )


def generalized_eigenvalue_problem() -> SymbolicExample:
    """用可逆重叠矩阵验证二态 GEVP 的广义本征值。"""

    e0, e1, time, time0, overlap = sp.symbols(
        "E_0 E_1 t t_0 s", positive=True, real=True
    )
    z_matrix = sp.Matrix([[1, overlap], [0, 1]])

    def correlator(at_time: sp.Expr) -> sp.Matrix:
        diagonal = sp.diag(sp.exp(-e0 * at_time), sp.exp(-e1 * at_time))
        return z_matrix * diagonal * z_matrix.T

    evolution = sp.simplify(correlator(time0).inv() * correlator(time))
    eigenvalue = sp.Symbol("lambda")
    characteristic = sp.factor((evolution - eigenvalue * sp.eye(2)).det())
    expected = sp.factor(
        (eigenvalue - sp.exp(-e0 * (time - time0)))
        * (eigenvalue - sp.exp(-e1 * (time - time0)))
    )
    return make_example(
        "MYQCD-SP-05",
        "二态相关矩阵的 GEVP 谱",
        ("27.05",),
        {"Z": z_matrix, "C0_inverse_Ct": evolution, "characteristic": characteristic},
        {
            "overlap_invertible": is_zero(z_matrix.det() - 1),
            "generalized_eigenvalues": is_zero(characteristic - expected),
            "correlator_symmetric": matrix_is_zero(correlator(time).T - correlator(time)),
        },
        ("Z 可逆", "两个精确态", "t>t0>=0", "无统计噪声"),
        "真实 GEVP 还需 Hermitian 正定性、条件化、态追踪和重采样；近简并态不能只按本征值排序。",
        ("PYQCD-SPECTRUM", "PYQCD-STATISTICS", "LQCDDB"),
    )


def luscher_leading_volume_shift() -> SymbolicExample:
    """检查两粒子阈值能移的 1/L 展开与无限体积极限。"""

    scattering_length, mass, length = sp.symbols("a_0 m L", positive=True, real=True)
    c1, c2 = sp.symbols("c_1 c_2", real=True)
    shift = -4 * sp.pi * scattering_length / (mass * length**3) * (
        1
        + c1 * scattering_length / length
        + c2 * (scattering_length / length) ** 2
    )
    return make_example(
        "MYQCD-SP-06",
        "Luescher 阈值能移的有限体积幂次",
        ("28.03", "29.02"),
        {"Delta_E": shift, "expansion_parameter": scattering_length / length},
        {
            "infinite_volume": is_zero(sp.limit(shift, length, sp.oo)),
            "leading_L_cubed_limit": is_zero(
                sp.limit(length**3 * shift, length, sp.oo)
                + 4 * sp.pi * scattering_length / mass
            ),
            "noninteracting_limit": is_zero(shift.subs(scattering_length, 0)),
        },
        ("|a0|/L << 1", "弹性阈值区", "采用本例所写散射长度符号约定"),
        "只检查低能展开结构；一般移动系、多通道、部分波混合需使用完整量子化条件。",
        ("BOOK-LQCD", "PYQCD-SPECTRUM"),
    )


def matsubara_boundary_conditions() -> SymbolicExample:
    """从 Euclidean 时间边界验证玻色/费米 Matsubara 频率。"""

    n = sp.Symbol("n", integer=True)
    temperature = sp.Symbol("T", positive=True, real=True)
    beta = 1 / temperature
    omega_b = 2 * sp.pi * n * temperature
    omega_f = (2 * n + 1) * sp.pi * temperature
    return make_example(
        "MYQCD-SP-07",
        "有限温度的周期与反周期频率",
        ("30.01", "30.02"),
        {"beta": beta, "omega_b": omega_b, "omega_f": omega_f},
        {
            "boson_periodic": is_zero(sp.exp(sp.I * omega_b * beta) - 1),
            "fermion_antiperiodic": is_zero(sp.exp(sp.I * omega_f * beta) + 1),
            "frequency_offset": is_zero(omega_f - omega_b - sp.pi * temperature),
        },
        ("n 为整数", "T>0", "Euclidean 时间长度 beta=1/T"),
        "相互作用热谱、解析延拓和有限 Nt 截止效应不由频率计数决定。",
        ("BOOK-QFT", "BOOK-LQCD"),
    )


def delete_one_jackknife_identity() -> SymbolicExample:
    """以三个精确样本验证 delete-one jackknife 的均值与方差因子。"""

    x1, x2, x3 = sp.symbols("x_1 x_2 x_3", real=True)
    samples = (x1, x2, x3)
    sample_mean = sum(samples) / 3
    jackknife = tuple((sum(samples) - value) / 2 for value in samples)
    jackknife_mean = sum(jackknife) / 3
    jackknife_variance = sp.Rational(2, 3) * sum(
        (value - jackknife_mean) ** 2 for value in jackknife
    )
    mean_variance_from_sample = sum(
        (value - sample_mean) ** 2 for value in samples
    ) / 6
    return make_example(
        "MYQCD-SP-08",
        "delete-one jackknife 的中心值与误差因子",
        ("14.02", "27.05"),
        {"sample_mean": sample_mean, "jackknife_samples": jackknife, "variance": jackknife_variance},
        {
            "center_preserved": is_zero(jackknife_mean - sample_mean),
            "variance_prefactor": is_zero(
                jackknife_variance - mean_variance_from_sample
            ),
        },
        ("三个等权独立样本", "估计量为线性样本均值"),
        "非线性拟合、自相关分箱、复协方差与共享重采样必须在真实分析中另行验证。",
        ("BOOK-STAT", "PYQCD-STATISTICS"),
    )


def build_examples() -> Tuple[SymbolicExample, ...]:
    """按稳定编号返回本章全部示例。"""

    return (
        lattice_dispersion_relation(),
        finite_time_meson_correlator(),
        baryon_parity_boundary_relation(),
        two_state_effective_energy(),
        generalized_eigenvalue_problem(),
        luscher_leading_volume_shift(),
        matsubara_boundary_conditions(),
        delete_one_jackknife_identity(),
    )

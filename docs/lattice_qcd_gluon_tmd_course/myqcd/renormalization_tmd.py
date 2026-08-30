"""梯度流、重整化、soft/rapidity 与 TMD 提取的 SymPy 例题。"""

from __future__ import annotations

from typing import Tuple

import sympy as sp

from ._common import SymbolicExample, is_zero, make_example, matrix_is_zero


def gradient_flow_heat_kernel() -> SymbolicExample:
    """验证线性化梯度流的热核方程、初值和半群。"""

    tau, tau1, tau2, momentum = sp.symbols(
        "tau tau_1 tau_2 p", nonnegative=True, real=True
    )
    initial = sp.Symbol("B_0")
    field = initial * sp.exp(-tau * momentum**2)
    kernel = lambda flow_time: sp.exp(-flow_time * momentum**2)
    return make_example(
        "MYQCD-RT-01",
        "线性化梯度流的热核半群",
        ("15.02", "26.03"),
        {"B(tau,p)": field, "K(tau,p)": kernel(tau)},
        {
            "flow_equation": is_zero(sp.diff(field, tau) + momentum**2 * field),
            "initial_condition": is_zero(field.subs(tau, 0) - initial),
            "semigroup": is_zero(
                kernel(tau1) * kernel(tau2) - kernel(tau1 + tau2)
            ),
        },
        ("tau>=0", "线性化/Abelian Fourier 模", "p 为 Euclidean 动量模"),
        "非线性 Yang--Mills 流、离散积分器误差和 SU(3) 幺正性需独立数值检查。",
        ("BOOK-LQCD", "PYQCD-GAUGE", "PYQCD-TMD"),
    )


def gradient_flow_scale_counting() -> SymbolicExample:
    """检查平滑半径 sqrt(8 tau) 与 t^2 E(tau) 的尺度结构。"""

    tau, scale, coefficient = sp.symbols("tau lambda c", positive=True, real=True)
    radius = sp.sqrt(8 * tau)
    energy_density = coefficient / tau**2
    return make_example(
        "MYQCD-RT-02",
        "梯度流平滑半径与能量密度标度",
        ("15.03", "33.05"),
        {"r_flow": radius, "E(tau)": energy_density, "tau2E": tau**2 * energy_density},
        {
            "radius_squared": is_zero(radius**2 - 8 * tau),
            "radius_rescaling": is_zero(
                radius.subs(tau, scale**2 * tau) - scale * radius
            ),
            "dimensionless_tau2E_proxy": is_zero(tau**2 * energy_density - coefficient),
        },
        ("tau>0", "[tau]=L^2", "树级尺度代理 E=c/tau^2"),
        "量纲由物理约定输入；SymPy 不证明真实 E(tau) 单调，也不确定参考尺度的数值。",
        ("PYQCD-GAUGE", "PYQCD-TMD-RENORM"),
    )


def wilson_line_linear_counterterm() -> SymbolicExample:
    """验证 Wilson 线线性发散指数因子的乘法抵消。"""

    delta_m, separation, spacing = sp.symbols(
        "delta_m z a", positive=True, real=True
    )
    finite_matrix_element = sp.Symbol("h_fin")
    bare = sp.exp(-delta_m * separation / spacing) * finite_matrix_element
    counterterm = sp.exp(delta_m * separation / spacing)
    return make_example(
        "MYQCD-RT-03",
        "Wilson 线线性发散的指数反项",
        ("18.02", "34.02"),
        {"h_bare": bare, "counterterm": counterterm},
        {
            "linear_factor_cancels": is_zero(counterterm * bare - finite_matrix_element),
            "local_limit": is_zero(bare.subs(separation, 0) - finite_matrix_element),
        },
        ("a,z,delta_m>0", "单一可乘指数发散代理", "未含算符混合"),
        "delta_m 必须由指定方案确定；抵消代数不证明有限部分、rapidity 发散或匹配已处理。",
        ("BOOK-QFT", "PYQCD-TMD-RENORM"),
    )


def ri_mom_and_ratio_schemes() -> SymbolicExample:
    """同时演示 RI/MOM 条件求解、方案转换与短距比值抵消。"""

    zq, vertex_bare, vertex_tree, conversion = sp.symbols(
        "Z_q Lambda_B Lambda_tree C_MS_RI", nonzero=True
    )
    operator_bare, common_z, h1, h0 = sp.symbols(
        "O_B Z_common h_1 h_0", nonzero=True
    )
    zop = zq * vertex_tree / vertex_bare
    projected_renormalized_vertex = zop * vertex_bare / zq
    operator_ms = conversion * operator_bare / zop
    ratio = (common_z * h1) / (common_z * h0)
    return make_example(
        "MYQCD-RT-04",
        "RI/MOM、MSbar 转换与比值方案",
        ("33.02", "33.03", "34.03"),
        {"Z_O_RI": zop, "O_MS": operator_ms, "short_distance_ratio": ratio},
        {
            "RI_MOM_condition": is_zero(
                projected_renormalized_vertex - vertex_tree
            ),
            "conversion_chain_contains_inverse_Z": is_zero(
                operator_ms * zop - conversion * operator_bare
            ),
            "common_factor_cancels": is_zero(ratio - h1 / h0),
        },
        ("所有分母非零", "固定规范与投影", "共同 UV 因子确实相同"),
        "实际 RI/MOM 需离壳 Green 函数、窗口和连续外推；比值法只消掉真正公共的因子。",
        ("BOOK-QFT", "PYQCD-TMD-RENORM"),
    )


def operator_mixing_matrix() -> SymbolicExample:
    """验证二算符混合矩阵的可逆条件及无混合极限。"""

    z11, z12, z21, z22 = sp.symbols("Z_11 Z_12 Z_21 Z_22")
    matrix = sp.Matrix([[z11, z12], [z21, z22]])
    determinant = sp.factor(matrix.det())
    inverse = matrix.inv()
    diagonal_inverse = inverse.subs({z12: 0, z21: 0})
    return make_example(
        "MYQCD-RT-05",
        "算符混合矩阵与可乘重整化极限",
        ("33.04", "34.04"),
        {"Z": matrix, "detZ": determinant, "Z_inverse": inverse},
        {
            "left_inverse": matrix_is_zero(sp.simplify(inverse * matrix - sp.eye(2))),
            "right_inverse": matrix_is_zero(sp.simplify(matrix * inverse - sp.eye(2))),
            "multiplicative_limit": matrix_is_zero(
                diagonal_inverse - sp.diag(1 / z11, 1 / z22)
            ),
        },
        ("det(Z)!=0", "二维闭合算符基", "同一正则化与方案"),
        "真实胶子算符基可能更大并含低维混合；选取 2x2 只展示线性代数结构。",
        ("BOOK-QFT", "PYQCD-TMD-RENORM"),
    )


def soft_subtraction_identity() -> SymbolicExample:
    """验证一个已完整声明的 quasi-soft 方案中的分层消除。"""

    zuv, qsoft, quasi_finite, conversion = sp.symbols(
        "Z_UV S_qsoft h_quasi C_qsoft_to_S", positive=True, real=True
    )
    bare = zuv * sp.sqrt(qsoft) * quasi_finite
    standard_scheme = conversion * bare / (zuv * sp.sqrt(qsoft))
    wrong_without_soft = conversion * bare / zuv
    return make_example(
        "MYQCD-RT-06",
        "TMD soft subtraction 不能由普通 UV 重整化替代",
        ("16.03", "34.01"),
        {
            "h_bare": bare,
            "h_standard_scheme": standard_scheme,
            "UV_only": wrong_without_soft,
        },
        {
            "declared_scheme_chain": is_zero(
                standard_scheme - conversion * quasi_finite
            ),
            "UV_only_leaves_soft": is_zero(
                wrong_without_soft
                - conversion * sp.sqrt(qsoft) * quasi_finite
            ),
            "all_unit_factors_special_case": is_zero(
                standard_scheme.subs(
                    {qsoft: 1, conversion: 1, zuv: 1}
                )
                - quasi_finite
            ),
        },
        (
            "Z_UV,S_qsoft,h_quasi,C_qsoft_to_S>0",
            "固定 f1g[-,-] link class、v/vbar、rapidity regulator rho 与 zero-bin",
            "beam、quasi-soft 与转换核采用兼容的表示、路径和流时间",
        ),
        "本例只验证已声明对称平方根约定的代数；它不把任意 Euclidean 真空 staple 认作标准 soft，也不计算 C_qsoft_to_S。",
        ("DOC-TMD", "PYQCD-TMD-RENORM", "PYQCD-TMD-VALIDATION"),
    )


def collins_soper_evolution() -> SymbolicExample:
    """验证以 y=ln sqrt(zeta/zeta0) 表示的 Collins--Soper 解。"""

    y, y1, y2, kernel = sp.symbols("y y_1 y_2 K", real=True)
    initial = sp.Symbol("F_0", positive=True)
    evolved = initial * sp.exp(kernel * y)
    return make_example(
        "MYQCD-RT-07",
        "Collins--Soper 快度演化的群性质",
        ("16.04", "34.05"),
        {"F(y)": evolved, "y": "log(sqrt(zeta/zeta0))"},
        {
            "CS_differential_equation": is_zero(
                sp.diff(sp.log(evolved), y) - kernel
            ),
            "initial_condition": is_zero(evolved.subs(y, 0) - initial),
            "composition": is_zero(
                initial * sp.exp(kernel * y1) * sp.exp(kernel * y2)
                - initial * sp.exp(kernel * (y1 + y2))
            ),
        },
        ("K 在本段演化中视为固定", "F0>0 以选定实对数支"),
        "实际 K(b,mu) 的非微扰部分、mu 演化和截断阶误差必须另行确定。",
        ("DOC-TMD", "PYQCD-TMD-RENORM"),
    )


def two_momentum_cs_estimator() -> SymbolicExample:
    """展示三动量如何把 CS 核与一个有限动量幂修正分开。"""

    y1, y2, y3 = sp.symbols("y_1 y_2 y_3", real=True)
    u1, u2, u3 = sp.symbols("u_1 u_2 u_3", positive=True)
    intercept, kernel, power = sp.symbols("A K c_P", real=True)
    design = sp.Matrix([[1, y1, u1], [1, y2, u2], [1, y3, u3]])
    truth = sp.Matrix([intercept, kernel, power])
    corrected_logs = design * truth
    fitted = sp.simplify(design.inv() * corrected_logs)
    two_point_estimator = sp.simplify(
        (corrected_logs[1] - corrected_logs[0]) / (y2 - y1)
    )
    expected_two_point = kernel + power * (u2 - u1) / (y2 - y1)
    return make_example(
        "MYQCD-RT-08",
        "共同运动学下的三动量 Collins--Soper 核与幂修正分离",
        ("19.04", "34.05"),
        {
            "design_matrix": design,
            "log(Phi_i/H_i)": corrected_logs,
            "fit_parameters": fitted,
            "two_point_K_proxy": two_point_estimator,
        },
        {
            "three_point_recovers_intercept_kernel_power": matrix_is_zero(
                fitted - truth
            ),
            "two_point_power_contamination": is_zero(
                two_point_estimator - expected_two_point
            ),
            "two_point_leading_power_limit": is_zero(
                two_point_estimator.subs(power, 0) - kernel
            ),
        },
        (
            "det(design)!=0，三个 (y_i,u_i) 不共线",
            "y_i 是除去已知硬因子后的 rapidity 对数，u_i=1/P_{z,i}^2",
            "三点比较位于共同 x，或共同 Ioffe time nu=zP_z",
        ),
        "三点线性代理只分离一个 1/P_z^2 项；真实分析还需 b_T/ell/x 依赖、更多动量、相关协方差、匹配截断和端点失效检查。",
        ("PYQCD-TMD", "PYQCD-TMD-RENORM"),
    )


def gaussian_tmd_fourier_transform() -> SymbolicExample:
    """精确计算归一化二维 Gaussian 的径向 Fourier--Bessel 变换。"""

    momentum, impact = sp.symbols("k b", nonnegative=True, real=True)
    width = sp.Symbol("Lambda", positive=True, real=True)
    density = sp.exp(-momentum**2 / width**2) / (sp.pi * width**2)
    transform = sp.integrate(
        2 * sp.pi * momentum * density * sp.besselj(0, impact * momentum),
        (momentum, 0, sp.oo),
    )
    expected = sp.exp(-width**2 * impact**2 / 4)
    normalization = sp.integrate(
        2 * sp.pi * momentum * density, (momentum, 0, sp.oo)
    )
    return make_example(
        "MYQCD-RT-09",
        "二维 Gaussian TMD 的冲击参数变换",
        ("16.02", "19.03"),
        {"f(kT)": density, "F(bT)": transform, "closed_form": expected},
        {
            "momentum_normalization": is_zero(normalization - 1),
            "Fourier_Bessel_transform": is_zero(transform - expected),
            "b_zero_normalization": is_zero(expected.subs(impact, 0) - 1),
        },
        ("Lambda>0", "b,k>=0", "二维径向对称 Gaussian", "Fourier 相位采用 exp(i k dot b)"),
        "Gaussian 是解析教学模型，不是核子胶子 TMD 数据或 QCD 因子化证明。",
        ("DOC-TMD", "PYQCD-TMD"),
    )


def matching_and_hybrid_continuity() -> SymbolicExample:
    """检查树级匹配极限及 hybrid 方案切换点连续性。"""

    alpha, coefficient, quasi = sp.symbols("alpha_s c_1 h_q", real=True)
    matching = 1 + alpha * coefficient
    matched = quasi / matching
    z, switch, short_slope, long_slope, short_value, long_value = sp.symbols(
        "z z_s delta_S delta_L h_S h_L", positive=True, real=True
    )
    normalization = short_value / long_value
    short_branch = short_value * sp.exp(-short_slope * (z - switch))
    long_branch = (
        normalization
        * long_value
        * sp.exp(-long_slope * (z - switch))
    )
    slope_jump = sp.simplify(
        sp.diff(short_branch, z).subs(z, switch)
        - sp.diff(long_branch, z).subs(z, switch)
    )
    return make_example(
        "MYQCD-RT-10",
        "匹配的树级极限与 hybrid 切换连续性",
        ("18.04", "19.05", "34.03"),
        {
            "C": matching,
            "h_matched": matched,
            "hybrid_normalization": normalization,
            "hybrid_short": short_branch,
            "hybrid_long": long_branch,
            "slope_jump": slope_jump,
        },
        {
            "tree_level_matching": is_zero(sp.limit(matched, alpha, 0) - quasi),
            "one_loop_inverse_series": is_zero(
                sp.series(matched, alpha, 0, 2).removeO()
                - quasi * (1 - alpha * coefficient)
            ),
            "hybrid_value_continuity": is_zero(
                short_branch.subs(z, switch) - long_branch.subs(z, switch)
            ),
            "hybrid_slope_jump_is_explicit": is_zero(
                slope_jump - short_value * (long_slope - short_slope)
            ),
        },
        ("|alpha_s c1|<1 用于级数", "h_L 非零", "z 是单一直 Wilson 线长度坐标"),
        "本例只强制 straight-line hybrid 的值连续，导数一般有跳跃；finite-staple 必须改用完整路径周长并另处理端点、cusp 与 mixing。",
        ("PYQCD-TMD-RENORM", "PYQCD-TMD-VALIDATION"),
    )


def finite_staple_geometry() -> SymbolicExample:
    """用二维坐标验证有限 staple 的端点、横向间隔和独立长度。"""

    longitudinal, transverse, staple = sp.symbols("z b ell", real=True)
    start = sp.Matrix([0, 0])
    first = sp.Matrix([staple, 0])
    second = sp.Matrix([longitudinal, transverse])
    third = sp.Matrix([-staple, 0])
    endpoint = start + first + second + third
    signed_area = sp.Matrix.hstack(sp.Matrix([1, 0]), second).det()
    return make_example(
        "MYQCD-RT-11",
        "非零横向间隔的有限 staple 几何",
        ("17.01", "17.02", "34.01"),
        {"segment_1": first, "segment_2": second, "segment_3": third, "endpoint": endpoint},
        {
            "endpoint_displacement": matrix_is_zero(
                endpoint - sp.Matrix([longitudinal, transverse])
            ),
            "staple_length_independent_of_z": is_zero(
                sp.diff(endpoint[0], staple)
            ),
            "signed_area_is_b": is_zero(signed_area - transverse),
            "b_zero_bare_path_area": is_zero(signed_area.subs(transverse, 0)),
            "straight_limit_endpoint": matrix_is_zero(
                endpoint.subs(transverse, 0) - sp.Matrix([longitudinal, 0])
            ),
        },
        ("ell、z、b 是独立几何参数", "路径依次为 +ell、(z,b)、-ell"),
        "端点代数不计算路径有序指数、角点发散或 soft 因子；b=0 只表示裸几何退化，重整化 TMD 与 collinear PDF 的关系必须用 small-b OPE。",
        ("PYQCD-TMD-GEOMETRY", "PYQCD-TMD-VALIDATION"),
    )


def joint_systematic_limits() -> SymbolicExample:
    """验证有序极限、finite-staple 停止门与 flow 支撑安全距离。"""

    spacing, momentum, flow_time, staple = sp.symbols(
        "a P_z tau ell", positive=True, real=True
    )
    target = sp.Symbol("F_target", real=True)
    ca, cp, ct, cl = sp.symbols("c_a c_P c_tau c_ell", real=True)
    transverse, longitudinal, inverse_qcd = sp.symbols(
        "b_T z_abs Lambda_inverse", positive=True, real=True
    )
    source_distance, sink_distance, boundary_distance = sp.symbols(
        "d_source d_sink d_boundary", positive=True, real=True
    )
    support_distance = sp.Min(
        transverse,
        longitudinal,
        staple,
        inverse_qcd,
        source_distance,
        sink_distance,
        boundary_distance,
    )
    flow_radius = sp.sqrt(8 * flow_time)
    model = (
        target
        + ca * spacing**2 / (8 * flow_time)
        + cp / momentum**2
        + ct * flow_time / support_distance**2
        + cl * sp.exp(-staple)
    )
    path_length = sp.Symbol("L_Gamma", positive=True, real=True)
    unconverted_path_term = path_length / sp.sqrt(8 * flow_time)
    limit_value = sp.limit(
        sp.limit(
            sp.limit(sp.limit(model, spacing, 0), momentum, sp.oo),
            flow_time,
            0,
        ),
        staple,
        sp.oo,
    )
    return make_example(
        "MYQCD-RT-12",
        "finite-staple 的 flow window 与有序联合极限",
        ("20.05", "35.02", "35.05"),
        {
            "support_distance": support_distance,
            "flow_radius": flow_radius,
            "fit_model_after_C_Gamma": model,
            "joint_limit": limit_value,
        },
        {
            "joint_limit_reaches_target": is_zero(limit_value - target),
            "continuum_leading_order": is_zero(sp.diff(model, spacing).subs(spacing, 0)),
            "large_momentum_power": is_zero(
                sp.limit(momentum**2 * (cp / momentum**2), momentum, sp.oo) - cp
            ),
            "unconverted_staple_has_no_polynomial_tau_limit": (
                sp.limit(unconverted_path_term, flow_time, 0, dir="+") is sp.oo
            ),
            "tau_before_continuum_is_singular": (
                sp.limit(spacing**2 / (8 * flow_time), flow_time, 0, dir="+")
                is sp.oo
            ),
            "source_distance_can_control_window": is_zero(
                support_distance.subs(
                    {
                        transverse: 5,
                        longitudinal: 6,
                        staple: 7,
                        inverse_qcd: 8,
                        source_distance: 2,
                        sink_distance: 9,
                        boundary_distance: 10,
                    }
                )
                - 2
            ),
            "sink_distance_can_control_window": is_zero(
                support_distance.subs(
                    {
                        transverse: 5,
                        longitudinal: 6,
                        staple: 7,
                        inverse_qcd: 8,
                        source_distance: 9,
                        sink_distance: 2,
                        boundary_distance: 10,
                    }
                )
                - 2
            ),
            "boundary_distance_can_control_window": is_zero(
                support_distance.subs(
                    {
                        transverse: 5,
                        longitudinal: 6,
                        staple: 7,
                        inverse_qcd: 8,
                        source_distance: 9,
                        sink_distance: 10,
                        boundary_distance: 2,
                    }
                )
                - 2
            ),
            "explicit_safe_window_example": bool(
                spacing.subs(spacing, sp.Rational(1, 4))
                < flow_radius.subs(flow_time, sp.Rational(1, 8))
                < support_distance.subs(
                    {
                        transverse: 5,
                        longitudinal: 6,
                        staple: 7,
                        inverse_qcd: 8,
                        source_distance: 2,
                        sink_distance: 9,
                        boundary_distance: 10,
                    }
                )
            ),
        },
        (
            "采用可分离领先修正代理",
            "Pz,tau,ell,a 及所有支撑距离为正",
            "tau 项只用于局域或已完成完整 C_Gamma 转换的对象",
            "d_source、d_sink、d_boundary 按整条路径支撑并扣除源汇 smearing 半径",
            "无交叉项与对数",
        ),
        "未转换 finite-staple 可含 L_Gamma/sqrt(8tau)、端点、cusp 与 mixing 项，不得套用本模型；真实联合拟合还含相关数据、交叉项、对数、x/bT/ell 依赖、周期绕回或开放边界效应和方案不确定度。",
        ("PYQCD-TMD", "PYQCD-TMD-VALIDATION", "PYQCD-STATISTICS"),
    )


def build_examples() -> Tuple[SymbolicExample, ...]:
    """按稳定编号返回本章全部示例。"""

    return (
        gradient_flow_heat_kernel(),
        gradient_flow_scale_counting(),
        wilson_line_linear_counterterm(),
        ri_mom_and_ratio_schemes(),
        operator_mixing_matrix(),
        soft_subtraction_identity(),
        collins_soper_evolution(),
        two_momentum_cs_estimator(),
        gaussian_tmd_fourier_transform(),
        matching_and_hybrid_continuity(),
        finite_staple_geometry(),
        joint_systematic_limits(),
    )

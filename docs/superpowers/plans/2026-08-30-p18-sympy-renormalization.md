# P18 LaMET 重整化与 quasi-TMD SymPy 增补实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `myqcd/` 中把 `refer/papers` 里 P18 LaMET 综述及相关重整化、quasi-TMD 论文的高价值结构公式转成可审计的 SymPy 推导入口，并为每个入口保留来源和明确的非目标边界。

**Architecture:** 继续采用 `DerivationResult` 的“方程—符号—假设—检查—状态”接口。有限维矩阵、标量重整化因子和解析代理只用于验证代数恒等式、连续性、指数发散抵消、卷积/比值消去和 CS 核提取；完整 QCD 圈积分、非微扰矩阵元、RI/MOM 数值因子和论文数据不被代理模型冒充。

**Tech Stack:** Python 3、SymPy、pytest；来源为 `refer/papers` 的只读 LaTeX 源，公共接口为 `myqcd.derivations`、`myqcd.formula_registry` 和 `myqcd.__init__`。

**Spec:** `refer/papers/大动量有效理论综述_latex`、`refer/papers/非定域夸克双线性的非微扰重正化_latex`、`refer/papers/准光前关联的混合重正化方案_latex`、`refer/papers/从准TMD波函数确定CS核_latex` 及 `refer/papers/CS_Kernel_Quasi_TMDWF_latex` 的公式源。

## Global Constraints

- 只修改 `myqcd/`、`tests/` 和本计划文件；`refer/papers` 与 `refer/books` 仅读取。
- 每个新入口必须先有会失败的行为测试，再写实现；测试断言独立于被测实现计算期望值。
- 结果必须区分“代数结构已验证”和“完整物理量未计算”，不得编造 RI/MOM、MS-bar、匹配核或格点数值。
- 运行 `run_core_checks()` 时所有新入口必须纳入；不改变现有入口语义，不删除旧产物，不提交或推送。

### Task 1: 辅助场与非局域 Wilson 线重整化

**Files:**
- Modify: `tests/test_myqcd_sympy.py`
- Modify: `myqcd/derivations.py`
- Modify: `myqcd/__init__.py`
- Modify: `myqcd/formula_registry.py`
- Modify: `myqcd/README.md`

**Interfaces:**
- Produces `derive_auxiliary_field_wilson_renormalization() -> DerivationResult`。
- Equation keys include `auxiliary_propagator`, `wilson_line_factorization`, `gamma_prime`, `operator_renormalized`, `gamma_prime_residual`, `operator_factorization_residual`。

- [x] 写测试，断言 `N**2=I` 时 `(I+r s N) Gamma (I+r s N)` 展开为 `Gamma+r*s*(N*Gamma+Gamma*N)+r**2*N*Gamma*N`，并断言 `e**(-m*abs(z))*e**(m*abs(z))=1`。
- [x] 运行专项测试，确认因入口不存在而失败。
- [x] 用显式 2×2 `N=diag(1,-1)` 与非交换 `Gamma` 实现辅助场混合和 Wilson 线指数抵消；只在给定矩阵代理中检查 Hermitian/代数关系。
- [x] 运行专项测试和核心回归，确认通过后再整理命名与来源说明。

### Task 2: RI/MOM、比值方案与坐标空间因子化

**Files:**
- Modify: `tests/test_myqcd_sympy.py`
- Modify: `myqcd/derivations.py`
- Modify: `myqcd/__init__.py`
- Modify: `myqcd/formula_registry.py`
- Modify: `myqcd/README.md`

**Interfaces:**
- Produces `derive_ri_mom_ratio_renormalization() -> DerivationResult`。
- Equation keys include `ri_to_ms_operator`, `ri_conversion_residual`, `ratio_renormalized_matrix_element`, `ratio_uv_cancellation_residual`, `tree_coordinate_matching`, `coordinate_matching_residual`。

- [x] 写测试，使用手工给定的 `O_bare=Z_RI*O_RI`、`O_MS=Z_MS*O_bare/Z_RI` 和一个 `h(λ)=1+λ+λ**2`，断言 RI 因子消去、共同 UV 因子在比值中消去、树级 `DiracDelta(α-1)` 坐标卷积还原 `h(λ)`。
- [x] 运行专项测试确认预期的缺入口失败。
- [x] 实现标量/函数代理的 RI→MS、比值和树级坐标因子化；对高扭度项仅保留带维数的形式符号并在假设中注明未计算。
- [x] 运行专项测试、全量 pytest 和 `run_core_checks()`。

### Task 3: 混合重整化的匹配点连续性和大动量方案模糊性

**Files:**
- Modify: `tests/test_myqcd_sympy.py`
- Modify: `myqcd/derivations.py`
- Modify: `myqcd/__init__.py`
- Modify: `myqcd/formula_registry.py`
- Modify: `myqcd/README.md`

**Interfaces:**
- Produces `derive_hybrid_renormalization() -> DerivationResult`。
- Equation keys include `Z_hybrid`, `matching_point_residual`, `piecewise_conversion`, `conversion_continuity_residual`, `hybrid_kernel_extra`, `scheme_ambiguity_kernel`, `scheme_ambiguity_limit`。

- [x] 写测试，断言 `Z_hybrid*exp(-delta_m*z_S)*h_bare=h_bare/Z_X(z_S)`，分段转换因子在 `z=z_S` 两侧取同一值，且 `delta=m/P_z` 在 `P_z→∞` 时为零。
- [x] 运行专项测试确认缺入口失败。
- [x] 实现 `Piecewise` 的短/长距离转换、匹配点连续性、`C_hybrid-C_ratio` 的显式对数附加项和 Lorentzian 方案差异的无穷动量极限；不计算 `C_ratio` 本身及 plus 分布数值积分。
- [x] 运行专项测试、全量 pytest 和核心审计。

### Task 4: quasi-TMD 因子化、Wilson-loop 抵消和 CS 核提取

**Files:**
- Modify: `tests/test_myqcd_sympy.py`
- Modify: `myqcd/derivations.py`
- Modify: `myqcd/__init__.py`
- Modify: `myqcd/formula_registry.py`
- Modify: `myqcd/README.md`

**Interfaces:**
- Produces `derive_quasi_tmd_matching_and_cs_kernel() -> DerivationResult`。
- Equation keys include `soft_subtracted_quasi_tmd`, `multiplicative_factorization`, `factorization_residual`, `cs_ratio`, `cs_extracted_kernel`, `cs_extraction_residual`, `plus_minus_average`。

- [x] 写测试，使用非零 `S_r`、`Psi`、`H`、`K` 和正 `P_1/P_2` 的符号代理，断言因子化代入后残差为零，CS 比值取对数后还原 `K`，以及 `S_r` 与光锥 `Psi` 在动量比中消去。
- [x] 运行专项测试确认预期的缺入口失败。
- [x] 实现乘法因子化、Wilson-loop 平方根对线性因子的抵消、树级 `H=1` 退化和带硬因子修正的 CS 提取；源文一圈硬核和 running coupling 仅保留为明确的未计算接口。
- [x] 运行专项测试、全量 pytest、`python -m compileall -q myqcd tests` 和核心审计。

### Task 6: RI-xMOM 条件的非微扰参数解法

**Files:**
- Modify: `tests/test_myqcd_sympy.py`
- Modify: `myqcd/derivations.py`
- Modify: `myqcd/__init__.py`
- Modify: `myqcd/formula_registry.py`
- Modify: `myqcd/README.md`

**Interfaces:**
- Produces `derive_ri_xmom_renormalization_conditions() -> DerivationResult`。
- Equation keys include `m_solution`, `zeta_solution`, `z_phi_solution`, `mass_condition_residual`, `zeta_condition_residual`, `phi_condition_residual`, `mixing_projection_residual`。

- [x] 写测试，使用源文三条条件的标量迹代理，断言 `m=-d(log Tr S_zeta)/d xi|xi0`、由两点传播子条件解出的 `Z_zeta`、由混合空间 Green 函数条件解出的 `Z_phi^±` 均使原条件残差为零，并验证 `Z_phi^±=Z_phi(1±r_mix)` 的投影关系。
- [x] 运行专项测试，确认入口缺失导致行为断言失败。
- [x] 实现只依赖 SymPy 的条件求解；把 Landau 规范、`p_0∝n`、RI-xMOM 到 MS-bar 的一圈 `Ci` 转换和静态夸克三圈结果保留为来源/假设，不猜测数值。
- [x] 运行专项测试、全量 pytest 和核心审计。

### Task 7: Wilson 线自能积分与线性反项

**Files:**
- Modify: `tests/test_myqcd_sympy.py`
- Modify: `myqcd/derivations.py`
- Modify: `myqcd/__init__.py`
- Modify: `myqcd/formula_registry.py`
- Modify: `myqcd/README.md`

**Interfaces:**
- Produces `derive_wilson_line_linear_counterterm() -> DerivationResult`。
- Equation keys include `coordinate_self_energy`, `coordinate_closed_form`, `coordinate_integral_residual`, `continuum_linear_coefficient`, `counterterm`, `linear_divergence_cancellation_residual`, `lattice_linear_coefficient`, `cutoff_matching_residual`。

- [ ] 写测试，断言坐标空间双重积分还原 `z/a*atan(z/a)-log(1+z**2/a**2)/2`，并断言用 `alpha_s=g**2/(4*pi)`、`Lambda=1/a` 后自能线性系数与源文 `delta_m` 相加为零。
- [ ] 运行专项测试确认入口缺失导致行为断言失败。
- [ ] 实现正 `z,a` 下的 SymPy 双重积分、`z→∞` 线性系数、连续/格点 cutoff 对齐和有限 `O(a/z)` 结构；不计算完整 Fourier 分布或格点数值拟合。
- [ ] 运行专项测试、全量 pytest 和核心审计。

### Task 8: 准 PDF 单圈匹配核的分支结构

**Files:**
- Modify: `tests/test_myqcd_sympy.py`
- Modify: `myqcd/derivations.py`
- Modify: `myqcd/__init__.py`
- Modify: `myqcd/formula_registry.py`
- Modify: `myqcd/README.md`

**Interfaces:**
- Produces `derive_quasi_pdf_one_loop_matching_kernel() -> DerivationResult`。
- Equation keys include `Z_one_loop_piecewise`, `outer_branch`, `inner_branch`, `negative_branch`, `delta_endpoint_integrand`, `tree_limit`, `log_argument_checks`, `dimensionless_argument_residual`。

- [ ] 写测试，断言三个 ξ 分支还原源文的对数结构，所有分支对数真数在各自物理区间为正，且 `alpha_s→0` 后匹配核退化为 `DiracDelta(xi-1)`。
- [ ] 运行专项测试确认入口缺失导致失败。
- [ ] 实现分段 `Piecewise`、端点 `DiracDelta` 形式和 `xi=y/x`、`p_z a`、`mu/p_z` 的无量纲检查；不执行未定义区间边界和 plus 分布的广义积分。
- [ ] 运行专项测试、全量 pytest 和核心审计。

### Task 5: 收尾复查

**Files:**
- Read: 本计划、改动文件、相关来源行和测试输出

- [ ] `git diff --check` 与 `git diff --stat`，确认无 `refer/papers` 改动、无冲突标记和无调试残留。
- [ ] 核对四个新入口均出现在导出、注册表和 `run_core_checks()` 中，来源路径存在于当前工作区。
- [ ] 用新鲜命令复跑专项测试、全量 pytest、compileall 和 `python -m myqcd`；只按实际输出报告已验证项与未验证项。

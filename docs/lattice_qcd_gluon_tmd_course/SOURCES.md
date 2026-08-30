# 来源注册表

本表区分课程自编补足、仓库 book/doc/code/skill 和完整论文原文。Pxx 的页级引用见论文图谱中的 Pxx-pyyy。

## 教材、讲义、代码与技能

| ID | 来源 | 定位 | 用途 |
|---|---|---|---|
| BOOK-EM | 规范势与经典场预备课（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | Abelian 场强与规范冗余。 |
| BOOK-GROUP | 连续群与生成元预备课（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | 从旋转群过渡到 SU(2)/SU(3)。 |
| BOOK-LINALG | 线性代数预备课（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | 向量、谱分解、张量指标和矩阵数值检查。 |
| BOOK-LQCD | Introduction to Lattice QCD / 格点 QCD 导论（仓库转排本） | ../PyQCD/refer/books/INTRODUCTION_TO_LATTICE_QCD_latex/；../PyQCD/refer/books/格点QCD导论_latex/ | 欧氏化、规范链接、费米子、连续极限和关联函数。 |
| BOOK-MATH | 数学预备课（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | 补足高中到微积分、Fourier 和量纲分析的完整推导。 |
| BOOK-MECHANICS | 作用量与经典力学预备课（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | 变分、Euler--Lagrange 与 Noether 思想。 |
| BOOK-NUMERICS | 数值分析预备课（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | 差分、求积、收敛阶、线性求解和误差账本。 |
| BOOK-QCD-LATTICE | Quantum Chromodynamics on the Lattice（仓库转排本） | ../PyQCD/refer/books/Quantum_Chromodynamics_on_the_Lattice_latex/ | 格点 QCD 形式体系、算法和系统误差的深入交叉核验。 |
| BOOK-QFT | An Introduction to Quantum Field Theory（仓库转排本） | ../PyQCD/refer/books/An_Introduction_to_Quantum_Field_Theory_latex/ | 量子场论、规范理论、QCD 和重整化的主教材交叉核验。 |
| BOOK-QM | 量子力学预备课（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | 态、算符、测量、谱与不确定关系。 |
| BOOK-STAT | Monte Carlo 统计与拟合讲义（课程自编） | docs/lattice_qcd_gluon_tmd_course/content/ | 协方差、重采样、覆盖率和模型系统学。 |
| DOC-3PT | 格点 QCD 中的三点函数构造 | ../PyQCD/docs/格点QCD中的3pt构造.tex | 核子三点函数、谱分解和代码接口。 |
| DOC-DGLAP | 格点 QCD 中的 DGLAP 演化 | ../PyQCD/docs/格点QCD中的DGLAP演化方程.tex | 部分子演化与卷积。 |
| DOC-DISCONNECTED | 连通图与非连通图 | ../PyQCD/docs/格点QCD中的连通图与非连通图.tex | 断连拓扑与真空扣除。 |
| DOC-EXTRAPOLATION | 格点 QCD 中的外推 | ../PyQCD/docs/格点QCD中的外推.tex | 连续、有限体积和物理点外推。 |
| DOC-FERMIONS | 格点费米子方案 | ../PyQCD/docs/格点QCD中的费米子方案.tex | 倍增、Wilson/Clover 与方案比较。 |
| DOC-FIELD-STRENGTH | 格点场强张量 | ../PyQCD/docs/格点QCD中的场强张量.tex | plaquette/clover 场强和约定。 |
| DOC-GLUON-POLARIZATION | 胶子极化 | ../PyQCD/docs/格点QCD中的胶子极化.tex | 胶子张量投影。 |
| DOC-OPE | 格点 QCD 中的 OPE 算符 | ../PyQCD/docs/格点QCD中的OPE算符.tex | 局域矩、twist 与算符基底。 |
| DOC-PDF | 部分子分布函数讲义 | ../PyQCD/docs/格点QCD中的部分子分布函数.tex | PDF 定义、矩与因子化。 |
| DOC-SYMANZIK | Symanzik 有效理论 | ../PyQCD/docs/格点QCD中的Symanzik有效理论.tex | 按格距幂次组织离散伪影。 |
| DOC-TMD | 格点 QCD 中的 TMD-PDF | ../PyQCD/docs/格点QCD中的TMD_PDF.tex | TMD、soft、rapidity 与冲击参数定义。 |
| LQCDDB | lqcddb distillation 与谱学技能 | ../PyQCD/skills/sush/lqcddb/SKILL.md | distillation、perambulator、GEVP、多强子缩并与独立审计边界。 |
| MYQCD-COURSE-EXAMPLES | 课程配套 SymPy 代码参考 | docs/lattice_qcd_gluon_tmd_course/myqcd/ | 群论/QFT、格点谱学、重整化与 TMD 的 26 个可运行教学例题。 |
| MYQCD-FORMULAS | MyQCD 可执行公式注册表 | myqcd/formula_registry.py；myqcd/derivations.py；tests/test_myqcd_sympy.py | 复杂公式的 SymPy 精确代理与证据边界。 |
| PYQCD-ANALYSIS | PyQCD 分析技能与模块 | ../PyQCD/skills/pyqcd-analysis/SKILL.md；../PyQCD/pyqcd/analysis/ | 断连、比值、多态拟合和图表。 |
| PYQCD-CONVENTIONS | PyQCD 共享约定技能 | ../PyQCD/skills/pyqcd-conventions/SKILL.md | gamma、轴顺序、精度和接口约定。 |
| PYQCD-CORRELATOR | PyQCD 关联函数技能 | ../PyQCD/skills/pyqcd-physics-correlator/SKILL.md | 强子二点/三点与谱学检查。 |
| PYQCD-DOCS | PyQCD 中文文档技能 | ../PyQCD/skills/pyqcd-docs/SKILL.md | 来源追溯、XeLaTeX 日志与逐页 PDF 验收。 |
| PYQCD-GAUGE | PyQCD 规范场技能 | ../PyQCD/skills/pyqcd-gauge/SKILL.md | 链接、plaquette、flow 和规范不变量。 |
| PYQCD-INFRA | PyQCD 基础设施技能 | ../PyQCD/skills/pyqcd-infra/SKILL.md | 后端、I/O、MPI 和资源治理。 |
| PYQCD-PIPELINE | PyQCD 流水线技能 | ../PyQCD/skills/pyqcd-pipeline/SKILL.md | 配置、守卫、元数据、断点续跑和产物清单。 |
| PYQCD-PROPAGATOR | PyQCD 传播子技能 | ../PyQCD/skills/pyqcd-propagator/SKILL.md | 线性求解、序贯源和传播子契约。 |
| PYQCD-SPECTRUM | PyQCD 谱学技能 | ../PyQCD/skills/pyqcd-physics-spectrum/SKILL.md | 谱分解、边界项、GEVP 与能级指认。 |
| PYQCD-STATISTICS | PyQCD 统计技能 | ../PyQCD/skills/pyqcd-statistics/SKILL.md | 自相关、重采样、协方差和拟合验证。 |
| PYQCD-TMD | PyQCD TMD 主链技能 | ../PyQCD/skills/pyqcd-tmd-chain/SKILL.md；../PyQCD/skills/pyqcd-tmd-algorithm/SKILL.md | 六阶段 TMD 物理链和端到端接口。 |
| PYQCD-TMD-GEOMETRY | PyQCD TMD 几何规范 | ../PyQCD/skills/pyqcd-tmd-algorithm/references/geometry.md | 非零 bT、finite staple、端点和路径签名。 |
| PYQCD-TMD-RENORM | PyQCD TMD 重整化规范 | ../PyQCD/skills/pyqcd-tmd-algorithm/references/renormalization.md | soft、ZR、hybrid、CS 和匹配边界。 |
| PYQCD-TMD-VALIDATION | PyQCD TMD 验证矩阵 | ../PyQCD/skills/pyqcd-tmd-algorithm/references/validation.md | 合成闭合、故障注入和生产质量门。 |
| PYQCD-WICK | PyQCD Wick 收缩实现 | ../PyQCD/pyqcd/contraction/_autowick.py | Wick 拓扑、费米符号和张量收缩。 |
| REPORT-TMD | 梯度流核子胶子 TMD 项目报告 | docs/report_gluon_tmd_gradient_flow_20260828.pdf；docs/report_gluon_tmd_gradient_flow_20260828_2.pdf | 本课程终点定义、实现现状、证据分级和关键物理边界。 |
| SKILL-LQCD-COURSE | MyQCD 格点 QCD 长课程技能 | skills/lqcd-course/SKILL.md | 35 卷课程合同、同源构建、SymPy 与 PDF 全页验收。 |

## 论文 P01--P50

| ID | 中文题名 | arXiv | 完整原始 PDF | 原始页 | SHA-256 | 图谱页 ID |
|---|---|---|---|---:|---|---|
| P01 | 夸克禁闭 | DOI/Wilson74 | ../PyQCD/refer/books/Confinement of qnarks.pdf | 15 | `6eadfb8d3e3cd217c379623857c6e1ab31e7298edbfd2c18f7ea93d17b49582c` | P01-p001--P01-p015 |
| P02 | SU3链接变量解析涂抹 | hep-lat/0311018 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P02.pdf | 8 | `650d53c2fafb947ca9360075544f187b05fb0173a4d28d7c85a734813c4a0634` | P02-p001--P02-p008 |
| P03 | 夸克场产生算符构造 | 0905.2160 | ../PyQCD/refer/papers/A novel quark-field creation operator construction for hadronic physics in lattice QCD.pdf | 14 | `89a5838789847d4ca65d4fc031f496295472d3411dfeacc1f4a71c0f68581e91` | P03-p001--P03-p014 |
| P04 | 高动量强子新夸克涂抹 | 1602.05525 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P04.pdf | 17 | `f174c9940ab182375c1e6f4e2f7cfcac90c09bdf074d2bdb19ef2eba49a77d53` | P04-p001--P04-p017 |
| P05 | 平凡化映射威尔逊流与HMC | 0907.5491 | ../PyQCD/refer/papers/Trivializing_maps_the_Wilson_flow_and_the_HMC_algorithm_Luscher_2010.pdf | 29 | `3320b1d4caaa4e902831a602b1894129683d92146ac4fbfa31ed5b8014578710` | P05-p001--P05-p029 |
| P06 | 连续威尔逊圈的无穷N相变 | hep-th/0601210 | ../PyQCD/refer/papers/Infinite_N_phase_transitions_in_continuum_Wilson_loop_operators_Narayanan_Neuberger_2006.pdf | 31 | `5cc24d7c400d7fe60c366f302bfef1609ceae3a3ba7cd37b33e1453a278cccfc` | P06-p001--P06-p031 |
| P07 | 威尔逊流的性质与应用 | 1006.4518 | ../PyQCD/refer/papers/Properties_and_uses_of_the_Wilson_flow_in_lattice_QCD_Luscher_2010.pdf | 21 | `63426411712d8b00e7b4cb496cc38bb0ae5fd7ebee641840f45d4026e7f0afa0` | P07-p001--P07-p021 |
| P08 | 梯度流的微扰分析 | 1101.0963 | ../PyQCD/refer/papers/Perturbative_analysis_of_the_gradient_flow_in_non-abelian_gauge_theories_Luscher_Weisz_2011.pdf | 28 | `da3927cb38f6f864ed2c32b69762765f4e82c7e2c574992a6fb107931d56c3cd` | P08-p001--P08-p028 |
| P09 | 手征对称性与杨米尔斯梯度流 | 1302.5246 | ../PyQCD/refer/papers/Chiral_symmetry_and_the_Yang-Mills_gradient_flow_Luscher_2013.pdf | 49 | `e284d70671c4eec0b5ed3f1b29717e995fae6cc4974d84fe06f11d80a6179d65` | P09-p001--P09-p049 |
| P10 | 杨米尔斯梯度流提取能动量张量 | 1304.0533 | ../PyQCD/refer/papers/Energy-momentum_tensor_from_the_Yang-Mills_gradient_flow_Suzuki_2013.pdf | 17 | `5c92373f0319577d7324d5fd7327a8b7d51ec22b2ada60bd1e64b849cf884040` | P10-p001--P10-p017 |
| P11 | 欧氏格点上的部分子物理 | 1305.1539 | ../PyQCD/refer/papers/Parton Physics on Euclidean Lattice.pdf | 8 | `8a8877826d6fd23b6bb2a45590ed126081c8095689b5a818ceb793822dec8162` | P11-p001--P11-p008 |
| P12 | 大动量有效理论与部分子物理 | 1404.6680 | ../PyQCD/refer/papers/Parton Physics from Large-Momentum Effective Field Theory.pdf | 10 | `d852e74b8817d53bac007c964e17eeba3331ea14b3ce182f7f7a24ea42074255` | P12-p001--P12-p010 |
| P13 | 准部分子分布单圈匹配 | 1310.7471 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P13.pdf | 10 | `eb81ff0c120f7fff4cc505bd291a158f7d64d9f8f644cb79a3843b4f22ae856a` | P13-p001--P13-p010 |
| P14 | 大动量有效理论再论 | 1706.07416 | ../PyQCD/refer/papers/More On Large-Momentum Effective Theory Approach to Parton Physics.pdf | 12 | `fdc102ad02bd3cc559e6b00670e1e917864f9f7091d21e5f2bef84a0730182a5` | P14-p001--P14-p012 |
| P15 | 准分布动量分布与伪分布 | 1705.01488 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P15.pdf | 6 | `a76dcf322909d2694e119de29491c89e75602414036ac5bb567c8edfaffc7f1b` | P15-p001--P15-p006 |
| P16 | 部分子伪分布的格点探索 | 1706.05373 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P16.pdf | 12 | `12401554a993d92d87d3fd0e21fbf83b502bf86db393c469ae2c942dbea75daa` | P16-p001--P16-p012 |
| P17 | 欧氏与光锥分布因子化定理 | 1801.03917 | ../PyQCD/refer/papers/Factorization Theorem Relating Euclidean and Light-Cone Parton Distributions.pdf | 21 | `c5398a1bd179b053bd8829efbc2747bf1d817ddb08331a894c1c33d8153a5749` | P17-p001--P17-p021 |
| P18 | 大动量有效理论综述 | 2004.03543 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P18.pdf | 75 | `bfcdc7b4100d0da21aa34f2bbe070d1c43994dff0e56c251e465955d2d79700f` | P18-p001--P18-p075 |
| P19 | 格点算符非微扰重正化一般方法 | hep-lat/9411010 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P19.pdf | 41 | `413c5263159d9dbf1b99df7f19e3717a77b27f78082a12a1b4f876aafee2a243` | P19-p001--P19-p041 |
| P20 | 准部分子分布的可重正性 | 1707.03107 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P20.pdf | 11 | `ec49d7b2ca691de65f716bfc7649e72fcb286da42831f18cfa3c221ded4f053c` | P20-p001--P20-p011 |
| P21 | 威尔逊线重正化改进准分布 | 1609.08102 | ../PyQCD/refer/papers/Improved quasi parton distribution through Wilson line renormalization.pdf | 9 | `722b1a13447fe16be64e992a9b7df0c05307058c4e0857506cdc599a23386ac8` | P21-p001--P21-p009 |
| P22 | 大动量有效理论的重正化 | 1706.08962 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P22.pdf | 5 | `7a288164a4f20121cc75585733e8e3c04b4ec542b8f1cd87c4c016593fd371c2` | P22-p001--P22-p005 |
| P23 | 非定域夸克双线性的非微扰重正化 | 1707.07152 | docs/lattice_qcd_gluon_tmd_course/paper_cache/P23.pdf | 6 | `71cc84a9fecb09fd046d5ef2d2488718bb79d9eb55316b87f92c6cfef23f044c` | P23-p001--P23-p006 |
| P24 | 准PDF完整非微扰重正化方案 | 1706.00265 | ../PyQCD/refer/papers/A complete non-perturbative renormalization prescription for quasi-PDFs.pdf | 24 | `aa8daa6632b2cc37e91edd28b1e004a2f92d4c7df3648eae576a9720a07200c8` | P24-p001--P24-p024 |
| P25 | 准部分子算符乘法可重正性 | 1809.01836 | ../PyQCD/refer/papers/Multiplicative renormalizability of quasi-parton operators.pdf | 7 | `90299e0614e9fbab4759dcc6797df2813f41fb880c5f1bd09a6551284116e478` | P25-p001--P25-p007 |
| P26 | 大动量有效理论获取胶子分布 | 1808.10824 | ../PyQCD/refer/papers/Accessing gluon parton distributions in large momentum effective theory.pdf | 5 | `51ef82db68b39777391e30c68038ccf91501a87653d92317604acefa716a2824` | P26-p001--P26-p005 |
| P27 | 胶子伪分布的短距行为 | 1910.13963 | ../PyQCD/refer/papers/Gluon Pseudo-Distributions at Short Distances Forward Case.pdf | 10 | `616f7927c036d3115011887895ec0940d40beb3fc6477c6a41c40f97f5f2bdf1` | P27-p001--P27-p010 |
| P28 | 准部分子分布与梯度流 | 1612.01584 | ../PyQCD/refer/papers/Quasi_parton_distributions_and_the_gradient_flow_Monahan_Orginos_2017.pdf | 15 | `df4b2d5a4f3e1ce7f352f38fc809997aa5a3c04447d715431913877879b7a2fe` | P28-p001--P28-p015 |
| P29 | 准光前关联函数的自重正化 | 2103.02965 | ../PyQCD/refer/papers/Self-Renormalization of Quasi-Light-Front Correlators on the Lattice.pdf | 29 | `1474d215f0d5e7c07938e721d7350a641ff0c7bf52c473dbfa83d7716c4c0f3c` | P29-p001--P29-p029 |
| P30 | 准光前关联的混合重正化方案 | 2008.03886 | ../PyQCD/refer/papers/A Hybrid Renormalization Scheme for Quasi Light-Front Correlations in Large-Momentum Effective Theory.pdf | 40 | `56f633040d3bcd07a8bf3c39310d6adb32c1b12b92640121ef33e8d9eff3dc28` | P30-p001--P30-p040 |
| P31 | CT18全局分析 | 1912.10053 | ../PyQCD/refer/papers/New CTEQ global analysis of quantum chromodynamics with high-precision data from the LHC.pdf | 116 | `98d4b253c3c926d543f053b1e849cc7ff3fad76facc47fb52761cb2640406fd3` | P31-p001--P31-p116 |
| P32 | NNPDF17高精度数据部分子分布 | 1706.00428 | ../PyQCD/refer/papers/Parton distributions from high-precision collider data.pdf | 103 | `9d3daadd61fc48bc43c0e93ff49f31246ff7af605d5def547eadece519294e35` | P32-p001--P32-p103 |
| P33 | 基于流的格点MCMC生成模型 | 1904.12072 | ../PyQCD/refer/papers/Flow-based generative models for Markov chain Monte Carlo in lattice field theory.pdf | 13 | `61749019a775a8141842ce23b4dce5678a3f712f311dfcc379747b943ccbe07d` | P33-p001--P33-p013 |
| P34 | 规范等变的流采样 | 2003.06413 | ../PyQCD/refer/papers/Equivariant flow-based sampling for lattice gauge theory.pdf | 6 | `6f5d0bb1effda44b3fcb55d40ba679495428944a8988c71c61e7ccf19258d1f4` | P34-p001--P34-p006 |
| P35 | 含费米子场的格点能动量张量 | 1403.4772 | ../PyQCD/refer/papers/Lattice_energy-momentum_tensor_from_gradient_flow_inclusion_of_fermion_fields_Makino_Suzuki_2014.pdf | 32 | `decefa1e7bf7e32a1ad77b55bdbbfb59a788b4e5cbd1e7196da5db8d2a92fcf6` | P35-p001--P35-p032 |
| P36 | 梯度流形式的双圈能动量张量 | 1808.09837 | ../PyQCD/refer/papers/Two-loop_energy-momentum_tensor_within_gradient-flow_formalism_Harlander_Kluth_Lange_2018.pdf | 24 | `b2059573143a27c826f101f22292c5e31459a0205b61cd5d45267a4a4492538f` | P36-p001--P36-p024 |
| P37 | 梯度流高阶计算的技术与结果 | 1905.00882 | ../PyQCD/refer/papers/Results_and_techniques_for_higher_order_calculations_within_gradient-flow_Artz_et_al_2019.pdf | 42 | `361dd002d310eb7148d491f60a0980c7d2e1011c5afa5394d7cfc704cb42215c` | P37-p001--P37-p042 |
| P38 | 局域涂抹算符乘积展开 | 1501.05348 | ../PyQCD/refer/papers/Locally_smeared_operator_product_expansions_in_scalar_field_theory_Monahan_Orginos_2015.pdf | 12 | `f16003f5503a6fce3914705652867adbb6e2d5459dabe542eda1ac27a0d96c96` | P38-p001--P38-p012 |
| P39 | 微扰论中的涂抹准分布 | 1710.04607 | ../PyQCD/refer/papers/Smeared_quasidistributions_in_perturbation_theory_Monahan_2018.pdf | 12 | `dcf036dda58e10f4b01e99bf0f81cff5a7ca2fc9e2a113a31fdb9bde87d8c1d9` | P39-p001--P39-p012 |
| P40 | 梯度流中的非光锥威尔逊线算符 | 2312.05032 | ../PyQCD/refer/papers/Off-lightcone_Wilson-line_operators_in_gradient_flow.pdf | 31 | `31292da5c276c237936e3c5f2a326fa1c862fb3ecf1583efbb65af4bf703519f` | P40-p001--P40-p031 |
| P41 | 首个核子胶子部分子分布 | 2505.13321 | ../PyQCD/refer/papers/First Nucleon Gluon PDF from Large Momentum Effective Theory.pdf | 10 | `09eff6064b5d9c6733e28067bb62936e3b822d428b149bab04e6af0a8faf519f` | P41-p001--P41-p010 |
| P42 | π介子胶子部分子分布 | 2104.06372 | ../PyQCD/refer/papers/Gluon Parton Distribution of the Pion from Lattice QCD.pdf | 10 | `9c567ec3e62b200911894e98229ef3d49379e157e3325caa368eca3e5bcfe0ed` | P42-p001--P42-p010 |
| P43 | K介子胶子分布初探 | 2112.03124 | ../PyQCD/refer/papers/First Glimpse into the Kaon Gluon Parton Distribution Using Lattice QCD.pdf | 8 | `e1aeac0db815750f376b21700c968aa8e3e29e5307cd9b8e24ad73303f698c93` | P43-p001--P43-p008 |
| P44 | 从准TMD波函数确定CS核 | 2204.00200 | ../PyQCD/refer/papers/Nonperturbative Determination of Collins-Soper Kernel from Quasi Transverse-Momentum Dependent Wave Functions.pdf | 17 | `589d870d484889ae7123d38ce062558dc2261dabba80f765bbeffb9af2b30af8` | P44-p001--P44-p017 |
| P45 | LaMET计算TMD软函数 | 2005.14572 | ../PyQCD/refer/papers/Lattice-QCD Calculations of TMD Soft Function Through Large-Momentum Effective Theory.pdf | 12 | `22b1f2cbca968f3066e4614069e1d2bcfe6c01333cf7e96c606e935c3d442b2b` | P45-p001--P45-p012 |
| P46 | 扩散模型即随机量化 | 2309.17082 | ../PyQCD/refer/papers/Diffusion Models as Stochastic Quantization in Lattice Field Theory.pdf | 31 | `3c6e52dcbf2a73118d59cb87490bb843ddbebce1e46c73b93f68caa144f242bc` | P46-p001--P46-p031 |
| P47 | 任意阶部分子分布矩 | 2311.18704 | ../PyQCD/refer/papers/Moments_of_parton_distribution_functions_of_any_order_from_lattice_QCD.pdf | 10 | `d72b64fbca3ac2d36f3dd92dc8e6e181d239e8ebddb9e7b76c65a52c43a1c17b` | P47-p001--P47-p010 |
| P48 | 准分布的幂修正与renormalon | 1810.00048 | ../PyQCD/refer/papers/Power corrections and renormalons in parton quasi-distributions.pdf | 14 | `978bb7d735bfed7704a3ba8364162cee7c9931e17d2d70c871e44cc83b2b14cb` | P48-p001--P48-p014 |
| P49 | 伪部分子分布的单圈演化 | 1801.02427 | ../PyQCD/refer/papers/One-loop evolution of parton pseudo-distribution functions on the lattice.pdf | 10 | `79c2772567b5119ce91d569d23a60bf2638aa28cd16d0e817a4694291ca84147` | P49-p001--P49-p010 |
| P50 | 同位旋矢量分布的重正化匹配系统分析 | 1807.06566 | ../PyQCD/refer/papers/Unpolarized isovector quark distribution function from Lattice QCD A systematic analysis of renormalization and matching.pdf | 17 | `460780f4eed9a77e9a5b8b7ca740de713a3ea8c8af9138121f164a0a8dde8022` | P50-p001--P50-p017 |

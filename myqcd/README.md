# `myqcd`：SymPy 公式复现与来源审计

本目录对应 `docs/report_refer_papers_all_contents_20260830.tex` 的公式层，
采用“可执行推导 + 全源公式索引”的证据边界：

1. `derivations.py` 用 SymPy 检查生成泛函高斯类比、格点链接变量、Wilson
   面积律、梯度流线性化、乘法重正化、Mellin 卷积、LaMET 幂修正、伪 ITD
   Fourier/矩/约化比值、靶质量修正、qPDF/pPDF Fourier 反演、stout SU(2)
   子群涂抹、Langevin--Fokker--Planck 平衡、热核半群、梯度流极点抵消、
   规范场横向/纵向投影热核、PDF/反 PDF 矩恒等式和靶质量多项式、
   方差扩张扩散过程、Gaussian 分数匹配投影、概率流 ODE/Jacobian、
   场流 Jacobian、标量 HMC、伪 PDF 红外 Bessel/Gamma 调节、TMD Fourier 变换、
	   normalizing flow Jacobian、梯度流树级传播子、流 MCMC 平衡/KL 恒等式、φ⁴ 格点作用量/观测量、
	   TMD 到 quasi-PDF 的 Gaussian 横向积分、夸克 Gaussian/Jacobi 涂抹与蒸馏投影、
   U(1) plaquette 规范不变性、离散场强规范平移抵消、拓扑荷与紧致作用量弱场展开、SU(3) 生成元代数与完备性、SU(3) Cayley--Hamilton 特征多项式、CT18 相关误差剖面化、Ising 平均场自洽方程、APE 极化投影、Wilson 圈本征值统计/边缘标定/Fourier 端点/连续统尺度、二维 QCD Wilson 圈 Laguerre 公式、瞬子 SU(2) holonomy、Grassmann 周期行列式、Wilson 圈能隙平方根/对数外推、Wilson/APE 涂抹横纵向投影核与连续统尺度换算、格点动量与自由色散极限、boost-smearing 宽度匹配、接受率—自相关下界、伪 PDF 单圈
   plus 分布核和欧氏关联函数谱提取；连续 Wilson 流的第五维记号、Abelian Fourier 流方程与作用量单调性、Wilson 圈边缘的 Painleve II/Airy 积分结构、Wilson 流三阶 Runge--Kutta 局部误差阶、梯度流 Duhamel 积分解、Wilson 流参考尺度与连续极限、格点 Wilson 流的群值单调性；欧拉流逆迭代与 Jacobian 链式分解、平凡化流因子化、梯度流圈积分 IBP 与尺度律、梯度流 RGE 对数递推/换方案、含费米子能动量张量算符基底、加圈费米子归一化和迹反常展开、纯 Yang--Mills 梯度流能动量张量小流时间反演。
   LaMET 综述的 DIS 壳条件与轻锥分解、GPD 非前向运动学边界和匹配测度、渐近 pion DA 归一化/Fourier 矩、TMD 软因子 RGE 与 Collins--Soper 解、辅助场 Wilson 线指数重整化与混合代数、RI/MOM—比值方案的 UV 抵消、混合重整化的切换点连续性、quasi-TMD 乘法因子化与硬因子修正的 CS 核提取、准 TMD 一圈硬核的 $i\epsilon$ 共轭结构、RI-xMOM 条件解法、Wilson 线自能线性反项、已去除线性反项的准 PDF 单圈匹配核，以及保留有限动量线性项的原始准 PDF 单圈核也分别在 `lamet_lightcone_kinematics`、`gpd_kinematics_and_matching`、`pion_da_normalization`、`tmd_soft_rge_consistency`、`auxiliary_field_wilson_renormalization`、`ri_mom_ratio_renormalization`、`hybrid_renormalization`、`quasi_tmd_matching_and_cs_kernel`、`quasi_tmd_hard_kernel_i_epsilon`、`ri_xmom_renormalization_conditions`、`wilson_line_linear_counterterm`、`quasi_pdf_one_loop_matching_kernel` 和 `quasi_pdf_finite_momentum_one_loop_matching_kernel` 中复现。
   其中 `hybrid_momentum_matching_kernel` 复现混合方案动量空间匹配核的
   plus 分布与正弦积分项，并保留其未计算一般广义函数积分的验证边界。
   `twist2_flowed_moment_matching` 复现任意阶 twist-2 矩的带流匹配、
   单圈有限系数与 RG 重求和结构；费曼积分和非微扰矩阵元仍未计算。
   `euclidean_lightcone_factorization` 复现欧氏—光锥因子化定理中
   gamma^z 的单圈支持修正、有限区间 plus 分布定义，以及无穷远端点在
   可积 PDF 幂律下的消失极限；不重新计算完整费曼积分和匹配核。
2. `formula_registry.py` 给出报告结构公式的 LaTeX、来源行号、推导入口和
   假设。`structural` 表示原式是跨论文结构接口，不能替代某篇论文的特定
   方案或匹配系数。
3. `latex_inventory.py` 扫描 `refer/papers/INDEX.md` 列出的 50 个中文论文
   目录，保留每个显示公式的源文件、起止行、环境和原文正文；不扫描
   `build/`。`unparsed` 是诚实的未语义化标记，不是对原文正确性的否定。

运行核心检查和索引统计：

```bash
python -m myqcd
```

若需要逐条 JSON 清单，显式指定输出路径：

```bash
python -m myqcd --inventory-json /tmp/myqcd_formula_inventory.json
```

这里的“验证”只覆盖代码中写出的假设和模型。非阿贝尔指标收缩、特定
重正化方案、完整一圈/多圈匹配核、格点数据和论文数值结果没有被自动猜测；
它们会留在来源索引中，不能被本目录的核心检查替代。随机量化的标量例子还
明确区分漂移 `-delta S` 对应的单位温度目标 `exp(-S)` 与一般噪声强度
`2 alpha` 产生的平衡权重 `exp(-S/alpha)`。

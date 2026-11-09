# MyQCD（中文）

[English](https://gitlab.itp.ac.cn/zhangxin8069/MyQCD/-/blob/main/README.md) | **中文**

MyQCD 为 PyQCD 使用的格点 QCD 公式提供可执行审计。它把物理报告拆成
SymPy 可检查推导、来源注册表，以及独立的算符构建与费曼图层。参考库以只读
Git 子模块引入；GPL-3.0 或无许可证的上游内容一律不复制。

## 安装

```bash
pip install myqcd
```

依赖：Python 3.10+ 与 SymPy 1.12+。完整测试套件当前在 Python 3.12 +
SymPy 1.14 上执行。

无需源码检出即可检查安装：

```bash
python -m myqcd.operator_audit
python -m myqcd
```

`python -m myqcd` 执行核心公式检查。缺少 `refer/papers/INDEX.md` 时会跳过论文
清单并报告 `verified_core_without_inventory`；核心检查仍然执行。

## 文档

* English — https://myqcd.readthedocs.io/en/latest/
* 中文 — https://myqcd.readthedocs.io/zh-cn/latest/

## 代码托管

| 平台 | 用途 | 地址 |
|---|---|---|
| GitLab（gitlab.itp.ac.cn） | 国内开发——主开发仓库 | https://gitlab.itp.ac.cn/zhangxin8069/MyQCD |
| Gitee | 国内发布——国内镜像 | https://gitee.com/zhangxin8069/MyQCD |
| GitHub | 国外发布——海外镜像 | https://github.com/zhangxin8069/MyQCD |

## 快速开始

```python
import sympy as sp

from myqcd import color, diagram_export, feynman, gamma, operators

assert gamma.gamma_basis_rank() == 16
assert gamma.trace_gamma_product((1, 1)) == 4
assert color.casimir_fundamental() == sp.Rational(4, 3)

operator = operators.BilinearOperator(
    name="O_V4", left_flavor="u", right_flavor="d", structure="V4"
)
assert operator.pyqcd_gamma_index == 4
assert operator.mass_dimension == 3

triangle = feynman.Diagram(
    vertices=("a", "b", "c"),
    edges=(
        feynman.Edge(0, 1, "gluon"),
        feynman.Edge(1, 2, "gluon"),
        feynman.Edge(2, 0, "gluon"),
    ),
)
assert triangle.loop_count == 1
assert diagram_export.to_tikz(triangle).startswith("%")
```

## 算符与费曼图

`myqcd` 提供全部 16 个 Dirac 双线性，并给出精确的宇称/C 符号、质量量纲与
PyQCD gamma 索引：

| 类别 | 结构 | 数量 |
|---|---|---|
| S | `I` | 1 |
| P | `γ₅` | 1 |
| V | `γμ` | 4 |
| A | `γμγ₅` | 4 |
| T | `σμν` | 6 |

完整表格及与标准 Dirac/SU(3) 值的逐项对照见
[算符](https://myqcd.readthedocs.io/zh-cn/latest/operators.html)。文档站用
LaTeX 渲染同一组公式。

![Sunset 两圈图](https://myqcd.readthedocs.io/zh-cn/latest/_images/sunset_two_loop.svg)

两点链图、三胶子三角图、单圈夸克自能、两圈 sunset 与 Wick 配对图的圈数，
以及 TikZ/DOT/SVG 导出见
[费曼图](https://myqcd.readthedocs.io/zh-cn/latest/diagrams.html)。

## 包内有什么

| 模块 | 内容 |
|---|---|
| `myqcd.audit` | 核心公式检查、论文清单与 JSON 报告 |
| `myqcd.pyqcd_theory_audit` | PyQCD 的 gamma、顶点、Wilson 线、Clover、ratio 与 TMD 边界审计 |
| `myqcd.derivations` | 格点规范场、梯度流、LaMET、PDF/TMD 与统计的 SymPy 推导 |
| `myqcd.formula_registry` | 公式到来源与推导入口的注册表 |
| `myqcd.latex_inventory` | 论文源文件的显示公式清单 |
| `myqcd.wick` | 精确味道 Wick 配对与 Grassmann 符号 |
| `myqcd.gamma` | DeGrand--Rossi gamma 基、迹定理与 16 个 Dirac 结构 |
| `myqcd.color` | SU(3) 生成元、结构常数、Casimir 与颜色 Fierz 恒等式 |
| `myqcd.color_traces` | SU(3) 迹、f/d 缩并与通用 Casimir 公式 |
| `myqcd.gamma_traces` | γ5 迹、epsilon 对应与手征投影迹 |
| `myqcd.operators` | Dirac 双线性分解、宇称/C 分类与 PyQCD 索引映射 |
| `myqcd.lorentz` | Euclidean epsilon 缩并、Schouten 恒等式、横向与 spin-2 投影 |
| `myqcd.fierz` | 16 基通用 Dirac Fierz 变换与精确系数 |
| `myqcd.operator_basis` | 导数算符、手征组合、颜色表示与算符表 |
| `myqcd.qcd_rules` | 符号 QCD 传播子、Ward 恒等式、顶点因子与量纲 |
| `myqcd.renormalization` | RI/MOM 投影器、Z 因子与混合矩阵代数 |
| `myqcd.wilson` | 符号 Wilson 路径乘积与规范协变检查 |
| `myqcd.matching` | 树级匹配、Fourier 前因子与 hybrid 开关 |
| `myqcd.evolution` | 单指数 RGE 演化与反常维度 |
| `myqcd.symmetry` | 顶点自同构与平行边交换计数 |
| `myqcd.lattice` | 格点动量、Fourier 相位与色散关系 |
| `myqcd.statistics` | Jackknife、bootstrap 与有效质量估计 |
| `myqcd.feynman` | 图结构、QCD 规则清单、Wick 配对图与圈数 |
| `myqcd.topology` | 图不变量、同构、拓扑枚举与构造器 |
| `myqcd.diagram_export` | 零依赖 JSON、Mermaid、LaTeX、TikZ、DOT 与 SVG 导出 |
| `myqcd.operator_audit` | 算符层与图层的一键审计 |

## 入口

```bash
python -m myqcd
python -m myqcd.operator_audit --root .
python -m myqcd.pyqcd_theory_audit --root .
```

`python -m myqcd.operator_audit` 在当前目录写出
`logs/data/operator_audit/operator_feynman_audit.json`；任一检查失败时返回非零
退出码。

## 证据边界

- `verified` 只覆盖实际检查过的代数、量纲、有限维代理与组合恒等式。
- 不声称完成圈积分、非微扰矩阵元、真实系综、GPU 数值、soft/rapidity 闭环
  或连续极限。
- `myqcd.color` 使用厄米归一化 `Tr[T^aT^b] = +delta^{ab}/2`；`myqcd.derivations`
  中的历史 SU(3) 推导使用反厄米 `-delta^{ab}/2`。两套约定不可混用。
- 费曼图导出只保证组合结构与字符串格式，不证明具体图的对称因子或圈积分结果。

## 许可

MIT。见 `LICENSE`。

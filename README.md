# MyQCD

MyQCD 是 PyQCD 格点 QCD 物理的可执行公式审计库：把报告中的结构公式拆成
SymPy 可检查推导、来源索引与独立的算符/费曼图层。它不复制上游 GPL 或无许可证
源码，所有新实现均以数学恒等式与精确代数测试为证据。

## 安装

```bash
pip install myqcd
```

唯一运行依赖是 `sympy`。Python 3.10 及以上可用；当前完整测试在 Python 3.12
（SymPy 1.14）上执行。

## 能力

| 模块 | 作用 |
|---|---|
| `myqcd.audit` | 核心公式检查、论文显示公式索引与 JSON 报告 |
| `myqcd.pyqcd_theory_audit` | PyQCD 的 gamma、顶点、Wilson 线、Clover、Jackknife、ratio、混合方案与量纲审计 |
| `myqcd.derivations` | 格点规范场、梯度流、LaMET、PDF/TMD、重正化与统计的 SymPy 推导 |
| `myqcd.formula_registry` | 公式到报告、来源行号与推导入口的注册表 |
| `myqcd.latex_inventory` | 论文 LaTeX 显示公式清单 |
| `myqcd.wick` | 精确味道 Wick 配对与 Grassmann 重排符号 |
| `myqcd.gamma` | PyQCD DeGrand--Rossi gamma 基、0..17 索引、迹定理、16 个 Dirac 基与 H/T/C 符号 |
| `myqcd.color` | SU(3) 生成元、结构常数、对称常数、Casimir 与颜色 Fierz 恒等式 |
| `myqcd.operators` | 16 个 Dirac 双线性结构、精确分解、宇称/C 分类、量纲与 PyQCD 索引映射 |
| `myqcd.feynman` | 费曼图数据结构、QCD 顶点/传播子规则清单、Wick 配对图与圈数 |
| `myqcd.diagram_export` | 零依赖导出 TikZ-Feynman、Graphviz DOT 与 SVG |
| `myqcd.operator_audit` | 算符/图构建一键审计 |

## 入口

```bash
python -m myqcd
python -m myqcd.operator_audit --root .
python -m myqcd.pyqcd_theory_audit --root .
```

`python -m myqcd` 在源码仓库中会附加论文公式清单；缺少 `refer/papers/INDEX.md`
时自动跳过清单并以 `verified_core_without_inventory` 报告，核心检查仍然执行。
纯安装环境可直接运行 `python -m myqcd` 或 `python -m myqcd.operator_audit`。

## 证据边界

- `verified` 只表示写明的代数、量纲、有限维代理或组合恒等式通过。
- 不声称完成非阿贝尔圈积分、非微扰矩阵元、真实系综、GPU 数值、soft/rapidity
  闭环或连续极限。
- 颜色约定：`myqcd.color` 使用厄米归一化 `Tr[T^aT^b] = +δ^{ab}/2`；历史
  `derivations.py` 中的 SU(3) 推导使用反厄米 `-δ^{ab}/2`，两套约定不可混用。
- 费曼图导出只保证组合结构与字符串格式，不证明具体图的对称因子或圈积分结果。

## 仓库与文档

- 主仓库：<https://gitlab.itp.ac.cn/zhangxin8069/MyQCD>
- Gitee 镜像：<https://gitee.com/zhangxin8069/MyQCD>
- GitHub 镜像（由 Gitee 自动同步）：<https://github.com/zhangxin8069/MyQCD>
- 文档：<https://myqcd.readthedocs.io/>

外部参考库以只读 Git 子模块固定在 `refer/git-rep/`，来源、提交与许可证见
`docs/absorb_reference_libraries_20261109.md`。

## 许可

MIT。见 `LICENSE`。

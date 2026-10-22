# `myqcd`：PyQCD 物理公式审计

本包为 MyQCD 的物理说明提供可执行证据。它以
`refer/git-rep/PyQCD/` 的源码、文档和 `refer/` 参考为事实源，并用局部 LaTeX
转排提供可检索的公式上下文。

## 模块

| 模块 | 作用 |
|---|---|
| `pyqcd_theory_audit.py` | 审计 PyQCD 的 gamma/宇称、顶点、Wilson 线、Clover/对偶场强、Jackknife、3pt/2pt ratio、混合方案、梯度流量纲和 TMD 边界 |
| `derivations.py` | 用 SymPy 检查格点规范场、梯度流、LaMET、PDF/TMD、重正化、统计和格点 QFT 的代数代理 |
| `formula_registry.py` | 把结构公式绑定到 `docs/pyqcd_physics/report_pyqcd_lattice_qcd_theory_20260906.tex`、来源行号和推导入口 |
| `latex_inventory.py` | 扫描 `refer/papers/INDEX.md` 中的论文转排，建立显示公式的可追溯清单 |
| `wick.py` | 独立实现精确味道 Wick 配对，保留 Grassmann 重排符号，不复制上游代码 |
| `audit.py` | 命令行入口：核心公式检查、论文公式索引和可选 JSON 输出 |

## 入口

```bash
python -m myqcd
python -m pytest
python -m myqcd.pyqcd_theory_audit --root .
```

`python -m myqcd.pyqcd_theory_audit` 默认读取仓库内
`refer/git-rep/PyQCD/`，并输出
`logs/data/pyqcd_theory_audit/theory_audit.json`。若需审计另一份显式提供的
PyQCD 检出，使用 `--pyqcd-root <path>`；未显式提供时不会读取仓库外路径。

## 证据边界

- `verified` 只表示写明的代数、量纲、有限维代理或组合恒等式通过。
- `unparsed` 表示显示公式已经定位但尚未在不引入额外物理约定的情况下语义化。
- 非阿贝尔圈积分、非微扰矩阵元、真实系综、GPU 数值、soft/rapidity 闭环和连续极限
  必须由相应测试或运行证据单独验证。
- 论文转排用于公式追溯；接口、轴序、归一化和方案冲突时，以 PyQCD 源码及其同提交
  文档为准。

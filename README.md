# MyQCD

MyQCD 是一个面向
[`PyQCD`](refer/git-rep/PyQCD/README.md) 的格点 QCD 物理说明与可验证推导库。
它不复制或替代 PyQCD，而是解释 PyQCD 中的物理对象、公式、算法、数据流和证据边界，
重点覆盖 QCD、欧氏格点场论、强子关联函数、梯度流、胶子算符、重正化、匹配以及
核子胶子 TMD-PDF。

## 主入口

| 入口 | 内容 |
|---|---|
| [`docs/pyqcd_physics/README.md`](docs/pyqcd_physics/README.md) | 按物理链组织的总导航与阅读顺序 |
| [`docs/pyqcd_physics/report_pyqcd_lattice_qcd_theory_20260906.pdf`](docs/pyqcd_physics/report_pyqcd_lattice_qcd_theory_20260906.pdf) | PyQCD 物理理论审计：从规范组态、蒸馏和 Wick 收缩到 OPE、梯度流、准 PDF/TMD |
| [`docs/pyqcd_physics/report_gluon_tmd_gradient_flow_20260828.pdf`](docs/pyqcd_physics/report_gluon_tmd_gradient_flow_20260828.pdf) | 梯度流重整化核子胶子 `f_1^g` 的物理方案、实现路径与验证门 |
| [`myqcd/`](myqcd/README.md) | 可执行 SymPy 公式审计、论文公式索引和精确 Wick 配对 |
| [`refer/git-rep/docs/pyqcd-physics-reference.md`](refer/git-rep/docs/pyqcd-physics-reference.md) | `PyQCD/refer` 的只读参考入口与主题映射 |

## 物理主线

```text
格点规范场与 SU(3) 链接
  -> 蒸馏、传播子、Wick 收缩与强子关联函数
  -> 谱学、比值、断连图和重采样统计
  -> Clover 场强、Wilson line 与胶子 OPE/TMD 算符
  -> Wilson/gradient flow 与 UV 平滑
  -> Z_R、hybrid/self-renormalization 与 NLO matching
  -> quasi-PDF/quasi-TMD、Fourier、Collins-Soper 核
  -> 连续极限、系统误差与物理结果判定
```

## 源码与参考

- [`refer/git-rep/PyQCD/`](refer/git-rep/PyQCD/) 是唯一 PyQCD 源码事实源，作为 Git
  子模块只读使用。
- [`refer/git-rep/PyQCD/refer/`](refer/git-rep/PyQCD/refer/) 是 PyQCD 自带的书籍、论文、
  历史代码和外部软件参考。MyQCD 只建立索引，不修改或复制其中内容。
- `refer/papers/` 与 `refer/books/` 保存 MyQCD 用于公式追溯和定义核对的本地 LaTeX
  转排；它们承担检索与教学辅助，不覆盖 PyQCD 的源码约定。

## 验证入口

```bash
python -m pytest
python -m myqcd
/root/configure/skills/form/scripts/form-audit.sh --root /root/MyQCD --strict --quiet
```

## 证据边界

- SymPy 检查只证明写明的代数、量纲、极限和有限维代理，不替代非微扰 QCD、圈积分、
  真实系综或 GPU 数值验证。
- 报告中的“接口存在”“测试通过”“方案闭合”“真实数据验证”是四个独立证据级别。
- 缺少 finite staple、同几何 soft/rapidity 处理、胶子 singlet matching、联合极限和误差账本时，
  不得把中间关联函数称为完整核子胶子 TMD-PDF 结果。

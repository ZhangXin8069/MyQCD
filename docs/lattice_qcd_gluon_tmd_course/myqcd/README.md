# `myqcd/`：课程配套 SymPy 代码参考

本目录把课程中的代表性推导写成可以逐行运行、修改和复查的 SymPy 例题。读者不需要先掌握计算机代数；建议先在 PPT 中学完表中对应单元，再打开函数，对照“定义 → 中间式 → 检查 → 边界”阅读。

这里共有 26 个例题：

| 文件 | 稳定编号 | 内容 |
|---|---|---|
| `group_qft.py` | `MYQCD-GQ-01`--`06` | SU(2)、SU(3)、BCH、U(1) 规范不变性、生成泛函、横向投影 |
| `lattice_spectroscopy.py` | `MYQCD-SP-01`--`08` | 格点色散、有限时间关联函数、重子反宇称、有效能量、GEVP、Lüscher、有限温度、jackknife |
| `renormalization_tmd.py` | `MYQCD-RT-01`--`12` | 梯度流、Wilson 线反项、RI/MOM、比值、混合矩阵、soft、CS、Fourier、匹配、staple 与联合极限 |

## 运行

本项目约定使用 Conda 的 `qcu` 环境（Python 3.11、SymPy 1.14）。从仓库根目录执行：

```bash
conda run -n qcu python docs/lattice_qcd_gluon_tmd_course/myqcd/run_all.py
```

需要保存便于检索的完整记录时：

```bash
conda run -n qcu python docs/lattice_qcd_gluon_tmd_course/myqcd/run_all.py \
  --json docs/lattice_qcd_gluon_tmd_course/generated/myqcd_examples.json
```

也可以进入课程目录后按模块运行或导入：

```python
from myqcd.group_qft import su3_fundamental_representation

result = su3_fundamental_representation()
print(result.equations["sum_Ta2"])
print(result.checks)
print(result.boundary)
```

每个函数返回 `SymbolicExample`：

- `equations` 保存 SymPy 中间式，不只给最终真假值；
- `checks` 是可重复执行的精确恒等式、极限或有限维代理；
- `assumptions` 写明正性、边界条件、表示和近似；
- `boundary` 说明该程序不能证明什么；
- `course_refs` 与 PPT 单元编号互相跳转，`source_refs` 对应课程来源注册表。

## 证据边界

SymPy 可以可靠检查代数、微分、积分、级数、极限和小矩阵，但不能凭符号输出证明 QCD 的非微扰动力学。尤其要区分：

1. 热核半群成立，不等于离散 Wilson flow 已达到步长无关；
2. 指数反项相消，不等于 Wilson 线的有限部分、算符混合和匹配已经确定；
3. 除以 `sqrt(S_qsoft)` 的代数成立，不等于两条 Wilson 方向、rapidity regulator、zero-bin 与 quasi-to-standard 转换已经闭合；
4. 三动量线性代理能分离一个 `1/P_z²` 项，不等于真实的 `x,b_T,ell` 依赖、端点失效与统计相关性已受控；
5. Gaussian Fourier 变换是解析教学模型，不是核子胶子 TMD 数据。

课程全部 175 个单元的验收事实源仍是上一级 `sympy_validation.py`；本目录是可读、可改的教学参考，不维护第二份课程单元注册表。仓库根目录的 `myqcd/` 则服务于论文公式审计，两者职责不同。

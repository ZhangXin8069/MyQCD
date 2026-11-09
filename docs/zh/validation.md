# 验证

`myqcd` 区分精确代数、结构检查、发布元数据与数值格点证据。

## 证据等级

| 等级 | 含义 | 例子 |
|---|---|---|
| `verified` | 已执行精确代数/组合 | Clifford、Fierz、颜色迹 |
| `structural` | 在声明假设下的代数闭合 | hybrid 拼接、Fourier 前因子 |
| `inferred` | 由外部约定推导 | 极限代理 |
| `unverified` | 需要圈图、系综或连续极限 | TMD 软因子 |

## 命令

```bash
python -m myqcd.operator_audit
python -m myqcd.pyqcd_theory_audit --root .
python -m pytest
```

审计写出机器可读 JSON。测试套件当前 298 项通过；剩余 11 项失败是
`refer/papers` 环境数据缺失，不是代数回归。

## 发布门禁

- 只发 sdist；`twine check` PASSED。
- `myqcd/py.typed`、两个 README 与 `pyproject.toml` 已跟踪。
- 干净 venv 从 PyPI 安装；缺 `refer/papers/INDEX.md` 时
  `python -m myqcd` 必须优雅降级。
- Sphinx `-W` 双语构建；双语代码块逐字节一致。
- 双推 GitLab 与 Gitee；GitHub 跟随 Gitee 镜像。

## 不声称

圈积分、非微扰矩阵元、真实系综、GPU 数值、soft/rapidity 闭环、连续
极限外推和完整重正化拟合。

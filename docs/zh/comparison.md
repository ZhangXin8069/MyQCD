# 与参考库比对

| 项目 | 角色 | 许可 | `myqcd` 取用的内容 |
|---|---|---|---|
| PyQCD | 格点 QCD 数值包 | MIT | DR gamma 约定、算符命名 |
| FeynCalc | Mathematica gamma/颜色代数 | GPL-3.0 | 数学恒等式，仅参考 |
| LQCD_Wickcontraction_reduce | Wick 归约 | 无 LICENSE | 算法思想，仅参考 |
| pyfeyn2 | Python 费曼图 | GPL-3.0 | 渲染器接口思想，仅参考 |
| pyfeyngen | 粒子语法 -> TikZ | MIT | 导出工作流思想 |

`myqcd` 不复制 GPL-3.0 或无许可证源码。每个实现的恒等式都独立重写并测试；
外部仓库是只读子模块。

## 结构差异

- PyQCD 做数值张量收缩；`myqcd` 检查精确代数。
- FeynCalc 是 Mathematica 包；`myqcd` 是 Python/SymPy，算符/图层无额外依赖。
- pyfeyn2 有更丰富的自动布局；`myqcd` 提供零依赖子集与显式拓扑不变量。
- `myqcd` 有意省略圈积分与系综拟合。

## 兼容性说明

Gamma 符号与颜色归一化依赖约定。`myqcd.color` 层使用
$+\delta^{ab}/2$；历史 `myqcd.derivations` 的 SU(3) 代码使用
$-\delta^{ab}/2$。跨库数值对照必须先做基变换与归一化转换。

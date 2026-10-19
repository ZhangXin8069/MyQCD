# 外部 QCD 代码参考

本目录只保存上游 Git 仓库的子模块指针，不把第三方源码复制进 MyQCD 主包。

| 子模块 | 锁定提交 | 用途 | 上游许可 | 本库处理 |
| --- | --- | --- | --- | --- |
| `LQCD_Wickcontraction_reduce` | `1c996a86b778b33d6fd670f025b8074bd6798093` | 格点关联函数的 Wick 配对、颜色/Dirac 约化与输出验证 | 仓库当前未附 `LICENSE`、`COPYING` 或等效授权文本 | 只吸收可独立重写的算法思想；不从子模块复制代码 |
| `feyncalc` | `1ee480093293a01a82b3e365d026808f1d4e1c17` | Mathematica 中的 Dirac、Lorentz、SU(N) 与圈积分符号计算 | GPL-3.0-or-later | 保持为独立子模块；MIT 主包不复制其源码 |

## 版本说明

- `LQCD_Wickcontraction_reduce` 上游当前只有一个初始提交，且未声明该代码的许可证。
  MyQCD 的 MIT 许可证不能替第三方子模块补充授权；未获版权人明确许可前，只能引用
  接口、公式和测试思想，不能把实现搬入 MyQCD。
- `feyncalc` 的包元数据写 `10.2.1`，但锁定提交带有 `.testing` 标记，且晚于
  `Release-10_2_1` 标签。引用时必须写成“`10.2.1` 之后的开发快照”并附完整提交 SHA，
  不能简称为 FeynCalc 10.2.1。
- 两个子模块只锁定提交，不锁定远端分支。更新子模块前应先审查上游差异、许可证和测试结果。

## 使用边界

- MyQCD 的 `myqcd.wick` 是独立实现的精确味道配对枚举器，不导入或复制上述子模块。
- FeynCalc 的 Mathematica 测试需要本机 Wolfram Engine/Mathematica；当前环境没有相应运行时，
  因此不能把静态审计写成 FeynCalc 运行通过。
- 详细审计结论、复现证据和已知上游问题见
  [`docs/reference-repositories-audit-20261020.md`](../../docs/reference-repositories-audit-20261020.md)。

上游地址：

- <https://github.com/YuhangJia123/LQCD_Wickcontraction_reduce.git>
- <https://github.com/FeynCalc/feyncalc.git>

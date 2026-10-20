# 外部 QCD 代码参考

本目录保存 4 个上游 Git 仓库的子模块指针，不把第三方源码复制进 MyQCD 主包。

| 子模块 | 锁定提交 | 用途 | 上游许可 | 本库处理 |
| --- | --- | --- | --- | --- |
| `LQCD_Wickcontraction_reduce` | `1c996a86b778b33d6fd670f025b8074bd6798093` | 格点关联函数的 Wick 配对、颜色/Dirac 约化与输出验证 | 仓库当前未附 `LICENSE`、`COPYING` 或等效授权文本 | 只吸收可独立重写的算法思想；不从子模块复制代码 |
| `feyncalc` | `1ee480093293a01a82b3e365d026808f1d4e1c17` | Mathematica 中的 Dirac、Lorentz、SU(N) 与圈积分符号计算 | GPL-3.0-or-later | 保持为独立子模块；MIT 主包不复制其源码 |
| `PyQCD` | `05f9080464fed7732e649fc7e5d1ca9cc869556e` | 格点 QCD 主包（`pyqcd/`、`refer/`、`docs/`） | MIT | 保持为独立子模块；只读参考，不复制源码 |
| `PyQCU` | `57f40fa1a89a9596ac885e39346f51115ac7383e` | 格点 QCD 算符求解与多后端实现（`pyqcu/`、`cpp/{cuda,cann,dtk,maca,kupl}/`） | MIT | 保持为独立子模块；只读参考，不复制源码 |

## 初始化状态（2026-10-21）

- `PyQCD`、`PyQCU` 已初始化，工作树干净，`HEAD` 与父仓库 gitlink 一致。
- `LQCD_Wickcontraction_reduce`、`feyncalc` 当前是空目录，未初始化
  （`git submodule status` 前缀为 `-`）；需要时执行
  `git submodule update --init -- <path>`，并重新审查上游差异、许可证和测试结果。
- 2026-10-20 的审计是在两个子模块检出状态下完成的；当前空目录不能复跑其测试，
  旧结论只作为历史证据，详见
  [`docs/reference-repositories-audit-20261020.md`](../../docs/reference-repositories-audit-20261020.md)。

## 版本说明

- `LQCD_Wickcontraction_reduce` 上游当前只有一个初始提交，且未声明该代码的许可证。
  MyQCD 的 MIT 许可证不能替第三方子模块补充授权；未获版权人明确许可前，只能引用
  接口、公式和测试思想，不能把实现搬入 MyQCD。
- `feyncalc` 的包元数据写 `10.2.1`，但锁定提交带有 `.testing` 标记，且晚于
  `Release-10_2_1` 标签。引用时必须写成“`10.2.1` 之后的开发快照”并附完整提交 SHA，
  不能简称为 FeynCalc 10.2.1。
- 四个子模块只锁定提交，不锁定远端分支。更新子模块前应先审查上游差异、许可证和测试结果。

## 使用边界

- MyQCD 的 `myqcd.wick` 是独立实现的精确味道配对枚举器，不导入或复制
  `LQCD_Wickcontraction_reduce` 的源码。
- FeynCalc 的 Mathematica 测试需要本机 Wolfram Engine/Mathematica；当前环境没有相应运行时，
  因此不能把静态审计写成 FeynCalc 运行通过。
- `PyQCD`、`PyQCU` 是本库的只读参考实现；其内部 `refer/`、`data/`、`logs/` 不属于本库的
  文献库或交付物，整理 `refer/` 时不要递归改写子模块内容。

上游地址：

- <https://github.com/YuhangJia123/LQCD_Wickcontraction_reduce.git>
- <https://github.com/FeynCalc/feyncalc.git>
- <https://gitee.com/zhangxin8069/PyQCD.git>
- <https://gitee.com/zhangxin8069/PyQCU.git>

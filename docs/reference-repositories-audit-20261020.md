# 新增参考仓库审计（2026-10-20）

## 范围与锁定版本

本次只读审计 `refer/git-rep/` 下新增的两个子模块：

| 子模块 | 锁定提交 | 上游状态 | 许可 |
| --- | --- | --- | --- |
| `LQCD_Wickcontraction_reduce` | `1c996a86b778b33d6fd670f025b8074bd6798093` | 单个初始提交 | 未附许可证 |
| `feyncalc` | `1ee480093293a01a82b3e365d026808f1d4e1c17` | `10.2.1` 标签之后的开发快照 | GPL-3.0-or-later |

两个子模块的实际 `HEAD` 都与父仓库 gitlink 一致，工作树干净。父仓库只锁定提交，
没有锁定远端分支。

## 主要结论

### Wick 约化项目

现有 153 项 `unittest` 全部通过。统一入口样例、`delta`/`pipi` 的
`complete` 与 `cross_time` 对照，以及随机复 Gamma/peram 的单介子直接收缩均通过；
没有发现可复现的 Wick 配对符号、介子 Dirac/Gamma 收缩或 epsilon/delta 颜色收缩错误。

仍确认了以下输入契约或端点语义问题：

| 严重度 | 问题 | 证据 |
| --- | --- | --- |
| 高 | 扁平 JSON 中 `side` 非法的记录被静默丢弃；字符串 `flavors="uu"` 被当作两个味道接受 | `kernels/wick_reducer/unified.py:125,147` |
| 高 | `normal-special` 把 `phase`/`clebsch` 作为端点标签，却不把它们乘入系数；与 Wick 路径语义不一致 | `kernels/wick_reducer/unified.py:251`、`kernels/wick_colour_orbit/user_api.py:289` |
| 中 | 空算符、数量不平衡输入在不同入口分别返回空配对、伪 `wick_count=1` 或异常 | `kernels/wick_reducer/reducer.py:1616`、`kernels/wick_colour_orbit/model.py:222` |
| 中 | 独立 colour-orbit JSON 解析器丢弃 `momentum`、`projector`、`phase` 等字段 | `kernels/wick_colour_orbit/input_json.py:106` |
| 中 | `cross_time` 的端点键只检查 source 端不同 `point`，sink 端标签改变可得到相同摘要 | `kernels/wick_colour_orbit/cross_time.py:33,637` |
| 中 | `sink_routes` 未验证覆盖与唯一性，重复路由仍通过 | `kernels/wick_colour_orbit/model.py:124` |
| 中 | 旧 normalizer 默认开放槽 2/Gamma `(0,1)`，统一模型默认开放槽 0/Gamma `(1,2)` | `kernels/correlator_wick_normalizer.py:327,1395`、`kernels/wick_reducer/operator_model.py:52` |
| 低 | 两个入口同名的 `pn` 夹具使用不同槽位和 source 味道顺序，跨入口比较容易误读 | `kernels/correlator_wick_normalizer.py:349`、`kernels/wick_reducer/operator_model.py:213` |
| 低 | `coarse` 路径不校验未注册 Gamma，只有更完整的约化路径才报错 | `kernels/wick_reducer/reducer.py` 的 coarse 分支 |

`pn` 的 `normal-special-check` 在未固定开放自旋时超过 4 分钟，审查进程被人工停止；
因此该组合不能记为已通过。固定 `external_spin` 后再测，属于上游后续工作。

### FeynCalc

该提交不是正式的 `Release-10_2_1` 标签。包内的
`FeynCalc/FeynCalc.m` 仍写 `10.2.1`，但 `.testing` 标记会把运行时识别为开发版。
本库引用时必须保留完整提交 SHA。

FeynCalc 的主要风险集中在安装器：

- 静默安装先删除旧目录，再下载和解压；网络或解压失败会丢失旧安装
  （`install.m:237,328,348-356`）。
- 默认从可变的 `master.zip`、`hotfix-stable.zip` 下载，没有固定提交、哈希或签名，
  随后直接加载下载代码（`install.m:159-160,442`）。
- 测试脚本仍尝试 `math8`/`math9`，而包本身已拒绝 Mathematica 10 以下版本。
- 文档链接和示例图片存在未提交目标；静态扫描记录 224 个未解析本地引用。

本机没有 `wolframscript`、`WolframKernel`、`math` 或 Mathics，无法运行 FeynCalc
MUnit/集成测试。可以确认的只有子模块完整性、shell/XML 语法和静态文档问题，
不能报告 FeynCalc 运行通过。

## 合并到 MyQCD 的内容

新增 `myqcd/wick.py`，只吸收以下可独立验证的组合层思想：

1. 按精确味道分组的完全配对枚举，配对数为
   \[
   N_{\mathrm{Wick}}=\prod_f n_{q,f}!.
   \]
2. 输入字段顺序属于 Grassmann 定义；相同的配对集合可因算符交错顺序改变符号。
3. 配对映射使用“夸克序号 -> 反夸克序号”，并显式记录 `+1/-1`。
4. 非法味道平衡、重复映射、错误字段类型直接报错，不静默丢弃。
5. Gamma、颜色张量、source 共轭和整体 Berezin 约定留在相关函数层，不混入组合枚举。

该实现没有导入、复制或改编上游 Python/Mathematica 源码。原因是前者未声明许可证，
后者为 GPL-3.0-or-later，而 MyQCD 根许可证是 MIT。

## 验证证据

```text
LQCD_Wickcontraction_reduce unittest: 153 passed
default normal-special-independent: 2 Wick, 288 basis terms
pip normal: 24 Wick
pn normal-wick-check: 36 Wick, 18 independent, 18 dependent
delta special check: complete=1944, cross_time=54 coefficients
pipi special check: complete=104544, cross_time=264 coefficients
random single-meson Dirac contraction max residual: 3.6e-14
MyQCD/upstream short-order pairing cross-check: 102 cases, exact match
```

MyQCD 的独立约定测试还覆盖：

- 交错单介子 `bar u, u` 得到符号 `-1`，块顺序 `u, bar u` 得到 `+1`；
- 双介子两个配对符号分别为 `-1`、`+1`；
- `pn=36`、`ppn=2880`、`Delta++Delta-=36`；
- `python -m myqcd` 将 Wick 配对检查纳入核心审计。

## 后续步骤

不直接修补外部子模块，以免把上游快照改成不可追踪的本地分支。若后续需要采用其约化器，
应先向上游报告上述输入校验与端点键问题，并在固定提交、明确许可后重新评估。

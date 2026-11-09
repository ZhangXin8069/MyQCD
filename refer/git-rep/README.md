# PyQCD 外部源码参考

本目录保存外部源码的只读 Git 子模块。所有子模块固定在上游提交，不在其工作树内写入
文件；MyQCD 只引用路径与行号，不复制内容。

| 子模块 | 上游 | 当前检出 | 用途 | 许可 |
|---|---|---|---|---|
| `PyQCD` | <https://gitlab.itp.ac.cn/zhangxin8069/PyQCD.git> | `2e6c868f4573b50746acdc7ad9dad2d7af4e9a0a` | 格点 QCD 主包、物理文档、历史参考代码（唯一事实源） | MIT |
| `feyncalc` | <https://github.com/FeynCalc/feyncalc.git> | `1ee480093293a01a82b3e365d026808f1d4e1c17` | γ 代数、SU(N) 颜色、张量化简参考 | GPL-3.0（只读参考，不复制） |
| `LQCD_Wickcontraction_reduce` | <https://github.com/YuhangJia123/LQCD_Wickcontraction_reduce.git> | `033d607cdb753e98ddc6c26dff594f319d8406f2` | Wick 收缩归约与 Dirac 索引图参考 | 无 LICENSE（只读参考，不复制） |
| `syhep` | <https://github.com/mardsouza/syhep> | `77d3d4861ef3556acdd1e3a757a6efbe6598428e` | SymPy 高能物理符号计算参考 | GPL-3.0（只读参考，不复制） |
| `RGBeta` | <https://github.com/aethomsen/RGBeta> | `946db15bdb489a772aa26272f527081708527920` | QCD/EFT 重整化群 beta 函数参考 | MIT |
| `pyfeyn2` | <https://github.com/APN-Pucky/pyfeyn2> | `d5de3ea0f0dd929be800b8a5dd377f9fec7fa0cf` | Python 费曼图绘制与 TikZ/DOT 渲染参考 | GPL-3.0（只读参考，不复制） |
| `pyfeyngen` | <https://github.com/paulhenry46/pyfeyngen> | `530a357467944e53320ce72e3e4683cbb771f0d2` | 粒子语法 → TikZ-Feynman 生成参考 | MIT |

PyQCD 子模块内部另有只读参考树 `refer/git-rep/PyQCD/refer/`，收录书籍、论文、历史代码
和外部软件来源。MyQCD 不复制这些内容，也不在其工作树内写入文件。

## 本库入口

- 物理说明总入口：`docs/pyqcd_physics/README.md`
- PyQCD 参考主题映射：`refer/git-rep/docs/pyqcd-physics-reference.md`
- 外部库吸收报告：`docs/absorb_reference_libraries_20261109.md`

## 维护边界

- 子模块工作树只读；更新子模块时先检查本地状态、上游差异、许可证和测试条件。
- 新增外部内容必须先登记来源、固定提交与许可证；GPL-3.0 或无许可证内容只能按数学恒等式
  独立重写，禁止复制源码。
- 不递归跟随 `PyQCD/refer/` 中的历史符号链接，不读取链接指向的仓库外路径。
- 不自动初始化子模块内部的嵌套参考树；需要时显式使用 `--recursive`。

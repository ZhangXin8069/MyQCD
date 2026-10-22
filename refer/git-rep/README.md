# PyQCD 外部源码参考

本目录只保留一个 Git 子模块：

| 子模块 | 上游 | 当前检出 | 用途 | 许可 |
|---|---|---|---|---|
| `PyQCD` | <https://gitee.com/zhangxin8069/PyQCD.git> | `0a2f85d30881fc8ead60972c0afb9c028abc348f` | 格点 QCD 主包、物理文档、历史参考代码 | MIT |

PyQCD 子模块内部另有只读参考树
`refer/git-rep/PyQCD/refer/`，收录书籍、论文、历史代码和外部软件来源。MyQCD 不复制
这些内容，也不在其工作树内写入文件。

## 本库入口

- 物理说明总入口：`docs/pyqcd_physics/README.md`
- PyQCD 参考主题映射：`refer/git-rep/docs/pyqcd-physics-reference.md`

## 维护边界

- 子模块工作树只读；更新 PyQCD 时先检查本地状态、上游差异、许可证和测试条件。
- 不递归跟随 `PyQCD/refer/` 中的历史符号链接，不读取链接指向的仓库外路径。
- `git-rep/PyQCD/refer/papers/` 没有项目级索引；文件身份以上游路径和文件本身为准，
  不从文件名推断未经验证的版本。
- 本库不再维护 PyQCU、FeynCalc 或独立 Wick 约化子模块；相关概念以 PyQCD 实现和
  `myqcd/wick.py` 的独立组合层审计为准。

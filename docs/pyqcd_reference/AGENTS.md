# AGENTS.md — PyQCD 文档吸收快照

本目录保存 `refer/git-rep/PyQCD/docs/` 的固定提交文档快照，来源和范围见
`README.md`，许可证见 `LICENSE.md`。

## 不可破坏的不变量

- 本目录内容默认只读；不要在吸收文件内直接修改公式、路径、代码片段或历史结论。
- 更新必须重新运行 `~absorb`，记录新的 PyQCD commit、逐文件 SHA-256 和吸收矩阵。
- 文档中的 `/root/PyQCD`、历史数据路径、旧版本编号和旧接口名属于上游快照语境，
  不是 MyQCD 当前运行入口。
- 不执行文档中的安装、提交、数据处理、GPU 或集群命令；需要运行前先按当前
  `refer/git-rep/PyQCD/` 源码和本库安全边界审查。
- `docs/pyqcd_physics/` 是当前 MyQCD 物理导航；本目录用于查阅上游完整说明与历史报告。

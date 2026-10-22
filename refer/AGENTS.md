# AGENTS.md — refer

本目录为 PyQCD 物理说明提供文献辅助，分为三部分：

- `git-rep/PyQCD/`：唯一外部源码子模块，探索 PyQCD 物理与接口的事实源；
  `git-rep/PyQCD/refer/` 是其只读书籍、论文、历史代码和外部软件参考树。
- `papers/`：50 篇格点 QCD/部分子物理论文的英中 LaTeX 转排，用于公式追溯和术语对照。
- `books/`：格点 QCD 与量子场论教材的英中 LaTeX 转排，用于定义和推导核对。

## 使用规则

- `git-rep/PyQCD/**` 是上游内容，只读；不在子模块工作树内新增、修改、移动或删除文件。
- 本库对 PyQCD 的索引、物理映射和分析写入 `git-rep/docs/`，来源与致谢写入
  `git-rep/README.md`。
- `papers/`、`books/` 只作为本地可检索辅助，不覆盖 PyQCD 源码中的轴序、符号、投影、
  归一化和方案约定。引用冲突时以 PyQCD 源码及其同提交文档为准。
- 原始 PDF 和转排内容的版权、许可与再分发条件未逐项重新认证；不得把上游参考内容复制
  进 `myqcd/` 或 `docs/`。
- `git-rep/PyQCD/refer/` 内存在指向仓库外的历史符号链接。工具不得递归跟随链接或读取
  仓库外目标。

## 入口

- PyQCD 参考索引：`git-rep/docs/pyqcd-physics-reference.md`
- 本地论文索引：`papers/INDEX.md`
- 本地教材说明：`books/AGENTS.md`

真实系综分析和 GPU 验证需要单独确认运行时与数据条件；旧日志不得作为本次验证通过的
直接证据。

# PyQCD 格点 QCD 文档吸收

本目录吸收 `refer/git-rep/PyQCD/docs/` 中与格点 QCD 物理直接相关的文档，
保留上游相对路径、文件名和内容快照。

## 来源

- 上游仓库：<https://gitee.com/zhangxin8069/PyQCD.git>
- 固定提交：`0a2f85d30881fc8ead60972c0afb9c028abc348f`
- 上游路径：`refer/git-rep/PyQCD/docs/`
- 许可证：MIT，见 [`LICENSE.md`](LICENSE.md)
- 逐文件 SHA-256：`logs/data/pyqcd-docs-absorb/manifest.tsv`
- 175 项完整吸收矩阵：`logs/data/pyqcd-docs-absorb/absorption.tsv`

## 吸收范围

| 分类 | 数量 | 说明 |
|---|---:|---|
| 主目录 TeX | 67 | 格点 QCD 笔记、胶子 PDF/TMD 推导、代码解析和专题报告 |
| 主目录 PDF | 70 | 与 TeX 配对成品及独立论文/报告 PDF |
| 主目录 Markdown | 3 | 胶子 PDF 流程、梯度流说明和胶子 TMD 审计 |
| `from-logs` TeX | 10 | 历史分析、谱学、蒸馏与 TMD 工作流报告 |
| `from-logs` PDF | 10 | 对应历史报告成品 |
| `from-logs` Markdown | 3 | 历史运行摘要和 PDF 检查记录 |
| 合计 | 163 | 约 56.2 MB |

## 主要内容

- 胶子 PDF/TMD：`胶子PDF完整推导.tex`、`胶子PDF笔记.tex`、`胶子TMD梯度流连续极限.tex`。
- 格点算符与重整化：`格点QCD中的OPE算符.tex`、`格点QCD中的场强张量.tex`、
  `格点QCD中的Wilson线.tex`、`格点QCD中的梯度流重整化.tex`。
- 格点方法：`格点QCD蒸馏方法解析.tex`、`格点QCD中的传播子求解.tex`、
  `格点QCD中的误差统计.tex`、`格点QCD中的重采样方法.tex`。
- 谱学与强子物理：`格点QCD中的GEVP.tex`、`格点QCD中的强子谱学.tex`、
  `格点QCD中的色散关系.tex`、`格点QCD中的形状因子.tex`。
- 全库分析与工作流：`analy_pyqcd_20260818.tex`、`pure_pyqcd_20260818.tex`、
  `analy_physics_chain_20260824.tex`、`理论解析与工作流-v20260911.tex`。
- 历史运行报告：`from-logs/logs/` 下的 distill、spectrum、TMD 与回归报告。

## 未复制项

175 个候选文件中，163 个复制到本目录；其余 12 个的处置如下：

- 11 个过程或维护元数据文件被拒绝：`.gitignore`、`AGENTS.md`、
  `EXAMPLES_MIGRATION_20260927.md`；
- `form_pyqcd_20260928.md`、`form_pyqcd_20261020.md`、`form_pyqcd_20261021.md`；
- `plans/2026-10-22-absorb-dev20-gluon-tmd-debug.md`；
- `superpowers/plans/` 下 3 个实施计划和 `superpowers/specs/` 下 1 个设计文件；
- 1 个构建附件 `_tree_pyqcd.txt` 标为 `reference-only`，保留在上游子模块中，不复制到
  `docs/` 的允许文件类型范围。

## 使用边界

- 本目录是上游文档快照；正文中的 `/root/PyQCD`、历史数据路径、旧版本编号和旧接口名
  不代表当前 MyQCD 运行入口。
- 不执行文档中的安装、集群提交、数据处理或 GPU 命令；需要运行时应先按当前
  `refer/git-rep/PyQCD` 代码和本库安全边界重新审查。
- TeX 与 PDF 按上游提交原样保存。若修改本地 TeX，必须重新编译并登记与上游哈希的差异。
- 当前 MyQCD 物理入口仍是 [`../pyqcd_physics/README.md`](../pyqcd_physics/README.md)；
  本目录用于查阅完整上游说明、推导和历史报告。

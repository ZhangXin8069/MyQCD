---
name: long-context-monograph
description: |
  当用户要求把大体量、多格式、只读参考资料全量整合为长书稿、专著或书籍，
  并同时强调“全质全量”“来源覆盖”“上下文安全”“分批评审”“LaTeX 编译”
  或“机器证据”时使用。也用于把现有论文扩展为专著、建立文件/知识单元双层
  覆盖账本、生成来源图谱，或审计整书引用、版面与来源闭合。
metadata:
  openclaw:
    emoji: 📚
---

# long-context-monograph — 长上下文专著整合

## 执行前置

遵循根 `AGENTS.md`、来源目录最近的 `AGENTS.md` 和 `~form` 的本地边界。先以
只读命令确认固定来源、许可证、Git 状态、现有主稿和构建目录，再建立可回退的
`data/build/<run>/` 工作区。来源快照只读；主稿修改由主代理串行完成。

- 设计子代理任务、上下文预算、失败重试或串行降级时，读取
  `references/context-safe-dispatch.md`。
- 合并章节、抽取可追踪模块、生成来源图谱、设置书籍结构或执行 XeLaTeX 验收时，
  读取 `references/book-and-atlas-checklist.md`。

## 核心原则

1. **先冻结来源，再解释内容。** 没有逐文件哈希、规模、类型和成对关系，无法证明
   “全量”对象在整合期间未漂移。清单是不可变基线，不是事后附录。
2. **文件覆盖与知识覆盖分开记账。** TeX/PDF 成对件、PDF 排版见证和历史版本会让
   文件数大于独立知识单元数；两个粒度都闭合，才能说明既未漏文件也未重复计内容。
3. **上下文按单元受控。** 整文件或整批摄取会把局部综合退化为上下文搬运。分块读取、
   逐单元落盘和硬输出上限让失败范围可定位、可重试。
4. **中间产物离开 `data/` 后才能进入书稿。** `data/` 是不入库运行区；最终
   `\input` 必须指向 `docs/` 中经审阅的纯正文或附录模块，编译链才能由 Git 复现。
5. **合并是语义重构，不是文件拼接。** 冲突标签、重复宏、宽表、长公式、旧章节号和
   非 ASCII 路径都会在跨批次合并后出现；编译成功只证明语法可解析。
6. **来源图谱由机器索引生成。** 手工维护 87 单元或 163 文件的大表会漂移；生成器
   从 inventory 与 ledger 读取路径、哈希、页数和目标章节。
7. **证据分层报告。** 来源事实、综合推断、当前运行验证和未执行边界分别记录；旧 PDF、
   历史日志或局部编译不能替代本轮验收。

## 工作流程

### 1. 建立不可变来源清单

固定来源提交、许可证和只读边界。对每个文件登记稳定路径、控制/内容分类、扩展名、
字节数、TeX/Markdown 行数、PDF 页数、SHA-256、manifest 哈希与匹配状态、成对文件、
`unit_id` 和来源提交。每一对 TeX/PDF 创建一个共享内容单元；独立文件各自成单元。

完成判据：manifest 缺失、额外文件和哈希不匹配均为 0；所有文件已分配，所有单元有
主文件和伴生关系。PDF 用 `pdfinfo` 取页数，不能从文件名推测。

### 2. 建立双层覆盖账本

文件账本至少包含 `path/type/bytes/lines/pages/sha256/manifest_match/pair_role/unit_id`。
单元账本至少包含
`unit_id/batch/primary/companions/read_depth/disposition/target_section/target_artifact/unique_content/coverage_status`。
每个单元只能有一个主批次；历史重复版本映射到主版本或历史章节，并说明差异用途。

完成判据：文件级 `N/N`、单元级 `M/M`、缺失与重复均为空。当前项目基线可用以下命令
复核：

```bash
python -c 'import json; d=json.load(open("data/build/pyqcd_monograph_20261023/integration_summary.json")); assert d["units_covered"] == d["units_total"]; assert d["manifest_hash_matches"] == d["content_files_total"]; assert d["all_units_covered"]; print(d["units_covered"], d["content_files_total"])'
awk -F '\t' 'NR > 1 {print $1}' data/build/pyqcd_monograph_20261023/integration_ledger.tsv | sort | uniq -d
```

第二条命令应无输出；若有输出，先修复重复归属，不进入批次综合。

### 3. 隔离批次并派发综合

按知识域划分互斥批次，在派发前读取 `references/context-safe-dispatch.md`。每个子代理
只读指定单元，只写自己的批次目录，并同时产出覆盖表、证据笔记、现有稿缺口、
带唯一前缀的 LaTeX 草案和机器可读 completion。主稿只由主代理合并。

完成判据：每批 `coverage_rows` 等于分配单元数，所有批次并集恰好覆盖全部单元（本轮为
B01–B10）；
每批至少抽查两个物理结论与来源行号或 PDF 页面对应。失败派发保留原提示词与错误，
执行一次受控重试；重试仍失败后由主代理按单元串行完成。

### 4. 审阅并抽取可追踪书稿模块

按定义、推导、近似、适用范围、失败条件、算法、实现事实、验证证据和历史边界审阅
草案。把通过的纯正文和附录从 `data/` 抽取到 `docs/<project>/monograph/`，删除批次
文档类、导言区、验证脚手架和私有时序内容；主稿只通过 `\input{docs/...}` 引用。

完成判据：主稿无 `\input{data/...}`；每个被引用模块都通过 `git check-ignore -q`
的“未被忽略”检查，并在交付时进入版本控制范围；批次标签已统一命名空间且没有重复定义。

### 5. 合并书籍结构与来源图谱

采用 `ctexbook`、`frontmatter/mainmatter/backmatter`、`part/chapter/section`、双向页眉
页码、章首页、目录、附录和参考文献。来源图谱由 inventory/ledger 生成，逐文件保留
TeX 主证据、PDF 见证、哈希、规模与章节归宿。合并与排版细节读取
`references/book-and-atlas-checklist.md`。

完成判据：章节层级、目录、页码、图表编号和来源图谱均可由最终 TeX 重建；不存在旧
章节号、未转义路径、溢出宽表或跨章重复宏。

### 6. 两遍编译并执行全量验收

在 `data/build/` 输出编译中间件，连续运行两遍 XeLaTeX。第二遍后同时检查日志、引用
与标签、PDF 字体和页数、文件/单元覆盖、哈希、根测试、公式审计、严格格式审计及 Git
空白。当前主稿的可执行编译骨架为：

```bash
BUILD_DIR=data/build/pyqcd_monograph_20261023/main_build
mkdir -p "$BUILD_DIR"
xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" docs/pyqcd_physics/report_gluon_tmd_lattice_qcd_review_20261023.tex
```

日志中 undefined refs/cites、`Overfull`、`Float too large` 和 `Missing character` 必须为零。
“能编译”不满足验收；还必须证明语义覆盖、排版权威性和来源哈希同时闭合。

### 7. 归档机器证据

最终日志记录固定来源与基线哈希、批次分配、失败派发、唯一一次重试、串行降级、实际
产出文件、最终页数、完整验证命令与退出码、严格审计相对基线的告警差异，以及未执行
的真实系综、GPU、集群或视觉检查。只报告实际运行结果。

## 错误处理

| 场景 | 正向动作 |
|---|---|
| 来源在整合中发生变化 | 停止合并，重新生成 inventory，确认新提交与许可证后再继续 |
| 子代理上下文超限 | 停止恢复循环，记录失败；按相同 provider/model/auth/settings 链做一次缩小读取预算的重试，仍失败则由主代理逐单元串行完成 |
| 批次覆盖表有缺行或重复 | 以 inventory 为准补齐或重新分配；不得用其他批次的重复行填充 |
| 草案位于 `data/` 且主稿直接引用 | 审阅后抽取为 `docs/` 纯模块，用 `git check-ignore -q` 排除被忽略路径后替换 `\input` |
| 合并后标签或宏重复 | 为批次标签加命名空间；合并等价宏，保留唯一权威定义并重新编译 |
| 宽表、长公式或 PDF 内容溢出 | 改用 `longtable`/`tabularx`、拆分公式或调整尺寸；不用隐藏日志或裁切内容规避 |
| CJK 路径或哈希缺字/溢出 | 使用可用 CJK 字体与 `seqsplit`/`allowbreak`，按固定宽度分段哈希并确认无 Missing character |
| 严格审计仍有历史告警 | 保存改动前基线，证明本次文件未新增告警；不得通过修改只读快照制造全绿 |
| 物理结论无法由来源行/页确认 | 在 completion 和最终日志标为未解决，降级为历史语境或不写入结论 |

## Git 检查

有 Git 且本次产生改动时，运行 `git diff --check`，定向复查改动文件与路径，保留工作区
中他人的未提交改动。本技能不自动暂存、提交、推送或改写标签。

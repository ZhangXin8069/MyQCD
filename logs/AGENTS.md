# Agent 日志索引

## git-history-large-files-audit - stage - 2026-10-20 00:39:59 +0800
- 主任务: 审计并清理远程 Git 历史中大于 10MB 的文件
- 日志文件: logs/v202610200039.txt
- 文件大小: 3186 bytes
- 触发原因: 阶段成果
- 关键内容: 列出远端可达历史中 3 个大文件并等待破坏性操作确认
- 验证: path, size, required sections, conflict markers
- 批次状态: in-progress

## git-history-large-files-cleanup - final - 2026-10-20 01:03:58 +0800
- 主任务: 删除远端 Git 历史中大于 10MB 的文件并完成本地和远端历史瘦身
- 日志文件: logs/v2026102001.txt
- 文件大小: 5087 bytes
- 触发原因: 任务完成
- 关键内容: 已删除 3 个大文件，重写并推送 main 与 11 个标签，独立远端克隆验证通过
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## form-myqcd-20261020 - final - 2026-10-20 01:27:59 +0800
- 主任务: MyQCD ~form 整改：清理 logs/.DS_Store、同步根 form 标记块并完成验证
- 日志文件: logs/v2026102001-2.txt
- 文件大小: 8556 bytes
- 触发原因: 任务完成
- 关键内容: 完成唯一格式冲突清理、精确忽略与根规则同步；全部测试和审计通过，未提交或推送
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## refer-wick-audit-20261020 - final - 2026-10-20 03:23:11 +0800
- 主任务: 分析新增参考文档与代码并合并有效内容
- 日志文件: logs/v2026102003.txt
- 文件大小: 7166 bytes
- 触发原因: 任务完成
- 关键内容: 审计两个新增参考子模块，记录上游错误与许可边界，独立实现并验证 Wick 精确味道配对枚举。
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## tag-dev5-20261020 - final - 2026-10-20 03:34:49 +0800
- 主任务: 创建 dev5 开发快照标签
- 日志文件: logs/v2026102003-2.txt
- 文件大小: 4139 bytes
- 触发原因: 任务完成
- 关键内容: 检查 dev4 以来变更与全历史标签链，创建并验证本地附注标签 dev5，未推送。
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## refer-docs-20261021 - final - 2026-10-21 04:25:08 +0800
- 主任务: 整理参考子库 refer
- 日志文件: logs/v2026102104.txt
- 文件大小: 6535 bytes
- 触发原因: 任务完成
- 关键内容: 修正 refer 文档/索引漂移，补全 git-rep 子模块说明，复验两套选集 36/35 页
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## tag-dev6-20261021 - final - 2026-10-21 04:27:19 +0800
- 主任务: ~tag:dev
- 日志文件: logs/v2026102104-2.txt
- 文件大小: 4217 bytes
- 触发原因: 任务完成
- 关键内容: 在 HEAD 创建本地注释标签 dev6，记录子模块与日志提交，明确 refer 改动未纳入且未推送
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## tag-dev7-20261022 - final - 2026-10-22 14:19:51 +0800
- 主任务: ~tag:dev
- 日志文件: logs/v2026102214.txt
- 文件大小: 4842 bytes
- 触发原因: 任务完成
- 关键内容: 在 HEAD 创建并验证本地附注标签 dev7，完成测试、历史链与格式审计
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## refer-git-rep-sync-20261022 - stage - 2026-10-22 18:35:26 +0800
- 主任务: 同步 refer/git-rep 子模块到最新远端版本
- 日志文件: logs/v202610221835.txt
- 文件大小: 4064 bytes
- 触发原因: 阶段成果
- 关键内容: PyQCD 与 PyQCU 已快进到 origin/main；两个 GitHub 子模块因连接拒绝未更新
- 验证: path, size, required sections, conflict markers
- 批次状态: in-progress
## refer-git-rep-sync-20261022-final - final - 2026-10-22 18:39:10 +0800
- 主任务: 同步 refer/git-rep 四个子模块到最新远端版本
- 日志文件: logs/v2026102218.txt
- 文件大小: 5122 bytes
- 触发原因: 任务完成
- 关键内容: 四个子模块均已初始化并与各自上游最新提交同步；LQCD 最小相关测试通过，FeynCalc 因缺少 Wolfram 运行时未测试
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## pyqcd-physics-refocus-20261022 - final - 2026-10-22 19:30:13 +0800
- 主任务: 重构 MyQCD 为 PyQCD 格点 QCD 物理说明库
- 日志文件: logs/v2026102219.txt
- 文件大小: 8147 bytes
- 触发原因: 任务完成
- 关键内容: 定位、目录、参考路径和子模块已重构；根测试与公式审计通过，课程 PDF 全量视觉验收保留为后续步骤
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## remove-deprecated-lqcd-course-20261022 - final - 2026-10-22 19:45:27 +0800
- 主任务: 删除 MyQCD 已弃用的课程内容
- 日志文件: logs/v2026102219-2.txt
- 文件大小: 6621 bytes
- 触发原因: 任务完成
- 关键内容: 课程文档、技能、生成/验证代码、日志和缓存已删除；现行引用清零，测试、报告编译和严格格式审计通过
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## absorb-pyqcd-docs-20261022 - final - 2026-10-22 20:10:06 +0800
- 主任务: 用 ~absorb 将 PyQCD docs 中的格点 QCD 物理文档吸收到 MyQCD docs
- 日志文件: logs/v2026102220.txt
- 文件大小: 6167 bytes
- 触发原因: 任务完成
- 关键内容: 完整审计 175 个候选文件，按固定提交吸收 163 个物理文档；哈希、PDF、TeX、测试、公式审计、理论审计和格式审计均完成
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## gluon-tmd-review-20261023 - final - 2026-10-23 00:27:45 +0800
- 主任务: 恢复并完成核子胶子 TMD-PDF 格点 QCD 详尽理论综述
- 日志文件: logs/v2026102300.txt
- 文件大小: 7108 bytes
- 触发原因: 任务完成
- 关键内容: 恢复会话 01a16448-8ccb-7f82-8652-5cfaafcbdeae；完成 43 页综述的文献修订、编译、公式/引用/格式与根测试验证；严格格式审计仅有 21 条既有只读快照路径告警
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## gluon-tmd-algorithm-figures-20261023 - final - 2026-10-23 00:50:47 +0800
- 主任务: 为核子胶子 TMD-PDF 综述补充 BiCGSTAB 算法、详细物理解释与图形化表达
- 日志文件: logs/v2026102300-2.txt
- 文件大小: 6992 bytes
- 触发原因: 任务完成
- 关键内容: 新增 1 个单页 Unpreconditioned BiCGSTAB 算法、2 个求解器/传播子物理子节、4 幅原生 TikZ 图，并把求解误差纳入预算、验收和复现清单；论文扩至 49 页且通过编译、引用、图形与格式验证
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## gluon-tmd-formulas-visual-20261023 - final - 2026-10-23 01:00:29 +0800
- 主任务: 增强核子胶子 TMD-PDF 理论综述的公式密度与版面层次
- 日志文件: logs/v2026102301.txt
- 文件大小: 6395 bytes
- 触发原因: 任务完成
- 关键内容: 新增 16 个编号关系、4 个关键公式卡、1 个物理判据框和 1 个尺度审计框；重构摘要框、章节标题规则与图题样式；论文扩至 50 页并通过编译、公式、引用、图形和格式验证
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## gluon-tmd-review-supplement - final - 2026-10-23 01:13:47 +0800
- 主任务: 充实核子胶子 TMD-PDF 综述并完成 PDF 与审计验证
- 日志文件: logs/v2026102301-2.txt
- 文件大小: 6951 bytes
- 触发原因: 任务完成
- 关键内容: 综合 PyQCD docs 的实现层材料，扩充综述公式、表格、物理解释和验收门控，并完成编译、格式、公式与 Git 验证。
- 验证: path, size, required sections, conflict markers
- 批次状态: complete
## gluon-tmd-review-resume-final - final - 2026-10-23 02:02:40 +0800
- 主任务: 完成核子胶子 TMD-PDF 教程型专著最终交付
- 日志文件: logs/v2026102302.txt
- 文件大小: 6298 bytes
- 触发原因: 任务完成
- 关键内容: 轻量恢复旧会话断点，完成 152 页教程型专著最终编译、PDF 替换、公式/引用/格式/来源/PDF 与根测试验证。
- 验证: path, size, required sections, conflict markers
- 批次状态: complete

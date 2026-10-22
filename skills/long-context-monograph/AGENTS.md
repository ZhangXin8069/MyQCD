# AGENTS.md — long-context-monograph

本目录维护长上下文专著整合技能；先读 MyQCD 根 `AGENTS.md` 与 `skills/AGENTS.md`。
`references/context-safe-dispatch.md` 只用于派发、上下文预算和故障降级分支；
`references/book-and-atlas-checklist.md` 只用于书稿合并、来源图谱和编译验收分支。
来源资料保持只读，批次中间件写入 `data/build/`，最终 `\input` 只使用 `docs/` 中已跟踪模块。
主稿由主代理串行合并；不自动暂存、提交、推送或改写已发布标签。

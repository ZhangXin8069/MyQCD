---
name: refer
description: |
  当用户要求整理/生成参考文献库、精选论文选集、论文或书籍的 LaTeX 转排与中文翻译、
  建立引文网络导读文选、维护 refer 文献工作目录（books/ 与 papers/），或为某篇论文/书籍
  补充、修复、重新编译其 LaTeX 版本时使用。
metadata:
  openclaw:
    emoji: 📚
---

# refer — 文献工作目录生成与维护技能

## 核心原则

1. **双形态并行**：每篇文献产出两个 LaTeX 目录——英文转排 `<Slug>_latex/`（article/book 类）
   与中文译本 `<中文名>_latex/`（ctexart/ctexbook），章节/公式/图表编号一一对应、共用一套
   label；理由：中文读者快速理解，英文版保证与原文逐字可核。
2. **忠实转录，不代改**：英文版正文逐字保留（含原文笔误）、参考文献原样并入；中文版
   公式照抄不改、人名/机构/参考文献列表保留英文。物理内容不是写作素材，是转录对象。
3. **底稿以 arXiv 官方源为准**：转排底稿取 `arxiv.org/e-print/<id>` 官方 LaTeX 源；
   库内本地 PDF 仅用于核对首页书目信息。无开放获取底稿的前印本经典 → 记入暂缺清单，
   不凭空重排。
4. **编译是硬闸门**：每个 LaTeX 目录必须 `xelatex` 两遍编译零错误（`-halt-on-error`，
   `build/` 输出）；报错逐个根因修复（如 xeCJK「bad native font flag」= 数学上标内
   老式 `\rm` 组），不降级为"看起来能编译"。
5. **证据驱动选编**：精选必须基于库内引文网络计数（每篇被库内多少篇引用），
   不凭印象取舍；书目信息用 Inspirehep API / 库内 PDF 交叉核对，不确定字段标 `[?]`。
6. **索引与文档随行**：每库必有 `INDEX.md`（目录对/实测页数/底稿/备注）与 `AGENTS.md`
   （结构约定与质量说明）；每个转排目录附 `CONVERSION_GUIDE.md`（英文来源与妥协点）
   或 `TRANSLATION_GUIDE.md`（翻译约定与术语表）——后人（含未来的 agent）靠它们维护。

## 执行前置

遵循当前目录 `AGENTS.md`「技能执行公共契约」；仅按需读取技能正文与 reference。
工作目录内已有 refer 结构时，先读其 `AGENTS.md` 与 `INDEX.md` 对齐既有约定。

## 触发时机

- 用户要求生成/扩充文献库："整理参考文献"、"精选论文"、"从论文库挑最精华的N篇"、
  "论文转排"、"翻译成中文LaTeX"、"建立参考工作目录"
- 用户要求维护："修复某篇编译"、"补充缺失论文"、"更新索引"、"重新编译"
- 输入形态如 `~refer <任务>`、`~auto-refer <任务>`（无人值守）

## 工作流程

### Step 0. 摸底与对齐

1. 查看目标文献目录现状（`books/`、`papers/` 及其 `AGENTS.md`/`INDEX.md`）；
2. 明确任务范围：输入源（论文库路径）、目标数量（默认 20–50 篇）、语言要求（默认英+中）；
3. 需求缺项（源路径/数量/目录）一次性列出提问，不逐次追问；无人值守模式按默认值执行。

### Step 1. 文献摸底与引文网络分析（选编阶段）

1. 读遍源论文库中的全部论文 PDF，提取书目信息：作者、标题、期刊卷页、arXiv id；
2. 遍历每篇的参考文献列表，统计库内论文被引次数——形成引文网络；
3. 精选规则：库内原文里程碑（直接覆盖主题的奠基论文）+ 引文网络枢纽
   （被库内 ≥3 篇引用，多数 ≥8 篇）；目标 20–50 篇；
4. 按主题分章组织（示例八章：理论根基 / 模拟引擎 / 梯度流 / LaMET / 重整化 /
   胶子PDF / TMD与拟合 / AI采样），每篇一条卡片：
   - 书目卡片（作者/标题/期刊/arXiv，Inspirehep 或库内 PDF 核对）；
   - 入选理由（附库内引文计数）；
   - 物理内容与关键公式；
   - 库内影响（与库内其他论文的关联）。

### Step 2. 导读文选输出（book 类）

1. 英文版：`Essential_Papers_on_Lattice_QCD_Parton_Physics_latex/`——`book` 类，
   `main.tex` + `chapters/chNN_<主题>.tex`（preface/epilogue 可选）；
   用 `\papercard` 宏开每条卡片（书目块 + Why selected / Physics content /
   Impact and echoes in this library 段落）；无图片依赖；
2. 中文版：`<中文书名>_latex/`——`ctexbook`（XeLaTeX，AR PL UMing CN /
   Droid Sans Fallback），逐条忠实翻译，公式照抄；
3. 编译：`cd <dir>/build && xelatex -interaction=nonstopmode -halt-on-error ../main.tex`
   两遍（相对 `\input` 必须在 `build/` 内编译）。

### Step 3. 原文转排库（paper 类，每篇一对目录）

1. **底稿获取**：从 arXiv 官方源下载 LaTeX 源（`arxiv.org/e-print/<id>`）；
   无开放底稿 → 记入暂缺清单（如 Gross–Wilczek/Altarelli–Parisi/HMC/
   Collins–Soper/Parisi–Wu），可复用已验证的 books/ 转排（如 Wilson74）；
2. **英文转排** `<Slug>_latex/`（article 类）：
   - 归一化改造：期刊私有宏（revtex4-1/elsarticle 等）→ 标准 article——
     `\documentclass[11pt]{article}` + `geometry` 2.5cm；
     统一宏包：amsmath/amssymb/mathtools/graphicx/microtype/enumitem/url/
     hidelinks-hyperref；`mathrsfs` 存在则加载，否则 `\mathscr` 回退 `\mathcal`；
   - `main.tex` + `chapters/sectionNN.tex`（每节一文件）+ `chapters/backmatter.tex`
     （致谢/附录/参考文献）+ `images/`；
   - 正文逐字保留；参考文献 = 源 `output.bbl` 原样并入，不删改条目；
   - 图复制到 `images/`（`figure*` 跨栏改单栏 `figure`）；标题块手工重排
     （作者上标单位 + 脚注式 arXiv 行）；
   - 双栏改单栏；原文笔误按原样保留；写 `CONVERSION_GUIDE.md`（底稿来源+妥协点）；
3. **中文译本** `<中文名>_latex/`（ctexart）：
   - 逐节忠实翻译全部散文（标题/摘要/小节名/图注/表注/脚注/致谢/附录导语）；
   - 数学公式照抄、label 保留、交叉引用一一对应（同一套 label）；
   - 人名/机构/参考文献列表保留英文；图直接复制英文目录 `images/`；
   - 字体 AR PL UMing CN / Droid Sans Fallback；行距 1.05、`\emergencystretch=3em`；
   - 写 `TRANSLATION_GUIDE.md`（来源+术语约定+妥协点）；两目录各附简版 `AGENTS.md`。

### Step 4. 编译验证（硬闸门）

```bash
cd <目录> && xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex  # 两遍
```

1. 全部目录两遍编译，`build/main.pdf` 实测页数记录；
2. 编译日志零错误才算通过；报错根因修复后重跑（典型根因：
   xeCJK「bad native font flag」= 数学上标内 `\rm` 组含 `\bar{希腊}` →
   改 `\mathrm{CC},\bar{\nu}` 等价形式；缺图 → 从源包补齐 `images/`）；
3. 收尾核对：各目录实测页数、EN/ZH 页数差异合理性。
4. 文献将被课程/论文图谱消费时维护 `papers/provenance.json`。对原始 PDF 记录来源、源文件 SHA-256、
   源页数、身份核对与检查状态；对转排件另记录源 PDF/源代码哈希、输出 PDF SHA-256、两遍编译日志哈希
   和检查状态。任一适用输入变化都使旧通过状态失效；不得要求未经转排的原始 PDF 提供 XeLaTeX 日志。

### Step 5. 索引与文档收尾

1. `papers/INDEX.md`：每篇一行——英文目录 / 中文目录 / EN页 / ZH页 / 底稿 / 备注；存在 provenance
   manifest 时从其生成或逐项核对，禁止手写页数与 manifest 漂移；
2. `papers/AGENTS.md`：结构约定、编译方式、质量说明、暂缺清单、勘误记录；
3. 更新 `books/AGENTS.md` 或 refer 级 `AGENTS.md` 中相关段落；
4. 过程只在终端输出，用户输入记录按工作区契约写入 `.agent.*.list`。

### Step 6. 总结（结构化输出）

```text
✓ refer 完成
    输入:   <源库/任务>
    精选:   <N 篇，依据: 库内里程碑 X 篇 + 引文枢纽 Y 篇（被 ≥3 篇引用）>
    文选:   <EN/ZH 目录与页数>
    转排:   <M 篇 × 2 目录，共 K 个目录，合计 P 页>
    编译:   <全部通过 / 修复项明细>
    索引:   <INDEX.md / AGENTS.md 更新情况>
    暂缺:   <无开放底稿清单>
    遗留:   <未处理项>
```

## 错误处理

| 场景 | 处理 |
|---|---|
| 需求不明确（源路径/数量/语言） | 一次性列出全部缺项提问，不逐次追问 |
| 无 arXiv 开放底稿 | 记入暂缺清单并说明，复用 books/ 已验证转排兜底 |
| 编译报错 | 逐目录根因修复（缺图/字体/坏宏/原生表），修到零错误再继续 |
| 书目信息不确定 | 交叉核对（Inspirehep API / 库内 PDF）；仍不确定标 `[?]` |
| 中文版 xeCJK 字体错误 | 改写老式 `\rm` 数学组为 `\mathrm`/`\bar{}` 等价形式，保留排版语义 |
| 引文计数无数据 | 以库内 PDF 书目信息为准做人工判断，标注依据 |
| 双语编号不一致 | 以英文版为准，统一 label，交叉引用逐一对齐 |
| 原文笔误 | 英文版原样保留；中文版按语义译出并记录于 TRANSLATION_GUIDE |

## 注意事项

- 不编造书目信息、arXiv id 或物理内容；一切以源 PDF/arXiv 官方源为准；
- 忠实转录优先于"修正"——原文错误（笔误、过时结论）不代改，只记录；
- 目录命名恒为 `<Slug>_latex/`（英文）+ `<中文名>_latex/`（中文），保证与既有索引一致；
- 编译命令固定 `xelatex -interaction=nonstopmode -halt-on-error`，两遍，`build/` 输出；
- 不越界访问工作目录之外的文献库；需要其他路径的文献时先向用户确认；
- 大批量转排（数十篇）拆批执行，每批验证后再推进下一批。

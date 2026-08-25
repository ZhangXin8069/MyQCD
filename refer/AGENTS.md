# AGENTS.md — refer

格点 QCD 部分子物理文献工作目录。包含论文库 `papers/`（99 篇 PDF，只读）、
教科书库 `books/`（源 PDF + agent 生成的英/中 LaTeX 转排）、以及本目录生成的
**精华论文选集**（agent 生成）。

## 精华论文选集（2026-08-25 生成）

从 papers/ 的 99 篇论文 + 其全部参考文献的引文网络中精选 **38 篇奠基文献**，
分八章导读（理论根基 / 模拟引擎 / 梯度流 / LaMET / 重整化 / 胶子PDF / TMD与拟合 /
AI采样），每条含书目卡片、入选理由（附库内引文计数）、物理内容与关键公式。

| 目录 | 语言 | 文档类 |
|---|---|---|
| `Essential_Papers_on_Lattice_QCD_Parton_Physics_latex/` | EN | book |
| `格点QCD部分子物理精华论文选_latex/` | 中文 | ctexbook |

## 编译

```bash
cd <dir>/build && xelatex -interaction=nonstopmode -halt-on-error ../main.tex  # 两遍
```

- 成品：各目录 `build/main.pdf`（英文 36 页；中文 35 页）
- 结构：`main.tex` + `chapters/*.tex`；无图片依赖
- 注意：`\input{../chapters/...}` 相对路径要求在 `build/` 内编译
- 用户输入清单：`.agent.*.list`（会话原始记录）

## 选编依据

38 篇 = 14 篇库内原文里程碑 + 24 篇引文网络枢纽（每篇被库内 ≥3 篇引用，
多数 ≥8 篇）。书目信息转录自库内论文参考文献并交叉核对；不确定字段标 [?]。

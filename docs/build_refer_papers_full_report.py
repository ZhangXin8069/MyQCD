#!/usr/bin/env python3
"""Build a full-content Chinese book from the verified refer/papers corpus.

The existing ``build_refer_papers_report.py`` is intentionally a short Beamer
overview.  This generator has a different contract: it writes a long-form
``ctexbook`` whose analytical pages explain the common physics, then embeds
the complete rendered Chinese paper for every indexed paper.  The embedded
pages retain the equations, tables, captions, and prose already present in
the repository instead of replacing them with generated pseudo-content.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
PAPERS_DIR = ROOT / "refer" / "papers"
REPORT_STEM = "report_refer_papers_all_contents_20260830"
REPORT_PATH = DOCS_DIR / f"{REPORT_STEM}.tex"
MANIFEST_PATH = DOCS_DIR / f"{REPORT_STEM}.manifest.tsv"

sys.path.insert(0, str(DOCS_DIR))
from build_refer_papers_report import (  # noqa: E402
    TOPIC_INFO,
    Paper,
    build_papers,
    tex_escape,
)


@dataclass
class SourceRecord:
    paper_id: str
    title_zh: str
    title_en: str
    topic: str
    arxiv: str
    zh_dir: str
    en_dir: str
    indexed_zh_pages: int
    actual_pages: int
    sha256: str
    source_pdf: str
    section_titles: str
    abstract_excerpt: str
    method_excerpt: str
    result_excerpt: str
    evidence_state: str


def pdf_pages(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdfinfo 失败：{path}\n{result.stdout}\n{result.stderr}")
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"pdfinfo 未返回 Pages：{path}")
    return int(match.group(1))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_pdf(record: Paper) -> Path:
    return PAPERS_DIR / record.zh_dir / "build" / "main.pdf"


def audit_sources(records: Sequence[Paper]) -> tuple[list[tuple[Paper, Path, int]], list[str]]:
    audited: list[tuple[Paper, Path, int]] = []
    errors: list[str] = []
    for record in records:
        path = source_pdf(record)
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing:{path}")
            continue
        try:
            actual = pdf_pages(path)
        except RuntimeError as error:
            errors.append(str(error))
            continue
        audited.append((record, path, actual))
        if actual != record.zh_pages:
            errors.append(
                f"page_mismatch:{record.paper_id}:indexed={record.zh_pages}:actual={actual}"
            )
    return audited, errors


def print_audit(records: Sequence[Paper], audited: Sequence[tuple[Paper, Path, int]], errors: Sequence[str]) -> int:
    indexed_pages = sum(record.zh_pages for record in records)
    actual_pages = sum(actual for _, _, actual in audited)
    missing = sum(1 for record in records if not source_pdf(record).is_file())
    mismatches = sum(
        1 for record, _, actual in audited if record.zh_pages != actual
    )
    print(f"papers={len(records)}")
    print(f"indexed_zh_pages={indexed_pages} actual_zh_pages={actual_pages}")
    print(f"missing_source_pdf={missing}")
    print(f"page_mismatches={mismatches}")
    if errors:
        print("errors:")
        for error in errors:
            print(error)
        return 1
    return 0


def build_source_records(
    records: Sequence[Paper], audited: Sequence[tuple[Paper, Path, int]]
) -> list[SourceRecord]:
    by_id = {record.paper_id: (record, path, actual) for record, path, actual in audited}
    result: list[SourceRecord] = []
    for record in records:
        _, path, actual = by_id[record.paper_id]
        result.append(
            SourceRecord(
                paper_id=record.paper_id,
                title_zh=record.title_zh,
                title_en=record.title_en,
                topic=record.topic,
                arxiv=record.arxiv,
                zh_dir=record.zh_dir,
                en_dir=record.en_dir,
                indexed_zh_pages=record.zh_pages,
                actual_pages=actual,
                sha256=sha256(path),
                source_pdf=str(path.relative_to(ROOT)),
                section_titles=record.section_titles,
                abstract_excerpt=record.abstract_excerpt,
                method_excerpt=record.method_excerpt,
                result_excerpt=record.result_excerpt,
                evidence_state=record.evidence_state,
            )
        )
    return result


def write_manifest(records: Sequence[SourceRecord]) -> None:
    fields = list(asdict(records[0]).keys()) if records else list(SourceRecord.__annotations__)
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def clean_cell(value: str, limit: int = 1400) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1] + "……"


def path_tex(path: str) -> str:
    """Render a repository-relative source path from the docs directory."""

    rendered = tex_escape(f"../{path}")
    rendered = rendered.replace("/", r"/\allowbreak{}")
    rendered = rendered.replace(r"\_", r"\_\allowbreak{}")
    return rendered


def pdf_path_tex(path: str) -> str:
    """Render a literal PDF path so pdfpages can count every source page."""

    return f"../{path}"


def text_cell(value: str, limit: int = 1400) -> str:
    return tex_escape(clean_cell(value, limit))


def tabular_rows(rows: Sequence[tuple[str, str]]) -> str:
    lines = []
    for label, value in rows:
        lines.append(f"{tex_escape(label)} & {value} {chr(92) * 2}")
    return "\n".join(lines)


def two_column_table(caption: str, rows: Sequence[tuple[str, str]]) -> str:
    return "\n".join(
        [
            r"\begin{table}[htbp]",
            r"  \centering",
            rf"  \caption{{{tex_escape(caption)}}}",
            r"  \small",
            r"  \begin{tabularx}{0.96\textwidth}{@{}p{3.3cm}>{\raggedright\arraybackslash}X@{}}",
            r"    \toprule",
            "    " + tabular_rows(rows).replace("\n", "\n    "),
            r"    \bottomrule",
            r"  \end{tabularx}",
            r"\end{table}",
        ]
    )


def topic_intro(topic: str, records: Sequence[SourceRecord]) -> str:
    info = TOPIC_INFO[topic]
    names = "、".join(record.title_zh for record in records)
    return "\n".join(
        [
            rf"\chapter*{{主题主线：{tex_escape(info['short'])}}}",
            rf"\addcontentsline{{toc}}{{chapter}}{{主题主线：{tex_escape(info['short'])}}}",
            tex_escape(info["description"]),
            r"\begin{equation}",
            rf"  {info['formula']}",
            r"\end{equation}",
            rf"\noindent\textbf{{结构解释：}}{tex_escape(info['check'])}",
            two_column_table(
                f"{topic}：论文与物理接口",
                [
                    ("本主题论文", tex_escape(names)),
                    ("共同关系", tex_escape(info["relation"])),
                    ("证据状态", "确证：每篇论文的中文全文 PDF；推断：本主题的共同接口；未验证：跨论文统一数值结论。"),
                    ("阅读顺序", "先读本主题的结构式与边界，再读下列论文的逐章明文内容；不把主题结构式当作某一篇的原文编号。"),
                ],
            ),
        ]
    )


def paper_summary(record: SourceRecord) -> str:
    info = TOPIC_INFO[record.topic]
    title = f"{record.paper_id}：{record.title_zh}"
    method = text_cell(record.method_excerpt)
    result = text_cell(record.result_excerpt)
    sections = text_cell(record.section_titles, 2200)
    source_display = path_tex(record.source_pdf)
    source_pdf = pdf_path_tex(record.source_pdf)
    rows = [
        ("论文来源", tex_escape(record.arxiv)),
        ("主题归属", tex_escape(record.topic)),
        ("中文全文页数", f"{record.actual_pages} 页（索引值与实测值一致）"),
        ("章节入口", sections or "源文件未提供可压缩的章节标题"),
        ("公式主线", "$" + info["formula"] + r"$\newline\scriptsize 结构式仅用于连接本篇与主题，不替代下方全文中的原文公式。"),
        ("全文证据", rf"{source_display}；SHA-256 见机器可读 manifest。"),
    ]
    workflow_rows = [
        ("输入/问题", text_cell(record.abstract_excerpt, 1800)),
        ("方法/推导", method),
        ("结果/讨论", result),
        ("物理边界", tex_escape(info["check"])),
        ("内容状态", tex_escape(record.evidence_state)),
    ]
    workflow_tex = "\n    ".join(
        rf"\textbf{{{tex_escape(label)}}}\quad {value} {chr(92) * 2}"
        for label, value in workflow_rows
    )
    return "\n".join(
        [
            rf"\chapter{{{tex_escape(title)}}}",
            r"\section*{本篇不是摘要卡片：总结接口与明文正文}",
            "本页先给出本篇正文的阅读接口；随后嵌入该篇中文全文的已构建 PDF。嵌入部分保留源文的散文、公式、表格、图注、附录和参考文献，不用生成式文字替换原始内容。",
            two_column_table(f"{title}：内容档案", rows),
            r"\begin{table}[htbp]",
            r"  \centering",
            rf"  \caption*{{{tex_escape(title)}：输入—推导—结果—边界的单列表格}}",
            r"  \small",
            r"  \begin{tabular}{@{}p{0.96\textwidth}@{}}",
            r"    \toprule",
            "    " + workflow_tex,
            r"    \bottomrule",
            r"  \end{tabular}",
            r"\end{table}",
            r"\section*{明文内容入口}",
            rf"\noindent 完整渲染页从下一页开始：{source_display}。页数证据为 {record.actual_pages} 页；对应的原始中文 TeX 目录为 \emph{{{tex_escape(record.zh_dir)}}}。",
            r"\clearpage",
            rf"\includepdf[pages=1-{record.actual_pages},fitpaper=true,pagecommand={{\thispagestyle{{plain}}}}]{{{source_pdf}}}",
            r"\clearpage",
        ]
    )


def front_matter(records: Sequence[SourceRecord]) -> str:
    zh_pages = sum(record.actual_pages for record in records)
    topic_rows = []
    for topic in TOPIC_INFO:
        group = [record for record in records if record.topic == topic]
        topic_rows.append(
            (
                topic,
                f"{len(group)} 篇；嵌入全文 {sum(record.actual_pages for record in group)} 页；" + tex_escape(TOPIC_INFO[topic]["short"]),
            )
        )
    return "\n".join(
        [
            r"\frontmatter",
            r"\begin{titlepage}",
            r"  \centering",
            r"  \vspace*{2.0cm}",
            r"  {\Huge\bfseries refer/papers 全量论文明文内容总结\\[0.8em]}",
            r"  {\Large 格点 QCD、部分子物理与数值方法\\[1.4em]}",
            r"  {\large 以公式、推导、表格和逐篇全文为主}",
            r"  \vfill",
            r"  {\large 2026 年 8 月 30 日\\[0.5em]}",
            r"  {\normalsize 生成入口：docs/build\_refer\_papers\_full\_report.py}",
            r"\end{titlepage}",
            r"\chapter*{编者说明：这里的“全量总结”是什么意思}",
            "本报告不是把论文压缩为标题、摘要或入选理由。它先用统一的物理主线说明每篇论文在格点可计算量、重正化、因子化、演化和物理输出中的位置，再按索引顺序嵌入 50 篇中文全文的已构建页面。因此，正文中可见的公式、表格、图注、附录与散文均来自当前工作区的中文译本构建结果；新增的跨论文文字只标作综合判断或结构式。",
            "由于当前工作区的论文目录以中文/英文 LaTeX 转排及其构建 PDF 为直接证据，本报告不声称重新下载或独立复现论文的外部 PDF、原始数据和数值结果。任何跨论文统一数值结论均列为未验证。",
            two_column_table(
                "报告范围与证据边界",
                [
                    ("纳入对象", "refer/papers/INDEX.md 中的 50 篇论文；英中目录对去重。"),
                    ("直接明文", f"50 个中文译本 build/main.pdf；实际嵌入 {zh_pages} 页。"),
                    ("辅助参考", "refer/books/ 中的格点 QCD、QFT 与 Wilson 禁闭转排，用于基础定义、欧氏路径积分、规范场、禁闭和部分子背景。"),
                    ("不作替代", "本报告不是对外部原始 PDF 的逐页校勘，也不是原始数据再分析；源目录缺失的内容保持未验证。"),
                ],
            ),
            r"\chapter*{全库物理主线：从欧氏格点到部分子观测量}",
            "全库内容可沿一条受对称性和尺度控制的链条阅读：先在欧氏格点上保持局域规范不变性，再用流、涂抹和重正化处理紫外结构，随后用大动量或短距离因子化把等时空间关联连接到光锥部分子分布，最后将 PDF/TMD 或采样系综与物理可观测量相比较。",
            r"\begin{align}",
            r"  Z[J] &= \int \mathcal D\phi\,\exp[-S_E[\phi]+J\phi], \\ ",
            r"  U_\mu(x) &= \exp\!\left[iag A_\mu\!\left(x+\tfrac{a}{2}\hat\mu\right)\right], \\ ",
            r"  \partial_t B_\mu(t,x) &= D_\nu G_{\nu\mu}(t,x), \qquad t\sim L_{\rm sm}^{2}, \\ ",
            r"  O^{R}(z,\mu) &= Z(z,\mu,a)\,O^{\rm bare}(z,a), \\ ",
            r"  \widetilde q(x,P_z,\mu) &= \int dy\,C(x,y,\mu/P_z)q(y,\mu)+\mathcal O(\Lambda_{\rm QCD}^{2}/P_z^{2}), \\ ",
            r"  \mathcal O_{\rm Euclid} &\xrightarrow[\rm matching/evolution]{} f_{g/h}(x,\mu)\;\text{或}\;F_{\rm TMD}(x,b_T,\mu,\zeta).",
            r"\end{align}",
            r"\noindent 这些是跨论文阅读的结构式；每篇的精确约定、阶数、方案和误差必须以随后嵌入的原文为准。",
            two_column_table("主题规模", topic_rows),
            r"\chapter*{辅助参考的用法}",
            "辅助书籍不替代论文正文，而是用来固定阅读所需的底层定义。格点 QCD 导论提供 Wick 转动、欧氏路径积分、链接变量、局域规范变换、关联函数和谱提取；Gattringer–Lang 转排补充格点作用量、费米子、强子谱和数值实现；Peskin–Schroeder 的非阿贝尔规范章节补充协变导数、场强、规范玻色子相互作用和渐近自由；Wilson 禁闭转排提供格点规范理论的历史起点。",
            two_column_table(
                "辅助来源入口",
                [
                    ("格点 QCD 导论", path_tex("refer/books/格点QCD导论_latex/chapters/sec05_minkowski_euclidean.tex") + "；" + path_tex("refer/books/格点QCD导论_latex/chapters/sec06_formulation_gauge.tex")),
                    ("禁闭与渐近自由", path_tex("refer/books/格点QCD导论_latex/chapters/sec14_confinement.tex") + "；" + path_tex("refer/books/夸克禁闭_latex/main.tex")),
                    ("格点规范专著", path_tex("refer/books/Quantum_Chromodynamics_on_the_Lattice_latex/chapters/chapter01.tex") + "；" + path_tex("refer/books/Quantum_Chromodynamics_on_the_Lattice_latex/chapters/chapter06.tex")),
                    ("非阿贝尔 QFT", path_tex("refer/books/量子场论导论_latex/chapters/ch15.tex") + "；" + path_tex("refer/books/量子场论导论_latex/chapters/ch16.tex")),
                ],
            ),
            r"\tableofcontents",
            r"\mainmatter",
        ]
    )


def generate_tex(records: Sequence[SourceRecord]) -> int:
    grouped = {topic: [record for record in records if record.topic == topic] for topic in TOPIC_INFO}
    preamble = r"""% ============================================================
% refer/papers 全量论文明文内容总结
% 生成器：docs/build_refer_papers_full_report.py
% 编译：cd docs && xelatex -interaction=nonstopmode -halt-on-error report_refer_papers_all_contents_20260830.tex
% ============================================================
\documentclass[UTF8,11pt,oneside]{ctexbook}
\usepackage[a4paper,margin=2.55cm]{geometry}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{tabularx}
\usepackage{caption}
\usepackage{pdfpages}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage{xcolor}
\setCJKmainfont{AR PL UMing CN}
\setCJKsansfont{Droid Sans Fallback}
\setCJKmonofont{Droid Sans Fallback}
\linespread{1.05}
\setlength{\parskip}{0.35\baselineskip}
\setlength{\parindent}{2em}
\setlength{\emergencystretch}{3em}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{refer/papers 全量论文明文内容总结}
\fancyhead[R]{\leftmark}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\hypersetup{pdftitle={refer/papers 全量论文明文内容总结},pdfauthor={Codex}}
\begin{document}
"""
    chunks = [preamble, front_matter(records)]
    for topic in TOPIC_INFO:
        group = grouped[topic]
        if not group:
            continue
        chunks.append(rf"\part{{{tex_escape(TOPIC_INFO[topic]['short'])}}}")
        chunks.append(topic_intro(topic, group))
        for record in group:
            chunks.append(paper_summary(record))
    chunks.append(
        "\n".join(
            [
                r"\backmatter",
                r"\chapter*{全库交叉结论与验证边界}",
                "本卷的跨论文主线是由源文本中反复出现的对象和尺度关系归纳而来：规范不变性保证格点对象可定义，流/涂抹和重正化处理短距离结构，LaMET/赝 PDF/TMD 因子化承担欧氏到光锥的桥梁，最终输出必须经过动量、格距、体积、流时间或距离、匹配阶数、激发态和采样相关性的分层检验。",
                two_column_table(
                    "交叉验证清单",
                    [
                        ("对称性", "检查局域规范变换、离散对称性和规范协变结构；不以形式相似替代具体算符验证。"),
                        ("量纲与极限", tex_escape("检查 a→0、P_z→∞、z→0、t→0、b_T→0 或大距离极限；每种极限的适用范围由单篇论文确定。")),
                        ("数值证据", "本报告嵌入源目录已经构建的 PDF，但没有在本次任务中重新运行论文原始数据分析；统一数值比较保持未验证。"),
                        ("可复查入口", f"逐篇页数、源 PDF 路径和 SHA-256 见 {path_tex(str(MANIFEST_PATH.relative_to(ROOT)))}。"),
                    ],
                ),
                r"\chapter*{机器可读来源清单}",
                f"本报告的来源清单为 {path_tex(str(MANIFEST_PATH.relative_to(ROOT)))}。它记录 50 篇论文的唯一编号、主题、索引页数、实际嵌入页数、源 PDF 路径和 SHA-256；生成器只读取当前工作区，不修改 refer/papers 源目录。",
                r"\end{document}",
            ]
        )
    )
    REPORT_PATH.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    return sum(record.actual_pages for record in records)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--audit", action="store_true")
    mode.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    records = build_papers()
    audited, errors = audit_sources(records)
    if args.audit:
        return print_audit(records, audited, errors)
    if errors:
        print_audit(records, audited, errors)
        return 1
    source_records = build_source_records(records, audited)
    write_manifest(source_records)
    embedded_pages = generate_tex(source_records)
    print(f"papers={len(source_records)}")
    print(f"embedded_zh_pages={embedded_pages}")
    print(f"manifest={MANIFEST_PATH}")
    print(f"tex={REPORT_PATH}")
    print("full_content_mode=50 Chinese full-text PDFs embedded after per-paper formula-led summaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

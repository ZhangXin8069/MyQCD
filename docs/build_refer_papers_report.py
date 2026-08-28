#!/usr/bin/env python3
"""Build a traceable long-form summary of the refer/papers LaTeX corpus.

The script deliberately uses only the Python standard library.  It reads the
existing English/Chinese conversion pairs, writes a compact TSV manifest, and
renders a fixed-frame Chinese Beamer report.  Scientific claims are sourced
from the existing LaTeX text; topic formulae are explicitly marked as
structural schematics rather than paper-specific numerical results.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "refer" / "papers"
INDEX_PATH = PAPERS_DIR / "INDEX.md"
DOCS_DIR = ROOT / "docs"
MANIFEST_PATH = DOCS_DIR / "report_refer_papers_all_20260828.manifest.tsv"
REPORT_PATH = DOCS_DIR / "report_refer_papers_all_20260828.tex"


TOPIC_INFO = {
    "格点规范基础": {
        "short": "格点规范理论与禁闭",
        "description": "从规范不变离散化、Wilson 圈和强耦合结构出发，建立欧氏格点上的规范场、夸克传播与禁闭图像。",
        "formula": r"\langle W(C)\rangle\sim\exp[-\sigma A(C)]",
        "check": "量纲检查：σ 具有面积倒数维度；大圈极限把面积律与线性势联系起来。",
        "relation": "为后续梯度流、重正化和部分子算符提供规范不变的格点底座。",
    },
    "梯度流与能动量张量": {
        "short": "梯度流、涂抹与能动量张量",
        "description": "用流时间平滑短距离涨落，在保持规范协变性的同时构造可控的复合算符、耦合、质量和能动量张量。",
        "formula": r"\partial_t B_\mu(t,x)=D_\nu G_{\nu\mu}(t,x),\qquad t\sim L_{\rm sm}^{2}",
        "check": "流时间与平滑长度满足平方关系；t→0 回到原始场，有限 t 则抑制紫外模式。",
        "relation": "把连续极限、微扰有限性和能动量张量重构连接到可计算的格点观测量。",
    },
    "LaMET、准 PDF 与赝 PDF": {
        "short": "LaMET、准分布与赝分布",
        "description": "以大动量强子和等时空间关联替代直接光锥算符，通过有效场论匹配与演化提取部分子信息。",
        "formula": r"\widetilde q(x,P_z,\mu)=\int dy\,C(x,y,\mu/P_z)q(y,\mu)+\mathcal O(\Lambda_{\rm QCD}^{2}/P_z^{2})",
        "check": "大动量极限 P_z→∞ 压低幂修正；有限动量、有限间距和核子激发态是必须单独控制的误差源。",
        "relation": "承接格点矩阵元，向重正化、匹配、演化和最终 PDF/TMD 现象学输出。",
    },
    "重正化与匹配": {
        "short": "非微扰重正化、OPE 与匹配",
        "description": "处理 Wilson 线自能、线性发散、算符混合和方案转换，建立格点裸矩阵元与连续方案物理分布之间的桥梁。",
        "formula": r"O^{R}(z,\mu)=Z(z,\mu,a)\,O^{\rm bare}(z,a)",
        "check": "重正化因子抵消截止依赖；a→0 和短距离 z→0 极限必须与匹配阶数、方案和尺度保持一致。",
        "relation": "是准/赝分布从格点数据走向 MS-bar 或其他连续方案的必要中间层。",
    },
    "胶子、强子 PDF 与 TMD": {
        "short": "胶子、强子部分子分布与 TMD",
        "description": "把上述格点工具应用到胶子、核子、π/K 介子和横向动量依赖结构，并与全局拟合或 Collins–Soper 演化衔接。",
        "formula": r"\mathcal O_{\rm Euclid}\xrightarrow[\rm matching\,/\,evolution]{}f_{g/h}(x,\mu)\;{\rm or}\;F_{\rm TMD}(x,b_T,\mu,\zeta)",
        "check": "纵向分数、横向距离和重正化尺度是不同变量；不能把有限动量或有限 b_T 的结果直接当作光锥分布。",
        "relation": "检验 LaMET/赝 PDF/准 TMD 方法是否能够覆盖真实强子结构与实验拟合所需的观测量。",
    },
    "机器学习采样与随机量化": {
        "short": "机器学习采样与随机量化",
        "description": "以流模型、规范等变结构、扩散过程或随机量化改造格点场配置生成与采样，关注可逆性、规范对称性和分布一致性。",
        "formula": r"z\sim p(z),\qquad U=f_\theta(z),\qquad p_\theta(U)\;\text{与目标系综比较}",
        "check": "规范不变性/等变性是结构约束；采样质量须由可观测量、接受率、自相关或分布距离验证，不能只看训练损失。",
        "relation": "为大规模格点系综生成提供算法补充，但必须回到物理可观测量和系综正确性检验。",
    },
}


@dataclass
class Paper:
    paper_id: str
    title_zh: str
    title_en: str
    en_dir: str
    zh_dir: str
    arxiv: str
    en_pages: int
    zh_pages: int
    source: str
    note: str
    topic: str
    section_titles: str
    abstract_excerpt: str
    method_excerpt: str
    result_excerpt: str
    method_source: str
    result_source: str
    source_files: str
    evidence_state: str
    zh_lines: int
    en_lines: int
    formula_hits: int
    figure_hits: int
    table_hits: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def clean_markdown_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("`", "").strip())


def parse_index() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for line in read_text(INDEX_PATH).splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 7 or not re.fullmatch(r"\d+", cells[1]):
            continue
        en_pages_match = re.search(r"\d+", cells[4])
        zh_pages_match = re.search(r"\d+", cells[5])
        if not en_pages_match or not zh_pages_match:
            raise ValueError(f"INDEX.md 页数无法解析：{line}")
        rows.append(
            {
                "paper_id": f"P{int(cells[1]):02d}",
                "en_dir": clean_markdown_cell(cells[2]),
                "zh_dir": clean_markdown_cell(cells[3]),
                "en_pages": int(en_pages_match.group()),
                "zh_pages": int(zh_pages_match.group()),
                "source": clean_markdown_cell(cells[6]),
                "note": clean_markdown_cell(cells[7]) if len(cells) > 7 else "",
            }
        )
    if len(rows) != 50:
        raise ValueError(f"INDEX.md 应有 50 篇论文，实际解析 {len(rows)} 篇")
    return rows


def balanced_command_arguments(text: str, names: Sequence[str]) -> Iterable[tuple[str, str, int, int]]:
    name_pattern = "|".join(re.escape(name) for name in names)
    pattern = re.compile(rf"\\({name_pattern})\*?(?:\[[^\]]*\])?\s*\{{")
    for match in pattern.finditer(text):
        start = match.end() - 1
        depth = 0
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    yield match.group(1), text[start + 1 : index], match.start(), index + 1
                    break


def remove_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def replace_unescaped_delimited(text: str, opener: str, closer: str, replacement: str) -> str:
    """Replace paired delimiters without regex backtracking.

    TeX line breaks written as two backslashes followed by an optional
    spacing bracket are not display-math openers. Skipping an opener preceded
    by a backslash handles that case and malformed source terminates
    deterministically.
    """

    chunks: list[str] = []
    position = 0
    while position < len(text):
        start = text.find(opener, position)
        if start < 0:
            chunks.append(text[position:])
            break
        if start > 0 and text[start - 1] == "\\":
            position = start + len(opener)
            continue
        chunks.append(text[position:start])
        end = text.find(closer, start + len(opener))
        if end < 0:
            chunks.append(replacement)
            position = len(text)
            break
        chunks.append(replacement)
        position = end + len(closer)
    return "".join(chunks)


def replace_single_math(text: str, replacement: str = " [公式] ") -> str:
    """Replace paired, unescaped single-dollar math delimiters linearly."""

    chunks: list[str] = []
    position = 0
    while position < len(text):
        start = text.find("$", position)
        if start < 0:
            chunks.append(text[position:])
            break
        if (start > 0 and text[start - 1] == "\\") or (
            start + 1 < len(text) and text[start + 1] == "$"
        ):
            chunks.append(text[position : start + 1])
            position = start + 1
            continue
        end = start + 1
        while end < len(text):
            end = text.find("$", end)
            if end < 0:
                chunks.append(text[position:])
                position = len(text)
                break
            if text[end - 1] != "\\" and (end + 1 >= len(text) or text[end + 1] != "$"):
                chunks.append(text[position:start])
                chunks.append(replacement)
                position = end + 1
                break
            end += 1
        else:
            chunks.append(text[position:])
            position = len(text)
    return "".join(chunks)


def replace_balanced_commands(
    text: str,
    names: Sequence[str],
    replacement: str,
) -> str:
    """Replace custom commands whose braced argument contains a formula."""

    matches = list(balanced_command_arguments(text, names))
    for _, _, start, end in reversed(matches):
        text = text[:start] + replacement + text[end:]
    return text


def clean_tex(text: str) -> str:
    """Convert source TeX into compact prose for a text-only report cell."""

    text = remove_comments(text)
    for environment in (
        "figure",
        "figure*",
        "table",
        "table*",
        "tabular",
        "tabularx",
        "equation",
        "equation*",
        "align",
        "align*",
        "eqnarray",
        "gather",
        "gather*",
        "multline",
        "verbatim",
        "lstlisting",
    ):
        pattern = rf"\\begin\{{{re.escape(environment)}\}}.*?\\end\{{{re.escape(environment)}\}}"
        text = re.sub(pattern, " [公式/图表] ", text, flags=re.DOTALL)

    text = re.sub(r"\\(?:cite|citep|citet|parencite|textcite)\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}", " [引文] ", text)
    text = re.sub(r"\\(?:ref|eqref|autoref)\s*\{[^{}]*\}", " [交叉引用] ", text)
    text = replace_unescaped_delimited(text, r"\(", r"\)", " [公式] ")
    text = replace_unescaped_delimited(text, r"\[", r"\]", " [公式] ")
    text = replace_unescaped_delimited(text, "$$", "$$", " [公式] ")
    text = replace_single_math(text)
    text = replace_balanced_commands(text, ("equation",), " [公式] ")

    # Common TeX text accents and escaped spaces should remain readable after
    # the math blocks have been removed.  Without this pass, e.g. ``M\\"uller``
    # would be rendered as a literal backslash in the generated report.
    accent_replacements = {
        r'\"a': "ä", r'\"o': "ö", r'\"u': "ü",
        r'\"A': "Ä", r'\"O': "Ö", r'\"U': "Ü",
        r"\\'e": "é", r"\\'E": "É", r"\\`e": "è", r"\\`E": "È",
        r"\~n": "ñ", r"\~N": "Ñ",
    }
    for source, replacement in accent_replacements.items():
        text = text.replace(source, replacement)
    text = text.replace("\\" + "'" + "e", "é")
    text = text.replace("\\" + "'" + "E", "É")
    text = text.replace("\\" + chr(96) + "e", "è")
    text = text.replace("\\" + chr(96) + "E", "È")
    text = text.replace("\\" + "^" + "o", "ô")
    text = text.replace("\\" + "^" + "O", "Ô")
    text = text.replace(r"\ ", " ")
    text = re.sub(r"\\+\s+", " ", text)
    text = text.replace(r"\/", "/")
    for spacing_command in (r"\,", r"\;", r"\:", r"\!", r"\quad", r"\qquad"):
        text = text.replace(spacing_command, " ")

    # Unwrap common one-argument formatting commands.  Repeating the pass
    # handles nested \textbf{\emph{...}} without trying to parse all TeX.
    wrappers = re.compile(
        r"\\(?:textbf|textit|textrm|textsf|texttt|emph|underline|mathrm|mathbf|mathit|operatorname|mbox|texorpdfstring)"
        r"(?:\[[^\]]*\])?\s*\{([^{}]*)\}"
    )
    previous = None
    while previous != text:
        previous = text
        text = wrappers.sub(r"\1", text)
    text = re.sub(r"\\[A-Za-z@]+\s*(?:\[[^\]]*\])?", " ", text)
    text = text.replace("\\%", "%").replace("\\&", "&").replace("\\_", "_")
    text = re.sub(r"\\+(?=\s|[,.;:!?])", " ", text)
    # At this point the value is prose rather than TeX.  Drop any residual
    # control characters from conversion-specific macros instead of exposing
    # them through tex_escape as \textbackslash{} or \textasciicircum{}.
    text = text.replace("\\", " ").replace("^", "")
    text = text.replace("\\\\", " ").replace("{", " ").replace("}", " ")
    text = text.replace("~", " ").replace("---", "—").replace("--", "–")
    text = re.sub(r"https?://\S+", "[链接]", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" [公式/图表] ", "（公式或图表位置）")
    text = text.replace(" [公式] ", "（公式）").replace(" [引文] ", "（引文）")
    text = text.replace(" [交叉引用] ", "（交叉引用）")
    return text.strip(" \t\r\n，。;；")


def compact(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "未验证：源文件未提供可用的散文摘录。"
    if len(text) <= limit:
        return text
    first = max(1, int(limit * 0.68))
    last = max(1, limit - first - 8)
    return f"{text[:first]}……{text[-last:]}"


def title_from_main(main_text: str, fallback: str) -> str:
    matches = list(balanced_command_arguments(main_text, ("title",)))
    if not matches:
        return fallback
    title = clean_tex(matches[0][1])
    return compact(title, 160) if title else fallback


def abstract_from_dir(directory: Path) -> str:
    candidates = [directory / "main.tex"] + sorted((directory / "chapters").glob("*.tex"))
    for path in candidates:
        if not path.exists():
            continue
        text = read_text(path)
        match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, flags=re.DOTALL)
        if match:
            value = clean_tex(match.group(1))
            if value:
                return value
    # Several conversions preserve a published-PDF title block instead of an
    # abstract environment.  Prefer the explicit Chinese abstract marker so
    # spacing commands and author metadata do not enter the excerpt.
    main = directory / "main.tex"
    if main.exists():
        text = read_text(main)
        document_body = text.split(r"\begin{document}", 1)[-1]
        document_body = document_body.split(r"\input{chapters/section01}", 1)[0]
        marker = re.search(r"(?:\\(?:subsection|section)\*?\{摘要\}|摘要)", document_body)
        if marker:
            tail = document_body[marker.end() :]
            stop = re.search(r"\\(?:vspace|noindent\\rule|input)\b", tail)
            if stop:
                tail = tail[: stop.start()]
            value = clean_tex(tail)
            if value:
                return value
        minipage = re.search(r"\\begin\{minipage\}.*?(.*?)\\end\{minipage\}", document_body, flags=re.DOTALL)
        if minipage:
            value = clean_tex(minipage.group(1))
            if value:
                return value
        value = clean_tex(document_body)
        if value:
            return value
    return "未验证：源文件未提供可识别的摘要环境。"


def chapter_sort_key(path: Path) -> tuple[int, int, str]:
    stem = path.stem.lower()
    if stem.startswith(("section", "zh")):
        priority = 0
    elif stem.startswith(("abstract", "backmatter")):
        priority = 2
    else:
        priority = 1
    number_match = re.search(r"(\d+)", stem)
    number = int(number_match.group(1)) if number_match else 9999
    return priority, number, stem


def chapter_entries(directory: Path) -> list[dict[str, str | int]]:
    entries: list[dict[str, str | int]] = []
    chapter_dir = directory / "chapters"
    paths = sorted(chapter_dir.glob("*.tex"), key=chapter_sort_key) if chapter_dir.exists() else []
    for path in paths:
        text = read_text(path)
        commands = list(balanced_command_arguments(text, ("section", "subsection", "subsubsection", "paragraph")))
        for position, (kind, title, start, end) in enumerate(commands):
            body_end = commands[position + 1][2] if position + 1 < len(commands) else len(text)
            body = clean_tex(text[end:body_end])
            entries.append(
                {
                    "kind": kind,
                    "title": compact(clean_tex(title), 180),
                    "body": body,
                    "file": str(path.relative_to(directory)),
                    "line": text[:start].count("\n") + 1,
                    "end_line": text[:body_end].count("\n") + 1,
                }
            )
        custom_commands = list(re.finditer(r"\\(lussec|lussubsec|lusapp)\b", text))
        for position, match in enumerate(custom_commands):
            body_end = custom_commands[position + 1].start() if position + 1 < len(custom_commands) else len(text)
            after = text[match.end() :]
            header_match = re.match(r"[ \t]*([^\n]+)", after)
            if not header_match:
                continue
            header = re.sub(r"\\par\s*$", "", header_match.group(1)).strip()
            if match.group(1) == "lussubsec":
                title_match = re.match(r"\S+\s+(.*)", header)
                kind = "subsection"
            else:
                title_match = re.match(r"\S+\.\s*(.*)", header)
                kind = "section"
            if not title_match:
                continue
            body_start = match.end() + header_match.end()
            body = clean_tex(text[body_start:body_end])
            entries.append(
                {
                    "kind": kind,
                    "title": compact(clean_tex(title_match.group(1)), 180),
                    "body": body,
                    "file": str(path.relative_to(directory)),
                    "line": text[: match.start()].count("\n") + 1,
                    "end_line": text[:body_end].count("\n") + 1,
                }
            )
        if not commands and not custom_commands and path.stem.lower() not in {"abstract", "backmatter", "backmatter_head", "backmatter_zh"}:
            body = clean_tex(text)
            if len(body) > 40:
                entries.append(
                    {
                        "kind": "file",
                        "title": path.stem,
                        "body": body,
                        "file": str(path.relative_to(directory)),
                        "line": 1,
                        "end_line": text.count("\n") + 1,
                    }
                )
    return entries


def compact_tail(text: str, limit: int) -> str:
    """Keep the end of a long source block for conclusion-style excerpts."""

    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "未验证：源文件未提供可用的散文摘录。"
    if len(text) <= limit:
        return text
    return f"……{text[-max(1, limit - 1):]}"


def choose_entry(
    entries: Sequence[dict[str, str | int]],
    patterns: Sequence[str],
    fallback: str,
    *,
    prefer_tail: bool = False,
) -> tuple[str, str]:
    regex = re.compile("|".join(patterns), flags=re.IGNORECASE)
    usable = [
        entry
        for entry in entries
        if not re.search(r"致谢|acknowledg|thebibliography|bibliography|参考文献|references", str(entry["title"]), flags=re.IGNORECASE)
        and not re.search(r"(?:^|/)(?:backmatter|backmatter_[^/]+|.*bibliograph.*|.*references?)\.tex$", str(entry["file"]), flags=re.IGNORECASE)
    ]
    for entry in usable:
        title = str(entry["title"])
        body = str(entry["body"])
        if regex.search(title) and len(body) > 40:
            source = f"{entry['file']}:{entry['line']}-{entry['end_line']}"
            return compact(body, 900), source
    for entry in usable:
        body = str(entry["body"])
        if len(body) > 40:
            source = f"{entry['file']}:{entry['line']}-{entry['end_line']}"
            excerpt = compact_tail(body, 900) if prefer_tail else compact(body, 900)
            return excerpt, source
    return fallback, "未验证：没有可用章节正文"


def topic_for(text: str) -> str:
    lowered = text.lower()
    if re.search(r"扩散|随机量化|生成模型|等变|采样|mcmc|equivariant|diffusion|flow_sampling|generative", lowered):
        return "机器学习采样与随机量化"
    if re.search(r"tmd|collins|soft.function|软函数|准tmd|波函数", lowered):
        return "胶子、强子 PDF 与 TMD"
    if re.search(r"任意阶.*矩|gradient|梯度流|威尔逊流|wilson.flow|能动量张量|energy.momentum", lowered):
        return "梯度流与能动量张量"
    if re.search(r"重正化|renorm|renormal|匹配|matching|ope|operator.*multiplicative|幂修正|renormalon", lowered):
        return "重正化与匹配"
    if re.search(r"ct18|nnpdf|全局分析|global.analysis|pion|π介子|kaon|k介子|核子胶子|gluon.pdf|胶子部分子", lowered):
        return "胶子、强子 PDF 与 TMD"
    if re.search(r"lamet|大动量|quasi|准分布|赝|pseudo|parton.physics|lightcone|光锥", lowered):
        return "LaMET、准 PDF 与赝 PDF"
    return "格点规范基础"


def count_hits(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def build_papers() -> list[Paper]:
    records: list[Paper] = []
    for raw in parse_index():
        en_path = PAPERS_DIR / str(raw["en_dir"])
        zh_path = PAPERS_DIR / str(raw["zh_dir"])
        en_main_path = en_path / "main.tex"
        zh_main_path = zh_path / "main.tex"
        if not en_main_path.exists() or not zh_main_path.exists():
            raise FileNotFoundError(f"缺少英中 main.tex：{en_main_path} / {zh_main_path}")

        en_main = read_text(en_main_path)
        zh_main = read_text(zh_main_path)
        zh_title_fallback = str(raw["zh_dir"]).removesuffix("_latex")
        en_title_fallback = str(raw["en_dir"]).removesuffix("_latex").replace("_", " ")
        title_zh = zh_title_fallback
        title_en = title_from_main(en_main, en_title_fallback)
        zh_entries = chapter_entries(zh_path)
        section_titles = "；".join(
            f"{entry['title']}"
            for entry in zh_entries
            if entry["kind"] in {"section", "subsection"}
            and not re.search(
                r"致谢|acknowledg|thebibliography|bibliography|参考文献|references",
                str(entry["title"]),
                flags=re.IGNORECASE,
            )
        )
        section_titles = compact(section_titles, 820)
        abstract = compact(abstract_from_dir(zh_path), 900)
        method_excerpt, method_source = choose_entry(
            zh_entries,
            ("理论", "方法", "框架", "设定", "定义", "模拟", "矩阵元", "factorization", "formalism", "setup"),
            "未验证：源文件未提供可用的方法章节摘录。",
        )
        result_excerpt, result_source = choose_entry(
            list(reversed(zh_entries)),
            ("总结", "结论", "结果", "讨论", "展望", "结束语", "结语", "summary", "conclusion", "result", "discussion"),
            "未验证：源文件未提供可用的结果/结论章节摘录。",
            prefer_tail=True,
        )
        zh_files = sorted(zh_path.rglob("*.tex"))
        en_files = sorted(en_path.rglob("*.tex"))
        all_zh = "\n".join(read_text(path) for path in zh_files)
        all_en = "\n".join(read_text(path) for path in en_files)
        all_titles = f"{title_zh} {title_en} {section_titles}"
        topic = topic_for(all_titles)
        source_files = ";".join(
            str(path.relative_to(ROOT)) for path in zh_files + en_files
        )
        evidence_state = "确证：中文/英文 LaTeX 正文、章节和索引可追溯；未验证：当前目录未提供论文 PDF、原始数据或独立复现。"
        records.append(
            Paper(
                paper_id=str(raw["paper_id"]),
                title_zh=title_zh,
                title_en=title_en,
                en_dir=str(raw["en_dir"]),
                zh_dir=str(raw["zh_dir"]),
                arxiv=str(raw["source"]),
                en_pages=int(raw["en_pages"]),
                zh_pages=int(raw["zh_pages"]),
                source=str(raw["source"]),
                note=str(raw["note"]),
                topic=topic,
                section_titles=section_titles,
                abstract_excerpt=abstract,
                method_excerpt=method_excerpt,
                result_excerpt=result_excerpt,
                method_source=method_source,
                result_source=result_source,
                source_files=source_files,
                evidence_state=evidence_state,
                zh_lines=sum(len(read_text(path).splitlines()) for path in zh_files),
                en_lines=sum(len(read_text(path).splitlines()) for path in en_files),
                formula_hits=count_hits(all_zh, r"\\begin\{(?:equation|align|eqnarray|gather|multline)\*?\}"),
                figure_hits=count_hits(all_zh, r"\\(?:begin\{figure|includegraphics)"),
                table_hits=count_hits(all_zh, r"\\(?:begin\{table|begin\{tabular|begin\{tabularx)") ,
            )
        )
    return records


def write_manifest(records: Sequence[Paper], path: Path = MANIFEST_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(asdict(records[0]).keys()) if records else list(Paper.__annotations__.keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def tex_escape(value: object) -> str:
    mapping = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "σ": r"$\sigma$",
        "π": r"$\pi$",
    }
    return "".join(mapping.get(char, char) for char in str(value))


def source_tex(path: str) -> str:
    parts = re.split(r"([σπ])", path)
    rendered: list[str] = []
    for part in parts:
        if part == "σ":
            rendered.append(r"$\sigma$")
        elif part == "π":
            rendered.append(r"$\pi$")
        elif part:
            rendered.append(rf"\detokenize{{{part}}}")
    return "".join(rendered)


def source_pair(record: Paper, detail: str) -> str:
    zh = f"refer/papers/{record.zh_dir}/{detail}"
    en = f"refer/papers/{record.en_dir}/{detail}"
    return f"{source_tex(zh)}；{source_tex(en)}"


def row_table(rows: Sequence[tuple[str, str]]) -> str:
    rendered = [r"\begingroup", r"\renewcommand{\arraystretch}{0.84}", r"\begin{tabularx}{0.98\linewidth}{@{}p{2.55cm}>{\raggedright\arraybackslash}X@{}}", r"\toprule"]
    for label, value in rows:
        rendered.append(f"{tex_escape(label)} & {value} " + r"\\")
    rendered.extend([r"\bottomrule", r"\end{tabularx}", r"\endgroup"])
    return "\n".join(rendered)


def topic_counts(records: Sequence[Paper]) -> dict[str, int]:
    counts = {topic: 0 for topic in TOPIC_INFO}
    for record in records:
        counts[record.topic] += 1
    return counts


def frame_manifest(frame_id: str, claim_id: str, visual_type: str, page: int, paper_id: str = "") -> str:
    return (
        f"%% frame_manifest|frame_id={frame_id}|paper_id={paper_id or 'GLOBAL'}|claim_id={claim_id}"
        f"|visual_type={visual_type}|width_budget=0.98linewidth|height_budget=0.86textheight"
        f"|min_font_pt=10|split_allowed=no|expected_page={page}|risks=title-table-source-footline"
    )


def front_frames(records: Sequence[Paper], page: int) -> tuple[str, int]:
    counts = topic_counts(records)
    chunks: list[str] = []

    def add(manifest: str, body: str) -> None:
        chunks.append(manifest)
        chunks.append(body)

    add(
        frame_manifest("G-01", "G1", "title", page),
        r"""\begin{frame}[plain]
  \titlepage
\end{frame}
""",
    )
    page += 1
    add(
        frame_manifest("G-02", "G2", "scope-table", page),
        r"""\begin{frame}[t]{这份报告总结了什么，以及哪些内容没有被越界推断}
  \small
  % 主张：报告对象是 50 篇索引论文，而不是过程日志或重复选集。
  """
        + row_table(
            [
                ("论文集合", r"\textbf{50 篇}；按 \detokenize{refer/papers/INDEX.md} 的英中目录对去重。"),
                ("直接证据", r"中文/英文 \detokenize{main.tex}、\detokenize{chapters/*.tex}、转换/翻译指南与索引。"),
                ("不纳入科学内容", r"已有 Essential Papers 选集不重复展开；\detokenize{.agent.*} 日志和构建缓存只作过程记录。"),
                ("当前限制", r"目录中未发现论文 PDF；PDF 原文逐页核验、原始数据复现和独立数值检查均标为\unverified。"),
            ]
        )
        + r"""
  \source{证据：\detokenize{refer/papers/INDEX.md}、\detokenize{refer/papers/AGENTS.md}；报告边界为本次任务定义。}
\end{frame}
""",
    )
    page += 1
    add(
        frame_manifest("G-03", "G3", "corpus-statistics", page),
        r"""\begin{frame}[t]{语料规模显示：原文转排库足以支撑逐论文档案，但不是 PDF 复核}
  \small
  """
        + row_table(
            [
                ("目录结构", r"50 个英/中目录对，另有 2 个已有精华选集目录；论文正文只按 50 篇计数。"),
                ("索引页数", r"英文转排页数合计 1285 页；中文译本页数合计 1175 页；库内索引合计 2460 页。"),
                ("报告规模", r"每篇论文 4 个固定 frame，加总览、主题综合、交叉结论与来源附录；预期页数在生成时实测。"),
                ("物理主线", r"格点规范底座 → 流/重正化 → LaMET/赝 PDF → 胶子、强子 PDF/TMD → 采样算法。"),
            ]
        )
        + r"""
  \source{页数证据：\detokenize{refer/papers/INDEX.md}；报告页数以新 PDF 的 \detokenize{pdfinfo} 实测为准。}
\end{frame}
""",
    )
    page += 1
    add(
        frame_manifest("G-04", "G4", "evidence-table", page),
        r"""\begin{frame}[t]{每一个判断都分成“确证、推断、未验证”三层}
  \small
  """
        + row_table(
            [
                ("确证", r"源 LaTeX 摘要、章节、公式、图表或结论中可以直接定位的内容；报告保留文件和行号。"),
                ("推断", r"由一个或多个确证内容得到的物理关系或跨论文接口；文字明确写出“综合判断/推断”。"),
                ("未验证", r"缺少 PDF、原始数据、独立复现或源文件证据的数值/外推；只写缺口与核验动作。"),
                ("物理检查", r"优先检查规范对称性、量纲、连续/大动量/短距离极限和守恒关系；检查不替代实测。"),
            ]
        )
        + r"""
  \source{证据规则：本报告规格与每篇论文的中文/英文源文件；颜色不是唯一状态编码。}
\end{frame}
""",
    )
    page += 1
    add(
        frame_manifest("G-05", "G5", "workflow-table", page),
        r"""\begin{frame}[t]{全库的共同计算链条是“欧氏可计算量 → 匹配/演化 → 光锥观测量”}
  \small
  """
        + row_table(
            [
                ("输入", r"格点规范场系综、强子关联函数、空间 Wilson 线或流场；对象必须保持规范不变/协变。"),
                ("中间量", r"矩阵元、Ioffe 时间分布、准/赝分布、流时间复合算符、非微扰重正化因子。"),
                ("理论桥梁", r"OPE、LaMET 因子化、重正化方案转换、微扰匹配、DGLAP 或 Collins--Soper 演化。"),
                ("输出", r"PDF/GPD/TMD/强子结构或经物理可观测量检验的采样系综；有限动量、有限间距和系统误差不能省略。"),
            ]
        )
        + r"""
  \source{综合依据：50 篇论文档案的章节路线；此页是跨论文结构示意，不是单篇论文的数值结果。}
\end{frame}
""",
    )
    page += 1

    for topic, info in TOPIC_INFO.items():
        paper_names = "、".join(record.title_zh for record in records if record.topic == topic)
        paper_names = compact(paper_names, 420)
        add(
            frame_manifest(f"T-{page:03d}", f"T-{topic}", "topic-map-formula", page),
            "\\begin{frame}[t]{"
            + tex_escape(info["short"])
            + f"：{counts[topic]} 篇论文围绕同一个中间量链条展开}}\n"
            + "  \\small\n"
            + row_table(
                [
                    ("共同问题", tex_escape(info["description"])),
                    ("代表结构式", "$" + info["formula"] + "$\\\\[-0.2em]\\scriptsize 结构式/示意：用于说明变量和极限，不冒充单篇原文公式。"),
                    ("物理校验", tex_escape(info["check"])),
                    ("本组论文", tex_escape(paper_names)),
                ]
            )
            + "\n  \\source{综合来源：本组论文的 \\detokenize{main.tex} 与章节源；结构式为本报告的主题示意。}\n\\end{frame}\n",
        )
        page += 1

    add(
        frame_manifest("G-12", "G12", "risk-matrix", page),
        r"""\begin{frame}[t]{最需要警惕的不是页数，而是把不同极限下的量混为一谈}
  \small
  """
        + row_table(
            [
                ("紫外/线性发散", r"裸 Wilson 线和非局域算符必须先重正化；未经方案转换的矩阵元不能直接比较。"),
                ("大动量幂修正", r"LaMET/准分布的 \(P_z\) 有限；外推到无限动量需要多个动量、匹配和稳定性证据。"),
                ("短距离/流时间", r"赝分布、梯度流和 OPE 的适用区间受 \(z\)、\(t\)、\(a\) 共同约束，不能只看单一变量。"),
                ("采样正确性", r"生成模型的损失下降不等于系综正确；必须回到规范不变可观测量、自相关和分布检验。"),
            ]
        )
        + r"""
  \source{综合判断：各主题论文的误差/讨论章节；具体数值与置信度仍以各篇源文件为准。}
\end{frame}
""",
    )
    page += 1
    add(
        frame_manifest("G-13", "G13", "reading-guide", page),
        r"""\begin{frame}[t]{阅读方式：先看每篇四页档案，再沿主题接口回到原文}
  \small
  """
        + row_table(
            [
                ("第 1 页", "问题、对象、摘要摘录和论文定位；回答“论文试图测量/证明什么”。"),
                ("第 2 页", "输入、算符/状态、方法链和结构式；回答“物理量如何从格点对象产生”。"),
                ("第 3 页", "结果、验证和物理含义；直接引用源文件，未提供的数据明确降级为未验证。"),
                ("第 4 页", "局限、跨论文接口、量纲/极限检查和完整来源；回答“下一步应核验什么”。"),
            ]
        )
        + r"""
  \source{报告结构：\detokenize{docs/superpowers/specs/2026-08-28-refer-papers-report-design.md}。}
\end{frame}
""",
    )
    page += 1
    return "\n".join(chunks), page


def paper_frames(record: Paper, page: int) -> tuple[str, int]:
    topic_info = TOPIC_INFO[record.topic]
    chunks: list[str] = []
    title = tex_escape(record.title_zh)
    source_index = source_tex(f"refer/papers/INDEX.md:{int(record.paper_id[1:])}")
    method_src = source_tex(f"refer/papers/{record.zh_dir}/{record.method_source}")
    result_src = source_tex(f"refer/papers/{record.zh_dir}/{record.result_source}")

    chunks.append(frame_manifest(f"{record.paper_id}-01", f"{record.paper_id}-定位", "paper-card", page, record.paper_id))
    chunks.append(
        "\\section{" + title + "}\n"
        "\\begin{frame}[t]{" + title + "：研究问题与论文定位}\n"
        "  \\fontsize{10}{10.8}\\selectfont\n"
        + row_table(
            [
                ("论文编号", tex_escape(record.paper_id) + r"；主题：" + tex_escape(topic_info["short"])),
                ("书目信息", tex_escape(record.title_en) + r"；" + tex_escape(record.arxiv) + r"；英/中转排页数 " + str(record.en_pages) + "/" + str(record.zh_pages)),
                ("研究对象", tex_escape(compact(record.abstract_excerpt, 170))),
                ("章节证据", tex_escape(compact(record.section_titles, 140))),
                ("证据状态", r"\verified：摘要和章节来自现有 LaTeX；\unverified：没有论文 PDF/原始数据独立复核。"),
            ]
        )
        + "\n  \\source{索引："
        + source_index
        + "；正文："
        + source_pair(record, "main.tex")
        + "}\n\\end{frame}\n"
    )
    page += 1

    chunks.append(frame_manifest(f"{record.paper_id}-02", f"{record.paper_id}-方法", "method-flow-formula", page, record.paper_id))
    method_route = compact(record.section_titles, 140)
    chunks.append(
        "\\begin{frame}[t]{" + title + "：理论结构与方法链}\n"
        "  \\fontsize{10}{10.8}\\selectfont\n"
        + row_table(
            [
                ("输入与状态", tex_escape("格点/解析输入 → " + topic_info["short"] + "中的算符、矩阵元或场配置；具体输入见源章节。")),
                ("章节路线", tex_escape(method_route)),
                ("方法摘录", tex_escape(compact(record.method_excerpt, 180))),
                ("结构式/示意", "$" + topic_info["formula"] + "$\\\\[-0.2em]\\scriptsize 该式只表达主题变量关系；论文特定推导以源文件为准。"),
                ("物理校验", tex_escape(topic_info["check"])),
            ]
        )
        + "\n  \\source{方法证据："
        + method_src
        + "；主题结构式为示意。}\n\\end{frame}\n"
    )
    page += 1

    chunks.append(frame_manifest(f"{record.paper_id}-03", f"{record.paper_id}-结果", "result-evidence-table", page, record.paper_id))
    result_state = "确证：源章节有结果/讨论摘录。" if not record.result_excerpt.startswith("未验证") else record.result_excerpt
    chunks.append(
        "\\begin{frame}[t]{" + title + "：结果、验证与物理含义}\n"
        "  \\fontsize{10}{10.8}\\selectfont\n"
        + row_table(
            [
                ("源文结果", tex_escape(compact(record.result_excerpt, 280))),
                ("验证状态", tex_escape(result_state)),
                ("库内可见证据", tex_escape(f"中文源约 {record.zh_lines} 行；公式命中 {record.formula_hits}，图命中 {record.figure_hits}，表/表格命中 {record.table_hits}。")),
                ("物理含义", tex_escape("在本主题共同链条中，本论文把上述输入推进到可比较的中间量或观测量；具体强度、误差和外推范围不超出源文档。")),
                ("未验证项", tex_escape("当前工作区没有论文 PDF、原始数据和独立复现脚本；因此数值复核、图像再现和统计显著性不作额外断言。")),
            ]
        )
        + "\n  \\source{结果证据："
        + result_src
        + "；图表/公式计数由本报告生成器对中文源的静态统计得到。}\n\\end{frame}\n"
    )
    page += 1

    chunks.append(frame_manifest(f"{record.paper_id}-04", f"{record.paper_id}-局限", "risk-relation-table", page, record.paper_id))
    relation = topic_info["relation"]
    if record.note:
        relation += " 索引备注：" + record.note
    chunks.append(
        "\\begin{frame}[t]{" + title + "：局限、跨论文接口与可复查入口}\n"
        "  \\fontsize{10}{10.8}\\selectfont\n"
        + row_table(
            [
                ("源文局限", tex_escape("需要回到结果/讨论/展望章节核对适用区间；本档案不把缺失的独立数据复核补成已证实结论。")),
                ("跨论文接口", tex_escape(relation)),
                ("极限检查", tex_escape(topic_info["check"])),
                ("下一步核验", tex_escape("补齐 PDF 或原始数据；按源文参数复现关键图表；比较不同动量、流时间、距离、格距或方案转换后的稳定性。")),
                ("完整来源", source_pair(record, "main.tex") + r"；章节源：" + source_tex(f"refer/papers/{record.zh_dir}/chapters/*.tex") + r"；英中目录：" + source_tex(f"refer/papers/{record.en_dir}") + "."),
            ]
        )
        + "\n  \\source{状态：\\inferred 为主题接口推断；\\unverified 为当前材料边界；完整文件清单见 manifest。}\n\\end{frame}\n"
    )
    page += 1
    return "\n".join(chunks), page


def closing_frames(records: Sequence[Paper], page: int) -> tuple[str, int]:
    chunks: list[str] = []

    def add(frame_id: str, claim: str, visual: str, body: str) -> None:
        nonlocal page
        chunks.append(frame_manifest(frame_id, claim, visual, page))
        chunks.append(body)
        page += 1

    add(
        "C-01",
        "C1",
        "synthesis-flow",
        r"""\begin{frame}[t]{交叉结论：不同方法最终都在控制“可计算性”和“光锥物理”的间隙}
  \small
  """
        + row_table(
            [
                ("格点底座", "规范不变离散化与强子关联函数使欧氏时空中的非微扰量可计算。"),
                ("紫外控制", "涂抹、梯度流和非微扰重正化抑制或拆分短距离发散，但引入流时间、方案和匹配尺度。"),
                ("运动学桥梁", "LaMET、准/赝 PDF 和 TMD 因子化用大动量或短距离展开连接等时算符与光锥分布。"),
                ("物理输出", "只有在动量、距离、格距、体积和匹配阶数等系统性检验闭合后，才可提升为强子结构结论。"),
            ]
        )
        + r"""
  \source{综合判断：50 篇论文的章节和结论；跨主题关系属于\inferred，不替代单篇论文证据。}
\end{frame}
""",
    )
    add(
        "C-02",
        "C2",
        "error-matrix",
        r"""\begin{frame}[t]{交叉结论：系统误差必须按物理极限分层，而不能用单一误差条代替}
  \small
  """
        + row_table(
            [
                ("离散化", "改变格距或使用改进作用量，检验 a→0；静态源文件未提供统一跨论文极限数据。"),
                ("有限体积", "检查 \(m_\pi L\)、长距离关联和强子动量；各论文参数不同，不能直接合并百分比。"),
                ("激发态", "多态拟合、源汇时间和矩阵元平台共同决定基态隔离；缺少原始相关函数时标记未验证。"),
                ("匹配/重正化", "方案、尺度、截断阶数和算符混合影响连续分布；必须与对应论文的公式和附录共同复核。"),
                ("统计/采样", "自相关、系综覆盖和相关误差影响有效样本数；机器学习采样必须回到物理可观测量。"),
            ]
        )
        + r"""
  \source{综合依据：各篇的设置、结果、误差和讨论章节；数值量级未从不同源文档强行合并。}
\end{frame}
""",
    )
    add(
        "C-03",
        "C3",
        "topic-relation",
        r"""\begin{frame}[t]{主题接口：从 Wilson 线到 TMD 的路径由重正化和匹配连接}
  \small
  """
        + row_table(
            [
                ("基础 → 流", "规范不变格点和 Wilson 线定义输入；梯度流/涂抹改变短距离行为并提供平滑尺度。"),
                ("流 → 重正化", "流时间、OPE 和能动量张量构造有限或可匹配的复合算符；方案转换仍需明确。"),
                ("重正化→", "线性发散、算符混合和 RI/MS-bar 转换决定准分布能否与连续 PDF 对接。"),
                ("LaMET→", "核子、$\\pi$/K 胶子分布和准 TMD 计算把形式体系推进到现象学所需的对象。"),
                ("采样 → 全链条", "流模型、扩散和规范等变采样影响系综成本，但不能绕过可观测量验证。"),
            ]
        )
        + r"""
  \source{综合来源：各主题档案页；箭头表示方法接口，不表示所有论文都有直接引文关系。}
\end{frame}
""",
    )
    add(
        "C-04",
        "C4",
        "coverage-table",
        r"""\begin{frame}[t]{证据覆盖结论：本报告能完整回指源文本，但不能替代原始数据复现}
  \small
  """
        + row_table(
            [
                ("已覆盖", "50 篇索引论文的英中目录、摘要/章节结构、方法与结果摘录、索引页数和源路径。"),
                ("静态统计", "中文源的行数、公式环境、图形命令和表格命中数；这些是文件结构统计，不是物理误差分析。"),
                ("未覆盖", "论文 PDF 版面逐页核验、原始数据、外部数据库书目信息、独立编译每篇源目录和数值再现。"),
                ("解释边界", "主题结构式和跨论文接口是带标签的综合推断；单篇论文的细节以对应源文件为准。"),
            ]
        )
        + r"""
  \source{直接证据：\detokenize{refer/papers/INDEX.md} 与各英中 LaTeX 目录；限制来自当前工作区材料。}
\end{frame}
""",
    )
    add(
        "C-05",
        "C5",
        "roadmap-table",
        r"""\begin{frame}[t]{后续核验清单：每项都有可验收产物，而不是泛泛的“继续优化”}
  \small
  """
        + row_table(
            [
                ("材料补齐", "为 50 篇论文补充可访问 PDF/官方源包或原始数据；验收：书目、图表和源文本逐项对账。"),
                ("编译复核", "逐目录重新执行双遍 XeLaTeX；验收：零错误、页数记录完整、英中编号对应。"),
                ("数值复现", "按每篇设置复现代表性图表；验收：参数、单位、误差和基线均可追溯。"),
                ("系统误差", "分离格距、体积、动量、流时间/距离、激发态和匹配截断；验收：稳定性表格闭合。"),
                ("物理输出", "仅在极限和误差证据闭合后更新 PDF/TMD/采样结论；验收：结论—证据—限制一一对应。"),
            ]
        )
        + r"""
  \source{计划依据：各篇结果/讨论中的未解决问题；具体排期需由研究者另行决定。}
\end{frame}
""",
    )
    add(
        "C-06",
        "C6",
        "source-catalog",
        r"""\begin{frame}[t]{来源目录：50 篇论文均有唯一编号和英中目录入口}
  \scriptsize
  \begin{tabularx}{0.98\linewidth}{@{}lXl@{}}
    \toprule
    编号 & 中文目录 & arXiv/索引来源 \\
    \midrule
"""
        + "\n".join(
            f"    {tex_escape(record.paper_id)} & {tex_escape(record.title_zh)} & {tex_escape(record.arxiv)} \\\\" for record in records[:17]
        )
        + r"""
    \bottomrule
  \end{tabularx}
  \vspace{0.2em}
  \scriptsize 本页列 P01–P17；后续页面继续列出其余论文。
  \source{索引：\detokenize{refer/papers/INDEX.md}；机器可读完整清单：\detokenize{docs/report_refer_papers_all_20260828.manifest.tsv}。}
\end{frame}
""",
    )
    add(
        "C-07",
        "C7",
        "source-catalog",
        r"""\begin{frame}[t]{来源目录（续）：中段论文与可追溯状态}
  \scriptsize
  \begin{tabularx}{0.98\linewidth}{@{}lXl@{}}
    \toprule
    编号 & 中文目录 & arXiv/索引来源 \\
    \midrule
"""
        + "\n".join(
            f"    {tex_escape(record.paper_id)} & {tex_escape(record.title_zh)} & {tex_escape(record.arxiv)} \\\\" for record in records[17:34]
        )
        + r"""
    \bottomrule
  \end{tabularx}
  \vspace{0.2em}
  \scriptsize 本页列 P18–P34；最后一页列出 P35–P50。
  \source{索引：\detokenize{refer/papers/INDEX.md}；完整源文件字段见 manifest。}
\end{frame}
""",
    )
    add(
        "C-08",
        "C8",
        "source-catalog",
        r"""\begin{frame}[t]{来源目录（续）：后段论文与可追溯状态}
  \scriptsize
  \begin{tabularx}{0.98\linewidth}{@{}lXl@{}}
    \toprule
    编号 & 中文目录 & arXiv/索引来源 \\
    \midrule
"""
        + "\n".join(
            f"    {tex_escape(record.paper_id)} & {tex_escape(record.title_zh)} & {tex_escape(record.arxiv)} \\\\" for record in records[34:]
        )
        + r"""
    \bottomrule
  \end{tabularx}
  \vspace{0.2em}
  \scriptsize 本页列 P35–P50；每篇档案第 4 页给出中文/英文 main.tex 与章节入口。
  \source{索引：\detokenize{refer/papers/INDEX.md}；机器可读完整清单：\detokenize{docs/report_refer_papers_all_20260828.manifest.tsv}。}
\end{frame}
""",
    )
    return "\n".join(chunks), page


def generate_tex(records: Sequence[Paper], path: Path = REPORT_PATH) -> int:
    page = 1
    front, page = front_frames(records, page)
    paper_parts: list[str] = []
    for record in records:
        part, page = paper_frames(record, page)
        paper_parts.append(part)
    closing, page = closing_frames(records, page)
    expected_pages = page - 1
    if expected_pages < 200:
        raise ValueError(f"生成 frame 数不足 200：{expected_pages}")

    preamble = r"""% ============================================================
% refer/papers 全量内容总结报告
% 生成器：docs/build_refer_papers_report.py
% 编译：XeLaTeX 两遍；本文件不依赖 refer/papers 的图片或外部数据
% ============================================================
\documentclass[UTF8,aspectratio=169,11pt]{ctexbeamer}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{tikz}
\usepackage{xcolor}
\usepackage{microtype}
\usepackage{hyperref}
\hypersetup{hidelinks}
\usetikzlibrary{arrows.meta,positioning,calc,fit,shapes.geometric}

\definecolor{primary}{HTML}{17365D}
\definecolor{accent}{HTML}{1F77B4}
\definecolor{evidence}{HTML}{1E8449}
\definecolor{warning}{HTML}{C55A11}
\definecolor{muted}{HTML}{5B6573}
\definecolor{panel}{HTML}{F4F7FA}
\setbeamersize{text margin left=0.55cm,text margin right=0.55cm}
\setlength{\emergencystretch}{3em}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{blocks}[rounded][shadow=false]
\setbeamercolor{normal text}{fg=black!86,bg=white}
\setbeamercolor{structure}{fg=primary}
\setbeamercolor{frametitle}{fg=primary,bg=white}
\setbeamercolor{block title}{fg=primary,bg=panel}
\setbeamercolor{block body}{fg=black!86,bg=panel}
\setbeamerfont{frametitle}{size=\large,series=\bfseries}
\setbeamertemplate{frametitle}{\vskip0.12cm\insertframetitle\par\vskip0.08cm}
\setbeamertemplate{footline}{%
  \hbox{\begin{beamercolorbox}[wd=\paperwidth,ht=2.3ex,dp=0.9ex,
    leftskip=0.55cm,rightskip=0.55cm]{author in head/foot}%
    \scriptsize\color{muted}\insertshortauthor\hfill
    \insertshorttitle\hfill\insertframenumber/\inserttotalframenumber
    \end{beamercolorbox}}}
\newcommand{\source}[1]{\vspace{0.08em}\par{\raggedright\scriptsize\color{muted}来源：#1\par}}
\newcommand{\verified}{\textcolor{evidence}{确证}}
\newcommand{\inferred}{\textcolor{accent}{推断}}
\newcommand{\unverified}{\textcolor{warning}{未验证}}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\title[refer/papers 全量总结]{refer/papers 全量论文内容总结}
\author[Codex]{Codex}
\institute{格点 QCD、部分子物理与数值方法文献档案}
\date{2026 年 8 月 28 日}

\begin{document}
"""
    ending = r"""
\end{document}
"""
    content = preamble + front + "\n" + "\n".join(paper_parts) + "\n" + closing + ending
    path.write_text(content, encoding="utf-8")
    return expected_pages


def check_manifest(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required = {"paper_id", "title_zh", "en_dir", "zh_dir", "arxiv", "section_titles", "abstract_excerpt", "result_excerpt"}
    missing_fields = sorted(required - set(rows[0]) if rows else required)
    ids = [row.get("paper_id", "") for row in rows]
    missing_rows = [row.get("paper_id", "?") for row in rows if any(not row.get(field, "").strip() for field in required)]
    print(f"papers={len(rows)} unique_ids={len(set(ids))} missing_required_fields={len(missing_rows) + len(missing_fields)}")
    print(f"missing_field_names={','.join(missing_fields) if missing_fields else 'none'}")
    for row in rows:
        print(
            f"{row.get('paper_id', '?')} sections={len([x for x in row.get('section_titles', '').split('；') if x])} "
            f"formula_hits={row.get('formula_hits', '0')} figure_hits={row.get('figure_hits', '0')} "
            f"table_hits={row.get('table_hits', '0')} state={row.get('evidence_state', '')[:24]}"
        )
    if len(rows) != 50 or len(set(ids)) != 50 or missing_fields or missing_rows:
        if missing_rows:
            print("missing_rows=" + ",".join(missing_rows), file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--manifest-only", action="store_true")
    mode.add_argument("--check-manifest", type=Path)
    mode.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    if args.check_manifest:
        return check_manifest(args.check_manifest)

    records = build_papers()
    write_manifest(records)
    en_pages = sum(record.en_pages for record in records)
    zh_pages = sum(record.zh_pages for record in records)
    print(f"parsed_papers={len(records)} unique_ids={len({record.paper_id for record in records})}")
    print(f"index_pages=EN:{en_pages} ZH:{zh_pages} total:{en_pages + zh_pages}")
    print("topic_counts=" + ", ".join(f"{topic}:{count}" for topic, count in topic_counts(records).items()))
    if args.manifest_only:
        print(f"manifest={MANIFEST_PATH}")
        return 0
    expected_pages = generate_tex(records)
    print(f"tex={REPORT_PATH}")
    print(f"expected_pages={expected_pages} paper_frames={len(records) * 4}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

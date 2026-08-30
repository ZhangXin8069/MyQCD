"""对 refer/papers 中文论文源文件建立可追溯的显示公式清单。"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


DISPLAY_ENVIRONMENTS = frozenset(
    {
        "equation",
        "equation*",
        "align",
        "align*",
        "alignat",
        "alignat*",
        "gather",
        "gather*",
        "multline",
        "multline*",
        "eqnarray",
        "eqnarray*",
        "displaymath",
        "flalign",
        "flalign*",
        "xalignat",
        "xalignat*",
    }
)

_BEGIN_RE = re.compile(r"\\begin\s*\{([^{}]+)\}")
_CUSTOM_BEGIN_RE = re.compile(r"\\bea(?![A-Za-z])|\\be(?![A-Za-z])")


def _closing_match(environment: str, text: str):
    if environment == "be":
        return re.search(r"\\ee(?![A-Za-z])", text)
    if environment == "bea":
        return re.search(r"\\eea(?![A-Za-z])", text)
    return re.search(r"\\end\s*\{" + re.escape(environment) + r"\}", text)


@dataclass(frozen=True)
class FormulaRecord:
    """源文件中的一段显示公式。"""

    formula_id: str
    paper_id: str
    source_file: str
    start_line: int
    end_line: int
    environment: str
    body: str
    status: str
    reason: str


@dataclass(frozen=True)
class InventoryReport:
    """公式索引及统计信息。"""

    paper_count: int
    source_file_count: int
    formula_count: int
    records: Tuple[FormulaRecord, ...]

    @property
    def unparsed_count(self) -> int:
        return sum(record.status == "unparsed" for record in self.records)

    def to_dict(self) -> dict:
        return {
            "paper_count": self.paper_count,
            "source_file_count": self.source_file_count,
            "formula_count": self.formula_count,
            "unparsed_count": self.unparsed_count,
            "records": [asdict(record) for record in self.records],
        }


def _without_tex_comment(line: str) -> str:
    """删除非转义百分号后的 TeX 注释，仅用于识别环境边界。"""

    escaped = False
    for index, character in enumerate(line):
        if character == "%" and not escaped:
            return line[:index]
        if character == "\\":
            escaped = not escaped
        else:
            escaped = False
    return line


def _record_formula(
    *,
    formula_id: str,
    paper_id: str,
    source_file: str,
    start_line: int,
    end_line: int,
    environment: str,
    body_lines: Sequence[str],
) -> FormulaRecord:
    return FormulaRecord(
        formula_id=formula_id,
        paper_id=paper_id,
        source_file=source_file,
        start_line=start_line,
        end_line=end_line,
        environment=environment,
        body="\n".join(body_lines).strip(),
        status="unparsed",
        reason=(
            "LaTeX 显示公式已索引，但尚未在不引入论文特定指标、方案、"
            "边界条件和微扰约定的情况下自动转换为 SymPy。"
        ),
    )


def extract_display_formulas(
    text: str,
    source_file: str = "<memory>",
    paper_id: str = "P00",
    formula_start: int = 0,
) -> Tuple[FormulaRecord, ...]:
    """提取显示数学环境，保留起止行号和原始正文。

    解析器只负责结构化定位，不试图猜测 LaTeX 宏的物理语义。嵌套的
    ``aligned``、``cases`` 等环境作为外层公式正文保留，不重复计数；
    论文常见的 ``\\be...\\ee`` 和 ``\\bea...\\eea`` 别名也被定位。
    """

    records: List[FormulaRecord] = []
    active_environment = None
    active_start = 0
    active_body: List[str] = []
    formula_number = formula_start

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        scan_line = _without_tex_comment(raw_line)
        if active_environment is None:
            opening = next(
                (
                    match
                    for match in _BEGIN_RE.finditer(scan_line)
                    if match.group(1) in DISPLAY_ENVIRONMENTS
                ),
                None,
            )
            if opening is not None:
                environment = opening.group(1)
            else:
                custom_opening = _CUSTOM_BEGIN_RE.search(scan_line)
                if custom_opening is None:
                    continue
                opening = custom_opening
                environment = custom_opening.group(0)[1:]
            tail = scan_line[opening.end() :]
            closing = _closing_match(environment, tail)
            if closing is not None:
                formula_number += 1
                records.append(
                    _record_formula(
                        formula_id=f"{paper_id}-F{formula_number:04d}",
                        paper_id=paper_id,
                        source_file=source_file,
                        start_line=line_number,
                        end_line=line_number,
                        environment=environment,
                        body_lines=[tail[: closing.start()]],
                    )
                )
                continue

            active_environment = environment
            active_start = line_number
            active_body = [raw_line[opening.end() :]]
            continue

        closing = _closing_match(active_environment, scan_line)
        if closing is None:
            active_body.append(raw_line)
            continue

        active_body.append(raw_line[: closing.start()])
        formula_number += 1
        records.append(
            _record_formula(
                formula_id=f"{paper_id}-F{formula_number:04d}",
                paper_id=paper_id,
                source_file=source_file,
                start_line=active_start,
                end_line=line_number,
                environment=active_environment,
                body_lines=active_body,
            )
        )
        active_environment = None
        active_start = 0
        active_body = []

    if active_environment is not None:
        formula_number += 1
        records.append(
            _record_formula(
                formula_id=f"{paper_id}-F{formula_number:04d}",
                paper_id=paper_id,
                source_file=source_file,
                start_line=active_start,
                end_line=len(text.splitlines()),
                environment=active_environment,
                body_lines=active_body,
            )
        )

    return tuple(records)


def _indexed_chinese_directories(papers_dir: Path) -> Tuple[Tuple[str, str], ...]:
    index_path = papers_dir / "INDEX.md"
    entries: List[Tuple[str, str]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        fields = [field.strip().strip("`") for field in line.split("|")]
        if len(fields) < 4 or not fields[1].isdigit():
            continue
        entries.append((f"P{int(fields[1]):02d}", fields[3]))
    if not entries:
        raise ValueError(f"未能从 {index_path} 读取论文索引")
    return tuple(entries)


def _source_files(directory: Path) -> Iterable[Path]:
    for path in sorted(directory.rglob("*.tex")):
        relative_parts = path.relative_to(directory).parts
        if "build" in relative_parts or any(part.startswith(".") for part in relative_parts):
            continue
        yield path


def scan_refer_papers(root: Path | str) -> InventoryReport:
    """扫描 INDEX.md 列出的 50 个中文论文目录。

    只读取 ``refer/papers/<中文目录>`` 下的 TeX 源文件，排除 build 产物，
    因此每条记录都可以直接回到工作区中的文件和行号。
    """

    root_path = Path(root).resolve()
    papers_dir = root_path / "refer" / "papers"
    records: List[FormulaRecord] = []
    source_file_count = 0
    paper_entries = _indexed_chinese_directories(papers_dir)
    for paper_id, directory_name in paper_entries:
        directory = papers_dir / directory_name
        paper_formula_number = 0
        for source_path in _source_files(directory):
            source_file_count += 1
            relative_source = source_path.relative_to(root_path).as_posix()
            source_records = extract_display_formulas(
                source_path.read_text(encoding="utf-8"),
                source_file=relative_source,
                paper_id=paper_id,
                formula_start=paper_formula_number,
            )
            records.extend(source_records)
            paper_formula_number += len(source_records)

    return InventoryReport(
        paper_count=len(paper_entries),
        source_file_count=source_file_count,
        formula_count=len(records),
        records=tuple(records),
    )


def write_inventory(path: Path | str, inventory: InventoryReport) -> None:
    """显式请求时把清单写成 UTF-8 JSON；默认扫描不会产生文件。"""

    output_path = Path(path)
    output_path.write_text(
        json.dumps(inventory.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

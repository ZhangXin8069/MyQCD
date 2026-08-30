"""同源生成并编译格点 QCD 核心课、索引与论文图谱。"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

from source_registry import SOURCES, Source


try:
    from course_content import VOLUMES
except Exception as exc:  # 让验证器报告结构错误，而不是在导入阶段退出
    VOLUMES = ()
    COURSE_CONTENT_IMPORT_ERROR: Optional[str] = f"{type(exc).__name__}: {exc}"
else:
    COURSE_CONTENT_IMPORT_ERROR = None


COURSE_DIR = Path(__file__).resolve().parent
REPO_ROOT = COURSE_DIR.parents[1]
GENERATED_DIR = COURSE_DIR / "generated"
BUILD_DIR = COURSE_DIR / "build"
PDF_DIR = COURSE_DIR / "pdf"
PAPER_INDEX = REPO_ROOT / "refer" / "papers" / "INDEX.md"
PAPER_SOURCE_MAP = COURSE_DIR / "paper_sources.json"
PYQCD_ROOT = REPO_ROOT.parent / "PyQCD"

EXPECTED_LESSON_CODES: Tuple[str, ...] = tuple(
    f"{volume:02d}.{lesson:02d}"
    for volume in range(1, 36)
    for lesson in range(1, 6)
)
EXPECTED_SYMPY_IDS: Tuple[str, ...] = tuple(
    f"SYM-{code}" for code in EXPECTED_LESSON_CODES
)

_SYMPY_PAYLOAD_KEYS = frozenset(("schema", "total", "passed", "records"))
_SYMPY_RECORD_KEYS = frozenset(
    (
        "validation_id",
        "lesson_code",
        "title",
        "engine",
        "status",
        "checks",
        "assumptions",
        "boundary",
    )
)


def require_course_content() -> None:
    if COURSE_CONTENT_IMPORT_ERROR is not None:
        raise RuntimeError(
            f"结构化课程内容导入失败：{COURSE_CONTENT_IMPORT_ERROR}"
        )


@dataclass(frozen=True)
class Paper:
    number: int
    english_dir: str
    chinese_dir: str
    english_pages: int
    chinese_pages: int
    origin: str
    note: str
    arxiv: Optional[str]
    repository: str
    source_locator: str
    source_url: str
    source_pdf: Path
    original_pages: int
    sha256: str

    @property
    def paper_id(self) -> str:
        return f"P{self.number:02d}"

    @property
    def title(self) -> str:
        return self.chinese_dir.removesuffix("_latex").replace("_", " ")

    @property
    def pdf_path(self) -> Path:
        return self.source_pdf


THEMES: Tuple[Tuple[str, str, Tuple[int, ...]], ...] = (
    ("A", "规范理论、格点与算符基础", tuple(range(1, 7)) + (19,)),
    ("B", "梯度流、涂抹与流时算符", tuple(range(7, 11)) + (28,) + tuple(range(35, 41))),
    ("C", "LaMET、quasi/pseudo 分布与因子化", tuple(range(11, 19)) + tuple(range(47, 51))),
    ("D", "非局域算符重整化与 hybrid 方案", tuple(range(20, 26)) + (29, 30)),
    ("E", "胶子 PDF、TMD、soft 与 Collins--Soper", (26, 27, 31, 32) + tuple(range(41, 46))),
    ("F", "Monte Carlo、规范等变流与随机量化", (33, 34, 46)),
)


_INLINE_MATH_MAPPING = {
    "±": r"\pm",
    "∓": r"\mp",
    "×": r"\times ",
    "·": r"\cdot ",
    "Γ": r"\Gamma",
    "Δ": r"\Delta",
    "Λ": r"\Lambda",
    "Π": r"\Pi",
    "Σ": r"\Sigma",
    "Φ": r"\Phi",
    "Ω": r"\Omega",
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "δ": r"\delta",
    "ε": r"\epsilon",
    "ζ": r"\zeta",
    "η": r"\eta",
    "θ": r"\theta",
    "κ": r"\kappa",
    "λ": r"\lambda",
    "μ": r"\mu",
    "ν": r"\nu",
    "ξ": r"\xi",
    "π": r"\pi",
    "ρ": r"\rho",
    "σ": r"\sigma",
    "τ": r"\tau",
    "φ": r"\phi",
    "χ": r"\chi",
    "ψ": r"\psi",
    "ω": r"\omega",
    "¹": r"^{1}",
    "²": r"^{2}",
    "³": r"^{3}",
    "⁴": r"^{4}",
    "⁵": r"^{5}",
    "⁷": r"^{7}",
    "⁺": r"^{+}",
    "⁻": r"^{-}",
    "ⁿ": r"^{n}",
    "₀": r"_{0}",
    "₁": r"_{1}",
    "₌": r"_{=}",
    "ₓ": r"_{x}",
    "ₙ": r"_{n}",
    "ᵧ": r"_{\gamma}",
    "→": r"\rightarrow",
    "↔": r"\leftrightarrow",
    "↦": r"\mapsto",
    "∂": r"\partial",
    "∈": r"\in",
    "−": "-",
    "ℓ": r"\ell",
    "ℏ": r"\hbar",
    "′": r"^{\prime}",
    "‴": r"^{\prime\prime\prime}",
    "⟨": r"\langle",
    "⟩": r"\rangle",
    "ᵀ": r"^{T}",
    "ˣ": r"^{x}",
    "ȳ": r"\bar y",
    "ᴸ": r"^{L}",
    "ᴺ": r"^{N}",
    "∝": r"\propto",
    "∞": r"\infty",
    "∫": r"\int",
    "≈": r"\approx",
    "≃": r"\simeq",
    "∼": r"\sim",
    "≠": r"\ne",
    "≤": r"\le",
    "≥": r"\ge",
    "≪": r"\ll",
    "≫": r"\gg",
    "≳": r"\gtrsim",
    "⊂": r"\subset",
    "⊕": r"\oplus",
    "⊗": r"\otimes",
    "†": r"\dagger",
}

_SUPERSCRIPT_RUN_MAPPING = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "⁺": "+", "⁻": "-", "⁼": "=", "⁽": "(", "⁾": ")",
    "ⁿ": "n", "ᵀ": "T", "ˣ": "x", "ᴸ": "L", "ᴺ": "N",
    "′": r"\prime", "‴": r"\prime\prime\prime",
}
_SUBSCRIPT_RUN_MAPPING = {
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
    "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
    "₊": "+", "₋": "-", "₌": "=", "₍": "(", "₎": ")",
    "ₓ": "x", "ₙ": "n", "ᵧ": r"\gamma",
}


def _inline_math_text(value: str) -> str:
    """把受信任的短数学片段转换为数学模式内容，不嵌套 ensuremath。"""

    chunks: List[str] = []
    for index, char in enumerate(value):
        replacement = _INLINE_MATH_MAPPING.get(char, char)
        if (
            re.fullmatch(r"\\[A-Za-z]+", replacement)
            and index + 1 < len(value)
            and value[index + 1].isascii()
            and value[index + 1].isalpha()
        ):
            replacement += "{}"
        chunks.append(replacement)
    return "".join(chunks)


def _script_run(
    text: str,
    start: int,
    mapping: Mapping[str, str],
) -> Tuple[str, int]:
    """把连续 Unicode 上标或下标合并成一个 TeX 脚本组。"""

    index = start
    values: List[str] = []
    while index < len(text) and text[index] in mapping:
        values.append(mapping[text[index]])
        index += 1
    return "".join(values), index


def _closing_inline_math_dollar(text: str, start: int) -> Optional[int]:
    """返回行内 ``$...$`` 的闭合位置；反斜线转义的美元符不闭合。"""

    index = start + 1
    while index < len(text):
        if text[index] in "\r\n":
            return None
        if text[index] == "$" and text[index - 1] != "\\":
            return index
        index += 1
    return None


def _balanced_argument(text: str, start: int) -> Tuple[Optional[str], int]:
    """读取从 ``start`` 开始的圆/方/花括号组，返回组内文本与下一位置。"""

    pairs = {"(": ")", "[": "]", "{": "}"}
    opener = text[start] if start < len(text) else ""
    closer = pairs.get(opener)
    if closer is None:
        return None, start
    depth = 1
    index = start + 1
    while index < len(text):
        if text[index] == opener:
            depth += 1
        elif text[index] == closer:
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
        index += 1
    return None, start


def _math_atom(text: str, start: int) -> Tuple[Optional[str], int]:
    """读取根号或未加花括号上标后的一个确定数学原子。"""

    if start >= len(text):
        return None, start
    if text[start] in "([{":
        return _balanced_argument(text, start)
    if text[start].isdigit():
        match = re.match(r"\d+(?:\.\d+)?", text[start:])
        assert match is not None
        return match.group(0), start + len(match.group(0))
    if (
        text[start] in "+-−"
        and start + 1 < len(text)
        and text[start + 1].isdigit()
    ):
        match = re.match(r"[+\-−]\d+(?:\.\d+)?", text[start:])
        assert match is not None
        return match.group(0).replace("−", "-"), start + len(match.group(0))
    if text[start] == "\\":
        match = re.match(r"\\[A-Za-z]+", text[start:])
        if match is not None:
            return match.group(0), start + len(match.group(0))
    return text[start], start + 1


def tex_text(value: object) -> str:
    mapping = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "%": r"\%",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "/": r"/\allowbreak{}",
        "±": r"\ensuremath{\pm}",
        "∓": r"\ensuremath{\mp}",
        "×": r"\ensuremath{\times}",
        "Γ": r"\ensuremath{\Gamma}",
        "Δ": r"\ensuremath{\Delta}",
        "Λ": r"\ensuremath{\Lambda}",
        "Π": r"\ensuremath{\Pi}",
        "Σ": r"\ensuremath{\Sigma}",
        "Φ": r"\ensuremath{\Phi}",
        "Ω": r"\ensuremath{\Omega}",
        "α": r"\ensuremath{\alpha}",
        "β": r"\ensuremath{\beta}",
        "γ": r"\ensuremath{\gamma}",
        "δ": r"\ensuremath{\delta}",
        "ε": r"\ensuremath{\epsilon}",
        "ζ": r"\ensuremath{\zeta}",
        "η": r"\ensuremath{\eta}",
        "θ": r"\ensuremath{\theta}",
        "κ": r"\ensuremath{\kappa}",
        "λ": r"\ensuremath{\lambda}",
        "μ": r"\ensuremath{\mu}",
        "ν": r"\ensuremath{\nu}",
        "ξ": r"\ensuremath{\xi}",
        "π": r"\ensuremath{\pi}",
        "ρ": r"\ensuremath{\rho}",
        "σ": r"\ensuremath{\sigma}",
        "τ": r"\ensuremath{\tau}",
        "φ": r"\ensuremath{\phi}",
        "χ": r"\ensuremath{\chi}",
        "ψ": r"\ensuremath{\psi}",
        "ω": r"\ensuremath{\omega}",
        "¹": r"\ensuremath{^{1}}",
        "²": r"\ensuremath{^{2}}",
        "³": r"\ensuremath{^{3}}",
        "⁴": r"\ensuremath{^{4}}",
        "⁵": r"\ensuremath{^{5}}",
        "⁷": r"\ensuremath{^{7}}",
        "⁺": r"\ensuremath{^{+}}",
        "⁻": r"\ensuremath{^{-}}",
        "ⁿ": r"\ensuremath{^{n}}",
        "₀": r"\ensuremath{_{0}}",
        "₁": r"\ensuremath{_{1}}",
        "₌": r"\ensuremath{_{=}}",
        "ₓ": r"\ensuremath{_{x}}",
        "ₙ": r"\ensuremath{_{n}}",
        "ᵧ": r"\ensuremath{_{\gamma}}",
        "→": r"\ensuremath{\rightarrow}",
        "↔": r"\ensuremath{\leftrightarrow}",
        "↦": r"\ensuremath{\mapsto}",
        "∂": r"\ensuremath{\partial}",
        "∈": r"\ensuremath{\in}",
        "−": r"\ensuremath{-}",
        "√": r"\ensuremath{\surd}",
        "ℓ": r"\ensuremath{\ell}",
        "ℏ": r"\ensuremath{\hbar}",
        "′": r"\ensuremath{^{\prime}}",
        "‴": r"\ensuremath{^{\prime\prime\prime}}",
        "⟨": r"\ensuremath{\langle}",
        "⟩": r"\ensuremath{\rangle}",
        "ᵀ": r"\ensuremath{^{T}}",
        "ˣ": r"\ensuremath{^{x}}",
        "ȳ": r"\ensuremath{\bar y}",
        "ᴸ": r"\ensuremath{^{L}}",
        "ᴺ": r"\ensuremath{^{N}}",
        "∝": r"\ensuremath{\propto}",
        "∞": r"\ensuremath{\infty}",
        "∫": r"\ensuremath{\int}",
        "≈": r"\ensuremath{\approx}",
        "≃": r"\ensuremath{\simeq}",
        "∼": r"\ensuremath{\sim}",
        "≠": r"\ensuremath{\ne}",
        "≤": r"\ensuremath{\le}",
        "≥": r"\ensuremath{\ge}",
        "≪": r"\ensuremath{\ll}",
        "≫": r"\ensuremath{\gg}",
        "≳": r"\ensuremath{\gtrsim}",
        "⊂": r"\ensuremath{\subset}",
        "⊕": r"\ensuremath{\oplus}",
        "⊗": r"\ensuremath{\otimes}",
    }
    text = str(value)
    chunks: List[str] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char in _SUPERSCRIPT_RUN_MAPPING:
            argument, next_index = _script_run(
                text, index, _SUPERSCRIPT_RUN_MAPPING
            )
            chunks.append(r"\ensuremath{^{" + argument + "}}")
            index = next_index
            continue
        if char in _SUBSCRIPT_RUN_MAPPING:
            argument, next_index = _script_run(
                text, index, _SUBSCRIPT_RUN_MAPPING
            )
            chunks.append(r"\ensuremath{_{" + argument + "}}")
            index = next_index
            continue
        if char == "$":
            closing = _closing_inline_math_dollar(text, index)
            if closing is not None and closing > index + 1:
                chunks.append(
                    r"\ensuremath{" + _inline_math_text(text[index + 1 : closing]) + "}"
                )
                index = closing + 1
                continue
        if char == "√":
            argument, next_index = _math_atom(text, index + 1)
            if argument is not None:
                chunks.append(
                    r"\ensuremath{\sqrt{" + _inline_math_text(argument) + "}}"
                )
                index = next_index
                continue
        elif char == "^":
            argument, next_index = _math_atom(text, index + 1)
            if argument is not None:
                chunks.append(
                    r"\ensuremath{^{" + _inline_math_text(argument) + "}}"
                )
                index = next_index
                continue
        elif char == "_" and index + 1 < len(text) and text[index + 1] == "{":
            argument, next_index = _balanced_argument(text, index + 1)
            if argument is not None:
                chunks.append(
                    r"\ensuremath{_{" + _inline_math_text(argument) + "}}"
                )
                index = next_index
                continue
        chunks.append(mapping.get(char, char))
        index += 1
    return "".join(chunks)


def tex_code(value: object) -> str:
    chunks: List[str] = []
    for char in str(value).replace("\\", "/"):
        chunks.append(tex_text(char))
        if char in "_.":
            chunks.append(r"\allowbreak{}")
    return r"\texttt{" + "".join(chunks) + "}"


def stable_definition_id(code: str, term_name: str) -> str:
    """由单元与术语身份生成稳定 Def ID；术语重排不改变编号。"""

    normalized = unicodedata.normalize("NFKC", str(term_name)).strip()
    if not normalized:
        raise ValueError(f"{code}: 定义术语名不能为空")
    payload = f"lqcd-definition-v1\0{code}\0{normalized}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:10]
    return f"{code}-{digest}"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _path_label(path: Path) -> str:
    """Return a host-independent label for an allowed fingerprint input."""

    resolved = path.resolve()
    roots = (("repo", REPO_ROOT.resolve()), ("pyqcd", PYQCD_ROOT.resolve()))
    for prefix, root in roots:
        if resolved == root or root in resolved.parents:
            return f"{prefix}/{resolved.relative_to(root).as_posix()}"
    raise ValueError(f"指纹输入不在允许根目录内：{path}")


def _fingerprinted_files(paths: Sequence[Path]) -> Mapping[str, str]:
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"构建输入缺失：{missing}")
    labeled = [(_path_label(path), path) for path in paths]
    labels = [label for label, _ in labeled]
    if len(labels) != len(set(labels)):
        raise ValueError("构建指纹输入路径重复")
    return {
        label: _sha256(path)
        for label, path in sorted(labeled, key=lambda item: item[0])
    }


def _generation_source_paths() -> Tuple[Path, ...]:
    """Enumerate every hand-maintained fact that can change generated output."""

    content_modules = tuple(sorted((COURSE_DIR / "content").glob("*.py")))
    teaching_modules = tuple(sorted((COURSE_DIR / "myqcd").glob("*.py")))
    shared_validation_modules = tuple(sorted((REPO_ROOT / "myqcd").glob("*.py")))
    return (
        COURSE_DIR / "build_course.py",
        COURSE_DIR / "course_content.py",
        COURSE_DIR / "source_registry.py",
        PAPER_SOURCE_MAP,
        PAPER_INDEX,
        COURSE_DIR / "course_style.tex",
        COURSE_DIR / "sympy_validation.py",
        GENERATED_DIR / "sympy_validation.json",
        GENERATED_DIR / "myqcd_examples.json",
        *content_modules,
        *teaching_modules,
        *shared_validation_modules,
    )


def generation_source_fingerprint() -> str:
    """Bind structured content, generator, sources, style, and validation facts."""

    identity = {
        "schema": "lattice-qcd-generation-source-v1",
        "files": _fingerprinted_files(_generation_source_paths()),
    }
    return hashlib.sha256(
        json.dumps(
            identity,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def document_source_fingerprint(
    stem: str,
    metadata: Mapping[str, object],
) -> str:
    """绑定一份 PDF 的生成事实、TeX、片段和论文原文输入。"""

    tex_path = GENERATED_DIR / str(metadata["tex"])
    paths = [tex_path]
    kind = str(metadata.get("kind", ""))
    if kind != "atlas":
        paths.append(COURSE_DIR / "course_style.tex")
    if kind == "volume":
        paths.append(
            GENERATED_DIR / "fragments" / f"V{metadata['volume']}.tex"
        )
    elif kind == "core":
        paths.extend(
            GENERATED_DIR / "fragments" / f"V{number:02d}.tex"
            for number in range(1, 36)
        )
    elif kind == "atlas":
        source_map = _load_paper_source_map()
        paper_ids = metadata.get("papers", [])
        if not isinstance(paper_ids, list):
            raise TypeError(f"{stem}: atlas papers 必须是数组")
        paths.extend(
            _source_path(str(source_map[str(paper_id)]["path"]))
            for paper_id in paper_ids
        )

    identity = {
        "schema": "lattice-qcd-document-source-v2",
        "stem": stem,
        "metadata": dict(metadata),
        "generation_source_fingerprint": generation_source_fingerprint(),
        "files": _fingerprinted_files(paths),
    }
    return hashlib.sha256(
        json.dumps(
            identity,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _write_text_atomic(path: Path, text: str) -> None:
    """Write complete UTF-8 bytes to a unique sibling, then publish atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(text.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _write_json_atomic(path: Path, payload: object) -> None:
    """Serialize JSON completely before atomically publishing it."""

    _write_text_atomic(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )


def _copy_file_atomic(source: Path, destination: Path) -> None:
    """Copy to a unique sibling so concurrent publishers never share a temp."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
        shutil.copy2(source, temporary)
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _reject_duplicate_json_keys(pairs: Sequence[Tuple[str, object]]) -> object:
    result: Dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSON 对象含重复键：{key}")
        result[key] = value
    return result


def _load_json_strict(path: Path) -> object:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_reject_duplicate_json_keys,
    )


def _load_paper_source_map() -> Mapping[str, Mapping[str, object]]:
    payload = _load_json_strict(PAPER_SOURCE_MAP)
    if not isinstance(payload, Mapping):
        raise ValueError("paper_sources.json 顶层必须是对象")
    if payload.get("schema") != "lattice-qcd-course-paper-sources-v1":
        raise ValueError("paper_sources.json schema 不受支持")
    entries = payload.get("sources")
    if not isinstance(entries, list):
        raise ValueError("paper_sources.json 缺少 sources 数组")
    result: Dict[str, Mapping[str, object]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("paper_sources.json 的每个 source 必须是对象")
        paper_id = str(entry.get("paper_id", ""))
        if paper_id in result:
            raise ValueError(f"paper_sources.json 编号重复：{paper_id}")
        result[paper_id] = entry
    expected = {f"P{number:02d}" for number in range(1, 51)}
    if set(result) != expected:
        missing = sorted(expected - set(result))
        extra = sorted(set(result) - expected)
        raise ValueError(f"论文原始 PDF 映射不闭合：missing={missing}, extra={extra}")
    return result


def _source_path(locator: str) -> Path:
    path = (REPO_ROOT / locator).resolve()
    allowed_roots = (REPO_ROOT.resolve(), PYQCD_ROOT.resolve())
    if not any(path == root or root in path.parents for root in allowed_roots):
        raise ValueError(f"论文 PDF 路径越界：{locator}")
    return path


def parse_papers(require_pdfs: bool = True) -> Tuple[Paper, ...]:
    pattern = re.compile(
        r"^\|\s*(\d+)\s*\|\s*\x60([^\x60]+)\x60\s*\|\s*\x60([^\x60]+)\x60\s*\|"
        r"\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$"
    )
    source_map = _load_paper_source_map()
    papers: List[Paper] = []
    missing_pdfs: List[str] = []
    for raw_line in PAPER_INDEX.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw_line)
        if not match:
            continue
        number = int(match.group(1))
        paper_id = f"P{number:02d}"
        source = source_map[paper_id]
        locator = str(source.get("path", ""))
        source_pdf = _source_path(locator)
        if not source_pdf.is_file():
            missing_pdfs.append(f"{paper_id}: {locator}")
            original_pages = 0
            digest = ""
        else:
            original_pages = _pdf_pages(source_pdf)
            digest = _sha256(source_pdf)
        expected_digest = source.get("sha256")
        if expected_digest and digest and digest != str(expected_digest):
            raise ValueError(
                f"{paper_id}: 原始 PDF SHA-256 不符，expected={expected_digest}, "
                f"actual={digest}"
            )
        origin = match.group(6).strip()
        origin_match = re.search(r"arXiv:([^\s|]+)", origin)
        index_arxiv = origin_match.group(1) if origin_match else None
        mapped_arxiv = source.get("arxiv")
        if index_arxiv != mapped_arxiv:
            raise ValueError(
                f"{paper_id}: INDEX arXiv={index_arxiv}, "
                f"paper_sources.json arXiv={mapped_arxiv}"
            )
        papers.append(
            Paper(
                number=number,
                english_dir=match.group(2),
                chinese_dir=match.group(3),
                english_pages=int(match.group(4)),
                chinese_pages=int(match.group(5)),
                origin=origin,
                note=match.group(7).strip(),
                arxiv=str(mapped_arxiv) if mapped_arxiv is not None else None,
                repository=str(source.get("repository", "")),
                source_locator=locator,
                source_url=str(source.get("url", "")),
                source_pdf=source_pdf,
                original_pages=original_pages,
                sha256=digest,
            )
        )
    if tuple(p.number for p in papers) != tuple(range(1, 51)):
        raise ValueError("论文 INDEX.md 必须恰好解析为 P01--P50")
    if require_pdfs and missing_pdfs:
        raise FileNotFoundError("缺少完整原始论文 PDF：\n" + "\n".join(missing_pdfs))
    return tuple(papers)


def validate_paper_sources(papers: Sequence[Paper]) -> None:
    """拒绝缺页、重复映射或主题遗漏的论文图谱输入。"""

    if tuple(paper.paper_id for paper in papers) != tuple(
        f"P{number:02d}" for number in range(1, 51)
    ):
        raise ValueError("论文对象必须严格为 P01--P50")
    if any(paper.original_pages <= 0 for paper in papers):
        raise ValueError("每篇完整原始 PDF 必须至少有一页")
    paths = [paper.pdf_path for paper in papers]
    if len(paths) != len(set(paths)):
        raise ValueError("不同论文不得映射到同一个原始 PDF")
    repositories = {
        name: sum(paper.repository == name for paper in papers)
        for name in {paper.repository for paper in papers}
    }
    if repositories != {"PyQCD": 40, "course-cache": 10}:
        raise ValueError(f"论文来源计数异常：{repositories}")
    themed = [number for _, _, numbers in THEMES for number in numbers]
    if sorted(themed) != list(range(1, 51)) or len(themed) != 50:
        raise ValueError("六个论文主题必须让 P01--P50 恰好各出现一次")


def validate_sympy_payload(payload: object) -> Dict[str, Mapping[str, object]]:
    """Validate the exact cached schema for all 175 course-level records."""

    if not isinstance(payload, dict):
        raise ValueError("SymPy 结果顶层必须是 JSON 对象")
    if set(payload) != _SYMPY_PAYLOAD_KEYS:
        raise ValueError(
            "SymPy 顶层字段不匹配："
            f"actual={sorted(payload)} expected={sorted(_SYMPY_PAYLOAD_KEYS)}"
        )
    if payload.get("schema") != "lattice-qcd-course-sympy-v1":
        raise ValueError("SymPy 结果 schema 不受支持")
    if type(payload.get("total")) is not int or payload["total"] != len(
        EXPECTED_LESSON_CODES
    ):
        raise ValueError(
            f"SymPy total 必须精确为 {len(EXPECTED_LESSON_CODES)}"
        )
    records = payload.get("records")
    if not isinstance(records, list) or len(records) != len(EXPECTED_LESSON_CODES):
        raise ValueError("SymPy records 必须精确包含 175 项")

    validated: Dict[str, Mapping[str, object]] = {}
    for index, (expected_code, expected_id, record) in enumerate(
        zip(EXPECTED_LESSON_CODES, EXPECTED_SYMPY_IDS, records),
        start=1,
    ):
        if not isinstance(record, dict):
            raise ValueError(f"SymPy records[{index}] 必须是对象")
        if set(record) != _SYMPY_RECORD_KEYS:
            raise ValueError(
                f"{expected_id}: 字段不匹配 actual={sorted(record)} "
                f"expected={sorted(_SYMPY_RECORD_KEYS)}"
            )
        if record.get("lesson_code") != expected_code:
            raise ValueError(
                f"SymPy 单元顺序/编号错误：expected={expected_code}, "
                f"actual={record.get('lesson_code')}"
            )
        if record.get("validation_id") != expected_id:
            raise ValueError(
                f"SymPy 验证 ID 错误：expected={expected_id}, "
                f"actual={record.get('validation_id')}"
            )
        for field in ("title", "engine", "boundary"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{expected_id}: {field} 必须是非空字符串")
        if record.get("status") != "verified":
            raise ValueError(
                f"{expected_id}: status 必须为 verified，"
                f"actual={record.get('status')}"
            )
        checks = record.get("checks")
        if not isinstance(checks, dict) or not checks:
            raise ValueError(f"{expected_id}: checks 必须是非空对象")
        if any(not isinstance(name, str) or not name.strip() for name in checks):
            raise ValueError(f"{expected_id}: checks 名称不得为空")
        if any(type(value) is not bool for value in checks.values()):
            raise ValueError(f"{expected_id}: checks 的值必须是 JSON 布尔值")
        if not all(checks.values()):
            raise ValueError(f"{expected_id}: 存在未通过检查")
        assumptions = record.get("assumptions")
        if not isinstance(assumptions, list) or not assumptions:
            raise ValueError(f"{expected_id}: assumptions 必须是非空数组")
        if any(
            not isinstance(value, str) or not value.strip()
            for value in assumptions
        ):
            raise ValueError(f"{expected_id}: assumptions 不得含空项")
        validated[expected_code] = record

    if type(payload.get("passed")) is not int or payload["passed"] != len(
        validated
    ):
        raise ValueError(
            f"SymPy passed 必须由逐记录状态精确得到 {len(validated)}"
        )
    return validated


def load_sympy_records() -> Dict[str, Mapping[str, object]]:
    require_course_content()
    path = GENERATED_DIR / "sympy_validation.json"
    if not path.is_file():
        raise FileNotFoundError("缺少 SymPy 结果；先运行 python sympy_validation.py")
    records = validate_sympy_payload(_load_json_strict(path))
    actual_course_codes = tuple(
        lesson.code for volume in VOLUMES for lesson in volume.lessons
    )
    if actual_course_codes != EXPECTED_LESSON_CODES:
        raise ValueError("课程单元编号已偏离固定 01.01--35.05 契约")
    return records


def source_lookup(papers: Sequence[Paper]) -> Dict[str, Source]:
    result = dict(SOURCES)
    for paper in papers:
        result[paper.paper_id] = Source(
            title=paper.title,
            locator=paper.source_locator,
            role=(
                f"论文图谱 {paper.paper_id} 的完整原始 PDF；"
                f"底稿 {paper.origin}；SHA-256 {paper.sha256[:16]}…。"
            ),
        )
    return result


def validate_content_sources(lookup: Mapping[str, Source]) -> None:
    """Fail before generation when any structured-content source is unknown."""

    require_course_content()
    used = {source_id for volume in VOLUMES for source_id in volume.sources}
    used.update(
        source_id
        for volume in VOLUMES
        for lesson in volume.lessons
        for source_id in lesson.sources
    )
    unknown = sorted(used - set(lookup))
    if unknown:
        raise ValueError(f"课程内容引用未知来源：{unknown}")


def preamble(title: str, short_title: str) -> str:
    return "\n".join(
        (
            r"\documentclass[aspectratio=169,10pt]{ctexbeamer}",
            r"\input{../course_style.tex}",
            rf"\title[{tex_text(short_title)}]{{{tex_text(title)}}}",
            r"\author[格点 QCD 核心课]{格点 QCD 核心课程讲义}",
            r"\institute{从第一性原理到梯度流核子胶子 TMD-PDF}",
            r"\date{2026 年 8 月}",
            r"\begin{document}",
            "",
        )
    )


def render_title_frame(volume) -> str:
    lesson_rows = "\n".join(
        rf"{tex_text(item.code)} & {tex_text(item.title)}\\"
        for item in volume.lessons
    )
    return "\n".join(
        (
            rf"\begin{{frame}}[plain]\FrameAnchor{{V{volume.code}-title}}",
            r"\centering",
            rf"{{\Large\bfseries\color{{courseblue}}第 {int(volume.code)} 卷\par}}",
            r"\vspace{0.35cm}",
            rf"{{\LARGE\bfseries {tex_text(volume.title)}\par}}",
            r"\vspace{0.35cm}",
            rf"{{\large {tex_text(volume.goal)}\par}}",
            r"\vfill",
            rf"\CourseID{{Tbl}}{{{volume.code}.00}}\quad 5 个学习单元，固定编号不随合订方式改变",
            r"\end{frame}",
            "",
            rf"\begin{{frame}}[t]{{第 {int(volume.code)} 卷路线图}}\FrameAnchor{{V{volume.code}-route}}",
            r"\small",
            r"\begin{tabularx}{\linewidth}{p{0.14\linewidth}Y}",
            r"\toprule 编号 & 学习单元\\\midrule",
            lesson_rows,
            r"\bottomrule\end{tabularx}",
            r"\vfill",
            rf"\SourceLine{{{tex_text('；'.join(volume.sources))}}}",
            r"\end{frame}",
            "",
        )
    )


def render_diagnostic_frame(volume) -> str:
    prereq = "\n".join(rf"\item {tex_text(x)}" for x in volume.prerequisites)
    outcomes = "\n".join(rf"\item {tex_text(x)}" for x in volume.outcomes)
    diagnostic_note = (
        r"第 1 卷从高中毕业知识起步；诊断项答不出时直接学习本卷对应单元。"
        if volume.code == "01"
        else r"若先修项答不出，回到相应前卷；不要以术语熟悉代替可计算能力。"
    )
    return "\n".join(
        (
            rf"\begin{{frame}}[t]{{先修诊断与本卷出口}}\FrameAnchor{{V{volume.code}-diagnostic}}",
            r"\begin{columns}[T,onlytextwidth]",
            r"\column{0.48\textwidth}\begin{block}{开始前应能回答}",
            r"\small\begin{itemize}",
            prereq,
            r"\end{itemize}\end{block}",
            r"\column{0.48\textwidth}\begin{block}{学完后应能独立完成}",
            r"\small\begin{itemize}",
            outcomes,
            r"\end{itemize}\end{block}",
            r"\end{columns}",
            rf"\vfill\scriptsize {diagnostic_note}",
            r"\end{frame}",
            "",
        )
    )


def render_chart_frame(volume) -> str:
    chart = volume.chart
    colors = ("courseblue", "courseorange", "coursegreen", "coursepurple")
    plots: List[str] = []
    for idx, (label, expression) in enumerate(chart.series):
        plots.extend(
            (
                rf"\addplot[very thick,{colors[idx % len(colors)]},domain={chart.x_min}:{chart.x_max},samples=160] {{{expression}}};",
                rf"\addlegendentry{{{tex_text(label)}}}",
            )
        )
    return "\n".join(
        (
            rf"\begin{{frame}}[t]{{定量图：{tex_text(chart.title)}}}\FrameAnchor{{V{volume.code}-chart}}",
            r"\centering\begin{tikzpicture}",
            rf"\begin{{axis}}[width=0.88\linewidth,height=0.63\textheight,xmin={chart.x_min},xmax={chart.x_max},ymin={chart.y_min},ymax={chart.y_max},"
            rf"xlabel={{{chart.x_label}}},ylabel={{{chart.y_label}}},grid=major,grid style={{courseline!55}},"
            r"legend style={font=\scriptsize,draw=none,fill=white},tick label style={font=\scriptsize},label style={font=\small}]",
            *plots,
            r"\end{axis}\end{tikzpicture}",
            rf"\par\scriptsize\FigureID{{{volume.code}.00}}：{tex_text(chart.note)}",
            rf"\SourceLine{{{tex_text(chart.source)}}}",
            r"\end{frame}",
            "",
        )
    )


def render_lesson(lesson, validation: Mapping[str, object]) -> str:
    code = lesson.code
    definition_ids = tuple(
        stable_definition_id(code, name) for name, _ in lesson.terms
    )
    if len(definition_ids) != len(set(definition_ids)):
        raise ValueError(f"{code}: 稳定 Definition ID 冲突")
    terms_rows = "\n".join(
        rf"\DefinitionID{{{definition_id}}} {tex_text(name)} & {tex_text(desc)}\\"
        for definition_id, (name, desc) in zip(definition_ids, lesson.terms)
    )
    derivation = "\n".join(rf"\item {tex_text(x)}" for x in lesson.derivation)
    algorithm = "\n".join(rf"\item {tex_text(x)}" for x in lesson.algorithm)
    checks = "\n".join(
        rf"\item[\CheckMark] {tex_text(x)}" for x in lesson.checks
    )
    assumptions = "；".join(str(x) for x in validation["assumptions"][:3])
    check_count = sum(bool(x) for x in validation["checks"].values())
    source_ids = "；".join(lesson.sources)
    return "\n".join(
        (
            rf"\begin{{frame}}[t]{{{tex_text(lesson.title)}：问题与图像}}\FrameAnchor{{{code}-1}}",
            r"\footnotesize",
            rf"\begin{{block}}{{本节问题}}{tex_text(lesson.question)}\end{{block}}",
            rf"\PhysicalFlow{{{tex_text(lesson.picture[0])}}}{{{tex_text(lesson.picture[1])}}}{{{tex_text(lesson.picture[2])}}}{{{code}}}",
            rf"\begin{{block}}{{物理原则}}\KnowledgeID{{{code}}}\quad {tex_text(lesson.principle)}\end{{block}}",
            rf"\SourceLine{{{tex_text(source_ids)}}}",
            r"\end{frame}",
            "",
            rf"\begin{{frame}}[t]{{{tex_text(lesson.title)}：定义与主公式}}\FrameAnchor{{{code}-2}}",
            r"\footnotesize\begin{tabularx}{\linewidth}{p{0.30\linewidth}Y}",
            r"\toprule 术语 & 本课程中的精确定义\\\midrule",
            terms_rows,
            r"\bottomrule\end{tabularx}\vspace{0.15cm}",
            rf"\begin{{block}}{{\EquationID{{{code}}} 主公式}}\centering"
            rf"\CourseDisplayEquation{{{lesson.equation}}}\end{{block}}",
            tex_text(lesson.equation_meaning),
            r"\end{frame}",
            "",
            rf"\begin{{frame}}[t]{{{tex_text(lesson.title)}：推导与证据边界}}\FrameAnchor{{{code}-3}}",
            r"\footnotesize",
            rf"\DerivationID{{{code}}}\quad 由本节定义与前置结论逐步推出 \CourseRef{{Eq}}{{{code}}}：",
            r"\begin{enumerate}",
            derivation,
            r"\end{enumerate}\begin{block}{可执行检查}",
            rf"\SympyID{{{code}}}\quad {tex_text(str(validation['title']))}；"
            rf"{check_count}/{len(validation['checks'])} 项通过；{tex_text(str(validation['engine']))}。",
            rf"\par\scriptsize 假设：{tex_text(assumptions)}",
            r"\end{block}",
            rf"\BoundaryLine{{{tex_text(str(validation['boundary']))}}}",
            r"\end{frame}",
            "",
            rf"\begin{{frame}}[t]{{{tex_text(lesson.title)}：计算算法}}\FrameAnchor{{{code}-4}}",
            r"\footnotesize",
            rf"\AlgorithmID{{{code}}}\begin{{enumerate}}",
            algorithm,
            r"\end{enumerate}\begin{columns}[T,onlytextwidth]",
            r"\column{0.56\textwidth}\begin{block}{停止条件与交叉检查}\scriptsize\begin{itemize}",
            checks,
            r"\end{itemize}\end{block}",
            r"\column{0.40\textwidth}\begin{block}{代码映射}",
            rf"\scriptsize {tex_code(lesson.code_map)}",
            r"\end{block}\end{columns}\end{frame}",
            "",
            rf"\begin{{frame}}[t]{{{tex_text(lesson.title)}：练习与完整解答}}\FrameAnchor{{{code}-5}}",
            r"\footnotesize",
            rf"\begin{{block}}{{\ExerciseID{{{code}}}}}{tex_text(lesson.exercise)}\end{{block}}",
            rf"\begin{{exampleblock}}{{\SolutionID{{{code}}}}}{tex_text(lesson.solution)}\end{{exampleblock}}",
            r"\vfill",
            rf"\scriptsize 回看：\CourseRef{{Def}}{{{definition_ids[0]}}}；\CourseRef{{Eq}}{{{code}}}；"
            rf"\CourseRef{{SYM}}{{{code}}}；\CourseRef{{Alg}}{{{code}}}。",
            rf"\SourceLine{{{tex_text(source_ids)}}}",
            r"\end{frame}",
            "",
        )
    )


def render_closing_frames(volume, lookup: Mapping[str, Source]) -> str:
    outcomes = "\n".join(
        rf"\item[\CheckMark] {tex_text(item)}" for item in volume.outcomes
    )
    source_ids: List[str] = []
    candidates = list(volume.sources)
    candidates.extend(
        source_id for lesson in volume.lessons for source_id in lesson.sources
    )
    for source_id in candidates:
        if source_id not in source_ids:
            source_ids.append(source_id)
    rows: List[str] = []
    for source_id in source_ids:
        if source_id not in lookup:
            raise ValueError(
                f"V{volume.code}: 课程内容引用未知来源 {source_id!r}"
            )
        source = lookup[source_id]
        rows.append(
            rf"\SourceID{{{tex_text(source_id)}}} & {tex_text(source.title)} & {tex_text(source.role)}\\"
        )
    blocks = [
        rf"\begin{{frame}}[t]{{第 {int(volume.code)} 卷能力清单}}\FrameAnchor{{V{volume.code}-outcomes}}",
        r"\small\begin{itemize}",
        outcomes,
        r"\end{itemize}\vfill\begin{block}{通过标准}",
        r"不以“看懂”为标准：应能从空白纸推导主公式、实现算法、解释检查失败意味着什么，并完成本卷练习。",
        r"\end{block}\end{frame}",
        "",
    ]
    chunks = [rows[index : index + 5] for index in range(0, len(rows), 5)]
    for index, chunk in enumerate(chunks, start=1):
        anchor = (
            rf"\FrameAnchor{{V{volume.code}-sources}}"
            if index == 1
            else rf"\FrameAnchor{{V{volume.code}-sources-{index}}}"
        )
        blocks.extend(
            (
                rf"\begin{{frame}}[t]{{第 {int(volume.code)} 卷来源（{index}/{len(chunks)}）}}{anchor}",
                r"\scriptsize\begin{tabularx}{\linewidth}{p{0.17\linewidth}p{0.28\linewidth}Y}",
                r"\toprule ID & 来源 & 本卷用途\\\midrule",
                *chunk,
                r"\bottomrule\end{tabularx}\end{frame}",
                "",
            )
        )
    return "\n".join(blocks)


def render_volume_fragment(volume, validations, lookup) -> str:
    parts = [
        render_title_frame(volume),
        render_diagnostic_frame(volume),
        render_chart_frame(volume),
    ]
    parts.extend(
        render_lesson(lesson, validations[lesson.code])
        for lesson in volume.lessons
    )
    parts.append(render_closing_frames(volume, lookup))
    return "\n".join(parts)


def render_course_front() -> str:
    all_rows = [
        rf"{int(volume.code):02d} & {tex_text(volume.title)} & {tex_text(volume.goal)}\\"
        for volume in VOLUMES
    ]
    evidence_rows = (
        r"\StatusImplemented & 接口或函数存在；尚未证明数值和物理闭合\\",
        r"\StatusTested & 单元、性质或合成测试通过\\",
        r"\StatusClosed & 物理定义、几何、重整化、统计和极限方案闭合\\",
        r"\StatusPhysical & 真实多构型、多尺度数据完成验证\\",
    )
    blocks = [
        r"\begin{frame}[plain]\FrameAnchor{course-cover}",
        r"\titlepage",
        r"\vfill\centering\small 核心主线超过 1000 页；另附 50 篇中文论文逐页图谱。",
        r"\end{frame}",
        "",
        r"\begin{frame}[t]{编号、跳转与证据语言}\FrameAnchor{course-numbering}",
        r"\small\begin{tabularx}{\linewidth}{p{0.22\linewidth}Y}",
        r"\toprule 前缀 & 对象\\\midrule",
        r"K / Def / Eq / Der / Thm & 知识点、定义、主公式、推导链、显式命名定理\\",
        r"Fig / Tbl / Alg & 图、表、算法\\",
        r"Ex / Sol / Src / SYM & 练习、解答、来源、SymPy 证据\\",
        r"\bottomrule\end{tabularx}\vspace{0.2cm}",
        r"\begin{tabularx}{\linewidth}{p{0.23\linewidth}Y}",
        r"\toprule 状态 & 含义\\\midrule",
        *evidence_rows,
        r"\bottomrule\end{tabularx}\end{frame}",
        "",
    ]
    route_chunks = [
        all_rows[index : index + 7]
        for index in range(0, len(all_rows), 7)
    ]
    for part, rows in enumerate(route_chunks, start=1):
        blocks.extend(
            (
                rf"\begin{{frame}}[t]{{全课程路线（{part}/{len(route_chunks)}）}}\FrameAnchor{{course-map-{part}}}",
                r"\scriptsize\begin{tabularx}{\linewidth}{p{0.07\linewidth}p{0.27\linewidth}Y}",
                r"\toprule 卷 & 主题 & 能力出口\\\midrule",
                *rows,
                r"\bottomrule\end{tabularx}\end{frame}",
                "",
            )
        )
    for volume in VOLUMES:
        rows = "\n".join(
            rf"\hyperlink{{Fr:{lesson.code}-1}}{{{tex_text(lesson.code)}}} & "
            rf"{tex_text(lesson.title)} & Eq {tex_text(lesson.code)} / SYM {tex_text(lesson.code)}\\"
            for lesson in volume.lessons
        )
        blocks.extend(
            (
                rf"\begin{{frame}}[t]{{全局索引：第 {int(volume.code)} 卷}}\FrameAnchor{{course-index-{volume.code}}}",
                r"\small\begin{tabularx}{\linewidth}{p{0.15\linewidth}Yp{0.27\linewidth}}",
                r"\toprule 单元 & 主题 & 稳定对象 ID\\\midrule",
                rows,
                r"\bottomrule\end{tabularx}",
                rf"\vfill\hyperlink{{Fr:V{volume.code}-title}}{{进入第 {int(volume.code)} 卷}}",
                r"\end{frame}",
                "",
            )
        )
    return "\n".join(blocks)


def render_standalone_index() -> str:
    parts = [
        r"\begin{frame}[plain]\centering",
        r"{\LARGE\bfseries 全局索引与稳定编号\par}",
        r"\vspace{0.4cm}{\large 配合 \texttt{core\_complete.pdf} 使用\par}",
        r"\vfill 公式、算法、练习和 SymPy 证据均以 卷.单元 编号。",
        r"\end{frame}",
    ]
    for volume in VOLUMES:
        rows = "\n".join(
            rf"{tex_text(lesson.code)} & {tex_text(lesson.title)} & "
            rf"K/Def/Eq/Der/Fig/Alg/Ex/Sol/SYM {tex_text(lesson.code)}\\"
            for lesson in volume.lessons
        )
        parts.extend(
            (
                rf"\begin{{frame}}[t]{{第 {int(volume.code)} 卷：{tex_text(volume.title)}}}",
                r"\small\begin{tabularx}{\linewidth}{p{0.13\linewidth}Yp{0.42\linewidth}}",
                r"\toprule 单元 & 标题 & 对象 ID\\\midrule",
                rows,
                r"\bottomrule\end{tabularx}\end{frame}",
            )
        )
    return "\n".join(parts)


def paper_interface(paper: Paper, theme_title: str) -> str:
    first = f"{paper.paper_id}-p001"
    last = f"{paper.paper_id}-p{paper.original_pages:03d}"
    note = paper.note or "索引未记录额外备注。"
    arxiv = paper.arxiv or "无 arXiv 编号；按 DOI/库内原始 PDF 核验"
    return "\n".join(
        (
            rf"\begin{{frame}}[t]{{{paper.paper_id}：{tex_text(paper.title)}}}",
            r"\small\begin{tabularx}{\linewidth}{p{0.22\linewidth}Y}",
            rf"\toprule 主题归属 & {tex_text(theme_title)}\\",
            rf"底稿 & {tex_text(paper.origin)}\\",
            rf"arXiv / DOI & {tex_text(arxiv)}\\",
            rf"完整原始 PDF & {paper.original_pages} 页；来源 {tex_text(paper.repository)}；"
            rf"SHA-256 {tex_text(paper.sha256[:12])}\ldots\\",
            rf"转排索引 & EN {paper.english_pages} 页；ZH {paper.chinese_pages} 页（只作书目对照）\\",
            rf"备注 & {tex_text(note)}\\",
            r"\bottomrule\end{tabularx}\vspace{0.25cm}",
            r"\begin{block}{阅读方法}",
            r"先按课程主线定位定义和计算阶段，再阅读原文中的假设、推导、数值设置与结论；原文证据不得由课程概述替代。",
            r"\end{block}",
            rf"\vfill 页码范围：\hyperlink{{{first}}}{{{first}}} -- \hyperlink{{{last}}}{{{last}}}",
            r"\end{frame}",
            "",
        )
    )


def paper_pages(paper: Paper) -> str:
    relative = Path(os.path.relpath(paper.pdf_path, GENERATED_DIR))
    commands: List[str] = []
    for page in range(1, paper.original_pages + 1):
        page_id = f"{paper.paper_id}-p{page:03d}"
        commands.append(
            r"\includepdf[pages={"
            + str(page)
            + r"},pagecommand={\thispagestyle{empty}\hypertarget{"
            + page_id
            + r"}{}\begin{tikzpicture}[remember picture,overlay]"
            + r"\node[anchor=south east,fill=white,fill opacity=.88,text opacity=1,"
            + r"inner sep=1.2pt,font=\tiny\ttfamily] at "
            + r"([xshift=-2mm,yshift=2mm]current page.south east){"
            + page_id
            + r"};\end{tikzpicture}}]{"
            + r"\detokenize{"
            + relative.as_posix()
            + "}"
            + "}"
        )
    return "\n".join(commands)


def atlas_document(code: str, title: str, papers: Sequence[Paper]) -> str:
    front = "\n".join(
        (
            r"\documentclass[aspectratio=169,10pt]{ctexbeamer}",
            r"\usepackage{pdfpages,tikz,tabularx,booktabs,xcolor,hyperref}",
            r"\newcolumntype{Y}{>{\raggedright\arraybackslash}X}",
            r"\definecolor{atlasblue}{HTML}{17365D}",
            r"\setbeamertemplate{navigation symbols}{}",
            r"\setbeamercolor{structure}{fg=atlasblue}",
            r"\hypersetup{colorlinks=true,linkcolor=atlasblue}",
            rf"\title{{论文图谱 {code}：{tex_text(title)}}}",
            r"\author{格点 QCD 核心课程讲义}",
            r"\date{2026 年 8 月}",
            r"\begin{document}",
            r"\begin{frame}[plain]\titlepage",
            rf"\vfill\centering 收录 {len(papers)} 篇完整原始论文，共 {sum(p.original_pages for p in papers)} 个原文页面。",
            r"\end{frame}",
            r"\begin{frame}[t]{图谱使用说明}",
            r"\small 原始 PDF 页面保持内容不变并缩放到 16:9 安全区；右下角叠加稳定页面 ID。",
            r"\begin{itemize}",
            r"\item 课程中的 Pxx 引用指向一篇论文；Pxx-pyyy 指向完整原始 PDF 的具体页。",
            r"\item 接口页只说明课程位置，不替代论文的假设、推导和数值证据。",
            r"\item 书目信息以 refer/papers/INDEX.md 为准；原始 PDF 路径、哈希和页数独立核验。",
            r"\end{itemize}\end{frame}",
        )
    )
    body: List[str] = [front]
    for paper in papers:
        body.append(paper_interface(paper, title))
        body.append(paper_pages(paper))
    body.append(r"\end{document}")
    return "\n".join(body) + "\n"


def write_sources_md(papers: Sequence[Paper], lookup: Mapping[str, Source]) -> None:
    lines = [
        "# 来源注册表",
        "",
        "本表区分课程自编补足、仓库 book/doc/code/skill 和完整论文原文。Pxx 的页级引用见论文图谱中的 Pxx-pyyy。",
        "",
        "## 教材、讲义、代码与技能",
        "",
        "| ID | 来源 | 定位 | 用途 |",
        "|---|---|---|---|",
    ]
    for source_id in sorted(SOURCES):
        source = lookup[source_id]
        lines.append(
            f"| {source_id} | {source.title} | {source.locator} | {source.role} |"
        )
    lines.extend(
        (
            "",
            "## 论文 P01--P50",
            "",
            "| ID | 中文题名 | arXiv | 完整原始 PDF | 原始页 | SHA-256 | 图谱页 ID |",
            "|---|---|---|---|---:|---|---|",
        )
    )
    for paper in papers:
        lines.append(
            f"| {paper.paper_id} | {paper.title} | {paper.arxiv or 'DOI/Wilson74'} | "
            f"{paper.source_locator} | {paper.original_pages} | `{paper.sha256}` | "
            f"{paper.paper_id}-p001--{paper.paper_id}-p{paper.original_pages:03d} |"
        )
    _write_text_atomic(COURSE_DIR / "SOURCES.md", "\n".join(lines) + "\n")


def _document(title: str, short_title: str, body: str) -> str:
    return "\n".join(
        (preamble(title, short_title), body, r"\end{document}", "")
    )


def _frame_count(text: str) -> int:
    return text.count(r"\begin{frame}")


def generate_all(paper_jobs: int = 2) -> Mapping[str, object]:
    """生成全部 TeX、片段、来源表和可验证页数清单。"""

    require_course_content()
    fragments_dir = GENERATED_DIR / "fragments"
    papers = parse_papers(require_pdfs=True)
    validate_paper_sources(papers)
    validations = load_sympy_records()
    lookup = source_lookup(papers)
    validate_content_sources(lookup)
    generation_fingerprint = generation_source_fingerprint()

    fragments_dir.mkdir(parents=True, exist_ok=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    documents: Dict[str, Mapping[str, object]] = {}
    fragment_names: List[str] = []
    fragment_pages: Dict[str, int] = {}

    for volume in VOLUMES:
        fragment = render_volume_fragment(volume, validations, lookup)
        fragment_name = f"V{volume.code}.tex"
        fragment_path = fragments_dir / fragment_name
        _write_text_atomic(fragment_path, fragment + "\n")
        fragment_names.append(fragment_name)
        fragment_pages[volume.code] = _frame_count(fragment)

        stem = f"volume_{volume.code}_{volume.slug}"
        body = rf"\input{{fragments/{fragment_name}}}"
        tex_path = GENERATED_DIR / f"{stem}.tex"
        _write_text_atomic(
            tex_path,
            _document(
                f"第 {int(volume.code)} 卷：{volume.title}",
                f"V{volume.code} {volume.title}",
                body,
            ),
        )
        documents[stem] = {
            "kind": "volume",
            "tex": tex_path.name,
            "expected_pages": fragment_pages[volume.code],
            "volume": volume.code,
        }

    front = render_course_front()
    core_body = "\n".join(
        [front]
        + [rf"\input{{fragments/{name}}}" for name in fragment_names]
    )
    core_path = GENERATED_DIR / "core_complete.tex"
    _write_text_atomic(
        core_path,
        _document(
            "从零开始学习格点 QCD：梯度流核子胶子 TMD-PDF",
            "格点 QCD 核心全集",
            core_body,
        ),
    )
    documents["core_complete"] = {
        "kind": "core",
        "tex": core_path.name,
        "expected_pages": _frame_count(front) + sum(fragment_pages.values()),
        "volumes": len(VOLUMES),
        "lessons": sum(len(volume.lessons) for volume in VOLUMES),
    }

    index_body = render_standalone_index()
    index_path = GENERATED_DIR / "course_index.tex"
    _write_text_atomic(
        index_path,
        _document("格点 QCD 核心课程全局索引", "课程索引", index_body),
    )
    documents["course_index"] = {
        "kind": "index",
        "tex": index_path.name,
        "expected_pages": _frame_count(index_body),
    }

    papers_by_number = {paper.number: paper for paper in papers}
    for code, title, numbers in THEMES:
        selected = tuple(papers_by_number[number] for number in numbers)
        atlas_text = atlas_document(code, title, selected)
        stem = f"paper_atlas_{code}"
        atlas_path = GENERATED_DIR / f"{stem}.tex"
        _write_text_atomic(atlas_path, atlas_text)
        documents[stem] = {
            "kind": "atlas",
            "tex": atlas_path.name,
            "expected_pages": 2
            + len(selected)
            + sum(paper.original_pages for paper in selected),
            "papers": [paper.paper_id for paper in selected],
            "original_pages": sum(paper.original_pages for paper in selected),
        }

    write_sources_md(papers, lookup)
    manifest: Dict[str, object] = {
        "schema": "lattice-qcd-course-build-v2",
        "generation_source_fingerprint": generation_fingerprint,
        "volumes": len(VOLUMES),
        "lessons": sum(len(volume.lessons) for volume in VOLUMES),
        "sympy_records": len(validations),
        "papers": len(papers),
        "paper_original_pages": sum(paper.original_pages for paper in papers),
        "paper_source_counts": {
            "PyQCD": sum(paper.repository == "PyQCD" for paper in papers),
            "course-cache": sum(
                paper.repository == "course-cache" for paper in papers
            ),
        },
        "paper_sha256": {
            paper.paper_id: paper.sha256 for paper in papers
        },
        "documents": documents,
    }
    _write_json_atomic(GENERATED_DIR / "course_manifest.json", manifest)
    return manifest


@dataclass(frozen=True)
class CompileResult:
    stem: str
    pages: int
    expected_pages: int
    pdf: str
    overfull: int
    underfull: int
    missing_characters: int
    undefined_references: int


def _pdf_pages(pdf_path: Path) -> int:
    if shutil.which("pdfinfo"):
        result = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            check=True,
            text=True,
            capture_output=True,
        )
        match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
        if match is None:
            raise RuntimeError(f"pdfinfo 未返回页数：{pdf_path}")
        return int(match.group(1))
    if shutil.which("gs"):
        literal = (
            str(pdf_path.resolve())
            .replace("\\", "\\\\")
            .replace("(", r"\(")
            .replace(")", r"\)")
        )
        result = subprocess.run(
            [
                "gs",
                "-q",
                "-dNOSAFER",
                "-dNODISPLAY",
                "-c",
                f"({literal}) (r) file runpdfbegin pdfpagecount = quit",
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        value = result.stdout.strip()
        if not value.isdigit():
            raise RuntimeError(f"Ghostscript 未返回页数：{pdf_path}: {value}")
        return int(value)
    raise RuntimeError("缺少 pdfinfo 与 Ghostscript，无法核对 PDF 页数")


def compile_document(
    stem: str,
    metadata: Mapping[str, object],
) -> CompileResult:
    """在独立 build 子目录中两遍编译一个文档并执行日志硬闸门。"""

    require_course_content()
    tex_path = GENERATED_DIR / str(metadata["tex"])
    if not tex_path.is_file():
        raise FileNotFoundError(tex_path)
    target_dir = BUILD_DIR / stem
    target_dir.mkdir(parents=True, exist_ok=True)
    source_fingerprint = document_source_fingerprint(stem, metadata)
    record_path = target_dir / "compile_record.json"
    _write_json_atomic(
        record_path,
        {
            "schema": "lattice-qcd-course-compile-record-v1",
            "stem": stem,
            "status": "building",
            "source_fingerprint": source_fingerprint,
        },
    )
    command = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={target_dir}",
        tex_path.name,
    ]
    outputs: List[str] = []
    for _ in range(2):
        result = subprocess.run(
            command,
            cwd=GENERATED_DIR,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        outputs.append(result.stdout)
        if result.returncode != 0:
            log_path = target_dir / "build.log"
            _write_text_atomic(log_path, "\n\n".join(outputs))
            raise RuntimeError(
                f"{stem}: XeLaTeX 失败（exit={result.returncode}），见 {log_path}"
            )

    combined = "\n\n".join(outputs)
    final_output = outputs[-1]
    log_path = target_dir / "build.log"
    _write_text_atomic(log_path, combined)
    overfull = len(re.findall(r"Overfull \\[hv]box", combined))
    underfull = len(re.findall(r"Underfull \\[hv]box", combined))
    missing = combined.count("Missing character:")
    undefined = len(
        re.findall(
            r"(?:undefined references|Reference .* undefined)",
            final_output,
            flags=re.IGNORECASE,
        )
    )
    float_too_large = combined.count("Float too large")
    if overfull or missing or undefined or float_too_large:
        raise RuntimeError(
            f"{stem}: 日志闸门失败 overfull={overfull}, "
            f"float_too_large={float_too_large}, missing={missing}, "
            f"undefined={undefined}；见 {log_path}"
        )

    built_pdf = target_dir / f"{stem}.pdf"
    if not built_pdf.is_file() or built_pdf.stat().st_size == 0:
        raise RuntimeError(f"{stem}: 未生成非空 PDF")
    pages = _pdf_pages(built_pdf)
    expected_pages = int(metadata["expected_pages"])
    if pages != expected_pages:
        raise RuntimeError(
            f"{stem}: 页数不闭合 expected={expected_pages}, actual={pages}"
        )
    final_pdf = PDF_DIR / built_pdf.name
    _copy_file_atomic(built_pdf, final_pdf)
    _write_json_atomic(
        record_path,
        {
            "schema": "lattice-qcd-course-compile-record-v1",
            "stem": stem,
            "status": "passed",
            "source_fingerprint": source_fingerprint,
            "xelatex_runs": 2,
            "pages": pages,
            "expected_pages": expected_pages,
            "pdf": str(final_pdf.relative_to(COURSE_DIR)),
            "pdf_sha256": _sha256(final_pdf),
            "log_sha256": _sha256(log_path),
        },
    )
    return CompileResult(
        stem=stem,
        pages=pages,
        expected_pages=expected_pages,
        pdf=str(final_pdf.relative_to(COURSE_DIR)),
        overfull=overfull,
        underfull=underfull,
        missing_characters=missing,
        undefined_references=undefined,
    )


def _selected_documents(
    documents: Mapping[str, Mapping[str, object]],
    target: str,
) -> Dict[str, Mapping[str, object]]:
    if target == "all":
        return dict(documents)
    kind = {
        "core": "core",
        "volumes": "volume",
        "index": "index",
        "atlases": "atlas",
    }[target]
    return {
        stem: metadata
        for stem, metadata in documents.items()
        if metadata["kind"] == kind
    }


def compile_all(
    manifest: Mapping[str, object],
    target: str = "all",
    jobs: int = 2,
) -> Tuple[CompileResult, ...]:
    require_course_content()
    if manifest.get("schema") != "lattice-qcd-course-build-v2":
        raise ValueError("拒绝编译旧版或未知 schema 的课程 manifest")
    actual_generation_fingerprint = generation_source_fingerprint()
    if (
        manifest.get("generation_source_fingerprint")
        != actual_generation_fingerprint
    ):
        raise ValueError(
            "课程 manifest 与当前结构化内容/生成器/来源/验证事实不一致；"
            "必须先重新 generate"
        )
    raw_documents = manifest["documents"]
    if not isinstance(raw_documents, Mapping):
        raise TypeError("manifest.documents 必须是映射")
    documents = _selected_documents(raw_documents, target)
    results: List[CompileResult] = []
    failures: List[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        future_map = {
            pool.submit(compile_document, stem, metadata): stem
            for stem, metadata in documents.items()
        }
        for future in concurrent.futures.as_completed(future_map):
            stem = future_map[future]
            try:
                result = future.result()
            except Exception as exc:  # 汇总所有独立文档失败
                failures.append(f"{stem}: {exc}")
            else:
                results.append(result)
                print(
                    f"compiled {stem}: {result.pages}/{result.expected_pages} pages"
                )
    if failures:
        raise RuntimeError("编译失败：\n" + "\n".join(sorted(failures)))
    results.sort(key=lambda item: item.stem)
    _write_json_atomic(
        GENERATED_DIR / f"compile_results_{target}.json",
        [result.__dict__ for result in results],
    )
    return tuple(results)


def load_manifest() -> Mapping[str, object]:
    path = GENERATED_DIR / "course_manifest.json"
    if not path.is_file():
        raise FileNotFoundError("缺少 course_manifest.json；先执行 generate")
    payload = _load_json_strict(path)
    if not isinstance(payload, Mapping):
        raise TypeError("course_manifest.json 顶层必须是对象")
    return payload


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        nargs="?",
        default="generate",
        choices=("generate", "compile", "all"),
    )
    parser.add_argument(
        "--target",
        default="all",
        choices=("all", "core", "volumes", "index", "atlases"),
    )
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--paper-jobs", type=int, default=2)
    args = parser.parse_args(argv)

    manifest = (
        generate_all(paper_jobs=args.paper_jobs)
        if args.action in {"generate", "all"}
        else load_manifest()
    )
    print(
        "generated: "
        f"volumes={manifest['volumes']}, lessons={manifest['lessons']}, "
        f"papers={manifest['papers']}, paper_pages={manifest['paper_original_pages']}"
    )
    if args.action in {"compile", "all"}:
        results = compile_all(manifest, target=args.target, jobs=args.jobs)
        print(f"compiled documents: {len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""验证格点 QCD 长课程的结构、证据、论文来源和 PDF 闭合性。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, List, Mapping, Optional, Sequence

from PIL import Image

from build_course import (
    COURSE_CONTENT_IMPORT_ERROR,
    COURSE_DIR,
    GENERATED_DIR,
    PDF_DIR,
    THEMES,
    VOLUMES,
    EXPECTED_LESSON_CODES,
    _reject_duplicate_json_keys,
    _write_json_atomic,
    _pdf_pages,
    document_source_fingerprint,
    generation_source_fingerprint,
    load_manifest,
    parse_papers,
    stable_definition_id,
    tex_text,
    validate_sympy_payload,
    validate_paper_sources,
)
from myqcd.run_all import EXPECTED_EXAMPLE_IDS
from render_audit import (
    AUDIT_SCHEMA,
    CONTACT_HEIGHT,
    CONTACT_WIDTH,
    GRID_COLUMNS,
    GRID_ROWS,
    MIN_DPI,
    audit_page_image,
    calculate_audit_fingerprint,
    expected_page_dimensions,
    render_source_identity,
)
from source_registry import SOURCES


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def _check(checks: List[Check], name: str, condition: object, detail: str) -> None:
    checks.append(Check(name=name, passed=bool(condition), detail=detail))


def _load_json(path: Path) -> Mapping[str, object]:
    if not path.is_file():
        raise FileNotFoundError(path)
    payload = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_reject_duplicate_json_keys,
    )
    if not isinstance(payload, Mapping):
        raise ValueError(f"{path}: JSON 顶层必须是对象")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_structure(checks: List[Check]) -> None:
    _check(
        checks,
        "structure.content_import",
        COURSE_CONTENT_IMPORT_ERROR is None,
        COURSE_CONTENT_IMPORT_ERROR or "结构化课程内容导入成功",
    )
    if COURSE_CONTENT_IMPORT_ERROR is not None:
        return
    lessons = [lesson for volume in VOLUMES for lesson in volume.lessons]
    codes = [lesson.code for lesson in lessons]
    _check(checks, "structure.volumes", len(VOLUMES) == 35, f"actual={len(VOLUMES)} expected=35")
    _check(checks, "structure.lessons", len(lessons) == 175, f"actual={len(lessons)} expected=175")
    _check(
        checks,
        "structure.five_lessons_per_volume",
        all(len(volume.lessons) == 5 for volume in VOLUMES),
        "每卷必须恰有 5 个单元",
    )
    _check(checks, "structure.unique_ids", len(codes) == len(set(codes)), f"unique={len(set(codes))}")
    expected_codes = [f"{volume:02d}.{lesson:02d}" for volume in range(1, 36) for lesson in range(1, 6)]
    _check(checks, "structure.ordered_ids", codes == expected_codes, "01.01--35.05 顺序闭合")
    _check(
        checks,
        "structure.content_contract",
        all(
            len(lesson.picture) == 3
            and len(lesson.terms) >= 3
            and len(lesson.derivation) >= 3
            and len(lesson.algorithm) >= 4
            and len(lesson.checks) >= 2
            and lesson.sympy_check == f"SYM-{lesson.code}"
            for lesson in lessons
        ),
        "物理图/定义/推导/算法/边界/SymPy ID",
    )
    definition_ids = [
        stable_definition_id(lesson.code, name)
        for lesson in lessons
        for name, _ in lesson.terms
    ]
    reordered_probe = [
        stable_definition_id(lessons[0].code, name)
        for name, _ in reversed(lessons[0].terms)
    ]
    _check(
        checks,
        "structure.stable_definition_ids",
        len(definition_ids) == len(set(definition_ids))
        and set(reordered_probe) == set(definition_ids[: len(reordered_probe)])
        and stable_definition_id("34.05", "目标 TMD") == "34.05-b2dca0f7e1",
        f"total={len(definition_ids)} unique={len(set(definition_ids))}",
    )
    used_sources = {source for lesson in lessons for source in lesson.sources}
    used_sources.update(source for volume in VOLUMES for source in volume.sources)
    allowed_papers = {f"P{number:02d}" for number in range(1, 51)}
    unknown = sorted(used_sources - set(SOURCES) - allowed_papers)
    _check(checks, "structure.source_ids", not unknown, f"unknown={unknown}")


_TEACHING_PAYLOAD_KEYS = frozenset(("schema", "total", "passed", "records"))
_TEACHING_RECORD_KEYS = frozenset(
    (
        "example_id",
        "title",
        "course_refs",
        "status",
        "checks",
        "assumptions",
        "boundary",
        "source_refs",
        "equations",
    )
)


def _nonblank_json_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def validate_teaching_payload(payload: object) -> Sequence[Mapping[str, object]]:
    """Validate exact IDs and every evidence-bearing field for 26 examples."""

    if not isinstance(payload, dict):
        raise ValueError("教学 SymPy 结果顶层必须是对象")
    if set(payload) != _TEACHING_PAYLOAD_KEYS:
        raise ValueError(
            "教学 SymPy 顶层字段不匹配："
            f"actual={sorted(payload)} expected={sorted(_TEACHING_PAYLOAD_KEYS)}"
        )
    if payload.get("schema") != "lqcd-course-myqcd-examples-v1":
        raise ValueError("教学 SymPy schema 不受支持")
    expected_total = len(EXPECTED_EXAMPLE_IDS)
    if type(payload.get("total")) is not int or payload["total"] != expected_total:
        raise ValueError(f"教学 SymPy total 必须精确为 {expected_total}")
    records = payload.get("records")
    if not isinstance(records, list) or len(records) != expected_total:
        raise ValueError(f"教学 SymPy records 必须精确包含 {expected_total} 项")

    allowed_sources = set(SOURCES) | {f"P{number:02d}" for number in range(1, 51)}
    for index, (expected_id, record) in enumerate(
        zip(EXPECTED_EXAMPLE_IDS, records),
        start=1,
    ):
        if not isinstance(record, dict):
            raise ValueError(f"教学 records[{index}] 必须是对象")
        if set(record) != _TEACHING_RECORD_KEYS:
            raise ValueError(
                f"{expected_id}: 字段不匹配 actual={sorted(record)} "
                f"expected={sorted(_TEACHING_RECORD_KEYS)}"
            )
        if record.get("example_id") != expected_id:
            raise ValueError(
                f"教学例题顺序/ID 错误：expected={expected_id}, "
                f"actual={record.get('example_id')}"
            )
        for field in ("title", "boundary"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{expected_id}: {field} 必须是非空字符串")
        if record.get("status") != "verified":
            raise ValueError(f"{expected_id}: status 必须为 verified")
        checks_map = record.get("checks")
        if not isinstance(checks_map, dict) or not checks_map:
            raise ValueError(f"{expected_id}: checks 必须是非空对象")
        if any(
            not isinstance(name, str) or not name.strip() for name in checks_map
        ):
            raise ValueError(f"{expected_id}: checks 名称不得为空")
        if any(type(value) is not bool for value in checks_map.values()):
            raise ValueError(f"{expected_id}: checks 值必须是 JSON 布尔值")
        if not all(checks_map.values()):
            raise ValueError(f"{expected_id}: 存在未通过检查")
        for field in ("course_refs", "assumptions", "source_refs"):
            if not _nonblank_json_strings(record.get(field)):
                raise ValueError(f"{expected_id}: {field} 必须是非空字符串数组")
        course_refs = record["course_refs"]
        if any(ref not in EXPECTED_LESSON_CODES for ref in course_refs):
            raise ValueError(f"{expected_id}: course_refs 含未知单元")
        source_refs = record["source_refs"]
        unknown_sources = sorted(set(source_refs) - allowed_sources)
        if unknown_sources:
            raise ValueError(
                f"{expected_id}: source_refs 含未知来源 {unknown_sources}"
            )
        equations = record.get("equations")
        if not isinstance(equations, dict) or not equations:
            raise ValueError(f"{expected_id}: equations 必须是非空对象")
        if any(
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(value, str)
            or not value.strip()
            for name, value in equations.items()
        ):
            raise ValueError(f"{expected_id}: equations 含空名称或空表达式")
    if type(payload.get("passed")) is not int or payload["passed"] != expected_total:
        raise ValueError(
            f"教学 SymPy passed 必须由逐记录状态精确得到 {expected_total}"
        )
    return records


def _payload_digest(payload: Mapping[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _command_detail(result: subprocess.CompletedProcess[str]) -> str:
    output = (result.stdout + result.stderr).strip()
    return output.splitlines()[-1] if output else f"exit={result.returncode}"


def verify_symbolic_evidence(checks: List[Check], run_sympy: bool) -> None:
    cached_payloads: dict[str, Mapping[str, object]] = {}
    cached_specs = (
        (
            "course",
            GENERATED_DIR / "sympy_validation.json",
            validate_sympy_payload,
            "175/175 exact IDs",
        ),
        (
            "teaching",
            GENERATED_DIR / "myqcd_examples.json",
            validate_teaching_payload,
            "26/26 exact IDs",
        ),
    )
    for name, path, validator, success_detail in cached_specs:
        try:
            payload = _load_json(path)
            validator(payload)
        except Exception as exc:
            _check(
                checks,
                f"sympy.{name}_cached",
                False,
                f"{type(exc).__name__}: {exc}",
            )
        else:
            cached_payloads[name] = payload
            _check(
                checks,
                f"sympy.{name}_cached",
                True,
                f"{success_detail}; sha256={_payload_digest(payload)}",
            )
    if not run_sympy:
        return

    with tempfile.TemporaryDirectory(prefix="lqcd-sympy-live-") as temporary:
        temporary_root = Path(temporary)
        course_output = temporary_root / "course"
        teaching_output = temporary_root / "myqcd_examples.json"
        jobs = (
            (
                "course",
                [
                    sys.executable,
                    str(COURSE_DIR / "sympy_validation.py"),
                    "--output-dir",
                    str(course_output),
                ],
                course_output / "sympy_validation.json",
                validate_sympy_payload,
            ),
            (
                "teaching",
                [
                    sys.executable,
                    str(COURSE_DIR / "myqcd" / "run_all.py"),
                    "--quiet",
                    "--json",
                    str(teaching_output),
                ],
                teaching_output,
                validate_teaching_payload,
            ),
        )
        for name, command, output_path, validator in jobs:
            try:
                result = subprocess.run(
                    command,
                    cwd=COURSE_DIR,
                    text=True,
                    capture_output=True,
                    timeout=900,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                _check(
                    checks,
                    f"sympy.live_{name}",
                    False,
                    f"{type(exc).__name__}: {exc}",
                )
                continue
            if result.returncode != 0:
                _check(
                    checks,
                    f"sympy.live_{name}",
                    False,
                    _command_detail(result),
                )
                continue
            try:
                live = _load_json(output_path)
                validator(live)
            except Exception as exc:
                _check(
                    checks,
                    f"sympy.live_{name}",
                    False,
                    f"{type(exc).__name__}: {exc}; {_command_detail(result)}",
                )
                continue
            cached = cached_payloads.get(name)
            matches = cached is not None and live == cached
            _check(
                checks,
                f"sympy.live_{name}",
                matches,
                f"live={_payload_digest(live)} "
                f"cached={_payload_digest(cached) if cached is not None else 'invalid'} "
                f"output={_command_detail(result)}",
            )


def _paper_identity(paper) -> bool:
    if not shutil.which("gs"):
        raise RuntimeError("缺少 Ghostscript，无法核验论文首页身份")
    result = subprocess.run(
        [
            "gs",
            "-q",
            "-dNOSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-dFirstPage=1",
            "-dLastPage=3",
            "-sDEVICE=txtwrite",
            "-sOutputFile=-",
            str(paper.pdf_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    text = result.stdout.decode("utf-8", errors="ignore").lower().replace(" ", "")
    if paper.arxiv:
        return result.returncode == 0 and paper.arxiv.lower().replace(" ", "") in text
    return result.returncode == 0 and "confinement" in text and "kenneth" in text and "wilson" in text


def verify_papers(checks: List[Check], check_identities: bool) -> None:
    papers = parse_papers(require_pdfs=True)
    validate_paper_sources(papers)
    total_pages = sum(paper.original_pages for paper in papers)
    _check(checks, "papers.count", len(papers) == 50, f"actual={len(papers)}")
    _check(checks, "papers.pages", total_pages == 1115, f"actual={total_pages}")
    _check(
        checks,
        "papers.repositories",
        sum(paper.repository == "PyQCD" for paper in papers) == 40
        and sum(paper.repository == "course-cache" for paper in papers) == 10,
        "PyQCD=40 course-cache=10",
    )
    themed = [number for _, _, numbers in THEMES for number in numbers]
    _check(
        checks,
        "papers.atlas_partition",
        len(themed) == 50 and sorted(themed) == list(range(1, 51)),
        "P01--P50 各出现一次",
    )
    if check_identities:
        failed = [paper.paper_id for paper in papers if not _paper_identity(paper)]
        _check(checks, "papers.identity", not failed, f"passed={50-len(failed)}/50 failed={failed}")


def verify_generated(checks: List[Check]) -> None:
    manifest = load_manifest()
    expected_generation_fingerprint = generation_source_fingerprint()
    _check(
        checks,
        "generated.generation_fingerprint",
        manifest.get("schema") == "lattice-qcd-course-build-v2"
        and manifest.get("generation_source_fingerprint")
        == expected_generation_fingerprint,
        f"schema={manifest.get('schema')} "
        f"recorded={manifest.get('generation_source_fingerprint')} "
        f"actual={expected_generation_fingerprint}",
    )
    documents = manifest.get("documents", {})
    if not isinstance(documents, dict):
        raise ValueError("manifest documents 必须是对象")
    kinds = {
        kind: sum(meta.get("kind") == kind for meta in documents.values())
        for kind in ("volume", "core", "index", "atlas")
    }
    _check(
        checks,
        "generated.documents_43",
        len(documents) == 43 and kinds == {"volume": 35, "core": 1, "index": 1, "atlas": 6},
        f"total={len(documents)} kinds={kinds}",
    )
    paths = [GENERATED_DIR / str(meta["tex"]) for meta in documents.values()]
    _check(checks, "generated.tex_files", all(path.is_file() for path in paths), f"present={sum(path.is_file() for path in paths)}/43")
    fragments = sorted((GENERATED_DIR / "fragments").glob("V??.tex"))
    expected_fragments = [
        GENERATED_DIR / "fragments" / f"V{number:02d}.tex"
        for number in range(1, 36)
    ]
    _check(
        checks,
        "generated.fragments",
        fragments == expected_fragments,
        f"actual={len(fragments)} expected=35",
    )
    serializer_cases = {
        "√(8τ)": r"\ensuremath{\sqrt{8\tau}}",
        "√13": r"\ensuremath{\sqrt{13}}",
        "R≃S": r"R\ensuremath{\simeq}S",
        "A∼B": r"A\ensuremath{\sim}B",
        "e^{-mL}": r"e\ensuremath{^{-mL}}",
        "T^-1": r"T\ensuremath{^{-1}}",
        "T⁻¹": r"T\ensuremath{^{-1}}",
        "xⁿ⁻¹": r"x\ensuremath{^{n-1}}",
        "Σₙ₌₁ᴺ⁻¹": r"\ensuremath{\Sigma}\ensuremath{_{n=1}}\ensuremath{^{N-1}}",
        "φ_{j+1}": r"\ensuremath{\phi}\ensuremath{_{j+1}}",
        "$f_1^{g[-,-]}$": r"\ensuremath{f_1^{g[-,-]}}",
        "$C_{S→std}$": r"\ensuremath{C_{S\rightarrow{}std}}",
        "目标 $f_1^{g[-,-]}$": r"目标 \ensuremath{f_1^{g[-,-]}}",
        "价格 $5": r"价格 \$5",
    }
    serializer_failures = {
        source: tex_text(source)
        for source, expected in serializer_cases.items()
        if tex_text(source) != expected
    }
    _check(
        checks,
        "generated.inline_math_serializer",
        not serializer_failures,
        f"failures={serializer_failures}",
    )
    core = documents.get("core_complete", {})
    _check(
        checks,
        "generated.core_over_1000",
        int(core.get("expected_pages", 0)) > 1000,
        f"expected_pages={core.get('expected_pages')}",
    )
    _check(
        checks,
        "generated.manifest_counts",
        manifest.get("volumes") == 35
        and manifest.get("lessons") == 175
        and manifest.get("sympy_records") == 175
        and manifest.get("papers") == 50
        and manifest.get("paper_original_pages") == 1115,
        "35/175/175/50/1115",
    )
    atlas_ids = [
        paper_id
        for meta in documents.values()
        if meta.get("kind") == "atlas"
        for paper_id in meta.get("papers", [])
    ]
    _check(
        checks,
        "generated.atlas_unique",
        len(atlas_ids) == 50 and len(set(atlas_ids)) == 50,
        f"occurrences={len(atlas_ids)} unique={len(set(atlas_ids))}",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    fragment_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(fragments)
    )
    teaching_text = combined + "\n" + fragment_text
    generated_definition_ids = re.findall(
        r"\\DefinitionID\{([^{}]+)\}", fragment_text
    )
    expected_definition_ids = [
        stable_definition_id(lesson.code, name)
        for volume in VOLUMES
        for lesson in volume.lessons
        for name, _ in lesson.terms
    ]
    derivation_count = fragment_text.count(r"\DerivationID{")
    _check(
        checks,
        "generated.stable_definition_ids",
        generated_definition_ids == expected_definition_ids,
        f"actual={len(generated_definition_ids)} expected={len(expected_definition_ids)}",
    )
    _check(
        checks,
        "generated.derivation_semantics",
        derivation_count == 175
        and r"\TheoremID{" not in fragment_text
        and "由本节定义与前置结论逐步推出" in fragment_text,
        f"derivations={derivation_count}",
    )
    v01_fragment = GENERATED_DIR / "fragments" / "V01.tex"
    v01_text = (
        v01_fragment.read_text(encoding="utf-8")
        if v01_fragment.is_file()
        else ""
    )
    _check(
        checks,
        "generated.v01_diagnostic",
        "第 1 卷从高中毕业知识起步" in v01_text
        and "回到相应前卷" not in v01_text,
        "首卷不得引用不存在的前卷",
    )
    broken_math_markers = {
        marker: teaching_text.count(marker)
        for marker in (r"\textasciicircum{}", r"\sqrt{\phantom{x}}")
        if marker in teaching_text
    }
    _check(
        checks,
        "generated.no_broken_inline_math",
        not broken_math_markers,
        f"found={broken_math_markers}",
    )
    placeholders = sorted(
        set(re.findall(r"<待填>|\bTODO\b|\bTBD\b", teaching_text))
    )
    _check(checks, "generated.no_placeholders", not placeholders, f"found={placeholders}")
    _check(
        checks,
        "generated.no_auto_framebreaks",
        "allowframebreaks" not in teaching_text,
        "固定 frame",
    )


def verify_compiled(checks: List[Check], require_all: bool) -> None:
    manifest = load_manifest()
    documents = manifest["documents"]
    present = 0
    failures: List[str] = []
    provenance_failures: List[str] = []
    for stem, meta in documents.items():
        pdf = PDF_DIR / f"{stem}.pdf"
        if not pdf.is_file():
            if require_all:
                failures.append(f"{stem}:missing-pdf")
            continue
        present += 1
        actual = _pdf_pages(pdf)
        if actual != int(meta["expected_pages"]):
            failures.append(f"{stem}:pages={actual}/{meta['expected_pages']}")
        log = COURSE_DIR / "build" / stem / "build.log"
        if not log.is_file():
            failures.append(f"{stem}:missing-log")
            continue
        text = log.read_text(encoding="utf-8", errors="replace")
        if re.search(r"Overfull \\[hv]box|Float too large|Missing character:", text):
            failures.append(f"{stem}:log-gate")
        final_pass = text[text.rfind("This is XeTeX") :] if "This is XeTeX" in text else text
        if re.search(r"undefined references|Reference .* undefined", final_pass, re.IGNORECASE):
            failures.append(f"{stem}:undefined-reference")
        record_path = COURSE_DIR / "build" / stem / "compile_record.json"
        if not record_path.is_file():
            provenance_failures.append(f"{stem}:missing-record")
            continue
        record = _load_json(record_path)
        try:
            source_fingerprint = document_source_fingerprint(stem, meta)
        except Exception as exc:
            provenance_failures.append(
                f"{stem}:source-fingerprint-{type(exc).__name__}"
            )
            continue
        if record.get("schema") != "lattice-qcd-course-compile-record-v1":
            provenance_failures.append(f"{stem}:record-schema")
        elif record.get("status") != "passed":
            provenance_failures.append(f"{stem}:record-{record.get('status')}")
        elif record.get("source_fingerprint") != source_fingerprint:
            provenance_failures.append(f"{stem}:stale-source")
        elif record.get("xelatex_runs") != 2:
            provenance_failures.append(f"{stem}:runs={record.get('xelatex_runs')}")
        elif record.get("pages") != actual or record.get("expected_pages") != int(meta["expected_pages"]):
            provenance_failures.append(f"{stem}:record-pages")
        elif record.get("pdf_sha256") != _sha256(pdf):
            provenance_failures.append(f"{stem}:stale-pdf")
        elif record.get("log_sha256") != _sha256(log):
            provenance_failures.append(f"{stem}:stale-log")
    _check(
        checks,
        "compiled.pdfs",
        not failures and (present == 43 if require_all else present > 0),
        f"present={present}/43 failures={failures}",
    )
    _check(
        checks,
        "compiled.provenance",
        not provenance_failures and (present == 43 if require_all else present > 0),
        f"present={present}/43 failures={provenance_failures}",
    )


def verify_visual_audit(checks: List[Check], require_all: bool) -> None:
    audit_path = COURSE_DIR / "visual_audit" / "render_audit.json"
    if not audit_path.is_file():
        _check(
            checks,
            "visual.report",
            not require_all,
            "missing visual_audit/render_audit.json"
            + ("（严格模式要求存在）" if require_all else "（非严格模式跳过）"),
        )
        return

    audit = _load_json(audit_path)
    if audit.get("schema") != AUDIT_SCHEMA:
        _check(
            checks,
            "visual.report",
            False,
            f"schema={audit.get('schema')} expected={AUDIT_SCHEMA}; 必须重新渲染",
        )
        return

    audit_root = audit_path.parent
    manifest = load_manifest()
    documents = manifest["documents"]
    if not isinstance(documents, Mapping):
        raise ValueError("manifest documents 必须是对象")
    parameters_ok = (
        type(audit.get("dpi")) is int
        and int(audit["dpi"]) >= MIN_DPI
        and audit.get("columns") == GRID_COLUMNS
        and type(audit.get("columns")) is int
        and audit.get("rows") == GRID_ROWS
        and type(audit.get("rows")) is int
    )
    expected_image_size = (
        expected_page_dimensions(int(audit["dpi"])) if parameters_ok else None
    )
    expected_pages = sum(int(meta["expected_pages"]) for meta in documents.values())
    expected_page_specs = [
        (
            str(stem),
            page,
            f"pages/{stem}/page-{page:04d}.jpg",
        )
        for stem, metadata in documents.items()
        for page in range(1, int(metadata["expected_pages"]) + 1)
    ]
    page_record_keys = frozenset(
        (
            "stem",
            "page",
            "image",
            "sha256",
            "width",
            "height",
            "aspect_ratio",
            "nonwhite_fraction",
            "outer_ink_fraction",
            "grayscale_stddev",
            "blank_suspect",
            "edge_suspect",
            "aspect_suspect",
        )
    )
    pages = audit.get("pages")
    page_records = pages if isinstance(pages, list) else []
    page_failures: List[str] = []
    recomputed_pages: List[Mapping[str, object]] = []
    recorded_page_paths: List[str] = []
    resolved_page_paths: List[Path] = []
    if len(page_records) != len(expected_page_specs):
        page_failures.append(
            f"record-count={len(page_records)}/{len(expected_page_specs)}"
        )
    for index, (stem, page, expected_path) in enumerate(expected_page_specs):
        if index >= len(page_records):
            page_failures.append(f"{stem}:p{page:04d}:missing-record")
            continue
        record = page_records[index]
        label = f"{stem}:p{page:04d}"
        if not isinstance(record, dict):
            page_failures.append(f"{label}:record-not-object")
            continue
        if set(record) != page_record_keys:
            page_failures.append(f"{label}:record-fields")
            continue
        recorded_page_paths.append(str(record.get("image")))
        if (
            record.get("stem") != stem
            or type(record.get("page")) is not int
            or record.get("page") != page
            or record.get("image") != expected_path
        ):
            page_failures.append(f"{label}:identity-or-path")
            continue
        image_path = audit_root / expected_path
        if not image_path.is_file() or image_path.is_symlink():
            page_failures.append(f"{label}:missing-or-symlink-image")
            continue
        resolved_page_paths.append(image_path.resolve())
        try:
            actual = asdict(audit_page_image(stem, page, image_path, audit_root))
        except Exception as exc:
            page_failures.append(f"{label}:image-{type(exc).__name__}")
            continue
        recomputed_pages.append(actual)
        if expected_image_size is not None and (
            abs(int(actual["width"]) - expected_image_size[0]) > 1
            or abs(int(actual["height"]) - expected_image_size[1]) > 1
        ):
            page_failures.append(
                f"{label}:dpi-size={actual['width']}x{actual['height']}"
            )
        if record != actual or any(
            type(record[key]) is not type(actual[key]) for key in page_record_keys
        ):
            mismatches = sorted(
                key
                for key in page_record_keys
                if type(record[key]) is not type(actual[key])
                or record[key] != actual[key]
            )
            page_failures.append(f"{label}:mismatch={mismatches}")
    if len(recorded_page_paths) != len(set(recorded_page_paths)):
        page_failures.append("duplicate-recorded-path")
    if len(resolved_page_paths) != len(set(resolved_page_paths)):
        page_failures.append("duplicate-resolved-path")
    expected_page_paths = {
        (audit_root / relative_path).resolve()
        for _, _, relative_path in expected_page_specs
    }
    actual_page_paths = {
        path.resolve() for path in audit_root.glob("pages/*/page-*.jpg")
    }
    if actual_page_paths != expected_page_paths:
        page_failures.append(
            f"filesystem-path-set={len(actual_page_paths)}/{len(expected_page_paths)}"
        )

    source_pdfs = audit.get("source_pdfs", {})
    source_failures: List[str] = []
    actual_sources: Mapping[str, Mapping[str, object]] = {}
    calculated_render_source: Optional[str] = None
    if not parameters_ok:
        source_failures.append(
            f"parameters={audit.get('dpi')}dpi/{audit.get('columns')}x{audit.get('rows')}"
        )
    if not isinstance(source_pdfs, Mapping) or set(source_pdfs) != set(documents):
        source_failures.append("source-pdf-keys")
    else:
        try:
            calculated_render_source, actual_sources = render_source_identity(
                documents,
                int(audit["dpi"]),
                int(audit["columns"]),
                int(audit["rows"]),
            )
        except Exception as exc:
            source_failures.append(f"source-pdfs-{type(exc).__name__}")
        else:
            if source_pdfs != actual_sources:
                source_failures.append("source-pdf-records")
            if audit.get("render_source_fingerprint") != calculated_render_source:
                source_failures.append("render-source-fingerprint")

    categories = ("volumes", "core", "index", "atlas")
    category_page_counts = {category: 0 for category in categories}
    for metadata in documents.values():
        kind = str(metadata.get("kind"))
        category = "volumes" if kind == "volume" else kind
        if category in category_page_counts:
            category_page_counts[category] += int(metadata["expected_pages"])
    expected_contact_counts = {
        category: (count + GRID_COLUMNS * GRID_ROWS - 1)
        // (GRID_COLUMNS * GRID_ROWS)
        for category, count in category_page_counts.items()
    }
    fixed_contact_counts = {"volumes": 18, "core": 19, "index": 1, "atlas": 19}
    contact_record_keys = frozenset(
        ("category", "sheet", "image", "sha256", "width", "height", "page_count")
    )
    contacts = audit.get("contact_sheets")
    contact_failures: List[str] = []
    recomputed_contacts: dict[str, List[Mapping[str, object]]] = {
        category: [] for category in categories
    }
    recorded_contact_paths: List[str] = []
    resolved_contact_paths: List[Path] = []
    if (
        not isinstance(contacts, Mapping)
        or set(contacts) != set(categories)
        or expected_contact_counts != fixed_contact_counts
    ):
        contact_failures.append(
            f"categories-or-count-contract={expected_contact_counts}"
        )
        contacts = {}
    for category in categories:
        records = contacts.get(category, []) if isinstance(contacts, Mapping) else []
        if not isinstance(records, list):
            contact_failures.append(f"{category}:records-not-list")
            records = []
        expected_count = expected_contact_counts[category]
        if len(records) != expected_count:
            contact_failures.append(
                f"{category}:record-count={len(records)}/{expected_count}"
            )
        for sheet_number in range(1, expected_count + 1):
            label = f"{category}:{sheet_number:03d}"
            if sheet_number > len(records):
                contact_failures.append(f"{label}:missing-record")
                continue
            record = records[sheet_number - 1]
            if not isinstance(record, dict) or set(record) != contact_record_keys:
                contact_failures.append(f"{label}:record-fields")
                continue
            expected_path = f"contact_sheets/{category}-{sheet_number:03d}.jpg"
            recorded_contact_paths.append(str(record.get("image")))
            if (
                record.get("category") != category
                or type(record.get("sheet")) is not int
                or record.get("sheet") != sheet_number
                or record.get("image") != expected_path
            ):
                contact_failures.append(f"{label}:identity-or-path")
                continue
            image_path = audit_root / expected_path
            if not image_path.is_file() or image_path.is_symlink():
                contact_failures.append(f"{label}:missing-or-symlink-image")
                continue
            resolved_contact_paths.append(image_path.resolve())
            try:
                with Image.open(image_path) as source:
                    source.load()
                    width, height = source.size
            except Exception as exc:
                contact_failures.append(f"{label}:image-{type(exc).__name__}")
                continue
            first_page = (sheet_number - 1) * GRID_COLUMNS * GRID_ROWS
            page_count = min(
                GRID_COLUMNS * GRID_ROWS,
                max(0, category_page_counts[category] - first_page),
            )
            actual = {
                "category": category,
                "sheet": sheet_number,
                "image": expected_path,
                "sha256": _sha256(image_path),
                "width": width,
                "height": height,
                "page_count": page_count,
            }
            recomputed_contacts[category].append(actual)
            if (
                (width, height) != (CONTACT_WIDTH, CONTACT_HEIGHT)
                or record != actual
                or any(
                    type(record[key]) is not type(actual[key])
                    for key in contact_record_keys
                )
            ):
                contact_failures.append(f"{label}:hash-dimensions-or-metadata")
    if len(recorded_contact_paths) != len(set(recorded_contact_paths)):
        contact_failures.append("duplicate-recorded-path")
    if len(resolved_contact_paths) != len(set(resolved_contact_paths)):
        contact_failures.append("duplicate-resolved-path")
    expected_contact_paths = {
        (audit_root / f"contact_sheets/{category}-{number:03d}.jpg").resolve()
        for category, count in expected_contact_counts.items()
        for number in range(1, count + 1)
    }
    actual_contact_paths = {
        path.resolve() for path in audit_root.glob("contact_sheets/*.jpg")
    }
    if actual_contact_paths != expected_contact_paths:
        contact_failures.append(
            f"filesystem-path-set={len(actual_contact_paths)}/{len(expected_contact_paths)}"
        )

    calculated_fingerprint: Optional[str] = None
    fingerprint_ok = False
    if (
        not page_failures
        and not contact_failures
        and not source_failures
        and len(recomputed_pages) == expected_pages
    ):
        calculated_fingerprint = calculate_audit_fingerprint(
            int(audit["dpi"]),
            int(audit["columns"]),
            int(audit["rows"]),
            actual_sources,
            recomputed_pages,
            recomputed_contacts,
        )
        fingerprint_ok = audit.get("audit_fingerprint") == calculated_fingerprint
        if not fingerprint_ok:
            page_failures.append("audit-fingerprint")

    _check(
        checks,
        "visual.pages",
        not page_failures
        and not source_failures
        and fingerprint_ok
        and audit.get("documents") == 43
        and audit.get("pages_expected") == expected_pages
        and audit.get("pages_rendered") == expected_pages
        and len(page_records) == expected_pages
        and parameters_ok,
        f"documents={audit.get('documents')}/43 pages={len(recomputed_pages)}/{expected_pages} "
        f"failures={(page_failures + source_failures)[:12]} "
        f"fingerprint={'ok' if fingerprint_ok else 'stale'}",
    )

    automatic = audit.get("automatic_checks", {})
    expected_automatic = {
        "blank_suspects": [
            f"{item['stem']}:p{int(item['page']):04d}"
            for item in recomputed_pages
            if item["blank_suspect"]
        ],
        "edge_suspects": [
            f"{item['stem']}:p{int(item['page']):04d}"
            for item in recomputed_pages
            if item["edge_suspect"]
        ],
        "aspect_suspects": [
            f"{item['stem']}:p{int(item['page']):04d}"
            for item in recomputed_pages
            if item["aspect_suspect"]
        ],
    }
    automatic_ok = (
        isinstance(automatic, Mapping)
        and automatic == expected_automatic
        and all(not values for values in expected_automatic.values())
        and len(recomputed_pages) == expected_pages
    )
    _check(
        checks,
        "visual.automatic",
        automatic_ok,
        f"recorded={automatic} recomputed={expected_automatic}",
    )

    actual_contact_counts = {
        category: len(recomputed_contacts[category]) for category in categories
    }
    _check(
        checks,
        "visual.contacts",
        not contact_failures
        and actual_contact_counts == fixed_contact_counts
        and audit.get("contact_sheets_total") == 57
        and sum(actual_contact_counts.values()) == 57,
        f"actual={actual_contact_counts} total={sum(actual_contact_counts.values())}/57 "
        f"failures={contact_failures[:12]}",
    )

    manual = audit.get("manual_review", {})
    manual_path = audit_root / "manual_review.json"
    try:
        manual_source = _load_json(manual_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        manual_source = {}
        manual_source_error: Optional[str] = type(exc).__name__
    else:
        manual_source_error = None
    manual_ok = (
        isinstance(manual, Mapping)
        and manual == manual_source
        and manual.get("schema")
        == "lattice-qcd-course-manual-visual-review-v1"
        and manual.get("status") == "passed"
        and calculated_fingerprint is not None
        and manual.get("audit_fingerprint") == calculated_fingerprint
        and manual.get("pages_checked") == expected_pages
        and manual.get("contact_sheets_checked") == 57
        and manual.get("occlusion_pairs") == 0
        and manual.get("clipped_objects") == 0
        and manual.get("outside_safe_area") == 0
    )
    _check(
        checks,
        "visual.manual",
        manual_ok,
        f"status={manual.get('status') if isinstance(manual, Mapping) else None} "
        f"pages={manual.get('pages_checked') if isinstance(manual, Mapping) else None}/{expected_pages} "
        f"contacts={manual.get('contact_sheets_checked') if isinstance(manual, Mapping) else None}/57 "
        f"source_error={manual_source_error}",
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="总开关：要求 43 PDF、v2 全页视觉审计、两层现场 SymPy 与论文身份",
    )
    parser.add_argument("--run-sympy", action="store_true", help="重新执行 175+26 条 SymPy 检查")
    parser.add_argument("--check-paper-identities", action="store_true", help="用 Ghostscript 核对 50 篇首页身份")
    parser.add_argument(
        "--require-pdfs",
        action="store_true",
        help="要求 43 份 PDF、日志、页数和编译来源证明全部通过",
    )
    parser.add_argument(
        "--require-visual-audit",
        action="store_true",
        help="即使未要求全部 PDF，也要求全页渲染与人工视觉验收记录",
    )
    parser.add_argument("--json", type=Path, help="可选：写出机器可读验收摘要")
    args = parser.parse_args(argv)
    if args.strict:
        args.run_sympy = True
        args.check_paper_identities = True
        args.require_pdfs = True
        args.require_visual_audit = True

    checks: List[Check] = []
    stages: Sequence[tuple[str, Callable[[], None]]] = (
        ("structure", lambda: verify_structure(checks)),
        ("sympy", lambda: verify_symbolic_evidence(checks, args.run_sympy)),
        ("papers", lambda: verify_papers(checks, args.check_paper_identities)),
        ("generated", lambda: verify_generated(checks)),
        ("compiled", lambda: verify_compiled(checks, args.require_pdfs)),
        (
            "visual",
            lambda: verify_visual_audit(
                checks,
                args.require_pdfs or args.require_visual_audit,
            ),
        ),
    )
    for stage_name, stage in stages:
        try:
            stage()
        except Exception as exc:
            checks.append(
                Check(
                    f"{stage_name}.exception",
                    False,
                    f"{type(exc).__name__}: {exc}",
                )
            )

    for item in checks:
        print(f"[{'PASS' if item.passed else 'FAIL'}] {item.name}: {item.detail}")
    failed = [item for item in checks if not item.passed]
    payload = {
        "schema": "lattice-qcd-course-verification-v1",
        "passed": len(checks) - len(failed),
        "total": len(checks),
        "status": "passed" if not failed else "failed",
        "checks": [asdict(item) for item in checks],
    }
    if args.json:
        _write_json_atomic(args.json, payload)
    print(f"course verification: {payload['passed']}/{payload['total']} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

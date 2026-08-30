"""全页渲染课程 PDF，生成联系表并执行可重复的页面边界审计。"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageStat

from build_course import COURSE_DIR, PDF_DIR, _write_json_atomic, load_manifest


AUDIT_SCHEMA = "lattice-qcd-course-render-audit-v2"
GRID_COLUMNS = 8
GRID_ROWS = 8
MIN_DPI = 96
CONTACT_CELL_WIDTH = 240
CONTACT_IMAGE_HEIGHT = 135
CONTACT_LABEL_HEIGHT = 18
CONTACT_WIDTH = GRID_COLUMNS * CONTACT_CELL_WIDTH
CONTACT_HEIGHT = GRID_ROWS * (CONTACT_IMAGE_HEIGHT + CONTACT_LABEL_HEIGHT)
SLIDE_WIDTH_MM = 160.0
SLIDE_HEIGHT_MM = 90.0


def expected_page_dimensions(dpi: int) -> Tuple[int, int]:
    """Expected raster size for Beamer's fixed 160 mm x 90 mm canvas."""

    return (
        round(SLIDE_WIDTH_MM * dpi / 25.4),
        round(SLIDE_HEIGHT_MM * dpi / 25.4),
    )


@dataclass(frozen=True)
class PageAudit:
    stem: str
    page: int
    image: str
    sha256: str
    width: int
    height: int
    aspect_ratio: float
    nonwhite_fraction: float
    outer_ink_fraction: float
    grayscale_stddev: float
    blank_suspect: bool
    edge_suspect: bool
    aspect_suspect: bool


@dataclass(frozen=True)
class ContactSheetAudit:
    category: str
    sheet: int
    image: str
    sha256: str
    width: int
    height: int
    page_count: int


def _render_document(
    stem: str,
    metadata: Mapping[str, object],
    render_root: Path,
    dpi: int,
) -> Tuple[str, Tuple[Path, ...]]:
    if not shutil.which("gs"):
        raise RuntimeError("缺少 Ghostscript，无法渲染 PDF")
    pdf = PDF_DIR / f"{stem}.pdf"
    if not pdf.is_file():
        raise FileNotFoundError(pdf)
    output_dir = render_root / stem
    output_dir.mkdir(parents=True, exist_ok=True)
    expected = int(metadata["expected_pages"])
    expected_paths = tuple(
        output_dir / f"page-{page:04d}.jpg"
        for page in range(1, expected + 1)
    )
    existing = tuple(sorted(output_dir.glob("page-*.jpg")))
    if existing and existing != expected_paths:
        raise RuntimeError(
            f"{stem}: 逐页图路径不闭合；必须精确为 page-0001.jpg--"
            f"page-{expected:04d}.jpg"
        )
    if not existing:
        command = [
            "gs",
            "-q",
            "-dNOSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            f"-r{dpi}",
            "-dJPEGQ=88",
            "-dTextAlphaBits=4",
            "-dGraphicsAlphaBits=4",
            f"-sOutputFile={output_dir / 'page-%04d.jpg'}",
            str(pdf),
        ]
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"{stem}: Ghostscript 渲染失败 exit={result.returncode}: "
                f"{result.stdout}{result.stderr}"
            )
        existing = tuple(sorted(output_dir.glob("page-*.jpg")))
    if existing != expected_paths:
        raise RuntimeError(
            f"{stem}: rendered={len(existing)}, expected={expected}"
        )
    return stem, existing


def _ink_fraction(image: Image.Image, threshold: int = 245) -> float:
    histogram = image.convert("L").histogram()
    total = image.width * image.height
    return sum(histogram[:threshold]) / total if total else 0.0


def _relative_audit_path(path: Path, audit_root: Path) -> str:
    try:
        return path.resolve().relative_to(audit_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"审计图像路径越界：{path}") from exc


def audit_page_image(
    stem: str,
    page: int,
    path: Path,
    audit_root: Path,
) -> PageAudit:
    with Image.open(path) as source:
        image = source.convert("RGB")
    width, height = image.size
    grayscale = image.convert("L")
    nonwhite = _ink_fraction(image, threshold=248)
    border = max(2, round(min(width, height) * 0.006))
    strips = (
        image.crop((0, 0, width, border)),
        image.crop((0, height - border, width, height)),
        image.crop((0, border, border, height - border)),
        image.crop((width - border, border, width, height - border)),
    )
    edge_pixels = sum(strip.width * strip.height for strip in strips)
    edge_ink = sum(
        _ink_fraction(strip, threshold=238) * strip.width * strip.height
        for strip in strips
    ) / edge_pixels
    stddev = float(ImageStat.Stat(grayscale).stddev[0])
    aspect = width / height
    return PageAudit(
        stem=stem,
        page=page,
        image=_relative_audit_path(path, audit_root),
        sha256=_sha256(path),
        width=width,
        height=height,
        aspect_ratio=aspect,
        nonwhite_fraction=nonwhite,
        outer_ink_fraction=edge_ink,
        grayscale_stddev=stddev,
        blank_suspect=nonwhite < 0.0015 or stddev < 2.0,
        edge_suspect=edge_ink > 0.015,
        aspect_suspect=abs(aspect - 16 / 9) > 0.025,
    )


def _audit_page(stem: str, page: int, path: Path) -> PageAudit:
    """Backward-compatible helper for the default audit directory."""

    return audit_page_image(stem, page, path, COURSE_DIR / "visual_audit")


def _category(stem: str, metadata: Mapping[str, object]) -> str:
    kind = str(metadata["kind"])
    return "volumes" if kind == "volume" else kind


def _short_label(stem: str, page: int) -> str:
    if stem.startswith("volume_"):
        prefix = "V" + stem.split("_", 2)[1]
    elif stem.startswith("paper_atlas_"):
        prefix = "Atlas-" + stem.rsplit("_", 1)[1]
    elif stem == "core_complete":
        prefix = "Core"
    else:
        prefix = "Index"
    return f"{prefix} p{page:04d}"


def _contact_sheets(
    category: str,
    pages: Sequence[Tuple[str, int, Path]],
    contact_root: Path,
    columns: int,
    rows: int,
    audit_root: Optional[Path] = None,
) -> Tuple[ContactSheetAudit, ...]:
    contact_root.mkdir(parents=True, exist_ok=True)
    root = audit_root if audit_root is not None else contact_root.parent
    cell_width = CONTACT_CELL_WIDTH
    image_height = CONTACT_IMAGE_HEIGHT
    label_height = CONTACT_LABEL_HEIGHT
    cell_height = image_height + label_height
    per_sheet = columns * rows
    expected_count = (len(pages) + per_sheet - 1) // per_sheet
    expected_outputs = tuple(
        contact_root / f"{category}-{sheet_number:03d}.jpg"
        for sheet_number in range(1, expected_count + 1)
    )
    unexpected = sorted(
        set(contact_root.glob(f"{category}-*.jpg")) - set(expected_outputs)
    )
    if unexpected:
        raise RuntimeError(
            f"{category}: 存在非预期联系表路径："
            f"{[path.name for path in unexpected]}"
        )
    outputs: List[ContactSheetAudit] = []
    for sheet_number, start in enumerate(range(0, len(pages), per_sheet), start=1):
        subset = pages[start : start + per_sheet]
        sheet = Image.new(
            "RGB", (columns * cell_width, rows * cell_height), "white"
        )
        draw = ImageDraw.Draw(sheet)
        for offset, (stem, page, path) in enumerate(subset):
            row, column = divmod(offset, columns)
            x0, y0 = column * cell_width, row * cell_height
            with Image.open(path) as source:
                thumb = source.convert("RGB")
            thumb.thumbnail((cell_width - 4, image_height - 4))
            x = x0 + (cell_width - thumb.width) // 2
            y = y0 + (image_height - thumb.height) // 2
            sheet.paste(thumb, (x, y))
            draw.rectangle(
                (x0, y0, x0 + cell_width - 1, y0 + image_height - 1),
                outline=(185, 193, 201),
                width=1,
            )
            draw.text((x0 + 4, y0 + image_height + 2), _short_label(stem, page), fill=(35, 45, 55))
        output = expected_outputs[sheet_number - 1]
        temporary: Optional[Path] = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=contact_root,
                prefix=f".{output.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temporary = Path(handle.name)
            sheet.save(
                temporary,
                format="JPEG",
                quality=90,
                optimize=True,
            )
            os.replace(temporary, output)
            temporary = None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        with Image.open(output) as saved:
            width, height = saved.size
        expected_size = (columns * cell_width, rows * cell_height)
        if (width, height) != expected_size:
            raise RuntimeError(
                f"{output.name}: 联系表尺寸错误 actual={(width, height)} "
                f"expected={expected_size}"
            )
        outputs.append(
            ContactSheetAudit(
                category=category,
                sheet=sheet_number,
                image=_relative_audit_path(output, root),
                sha256=_sha256(output),
                width=width,
                height=height,
                page_count=len(subset),
            )
        )
    return tuple(outputs)


def _manual_review(
    output: Path,
    expected_pages: int,
    expected_contacts: int,
    audit_fingerprint: str,
) -> Mapping[str, object]:
    """只接受与本次渲染页数、联系表数完全匹配的人工审阅记录。"""

    pending: Dict[str, object] = {
        "status": "pending",
        "pages_checked": 0,
        "contact_sheets_checked": 0,
        "occlusion_pairs": None,
        "clipped_objects": None,
        "outside_safe_area": None,
    }
    review_path = output / "manual_review.json"
    if not review_path.is_file():
        pending["reason"] = "缺少 visual_audit/manual_review.json"
        return pending
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        pending["reason"] = f"人工审阅记录不可读：{exc}"
        return pending
    required = {
        "schema": "lattice-qcd-course-manual-visual-review-v1",
        "status": "passed",
        "audit_fingerprint": audit_fingerprint,
        "pages_checked": expected_pages,
        "contact_sheets_checked": expected_contacts,
        "occlusion_pairs": 0,
        "clipped_objects": 0,
        "outside_safe_area": 0,
    }
    mismatches = {
        key: {"actual": review.get(key), "expected": value}
        for key, value in required.items()
        if review.get(key) != value
    }
    if mismatches:
        pending["reason"] = f"人工审阅记录与当前渲染不匹配：{mismatches}"
        return pending
    return review


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fingerprint_json(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def render_source_identity(
    documents: Mapping[str, Mapping[str, object]],
    dpi: int,
    columns: int,
    rows: int,
) -> Tuple[str, Mapping[str, Mapping[str, object]]]:
    sources: Dict[str, Mapping[str, object]] = {}
    for stem, metadata in documents.items():
        pdf = PDF_DIR / f"{stem}.pdf"
        if not pdf.is_file():
            raise FileNotFoundError(pdf)
        sources[stem] = {
            "pdf": pdf.relative_to(COURSE_DIR).as_posix(),
            "sha256": _sha256(pdf),
            "expected_pages": int(metadata["expected_pages"]),
        }
    identity = {
        "schema": "lattice-qcd-course-render-source-v1",
        "dpi": dpi,
        "columns": columns,
        "rows": rows,
        "source_pdfs": sources,
    }
    return _fingerprint_json(identity), sources


def calculate_audit_fingerprint(
    dpi: int,
    columns: int,
    rows: int,
    source_pdfs: Mapping[str, Mapping[str, object]],
    pages: Sequence[Mapping[str, object]],
    contact_sheets: Mapping[str, Sequence[Mapping[str, object]]],
) -> str:
    """Bind every expected page/contact path to its bytes and dimensions."""

    page_identity = [
        {
            key: record[key]
            for key in ("stem", "page", "image", "sha256", "width", "height")
        }
        for record in pages
    ]
    contact_identity = {
        category: [
            {
                key: record[key]
                for key in (
                    "category",
                    "sheet",
                    "image",
                    "sha256",
                    "width",
                    "height",
                    "page_count",
                )
            }
            for record in records
        ]
        for category, records in contact_sheets.items()
    }
    return _fingerprint_json(
        {
            "schema": "lattice-qcd-course-render-evidence-v2",
            "dpi": dpi,
            "columns": columns,
            "rows": rows,
            "source_pdfs": source_pdfs,
            "pages": page_identity,
            "contact_sheets": contact_identity,
        }
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=COURSE_DIR / "visual_audit")
    parser.add_argument("--dpi", type=int, default=MIN_DPI)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--columns", type=int, default=GRID_COLUMNS)
    parser.add_argument("--rows", type=int, default=GRID_ROWS)
    parser.add_argument(
        "--adopt-existing",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)
    if args.adopt_existing:
        raise ValueError("--adopt-existing 无法证明图像来源，已禁用；请使用新的 --output")
    if args.dpi < MIN_DPI:
        raise ValueError(f"视觉审阅渲染 DPI 不得低于 {MIN_DPI}")
    if args.columns != GRID_COLUMNS or args.rows != GRID_ROWS:
        raise ValueError(
            f"联系表必须固定为 {GRID_COLUMNS}x{GRID_ROWS}，"
            f"actual={args.columns}x{args.rows}"
        )

    manifest = load_manifest()
    documents = manifest["documents"]
    if not isinstance(documents, Mapping):
        raise TypeError("manifest.documents 必须是映射")
    typed_documents = {
        str(stem): metadata
        for stem, metadata in documents.items()
        if isinstance(metadata, Mapping)
    }
    if len(typed_documents) != len(documents):
        raise TypeError("manifest.documents 的每项必须是映射")
    output = args.output.resolve()
    render_root = output / "pages"
    contact_root = output / "contact_sheets"
    render_source_fingerprint, source_pdfs = render_source_identity(
        typed_documents,
        args.dpi,
        args.columns,
        args.rows,
    )
    previous_path = output / "render_audit.json"
    previous_source_fingerprint: Optional[str] = None
    if previous_path.is_file():
        try:
            previous = json.loads(previous_path.read_text(encoding="utf-8"))
            previous_source_fingerprint = previous.get(
                "render_source_fingerprint"
            )
        except (OSError, json.JSONDecodeError):
            previous_source_fingerprint = None
    existing_pages = any(render_root.glob("*/page-*.jpg"))
    if existing_pages and previous_source_fingerprint != render_source_fingerprint:
        raise RuntimeError(
            "现有逐页图与当前 PDF/渲染参数的指纹不一致；"
            "请改用新的 --output，不能采纳来源未经机器绑定的旧图"
        )
    render_root.mkdir(parents=True, exist_ok=True)
    contact_root.mkdir(parents=True, exist_ok=True)

    rendered: Dict[str, Tuple[Path, ...]] = {}
    failures: List[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {
            pool.submit(_render_document, stem, metadata, render_root, args.dpi): stem
            for stem, metadata in typed_documents.items()
        }
        for future in concurrent.futures.as_completed(futures):
            stem = futures[future]
            try:
                completed, paths = future.result()
            except Exception as exc:
                failures.append(f"{stem}: {exc}")
            else:
                rendered[completed] = paths
                print(f"rendered {completed}: {len(paths)} pages")
    if failures:
        raise RuntimeError("渲染失败：\n" + "\n".join(sorted(failures)))

    audits: List[PageAudit] = []
    categorized: Dict[str, List[Tuple[str, int, Path]]] = {
        "volumes": [],
        "core": [],
        "index": [],
        "atlas": [],
    }
    for stem, metadata in typed_documents.items():
        category = _category(stem, metadata)
        for page, path in enumerate(rendered[stem], start=1):
            audits.append(audit_page_image(stem, page, path, output))
            categorized[category].append((stem, page, path))
    expected_width, expected_height = expected_page_dimensions(args.dpi)
    wrong_sizes = [
        f"{item.stem}:p{item.page:04d}={item.width}x{item.height}"
        for item in audits
        if abs(item.width - expected_width) > 1
        or abs(item.height - expected_height) > 1
    ]
    if wrong_sizes:
        raise RuntimeError(
            f"逐页图尺寸与 {args.dpi} DPI 的 16:9 画布不符："
            f"expected≈{expected_width}x{expected_height}, "
            f"failures={wrong_sizes[:20]}"
        )

    contacts: Dict[str, List[Mapping[str, object]]] = {}
    for category, pages in categorized.items():
        contact_records = _contact_sheets(
            category,
            pages,
            contact_root,
            args.columns,
            args.rows,
            output,
        )
        contacts[category] = [asdict(item) for item in contact_records]

    blank = [item for item in audits if item.blank_suspect]
    edge = [item for item in audits if item.edge_suspect]
    aspect = [item for item in audits if item.aspect_suspect]
    expected_pages = sum(
        int(meta["expected_pages"]) for meta in typed_documents.values()
    )
    contact_count = sum(map(len, contacts.values()))
    expected_contacts = {"volumes": 18, "core": 19, "index": 1, "atlas": 19}
    actual_contacts = {
        category: len(contacts.get(category, ()))
        for category in expected_contacts
    }
    if actual_contacts != expected_contacts or contact_count != 57:
        raise RuntimeError(
            f"联系表数量不闭合：actual={actual_contacts}, total={contact_count}"
        )
    page_records = [asdict(item) for item in audits]
    audit_fingerprint = calculate_audit_fingerprint(
        args.dpi,
        args.columns,
        args.rows,
        source_pdfs,
        page_records,
        contacts,
    )
    manual_review = _manual_review(
        output,
        expected_pages,
        contact_count,
        audit_fingerprint,
    )
    payload = {
        "schema": AUDIT_SCHEMA,
        "dpi": args.dpi,
        "columns": args.columns,
        "rows": args.rows,
        "render_source_fingerprint": render_source_fingerprint,
        "audit_fingerprint": audit_fingerprint,
        "source_pdfs": source_pdfs,
        "documents": len(typed_documents),
        "pages_expected": expected_pages,
        "pages_rendered": len(audits),
        "contact_sheets_total": contact_count,
        "contact_sheets": contacts,
        "automatic_checks": {
            "blank_suspects": [f"{item.stem}:p{item.page:04d}" for item in blank],
            "edge_suspects": [f"{item.stem}:p{item.page:04d}" for item in edge],
            "aspect_suspects": [f"{item.stem}:p{item.page:04d}" for item in aspect],
        },
        "manual_review": manual_review,
        "pages": page_records,
    }
    _write_json_atomic(output / "render_audit.json", payload)
    print(
        f"render audit: documents={len(typed_documents)}, "
        f"pages={len(audits)}/{expected_pages}, contacts={contact_count}, "
        f"blank={len(blank)}, edge={len(edge)}, aspect={len(aspect)}"
    )
    complete = all(
        (
            len(audits) == expected_pages,
            not blank,
            not edge,
            not aspect,
            manual_review.get("status") == "passed",
        )
    )
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Extract figures from 'An Introduction to Quantum Field Theory.pdf' (Peskin & Schroeder).

Caption->crop extraction using PyMuPDF's line-level text structure:

1. For each page, get lines (with bbox + concatenated text) via
   page.get_text("dict").
2. A caption line starts with "Figure X.Y." (the number may be separated
   by stray spaces, e.g. "Figure 2 .1 ."), matched with a tolerant regex.
3. Walk UP from the caption line, skipping figure-internal label rows
   (short fragmentary lines), until we hit a full-sentence row (running
   head, previous paragraph, or previous caption).  That boundary is the
   top of the figure.  If none is found, use the running-head / page-top
   boundary.
4. Render the chosen region at 300 dpi with PyMuPDF, name it figX.Y.png.
   Cross-reference lines ("Figure 17.5 has been adapted ...") produce
   empty regions and are dropped via an ink-coverage threshold.
5. Captions sitting near the top of a page often belong to a figure that
   spans from the previous page: also render the bottom band of the
   previous page and keep the richer crop.
"""
import os, re
import fitz
from PIL import Image

PDF = "/root/lattice-pdf/books/An Introduction to Quantum Field Theory.pdf"
OUT = "/root/lattice-pdf/books/An_Introduction_to_Quantum_Field_Theory_latex/images"
DPI = 300
ROW_Y_TOL = 5.0       # pt tolerance for grouping lines into visual rows
PREV_PAGE_BAND = 0.52
PREV_PAGE_TOP = 0.40

# "Figure 1.1. ..." or "Figure 2 .1 . ..." (stray spaces in this scan)
CAPTION_RE = re.compile(r"^Figure\s+(\d+)\s*\.\s*(\d+)\s*\.?\s")


def page_lines(page):
    """Return list of (x0,y0,x1,y1,text) for text lines in visual order."""
    d = page.get_text("dict")
    lines = []
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            text = "".join(s["text"] for s in l["spans"]).strip()
            if text:
                lines.append((l["bbox"][0], l["bbox"][1],
                              l["bbox"][2], l["bbox"][3], text))
    return lines


def rows_of(lines, tol=ROW_Y_TOL):
    """Cluster lines into visual rows (running-order preserved)."""
    sl = sorted(lines, key=lambda l: (l[1], l[0]))
    rows = []
    for l in sl:
        if rows and abs(l[1] - rows[-1][0][1]) <= tol:
            rows[-1].append(l)
        else:
            rows.append([l])
    return rows


def is_caption_row(row):
    """True if a visual row starts with a 'Figure X.Y.' caption."""
    first = sorted(row, key=lambda l: l[0])[0]
    return bool(CAPTION_RE.match(first[4]))


def caption_key(row):
    first = sorted(row, key=lambda l: l[0])[0]
    m = CAPTION_RE.match(first[4])
    if m:
        return f"fig{m.group(1)}.{m.group(2)}"
    return None


def is_sentence_row(row, left_margin, right_margin):
    """Full-width prose row (paragraph or running head)."""
    ls = sorted(row, key=lambda l: l[0])
    if len(ls) < 3:
        return False
    return ls[0][0] <= left_margin + 8.0 and ls[-1][2] >= right_margin - 30.0


def figure_top(rows, cap_index, left_margin, right_margin, page_top_boundary=52.0):
    """Walk up from caption row to find the top boundary of the figure."""
    for r in rows[cap_index - 1::-1]:
        if is_sentence_row(r, left_margin, right_margin):
            return max(l[3] for l in r)
    return page_top_boundary  # below running head / page top


def page_margins(lines):
    if not lines:
        return 53.0, 407.0  # default left/right margin for P&S
    lm = min(l[0] for l in lines)
    rm = max(l[2] for l in lines)
    return lm, rm


def render_crop(doc, page_idx, x0, y0, x1, y1, path):
    """Render a region of a page at DPI into path."""
    if x1 - x0 <= 2 or y1 - y0 <= 2:
        return None
    page = doc.load_page(page_idx)
    clip = fitz.Rect(x0, y0, x1, y1)
    mat = fitz.Matrix(DPI / 72.0, DPI / 72.0)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    pix.save(path)
    return path if os.path.exists(path) else None


def ink_fraction(path):
    try:
        im = Image.open(path).convert("L")
        dark = sum(1 for px in im.getdata() if px < 200)
        return dark / (im.size[0] * im.size[1])
    except Exception:
        return -1.0


def main():
    os.makedirs(OUT, exist_ok=True)
    doc = fitz.open(PDF)
    n_pages = doc.page_count
    candidates = {}   # figkey -> list of (page, path, ink)
    tmp = 0

    for p in range(0, n_pages):
        page = doc.load_page(p)
        lines = page_lines(page)
        if not lines:
            continue
        lm, rm = page_margins(lines)
        rows = rows_of(lines)
        for i, row in enumerate(rows):
            if not is_caption_row(row):
                continue
            key = caption_key(row)
            cap_top = min(l[1] for l in row)
            top = figure_top(rows, i, lm, rm)
            x0, y0 = lm - 3.0, top
            x1, y1 = rm + 3.0, cap_top - 3.0
            cands = []
            tmp += 1
            p1 = os.path.join(OUT, f"_tmp_{tmp:04d}.png")
            if render_crop(doc, p, x0, y0, x1, y1, p1):
                cands.append((p, p1, ink_fraction(p1)))
            # split-across-page: caption near top -> also try previous page bottom
            if cap_top < 110.0 and p > 18:
                prev = p - 1
                p2 = os.path.join(OUT, f"_tmp_{tmp:04d}b.png")
                y2a = PREV_PAGE_TOP * page.rect.height
                y2b = (PREV_PAGE_TOP + PREV_PAGE_BAND) * page.rect.height
                if render_crop(doc, prev, x0, y2a, x1, y2b, p2):
                    cands.append((prev, p2, ink_fraction(p2)))
            if not cands:
                continue
            best = max(cands, key=lambda c: c[2])
            candidates.setdefault(key, []).append(best)
            for cp in cands:
                if cp[1] != best[1] and os.path.exists(cp[1]):
                    os.remove(cp[1])

    best_by_key = {}
    for key, lst in candidates.items():
        page, path, ink = max(lst, key=lambda c: c[2])
        best_by_key[key] = (page, path, ink)

    print(f"{'key':<9} {'page':>5} {'ink':>7}  status")
    n = 0
    for key in sorted(best_by_key):
        page, path, ink = best_by_key[key]
        final = os.path.join(OUT, key + ".png")
        if os.path.exists(final):
            os.remove(final)
        os.rename(path, final)
        if ink < 0.0025:
            print(f"{key:<9} {page:>5} {ink*100:6.2f}%  DROPPED (cross-ref/empty)")
            continue
        n += 1
        print(f"{key:<9} {page:>5} {ink*100:6.2f}%  kept")
    print(f"\nKEPT figures: {n} / {len(best_by_key)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract figures from 'Quantum Chromodynamics on the Lattice.pdf' into images/.

Robust caption->crop extraction:

1. For each content page, get word bounding boxes via `pdftotext -bbox`.
2. Find caption start-lines "Fig. X.Y." at the left text margin.
3. Walk UP from the caption, skipping figure-internal label rows (short
   fragmentary lines, axis tick labels) until we hit a full-sentence row
   (running head, previous paragraph, or previous caption).  That boundary is
   the top of the figure.  If no sentence row is found (figure at top of page),
   the running-head / page-top boundary is used.
4. For captions sitting near the top of a page (figure split across pages),
   also render the bottom band of the previous page and keep the richer crop.
5. Render the chosen region with pdftoppm (300 dpi), name it figX.Y.png.
   Cross-reference lines ("Fig. 6.5 ..." inside a paragraph) produce empty
   regions and are dropped via an ink-coverage threshold.
"""
import subprocess, os, re

PDF = "/root/lattice-pdf/books/Quantum Chromodynamics on the Lattice.pdf"
OUT = "/root/lattice-pdf/books/Quantum_Chromodynamics_on_the_Lattice_latex/images"
DPI = 300
SCALE = DPI / 72.0
PAGE_H = 666.142  # pt

WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',
    re.S)


def page_bbox(page):
    out = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page),
                          PDF, "-"], capture_output=True, text=True).stdout
    words = [(m.group(5), float(m.group(1)), float(m.group(2)),
              float(m.group(3)), float(m.group(4))) for m in WORD_RE.finditer(out)]
    return words


def rows_of(words, tol=6.0):
    """Cluster words into visual rows (list of rows, each a list of words)."""
    sw = sorted(words, key=lambda w: (w[2], w[1]))
    rows = []
    for w in sw:
        if rows and abs(w[2] - rows[-1][0][2]) <= tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return rows


def is_caption_row(row, left_margin):
    """True if row is a caption: 'Fig.' is the FIRST word of the row and the
    second word is a figure number with a trailing period (e.g. '2.3.').
    Centered captions are thus caught; inline cross-references like
    '... see Fig. 6.5 ...' (no trailing period, or not line-initial) are not."""
    ws = sorted(row, key=lambda w: w[1])
    if not ws:
        return False
    if not ws[0][0].startswith("Fig."):
        return False
    for w in ws[1:]:
        if w[2] >= ws[0][2] - 2 and w[2] <= ws[0][4] + 2:
            return bool(re.match(r"^\d+\.\d+\.$", w[0]))
    return False


def caption_key(row):
    ws = sorted(row, key=lambda w: w[1])
    for w in ws[1:]:
        if w[2] >= ws[0][2] - 2 and w[2] <= ws[0][4] + 2:
            m = re.match(r"^(\d+\.\d+)\.$", w[0])
            if m:
                return "fig" + m.group(1).replace(".", "")
            break
    return None


def is_sentence_row(row, left_margin, right_margin):
    ws = sorted(row, key=lambda w: w[1])
    if len(ws) < 3:
        return False
    return ws[0][1] <= left_margin + 8.0 and ws[-1][3] >= right_margin - 30.0


def figure_top(rows, cap_index, left_margin, right_margin):
    """Walk up from caption row to find the top boundary of the figure."""
    for r in rows[cap_index - 1::-1]:
        if is_sentence_row(r, left_margin, right_margin):
            return max(w[4] for w in r)
    return 45.0  # below running head / page top


def page_margins(words):
    lm = min(w[1] for w in words) if words else 53.0
    rm = max(w[3] for w in words) if words else 385.0
    return lm, rm


_tmp_counter = [0]
def render_crop(page, x, y, w, h):
    if w <= 2 or h <= 2:
        return None
    px, py = int(x * SCALE), int(y * SCALE)
    pw, ph = int(w * SCALE), int(h * SCALE)
    _tmp_counter[0] += 1
    tmp = os.path.join(OUT, f"_tmp_{_tmp_counter[0]:04d}")
    subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-f", str(page), "-l", str(page),
                    "-x", str(px), "-y", str(py), "-W", str(pw), "-H", str(ph),
                    "-singlefile", PDF, tmp], capture_output=True, text=True)
    p = tmp + ".png"
    return p if os.path.exists(p) else None


def ink_fraction(path):
    try:
        from PIL import Image
        im = Image.open(path).convert("L")
        dark = sum(1 for px in im.getdata() if px < 200)
        return dark / (im.size[0] * im.size[1])
    except Exception:
        return -1.0


def main():
    os.makedirs(OUT, exist_ok=True)
    candidates = {}   # figkey -> list of (page, path, ink, box)
    all_crops = []    # every rendered crop, deduped at the end
    for page in range(16, 346):
        words = page_bbox(page)
        if not words:
            continue
        lm, rm = page_margins(words)
        rows = rows_of(words)
        for i, row in enumerate(rows):
            if not is_caption_row(row, lm):
                continue
            key = caption_key(row)
            cap_top = min(w[2] for w in row)
            # --- main region: figure band above caption ---
            top = figure_top(rows, i, lm, rm)
            x, y = lm - 3.0, top
            w, h = (rm - x), (cap_top - 3.0 - top)
            cands = []
            p = render_crop(page, x, y, w, h)
            if p:
                cands.append((p, ink_fraction(p)))
            # --- split-across-page: caption near top -> also try previous page bottom ---
            if cap_top < 110 and page > 17:
                prev = page - 1
                p2 = render_crop(prev, lm - 3.0, 0.45 * PAGE_H,
                                 (rm - lm + 6), 0.52 * PAGE_H)
                if p2:
                    cands.append((p2, ink_fraction(p2)))
            if not cands:
                continue
            best = max(cands, key=lambda c: c[1])
            all_crops.append((key, page, best[0], best[1]))
            for cpath, _ in cands:
                if cpath != best[0]:
                    os.path.exists(cpath) and os.remove(cpath)

    # keep the best crop per figure key
    best_by_key = {}
    for key, page, path, ink in all_crops:
        if key not in best_by_key or ink > best_by_key[key][2]:
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

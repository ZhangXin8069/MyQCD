#!/usr/bin/env python3
"""Extract figures from 'INTRODUCTION TO LATTICE QCD.pdf' into images/.

Adapted from the Gattringer & Lang extractor (../Quantum_Chromodynamics_on_the_Lattice_latex/)
for this document's single-numbered caption style "Fig. N." (Rajan Gupta,
Introduction to Lattice QCD, arXiv:hep-lat/9807028, 150 pages, 35 figures).

Method:
1. Per content page, get word bounding boxes via `pdftotext -bbox`.
2. Find caption rows: a row whose first word is "Fig." at the left text
   margin, immediately followed by a bare integer token "N.".
   In-line cross references ("shown in Fig. 12.") do not start at the left
   margin, so they are never treated as captions.
3. Walk UP from the caption, skipping figure-internal label rows (short
   fragmentary rows, axis tick labels) until a full-sentence row is hit
   (running head, previous paragraph, or a previous caption).  That row's
   bottom edge is the top of the figure.  If none is found, use the
   running-head boundary.
4. Render the crop with pdftoppm at 300 dpi -> images/figN.png.
5. Drop crops below an ink threshold (cross-references / empty regions).
"""
import subprocess, os, re

PDF = "/root/lattice-pdf/books/INTRODUCTION TO LATTICE QCD.pdf"
OUT = "/root/lattice-pdf/books/INTRODUCTION_TO_LATTICE_QCD_latex/images"
DPI = 300
SCALE = DPI / 72.0

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
    """Cluster words into visual rows by baseline (yMax, i.e. y from page top)."""
    sw = sorted(words, key=lambda w: (w[2], w[1]))
    rows = []
    for w in sw:
        if rows and abs(w[2] - rows[-1][0][2]) <= tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return rows


def is_caption_row(row, left_margin):
    """True if row starts (leftmost word) with 'Fig.' <int>. .
    Some captions are indented/centered under their figure, so do not require
    the absolute page margin; requiring 'Fig.' to be the leftmost word of the
    visual row is enough to reject in-paragraph cross references."""
    ws = sorted(row, key=lambda w: w[1])
    if not ws:
        return False
    first, txt = ws[0][1], ws[0][0]
    if txt != "Fig.":
        return False
    for w in ws[1:]:
        # next word on the same baseline
        if w[2] >= ws[0][2] - 2 and w[2] <= ws[0][4] + 2:
            return re.match(r"^\d+\.$", w[0]) is not None
    return False


def caption_key(row):
    ws = sorted(row, key=lambda w: w[1])
    for w in ws[1:]:
        if w[2] >= ws[0][2] - 2 and w[2] <= ws[0][4] + 2:
            m = re.match(r"^(\d+)\.$", w[0])
            if m:
                return "fig" + m.group(1)
            break
    return None


def is_sentence_row(row, left_margin, right_margin):
    ws = sorted(row, key=lambda w: w[1])
    if len(ws) < 3:
        return False
    return ws[0][1] <= left_margin + 8.0 and ws[-1][3] >= right_margin - 30.0


SUBLABEL_RE = re.compile(r"^\([A-Z]\)$")


def figure_top(rows, cap_index, left_margin, right_margin):
    """Walk up from the caption row to find the top boundary of the figure.

    Boundary candidates, in order of preference:
      * the previous figure's caption directly above (stacked figures, e.g.
        Fig. 18/19 on the same page);
      * the bottom of a paragraph block -- a run of >=2 consecutive
        full-width sentence rows, which proves the row is body text rather
        than an isolated full-width figure label;
      * otherwise the running head (figure starts at the top of the page).
    A single isolated full-width row is treated as figure content and skipped
    (e.g. the CKM-matrix row in Fig. 1, quark labels in Fig. 21).
    """
    prev_sentence = False
    for j in range(cap_index - 1, -1, -1):
        ws = sorted(rows[j], key=lambda w: w[1])
        if ws and SUBLABEL_RE.match(ws[0][0]):
            continue
        if is_caption_row(rows[j], left_margin):
            return max(w[4] for w in rows[j])
        if is_sentence_row(rows[j], left_margin, right_margin):
            if prev_sentence:
                # two consecutive sentence rows -> a paragraph block.  The
                # run's lowest line is rows[j+1]; the row just below it is
                # either the paragraph's short last line (body text) or figure
                # content.
                below = rows[j + 2] if j + 2 < len(rows) else None
                if below is not None:
                    bw = sorted(below, key=lambda w: w[1])
                    if bw and bw[0][1] <= left_margin + 8.0:
                        return max(w[4] for w in below)
                return max(w[4] for w in rows[j + 1])
            prev_sentence = True
        else:
            prev_sentence = False
    # No paragraph/caption boundary above: the figure occupies the page below
    # the running head.  Locate the running head by its text ("INTRODUCTION TO
    # LATTICE QCD" / "Rajan Gupta") -- a position window is unsafe because
    # figure content can start just 3pt below the header (e.g. Fig. 1's top
    # decay line sits at yMin=169 vs the header at yMin=158).
    if not rows:
        return 55.0
    header_rows = [r for r in rows
                   if any(w[0] in ("INTRODUCTION", "Rajan", "Gupta") for w in r)]
    if header_rows:
        return max(max(w[4] for w in r) for r in header_rows)
    return 55.0


def page_margins(words):
    lm = min(w[1] for w in words) if words else 136.0
    rm = max(w[3] for w in words) if words else 459.0
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
    all_crops = []   # (figkey, page, path, ink)
    for page in range(5, 150):
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
            top = figure_top(rows, i, lm, rm)
            x, y = lm - 3.0, top
            w, h = (rm + 3.0 - x), (cap_top - 3.0 - top)
            cands = []
            p = render_crop(page, x, y, w, h)
            if p:
                cands.append((p, ink_fraction(p)))
            # split-across-page: caption near page top -> also try prev page bottom
            if cap_top < 120 and page > 5:
                p2 = render_crop(page - 1, lm - 3.0, 0.5 * 792.0,
                                 (rm - lm + 6), 0.44 * 792.0)
                if p2:
                    cands.append((p2, ink_fraction(p2)))
            if not cands:
                continue
            best = max(cands, key=lambda c: c[1])
            all_crops.append((key, page, best[0], best[1]))
            for cpath, _ in cands:
                if cpath != best[0]:
                    os.path.exists(cpath) and os.remove(cpath)

    best_by_key = {}
    for key, page, path, ink in all_crops:
        if key not in best_by_key or ink > best_by_key[key][2]:
            best_by_key[key] = (page, path, ink)

    print(f"{'key':<6} {'page':>5} {'ink':>7}  status")
    n = 0
    for key in sorted(best_by_key, key=lambda k: int(k[3:])):
        page, path, ink = best_by_key[key]
        final = os.path.join(OUT, key + ".png")
        if os.path.exists(final):
            os.remove(final)
        os.rename(path, final)
        if ink < 0.0005:
            print(f"{key:<6} {page:>5} {ink*100:6.2f}%  DROPPED (empty/cross-ref)")
            continue
        n += 1
        print(f"{key:<6} {page:>5} {ink*100:6.2f}%  kept")
    print(f"\nKEPT figures: {n} / {len(best_by_key)}")


if __name__ == "__main__":
    main()

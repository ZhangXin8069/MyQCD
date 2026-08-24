#!/usr/bin/env python3
"""Extract figures from 'Confinement of quarks.pdf' (Wilson, PRD 10, 2445 (1974))
into images/.

The paper is a two-column Phys. Rev. layout. Each figure is a small line drawing
inside one column, sitting just above its caption. The figure regions below were
verified by hand against the scan: (page, column, y-top, y-bottom) in PDF points
(0 = page top). Each region is rendered at 300 dpi with pdftoppm and then
auto-cropped to its ink bounding box, saving images/figN.png.
"""
import subprocess, os
from PIL import Image

PDF = "/root/lattice-pdf/books/Confinement of qnarks.pdf"
OUT = "/root/lattice-pdf/books/Confinement_of_quarks_latex/images"
DPI = 300
SCALE = DPI / 72.0

COL_L = (62.0, 305.0)
COL_R = (307.0, 555.0)

# (figure, page, column, y_top, y_bottom)  -- y in PDF points from top of page.
REGIONS = [
    (1,  2, "R", 138.0, 200.0),
    (2,  2, "R", 640.0, 703.0),
    (3,  3, "L", 610.0, 704.0),
    (4,  3, "R", 135.0, 212.0),
    (5,  3, "R", 610.0, 694.0),
    (6,  4, "R", 135.0, 216.0),
    (7,  4, "R", 610.0, 705.0),
    (8,  6, "R", 135.0, 204.0),
    (9,  9, "R", 630.0, 713.0),
    (10, 10, "R", 590.0, 701.0),
]


def render(page, x, y, w, h, tag):
    px, py = int(x * SCALE), int(y * SCALE)
    pw, ph = int(w * SCALE), int(h * SCALE)
    tmp = os.path.join(OUT, f"_tmp_{tag}")
    subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-f", str(page), "-l", str(page),
                    "-x", str(px), "-y", str(py), "-W", str(pw), "-H", str(ph),
                    "-singlefile", PDF, tmp], capture_output=True, text=True)
    p = tmp + ".png"
    return p if os.path.exists(p) else None


def ink_crop(path, pad=4):
    im = Image.open(path).convert("L")
    px = im.load()
    W, H = im.size
    xs, ys = [], []
    for yy in range(H):
        for xx in range(W):
            if px[xx, yy] < 190:
                xs.append(xx); ys.append(yy)
    if not xs:
        return path
    x0, x1 = max(0, min(xs) - pad), min(W, max(xs) + pad)
    y0, y1 = max(0, min(ys) - pad), min(H, max(ys) + pad)
    im.crop((x0, y0, x1, y1)).save(path)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    for n, page, colname, ytop, ybot in REGIONS:
        col = COL_L if colname == "L" else COL_R
        x, w = col[0] - 2.0, col[1] + 2.0 - col[0]
        p = render(page, x, ytop, w, ybot - ytop, f"fig{n}")
        if not p:
            print(f"fig{n}: render failed (page {page})")
            continue
        ink_crop(p)
        final = os.path.join(OUT, f"fig{n}.png")
        if os.path.exists(final):
            os.remove(final)
        os.rename(p, final)
        print(f"fig{n}: page {page} col {colname} y {ytop:.0f}..{ybot:.0f}  "
              f"size {Image.open(final).size}")


if __name__ == "__main__":
    main()

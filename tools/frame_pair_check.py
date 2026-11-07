"""Frame-pair check before a paid first/last-frame video job.

Adopted 7 Nov 2026 (PRODUCTION_PLAYBOOK.md section 8, item 11). Writes, into OUT_DIR:
  overlay.png     the two frames blended 50/50: ghosting shows where they disagree
  diff.png        the absolute difference, amplified, as a heat map (dark = same)
  diff_grid.png   the END frame with the most-changed grid cells outlined
  report.json     per-cell change scores and the cells above the threshold
and prints the cells that changed most, as "row,col" on an 8x8 grid plus the
percentage of the frame that changed. Anything that should stay fixed (walls,
props, cup size, sky) must not appear in that list.

Usage:
  python -I tools/frame_pair_check.py START.png END.png OUT_DIR [--grid 8] [--threshold 6]

threshold is the mean absolute difference (0-255) a grid cell must exceed to be
listed; 6 catches a wall-colour shift, while a moving person scores far higher.
Frames of different sizes are compared after resizing END to START, with a warning,
because frames sent to the model must already be the same size.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw


def load(path):
    return Image.open(path).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start")
    ap.add_argument("end")
    ap.add_argument("out_dir")
    ap.add_argument("--grid", type=int, default=8)
    ap.add_argument("--threshold", type=float, default=6.0)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    s, e = load(a.start), load(a.end)
    size_warning = None
    if s.size != e.size:
        size_warning = f"sizes differ: start {s.size}, end {e.size}; END resized to START for the comparison"
        print("WARNING:", size_warning, file=sys.stderr)
        e = e.resize(s.size, Image.LANCZOS)

    sa = np.asarray(s).astype(np.int16)
    ea = np.asarray(e).astype(np.int16)
    diff = np.abs(sa - ea).mean(axis=2)  # H x W, 0-255

    Image.blend(s, e, 0.5).save(os.path.join(a.out_dir, "overlay.png"))

    amp = np.clip(diff * 4, 0, 255).astype(np.uint8)
    heat = np.zeros((*amp.shape, 3), dtype=np.uint8)
    heat[..., 0] = amp                                   # red grows with change
    heat[..., 1] = np.clip(amp.astype(np.int16) - 128, 0, 255).astype(np.uint8) * 2
    Image.fromarray(heat).save(os.path.join(a.out_dir, "diff.png"))

    h, w = diff.shape
    g = a.grid
    cells = []
    for r in range(g):
        for c in range(g):
            y0, y1 = r * h // g, (r + 1) * h // g
            x0, x1 = c * w // g, (c + 1) * w // g
            cells.append({"row": r, "col": c, "mean_abs_diff": round(float(diff[y0:y1, x0:x1].mean()), 2),
                          "box": [x0, y0, x1, y1]})
    flagged = sorted([k for k in cells if k["mean_abs_diff"] > a.threshold],
                     key=lambda k: -k["mean_abs_diff"])

    marked = e.copy()
    d = ImageDraw.Draw(marked)
    for k in flagged:
        x0, y0, x1, y1 = k["box"]
        d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(255, 40, 40), width=max(2, w // 400))
        d.text((x0 + 4, y0 + 4), f"{k['row']},{k['col']} {k['mean_abs_diff']:.0f}", fill=(255, 40, 40))
    marked.save(os.path.join(a.out_dir, "diff_grid.png"))

    changed_pct = round(float((diff > a.threshold).mean() * 100), 1)
    report = {"start": os.path.abspath(a.start), "end": os.path.abspath(a.end), "size": list(s.size),
              "grid": g, "threshold": a.threshold, "changed_pixels_pct": changed_pct,
              "flagged_cells": flagged, "all_cells": cells, "warning": size_warning}
    with open(os.path.join(a.out_dir, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    print(f"{changed_pct}% of pixels differ by more than {a.threshold}")
    print(f"{len(flagged)} of {g*g} cells above threshold (row,col = score):")
    for k in flagged:
        print(f"  {k['row']},{k['col']} = {k['mean_abs_diff']}")
    print("Check: does every flagged cell hold something that is MEANT to move? "
          "A flagged wall, sky, prop or fixed object means the frames disagree; fix the frame before paying.")


if __name__ == "__main__":
    main()

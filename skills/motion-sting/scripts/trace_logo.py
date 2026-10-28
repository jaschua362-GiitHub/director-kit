"""Trace a flat-colour raster logo into per-glyph vector paths for canvas animation.

    python trace_logo.py LOGO.png --palette brown=#6C3715 olive=#A9A937 [yellow=#FEDA00 ...]
                         [--bg #FFFFFF] [--scale 4] [--out glyphs.js]

Output
  glyphs.js           window.GLYPHS = [{id, layer, row, d, bbox}]   (coords = source pixels)
  glyphs_preview.svg  every glyph drawn in its colour with its id — open it to map ids → letters,
                      then give ids meaningful names in your scene code (e.g. G('olive_r1_3') = 'A').

Rules learned the hard way
  * Use the largest raster you have (≥1200 px wide); a vector master beats any trace — ask first.
  * potracer treats True as background: pass `mask <= 127` (inverted), or you get one giant frame curve.
  * Anti-aliased edges get mis-read as a third palette colour by nearest-colour matching (a caramel
    halo round brown letters). Colour unmixing (below) fixes it; --open erodes leftovers but breaks
    thin type (taglines) — off by default.
  * Simple geometric marks (a cup, a circle icon) are better rebuilt as exact geometry in code
    than traced — then verify alignment with a multiply overlay of the original (sting.js ?debug).
Requires: pip install numpy pillow potracer
"""
import argparse, json, os
import numpy as np
import potrace
from PIL import Image, ImageFilter


def hex2rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('--palette', nargs='+', required=True, help='name=#hex for each logo colour')
ap.add_argument('--bg', default='#FFFFFF')
ap.add_argument('--scale', type=int, default=4)
ap.add_argument('--min-size', type=float, default=3.0, help='drop components smaller than this (px)')
ap.add_argument('--out', default='glyphs.js')
ap.add_argument('--open', action='store_true', help='1-px morphological opening per layer (kills AA slivers; breaks hairline type)')
a = ap.parse_args()

pal = [('bg', hex2rgb(a.bg))] + [(p.split('=')[0], hex2rgb(p.split('=')[1])) for p in a.palette]
names = [n for n, _ in pal]
im = Image.open(a.src).convert('RGB')
W, H = im.size
arr = np.asarray(im).astype(np.float32)
cols = np.array([c for _, c in pal], np.float32)
# Colour unmixing: model every pixel as a blend of the background and ONE logo colour. The colour whose
# bg→colour line explains the pixel best owns it, with coverage = position along that line. Edge pixels of a
# brown letter on white therefore stay brown (partial coverage) instead of being mis-read as caramel.
bg = cols[0]
res, cov = [], []
for c in cols[1:]:
    v = c - bg
    t = np.clip(((arr - bg) @ v) / (v @ v), 0, 1)
    res.append(((arr - (bg + t[..., None] * v)) ** 2).sum(-1)); cov.append(t)
res, cov = np.stack(res), np.stack(cov)
owner = res.argmin(0) + 1                                    # 1..n (0 = background)


def layer_mask(i):
    m = np.where(owner == i, cov[i - 1], 0)
    img = Image.fromarray((m * 255).astype(np.uint8))
    if a.open:
        img = img.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))  # opening
    img = img.resize((W * a.scale, H * a.scale), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))
    return np.asarray(img) <= 127                                                   # potracer: True = background


def curve_d(c):
    s = a.scale
    f = lambda p: f'{p.x / s:.2f},{p.y / s:.2f}'
    out, xs, ys = [f'M{f(c.start_point)}'], [c.start_point.x], [c.start_point.y]
    for sg in c.segments:
        if sg.is_corner:
            out.append(f'L{f(sg.c)}L{f(sg.end_point)}'); xs += [sg.c.x, sg.end_point.x]; ys += [sg.c.y, sg.end_point.y]
        else:
            out.append(f'C{f(sg.c1)} {f(sg.c2)} {f(sg.end_point)}'); xs.append(sg.end_point.x); ys.append(sg.end_point.y)
    out.append('Z')
    return ''.join(out), [min(xs) / s, min(ys) / s, max(xs) / s, max(ys) / s]


def inside(o, i): return o[0] <= i[0] + 1 and o[1] <= i[1] + 1 and o[2] >= i[2] - 1 and o[3] >= i[3] - 1


glyphs = []
for li, name in enumerate(names):
    if li == 0: continue
    curves = [curve_d(c) for c in potrace.Bitmap(layer_mask(li)).trace(turdsize=40, alphamax=1.0, opticurve=True, opttolerance=.2)]
    curves.sort(key=lambda c: -(c[1][2] - c[1][0]) * (c[1][3] - c[1][1]))
    comps = []
    for d, bb in curves:                                     # holes join the outline that contains them
        host = next((g for g in comps if inside(g['bbox'], bb)), None)
        if host: host['d'] += d
        else: comps.append({'d': d, 'bbox': bb})
    comps = [g for g in comps if min(g['bbox'][2] - g['bbox'][0], g['bbox'][3] - g['bbox'][1]) >= a.min_size]
    for g in comps: g['layer'] = name
    glyphs += comps

# rows: glyphs whose vertical extents overlap belong to the same row (dots, inner marks stay with their line)
glyphs.sort(key=lambda g: g['bbox'][1])
row, row_bottom = -1, -1e9
for g in glyphs:
    if g['bbox'][1] > row_bottom - 2: row += 1; row_bottom = g['bbox'][3]
    else: row_bottom = max(row_bottom, g['bbox'][3])
    g['row'] = row
count = {}
for g in sorted(glyphs, key=lambda g: (g['row'], g['layer'], g['bbox'][0])):
    k = (g['layer'], g['row']); count[k] = count.get(k, 0) + 1
    g['id'] = f"{g['layer']}_r{g['row']}_{count[k]}"
    g['bbox'] = [round(v, 2) for v in g['bbox']]

with open(a.out, 'w') as f:
    f.write('window.GLYPHS=' + json.dumps(glyphs) + ';')
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       f'<rect width="100%" height="100%" fill="{a.bg}"/>']
colour = dict(pal)
for g in glyphs:
    r, gg, b = colour[g['layer']]
    svg.append(f'<path d="{g["d"]}" fill="rgb({r},{gg},{b})" fill-rule="evenodd" opacity=".85"/>')
    svg.append(f'<text x="{g["bbox"][0]}" y="{g["bbox"][1] - 3}" font-size="11" font-family="monospace" fill="#c0f">{g["id"]}</text>')
svg.append('</svg>')
open(os.path.splitext(a.out)[0] + '_preview.svg', 'w').write('\n'.join(svg))
print(f'{len(glyphs)} glyphs -> {a.out} (+ _preview.svg)')
for g in glyphs: print(f"  {g['id']:<16} bbox {g['bbox']}")

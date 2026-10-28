"""Turn an ImageGen sumi-ink kanji (black on white) into a ruby-red alpha matte and inline it into title_mock.html.

Usage: python make_kanji_matte.py TK01
"""
import base64, io, pathlib, re, sys
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "startframes/returns"
RUBY_DARK, RUBY_LIGHT = np.array([158, 14, 34]), np.array([222, 34, 56])


def matte(job):
    g = np.asarray(Image.open(SRC / f"{job}-a01.png").convert("L"), dtype=np.float32) / 255
    ink = np.clip((0.92 - g) / 0.80, 0, 1)                 # paper -> 0, solid ink -> 1, dry brush in between
    ys, xs = np.where(ink > 0.05)
    pad = 24
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, g.shape[0])
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, g.shape[1])
    ink = ink[y0:y1, x0:x1]
    # Dense ink reads deeper red, thin dry-brush reads brighter: keeps the stroke's tonal life.
    rgb = RUBY_LIGHT + (RUBY_DARK - RUBY_LIGHT) * ink[..., None]
    rgba = np.dstack([rgb, ink * 255]).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    out.save(HERE / f"kanji_matte_{job}.png")
    return out


def inline(img):
    buf = io.BytesIO(); img.save(buf, "PNG", optimize=True)
    uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    page = HERE / "title_mock.html"
    s = page.read_text(encoding="utf-8")
    s = re.sub(r"const KANJI_MATTE = '[^']*';", f"const KANJI_MATTE = '{uri}';", s, count=1)
    page.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    job = sys.argv[1] if len(sys.argv) > 1 else "TK01"
    m = matte(job)
    inline(m)
    print(job, m.size)

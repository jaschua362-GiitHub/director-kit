"""Epigraph overlay for Hold the Note (EPIGRAPH_SPEC.md). Set locally with PIL, never generated.
Hanja column 合之然後有聲 (one vertical column), English line under it. Static ink texture (<= 4 % luminance range), no glow/outline,
very soft shadow (<= 35 %, 6 px blur). Opacity schedule in record frames."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HANJA = "合之然後有聲"
ENGLISH = "Only when joined does sound arise."
# ======================= CONFIG (edit here; re-run only the epigraph + finish steps) =======================
HFONT = r"<LAB>\experiments\TEST-020-hold-the-note\production\p5c_build\epigraph\fonts_dl\kouzan\KouzanGyousho.ttf"   # Kouzan Gyosho (brush running script), Jason final choice
HFONT_INDEX = 0
HWEIGHT = None            # variable-font weight axis; set None for a static font
EFONT = r"C:\Windows\Fonts\segoeuisl.ttf"        # Segoe UI Semilight (director: more visible than Light)
SIZES = {"H": (1920, 1080), "V": (1080, 1920)}
# size = glyph px, step = column step px, top = top of first glyph cell, esz = English px, gap = last glyph cell bottom -> English centre, cx = column centre x
LAYOUT = {"H": dict(size=92, step=104, top=170, esz=34, gap=64, cx=960),   # 5C: English 28->34 px for phone legibility
          "V": dict(size=96, step=110, top=525, esz=38, gap=66, cx=540)}   # 5C: English 30->38 px   # gap: last glyph cell bottom -> English centre (about 46 px clear under the glyph)
# ===========================================================================================================
IN0, IN1, OUT0, OUT1 = 966, 980, 1041, 1054        # fade in 966-980, full 981-1040, fade out 1041-1054
EN_DELAY = 8
SHADOW_OP, SHADOW_BLUR, SHADOW_DY = 0.32, 6, 2
SPACING = 0.7


def ss(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)


def opacity(f):
    """(hanja, english) opacity factors 0..1 at record frame f"""
    if f < IN0 or f > OUT1:
        return 0.0, 0.0
    fin = ss((f - IN0 + 1) / (IN1 - IN0 + 1))
    fout = 1.0 - ss((f - OUT0 + 1) / (OUT1 - OUT0 + 1)) if f >= OUT0 else 1.0
    ein = ss((f - (IN0 + EN_DELAY) + 1) / (IN1 - IN0 + 1))
    return fin * fout, ein * fout


def choose_colour(mean_luma):
    if mean_luma > 150:
        return (34, 30, 28), 0.88, "ink-dark"
    return (240, 235, 224), 0.95, "warm off-white"


class Epigraph:
    def __init__(self, fmt, colour, base_op):
        W, H = SIZES[fmt]; L = LAYOUT[fmt]; self.fmt, self.W, self.H = fmt, W, H
        self.colour = np.array(colour, np.float32); self.base_op = base_op
        hf = ImageFont.truetype(HFONT, L["size"], index=HFONT_INDEX)
        if HWEIGHT is not None:
            hf.set_variation_by_axes([HWEIGHT])
        ef = ImageFont.truetype(EFONT, L["esz"])
        hm = Image.new("L", (W, H), 0); dh = ImageDraw.Draw(hm)
        self.glyph_boxes = []
        for k, ch in enumerate(HANJA):
            cy = L["top"] + L["size"] / 2 + k * L["step"]
            dh.text((L["cx"], cy), ch, font=hf, fill=255, anchor="mm")
            self.glyph_boxes.append(hm.getbbox() if k == 0 else None)
        # English with letter-spacing, centred
        em = Image.new("L", (W, H), 0); de = ImageDraw.Draw(em)
        widths = [ef.getlength(c) + SPACING for c in ENGLISH]; tw = sum(widths) - SPACING
        x = L["cx"] - tw / 2; ey = L["top"] + 5 * L["step"] + L["size"] + L["gap"]
        for c, w in zip(ENGLISH, widths):
            de.text((x, ey), c, font=ef, fill=255, anchor="lm"); x += w
        self.hm = np.asarray(hm, np.float32) / 255; self.em = np.asarray(em, np.float32) / 255
        both = np.maximum(self.hm, self.em)
        ys, xs = np.nonzero(self.hm > 0.02); self.hanja_box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
        ys, xs = np.nonzero(self.em > 0.02); self.english_box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
        a, b = self.hanja_box, self.english_box
        self.reg = (max(0, min(a[0], b[0]) - 24), max(0, a[1] - 24), min(W, max(a[2], b[2]) + 24), min(H, b[3] + 24))
        x0, y0, x1, y1 = self.reg
        self.hm, self.em = self.hm[y0:y1, x0:x1], self.em[y0:y1, x0:x1]
        # static ink texture inside the glyphs: low-frequency noise, +-2 % (4 % range) of luminance
        rng = np.random.default_rng(6112026)
        n = np.asarray(Image.fromarray((rng.random(self.hm.shape) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)), np.float32)
        n = (n - n.mean()) / (n.std() + 1e-6); n = np.clip(n / 4.0, -1, 1)        # about +-1 within 4 sigma
        self.tex = (1.0 + 0.02 * n)[..., None]
        sh = Image.fromarray((np.maximum(self.hm, self.em) * 255).astype(np.uint8))
        sh = sh.transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, -SHADOW_DY)).filter(ImageFilter.GaussianBlur(SHADOW_BLUR))
        self.sm = (np.asarray(sh, np.float32) / 255)[..., None]
        self.hm, self.em = self.hm[..., None], self.em[..., None]
        self.max_tex_range = float(self.tex.max() - self.tex.min())

    def apply(self, fr, f):
        oh, oe = opacity(f)
        if oh <= 0 and oe <= 0:
            return fr
        x0, y0, x1, y1 = self.reg
        reg = fr[y0:y1, x0:x1].astype(np.float32)
        a = self.base_op * (self.hm * oh + self.em * oe)
        reg *= 1 - SHADOW_OP * self.sm * np.maximum(oh, oe)
        col = np.clip(self.colour * self.tex, 0, 255)
        reg = reg * (1 - a) + col * a
        fr[y0:y1, x0:x1] = np.clip(reg + 0.5, 0, 255).astype(np.uint8)
        return fr

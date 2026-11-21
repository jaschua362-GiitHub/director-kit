"""Crenature logo intro v4+ - "light carves the dragon" (dark to light). Code only, 2.5D.

    python build/render2.py --times 0.3 1.0 2.0 2.6 3.1 4.5 --out stills/v4      # stills
    python build/render2.py --all --fps 60 --sub 4 --out frames/v4                 # full sequence

The mark never deforms: the dragon is the rigid glossy 3D logo from the first frame. Light, camera,
the eye and hard type cuts tell the story (see BRIEF.md, "Direction change").
Layout space = the final frame at 2x (3840x2160), from parts/*.png (approved SVG).
"""
import argparse, json, os
import numpy as np
from multiprocessing import Pool
from PIL import Image, ImageFilter
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DUR = 5.6
W2, H2, W, H = 3840, 2160, 1920, 1080
EYE = np.array([0xFF, 0x6A, 0x24]) / 255
EYE_HOT = np.array([0xFF, 0xBE, 0x77]) / 255
INK = np.array([0x10, 0x10, 0x10]) / 255
LETTER = np.array([0x12, 0x12, 0x12]) / 255
WARM = np.array([1.0, 0.93, 0.84])                     # rim-light colour

# ---------------------------------------------------------------- timeline
T_EYE0, T_EYE1 = 0.15, 0.50          # eye opens in the dark
T_TRACE0, T_TRACE1 = 0.55, 2.25      # rim-light runs head -> tail
T_PULL0, T_PULL1 = 0.30, 2.35        # camera pulls back from the eye to the whole dragon (centred)
T_L1, T_L2, T_L3 = 2.42, 2.52, 2.61  # studio lights snap on: floor strip, backdrop, key
T_LIGHT0, T_LIGHT1 = T_L1, T_L3 + 0.04
T_LIGHT_HIT = T_L1
T_SLIDE0, T_SLIDE1 = 2.65, 3.45      # camera slides from the dragon to the full lockup
T_TYPE0, T_TYPE_STEP, T_TYPE_DUR = 2.85, 0.05, 0.07   # hard letter cuts (~4 frames each)
T_BLINK = 3.35
T_GLINT = 4.40                        # light sweep + eye glint in the hold
Z_CLOSE = 3.0


def sstep(a, b, x):
    x = np.clip((x - a) / (b - a), 0, 1)
    return x * x * (3 - 2 * x)


def ease_io(a, b, x, p=3):
    x = np.clip((x - a) / (b - a), 0, 1)
    return np.where(x < .5, 2 ** (p - 1) * x ** p, 1 - (-2 * x + 2) ** p / 2)


def ease_out(a, b, x, p=3):
    x = np.clip((x - a) / (b - a), 0, 1)
    return 1 - (1 - x) ** p


def load_mask(name):
    return np.asarray(Image.open(f'parts/{name}.png'))[..., 3].astype(np.float32) / 255


class Assets:
    def __init__(self):
        L = json.load(open('parts/layout.json'))
        self.letters = [load_mask(n) for n in L['parts'] if n.startswith('L')]
        self.letter_boxes = [self.bbox(m) for m in self.letters]
        body, horns, self.eye = load_mask('body'), load_mask('horns'), load_mask('eye')
        full = np.clip(body + horns, 0, 1)
        self.x0, self.y0, self.x1, self.y1 = self.bbox(full, pad=160)
        sl = (slice(self.y0, self.y1), slice(self.x0, self.x1))
        self.M = full[sl]
        self.eye_c = np.argwhere(self.eye > 0.5).mean(0)[::-1]
        ys, xs = np.nonzero(body > 0.5)
        self.foot_y, self.foot_x = ys.max(), xs[ys > ys.max() - 40].mean()
        # static 3D surface (the mark never deforms)
        ink = self.M > 0.5
        d = ndimage.gaussian_filter(ndimage.distance_transform_edt(ink), 2.0)
        half = np.maximum(ndimage.gaussian_filter(ndimage.grey_dilation(d, size=(41, 41)), 14), 2.0)
        tt = np.clip(d / half, 0, 1)
        hgt = ndimage.gaussian_filter(half * np.sqrt(1 - (1 - tt) ** 2) * 0.95, 1.6)
        din = ndimage.distance_transform_edt(self.M > 0.5)
        self.rimline = (np.exp(-(din / 3.2) ** 2) * (self.M > 0.3)).astype(np.float32)   # ~1.5 px at 1x
        gy, gx = np.gradient(hgt)
        n = np.dstack([-gx, -gy, np.ones_like(hgt)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
        self.n = n.astype(np.float32)
        self.ndv = np.clip(n[..., 2], 0, 1).astype(np.float32)
        self.r = (2 * n * self.ndv[..., None] - np.array([0, 0, 1.0])).astype(np.float32)
        # sigma: where each pixel sits along the dragon, 0 = tail tip, 1 = nose (horns/head = 1)
        sp = np.load('parts/spine.npz'); P = sp['pts']
        yy, xx = np.nonzero(self.M > 0.02)
        _, own = cKDTree(P).query(np.c_[xx + self.x0, yy + self.y0])
        sig = np.zeros(self.M.shape, np.float32); sig[yy, xx] = own / (len(P) - 1)
        hz = horns[sl] > 0.3
        sig[hz] = 1.0
        self.sig = ndimage.gaussian_filter(sig, 3)
        # light-front path (for the sound and the camera): spine points head -> tail
        self.P = P
        bx = self.bbox(body)
        self.dcx, self.dcy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2 - 10

    @staticmethod
    def bbox(m, pad=0):
        ys, xs = np.nonzero(m > 0.02)
        return (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                min(xs.max() + pad + 1, W2), min(ys.max() + pad + 1, H2))


def front(t):
    """light-front position along the dragon (1 = nose ... 0 = tail tip), head first."""
    return 1.10 - 1.16 * ease_io(T_TRACE0, T_TRACE1, t, 2)


def st(t, t0, d=0.035):
    return float(np.clip((t - t0) / d, 0, 1))


def light_level(t):
    """how much studio light is on the dragon (3 snaps)."""
    return 0.35 * st(t, T_L1) + 0.25 * st(t, T_L2) + 0.40 * st(t, T_L3)


def bg_levels(t):
    return st(t, T_L1), st(t, T_L2)          # floor strip, backdrop


def exposure_kick(t):
    return sum(0.22 * np.exp(-((t - tk - 0.025) / 0.028) ** 2) for tk in (T_L1, T_L2, T_L3))


def shade(A, t):
    """RGB of the dragon (bbox crop): dark rim-carved look blended into the full studio look."""
    n, ndv, r = A.n, A.ndv, A.r
    E = light_level(t)
    # --- studio look (as in the approved end frame), key light sweeps at the glint
    b2 = np.sin(np.pi * np.clip((t - (T_GLINT - 0.45)) / 1.1, 0, 1)) ** 2
    az = np.radians(-150 + 10 * sstep(T_LIGHT0, DUR, t) + 32 * b2)
    key = np.array([np.cos(az) * 0.75, np.sin(az) * 0.75 - 0.35, 0.55]); key /= np.linalg.norm(key)
    rk = np.clip((r * key).sum(2), 0, 1)
    env = (0.24 + 0.60 * np.clip(-r[..., 1], 0, 1) ** 1.2 + 0.35 * np.clip(r[..., 0], 0, 1) ** 2
           + 0.80 * rk ** 1.5 + 1.4 * rk ** 30)
    fres = 0.05 + 0.95 * (1 - ndv) ** 4
    hv = (key + [0, 0, 1]) / np.linalg.norm(key + [0, 0, 1])
    hl = np.clip((n * hv).sum(2), 0, 1) ** 220
    ndl = np.clip((n * key).sum(2), 0, 1)
    val = 0.07 * (0.4 + 0.6 * ndl) + (0.04 + fres) * env * 0.66 + 0.70 * hl
    # a narrow specular streak travels across the body at the glint
    sw = np.clip((t - (T_GLINT - 0.35)) / 0.8, 0, 1)
    if 0 < sw < 1:
        a2 = np.radians(-205 + 110 * sw)
        k2 = np.array([np.cos(a2) * 0.8, np.sin(a2) * 0.5 - 0.2, 0.5]); k2 /= np.linalg.norm(k2)
        val = val + 1.3 * np.sin(np.pi * sw) * np.clip((r * k2).sum(2), 0, 1) ** 40
    rimw = (1 - ndv) ** 2 * np.clip(-(n[..., 0] * 0.6 + n[..., 1] * 0.8) + 0.25, 0, 1) * 0.45
    studio = np.dstack([val + rimw, val * 0.985 + rimw * 0.86, val * 0.97 + rimw * 0.70])
    # --- dark look: a razor rim-light front runs along the body, leaving a faint lit edge behind
    f = front(t)
    ds = A.sig - f
    band = np.exp(-(ds / 0.03) ** 2) * (ds > -0.06)           # the hot front
    passed = np.clip(ds / 0.04, 0, 1)                           # already carved
    edge = (1 - ndv) ** 2.2
    # a hard light from upper-left grazing the surface where the front is
    kd = np.array([-0.55, -0.65, 0.5]); kd /= np.linalg.norm(kd)
    graze = np.clip((n * kd).sum(2), 0, 1) ** 6
    lum = (A.rimline * (1.35 * band + 0.78 * passed)               # the razor line itself
           + band * (0.55 * edge + 0.30 * graze) + passed * (0.12 * edge + 0.035 * graze + 0.01))
    dark = lum[..., None] * WARM[None, None]
    return np.clip(dark * (1 - E) + studio * E, 0, 1)


def eye_rgba(A, t):
    """eye diamond (alpha), its colour, and glow (layout 2x full frame)."""
    e = A.eye
    open_ = max(0.04, float(sstep(T_EYE0, T_EYE1, t)))
    for tb, d in ((T_BLINK, 0.16),):
        if tb <= t <= tb + d:
            open_ = max(0.06, abs(np.cos(np.pi * (t - tb) / d)))
    if open_ < 1:
        cy = A.eye_c[1]
        ys = np.arange(H2)
        src = cy + (ys - cy) / open_
        e = ndimage.map_coordinates(e, [np.repeat(src[:, None], W2, 1)[int(cy) - 60:int(cy) + 60],
                                        np.tile(np.arange(W2), (120, 1))], order=1)
        full = np.zeros((H2, W2), np.float32); full[int(cy) - 60:int(cy) + 60] = e; e = full
    core = ndimage.distance_transform_edt(e > 0.5)
    hot = np.clip(core / max(core.max(), 1), 0, 1) ** 0.8
    rgb = EYE[None, None] * (1 - hot[..., None]) + EYE_HOT[None, None] * hot[..., None]
    im = Image.fromarray((e * 255).astype(np.uint8))
    E = light_level(t)
    g_small = np.asarray(im.filter(ImageFilter.GaussianBlur(20))).astype(np.float32) / 255
    q = e[::4, ::4].astype(np.float32)                       # wide halo in float (no 8-bit steps)
    g_wide = ndimage.zoom(ndimage.gaussian_filter(q, 22), 4, order=1)[:H2, :W2]
    pulse = np.exp(-((t - T_EYE1) / 0.22) ** 2) + 0.8 * np.exp(-((t - T_GLINT - 0.1) / 0.18) ** 2)
    glow = g_small * (0.9 * (1 - E) + 0.85 * E) + g_wide * (6.0 * (1 - E) * (0.5 + pulse) + 3.0 * E * pulse)
    return e, rgb, glow


def camera(t, A):
    """focus point (layout 2x) and zoom (1 = full frame)."""
    k1 = ease_io(T_PULL0, T_PULL1, t, 3)
    k2 = ease_io(T_SLIDE0, T_SLIDE1, t, 3)
    head = A.eye_c + np.array([-60, 40])
    drag = np.array([A.dcx, A.dcy])
    lock = np.array([W2 / 2 - 30, H2 / 2])
    fx, fy = (head * (1 - k1) + drag * k1) * (1 - k2) + lock * k2
    z0 = Z_CLOSE * (1 - k1) + 1.32 * k1
    z = z0 * (1 - k2) + 0.95 * k2
    x = np.clip((t - T_SLIDE1) / (DUR - T_SLIDE1), 0, 1)
    z = z * (1 + 0.095 * (x - 0.15 * (1 - np.exp(-x / 0.15))))       # ~4 %/s push through the hold
    rot = np.radians(-2.2 * (1 - k1) + 0.15 * np.sin(0.7 * t) * (1 - sstep(3.5, 5.2, t)))
    return fx, fy, z, rot


def burst(t, xx, yy, cx, cy):
    """per-pixel light level: a radial wave from behind the dragon (accelerating), then full."""
    x = np.clip((t - T_LIGHT0) / (T_LIGHT1 - T_LIGHT0), 0, 1)
    R = 2600 * x ** 1.6
    return np.clip((R - np.hypot(xx - cx, yy - cy)) / 420, 0, 1)


def background(E, floor=0.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    if floor > 0:
        E = np.clip(E + floor * 0.55 * sstep(0.45 * H, 1.05 * H, yy), 0, 1)
    r = np.hypot((xx - 0.5 * W) / (0.75 * W), (yy - 0.42 * H) / (0.75 * H))
    k = np.clip(r, 0, 1) ** 1.6
    hi, lo = np.array([0xFE, 0xFD, 0xFC]) / 255, np.array([0xF2, 0xF0, 0xED]) / 255
    light = hi * (1 - k[..., None]) + lo * k[..., None]
    dhi, dlo = np.array([0x0B, 0x0B, 0x0B]) / 255, np.array([0x04, 0x04, 0x05]) / 255
    dark = dhi * (1 - k[..., None]) + dlo * k[..., None]
    E = E[..., None] if np.ndim(E) == 2 else E
    return dark * (1 - E) + light * E


def render(A, t):
    E = light_level(t)
    rgb = np.zeros((H2, W2, 3), np.float32)
    a = np.zeros((H2, W2), np.float32)
    # floor shadow, as the light comes up
    if E > 0:
        yy, xx = np.mgrid[0:H2, 0:W2]
        cx, by = A.foot_x + 30, A.foot_y - 4
        sh = (np.exp(-(((xx - cx) / 250) ** 2 + ((yy - by - 8) / 42) ** 2)) * 0.20
              + np.exp(-(((xx - cx) / 120) ** 2 + ((yy - by) / 9) ** 2)) * 0.25) * bg_levels(t)[1]
        a = sh.astype(np.float32)
    # dragon
    c = shade(A, t)
    sl = (slice(A.y0, A.y1), slice(A.x0, A.x1))
    # in the dark the body only exists where the light has carved it
    vis = np.clip((A.sig - front(t) + 0.07) / 0.07, 0, 1)
    m = A.M * (E + (1 - E) * vis)
    rgb[sl] = rgb[sl] * (1 - m[..., None]) + c * m[..., None]
    a[sl] = a[sl] * (1 - m) + m
    # eye
    e, ergb, glow = eye_rgba(A, t)
    rgb = rgb * (1 - e[..., None]) + ergb * e[..., None]
    a = a * (1 - e) + e
    # wordmark: hard slices from the baseline up, letter by letter (no fades)
    for i, (Lm, (x0, y0, x1, y1)) in enumerate(zip(A.letters, A.letter_boxes)):
        k = float(np.clip((t - (T_TYPE0 + i * T_TYPE_STEP)) / T_TYPE_DUR, 0, 1))
        if k <= 0: continue
        cut = int(y1 - (y1 - y0) * (1 - (1 - k) ** 2))      # rows below `cut` are visible
        dy = int(round((1 - k) * 10))
        la = np.zeros((y1 - y0, x1 - x0), np.float32)
        la[cut - y0:] = Lm[cut:y1, x0:x1]
        ys = slice(y0 + dy, y1 + dy)
        rgb[ys, x0:x1] = rgb[ys, x0:x1] * (1 - la[..., None]) + LETTER * la[..., None]
        a[ys, x0:x1] = a[ys, x0:x1] * (1 - la) + la
    # white light: the carve's hot leading point, and a star glint on the eye in the hold
    wl = np.zeros((H2, W2), np.float32)
    f = front(t)
    if -0.05 < f < 1.05 and t < T_L3:
        ds = A.sig - f
        src = A.rimline * np.exp(-(ds / 0.03) ** 2) * (ds > -0.06)
        blo = ndimage.zoom(ndimage.gaussian_filter(src[::2, ::2], 9), 2, order=1)
        hh, ww = min(blo.shape[0], A.y1 - A.y0), min(blo.shape[1], A.x1 - A.x0)
        wl[A.y0:A.y0 + hh, A.x0:A.x0 + ww] += (blo[:hh, :ww] * 2.2 * (1 - light_level(t))).astype(np.float32)
    gk = np.exp(-((t - T_GLINT - 0.12) / 0.06) ** 2)
    if gk > 0.02:
        ex, ey = A.eye_c
        yy2, xx2 = np.ogrid[0:H2, 0:W2]
        dx, dy = xx2 - ex, yy2 - ey
        star = (np.exp(-(dy / 3.0) ** 2) * np.exp(-np.abs(dx) / 90) + np.exp(-(dx / 3.0) ** 2) * np.exp(-np.abs(dy) / 60)
                + np.exp(-(dx ** 2 + dy ** 2) / (2 * 14.0 ** 2)))
        wl += (star * gk * 0.9).astype(np.float32)
    # camera: sample the 2x layout directly
    fx, fy, z, rot = camera(t, A)
    layer = np.dstack([rgb, a, glow, wl])
    if z < 1.1:                                   # pre-filter when minifying
        layer = ndimage.gaussian_filter(layer, (0.6, 0.6, 0))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    px, py = (xx - W / 2) / (0.5 * z), (yy - H / 2) / (0.5 * z)
    c_, s_ = np.cos(rot), np.sin(rot)
    lx, ly = c_ * px + s_ * py + fx, -s_ * px + c_ * py + fy
    out = np.empty((H, W, 6), np.float32)
    for ch in range(6):
        out[..., ch] = ndimage.map_coordinates(layer[..., ch], [ly, lx], order=1, mode='constant', cval=0)
    # where is the dragon's centre on screen -> centre of the light burst
    dcx, dcy = (A.x0 + A.x1) / 2, (A.y0 + A.y1) / 2
    sx = c_ * (dcx - fx) - s_ * (dcy - fy); sy = s_ * (dcx - fx) + c_ * (dcy - fy)
    cxs, cys = W / 2 + sx * 0.5 * z, H / 2 + sy * 0.5 * z
    ef, eb = bg_levels(t)
    img = background(np.full((H, W), eb, np.float32), ef * (1 - eb)) * (1 - out[..., 3:4]) + out[..., :3]
    g = out[..., 4:5]
    img = img + EYE[None, None] * g * (1 - img) * 1.5
    img = img + out[..., 5:6] * (1 - img)                      # white light: carve front + glint
    kick = exposure_kick(t)
    if kick > 0.01:                                            # light snaps on: overexpose + bloom
        img = 1 - (1 - img) / (1 + kick)
        hb = np.clip(img - 0.8, 0, 1)
        img = img + ndimage.gaussian_filter(hb, (18, 18, 0)) * kick * 3
    return np.clip(img, 0, 1)


A = None


def work(job):
    global A
    if A is None: A = Assets()
    i, t, sub, fps, out = job
    if sub > 1:
        acc = 0
        for k in range(sub):
            acc = acc + render(A, t + (k / sub - 0.5 + 0.5 / sub) * (0.5 / fps))
        f = acc / sub
    else:
        f = render(A, t)
    rg = np.random.default_rng(i)
    f = f + (rg.random(f.shape) + rg.random(f.shape) - 1.0) / 255
    Image.fromarray((np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--times', type=float, nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--fps', type=int, default=60)
    ap.add_argument('--sub', type=int, default=1)
    ap.add_argument('--out', default='stills/v4')
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.all:
        n = int(round(DUR * a.fps))
        jobs = [(i, i / a.fps, a.sub if i / a.fps < 3.0 else 1, a.fps, f'{a.out}/f{i:05d}.png') for i in range(n)]
    else:
        jobs = [(i, t, a.sub, a.fps, f'{a.out}/t{t:05.2f}.png') for i, t in enumerate(a.times)]
    with Pool(a.jobs) as p:
        for k, o in enumerate(p.imap(work, jobs)):
            if k % 30 == 0 or not a.all: print(o, flush=True)

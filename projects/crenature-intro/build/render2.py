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
T_PULL0, T_PULL1 = 0.30, 2.60        # camera pulls back from the eye to the full mark
T_LIGHT0, T_LIGHT1 = 2.32, 2.62      # studio lights rise (hit at T_LIGHT_HIT)
T_LIGHT_HIT = 2.45
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
        hgt = ndimage.gaussian_filter(half * np.sqrt(1 - (1 - tt) ** 2) * 0.95, 3.0)
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

    @staticmethod
    def bbox(m, pad=0):
        ys, xs = np.nonzero(m > 0.02)
        return (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                min(xs.max() + pad + 1, W2), min(ys.max() + pad + 1, H2))


def front(t):
    """light-front position along the dragon (1 = nose ... 0 = tail tip), head first."""
    return 1.10 - 1.16 * ease_io(T_TRACE0, T_TRACE1, t, 2)


def light_level(t):
    return float(ease_out(T_LIGHT0, T_LIGHT1, t, 2))


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
           + 1.05 * rk ** 1.5 + 0.9 * rk ** 9)
    fres = 0.05 + 0.95 * (1 - ndv) ** 4
    hv = (key + [0, 0, 1]) / np.linalg.norm(key + [0, 0, 1])
    hl = np.clip((n * hv).sum(2), 0, 1) ** 70
    ndl = np.clip((n * key).sum(2), 0, 1)
    val = 0.07 * (0.4 + 0.6 * ndl) + (0.04 + fres) * env * 0.66 + 0.32 * hl
    rimw = (1 - ndv) ** 3 * np.clip(-(n[..., 0] * 0.6 + n[..., 1] * 0.8) + 0.2, 0, 1) * 0.30
    studio = np.dstack([val + rimw, val * 0.985 + rimw * 0.86, val * 0.97 + rimw * 0.70])
    # --- dark look: a razor rim-light front runs along the body, leaving a faint lit edge behind
    f = front(t)
    ds = A.sig - f
    band = np.exp(-(ds / 0.035) ** 2) * (ds > -0.08)          # the hot front
    passed = np.clip(ds / 0.05, 0, 1)                           # already carved
    edge = (1 - ndv) ** 2.2
    # a hard light from upper-left grazing the surface where the front is
    kd = np.array([-0.55, -0.65, 0.5]); kd /= np.linalg.norm(kd)
    graze = np.clip((n * kd).sum(2), 0, 1) ** 6
    lum = band * (1.25 * edge + 0.55 * graze) + passed * (0.32 * edge + 0.06 * graze + 0.012)
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
    hot = np.clip(core / max(core.max(), 1), 0, 1) ** 1.5
    rgb = EYE[None, None] * (1 - hot[..., None]) + EYE_HOT[None, None] * hot[..., None]
    im = Image.fromarray((e * 255).astype(np.uint8))
    E = light_level(t)
    g_small = np.asarray(im.filter(ImageFilter.GaussianBlur(20))).astype(np.float32) / 255
    q = e[::4, ::4].astype(np.float32)                       # wide halo in float (no 8-bit steps)
    g_wide = ndimage.zoom(ndimage.gaussian_filter(q, 22), 4, order=1)[:H2, :W2]
    pulse = np.exp(-((t - T_EYE1) / 0.22) ** 2) + 0.8 * np.exp(-((t - T_GLINT - 0.1) / 0.18) ** 2)
    glow = g_small * (0.9 * (1 - E) + 0.35 * E) + g_wide * (6.0 * (1 - E) * (0.5 + pulse) + 3.0 * E * pulse)
    return e, rgb, glow


def camera(t, A):
    """focus point (layout 2x) and zoom (1 = full frame)."""
    k = ease_io(T_PULL0, T_PULL1, t, 3)
    zc = Z_CLOSE * (1 - k) + 1.0 * k
    x = np.clip((t - 2.6) / 3.0, 0, 1)
    z = zc * (1 + 0.055 * (x - 0.2 * (1 - np.exp(-x / 0.2))))       # slow push through the hold
    head = A.eye_c + np.array([-60, 40])
    fx, fy = head * (1 - k) + np.array([W2 / 2 - 30, H2 / 2]) * k
    rot = np.radians(-2.2 * (1 - k) + 0.15 * np.sin(0.7 * t) * (1 - sstep(3.5, 5.2, t)))
    return fx, fy, z, rot


def burst(t, xx, yy, cx, cy):
    """per-pixel light level: a radial wave from behind the dragon (accelerating), then full."""
    x = np.clip((t - T_LIGHT0) / (T_LIGHT1 - T_LIGHT0), 0, 1)
    R = 2600 * x ** 1.6
    return np.clip((R - np.hypot(xx - cx, yy - cy)) / 420, 0, 1)


def background(E):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
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
              + np.exp(-(((xx - cx) / 120) ** 2 + ((yy - by) / 9) ** 2)) * 0.25) * E
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
    # camera: sample the 2x layout directly
    fx, fy, z, rot = camera(t, A)
    layer = np.dstack([rgb, a, glow])
    if z < 1.3:                                   # pre-filter when minifying
        layer = ndimage.gaussian_filter(layer, (0.7, 0.7, 0))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    px, py = (xx - W / 2) / (0.5 * z), (yy - H / 2) / (0.5 * z)
    c_, s_ = np.cos(rot), np.sin(rot)
    lx, ly = c_ * px + s_ * py + fx, -s_ * px + c_ * py + fy
    out = np.empty((H, W, 5), np.float32)
    for ch in range(5):
        out[..., ch] = ndimage.map_coordinates(layer[..., ch], [ly, lx], order=1, mode='constant', cval=0)
    # where is the dragon's centre on screen -> centre of the light burst
    dcx, dcy = (A.x0 + A.x1) / 2, (A.y0 + A.y1) / 2
    sx = c_ * (dcx - fx) - s_ * (dcy - fy); sy = s_ * (dcx - fx) + c_ * (dcy - fy)
    cxs, cys = W / 2 + sx * 0.5 * z, H / 2 + sy * 0.5 * z
    Emap = burst(t, xx, yy, cxs, cys) if T_LIGHT0 < t < T_LIGHT1 + 0.2 else np.full((H, W), E, np.float32)
    img = background(Emap) * (1 - out[..., 3:4]) + out[..., :3]
    g = out[..., 4:5]
    img = img + EYE[None, None] * g * (1 - img) * 1.5
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

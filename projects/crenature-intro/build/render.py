"""Crenature logo intro - frame renderer (2.5D, code only).

    python build/render.py --times 0.5 1.2 2.0 2.6 3.0 3.4 4.0 5.2 --out stills/beats     # stills
    python build/render.py --all --fps 60 --out frames/v1 [--sub 4] [--jobs 4]           # full sequence

Everything is a pure function of time t (seconds). Geometry lives in "layout" space = the final
frame at 2x (3840x2160); a camera (slow push + drift) maps layout -> the 1920x1080 frame.

Beats (see BRIEF.md):
  0.00-0.25  empty studio, push already moving
  0.25-2.55  the dragon flies in head first (glowing eye leads), loops, dives into the centre and
             spirals outward along its own coil until the head locks in place
  2.45-2.85  fin, tail flick, crest and edges grow in from the body
  2.60-3.05  the flat ink body inflates into glossy 3D; light sweep; floor shadow fades in
  3.00-3.15  blink + glint
  3.05-3.80  wordmark letters rise in, left to right
  3.80-5.20  hold, still pushing
"""
import argparse, json, os
import numpy as np
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from scipy.spatial import cKDTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DUR = 5.6
W2, H2 = 3840, 2160            # layout (2x)
W, H = 1920, 1080              # output
INK = np.array([0x10, 0x10, 0x10]) / 255
EYE = np.array([0xFF, 0x6A, 0x24]) / 255
EYE_HOT = np.array([0xFF, 0xBE, 0x77]) / 255
LETTER = np.array([0x12, 0x12, 0x12]) / 255

T_FLY0, T_FLY1 = 0.45, 2.55
T_EYE0, T_EYE1 = 0.12, 0.42     # the eye opens alone in the empty field
T_REV0, T_REV1 = 0.36, 0.62     # the body materialises outward from the eye
T_RIM0, T_RIM1 = 2.33, 2.58     # edge slivers settle in as the coil tightens (no one-frame pop)
T_BLINK2 = 4.28                 # second blink + light sweep in the hold
T_WIPE0, T_WIPE1 = 3.0, 3.75    # wordmark sweep
L_FLY = 900                    # body length in flight (2x px); grows to the full spine in the coil
T_GROW0, T_GROW1 = 2.58, 2.90
T_INF0, T_INF1 = 2.60, 3.05
T_BLINK = 3.00
T_TYPE0, T_TYPE_STEP, T_TYPE_DUR = 3.05, 0.055, 0.32


def sstep(a, b, x):
    x = np.clip((x - a) / (b - a), 0, 1)
    return x * x * (3 - 2 * x)


def ease_out(a, b, x, p=3):
    x = np.clip((x - a) / (b - a), 0, 1)
    return 1 - (1 - x) ** p


# ---------------------------------------------------------------- static assets (loaded once)
def load_mask(name):
    return np.asarray(Image.open(f'parts/{name}.png'))[..., 3].astype(np.float32) / 255


class Assets:
    def __init__(self):
        L = json.load(open('parts/layout.json'))
        self.letters = [load_mask(n) for n in L['parts'] if n.startswith('L')]
        self.letter_boxes = [self.bbox(m) for m in self.letters]
        self.body = load_mask('body')
        self.horns = load_mask('horns')
        self.eye = load_mask('eye')
        sp = np.load('parts/spine.npz')
        self.P, self.R, self.Rs = sp['pts'], sp['radius'], sp['radius_s']
        self.N = len(self.P)
        B = self.body > 0.5
        # nearest spine sample for every body pixel -> head patch = pixels owned by the last 170 samples
        ys, xs = np.nonzero(B)
        _, own = cKDTree(self.P).query(np.c_[xs, ys])
        owner = np.full(B.shape, -1); owner[ys, xs] = own
        self.k_head = self.N - 170
        head = (owner >= self.k_head) & B
        self.head = head.astype(np.float32) * self.body
        rec = np.load('parts/recon_mask.npy')
        base = rec | head
        grow = B & ~base
        self.grow_d = ndimage.distance_transform_edt(~base)        # distance from the landed body
        self.grow_d[~grow] = 0
        self.grow_max = float(self.grow_d.max())
        self.full = np.clip(self.body + self.horns, 0, 1)          # final silhouette
        # rigid patches carried by the head frame during flight: head patch + horns + eye
        self.bx0, self.by0, self.bx1, self.by1 = self.bbox(self.full, pad=140)
        hb = self.bbox(np.maximum(self.head, self.horns), pad=40)
        self.hbox = hb
        x0, y0, x1, y1 = hb
        self.head_patch = np.maximum(self.head, self.horns)[y0:y1, x0:x1]
        eb = self.bbox(self.eye, pad=60)
        self.ebox = eb
        self.eye_patch = self.eye[eb[1]:eb[3], eb[0]:eb[2]]
        self.eye_c = np.argwhere(self.eye > 0.5).mean(0)[::-1]     # (x, y)
        ys, xs = np.nonzero(self.body > 0.5)
        self.foot_y = ys.max()
        self.foot_x = xs[ys > self.foot_y - 40].mean()
        self.route, self.h_end = self.build_route()
        self.prog = self.progress_table()

    @staticmethod
    def bbox(m, pad=0):
        ys, xs = np.nonzero(m > 0.02)
        return (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                min(xs.max() + pad + 1, W2), min(ys.max() + pad + 1, H2))

    def build_route(self):
        """pre-extension + flight spline + the spine itself (tail -> nose), resampled at 1 px."""
        P = self.P
        t0 = P[40] - P[0]; t0 /= np.linalg.norm(t0)
        way = np.array([[4800, 60], [3150, 470], [2650, 620], [2450, 1050], [1900, 1500],
                        [1250, 1830], [820, 1860], [660, 1720]], float)       # S-shaped dive
        # approach the tail tip from behind, along the spine's starting direction
        ctrl = np.vstack([way, P[0] - t0 * 300, P[0], P[0] + t0 * 120])
        pts = catmull_rom(ctrl, 400)
        # cut the spline where it reaches P[0]
        k = np.argmin(np.hypot(*(pts - P[0]).T)); fly = pts[:k]
        fly = resample(fly, 1.0)
        d0 = fly[1] - fly[0]; d0 /= np.linalg.norm(d0)
        pre = fly[0] - d0 * np.arange(L_FLY + 300, 0, -1)[:, None]
        route = np.vstack([pre, fly, P])
        self.s_p0 = len(pre) + len(fly)                 # route index of the tail tip
        self.h_start = len(pre) + int(np.argmin(np.hypot(*(fly - [3150, 470]).T)))
        return route, len(route) - 1

    def progress_table(self):
        x = np.linspace(0, 1, 4001)
        v = (1 - x) ** 1.7 * (1 - np.exp(-x / 0.06))
        p = np.cumsum(v); p = (p - p[0]) / (p[-1] - p[0])
        return x, p

    def head_index(self, t):
        creep = 60 * sstep(0, T_FLY0, t)                # the waiting head edges forward
        h0 = self.h_start + creep
        x = np.clip((t - T_FLY0) / (T_FLY1 - T_FLY0), 0, 1)
        p = np.interp(x, *self.prog)
        return h0 + (self.h_end - self.h_start - 60) * p


def catmull_rom(C, n):
    out = []
    C = np.vstack([C[0] * 2 - C[1], C, C[-1] * 2 - C[-2]])
    for i in range(1, len(C) - 2):
        p0, p1, p2, p3 = C[i - 1], C[i], C[i + 1], C[i + 2]
        t = np.linspace(0, 1, n, endpoint=False)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.vstack(out)


def resample(pts, step):
    s = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    u = np.arange(0, s[-1], step)
    return np.stack([np.interp(u, s, pts[:, 0]), np.interp(u, s, pts[:, 1])], 1)


def route_at(A, f):
    """position + unit tangent on the route at fractional index f (array)."""
    f = np.clip(f, 0, len(A.route) - 2)
    i = np.floor(f).astype(int); a = (f - i)[..., None]
    p = A.route[i] * (1 - a) + A.route[i + 1] * a
    j = np.clip(i + 6, 0, len(A.route) - 1); k = np.clip(i - 6, 0, len(A.route) - 1)
    tg = A.route[j] - A.route[k]; tg /= np.linalg.norm(tg, axis=-1, keepdims=True) + 1e-9
    return p, tg


def spine_frame(A, k):
    j, i = min(k + 6, A.N - 1), max(k - 6, 0)
    tg = A.P[j] - A.P[i]
    return A.P[k], np.arctan2(tg[1], tg[0])


def paste_rigid(dst, patch, box, anchor_f, ang_f, anchor_c, ang_c):
    """Rotate/translate a patch (cut from final-layout box) so anchor_f/ang_f -> anchor_c/ang_c."""
    x0, y0, x1, y1 = box
    im = Image.fromarray((patch * 255).astype(np.uint8))
    # rotate about the anchor (in patch coords), then translate
    ax, ay = anchor_f[0] - x0, anchor_f[1] - y0
    d = np.degrees(ang_c - ang_f)
    big = max(im.size) * 2 + 200
    canvas = Image.new('L', (big, big), 0)
    off = (big // 2 - int(round(ax)), big // 2 - int(round(ay)))
    canvas.paste(im, off)
    canvas = canvas.rotate(-d, resample=Image.BICUBIC, center=(big // 2, big // 2))
    tx, ty = int(round(anchor_c[0])) - big // 2, int(round(anchor_c[1])) - big // 2
    dst.paste(Image.new('L', canvas.size, 255), (tx, ty), canvas)


# ---------------------------------------------------------------- layers
def flight_mask(A, t):
    """dragon silhouette (L image, layout 2x) while it flies: discs on the route + rigid head/horns."""
    h = A.head_index(t)
    m = Image.new('L', (W2, H2), 0)
    dr = ImageDraw.Draw(m)
    s_t = min(h - L_FLY, A.s_p0)
    ell = h - s_t                                     # current body length
    u = np.arange(A.N - 1 - (A.k_head + 20), int(ell), 3)   # distance from the head
    pos, _ = route_at(A, h - u)
    k = np.clip((A.N - 1 - ell) / 250, 0, 1)          # taper fades as the body reaches full length
    rad = A.Rs[A.N - 1 - u] * (1 - k * (1 - sstep(0, 280, ell - u)))
    for (x, y), r in zip(pos, rad):
        if -200 < x < W2 + 200 and -200 < y < H2 + 200:
            dr.ellipse([x - r, y - r, x + r, y + r], fill=255)
    # head frame: spine sample k_head now vs. in the final pose
    pf, af = spine_frame(A, A.k_head)
    pc, tc = route_at(A, np.array([h - (A.N - 1) + A.k_head]))
    ac = np.arctan2(tc[0, 1], tc[0, 0])
    paste_rigid(m, A.head_patch, A.hbox, pf, af, pc[0], ac)
    if t < T_REV1:
        rr = 2200 * ease_out(T_REV0, T_REV1, t, 2)
        yy, xx = np.mgrid[0:H2:4, 0:W2:4]
        ex, ey = pc[0] + (A.eye_c - pf)            # roughly the eye's current position
        vis = np.clip((rr - np.hypot(xx - ex, yy - ey)) / 90, 0, 1)
        vis = np.kron(vis, np.ones((4, 4)))[:H2, :W2]
        m = Image.fromarray((np.asarray(m) * vis).astype(np.uint8))
    return m, (pf, af, pc[0], ac)


def grow_reach(A, t):
    RIM = 36.0
    return RIM * sstep(T_RIM0, T_RIM1, t) + ease_out(T_GROW0, T_GROW1, t, 2) * (A.grow_max - RIM + 2)


def landed_mask(A, t):
    grown = (A.grow_d > 0) & (A.grow_d <= grow_reach(A, t))
    base = (A.body > 0) & (A.grow_d == 0)
    m = np.where(base | grown, A.body, 0)
    return np.clip(m + A.horns, 0, 1)


def shade(A, mask, t, inflate):
    """glossy studio shading of a silhouette (float mask, layout 2x crop) -> RGB, alpha."""
    x0, y0, x1, y1 = A.bx0, A.by0, A.bx1, A.by1
    M = mask[y0:y1, x0:x1]
    ink = M > 0.5
    d = ndimage.distance_transform_edt(ink)
    d = ndimage.gaussian_filter(d, 2.0)
    half = ndimage.grey_dilation(d, size=(41, 41))
    half = np.maximum(ndimage.gaussian_filter(half, 14), 2.0)
    tt = np.clip(d / half, 0, 1)
    hgt = half * np.sqrt(1 - (1 - tt) ** 2) * 0.95 * inflate
    hgt = ndimage.gaussian_filter(hgt, 3.0)
    gy, gx = np.gradient(hgt)
    n = np.dstack([-gx, -gy, np.ones_like(hgt)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    # key light sweeps from far left to upper-left as the body inflates
    sw = sstep(T_INF0, T_INF1 + 0.35, t)
    b2 = np.sin(np.pi * np.clip((t - (T_BLINK2 - 0.3)) / 0.9, 0, 1)) ** 2
    az = np.radians(-170 + 45 * sw + 14 * sstep(3.3, DUR, t) + 30 * b2)
    key = np.array([np.cos(az) * 0.75, np.sin(az) * 0.75 - 0.35, 0.55]); key /= np.linalg.norm(key)
    V = np.array([0, 0, 1.0])
    ndv = np.clip(n[..., 2], 0, 1)
    r = 2 * n * ndv[..., None] - V
    rk = np.clip((r * key).sum(2), 0, 1)
    env = (0.24 + 0.60 * np.clip(-r[..., 1], 0, 1) ** 1.2       # bright studio ceiling
           + 0.35 * np.clip(r[..., 0], 0, 1) ** 2              # bounce from the right
           + 1.05 * rk ** 1.5 + 0.9 * rk ** 9)                   # broad grey softbox + hot core
    fres = 0.05 + 0.95 * (1 - ndv) ** 4
    hl = np.clip((n * ((key + V) / np.linalg.norm(key + V))).sum(2), 0, 1) ** 70
    ndl = np.clip((n * key).sum(2), 0, 1)
    val = 0.07 * (0.4 + 0.6 * ndl) + (0.04 + fres) * env * 0.66 + 0.32 * hl
    rim = (1 - ndv) ** 3 * np.clip(-(n[..., 0] * 0.6 + n[..., 1] * 0.8) + 0.2, 0, 1) * 0.30
    flat = INK.mean()
    val = flat + (val - flat) * inflate
    rgb = np.dstack([val + rim * 1.0, val * 0.985 + rim * 0.86, val * 0.97 + rim * 0.70])
    rgb = np.where(inflate > 0, rgb, INK[None, None, :])
    return np.clip(rgb, 0, 1), M


def eye_layer(A, t, frame):
    """eye diamond + glow as (rgb, alpha) on the full layout, following the head frame."""
    pf, af, pc, ac = frame
    eb = A.ebox
    m = Image.new('L', (W2, H2), 0)
    blink = max(0.04, sstep(T_EYE0, T_EYE1, t))
    for tb in (T_BLINK, T_BLINK2):
        if tb <= t <= tb + 0.16:
            blink = max(0.08, abs(np.cos(np.pi * (t - tb) / 0.16)))
    patch = A.eye_patch
    if blink < 1:
        im = Image.fromarray((patch * 255).astype(np.uint8))
        cy = A.eye_c[1] - eb[1]
        hh = im.size[1]
        sq = im.resize((im.size[0], max(1, int(hh * blink))), Image.BICUBIC)
        im = Image.new('L', im.size, 0); im.paste(sq, (0, int(cy - cy * blink)))
        patch = np.asarray(im).astype(np.float32) / 255
    paste_rigid(m, patch, eb, pf, af, pc, ac)
    e = np.asarray(m).astype(np.float32) / 255
    core = ndimage.distance_transform_edt(e > 0.5)
    hot = np.clip(core / max(core.max(), 1), 0, 1) ** 1.5
    rgb = EYE[None, None] * (1 - hot[..., None]) + EYE_HOT[None, None] * hot[..., None]
    glow_a = (0.55 + 0.6 * np.exp(-((t - T_EYE1) / 0.12) ** 2)) if t < T_INF1 else 0.35 + 0.35 * np.exp(-((t - T_BLINK2 - 0.2) / 0.15) ** 2)
    eim = Image.fromarray((e * 255).astype(np.uint8))
    glow = np.asarray(eim.filter(ImageFilter.GaussianBlur(22))).astype(np.float32) / 255 * glow_a
    op = np.exp(-((t - T_EYE1) / 0.18) ** 2) if t < 1.0 else 0.0       # wide halo as the eye opens
    if op > 0.01:
        glow = glow + np.asarray(eim.filter(ImageFilter.GaussianBlur(70))).astype(np.float32) / 255 * 9.0 * op
    return e, rgb, glow


def camera(t):
    x = np.clip((t - 3.4) / 2.2, 0, 1)
    # gentle push all along, then ~3 %/s through the hold (velocity eases in, no kink)
    z = 0.975 + 0.015 * (t / DUR) + 0.07 * (x - 0.15 * (1 - np.exp(-x / 0.15)))
    damp = 1 - sstep(3.6, 5.2, t)
    dx = 6 * np.sin(1.3 * t + 0.4) * damp + 15
    dy = 4 * np.sin(0.9 * t + 1.1) * damp
    rot = np.radians(0.18 * np.sin(0.7 * t)) * damp
    return z, dx, dy, rot


def background():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot((xx - 0.5 * W) / (0.75 * W), (yy - 0.42 * H) / (0.75 * H))
    hi, lo = np.array([0xFE, 0xFD, 0xFC]) / 255, np.array([0xF2, 0xF0, 0xED]) / 255
    k = np.clip(r, 0, 1) ** 1.6
    return hi * (1 - k[..., None]) + lo * k[..., None]


BG = None


def render(A, t):
    """one frame at time t -> float RGB (H, W, 3)."""
    global BG
    if BG is None: BG = background()
    rgb = np.zeros((H2, W2, 3), np.float32)
    alpha = np.zeros((H2, W2), np.float32)
    inflate = ease_out(T_INF0, T_INF1, t, 2)

    # floor shadow (only as strong as the 3D look)
    if inflate > 0:
        x0, y0, x1, y1 = A.bx0, A.by0, A.bx1, A.by1
        yy, xx = np.mgrid[0:H2, 0:W2]
        cx, base_y = A.foot_x + 30, A.foot_y - 4
        floor = (np.exp(-(((xx - cx) / 250) ** 2 + ((yy - base_y - 8) / 42) ** 2)) * 0.20
                 + np.exp(-(((xx - cx) / 120) ** 2 + ((yy - base_y) / 9) ** 2)) * 0.25)   # contact
        sil = np.zeros((H2, W2), np.float32); sil[y0:y1, x0:x1] = A.full[y0:y1, x0:x1]
        soft = ndimage.gaussian_filter(np.roll(sil, (40, 18), (0, 1))[::4, ::4], 12)
        soft = np.kron(soft, np.ones((4, 4), np.float32))[:H2, :W2] * 0.18
        sh = np.clip(floor + soft, 0, 0.5) * inflate
        rgb[:] = 0; alpha = sh.astype(np.float32)      # black at alpha=sh

    # dragon
    if t < T_FLY1:
        m, frame = flight_mask(A, t)
        M = np.asarray(m).astype(np.float32) / 255
        if t >= T_RIM0:
            g = grow_reach(A, t)
            M = np.maximum(M, np.where((A.grow_d > 0) & (A.grow_d <= g), A.body, 0))
        a = M
        rgb = rgb * (1 - a[..., None]) + INK * a[..., None]
        alpha = alpha * (1 - a) + a
    else:
        frame = (*spine_frame(A, A.k_head), *spine_frame(A, A.k_head))
        M = landed_mask(A, t)
        c, Mc = shade(A, M, t, inflate)
        x0, y0, x1, y1 = A.bx0, A.by0, A.bx1, A.by1
        a = Mc
        rgb[y0:y1, x0:x1] = rgb[y0:y1, x0:x1] * (1 - a[..., None]) + c * a[..., None]
        alpha[y0:y1, x0:x1] = alpha[y0:y1, x0:x1] * (1 - a) + a

    # eye + glow
    if True:
        e, ergb, glow = eye_layer(A, t, frame)
        rgb = rgb * (1 - e[..., None]) + ergb * e[..., None]
        alpha = alpha * (1 - e) + e
        add_glow = glow

    # wordmark
    lx0, lx1 = A.letter_boxes[0][0] - 120, A.letter_boxes[-1][2] + 160
    xw = lx0 + (lx1 - lx0) * ease_out(T_WIPE0, T_WIPE1, t, 2.2)
    for i, (Lm, box) in enumerate(zip(A.letters, A.letter_boxes)):
        x0, y0, x1, y1 = box
        if xw <= x0 - 1: continue
        kc = np.clip((xw - (x0 + x1) / 2 + 180) / 360, 0, 1)
        dy = int(round((1 - (1 - (1 - kc) ** 3)) * 30))
        cols = np.clip((xw - np.arange(x0, x1)) / 110, 0, 1)
        a = np.zeros_like(alpha)
        a[y0 + dy:y1 + dy, x0:x1] = Lm[y0:y1, x0:x1] * cols[None, :]
        rgb = rgb * (1 - a[..., None]) + LETTER * a[..., None]
        alpha = alpha * (1 - a) + a

    # 2x -> 1x (box) then camera affine at 1x
    pre = np.dstack([rgb, alpha])                          # rgb is premultiplied-ish (blended over 0)
    small = pre.reshape(H, 2, W, 2, 4).mean((1, 3))
    z, dx, dy, rot = camera(t)
    small = cam_warp(small, z, dx, dy, rot)
    out = BG * (1 - small[..., 3:4]) + small[..., :3]
    if True:
        g = cam_warp(add_glow.reshape(H, 2, W, 2).mean((1, 3))[..., None], z, dx, dy, rot)[..., 0]
        out = out + (EYE[None, None] * 1.0) * g[..., None] * (1 - out) * 1.6
    return np.clip(out, 0, 1)


def cam_warp(img, z, dx, dy, rot):
    c, s = np.cos(rot) / z, np.sin(rot) / z
    cx, cy = W / 2, H / 2
    # output (x,y) <- input: inv(R*z) * (p - c - d) + c
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    px, py = xx - cx - dx, yy - cy - dy
    ix = c * px + s * py + cx
    iy = -s * px + c * py + cy
    out = np.empty_like(img)
    for ch in range(img.shape[2]):
        out[..., ch] = ndimage.map_coordinates(img[..., ch], [iy, ix], order=1, mode='constant', cval=0)
    return out


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
    f = f + (rg.random(f.shape) + rg.random(f.shape) - 1.0) / 255      # triangular dither vs banding
    Image.fromarray((np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--times', type=float, nargs='*')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--fps', type=int, default=60)
    ap.add_argument('--sub', type=int, default=1, help='motion-blur sub-frames for moving frames')
    ap.add_argument('--out', default='stills/beats')
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.all:
        n = int(round(DUR * a.fps))
        jobs = [(i, i / a.fps, a.sub if i / a.fps < T_INF1 + 0.1 else 1, a.fps, f'{a.out}/f{i:05d}.png') for i in range(n)]
    else:
        jobs = [(i, t, a.sub, a.fps, f'{a.out}/t{t:05.2f}.png') for i, t in enumerate(a.times)]
    with Pool(a.jobs) as p:
        for k, o in enumerate(p.imap(work, jobs)):
            if k % 20 == 0 or not a.all: print(o, flush=True)

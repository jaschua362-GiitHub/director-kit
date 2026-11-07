"""Hold the Note - grain effects E1 (edge shedding), E2 (bands re-sharpening), E3 (the release).

Local, free, deterministic (fixed seeds).  numpy + cv2 + ffmpeg (project-bundled) only.
Physics: g = 9.81 m/s^2, 24 fps, 180 deg shutter (1/48 s), 48 frames, wind 2-4 m/s down-gorge.
Usage:  python grain_fx.py e1s05 | e1s01 | e3 | e2 | sheet | all
"""
import os, sys, json, subprocess
import numpy as np
import cv2

ROOT = r"<LAB>"
T20 = ROOT + r"\experiments\TEST-020-hold-the-note"
FIN = T20 + r"\startframes\final"
RET = T20 + r"\startframes\returns"
FX = T20 + r"\effects"
TESTS = FX + r"\tests"
PLATES = FX + r"\plates"
FFMPEG = ROOT + r"\experiments\TEST-001\tools\python-media\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
SCRATCH = os.environ.get("FX_SCRATCH", r"C:\Users\IQCOM~1\AppData\Local\Temp\claude\9d7fd9415a8b3357\c732e42f-b6ac-446c-b1be-febef19af77c\scratchpad")
SHEETDIR = os.path.join(SCRATCH, "sheet_frames")
LOGJSON = os.path.join(SCRATCH, "fx_log.json")

FPS, NF, G, SHUT = 24, 48, 9.81, 1.0 / 48
SHEET_IDX = [0, 10, 19, 29, 38, 47]          # t = 0, 0.4, 0.8, 1.2, 1.6, 1.96 s
for d in (TESTS, PLATES, SHEETDIR):
    os.makedirs(d, exist_ok=True)


# ----------------------------------------------------------------- helpers
def log_put(key, val):
    d = {}
    if os.path.exists(LOGJSON):
        d = json.load(open(LOGJSON))
    d[key] = val
    json.dump(d, open(LOGJSON, "w"), indent=1)


def load_rgb(path):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None:
        raise FileNotFoundError(path)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32)


def save_rgb(path, im):
    cv2.imwrite(path, cv2.cvtColor(np.clip(im, 0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR))


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def noise1(n, scale, rng):
    g = rng.standard_normal(max(4, int(n / scale) + 4)).astype(np.float32)
    x = np.linspace(0, len(g) - 3, n)
    return np.interp(x, np.arange(len(g)), g)


def noise2(h, w, scale, rng):
    gh, gw = int(h / scale) + 4, int(w / scale) + 4
    g = rng.standard_normal((gh, gw)).astype(np.float32)
    n = cv2.resize(g, (gw * scale, gh * scale), interpolation=cv2.INTER_CUBIC)
    return n[:h, :w]


def conform(img, W, H):
    """centre-crop to exact ratio then Lanczos to size"""
    h, w = img.shape[:2]
    r, t = w / h, W / H
    if r > t:
        nw = int(round(h * t)); x0 = (w - nw) // 2; img = img[:, x0:x0 + nw]
    else:
        nh = int(round(w / t)); y0 = (h - nh) // 2; img = img[y0:y0 + nh]
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_LANCZOS4)


def write_video(name, frame_fn, W, H):
    out = os.path.join(TESTS, name + ".mp4")
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", "24", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
           "-pix_fmt", "yuv420p", "-r", "24", "-frames:v", str(NF), out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(NF):
        fr = np.clip(frame_fn(k), 0, 255).astype(np.uint8)
        assert fr.shape == (H, W, 3), fr.shape
        p.stdin.write(fr.tobytes())
        if k in SHEET_IDX:
            cv2.imwrite(os.path.join(SHEETDIR, f"{name}_{SHEET_IDX.index(k)}.jpg"),
                        cv2.cvtColor(fr, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    p.stdin.close()
    p.wait()
    return out


# ---------------------------------------------------- capsule (streak) renderer
SIG_EDGES = np.array([0.3, 0.9, 1.8, 3.6, 7.2, 14.4])
SIG_BIN = np.array([0.0, 0.6, 1.2, 2.4, 4.8, 9.6, 19.2])


def draw_grains(bg, P0, P1, D0, D1, col, alpha, sigma, asp=None, ang=None):
    """Motion-blurred grains: capsule from P0 to P1, diameters D0->D1 (px), exposure alpha
    (already d/(d+L)), colour, defocus sigma (px).  Premultiplied, blurred per defocus bin."""
    H, W = bg.shape[:2]
    out = bg.copy()
    if len(P0) == 0:
        return out
    bi = np.digitize(sigma, SIG_EDGES)
    for b in range(len(SIG_BIN)):
        sel = np.where(bi == b)[0]
        if len(sel) == 0:
            continue
        C = np.zeros((H, W, 3), np.uint8)
        A = np.zeros((H, W), np.uint8)
        for i in sel:
            a = float(alpha[i])
            c = tuple(int(v) for v in np.clip(col[i] * a, 0, 255))
            p0 = (int(P0[i, 0] * 16), int(P0[i, 1] * 16)); p1 = (int(P1[i, 0] * 16), int(P1[i, 1] * 16))
            ai = 1.0 if asp is None else float(asp[i]); an = 0.0 if ang is None else float(ang[i])
            th = max(1, int(round(0.5 * (D0[i] + D1[i]) * min(1.0, ai))))
            for im, cc in ((C, c), (A, int(a * 255))):
                cv2.line(im, p0, p1, cc, th, cv2.LINE_AA, 4)
                cv2.ellipse(im, p0, (int(round(D0[i] * 8 * ai)), int(round(D0[i] * 8))), an, 0, 360, cc, -1, cv2.LINE_AA, 4)
                cv2.ellipse(im, p1, (int(round(D1[i] * 8 * ai)), int(round(D1[i] * 8))), an + 40, 0, 360, cc, -1, cv2.LINE_AA, 4)
        Cf, Af = C.astype(np.float32), A.astype(np.float32)[..., None] / 255
        if SIG_BIN[b] > 0:
            Cf = cv2.GaussianBlur(Cf, (0, 0), float(SIG_BIN[b]))
            Af = cv2.GaussianBlur(Af, (0, 0), float(SIG_BIN[b]))[..., None]
        out = out * (1 - Af) + Cf
    return out


def luma(im):
    return im[..., 0] * 0.299 + im[..., 1] * 0.587 + im[..., 2] * 0.114


# ==================================================================== E1 shot 5
E1S5 = {
    # ppm measured on the boot sole in the plate (sole 0.29 m): H sole ~104 px, V sole ~125 px
    "H": dict(plate="S05H_a01.png", ppm=360.0, sole_px=104, ysure=520, xspan=(330, 1060), xs=900, ymin=540, ymax=700),
    "V": dict(plate="S05V_a01.png", ppm=430.0, sole_px=125, ysure=640, xspan=(170, 920), xs=640, ymin=660, ymax=800),
}
Z0 = 4.7          # camera below the ribbon, m
ZF = 4.7          # focus plane (ribbon)
F_MM, N_STOP = 24.0, 5.6
WIND = 3.0        # m/s mean, gusting 2-4
TAU_R = 3.0       # s, response time of a pebble to the wind -> a_x = wind / TAU_R


def lower_edge(plate, x0, x1, ysure, ymax):
    g = luma(plate)
    dark = (g < 130).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    edge = np.zeros(x1 - x0, np.float32)
    for i, x in enumerate(range(x0, x1)):
        col = dark[ysure:ymax, x]
        nz = np.where(col == 0)[0]
        edge[i] = ysure + (nz[0] if len(nz) else ymax - ysure) - 1
    return cv2.medianBlur(edge.reshape(1, -1), 5).ravel() if False else np.convolve(np.pad(edge, 3, mode="edge"), np.ones(7) / 7, "valid")


def e1_s5(fmt, write=True):
    cfg = E1S5[fmt]
    plate = load_rgb(os.path.join(FIN, cfg["plate"]))
    H, W = plate.shape[:2]
    rng = np.random.default_rng(5000 + (fmt == "V"))
    ppm = cfg["ppm"]; f_px = ppm * Z0
    x0, x1 = cfg["xspan"]
    n = x1 - x0
    edge = lower_edge(plate, x0, x1, cfg["ysure"], cfg["ymax"])
    cx, cy = 0.5 * (x0 + x1), float(edge.mean()) - 380.0    # looks up at an angle: motion mostly DOWN the frame, mild outward spread
    dmax = 0.19 * ppm                                     # the bite: ~15-19 cm deep (clearly readable)
    xs = np.arange(x0, x1, dtype=np.float32)
    u = (xs - x0) / n
    env = np.sin(np.pi * u) ** 0.7
    rag = 0.62 + 0.38 * np.clip(0.6 * noise1(n, 14, rng) + 0.5 * noise1(n, 45, rng), -1.5, 1.5) / 1.2
    D = np.clip(dmax * env * rag, 0, dmax * 1.05)
    dist = np.abs(xs - cfg["xs"]) / ppm                  # m along the ribbon from his toe
    onset = 0.22 + 0.42 * dist + 0.10 * noise1(n, 20, rng)
    onset = np.clip(onset, 0.18, None)
    dur = 0.25 + 0.10 * np.abs(noise1(n, 30, rng))
    gn = noise2(H, W, 6, rng) * 4.5 + noise2(H, W, 14, rng) * 3.0   # grain-scale ragged front (px)
    yy = np.arange(H, dtype=np.float32)[:, None]
    ecol = np.full(W, -1e4, np.float32); ecol[x0:x1] = edge
    Dfull = np.zeros(W, np.float32); Dfull[x0:x1] = D
    onf = np.full(W, 9.0, np.float32); onf[x0:x1] = onset
    durf = np.ones(W, np.float32); durf[x0:x1] = dur
    inspan = np.zeros(W, bool); inspan[x0:x1] = True

    def mask_at(t):
        depth = Dfull * smoothstep((t - onf) / durf)                         # per column (px)
        m = ((ecol[None, :] - yy) < (depth[None, :] + gn)) & (yy <= ecol[None, :] + 3) & inspan[None, :] \
            & (depth[None, :] > 0.5) & ((ecol[None, :] - yy) > -4)
        return m

    # sky fill: smooth sky from just below the edge, no dark ribbon pulled in
    blur = cv2.GaussianBlur(plate, (0, 0), 7)
    skyrow = np.zeros((W, 3), np.float32)
    for x in range(x0, x1):
        skyrow[x] = blur[min(H - 1, int(edge[x - x0]) + 16), x]
    skyrow[x0:x1] = cv2.GaussianBlur(skyrow[x0:x1][None], (0, 0), 14)[0]
    sky = np.broadcast_to(skyrow[None], (H, W, 3)).copy()
    sky += rng.standard_normal((H, W, 1)).astype(np.float32) * 1.2

    # emission: every newly eroded pixel releases grains (A_grain = (10 mm * ppm)^2)
    A_g = (0.010 * ppm) ** 2
    times = [k / FPS for k in range(NF + 1)]
    masks = [mask_at(t) for t in times]
    pb = cv2.erode(cv2.GaussianBlur(plate, (0, 0), 1.0), np.ones((9, 9), np.uint8))      # darkest tones of the ribbon
    G_t, G_x, G_y, G_d, G_c = [], [], [], [], []
    prev = np.zeros((H, W), bool)
    for k in range(1, NF + 1):
        new = masks[k] & ~prev
        prev = masks[k]
        ys, xs_ = np.nonzero(new)
        if len(ys) == 0:
            continue
        cnt = int(len(ys) / A_g)
        if cnt < 1:
            continue
        pick = rng.choice(len(ys), cnt, replace=False if cnt <= len(ys) else True)
        G_t.append(times[k - 1] + rng.random(cnt) / FPS)
        G_x.append(xs_[pick] + rng.random(cnt)); G_y.append(ys[pick] + rng.random(cnt))
        G_c.append(pb[ys[pick], xs_[pick]])
    # the first stragglers: a few single grains drop from the roughening edge ahead of the boot (0-0.3 s)
    for _ in range(7):
        x = cfg["xs"] + rng.uniform(-0.45, 0.2) * ppm * (1 if fmt == "H" else -1)
        x = float(np.clip(x, x0 + 20, x1 - 20)); y = edge[int(x) - x0] - rng.uniform(1, 8)
        G_t.append(np.array([rng.uniform(0.02, 0.30)])); G_x.append(np.array([x])); G_y.append(np.array([y]))
        G_c.append(pb[[int(y)], [int(x)]])
    # tail-off: stragglers after 1.6 s
    for _ in range(14):
        x = float(rng.uniform(x0 + 40, x1 - 40)); y = edge[int(x) - x0] - rng.uniform(1, 30)
        G_t.append(np.array([rng.uniform(1.2, 1.95)])); G_x.append(np.array([x])); G_y.append(np.array([y]))
        G_c.append(pb[[int(y)], [int(x)]])
    gt = np.concatenate(G_t); gx = np.concatenate(G_x); gy = np.concatenate(G_y); gc = np.concatenate(G_c)
    cl = np.where(rng.random(len(gt)) < 0.16)[0]                                   # small clusters: a grain with 1-2 neighbours
    for rep_ in range(2):
        sub = cl[rng.random(len(cl)) < (1.0 if rep_ == 0 else 0.4)]
        gt = np.concatenate([gt, gt[sub] + rng.uniform(0, 0.02, len(sub))])
        gx = np.concatenate([gx, gx[sub] + rng.uniform(-2.2, 2.2, len(sub)) * 0.010 * ppm])
        gy = np.concatenate([gy, gy[sub] + rng.uniform(-2.2, 2.2, len(sub)) * 0.010 * ppm])
        gc = np.concatenate([gc, gc[sub]])
    ng = len(gt)
    dia = np.exp(rng.normal(np.log(0.0105), 0.30, ng)).clip(0.008, 0.015)        # 8-15 mm
    z0 = Z0 + rng.uniform(-0.04, 0.04, ng)                                        # ribbon thickness
    X0 = (gx - cx) * z0 / f_px; Y0 = (gy - cy) * z0 / f_px                        # unproject at z0
    vz = rng.normal(0.0, 0.15, ng)                                                # m/s, small
    gust = WIND + 0.8 * np.sin(2 * np.pi * gt / 1.3 + 1.0)
    ax = gust / TAU_R * rng.uniform(0.7, 1.3, ng)                                 # m/s^2 down-gorge (+x on screen)
    colv = np.clip(gc.astype(np.float32) * 0.85, 12, 58)                          # darkest ribbon tones, always darker than the sky
    asp = rng.uniform(0.55, 1.0, ng); ang = rng.uniform(0, 180, ng)               # irregular pebbles, random orientation
    coc_k = (F_MM / N_STOP * 1e-3) * f_px / ZF                                      # px

    def state(t):
        tau = t - gt
        act = tau >= 0
        tc = np.where(act, tau, 0.0)
        z = z0 - 0.5 * G * tc ** 2 - vz * tc
        X = X0 + 0.5 * ax * tc ** 2
        zc = np.maximum(z, 0.05)
        sx = cx + f_px * X / zc; sy = cy + f_px * Y0 / zc
        return act & (z > 0.10), sx, sy, f_px * dia / zc, zc

    def frame(k):
        t = k / FPS
        m = mask_at(t)
        mf = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.9)[..., None]
        base = plate * (1 - mf) + sky * mf
        a0, sx0, sy0, d0, z_a = state(t)
        a1, sx1, sy1, d1, z_b = state(t + SHUT)
        ok = a0 & a1 & (sx0 > -200) & (sx0 < W + 200) & (sy0 > -200) & (sy0 < H + 200)
        # keep grains that are on screen at either end
        ok &= ((sx0 > -60) & (sx0 < W + 60) & (sy0 > -60) & (sy0 < H + 60)) | ((sx1 > -60) & (sx1 < W + 60) & (sy1 > -60) & (sy1 < H + 60))
        idx = np.where(ok)[0]
        if len(idx) == 0:
            return base
        P0 = np.stack([sx0[idx], sy0[idx]], 1); P1 = np.stack([sx1[idx], sy1[idx]], 1)
        L = np.hypot(*(P1 - P0).T)
        dm = 0.5 * (d0[idx] + d1[idx])
        alpha = np.clip(3.2 * dm / (dm + L), 0.45, 0.98)
        zm = 0.5 * (z_a[idx] + z_b[idx])
        sig = 0.5 * coc_k * np.abs(zm - ZF) / zm
        sig = np.maximum(sig, 0.5)
        return draw_grains(base, P0, P1, d0[idx], d1[idx], colv[idx], alpha, sig, asp[idx], ang[idx] + 180 * (t * 3 + idx * 0.37) % 180)

    log_put(f"E1-s05-{fmt}", dict(ppm=ppm, sole_px=cfg["sole_px"], f_px=round(f_px, 1), grain_px_at_ribbon=round(0.010 * ppm, 2),
                                  grain_ratio=f"1:{cfg['sole_px'] / (0.010 * ppm):.0f}" if False else f"1:{0.29 / 0.010:.0f} (sole 0.29 m / grain 10 mm)",
                                  bite_depth_px=round(dmax, 1), bite_span_m=round(n / ppm, 2), n_grains=int(ng), cx=cx, cy=round(cy, 1)))
    if write:
        write_video(f"E1-s05-{fmt}", frame, W, H)
    return frame


# ==================================================================== E1 shot 1 (trickle)
E1S1 = {
    "H": dict(plate="S01H_a01.png", ppm=1480.0, sole_px=430,
              lip=[(0, 890), (100, 838), (220, 800), (330, 760), (430, 726), (520, 700), (570, 685)], xr=(60, 540)),
    "V": dict(plate=None, ppm=655.0, sole_px=190,
              lip=[(0, 1135), (100, 1110), (200, 1062), (300, 1015), (400, 968), (500, 926), (600, 890), (700, 846), (800, 802)],
              xr=(150, 800)),
}


def e1_s1(fmt, write=True):
    cfg = E1S1[fmt]
    pname = cfg["plate"] or ("S01V_a02.png" if os.path.exists(os.path.join(FIN, "S01V_a02.png")) else "S01V_a01.png")
    plate = load_rgb(os.path.join(FIN, pname))
    H, W = plate.shape[:2]
    rng = np.random.default_rng(1000 + (fmt == "V"))
    lx = np.array([p[0] for p in cfg["lip"]], float); ly = np.array([p[1] for p in cfg["lip"]], float)
    ng = 11                                                       # ~5 per second
    tt = np.sort(0.08 + (np.arange(ng) + rng.uniform(0.0, 0.8, ng)) * (1.75 / ng))
    # fall where the background below the lip is brightest (mist / air): dark specks against light
    gl = luma(cv2.GaussianBlur(plate, (0, 0), 6))
    cand = np.arange(cfg["xr"][0], cfg["xr"][1])
    yl = np.interp(cand, lx, ly).astype(int)
    bright = np.array([gl[min(H - 2, y + 30):min(H, y + 420), max(0, x - 12):x + 12].mean() for x, y in zip(cand, yl)])
    good = cand[bright >= np.percentile(bright, 55)]
    xg = rng.choice(good, ng) + rng.uniform(-3, 3, ng)
    pb = cv2.erode(cv2.GaussianBlur(plate, (0, 0), 1.2), np.ones((7, 7), np.uint8))
    ppm0 = cfg["ppm"]
    ppm_x = ppm0 * np.clip(1.12 - 0.00045 * xg, 0.7, 1.3) if fmt == "H" else ppm0 * np.clip(1 + (370 - xg) * 0.0012, 0.6, 1.5)
    dia = rng.uniform(0.009, 0.015, ng)
    dpx = dia * ppm_x * (1.35 if fmt == 'V' else 1.0)
    y_lip = np.interp(xg, lx, ly)
    ax = (WIND + 0.7 * np.sin(2 * np.pi * tt / 1.3)) / TAU_R * rng.uniform(0.7, 1.3, ng)
    vx0 = rng.uniform(0.05, 0.25, ng)                              # rolled off the lip, a gentle push
    col = np.zeros((ng, 3), np.float32)
    for i in range(ng):
        c = pb[int(np.clip(y_lip[i] - dpx[i] * 0.5, 0, H - 1)), int(xg[i])]
        col[i] = np.clip(c * 0.7, 10, 42)
    HOLD = 0.0417     # one frame sitting on the lip

    def pos(t):
        s = t - tt
        roll = np.clip(s + 2 / FPS, 0, 2 / FPS) / (2 / FPS) * 0.0              # (kept for clarity)
        tau = np.maximum(s - HOLD, 0.0)
        # before drop: sits on lip, 2-frame roll-in of ~0.3 px/frame toward the edge
        pre = np.clip((s + 2 / FPS) / (2 / FPS), 0, 1)
        x = xg + (tau * vx0 + 0.5 * ax * tau ** 2) * ppm_x - (1 - pre) * 0.0
        y = y_lip - dpx * 0.5 + 0.5 * G * tau ** 2 * ppm_x
        return (s > -2 / FPS), x, y

    def frame(k):
        t = k / FPS
        a0, x0_, y0_ = pos(t); a1, x1_, y1_ = pos(t + SHUT)
        ok = a0 & (y0_ < H + 60) & (x0_ < W + 60)
        idx = np.where(ok)[0]
        if len(idx) == 0:
            return plate
        P0 = np.stack([x0_[idx], y0_[idx]], 1); P1 = np.stack([x1_[idx], y1_[idx]], 1)
        L = np.hypot(*(P1 - P0).T)
        alpha = np.clip(1.6 * dpx[idx] / (dpx[idx] + L), 0.55, 0.98)
        # a grain sitting on the lip is fully opaque
        alpha = np.where(L < 0.5, 0.98, alpha)
        sig = np.full(len(idx), 0.7)
        return draw_grains(plate, P0, P1, dpx[idx], dpx[idx], col[idx], alpha, sig)

    log_put(f"E1-s01-{fmt}", dict(plate=pname, ppm=ppm0, sole_px=cfg["sole_px"], grain_px=[round(float(v), 1) for v in (0.010 * ppm0,)],
                                  grain_ratio="1:29 (sole 0.29 m / grain 10 mm)", grains_per_s=round(ng / 2.0, 1),
                                  fall_exit_s=round(float(np.sqrt(2 * (H - y_lip.mean()) / (ppm0 * G))), 2)))
    if write:
        write_video(f"E1-s01-{fmt}", frame, W, H)
    return frame


# ==================================================================== E3 shot 14 (the release)
E3 = {
    "H": dict(plate="S14H_a01.png", p14="P14H-a01.png",
              centre=[(470, 697), (850, 670), (1000, 662), (1300, 630), (1665, 578)], hw=[48, 45, 42, 40, 36],
              ppm_sheet=10.0, woman_px=290, thr=88),
    "V": dict(plate="S14V_a01.png", p14="P14V-a01.png",
              centre=[(150, 975), (350, 920), (500, 880), (700, 835), (940, 765)], hw=[75, 70, 65, 60, 50],
              ppm_sheet=7.2, woman_px=560, thr=88),
}
L_FADE = 8.0      # m of fall for contrast to fall by 1/e into the haze (gone within ~40 m)


def band_mask(plate, cfg):
    H, W = plate.shape[:2]
    cp = np.array(cfg["centre"], float)
    xs = np.arange(int(cp[0, 0]), int(cp[-1, 0]))
    yc = np.interp(xs, cp[:, 0], cp[:, 1]); hw = np.interp(xs, cp[:, 0], cfg["hw"])
    corr = np.zeros((H, W), np.uint8)
    for x, y, h in zip(xs, yc, hw):
        corr[int(y - h):int(y + h), x] = 1
    g = luma(cv2.GaussianBlur(plate, (0, 0), 1.0))
    m = ((g < cfg["thr"]) & (corr > 0)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    m = (lab == big).astype(np.uint8)
    # fill holes column-wise between top and bottom
    out = np.zeros_like(m)
    top = np.full(W, -1); bot = np.full(W, -1)
    for x in range(W):
        ys = np.nonzero(m[:, x])[0]
        if len(ys):
            top[x], bot[x] = ys[0], ys[-1]
    return top, bot


def build_end_plate(plate, top, bot, x0, x1, rng):
    """mirror-fill the ribbon band from the background above / below, then a soft mist pass."""
    H, W = plate.shape[:2]
    xs = np.arange(x0, x1)
    t = np.convolve(np.pad(top[x0:x1].astype(float), 6, mode="edge"), np.ones(13) / 13, "valid") - 4
    b = np.convolve(np.pad(bot[x0:x1].astype(float), 6, mode="edge"), np.ones(13) / 13, "valid") + 4
    out = plate.copy()
    pb = cv2.GaussianBlur(plate, (0, 0), 2.0)
    m = np.zeros((H, W), np.float32)
    for i, x in enumerate(xs):
        yt, yb = int(t[i]), int(b[i])
        th = yb - yt
        for y in range(yt, yb + 1):
            d = y - yt                      # distance from top edge
            ydn = yb - y                    # distance from bottom edge
            su = plate[max(0, yt - 1 - d), x]
            sd = plate[min(H - 1, yb + 1 + ydn), x]
            w = (y - yt) / max(1, th)       # 0 at top -> 1 at bottom
            out[y, x] = su * (1 - smoothstep(w * 1.4 - 0.2)) + sd * smoothstep(w * 1.4 - 0.2)
            m[y, x] = 1
    # soft mist pass: blend the filled band toward a blurred, haze-lifted version, feathered
    mf = cv2.GaussianBlur(m, (0, 0), 3.0)[..., None]
    haze = cv2.GaussianBlur(plate, (0, 0), 14)
    mist = out * 0.75 + haze * 0.25
    mist = mist + (np.array([205, 208, 215], np.float32) - mist) * 0.10
    res = out * (1 - mf * 0.7) + mist * (mf * 0.7)
    res += rng.standard_normal((H, W, 1)).astype(np.float32) * 1.0 * mf
    return np.clip(res, 0, 255), m


def e3(fmt, write=True):
    cfg = E3[fmt]
    plate = load_rgb(os.path.join(FIN, cfg["plate"]))
    H, W = plate.shape[:2]
    rng = np.random.default_rng(14000 + (fmt == "V"))
    top, bot = band_mask(plate, cfg)
    valid = np.where(top >= 0)[0]
    x0, x1 = int(valid.min()), int(valid.max()) + 1
    # which end plate: Codex return if pixel-aligned, else local mirror-fill inpaint
    ret = os.path.join(RET, cfg["p14"])
    used = "local mirror-fill inpaint + mist pass"
    end = None
    if os.path.exists(ret):
        r = conform(load_rgb(ret), W, H)
        mk = np.ones((H, W), bool)
        for x in range(x0, x1):
            mk[max(0, top[x] - 12):bot[x] + 13, x] = False
        mk[:, :x0 - 20] = mk[:, x1 + 20:] = False
        d = np.abs(luma(cv2.GaussianBlur(r, (0, 0), 2)) - luma(cv2.GaussianBlur(plate, (0, 0), 2)))[mk]
        diff = float(d.mean())
        used_try = f"P14 return: mean |diff| outside ribbon = {diff:.1f} levels"
        if diff < 6.0:
            end, used = r, used_try + " -> used"
        else:
            used = used_try + " -> NOT pixel-aligned, rejected; " + used
    if end is None:
        end, _ = build_end_plate(plate, top, bot, x0, x1, rng)
    save_rgb(os.path.join(PLATES, f"P14{fmt}_end.png"), end)

    # scale: measured from the woman (1.65 m) in the plate, and the sheet's design scale
    ppm_woman = cfg["woman_px"] / 1.65
    thick = (bot - top).astype(float)
    xb_ = int(0.5 * (x0 + x1))
    ppm_ribbon = float(np.median(thick[xb_ - 60:xb_ + 60]))             # ribbon width 1.0 m at mid-span
    ppm_span40 = (x1 - x0) / 40.0                                        # if the span between the collars were ~40 m
    ppm = ppm_ribbon
    # dark ribbon pixels
    xb = 0.5 * (x0 + x1)                                    # the bite, mid-span
    span = (x1 - x0)
    v = (0.5 * span) / 1.15                                 # px/s: reaches both collars at ~1.35 s
    xr = np.arange(x0, x1)
    T = 0.20 + np.abs(xr - xb) / v + 0.05 * noise1(len(xr), 45, rng) + 0.015 * noise1(len(xr), 14, rng)
    Tfull = np.full(W, 9.0, np.float32); Tfull[x0:x1] = T
    sag_px = 0.30 * ppm                                      # ~0.3 m just before each part lets go
    # ribbon layer mask (alpha) from top/bot, feathered
    rmask = np.zeros((H, W), np.float32)
    for x in range(x0, x1):
        rmask[top[x]:bot[x] + 1, x] = 1
    rmask = cv2.GaussianBlur(rmask, (0, 0), 0.8)
    # grain representatives (density curtain)
    R = 30
    cols = np.repeat(xr, R).astype(np.float32)
    colidx = np.repeat(np.arange(len(xr)), R)
    gx = cols + rng.random(len(cols)).astype(np.float32)
    frac = rng.random(len(cols)).astype(np.float32)
    gy = top[cols.astype(int)] + frac * (bot[cols.astype(int)] - top[cols.astype(int)])
    pb = cv2.GaussianBlur(plate, (0, 0), 0.8)
    gcol = pb[np.clip(gy.astype(int), 0, H - 1), cols.astype(int)]
    clump = np.exp(0.8 * rng.standard_normal(len(xr))).astype(np.float32)
    clump = np.convolve(np.pad(clump, 1, mode="edge"), [0.25, 0.5, 0.25], "valid")
    trel = T[colidx] + rng.random(len(cols)) * 0.12
    unit = (62.0 / R) * clump[colidx]
    ax_ = (WIND + 0.8 * np.sin(2 * np.pi * trel / 1.3)) / TAU_R * rng.uniform(0.7, 1.3, len(cols))
    v0 = rng.normal(0, 0.05, len(cols))
    # last thin dribble from each collar lip
    nd = 14
    dx = np.concatenate([x0 + rng.uniform(0, 7, nd), x1 - rng.uniform(0, 7, nd)]).astype(np.float32)
    dT = np.concatenate([np.full(nd, T[0]), np.full(nd, T[-1])]) + rng.uniform(0.06, 0.55, 2 * nd)
    dy0 = np.array([top[int(x)] + rng.random() * (bot[int(x)] - top[int(x)]) for x in dx], np.float32)
    dcol = pb[dy0.astype(int), dx.astype(int)]
    gx = np.concatenate([gx, dx]); gy = np.concatenate([gy, dy0]); gcol = np.concatenate([gcol, dcol])
    trel = np.concatenate([trel, dT]); unit = np.concatenate([unit, np.full(2 * nd, 0.35 / 2)])
    ax_ = np.concatenate([ax_, np.full(2 * nd, WIND / TAU_R)]); v0 = np.concatenate([v0, np.zeros(2 * nd)])
    gcol = np.clip(gcol * 0.55, 8, 70)
    hazeimg = cv2.GaussianBlur(end, (0, 0), 10)
    K = 8

    def frame(k):
        t = k / FPS
        # ribbon layer: columns sag then are released (never dissolved in place: their grains fall)
        dyc = np.zeros(W, np.float32)
        alpha_c = np.zeros(W, np.float32)
        alpha_c[x0:x1] = 1 - smoothstep((t - T) / 0.12)
        dyc[x0:x1] = sag_px * smoothstep((t - (T - 0.45)) / 0.45) * (1 - smoothstep((t - T) / 0.12))
        mapx, mapy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
        mapy = mapy - dyc[None, :]
        rl = cv2.remap(plate, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        ra = cv2.remap(rmask, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) * alpha_c[None, :]
        base = end * (1 - ra[..., None]) + rl * ra[..., None]
        # density curtain
        rho = np.zeros(H * W, np.float32); rc = np.zeros((H * W, 3), np.float32)
        for j in range(K):
            ts = t + (j + 0.5) / K * SHUT
            tau = ts - trel
            act = tau >= 0
            if not act.any():
                continue
            tc = tau[act]
            dfall = 0.5 * G * tc ** 2 + v0[act] * tc                       # m
            px = gx[act] + 0.5 * ax_[act] * tc ** 2 * ppm
            py = gy[act] + dfall * ppm
            fade = np.exp(-dfall / L_FADE)
            ok = (px >= 0) & (px < W - 1) & (py >= 0) & (py < H - 1)
            px, py, fade = px[ok], py[ok], fade[ok]
            u_ = unit[act][ok] * (0.4 + 0.6 * fade) / K
            gc_ = gcol[act][ok]
            hz = hazeimg[py.astype(int), px.astype(int)]
            cc = hz + (gc_ - hz) * fade[:, None]
            ix = np.floor(px).astype(int); iy = np.floor(py).astype(int)
            fx = px - ix; fy = py - iy
            for (ox, oy, w) in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
                idx = (iy + oy) * W + (ix + ox)
                rho += np.bincount(idx, weights=u_ * w, minlength=H * W).astype(np.float32)
                for c in range(3):
                    rc[:, c] += np.bincount(idx, weights=u_ * w * cc[:, c], minlength=H * W).astype(np.float32)
        rho2 = rho.reshape(H, W)
        a = (1 - np.exp(-1.5 * rho2))[..., None]
        cbar = rc.reshape(H, W, 3) / np.maximum(rho2[..., None], 1e-6)
        a = cv2.GaussianBlur(a[..., 0], (0, 0), 0.6)[..., None]
        cbar = cv2.GaussianBlur(cbar, (0, 0), 0.6)
        return base * (1 - a) + cbar * a

    log_put(f"E3-s14-{fmt}", dict(plate=cfg["plate"], ppm_from_woman=round(ppm_woman, 1), woman_px=cfg["woman_px"],
                                  ppm_from_ribbon_width_used=round(ppm_ribbon, 1), ppm_if_span_40m=round(ppm_span40, 1), ribbon_x=[x0, x1], ribbon_thick_px=[int(thick[valid].min()), int(thick[valid].max())],
                                  bridge_len_m_at_used_scale=round(span / ppm, 1), end_plate=used, sag_px=round(sag_px, 1),
                                  front_speed_px_s=round(v, 0), grain_px_at_used_scale=round(0.010 * ppm, 2), grain_ratio="below one pixel (sub-pixel, density curtain)",
                                  reps=int(len(gx))))
    if write:
        write_video(f"E3-s14-{fmt}", frame, W, H)
    return frame



# ==================================================================== E2 shot 7 inset (bands re-sharpening)
E2PPM = 1790.0        # P07: boot sole ~520 px / 0.29 m
E2_SOLE_PX = 520
E2_BOOT = [(225, 1000), (240, 700), (500, 520), (600, 700), (790, 860), (805, 1020), (700, 1065), (500, 1150), (300, 1145), (255, 1100)]
E2_TOP = [(0, 930), (560, 745), (1000, 600), (1340, 395), (1440, 380)]
E2_ORIGIN = (530.0, 1060.0)       # under his boot
E2_SPEED = 0.5 * E2PPM            # 0.5 m/s


def sample_patches(P, ys, xs, r=10):
    pp = np.pad(P, ((r, r), (r, r), (0, 0)), mode="edge")
    return np.stack([pp[int(y):int(y) + 2 * r, int(x):int(x) + 2 * r] for y, x in zip(ys, xs)])


def e2_setup():
    P = load_rgb(os.path.join(FIN, "P07_a01.png"))
    H, W = P.shape[:2]
    rng = np.random.default_rng(7007)
    L = luma(P)
    top = np.interp(np.arange(W), [p[0] for p in E2_TOP], [p[1] for p in E2_TOP])
    yy = np.arange(H)[:, None]
    reg = (luma(cv2.GaussianBlur(P, (0, 0), 2)) < 82) & (yy > top[None, :] - 4)
    boot = np.zeros((H, W), np.uint8); cv2.fillPoly(boot, [np.array(E2_BOOT, np.int32)], 1)
    boot = cv2.dilate(boot, np.ones((15, 15), np.uint8))
    reg &= boot == 0
    reg = cv2.morphologyEx(reg.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    reg = cv2.morphologyEx(reg, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(reg)
    reg = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.float32)
    mreg = cv2.GaussianBlur(reg, (0, 0), 3)
    # ridge field (band-pass luminance, crest = max); grains slump away from crests, hop back toward them
    R = cv2.GaussianBlur(L, (0, 0), 10) - cv2.GaussianBlur(L, (0, 0), 45)
    Rs = cv2.GaussianBlur(R, (0, 0), 18)
    gx = cv2.Sobel(Rs, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(Rs, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    sc = np.percentile(mag[reg > 0], 90) + 1e-6
    A = 7.0                                                   # px  (~8 mm)
    dx = np.tanh(gx / sc) * A + 4.0 * noise2(H, W, 9, rng); dy = np.tanh(gy / sc) * A + 4.0 * noise2(H, W, 9, rng)
    ratio = np.clip(cv2.GaussianBlur(L, (0, 0), 100) / np.maximum(cv2.GaussianBlur(L, (0, 0), 14), 1), 0.4, 2.5)[..., None]
    X, Y = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    dist = np.hypot(X - E2_ORIGIN[0], Y - E2_ORIGIN[1])
    Tf = 0.20 + dist / E2_SPEED + 0.07 * noise2(H, W, 60, rng) + 0.03 * noise2(H, W, 14, rng)
    return dict(P=P, H=H, W=W, reg=reg, mreg=mreg, dx=dx, dy=dy, ratio=ratio, X=X, Y=Y, Tf=Tf, rng=rng, L=L)


def p07s_alignment():
    ret = os.path.join(RET, "P07S-a01.png")
    if not os.path.exists(ret):
        return None
    P = load_rgb(os.path.join(FIN, "P07_a01.png"))
    S = conform(load_rgb(ret), 1440, 1440)
    return float(np.abs(luma(cv2.GaussianBlur(S, (0, 0), 3)) - luma(cv2.GaussianBlur(P, (0, 0), 3))).mean())


def e2_frames():
    d = e2_setup()
    P, H, W, X, Y, Tf = d["P"], d["H"], d["W"], d["X"], d["Y"], d["Tf"]
    rng = d["rng"]
    ppm = E2PPM
    soft = cv2.remap(P, X + d["dx"], Y + d["dy"], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) * d["ratio"]
    soft = cv2.GaussianBlur(soft, (0, 0), 1.2)
    save_rgb(os.path.join(PLATES, "P07S.png"), P * (1 - d["mreg"][..., None]) + soft * d["mreg"][..., None])
    nh = 7000
    ridx = np.argwhere(d["reg"] > 0)
    pick = ridx[rng.choice(len(ridx), nh)]
    hy, hx = pick[:, 0].astype(np.float32), pick[:, 1].astype(np.float32)
    ht = Tf[pick[:, 0], pick[:, 1]] + rng.uniform(-0.05, 0.10, nh)
    hh = rng.uniform(0.005, 0.015, nh)                               # hop height 5-15 mm
    hT = 2 * np.sqrt(2 * hh / G)                                      # flight time 0.064-0.11 s
    far = np.argsort(-Tf[pick[:, 0], pick[:, 1]])[:4]
    ht[far] = rng.uniform(1.50, 1.85, len(far))
    sx = hx - d["dx"][pick[:, 0], pick[:, 1]]; sy = hy - d["dy"][pick[:, 0], pick[:, 1]]
    R_ = 11
    patches = sample_patches(P, hy, hx, R_)
    yy, xx = np.mgrid[-R_:R_, -R_:R_]
    pm = np.clip(1.15 - np.hypot(xx + 0.5, yy + 0.5) / R_, 0, 1) ** 0.8
    pm = pm.astype(np.float32)[..., None]

    def frame_rgb(k):
        t = k / FPS
        s = smoothstep((t - Tf) / 0.13)[..., None]
        wp = cv2.remap(P, X + (1 - s[..., 0]) * d["dx"], Y + (1 - s[..., 0]) * d["dy"], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        wp = wp * d["ratio"] ** (1.0 * (1 - s))
        wb = cv2.GaussianBlur(wp, (0, 0), 1.2)
        wp = wp * (1 - 0.8 * (1 - s)) + wb * 0.8 * (1 - s)
        m = d["mreg"][..., None]
        out = P * (1 - m) + wp * m
        for j in range(3):
            ts = t + (j + 0.5) / 3 * SHUT
            u = (ts - ht) / hT
            act = np.where((u > 0) & (u < 1))[0]
            for i in act:
                uu = u[i]
                gxp = sx[i] + (hx[i] - sx[i]) * uu; gyp = sy[i] + (hy[i] - sy[i]) * uu
                lift = hh[i] * ppm * 4 * uu * (1 - uu)
                x0 = int(round(gxp)) - R_; y0g = int(round(gyp)) - R_
                if x0 < 0 or y0g - int(lift) < 0 or x0 + 2 * R_ >= W or y0g + 2 * R_ + 4 >= H:
                    continue
                sh = 0.18 * (1 - min(1, lift / (hh[i] * ppm + 1e-6)) * 0.6) / 3
                out[y0g + 3:y0g + 2 * R_ + 3, x0:x0 + 2 * R_] *= (1 - sh * pm)
                y0 = y0g - int(lift)
                reg_ = out[y0:y0 + 2 * R_, x0:x0 + 2 * R_]
                reg_[:] = reg_ * (1 - pm / 3) + patches[i] * (pm / 3)
        return out

    log_put("E2-core", dict(ppm=E2PPM, sole_px=E2_SOLE_PX, ridge_pitch_px=round(0.04 * E2PPM, 0), grain_px=round(0.010 * E2PPM, 1),
                            grain_ratio="1:29 (sole 0.29 m / grain 10 mm)", front_speed_m_s=0.5, front_speed_px_s=E2_SPEED,
                            n_hops=int(nh), flight_s=[round(float(hT.min()), 3), round(float(hT.max()), 3)],
                            p07s_vs_p07_mean_diff=p07s_alignment()))
    return frame_rgb


def e2(fmt, write=True):
    fr = e2_frames()
    if fmt == "H":
        W, H = 1920, 1080
        bgp = os.path.join(RET, "S07H-a02.png"); sz = int(0.34 * H); x0, y0 = 48, H - 48 - sz; kl = 2
    else:
        W, H = 1080, 1920
        bgp = os.path.join(RET, "S07V-a03.png"); sz = int(0.34 * H); x0, y0 = (W - sz) // 2, 1250; kl = 3
    bg = conform(load_rgb(bgp), W, H)
    key = np.array([176, 164, 148], np.float32)

    def frame(k):
        ins = cv2.resize(fr(k), (sz, sz), interpolation=cv2.INTER_AREA)
        out = bg.copy()
        out[y0 - kl:y0 + sz + kl, x0 - kl:x0 + sz + kl] = key
        out[y0:y0 + sz, x0:x0 + sz] = ins
        return out
    log_put(f"E2-s07-{fmt}", dict(bg=os.path.basename(bgp), inset_px=sz, inset_pos=[x0, y0], px_per_m_in_inset=round(E2PPM * sz / 1440, 1)))
    if write:
        write_video(f"E2-s07-{fmt}", frame, W, H)
    return frame, fr


if __name__ == "__main__":
    what = sys.argv[1:] or ["all"]
    for w in what:
        if w in ("e1s05", "all"):
            for f in "HV": e1_s5(f)
        if w in ("e1s01", "all"):
            for f in "HV": e1_s1(f)
        if w in ("e2", "all"):
            for f in "HV": e2(f)
        if w in ("e3", "all"):
            for f in "HV": e3(f)

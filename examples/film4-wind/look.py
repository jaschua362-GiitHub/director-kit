"""TEST-010 photographic finish ("look") for WIND v04 (Jason 2026-10-15: too bright / CGI).
Per frame, deterministic except grain: exposure down, filmic toe/shoulder curve, highlight roll-off + slight
highlight desaturation, warm halation bloom, very slight lens softness, vignette, luminance grain.
A grade cannot relight a CG start frame; this unifies and photographs the final shading only.
usage:  python -I work/look.py img  in.png out.png [preset]
        python -I work/look.py video in.mp4 out.mkv [preset]
"""
import sys, subprocess, numpy as np, cv2

PRESETS = {
    # stops, contrast, halation, soft, vignette, grain
    "A": dict(ev=-0.6, k=1.10, hal=0.18, soft=0.6, vig=0.30, grain=3.2),
    "B": dict(ev=-1.0, k=1.20, hal=0.22, soft=0.7, vig=0.40, grain=3.8),
    # E1 (2026-10-17, "a bit dark" feedback): highlights reach ~92-95%, faces ~35% (was ~25%), black re-seated ~2-3%
    "E1": dict(ev=-0.15, k=1.12, hal=0.18, soft=0.6, vig=0.20, grain=3.2, wp=1.3, gam=0.82, blk=0.025),
    "E1V": dict(ev=-0.08, k=1.12, hal=0.18, soft=0.6, vig=0.20, grain=3.2, wp=1.3, gam=0.82, blk=0.025),  # 9:16: skin matched to H
}

def srgb2lin(x): return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
def lin2srgb(x): return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(np.clip(x, 0, None), 1 / 2.4) - 0.055)

def filmic(x, k, wp=2.0):
    # Hable-like curve on linear light, normalised to white=4.0 so highlights roll off softly
    A, B, C, D, E, F = 0.22, 0.30, 0.10, 0.20 * k, 0.01, 0.30
    f = lambda v: ((v * (A * v + C * B) + D * E) / (v * (A * v + B) + D * F)) - E / F
    return f(x * 2.0) / f(np.float32(2.0 * wp))   # wp: linear input that maps to white (A used 2.0)

_vig = {}
def grade(bgr, p, rng):
    h, w = bgr.shape[:2]
    x = srgb2lin(bgr.astype(np.float32) / 255.0) * (2.0 ** p["ev"])
    # halation: bright areas bloom warm
    lum = x @ np.array([0.0722, 0.7152, 0.2126], np.float32)
    hi = np.clip((lum - 0.35) / 0.65, 0, 1)[..., None] * x
    bloom = cv2.GaussianBlur(hi, (0, 0), w / 90) * np.array([0.55, 0.8, 1.15], np.float32)  # BGR: warm
    x = x + p["hal"] * bloom
    y = filmic(x, p["k"], p.get("wp", 2.0))
    # desaturate the top end a little (film shoulder), keep shadows rich
    l2 = (y @ np.array([0.0722, 0.7152, 0.2126], np.float32))[..., None]
    y = l2 + (y - l2) * (1 - 0.35 * np.clip((l2 - 0.55) / 0.45, 0, 1))
    y = lin2srgb(np.clip(y, 0, 1))
    if p.get("gam", 1.0) != 1.0: y = np.power(y, p["gam"])   # display-space mid lift; black and white fixed
    if p.get("blk", 0.0): y = np.clip((y - p["blk"]) / (1 - p["blk"]), 0, 1)   # re-seat black after the lift
    if p["soft"]: y = cv2.GaussianBlur(y, (0, 0), p["soft"])
    if (h, w) not in _vig:
        yy, xx = np.mgrid[0:h, 0:w]; r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2))
        _vig[(h, w)] = (1 - p["vig"] * np.clip((r - 0.45) / 0.95, 0, 1) ** 1.6)[..., None].astype(np.float32)
    y = y * _vig[(h, w)]
    n = rng.normal(0, p["grain"] / 255.0, (h, w)).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), 0.6) * 1.6
    y = y + n[..., None] * (0.6 + 0.8 * (1 - np.abs(y - 0.45) * 2).clip(0, 1))  # most grain in mids
    return (np.clip(y, 0, 1) * 255 + 0.5).astype(np.uint8)

if __name__ == "__main__":
    mode, src, out = sys.argv[1:4]; p = PRESETS[sys.argv[4] if len(sys.argv) > 4 else "A"]
    rng = np.random.default_rng(7)
    if mode == "img":
        cv2.imwrite(out, grade(cv2.imread(src), p, rng))
    else:
        cap = cv2.VideoCapture(src); W, H = int(cap.get(3)), int(cap.get(4))
        o = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24',
                              '-i', '-', '-c:v', 'ffv1', out], stdin=subprocess.PIPE)
        while True:
            ok, f = cap.read()
            if not ok: break
            o.stdin.write(grade(f, p, rng).tobytes())
        o.stdin.close(); o.wait()

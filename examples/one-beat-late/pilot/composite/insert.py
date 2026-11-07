"""P11 insert: low glass close-up beside her boot, animated locally from one still (free).
The grains under the glass swirl (a vortex warp of the grain texture itself), then a bare footprint presses into
them beside her boot, parallel to it. A slow eased push-in and per-frame film grain keep the shot alive.
Glass reflections (bright pixels) are protected so they stay on top and never swirl.

Usage: python -I insert.py <still.png> <out_dir> <n_frames> [grade_ref.png]
"""
import sys, pathlib
import cv2, numpy as np

still = cv2.imread(sys.argv[1]).astype(np.float32)
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
N = int(sys.argv[3]); FPS = 24
OW, OH = 1920, 1080
h0, w0 = still.shape[:2]; sx = w0 / 1672.0

# optional grade match to the 1080p finish: per-channel mean/std on the dark grain floor
if len(sys.argv) > 4:
    ref = cv2.imread(sys.argv[4]).astype(np.float32)
    a = still[int(0.62 * h0):, int(0.55 * w0):].reshape(-1, 3)
    b = ref[int(0.80 * ref.shape[0]):, int(0.50 * ref.shape[1]):].reshape(-1, 3)
    still = np.clip((still - a.mean(0)) / (a.std(0) + 1e-6) * b.std(0) + b.mean(0), 0, 255) * 0.5 + still * 0.5

L = cv2.cvtColor(np.clip(still, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
protect = 1 - np.clip((cv2.GaussianBlur(L, (0, 0), 3) - 0.30) / 0.20, 0, 1)   # reflections and the boot sole stay put
yy, xx = np.mgrid[0:h0, 0:w0].astype(np.float32)

# floor-plane coordinates around the glyph (foreshortened: depth squashed toward the horizon)
CX, CY = 1160 * sx, 760 * sx
FS = 0.48                                    # vertical foreshortening at this depth
u, v = (xx - CX), (yy - CY) / FS             # top-down floor coords (px)
r, th = np.hypot(u, v), np.arctan2(v, u)

def footprint_height(n_len=520 * sx):
    """Top-down bare-foot depression (0..1), toes toward +u (screen right), heel toward -u."""
    k = n_len / 520.0
    hgt = np.zeros_like(u)
    def blob(cu, cv, ru, rv, w=1.0):
        return w * np.exp(-(((u - cu * k) / (ru * k)) ** 2 + ((v - cv * k) / (rv * k)) ** 2) ** 1.6)
    hgt = np.maximum(hgt, blob(-170, 6, 78, 62))          # heel
    hgt = np.maximum(hgt, blob(-40, 18, 120, 52, 0.75))   # arch (shallower, outer edge)
    hgt = np.maximum(hgt, blob(95, -2, 95, 82))           # ball
    for cu, cv, rr in [(205, -52, 30), (222, -8, 22), (218, 28, 20), (205, 60, 18), (186, 86, 15)]:
        hgt = np.maximum(hgt, blob(cu, cv, rr, rr * 0.95, 0.9))   # toes, big toe on the far (-v) side
    return hgt
HGT = footprint_height().astype(np.float32)

def ease(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

E = cv2.imread(sys.argv[5] if len(sys.argv) > 5 else str(pathlib.Path(__file__).resolve().parents[4] / "approved/DCL-20261030-BEAT/v04/environments/E01/E01-07.png"))
es = E.shape[1] / 1672.0
crop = cv2.cvtColor(E[int(515 * es):int(620 * es), int(880 * es):int(1005 * es)], cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
rel = cv2.GaussianBlur(crop, (0, 0), 1.5) - cv2.GaussianBlur(crop, (0, 0), 12)
wy, wx = np.mgrid[0:crop.shape[0], 0:crop.shape[1]].astype(np.float32)
win = np.clip(1 - np.hypot((wx - crop.shape[1] * 0.5) / (crop.shape[1] * 0.40), (wy - crop.shape[0] * 0.52) / (crop.shape[0] * 0.42)), 0, 1) ** 0.6
rel = rel * win / (np.abs(rel * win).max() + 1e-6)
FW = int(500 * sx); FH = int(rel.shape[0] / rel.shape[1] * FW * 0.85)      # a little flatter: this lens is lower
relr = cv2.resize(rel, (FW, FH), interpolation=cv2.INTER_CUBIC)
FP = np.zeros((h0, w0), np.float32)
x0, y0 = int(CX - FW / 2), int(CY - FH / 2)
FP[y0:y0 + FH, x0:x0 + FW] = relr[:max(0, min(FH, h0 - y0)), :max(0, min(FW, w0 - x0))]

T = lambda i: i / FPS
SW0, SW1, FP0, FP1 = 0.15, 0.90, 0.60, 1.00
rng = np.random.default_rng(7)
noise_sigma = 1.6

for i in range(N):
    t = T(i)
    img = still.copy()
    # 1) grain swirl: rotate the grain texture inside a shrinking disc, strongest at the centre
    if SW0 <= t <= SW1 + 0.15:
        sp = (t - SW0) / (SW1 - SW0)
        amp = ease((t - SW0) / 0.2) * (1 - ease((t - SW1 + 0.05) / 0.2))
        R = 330 * sx * (1 - 0.45 * np.clip(sp, 0, 1))
        ang = amp * 3.4 * np.clip(1 - r / R, 0, 1) ** 1.5 * (0.6 + sp)
        uu = u * np.cos(ang) - v * np.sin(ang); vv = u * np.sin(ang) + v * np.cos(ang)
        mx, my = (uu + CX).astype(np.float32), (vv * FS + CY).astype(np.float32)
        sw = cv2.remap(still, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        arms = 0.5 + 0.5 * np.cos(3 * th + r / (26 * sx) - sp * 10)
        dark = 1 - 0.40 * amp * arms * np.clip(1 - r / R, 0, 1)
        wgt = (protect * np.clip(1 - r / (R * 1.05), 0, 1) ** 0.3)[..., None]
        img = img * (1 - wgt) + sw * dark[..., None] * wgt
    # 2) the footprint presses in: the approved E01-07 footprint relief (toes away from camera, as the board
    #    draws it), low-frequency shading only, so this still's own grain stays crisp inside it
    if t >= FP0:
        mod = 1.05 * ease((t - FP0) / (FP1 - FP0)) * FP * protect
        img = img * (1 + mod[..., None])
    # 3) eased push-in toward the glyph, rendered to 1920x1080
    z = 1.0 + 0.07 * (t / (N / FPS)) ** 1.6                      # accelerating push: still moving at the cut
    k = OW / w0; px, py = (w0 * 0.5 * 0.6 + CX * 0.4) * k, (h0 * 0.5 * 0.6 + CY * 0.4) * k   # push toward the glyph
    M = np.float32([[z * k, 0, px - z * px], [0, z * k, py - z * py]])
    fr = cv2.warpAffine(np.clip(img, 0, 255), M, (OW, OH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    fr = fr + rng.normal(0, noise_sigma, fr.shape[:2])[..., None]   # fresh film grain each frame
    cv2.imwrite(str(out / f"i_{i + 1:03d}.png"), np.clip(fr, 0, 255).astype(np.uint8))
print("insert frames:", N)

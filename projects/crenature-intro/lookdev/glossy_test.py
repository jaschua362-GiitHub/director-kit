"""Look test: can code alone turn the flat locked creature mark into the glossy 3D finish
of refs/final_look_3d.jpg?  Height field from a distance transform of the silhouette ->
normals -> studio shading (key, soft env reflection, fresnel rim, specular) + contact shadow.

    python lookdev/glossy_test.py [--inflate 1.0] [--out stills/look_glossy_v1.png]

`--inflate 0` gives the flat ink mark, 1 the full 3D look: the animation can ramp it.
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument('--inflate', type=float, default=1.0)
ap.add_argument('--out', default='stills/look_glossy_v1.png')
a = ap.parse_args()

W, H = 1920, 1080
AMBER = np.array([0xFB, 0x8F, 0x18]) / 255.0

# --- masks from the locked creature PNG -------------------------------------------------
src = np.asarray(Image.open('source/LOCKED-creature.png').convert('RGB')).astype(float) / 255
lum = src.mean(2)
sat = src.max(2) - src.min(2)
eye = sat > 0.35
ink = (lum < 0.5) | eye                                   # body incl. the eye hole
ink = ndimage.binary_fill_holes(ndimage.binary_closing(ink, iterations=2))
ys, xs = np.where(ink)
pad = 12
y0, y1, x0, x1 = ys.min() - pad, ys.max() + pad, xs.min() - pad, xs.max() + pad
ink, eye = ink[y0:y1, x0:x1], eye[y0:y1, x0:x1]

# --- height field: rounded "inflated" profile --------------------------------------------
d = ndimage.distance_transform_edt(ink)
# local half-thickness: spread the medial-axis distance outwards, so every limb is a full
# rounded tube (thick coil = fat tube, horns/tail tip = thin tube), like the reference
d = ndimage.gaussian_filter(d, 1.5)
half = ndimage.grey_dilation(d, size=(25, 25))
half = np.maximum(ndimage.gaussian_filter(half, 8), 1.0)
t = np.clip(d / half, 0, 1)
h = half * np.sqrt(1 - (1 - t) ** 2) * 0.9 * a.inflate      # circular cross-section
h = ndimage.gaussian_filter(h, 2.5)
gy, gx = np.gradient(h)
n = np.dstack([-gx, -gy, np.ones_like(h)])
n /= np.linalg.norm(n, axis=2, keepdims=True)

# --- shading -------------------------------------------------------------------------------
V = np.array([0, 0, 1.0])
def norm(v): v = np.array(v, float); return v / np.linalg.norm(v)
key = norm([-0.55, -0.65, 0.55])                            # upper-left softbox
fill = norm([0.7, 0.2, 0.6])
ndl = np.clip((n * key).sum(2), 0, 1)
ndf = np.clip((n * fill).sum(2), 0, 1)
ndv = np.clip(n[..., 2], 0, 1)
r = 2 * n * ndv[..., None] - V                              # reflection vector
# studio environment: bright top-left softbox, darker floor, grey walls
rk = np.clip((r * key).sum(2), 0, 1)
env = (0.12 + 0.45 * np.clip(-r[..., 1], 0, 1) ** 1.5          # sky/ceiling
       + 0.35 * rk ** 3 + 0.9 * rk ** 14                      # broad sheen + softbox
       + 0.25 * np.clip(r[..., 0], 0, 1) ** 4)                 # right-side bounce card
fres = 0.04 + 0.96 * (1 - ndv) ** 5
hl = np.clip((n * norm(key + V)).sum(2), 0, 1) ** 140        # tight specular
base = 0.035
shade = base * (0.35 + 0.65 * ndl + 0.25 * ndf) + (0.05 + fres) * env * 0.75 + 0.5 * hl
col = np.dstack([shade] * 3) * np.array([1.0, 0.985, 0.97])  # slightly warm studio light
# eye: glowing amber, kept flat and bright
eyeb = ndimage.gaussian_filter(eye.astype(float), 1.0)
col = col * (1 - eyeb[..., None]) + AMBER * (1.0 + 0.3 * eyeb[..., None]) * eyeb[..., None]
alpha = ndimage.gaussian_filter(ink.astype(float), 0.7)

# --- place in a 16:9 frame -------------------------------------------------------------------
yy, xx = np.mgrid[0:H, 0:W]
bg = 0.94 - 0.10 * (np.hypot((xx - 0.35 * W) / W, (yy - 0.25 * H) / H) ** 1.4)
frame = np.dstack([bg, bg * 0.995, bg * 0.99])

scale = 600 / ink.shape[0]
size = (int(ink.shape[1] * scale), int(ink.shape[0] * scale))
cx, cy = 560, 520
ox, oy = cx - size[0] // 2, cy - size[1] // 2
def fit(arr):
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.resize(size, Image.LANCZOS)).astype(float) / 255
C, A = fit(col), fit(alpha)

# contact + soft drop shadow (only as strong as the inflation)
sh = np.zeros((H, W))
sh[oy:oy + size[1], ox:ox + size[0]] = A
soft = ndimage.gaussian_filter(np.roll(sh, (18, 10), (0, 1)), 22) * 0.35
floor = np.exp(-(((xx - cx + 10) / 170) ** 2 + ((yy - (oy + size[1] - 14)) / 12) ** 2)) * 0.5
shadow = np.clip(soft + floor, 0, 0.6) * a.inflate
frame *= (1 - shadow)[..., None]

roi = frame[oy:oy + size[1], ox:ox + size[0]]
roi[:] = roi * (1 - A[..., None]) + C * A[..., None]

# --- wordmark: locked custom wordmark, dot recoloured amber ----------------------------------
wm = np.asarray(Image.open('source/LOCKED-wordmark.png').convert('RGB')).astype(float) / 255
wl, ws = wm.mean(2), wm.max(2) - wm.min(2)
wink, wdot = wl < 0.5, ws > 0.35
ys, xs = np.where(wink | wdot)
wink, wdot = wink[ys.min():ys.max() + 1, xs.min():xs.max() + 1], wdot[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
wsize = (760, int(720 * wink.shape[0] / wink.shape[1]))
def fitm(m): return np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize(wsize, Image.LANCZOS)).astype(float) / 255
WI, WD = fitm(wink.astype(float)), fitm(wdot.astype(float))
wx, wy = 900, 540 - wsize[1] // 2
roi = frame[wy:wy + wsize[1], wx:wx + wsize[0]]
roi[:] = roi * (1 - WI[..., None]) + np.array([0.063, 0.063, 0.063]) * WI[..., None]
roi[:] = roi * (1 - WD[..., None]) + AMBER * WD[..., None]

# dither against H.264 banding (craft rule: no visible grain)
frame += (np.random.default_rng(1).random(frame.shape) - 0.5) / 255
Image.fromarray((np.clip(frame, 0, 1) * 255).astype(np.uint8)).save(a.out)
print('wrote', a.out)

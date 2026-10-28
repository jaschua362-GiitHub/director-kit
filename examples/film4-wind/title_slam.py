"""WIND end title v2 (Jason 2026-10-16): the 上弦 / WIND THE MAN lockup SLAMS in on the approved mix's pang
(no added sound), centred, mostly black. Clip frame 0 = v06 smash-to-black (film frame 674); contact = clip frame CONTACT
(film 683 = pang onset 28.44 s). Approach: 0.17 s accelerating zoom-in from 2.4x with zoom blur -> contact: hot flash,
cyan charge across the strokes, ember burst, decaying shake, small overshoot -> hold with slow push-in + light sweep -> fade.
usage: python -I work/title_slam.py <matte.png> <out.mkv> [--still frame ...]
env: TFONT (default PERTIBD.TTF), TSIZE, TTRACK
"""
import sys, os, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = int(os.environ.get('TW', 1920)), int(os.environ.get('THH', 1080)), 24
NF, CONTACT, APPROACH = 96, 9, 4                 # 4.0 s clip, contact frame, approach frames
matte_p, out = sys.argv[1], sys.argv[2]
STILLS = [int(sys.argv[i + 1]) for i, a in enumerate(sys.argv) if a == '--still']
rng = np.random.default_rng(11)
def sm(a, b, x): x = np.clip((x - a) / (b - a), 0, 1); return x * x * (3 - 2 * x)

# ---------- lockup on a local canvas ----------
g = cv2.imread(matte_p, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
ink = np.clip((0.82 - g) / 0.55, 0, 1)
ys, xs = np.where(ink > 0.3); pad = 20
ink = ink[max(0, ys.min() - pad):ys.max() + pad, max(0, xs.min() - pad):xs.max() + pad]
TH = int(os.environ.get('TLH', 672))
ink = cv2.resize(ink, (int(ink.shape[1] * TH / ink.shape[0]), TH), interpolation=cv2.INTER_AREA); th, tw = ink.shape
CW, CH = tw + 260, th + 40
M = np.zeros((CH, CW), np.float32); OX, OY = 40, 20; M[OY:OY + th, OX:OX + tw] = ink
# English, fitted to the free channel right of 弦 (between 上's stroke and the tail) — Jason's layout
img = Image.new('L', (900, 90), 0); d = ImageDraw.Draw(img)
f = ImageFont.truetype('C:/Windows/Fonts/' + os.environ.get('TFONT', 'TCM_____.TTF'), int(os.environ.get('TSIZE', 36)))
x = 0
for ch in 'WIND THE MAN':
    d.text((x, 8), ch, fill=255, font=f); x += f.getlength(ch) + int(os.environ.get('TTRACK', 3))
a = np.array(img, np.float32)[:, :int(x)] / 255; r = np.where(a.max(1) > 0.05)[0]; a = np.rot90(a[r.min():r.max() + 1], -1)
body = M[OY + int(th * 0.47):OY + int(th * 0.70)]
ex = int(np.percentile(np.where(body > 0.2)[1], 99.5)) + 16
free = cv2.dilate(M, np.ones((7, 7), np.uint8))[:, ex - 6:ex + a.shape[1] + 6].max(1) < 0.08
best, cur, s0 = (0, 0), 0, 0
for yv in range(OY + int(th * 0.25), OY + th):
    if free[yv]:
        if cur == 0: s0 = yv
        cur += 1
        if cur > best[1]: best = (s0, cur)
    else: cur = 0
y0, run = best; mg = 8
if a.shape[0] > run - 2 * mg:
    k = (run - 2 * mg) / a.shape[0]; a = cv2.resize(a, (max(1, int(a.shape[1] * k)), int(a.shape[0] * k)), interpolation=cv2.INTER_AREA)
E = np.zeros_like(M); E[y0 + mg:y0 + mg + a.shape[0], ex:ex + a.shape[1]] = a
# centre the union bbox on screen
U = np.maximum(M, E); uy, ux = np.where(U > 0.1)
# optical centre: character bodies + English column (exclude the long 弦 tail and ink splatter)
core = cv2.morphologyEx((U[:OY + int(th * 0.80)] > 0.3).astype(np.uint8), cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
core = np.maximum(core, (E[:OY + int(th * 0.80)] > 0.2).astype(np.uint8))
cy_, cx_ = np.where(core > 0)
LCX, LCY = (np.percentile(cx_, 1) + np.percentile(cx_, 99)) / 2, (uy.min() + uy.max()) / 2

# ---------- material (local) ----------
yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
hb = cv2.GaussianBlur(M, (0, 0), 3.0)
gx, gy = cv2.Sobel(hb, cv2.CV_32F, 1, 0, ksize=5), cv2.Sobel(hb, cv2.CV_32F, 0, 1, ksize=5)
nz = np.full_like(gx, 3.0); nn = np.sqrt(gx ** 2 + gy ** 2 + nz ** 2)
L = np.array([-0.55, -0.6, 0.58]); L /= np.linalg.norm(L)
diffuse = np.clip((-gx * L[0] - gy * L[1] + nz * L[2]) / nn, 0, 1)
_n = rng.normal(0, 1, (CH, CW)).astype(np.float32)
bh = cv2.GaussianBlur(_n, (0, 0), sigmaX=9, sigmaY=0.8); bv = cv2.GaussianBlur(_n, (0, 0), sigmaX=0.8, sigmaY=9)
_g = cv2.GaussianBlur(M, (0, 0), 6); _gx, _gy = cv2.Sobel(_g, cv2.CV_32F, 1, 0, ksize=5), cv2.Sobel(_g, cv2.CV_32F, 0, 1, ksize=5)
_wv = cv2.GaussianBlur(_gx ** 2, (0, 0), 8) / (cv2.GaussianBlur(_gx ** 2 + _gy ** 2, (0, 0), 8) + 1e-6)
bristle = (1 - _wv) * bh / bh.std() + _wv * bv / bv.std()
dry = cv2.GaussianBlur(M, (0, 0), 1.0)
gold_dark = np.array([0.02, 0.08, 0.20]); gold_mid = np.array([0.12, 0.40, 0.78]); gold_hi = np.array([0.70, 0.92, 1.0])  # BGR
cyan = np.array([1.0, 0.85, 0.25]); hot = np.array([0.70, 0.92, 1.0])
base = gold_dark + (gold_mid - gold_dark) * diffuse[..., None] ** 0.8
tex = (0.86 + 0.14 * np.tanh(bristle))[..., None] * (0.55 + 0.45 * dry)[..., None]

def lockup_rgb(t, flash, charge):
    sweep = np.exp(-(((xx - (-300 + (CW + 600) * sm(0.8, 3.6, t))) + 0.6 * (yy - CH / 2)) ** 2) / (2 * 120 ** 2))
    spec = (diffuse ** 12)[..., None] * gold_hi * 1.2 + sweep[..., None] * diffuse[..., None] ** 3 * gold_hi * 0.8
    col = (base + spec) * tex
    edge = np.clip(cv2.GaussianBlur(M, (0, 0), 2) - cv2.GaussianBlur(M, (0, 0), 6), 0, 1)
    col = col + cyan * (edge * 3.0 + 0.25 * M)[..., None] * charge + hot * flash
    gv = np.clip((yy - OY) / th, 0, 1)[..., None] ** 1.3              # top deep amber -> bottom pale cream gold
    cream = np.array([0.52, 0.80, 0.98])
    col = (col * (1 - 0.55 * gv) + cream * gv * (0.45 + 0.75 * diffuse[..., None]) * tex) * 1.25
    # English takes the calligraphy's own colour at each height (row-average of the strokes, smoothed)
    wsum = M.sum(1); rowc = (col * M[..., None]).sum(1) / (wsum[:, None] + 1e-6)
    have = wsum > 2; idx = np.arange(CH)
    rowc = np.stack([np.interp(idx, idx[have], rowc[have, c]) for c in range(3)], 1)
    rowc = cv2.GaussianBlur(rowc[:, None, :].astype(np.float32), (0, 0), sigmaX=0.1, sigmaY=30)[:, 0, :]
    rgb = col * M[..., None] + E[..., None] * rowc[:, None, :] * 1.1
    return rgb, U

def place(rgb, alpha, scale, dx, dy):
    A = np.float32([[scale, 0, W / 2 - scale * LCX + dx], [0, scale, H / 2 - scale * LCY + dy]])
    return (cv2.warpAffine(rgb, A, (W, H), flags=cv2.INTER_LINEAR), cv2.warpAffine(alpha, A, (W, H), flags=cv2.INTER_LINEAR))

shake = rng.normal(0, 1, (NF, 2))
emb = [dict(a=rng.uniform(0, 6.28), v=rng.uniform(200, 900), s=rng.uniform(1.0, 2.8), w=rng.uniform(0.4, 1.0), up=rng.uniform(20, 80)) for _ in range(90)]
drift = [dict(x=rng.uniform(200, 1720), y=rng.uniform(100, 1080), v=rng.uniform(10, 30), s=rng.uniform(0.8, 2.0), w=rng.uniform(0.2, 0.6)) for _ in range(40)]
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def frame(i):
    t = i / FPS; tc = (i - CONTACT) / FPS
    img = np.zeros((H, W, 3), np.float32)
    if i < CONTACT - APPROACH: return img
    if i < CONTACT:                                            # accelerating approach with zoom blur
        p = (i - (CONTACT - APPROACH)) / APPROACH
        rgb, al = lockup_rgb(t, 0.0, 0.0)
        S = 16
        for k in range(S):
            pk = p + k / S / APPROACH
            sc = 1.0 + 1.4 * (1 - pk) ** 2
            c, a_ = place(rgb, al, sc, 0, 0)
            img += c * (0.30 + 0.70 * pk) / S
        return cv2.GaussianBlur(img, (0, 0), 1.2)
    flash = np.exp(-tc / 0.05) * 0.9 + 0.15 * np.exp(-tc / 0.30)
    charge = np.exp(-tc / 0.45)
    sc = 1.0 - 0.025 * np.exp(-tc / 0.12) * np.cos(tc * 30) + 0.035 * sm(0.3, 4.0, t)   # overshoot, then slow push-in
    amp = 14 * np.exp(-tc / 0.18)
    rgb, al = lockup_rgb(t, flash, charge)
    c, a_ = place(rgb, al, sc, shake[i, 0] * amp, shake[i, 1] * amp)
    glow = cv2.GaussianBlur(c, (0, 0), 14) * (0.40 + 0.8 * flash) + cv2.GaussianBlur(c, (0, 0), 70) * (0.30 + 0.9 * flash)
    img = c + glow
    # contact shockwave: a thin warm ring + ember burst outward from the lockup
    rr = np.hypot(XX - W / 2, YY - H / 2)
    R = 120 + 1800 * (1 - np.exp(-tc / 0.25))
    em = np.zeros((H, W), np.float32)
    for e in emb:
        dist = e['v'] * (1 - np.exp(-tc / 0.5)); x = W / 2 + np.cos(e['a']) * dist; y = H / 2 + np.sin(e['a']) * dist * 0.6 - e['up'] * tc
        if 0 <= x < W and 0 <= y < H: cv2.circle(em, (int(x), int(y)), int(e['s']), e['w'] * np.exp(-tc / 1.2), -1, cv2.LINE_AA)
    for e in drift:
        x = e['x']; y = e['y'] - e['v'] * tc * 2
        if 0 <= y < H: cv2.circle(em, (int(x), int(y)), int(e['s']), e['w'] * sm(0, 1.0, tc), -1, cv2.LINE_AA)
    img += cv2.GaussianBlur(em, (0, 0), 1.0)[..., None] * np.array([0.35, 0.65, 1.0])
    img += (np.exp(-((XX - W / 2) ** 2 + (YY - H / 2) ** 2) / (2 * 520 ** 2)) * 0.035)[..., None] * np.array([0.12, 0.28, 0.5])  # faint warm air
    img *= 1 - sm(NF / FPS - 0.7, NF / FPS, t)
    return img

def finish(img):
    img = 1 - np.exp(-np.maximum(img, 0) * 1.15)
    n = cv2.GaussianBlur(rng.normal(0, 3.2 / 255, (H, W)).astype(np.float32), (0, 0), 0.6) * 1.6
    return (np.clip(img + n[..., None], 0, 1) * 255 + 0.5).astype(np.uint8)

if STILLS:
    for i in STILLS: cv2.imwrite(out.replace('.mkv', f'_f{i}.png'), finish(frame(i)))
else:
    o = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'ffv1', out], stdin=subprocess.PIPE)
    for i in range(NF): o.stdin.write(finish(frame(i)).tobytes())
    o.stdin.close(); o.wait(); print('ok', out)

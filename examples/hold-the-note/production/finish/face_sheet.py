"""Face check sheet: SeedVR2 (from the 480p draft) vs the bicubic draft, same frame, face crop at 100 %.
Decode with the bundled ffmpeg only; face box from a skin-tone mask (numpy/scipy).
usage: python face_sheet.py OUT.jpg 04H:21 04V:21 ...   (name:skip)"""
import sys, subprocess, json, numpy as np
from scipy import ndimage as ndi
from pathlib import Path
from PIL import Image, ImageDraw
FF = r"<LAB>\experiments\TEST-001\tools\python-media\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
HERE = Path(__file__).parent; TAKES = HERE.parents[1] / "p4_takes"
def frames(path, w, h, scale=None):
    vf = ["-vf", f"scale={w}:{h}:flags=bicubic"] if scale else []
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), *vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
def face_box(img):
    # skin-tone mask (Kovac rule), largest blob in the upper 70 % of the frame
    r, g, b = [img[..., k].astype(int) for k in range(3)]
    m = (r > 95) & (g > 40) & (b > 20) & (r - np.minimum(g, b) > 15) & (abs(r - g) > 15) & (r > g) & (r > b)
    m[int(img.shape[0] * 0.85):] = False
    m = ndi.binary_opening(m, iterations=3); lab, n = ndi.label(m)
    if n == 0: return None
    sizes = ndi.sum(m, lab, range(1, n + 1)); k = int(np.argmax(sizes)) + 1
    if sizes[k - 1] < 2500: return None
    ys, xs = np.nonzero(lab == k); return (xs.min(), ys.min(), xs.max() - xs.min(), ys.max() - ys.min())
out, specs = sys.argv[1], sys.argv[2:]
T = 300; rows = []; report = {}
for sp in specs:
    parts = sp.split(":"); name, skip = parts[0], int(parts[1]); src = Path(parts[2]) if len(parts) > 2 else HERE / f"{name}.mkv"
    sv = frames(src, *((1920, 1080) if name.endswith("H") else (1080, 1920)))
    H_, W_ = sv.shape[1:3]
    dr = frames(TAKES / f"{name}.mp4", W_, H_, scale=True)[skip:skip + len(sv)]
    n = min(len(sv), len(dr)); sv, dr = sv[:n], dr[:n]
    mid = sv[n // 2]; fb = face_box(mid)
    if fb is None: cx, cy, s = W_ // 2, H_ // 3, 520
    else: x, y, w, h = fb; cx, cy, s = x + w // 2, y + h // 2, int(max(w, h) * 1.3)
    s = max(300, min(s, min(W_, H_))); x0 = int(np.clip(cx - s // 2, 0, W_ - s)); y0 = int(np.clip(cy - s // 2, 0, H_ - s))
    crop = lambda a: a[..., y0:y0 + s, x0:x0 + s, :]
    csv, cdr = crop(sv).astype(np.float32), crop(dr).astype(np.float32)
    # temporal flicker: mean |frame diff| of the high-pass detail, SeedVR2 vs draft
    def hp(a): return a - ndi.gaussian_filter(a, (0, 3, 3))
    fl_sv = float(np.abs(np.diff(hp(csv[::1].mean(-1)), axis=0)).mean()); fl_dr = float(np.abs(np.diff(hp(cdr.mean(-1)), axis=0)).mean())
    report[name] = dict(frames=n, face_found=fb is not None, crop=[x0, y0, s], flicker_sv=round(fl_sv, 2), flicker_draft=round(fl_dr, 2), ratio=round(fl_sv / max(fl_dr, 1e-6), 2))
    tiles = []
    for i in (3, n // 2, n - 4):
        for a, lab in ((cdr[i], "draft"), (csv[i], "SeedVR2")):
            im = Image.fromarray(a.astype(np.uint8)).resize((T, T), Image.LANCZOS); d = ImageDraw.Draw(im)
            d.rectangle([0, 0, T, 14], fill=(0, 0, 0)); d.text((3, 1), f"{name} f{skip + i} {lab}", fill=(255, 230, 80)); tiles.append(im)
    row = Image.new("RGB", (T * 6, T)); [row.paste(t, (k * T, 0)) for k, t in enumerate(tiles)]; rows.append(row)
sheet = Image.new("RGB", (T * 6, T * len(rows))); [sheet.paste(r, (0, k * T)) for k, r in enumerate(rows)]
sheet.save(out, quality=88); print(json.dumps(report))

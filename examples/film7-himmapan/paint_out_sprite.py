"""Paint a frozen sprite (Seedance's frozen winged elephant) out of a take. Generalises paint_out_elephant.py.

Usage: python -I paint_out_sprite.py <video> <name> <ref_frame> <x> <y> <w> <h> [first last]

The sprite is a frozen copy of the same pixels, so it is template-tracked, inpainted once in the
reference frame, and that clean patch is placed in every frame where it appears, with focus
matching and ECC alignment. Pixels are replaced only where the frame still matches the sprite,
or where they are mid-grey leftovers darker than the mist, so anything passing in front is kept.
The mask is the darker-than-mist area inside the box, which suits a sprite against bright mist.
"""
import json, pathlib, subprocess, sys
import cv2
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
FF = r"<LAB>\experiments\TEST-001\tools\python-media\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
PAD = 24


def sprite_mask(img, x, y, w, h):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0]
    bg = cv2.medianBlur(np.clip(L, 0, 255).astype(np.uint8), 61).astype(np.float32)
    m = np.zeros(L.shape, np.uint8)
    roi = (L[y:y + h, x:x + w] < bg[y:y + h, x:x + w] - 10).astype(np.uint8) * 255
    roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lbl, st, _ = cv2.connectedComponentsWithStats(roi)
    keep = np.zeros_like(roi)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] > 0.01 * w * h:
            keep[lbl == k] = 255
    m[y:y + h, x:x + w] = keep
    return cv2.dilate(m, np.ones((7, 7), np.uint8), iterations=2)


def main():
    src, name, ri, x, y, w, h = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:8])
    src = pathlib.Path(src)
    fr_dir = HERE / f"work/{name}_frames"; out_dir = HERE / f"work/{name}_clean"
    fr_dir.mkdir(parents=True, exist_ok=True); out_dir.mkdir(parents=True, exist_ok=True)
    if not any(fr_dir.iterdir()):
        subprocess.run([FF, "-v", "error", "-y", "-i", str(src), str(fr_dir / "f_%04d.png")], check=True)
    FR = sorted(fr_dir.glob("f_*.png"))
    first, last = (int(sys.argv[8]), int(sys.argv[9])) if len(sys.argv) > 9 else (0, len(FR) - 1)

    ref = cv2.imread(str(FR[ri])).astype(np.float32)
    poly = HERE / f"work/{name}_poly.json"
    if poly.exists():                                  # hand-drawn silhouette (more reliable than the auto mask)
        mask = np.zeros(ref.shape[:2], np.uint8)
        cv2.fillPoly(mask, [np.int32(json.load(open(poly)))], 255)
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
    else:
        mask = sprite_mask(ref.astype(np.uint8), x, y, w, h)
    cv2.imwrite(str(HERE / f"work/{name}_mask.png"), mask)
    clean = cv2.inpaint(ref.astype(np.uint8), mask, 9, cv2.INPAINT_TELEA).astype(np.float32)
    x0, y0, x1, y1 = x - PAD, y - PAD, x + w + PAD, y + h + PAD
    O, C, M = ref[y0:y1, x0:x1], clean[y0:y1, x0:x1], mask[y0:y1, x0:x1].astype(np.float32) / 255
    Mf = cv2.GaussianBlur(cv2.dilate(M, np.ones((9, 9), np.uint8)), (0, 0), 3)
    ring = (cv2.dilate(M, np.ones((15, 15), np.uint8)) - cv2.dilate(M, np.ones((5, 5), np.uint8))) > 0.5
    Tg = cv2.cvtColor(ref[y:y + h, x:x + w].astype(np.uint8), cv2.COLOR_BGR2GRAY)

    log = []
    for i, f in enumerate(FR):
        cur = cv2.imread(str(f)).astype(np.float32)
        changed, pos = 0, None
        if first <= i <= last:
            g = cv2.cvtColor(cur.astype(np.uint8), cv2.COLOR_BGR2GRAY); best = (-1, None)
            for sig in (0, 3):
                Tb = cv2.GaussianBlur(Tg, (0, 0), sig) if sig else Tg
                for s in np.arange(0.85, 1.16, 0.05):
                    t = cv2.resize(Tb, None, fx=s, fy=s)
                    r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
                    if mv > best[0]: best = (mv, (ml[0], ml[1], float(s)))
            if best[0] >= 0.8: pos = best[1]
        if pos is not None:
            px, py, s = pos
            A = np.float32([[s, 0, px - s * PAD], [0, s, py - s * PAD]])
            H, W = cur.shape[:2]
            cg = cv2.cvtColor(np.clip(cur, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
            best_sig, best_err = 0.0, 1e9
            for sig in (0, 0.7, 1.2, 1.8, 2.5, 3.5, 5, 7):
                Ob = cv2.GaussianBlur(O, (0, 0), sig) if sig else O
                wOg = cv2.warpAffine(cv2.cvtColor(Ob.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32), A, (W, H))
                wm = cv2.warpAffine(M, A, (W, H)) > 0.5
                err = np.median(np.abs(cg[wm] - wOg[wm])) if wm.sum() > 50 else 1e9
                if err < best_err: best_sig, best_err = sig, err
            Ob = cv2.GaussianBlur(O, (0, 0), best_sig) if best_sig else O
            Cb = cv2.GaussianBlur(C, (0, 0), best_sig) if best_sig else C
            try:
                warp = A.copy()
                _, warp = cv2.findTransformECC(cv2.cvtColor(Ob.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32), cg, warp,
                                               cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 60, 1e-5), None, 5)
                if np.abs(warp - A).max() < 8: A = warp
            except cv2.error:
                pass
            wO = cv2.warpAffine(Ob, A, (W, H)); wC = cv2.warpAffine(Cb, A, (W, H))
            wM = cv2.warpAffine(Mf, A, (W, H)); wR = cv2.warpAffine(ring.astype(np.float32), A, (W, H)) > 0.5
            diff = cv2.GaussianBlur(np.abs(cur - wO).mean(-1), (0, 0), 4)
            vis = cv2.GaussianBlur(np.clip((34 - diff) / 12, 0, 1), (0, 0), 2)
            ok = wR & (diff < 20)
            gain = (cur[ok].mean(0) + 1) / (wO[ok].mean(0) + 1) if ok.sum() > 50 else np.ones(3)
            lab_c = cv2.cvtColor(np.clip(cur, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
            lab_m = cv2.cvtColor(np.clip(wC * gain, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
            chroma = np.hypot(lab_c[..., 1] - 128, lab_c[..., 2] - 128)
            rem = ((lab_c[..., 0] > 95) & (lab_c[..., 0] < lab_m[..., 0] - 8) & (chroma < 14)).astype(np.float32)
            vis = np.maximum(vis, cv2.GaussianBlur(cv2.dilate(rem, np.ones((3, 3), np.uint8)), (0, 0), 1.5))
            a = (wM * vis)[..., None]
            cur = cur * (1 - a) + (wC * gain) * a
            changed = int((a[..., 0] > 0.5).sum())
        log.append(dict(i=i, pos=None if pos is None else [int(pos[0]), int(pos[1]), round(pos[2], 2)], replaced_px=changed))
        cv2.imwrite(str(out_dir / f.name), np.clip(cur, 0, 255).astype(np.uint8))
    json.dump(log, open(HERE / f"work/{name}_paintout_log.json", "w"), indent=0)
    out = HERE / f"fix/{name}_nosprite.mp4"
    subprocess.run([FF, "-v", "error", "-y", "-framerate", "24", "-i", str(out_dir / "f_%04d.png"), "-i", str(src),
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-shortest", str(out)], check=True)
    print("frames", len(log), "edited", sum(1 for l in log if l["replaced_px"] > 0), "->", out)


if __name__ == "__main__":
    main()

"""Per-event luma (BT.709 Y %, from 8-bit RGB as delivered) of a 1080p film file + one still per event.
usage: python -I measure.py FILE [--sheet out.jpg]"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
FIN = Path(__file__).resolve().parent
sys.path.insert(0, str(FIN)); sys.argv += [] 
import build_final_1080 as B
A = json.loads((FIN / "assembly.json").read_text())
FACES = json.loads((FIN / "faces.json").read_text()) if (FIN / "faces.json").exists() else {}
path = sys.argv[1]; sheet = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--sheet" else None
Y = np.array([0.0722, 0.7152, 0.2126], np.float32)   # BGR
per = {}; stills = {}
for i, f in enumerate(B.frames_of(path, 960, 540)):
    k = A["frames"][i]["event"]; e = A["events"][k]
    y = (f.astype(np.float32) / 255) @ Y * 100
    d = per.setdefault(k, {"y": [], "face": []})
    d["y"].append(y[::2, ::2].ravel())
    fb = FACES.get(str(k))
    if fb:
        x0, y0, x1, y1 = [int(v * s) for v, s in zip(fb, (960, 540, 960, 540))]
        hsv = cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2HSV); yy = y[y0:y1, x0:x1]
        sk = (hsv[..., 0] <= 20) & (hsv[..., 1] > 50) & (hsv[..., 1] < 170) & (hsv[..., 2] > 70)   # lit skin
        if sk.sum() > 200: d["face"].append(np.median(yy[sk]))
    if A["frames"][i]["j"] == A["frames"][i]["n"] // 2:
        stills[k] = f.copy()
rows = []; apl = []
print("ev P   room   mean   p2    p50   p98  p99.9  face")
for k, d in per.items():
    e = A["events"][k]; y = np.concatenate(d["y"])
    face = f"{np.median(d['face']):5.1f}" if d["face"] else "  -  "
    r = dict(event=k, panel=e["panel"], room=e["room"], mean=float(y.mean()), p2=float(np.percentile(y, 2)), p50=float(np.percentile(y, 50)),
             p98=float(np.percentile(y, 98)), p999=float(np.percentile(y, 99.9)), face=float(np.median(d["face"])) if d["face"] else None)
    rows.append(r)
    if e["room"] != "black": apl.append((y.mean(), len(d["y"])))
    print(f"{k:2d} P{e['panel']:<2d} {e['room']:6s} {r['mean']:5.1f} {r['p2']:5.1f} {r['p50']:5.1f} {r['p98']:5.1f} {r['p999']:5.1f}  {face}")
film = float(sum(m * n for m, n in apl) / sum(n for _, n in apl))
print(f"film APL (picture events, frame-weighted) {film:.1f}")
Path(path).with_suffix(".luma.json").write_text(json.dumps({"events": rows, "film_apl": film}, indent=1))
if sheet:
    ts = []
    for k in sorted(stills):
        t = cv2.resize(stills[k], (480, 270)); fb = FACES.get(str(k))
        if fb: cv2.rectangle(t, (int(fb[0] * 480), int(fb[1] * 270)), (int(fb[2] * 480), int(fb[3] * 270)), (0, 255, 0), 1)
        cv2.putText(t, f"ev{k} P{A['events'][k]['panel']}", (5, 16), 0, 0.5, (0, 255, 255), 1); ts.append(t)
    while len(ts) % 4: ts.append(np.zeros_like(ts[0]))
    cv2.imwrite(sheet, np.vstack([np.hstack(ts[r:r + 4]) for r in range(0, len(ts), 4)]), [cv2.IMWRITE_JPEG_QUALITY, 80])

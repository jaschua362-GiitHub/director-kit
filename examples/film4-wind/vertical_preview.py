"""Preview a 9:16 framing plan on the approved 16:9 film (local, free, no enhancement).
usage: python -I work/vertical_preview.py <plan.json> <film.mp4> <out_prefix> [--optionB]
writes <out_prefix>_preview.mp4 (540x960 with the approved audio) and <out_prefix>_board.png (start/mid/end per shot).
Areas that would need AI extension (w > 608) are shown as magenta-hatched bands."""
import sys, json, subprocess, numpy as np, cv2
plan, film, pre = sys.argv[1:4]; OB = '--optionB' in sys.argv
P = json.load(open(plan, encoding='utf-8'))['shots']
cap = cv2.VideoCapture(film); FR = []
while True:
    ok, x = cap.read()
    if not ok: break
    FR.append(x)
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def shot_of(i):
    for s in P:
        if s['f'][0] <= i <= s['f'][1]: return s
def window(i):
    s = shot_of(i); o = s.get('option_B') if OB and s.get('option_B') else s
    u = ease((i - s['f'][0]) / max(1, s['f'][1] - s['f'][0]))
    cx = o['cx'][0] + (o['cx'][1] - o['cx'][0]) * u; w = o['w'][0] + (o['w'][1] - o['w'][0]) * u
    return cx, w
def render(i, OW=540):
    x = FR[min(i, len(FR) - 1)]; cx, w = window(i); h = w * 16 / 9
    x0 = int(round(np.clip(cx - w / 2, 0, 1920 - w))); y0 = int(round(540 - h / 2))
    canvas = np.zeros((int(round(h)), int(round(w)), 3), np.uint8)
    ys, ye = max(0, y0), min(1080, y0 + int(round(h)))
    canvas[ys - y0:ye - y0] = x[ys:ye, x0:x0 + int(round(w))]
    if h > 1080:   # band needing AI extension: hatched preview
        for band in [(0, ys - y0), (ye - y0, canvas.shape[0])]:
            seg = canvas[band[0]:band[1]]
            seg[:] = (60, 20, 60)
            for k in range(-seg.shape[0], seg.shape[1], 24): cv2.line(seg, (k, 0), (k + seg.shape[0], seg.shape[0]), (200, 60, 200), 2)
    return cv2.resize(canvas, (OW, int(OW * 16 / 9)), interpolation=cv2.INTER_AREA)
tmp = pre + '_v.mp4'
o = subprocess.Popen(['ffmpeg', '-v', 'warning', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '540x960', '-r', '24', '-i', 'pipe:0',
                      '-c:v', 'libopenh264', '-b:v', '6M', tmp], stdin=subprocess.PIPE)
for i in range(len(FR)): o.stdin.write(render(i).tobytes())
o.stdin.close(); o.wait()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', film, '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', pre + '_preview.mp4'], check=True)
tiles = []
for s in P:
    a, b = s['f']; row = []
    for i in [a, (a + b) // 2, b]:
        t = render(i, 180); cv2.putText(t, f"{s['id']} f{i}", (4, 14), 0, 0.42, (0, 255, 255), 1); row.append(t)
    tiles.append(np.hstack(row))
cols = 5; rows = []
for r in range(0, len(tiles), cols):
    chunk = tiles[r:r + cols]; chunk += [np.zeros_like(tiles[0])] * (cols - len(chunk))
    rows.append(np.hstack([np.pad(c, ((0, 0), (0, 12), (0, 0))) for c in chunk]))
cv2.imwrite(pre + '_board.png', np.vstack([np.pad(r, ((0, 12), (0, 0), (0, 0))) for r in rows]))
print('ok', pre)

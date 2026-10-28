"""9:16 finish of WIND v07 per edits/vertical_plan_v02.json (Jason-approved plan A + extensions).
Source: the pre-look v07 picture (no grade/grain), so ESRGAN never sees grain; look.py is applied once at the end.
stage crops : sub-pixel window crops of film frames 0..673 -> work/vert/crop/%04d.png (extend shots: the w x 1080 centre only)
stage esr   : Real-ESRGAN x4 (local) on all crops -> work/vert/esr/
stage frames: 70/30 ESRGAN/Lanczos blend to final size -> work/vert/frames/%04d.png (1080x1920); extend shots get the centre
              placed at its scaled position with empty bands + a mask, to be filled by work/vace_fill.py
usage: python -I work/vertical_finish.py <stage>"""
import sys, os, json, subprocess, shutil, numpy as np, cv2
from pathlib import Path
ROOT = Path(__file__).resolve().parent
PLAN = json.load(open(ROOT.parent / 'edits/vertical_plan_v02.json', encoding='utf-8'))['shots']
SRC = ROOT / 'WIND10_director_v07_musicC_picture.mp4'
V = ROOT / 'vert'; CROP, ESR, OUT = V / 'crop', V / 'esr', V / 'frames'
OW, OH = 1080, 1920; NF = 674
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def shot(i):
    for s in PLAN:
        if s['f'][0] <= i <= s['f'][1]: return s
def window(i):
    s = shot(i); o = s['option_B'] if s.get('extend') else s
    u = ease((i - s['f'][0]) / max(1, s['f'][1] - s['f'][0]))
    cx = o['cx'][0] + (o['cx'][1] - o['cx'][0]) * u; w = o['w'][0] + (o['w'][1] - o['w'][0]) * u
    return s, cx, w
def crop(i, frame):
    s, cx, w = window(i); wi = int(round(w))
    cx = float(np.clip(cx, w / 2, 1920 - w / 2))
    return cv2.getRectSubPix(frame, (wi, 1080), (cx, 539.5)), s, w
stage = sys.argv[1]
if stage == 'crops':
    shutil.rmtree(CROP, ignore_errors=True); CROP.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(SRC))
    for i in range(NF):
        ok, f = cap.read(); c, s, w = crop(i, f); cv2.imwrite(str(CROP / f'{i:04d}.png'), c)
    print('crops', NF)
elif stage == 'esr':
    exe = ROOT.parents[1] / 'TEST-005/tools/realesrgan/realesrgan-ncnn-vulkan.exe'
    ESR.mkdir(parents=True, exist_ok=True)
    todo = V / 'todo'; todo.mkdir(exist_ok=True); [f.unlink() for f in todo.glob('*')]
    for p in sorted(CROP.glob('*.png')):
        if not (ESR / p.name).exists(): shutil.copy(p, todo / p.name)
    if any(todo.iterdir()):
        r = subprocess.run([str(exe), '-i', str(todo), '-o', str(ESR), '-m', str(exe.parent / 'models'), '-n', 'realesrgan-x4plus',
                            '-s', '4', '-t', '256', '-j', '2:2:2', '-f', 'png'], cwd=exe.parent, capture_output=True)
        assert r.returncode == 0, r.stderr[-400:]
    print('esr', len(list(ESR.glob('*.png'))))
elif stage == 'frames':
    OUT.mkdir(parents=True, exist_ok=True); (V / 'mask').mkdir(exist_ok=True)
    for i in range(NF):
        s, cx, w = window(i); c = cv2.imread(str(CROP / f'{i:04d}.png')); e = cv2.imread(str(ESR / f'{i:04d}.png'))
        cw = OW if not s.get('extend') else int(round(OW))            # centre always spans full output width
        ch = OH if not s.get('extend') else int(round(1080 * OW / c.shape[1]))   # crop shots fill 1920 exactly
        base = cv2.resize(c, (cw, ch), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        up = cv2.resize(e, (cw, ch), interpolation=cv2.INTER_AREA).astype(np.float32)
        centre = np.clip(0.3 * base + 0.7 * up, 0, 255).astype(np.uint8)
        img = np.zeros((OH, OW, 3), np.uint8); y0 = (OH - ch) // 2
        img[y0:y0 + ch] = centre[:OH] if ch >= OH else centre
        if ch < OH:
            m = np.full((OH, OW), 255, np.uint8); m[y0:y0 + ch] = 0; cv2.imwrite(str(V / 'mask' / f'{i:04d}.png'), m)
        cv2.imwrite(str(OUT / f'{i:04d}.png'), img)
    print('frames', NF)

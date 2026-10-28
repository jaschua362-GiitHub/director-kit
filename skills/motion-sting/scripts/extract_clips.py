"""Real footage -> JPEG sequences the canvas engine can draw frame-exactly.

    python extract_clips.py --project <project> [--fps 30] [--max 1080]

Reads <project>/clips.json:
    [{"id": "pour", "src": "F:/.../clip.mp4", "in": 10.0, "out": 12.4}, ...]
Writes <project>/footage/<id>/f_00001.jpg ... and <project>/footage/manifest.json
    {"pour": {"n": 72, "fps": 30, "w": 608, "h": 1080, "dur": 2.4}, ...}

Why image sequences (not <video>): a <video> element seeks asynchronously and approximately, so an export
would not be a pure function of time. JPEGs at a fixed fps are exact; footage.js decodes only the frames each
export frame needs. Longest side is capped at --max (the engine cover-fits them; 1080 is enough for 9:16).
Rights: only extract footage Jason owns or has licensed for the use. Record the source in BRIEF.md.
"""
import argparse, json, os, shutil, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument('--project', required=True)
ap.add_argument('--fps', type=int, default=30)
ap.add_argument('--max', type=int, default=1080)
a = ap.parse_args()
proj = os.path.abspath(a.project)
clips = json.load(open(os.path.join(proj, 'clips.json'), encoding='utf-8'))
root = os.path.join(proj, 'footage')
os.makedirs(root, exist_ok=True)
man = {}
for c in clips:
    out = os.path.join(root, c['id'])
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    scale = f"scale='if(gt(iw,ih),min({a.max},iw),-2)':'if(gt(iw,ih),-2,min({a.max},ih))'"
    dur = ['-t', str(c['out'] - c.get('in', 0))] if 'out' in c else []   # -ss before -i: fast seek; -t = window length
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(c.get('in', 0)), '-i', c['src']] + dur + [
           '-vf', f"fps={a.fps},{scale}", '-q:v', '3', os.path.join(out, 'f_%05d.jpg')]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"ffmpeg failed on {c['id']}:\n{r.stderr}")
    files = sorted(f for f in os.listdir(out) if f.endswith('.jpg'))
    if not files: sys.exit(f"{c['id']}: no frames extracted (check in/out against the clip length)")
    from PIL import Image
    w, h = Image.open(os.path.join(out, files[0])).size
    man[c['id']] = {'n': len(files), 'fps': a.fps, 'w': w, 'h': h, 'dur': round(len(files) / a.fps, 3)}
    print(f"[clips] {c['id']}: {len(files)} frames {w}x{h}")
json.dump(man, open(os.path.join(root, 'manifest.json'), 'w'), indent=1)
print(f'[clips] manifest -> {os.path.join(root, "manifest.json")}')

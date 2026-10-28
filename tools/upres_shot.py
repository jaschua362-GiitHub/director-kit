"""Shared per-shot finish (adopted 2026-10-27, workflow v1.2 review). Real-ESRGAN x4plus (local, no credits) on the USED range of
ONE original take, plus spare handle frames, -> WxH FFV1. 70/30 blend with Lanczos (TEST-009/010 recipe). NO grain: add grain once,
after grading. Never run this on an assembled lower-resolution picture; upscale each shot from its original clip, then assemble.
usage: python -I tools/upres_shot.py <take.mp4> <in_f> <n_f> <out.mkv> [--handles 12] [--size 1920x1080] [--work <tmp dir>]
Writes <out>.json with the time map: output frame 0 == source frame `first_src_frame`; the used range starts at `used_out_offset`.
"""
import argparse, hashlib, json, os, shutil, subprocess, tempfile
from pathlib import Path
import numpy as np, cv2
# Director Kit: set DCL_FFMPEG when the PATH ffmpeg is missing or blocked, and REALESRGAN_EXE (see SETUP.md).
FFMPEG = os.environ.get('DCL_FFMPEG') or 'ffmpeg'
ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('in_f', type=int); ap.add_argument('n_f', type=int); ap.add_argument('dst')
ap.add_argument('--handles', type=int, default=12); ap.add_argument('--size', default='1920x1080'); ap.add_argument('--work')
a = ap.parse_args()
W, H = map(int, a.size.lower().split('x'))
exe = Path(os.environ.get('REALESRGAN_EXE', 'realesrgan-ncnn-vulkan.exe'))
assert exe.is_file(), 'set REALESRGAN_EXE to the full path of realesrgan-ncnn-vulkan.exe (see SETUP.md)'
cap = cv2.VideoCapture(a.src); total, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS); cap.release()
first = max(0, a.in_f - a.handles); last = min(total - 1, a.in_f + a.n_f - 1 + a.handles)
work = Path(a.work or tempfile.mkdtemp(prefix='upres_')); nat, ai = work / 'n', work / 'ai'
for d in (nat, ai): shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
subprocess.run([FFMPEG, '-v', 'error', '-i', a.src, '-vf', f'select=between(n\\,{first}\\,{last})', '-fps_mode', 'passthrough',
                str(nat / '%04d.png')], check=True)
r = subprocess.run([str(exe), '-i', str(nat), '-o', str(ai), '-m', str(exe.parent / 'models'), '-n', 'realesrgan-x4plus', '-s', '4',
                    '-t', '256', '-j', '2:2:2', '-f', 'png'], cwd=exe.parent, capture_output=True)
assert r.returncode == 0, r.stderr[-500:]
o = subprocess.Popen([FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', f'{fps:g}', '-i', '-',
                      '-c:v', 'ffv1', a.dst], stdin=subprocess.PIPE)
frames = sorted(nat.glob('*.png'))
for f in frames:
    base = cv2.resize(cv2.imread(str(f)), (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    up = cv2.resize(cv2.imread(str(ai / f.name)), (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
    # 2026-10-27 (Shadow T11): the GPU once returned black AI frames mid-batch; the 30 % Lanczos share hid it as a dark shot
    assert base.mean() < 8 or up.mean() > 0.6 * base.mean(), f'Real-ESRGAN frame {f.name} came back dark - rerun this shot'
    o.stdin.write(np.clip(0.3 * base + 0.7 * up, 0, 255).astype(np.uint8).tobytes())
o.stdin.close(); o.wait(); assert o.returncode == 0, 'encode failed'
shutil.rmtree(work, ignore_errors=True)
rec = {'source': a.src, 'source_sha256': hashlib.sha256(open(a.src, 'rb').read()).hexdigest(), 'fps': fps,
       'used_in_f': a.in_f, 'used_n_f': a.n_f, 'first_src_frame': first, 'last_src_frame': last, 'out_frames': len(frames),
       'used_out_offset': a.in_f - first, 'handles_requested': a.handles, 'size': [W, H],
       'method': 'Real-ESRGAN x4plus ncnn-vulkan, 70/30 blend with Lanczos, no grain', 'credits': 0}
json.dump(rec, open(a.dst + '.json', 'w'), indent=1); print('ok', a.dst, len(frames), 'frames; used range starts at out frame', rec['used_out_offset'])

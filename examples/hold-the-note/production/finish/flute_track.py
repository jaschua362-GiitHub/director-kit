"""Shot 10 (16:9) flute-length check, every frame. Decodes with the bundled ffmpeg, scales to 1920x1080 (grey),
tracks horizontal shift of the flute body (rows y0..y1) separately for its LEFT part (x 0-700) and RIGHT end (x 1100-1700)
by 1-D phase correlation against a reference frame. A rigid flute moves both parts together; a length morph makes them
diverge. usage: python flute_track.py FILE [y0 y1 ref]   -> prints per-frame shifts, divergence, longest clean run."""
import sys, subprocess, numpy as np
FF = r"<LAB>\experiments\TEST-001\tools\python-media\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
f = sys.argv[1]; y0 = int(sys.argv[2]) if len(sys.argv) > 2 else 700; y1 = int(sys.argv[3]) if len(sys.argv) > 3 else 730
ref = int(sys.argv[4]) if len(sys.argv) > 4 else 30
r = subprocess.run([FF, "-v", "error", "-i", f, "-vf", "scale=1920:1080:flags=bicubic", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(r, np.uint8).reshape(-1, 1080, 1920).astype(np.float32)
def shift(p, q):
    F = np.fft.fft(p - p.mean()) * np.conj(np.fft.fft(q - q.mean())); c = np.fft.ifft(F / (np.abs(F) + 1e-6)).real
    k = int(np.argmax(c)); return k if k < len(c) // 2 else k - len(c)
L = a[:, y0:y1, 0:700].mean(1); R = a[:, y0:y1, 1100:1700].mean(1)
div = []
for k in range(len(a)):
    sl, sr = shift(L[ref], L[k]), shift(R[ref], R[k]); div.append(abs(sl - sr)); print(k, "left %+d" % sl, "right %+d" % sr, "div %d" % abs(sl - sr))
ok = np.array(div) <= 2; best = (0, 0); s = None
for k, v in enumerate(list(ok) + [False]):
    if v and s is None: s = k
    if not v and s is not None:
        if k - s > best[1] - best[0]: best = (s, k)
        s = None
print("longest clean run (divergence <= 2 px): frames %d-%d (%d frames)" % (best[0], best[1] - 1, best[1] - best[0]))

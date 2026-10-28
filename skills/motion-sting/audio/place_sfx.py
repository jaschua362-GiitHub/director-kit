"""Place recorded / library sound effects so each one's PEAK lands on its event (not the file start).

    python place_sfx.py cues.json out.wav --dur 30 [--gain-db -6]

cues.json: [{"t": 4.20, "file": "sfx/whoosh.wav", "gain": 0.6, "pan": -0.3}, ...]
  t     = the visual event (cut, landing, click) in seconds
  gain  = linear gain (default 1), pan = -1..1 (default 0)
Each file is read with ffmpeg (any format), its peak is found from the smoothed envelope (5 ms window, so a
single-sample spike does not win), and the file is shifted so that peak sits on t. A whoosh's peak is its
loudest moment, often 0.2-0.5 s after the file starts; placing by file start makes every cut feel late.
Output: 48 kHz stereo 24-bit WAV (pre-master; mix with music via mix.py, which masters to -14 LUFS).
Licences: only use effects whose licence allows commercial use; note the source in BRIEF.md.
"""
import argparse, json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfxlib import write_wav24, pan_gains

SR = 48000


def read(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True)
    if r.returncode: sys.exit(f'ffmpeg could not read {path}\n{r.stderr.decode(errors="replace")}')
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).T.copy()


def peak_offset(x):
    env = np.abs(x).max(0)
    k = int(.005 * SR)
    sm = np.convolve(env, np.ones(k) / k, 'same')
    return int(np.argmax(sm))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cues'); ap.add_argument('out')
    ap.add_argument('--dur', type=float, required=True)
    ap.add_argument('--gain-db', type=float, default=0.0)
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.cues))
    cues = json.load(open(a.cues, encoding='utf-8'))
    n = int(a.dur * SR); bus = np.zeros((2, n))
    for c in cues:
        x = read(c['file'] if os.path.isabs(c['file']) else os.path.join(base, c['file']))
        off = peak_offset(x)
        i0 = int(round(c['t'] * SR)) - off
        gl, gr = pan_gains(c.get('pan', 0.0)); g = c.get('gain', 1.0)
        x = np.vstack([x[0] * gl * 1.414, x[1] * gr * 1.414]) * g
        s0, d0 = max(0, -i0), max(0, i0)
        k = min(x.shape[1] - s0, n - d0)
        if k > 0: bus[:, d0:d0 + k] += x[:, s0:s0 + k]
        print(f"[sfx] {os.path.basename(c['file'])}: peak at +{off / SR * 1000:.0f} ms -> starts {i0 / SR:.3f}s, peak on {c['t']:.3f}s")
    bus *= 10 ** (a.gain_db / 20)
    pk = np.abs(bus).max()
    if pk > .89: bus *= .89 / pk; print('[sfx] bus peak limited to -1 dBFS (sample)')
    write_wav24(a.out, bus)
    print(f'[sfx] -> {a.out}')


if __name__ == '__main__':
    main()

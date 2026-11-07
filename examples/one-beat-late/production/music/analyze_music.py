"""Measure a music take before using it (Film 7 lesson: generated music ignores timestamps).

For each file: global tempo (autocorrelation of a spectral-flux onset envelope, 60-140 bpm), tempo stability in 8 s
windows, the beat grid phase, a per-bar loudness map (to find the thin section, the full return and the natural
ending), and the last strong downbeat before the tail. scipy only.

Usage: python -I analyze_music.py take1.mp3 [take2.mp3 ...]  -> <take>.analysis.json + <take>.bars.png
"""
import json, pathlib, subprocess, sys
import numpy as np
from scipy import signal

LAB = pathlib.Path(__file__).resolve().parents[4]
FF = str(LAB / "experiments/TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
SR, HOP = 22050, 256


def load(path):
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def onset_env(y):
    f, t, Z = signal.stft(y, SR, nperseg=1024, noverlap=1024 - HOP)
    mag = np.log1p(np.abs(Z))
    flux = np.maximum(0, np.diff(mag, axis=1)).sum(axis=0)
    flux = flux - signal.medfilt(flux, 31)
    return np.maximum(flux, 0), HOP / SR


def tempo(env, dt, lo=60, hi=140):
    ac = signal.correlate(env - env.mean(), env - env.mean(), mode="full")[len(env) - 1:]
    lags = np.arange(len(ac)) * dt
    bpms = 60 / np.maximum(lags, 1e-9)
    ok = (bpms >= lo) & (bpms <= hi)
    i = np.argmax(np.where(ok, ac, -np.inf))
    # parabolic refinement of the peak lag
    if 0 < i < len(ac) - 1:
        a, b, c = ac[i - 1], ac[i], ac[i + 1]
        i = i + 0.5 * (a - c) / (a - 2 * b + c + 1e-12)
    return 60 / (i * dt)


def phase(env, dt, bpm):
    beat = 60 / bpm
    best = (-1, 0)
    for off in np.arange(0, beat, dt):
        idx = (np.arange(off, len(env) * dt, beat) / dt).astype(int)
        idx = idx[idx < len(env)]
        s = env[idx].sum()
        if s > best[0]:
            best = (s, off)
    return best[1]


def main():
    for p in map(pathlib.Path, sys.argv[1:]):
        y = load(p)
        dur = len(y) / SR
        env, dt = onset_env(y)
        bpm = tempo(env, dt)
        win, step = int(8 / dt), int(4 / dt)
        local = [(round(i * dt, 1), round(float(tempo(env[i:i + win], dt)), 1)) for i in range(0, len(env) - win, step)]
        off = phase(env, dt, bpm)
        beat, bar = 60 / bpm, 240 / bpm
        rms = np.sqrt(np.convolve(y ** 2, np.ones(int(0.05 * SR)) / int(0.05 * SR), "same"))
        nb = int((dur - off) / bar)
        bars = []
        for k in range(nb):
            a, b = int((off + k * bar) * SR), int((off + (k + 1) * bar) * SR)
            bars.append(round(float(20 * np.log10(np.sqrt(np.mean(y[a:b] ** 2)) + 1e-9)), 1))
        loud_db = 20 * np.log10(rms + 1e-9)
        last_loud = np.nonzero(loud_db > loud_db.max() - 30)[0][-1] / SR
        out = {"file": p.name, "duration_s": round(dur, 2), "tempo_bpm": round(float(bpm), 2),
               "tempo_spread_bpm": round(float(np.std([t for _, t in local])), 2) if local else None,
               "local_tempo_8s": local, "beat_s": round(float(beat), 4), "first_downbeat_phase_s": round(float(off), 3),
               "bar_s": round(float(bar), 3), "bar_rms_db": bars, "last_audible_s": round(float(last_loud), 2)}
        p.with_suffix(".analysis.json").write_text(json.dumps(out, indent=1))
        print(p.name, "dur", out["duration_s"], "tempo", out["tempo_bpm"], "spread", out["tempo_spread_bpm"],
              "phase", out["first_downbeat_phase_s"], "bars", len(bars), "last audible", out["last_audible_s"])
        print("  bar loudness dB:", bars)


if __name__ == "__main__":
    main()

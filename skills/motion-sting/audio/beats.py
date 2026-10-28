"""Measure a supplied music track -> beats.json, so the picture can be cut to the music.

    python beats.py audio/track.wav > audio/beats.json        (any format ffmpeg reads: wav, mp3, m4a ...)
    python beats.py audio/track.mp3 --bpm 120 > audio/beats.json   (force the tempo if the guess is off by 2x)

Output (seconds, 3 decimals):
    bpm        measured tempo
    beats      every beat         -> state changes / scene beats go here (T in sting.js)
    downbeats  every bar's beat 1 -> big moments: cuts, morph landings, logo lock
               (bar phase is a guess from kick energy -- listen; fix with --downbeat <sec>)
    hits       strong onsets      -> SFX accents (they may fall between beats)
    duration   track length

Only numpy + scipy + ffmpeg (no librosa), so it runs on both machines as-is.
Method: spectral-flux onset envelope -> tempo by autocorrelation with a 120 BPM prior -> beats by
dynamic programming (Ellis 2007) -> bar phase from low-band (kick) energy. Accurate to ~6 ms on
steady-tempo music; it does not follow tempo changes (rubato, live drummers) -- check the
spectrogram from audio_check.py and say so if the track drifts.
"""
import argparse, json, subprocess, sys
import numpy as np
from scipy.signal import find_peaks, stft

SR, HOP, NFFT = 22050, 256, 1024
FPS = SR / HOP                      # onset-envelope frames per second (~86)
T0 = NFFT / 2 / SR                  # flux frame i is centred at i / FPS + T0 (STFT window centre)


def load(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                       capture_output=True)
    if r.returncode: sys.exit('ffmpeg could not read ' + path + '\n' + r.stderr.decode(errors='replace'))
    return np.frombuffer(r.stdout, np.float32)


def onset_env(y):
    _, _, Z = stft(y, SR, nperseg=NFFT, noverlap=NFFT - HOP, boundary=None, padded=False)
    S = np.log1p(100 * np.abs(Z))                      # compressed magnitude
    flux = np.maximum(0, np.diff(S, axis=1))            # rising energy only
    freqs = np.fft.rfftfreq(NFFT, 1 / SR)
    full = np.concatenate([[0], flux.mean(0)])
    low = np.concatenate([[0], flux[freqs < 150].mean(0)])   # kick band, for the bar phase
    k = int(FPS)                                        # subtract a 1 s moving average (local contrast)
    full = np.maximum(0, full - np.convolve(full, np.ones(k) / k, 'same'))
    return full / (full.std() + 1e-9), low / (low.std() + 1e-9)


def tempo(env, lo=60, hi=200):
    ac = np.correlate(env, env, 'full')[len(env) - 1:]
    lags = np.arange(int(60 * FPS / hi), int(60 * FPS / lo) + 1)
    bpms = 60 * FPS / lags
    prior = np.exp(-.5 * (np.log2(bpms / 120) / 1.0) ** 2)   # log-normal around 120 BPM, 1 octave wide
    score = ac[lags] * prior
    i = int(np.argmax(score))
    if 0 < i < len(lags) - 1:                           # parabolic refinement of the lag
        a, b, c = score[i - 1], score[i], score[i + 1]
        d = .5 * (a - c) / (a - 2 * b + c + 1e-12)
        return float(60 * FPS / (lags[i] + d))
    return float(bpms[i])


def pulse(env, period):
    """Mean onset strength on the best-phased pulse train of this period (max within +-1 frame)."""
    best = 0.0
    for ph in np.arange(0, period, 1.0):
        pos = np.round(np.arange(ph, len(env) - 1, period)).astype(int)
        pos = pos[(pos > 0) & (pos < len(env) - 1)]
        if len(pos): best = max(best, float(np.maximum(np.maximum(env[pos - 1], env[pos]), env[pos + 1]).mean()))
    return best


def octave_fix(env, bpm, hi=180):
    """Autocorrelation loves the kick's period, so a kick on 1 and 3 reads as half tempo (128 -> 64).
    Double while the in-between pulses carry real onsets (snare on 2 and 4 does; hi-hat off-beats don't).
    Measured on synthetic kits: ratio ~0.56 at true->double, >=0.65 at half->true; threshold 0.6."""
    while bpm * 2 <= hi:
        p = 60 * FPS / bpm
        r = pulse(env, p / 2) / pulse(env, p)
        if .57 < r < .63:
            print(f'[beats] WARNING tempo octave ambiguous at {bpm:.1f} / {bpm * 2:.1f} BPM (ratio {r:.2f}); '
                  'tap along and re-run with --bpm if wrong', file=sys.stderr)
        if r < .6: break
        bpm *= 2
    return bpm


def track_beats(env, bpm, tight=100.0):
    period = 60 * FPS / bpm
    n = len(env)
    score, back = env.copy(), -np.ones(n, int)
    w = np.arange(-int(round(2 * period)), -int(round(period / 2)) + 1)
    penalty = -tight * np.log(-w / period) ** 2
    for t in range(n):
        p = t + w
        ok = p >= 0
        if not ok.any(): continue
        cand = score[p[ok]] + penalty[ok]
        j = int(np.argmax(cand))
        score[t] = env[t] + cand[j]
        back[t] = p[ok][j]
    # end on the best-scoring frame among the last period, then backtrack
    t = int(np.argmax(score[-int(period) - 1:]) + n - int(period) - 1)
    beats = []
    while t >= 0:
        beats.append(t); t = back[t]
    beats = np.array(beats[::-1])
    # trim weak beats at the ends (silence / fade-in / fade-out)
    strong = env[beats] > .3 * np.median(env[beats]) if len(beats) else []
    if len(beats) and strong.any():
        i0, i1 = np.argmax(strong), len(strong) - np.argmax(strong[::-1])
        beats = beats[i0:i1]
    return beats


def refine(env, frames):
    """Sub-frame peak position (parabola through the 3 samples around each frame)."""
    out = []
    for f in frames:
        f = int(f)
        if 0 < f < len(env) - 1:
            a, b, c = env[f - 1], env[f], env[f + 1]
            den = a - 2 * b + c
            out.append(f + (.5 * (a - c) / den if den < 0 else 0))
        else:
            out.append(f)
    return np.array(out) / FPS + T0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('track')
    ap.add_argument('--bpm', type=float, help='force the tempo (use when the guess is half/double)')
    ap.add_argument('--beats-per-bar', type=int, default=4)
    ap.add_argument('--downbeat', type=float, help='time (s) of any bar-1 you hear; overrides the phase guess')
    a = ap.parse_args()

    y = load(a.track)
    env, low = onset_env(y)
    bpm = a.bpm or octave_fix(env, tempo(env))
    bf = track_beats(env, bpm)
    beats = refine(env, bf)
    if len(beats) > 8:                                  # report the tempo the beats actually keep
        bpm = 60 / np.median(np.diff(beats))
    n = a.beats_per_bar
    if a.downbeat is not None and len(beats):
        phase = int(round((a.downbeat - beats[0]) / (60 / bpm))) % n   # extrapolate the grid: D may precede beat 0
    else:   # loudest kick-band phase: right on most pop/electronic, a guess on kick-on-1-and-3 patterns
        phase = int(np.argmax([low[bf[p::n]].sum() for p in range(n)])) if len(bf) >= n else 0
    pk, _ = find_peaks(env, height=env.mean() + 1.5 * env.std(), distance=int(.1 * FPS))
    json.dump({
        'bpm': round(float(bpm), 2),
        'beats': [round(float(t), 3) for t in beats],
        'downbeats': [round(float(t), 3) for t in beats[phase::n]],
        'hits': [round(float(t), 3) for t in refine(env, pk)],
        'duration': round(len(y) / SR, 3),
    }, sys.stdout, indent=1)
    sys.stdout.write('\n')
    print(f'[beats] {bpm:.2f} BPM, {len(beats)} beats, first downbeat {beats[phase] if len(beats) else 0:.3f}s, '
          f'{len(pk)} hits', file=sys.stderr)


if __name__ == '__main__':
    main()

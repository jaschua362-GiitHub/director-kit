"""sfxlib — procedural sound-design kit for motion stings (numpy + scipy).

    from sfxlib import *
    m = Mix(dur=10)                                   # 48 kHz stereo, dry bus + reverb send
    m.add(bell(hz(74)), t0=5.28, gain=.2, pan=-.3, rev=.55)
    m.render('sfx.wav')                               # reverb, master HP, peak −1.5 dBFS, 24-bit WAV

Cue every sound from the SAME timeline constants as the animation (copy the T / key times from the
engine), so picture and sound cannot drift. See cues_example.py (the coffee-brand sting) for a full cue sheet.

Speed: sweeping filters run block-wise (RBJ biquad per 128 samples via lfilter + carried state) — a 10 s
sting renders in seconds, not the minutes a per-sample Python filter takes.
Requires: pip install numpy scipy
"""
import wave
import numpy as np
import scipy.signal as ss

SR = 48000
rng = np.random.default_rng(11)


def reseed(s): global rng; rng = np.random.default_rng(s)


# ---------------------------------------------------------------- time + easing (mirror the JS engine)
def clamp(x, a=0.0, b=1.0): return np.minimum(b, np.maximum(a, x))
def seg(t, a, b): return clamp((t - a) / (b - a))
def inout(x): return np.where(x < .5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2)
def inout_sine(x): return -(np.cos(np.pi * x) - 1) / 2
def outexpo(x): return np.where(x >= 1, 1.0, 1 - 2.0 ** (-10 * x))
def hz(midi): return 440.0 * 2 ** ((midi - 69) / 12)
def secs(d): return int(round(d * SR))
def tax(n): return np.arange(n) / SR
def env_ad(n, a, tau):
    t = tax(n); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / tau)


def pan_gains(p):
    a = (np.asarray(p, float) + 1) * np.pi / 4
    return np.cos(a), np.sin(a)


# ---------------------------------------------------------------- sources + filters
def osc(freq, n):
    """Phase-continuous sine; freq may be an array (glides, vibrato, Doppler)."""
    f = np.broadcast_to(np.asarray(freq, float), (n,))
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def pink(n):
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR); f[0] = f[1]
    x = np.fft.irfft(spec / np.sqrt(f), n)
    return x / np.max(np.abs(x))


def brown(n):
    x = ss.sosfilt(ss.butter(1, 20, 'hp', fs=SR, output='sos'), np.cumsum(rng.standard_normal(n)))
    return x / np.max(np.abs(x))


def static(x, kind, f, order=2):
    """Fixed Butterworth: kind 'lp' | 'hp' | 'bp' (f=[lo,hi])."""
    return ss.sosfilt(ss.butter(order, f, kind, fs=SR, output='sos'), x)


def bp_sweep(x, fc, q=1.0, block=128):
    """Band-pass with a moving centre frequency (array or scalar) — RBJ biquad per block, state carried."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    y, zi = np.empty_like(x), np.zeros(2)
    for i in range(0, len(x), block):
        f = float(np.clip(fc[min(i + block // 2, len(x) - 1)], 20, SR * .45))
        w0 = 2 * np.pi * f / SR; al = np.sin(w0) / (2 * q)
        a = np.array([1 + al, -2 * np.cos(w0), 1 - al])
        b = np.array([al, 0, -al]) / a[0]
        y[i:i + block], zi = ss.lfilter(b, a / a[0], x[i:i + block], zi=zi)
    return y


# ---------------------------------------------------------------- instruments
def bell(f, dur=2.8):
    n = secs(dur); t = tax(n)
    parts = [(1, 1, 2.4), (2.0, .3, 1.3), (2.76, .45, .9), (5.4, .14, .35), (8.93, .05, .15)]
    x = sum(a * np.sin(2 * np.pi * f * r * t + r) * np.exp(-t / d) for r, a, d in parts)
    return x * np.minimum(1, t / .003)


def marimba(f, dur=1.1):
    n = secs(dur); t = tax(n)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / .45) + .3 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t / .09)
    x += .06 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t / .03)
    click = static(rng.standard_normal(n), 'bp', [2500, 6000]) * np.exp(-t / .002) * .25
    return (x + click) * np.minimum(1, t / .001)


def glass(f, dur=.9, tau=.35):
    n = secs(dur); t = tax(n)
    return (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 2.01 * t)) * env_ad(n, .004, tau)


def droplet(f0=450, f1=1400, dur=.18):
    n = secs(dur); t = tax(n)
    f = f0 * (f1 / f0) ** np.minimum(1, t / .03)
    return osc(f, n) * env_ad(n, .001, .03) + .3 * osc(f * 2.3, n) * env_ad(n, .001, .012)


def pop(dur=.05):
    """One crackle (first crack, popcorn, fire). Randomised each call."""
    n = secs(dur); t = tax(n)
    nz = static(rng.standard_normal(n), 'bp', [1500, 7500])
    body = np.sin(2 * np.pi * rng.uniform(260, 420) * t) * np.exp(-t / .008) * .5
    return (nz * np.exp(-t / rng.uniform(.0015, .004)) + body) * np.minimum(1, t / .0003)


def tock(f=950):
    n = secs(.08); t = tax(n)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / .012) + static(rng.standard_normal(n), 'bp', [1500, 4000]) * np.exp(-t / .004) * .6


def sub_thump(f0=80, f1=45, dur=.9):
    n = secs(dur); t = tax(n)
    return osc(f0 * (f1 / f0) ** np.minimum(1, t / .15), n) * env_ad(n, .003, .22)


def whoosh(fc, amp, q=.9, hp=140):
    """Pink noise through a moving band-pass. fc/amp are per-sample arrays (drive them from the motion)."""
    n = len(amp)
    x = static(bp_sweep(pink(n), fc, q), 'hp', hp)
    return x / (np.max(np.abs(x)) + 1e-9) * amp


def saw_voice(f0, n, cutoff, harmonics=18, detune_cents=(-5, 0, 5)):
    """Additive band-limited saw; per-harmonic gain follows a (time-varying) low-pass → cheap filter sweeps."""
    t = tax(n)
    cutoff = np.broadcast_to(np.asarray(cutoff, float), (n,))
    out = np.zeros(n)
    for dc in detune_cents:
        f = f0 * 2 ** (dc / 1200)
        for h in range(1, harmonics + 1):
            if f * h > SR / 2.2: break
            out += (1 / h / np.sqrt(1 + (f * h / cutoff) ** 4)) * np.sin(2 * np.pi * f * h * t + h * .7 + dc)
    return out / len(detune_cents)


# ---------------------------------------------------------------- mixer
class Mix:
    def __init__(self, dur):
        self.dur, self.n = dur, int(SR * dur)
        self.dry = np.zeros((2, self.n)); self.wet = np.zeros((2, self.n))

    def add(self, sig, t0, gain=1.0, pan=0.0, rev=0.25):
        """Mono sig (pan scalar or per-sample array) or stereo (2, n). rev = reverb send."""
        if sig.ndim == 1:
            gl, gr = pan_gains(pan); sig = np.vstack([sig * gl, sig * gr])
        i0 = secs(t0)
        if i0 < 0: sig, i0 = sig[:, -i0:], 0
        k = min(sig.shape[1], self.n - i0)
        if k <= 0: return
        self.dry[:, i0:i0 + k] += sig[:, :k] * gain
        self.wet[:, i0:i0 + k] += sig[:, :k] * gain * rev

    def render(self, path, rt_tau=.38, predelay=.018, peak_db=-1.5, hp=28):
        irn = secs(2.6); ti = tax(irn)
        ir = static(rng.standard_normal((2, irn)) * np.exp(-ti / rt_tau), 'lp', 5500, order=1)
        ir[:, :secs(predelay)] = 0
        ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
        verb = np.vstack([ss.fftconvolve(self.wet[c], ir[c])[:self.n] for c in range(2)]) * .9
        mix = static(self.dry + verb, 'hp', hp)
        mix[:, -secs(.08):] *= np.linspace(1, 0, secs(.08))
        mix /= np.max(np.abs(mix)) / 10 ** (peak_db / 20)
        write_wav24(path, mix)
        return mix


def write_wav24(path, stereo):
    pcm = (np.clip(stereo.T, -1, 1) * (2 ** 23 - 1)).astype(np.int32).astype(np.uint32)
    raw = np.zeros((pcm.shape[0], 2, 3), np.uint8)
    for c in range(2):
        raw[:, c, 0], raw[:, c, 1], raw[:, c, 2] = pcm[:, c] & 255, (pcm[:, c] >> 8) & 255, (pcm[:, c] >> 16) & 255
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(2); wf.setsampwidth(3); wf.setframerate(SR); wf.writeframes(raw.tobytes())

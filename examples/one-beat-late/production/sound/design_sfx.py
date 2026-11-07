"""Locally designed sound effects for One Beat Late (free). See ../SOUND_PLAN.md.

One grain-arrival hiss is reused for every arrival (the mix varies its gain and pitch slightly); the melt, the long
arrival cue (P8) and the hand gather (P12) are its softer and longer relatives. Room tones, the heel click on glass,
watch ticks and tones, the rail tick and a breath are also built here, because the ChatCut library was unavailable
(project held by another session). Deterministic (fixed seeds). 48 kHz stereo float WAV.

Usage: python -I design_sfx.py  -> sfx/*.wav
"""
import pathlib
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
OUT = pathlib.Path(__file__).parent / "sfx"
OUT.mkdir(exist_ok=True)


def save(name, x):
    x = np.asarray(x, np.float32)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    x /= np.abs(x).max() + 1e-9
    wavfile.write(OUT / f"{name}.wav", SR, (x * 0.9).astype(np.float32))


def bp(x, lo, hi, order=4):
    return signal.sosfilt(signal.butter(order, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, "lowpass", fs=SR, output="sos"), x)


def env(n, a, d, shape=2.0):
    """attack fraction a, decay from d (fractions of n)"""
    t = np.linspace(0, 1, n)
    e = np.clip(t / max(a, 1e-6), 0, 1) * np.clip((1 - t) / max(1 - d, 1e-6), 0, 1)
    return e ** shape


def granular(dur, lo, hi, density, seed, grain=(0.002, 0.006), swirl=0.0):
    """Many tiny band-passed noise grains; density(t) in grains/s; optional slow stereo swirl."""
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    L = np.zeros(n); R = np.zeros(n)
    t = 0.0
    while t < dur:
        d = max(density(t / dur), 1.0)
        t += rng.exponential(1.0 / d)
        if t >= dur:
            break
        gl = int(rng.uniform(*grain) * SR)
        g = rng.normal(0, 1, gl) * np.hanning(gl)
        i = int(t * SR)
        pan = 0.5 + 0.5 * np.sin(2 * np.pi * swirl * t + rng.uniform(-0.6, 0.6)) if swirl else rng.uniform(0.3, 0.7)
        amp = rng.uniform(0.4, 1.0)
        L[i:i + gl] += g[: n - i] * amp * (1 - pan)
        R[i:i + gl] += g[: n - i] * amp * pan
    return np.stack([bp(L, lo, hi), bp(R, lo, hi)], 1)


# ---- the hiss family ----
# arrival: grains swirl in, thicken, then settle into a softer lower texture (0.8 s)
arr = granular(0.8, 2800, 9000, lambda u: 9000 * np.sin(np.pi * min(u / 0.8, 1)) ** 1.5 + 400, 1, swirl=1.6)
settle = granular(0.8, 1200, 3500, lambda u: 2500 * np.exp(-((u - 0.82) / 0.12) ** 2), 2)
x = arr + 0.7 * settle
save("hiss_arrival", x * env(len(x), 0.08, 0.7, 1.2)[:, None])
# melt: airy, sparse, longer, quieter character (1.2 s)
m = granular(1.2, 1800, 6500, lambda u: 2200 * (1 - u) ** 1.5 + 150, 3, grain=(0.004, 0.012))
save("hiss_melt", m * env(len(m), 0.15, 0.3, 1.5)[:, None])
# long arrival cue (P8): slow build, clear and bright, settles (1.6 s)
la = granular(1.6, 3200, 11000, lambda u: 7000 * np.sin(np.pi * min(u / 0.85, 1)) ** 2 + 300, 4, swirl=0.7)
la += 0.6 * granular(1.6, 1300, 3600, lambda u: 2200 * np.exp(-((u - 0.85) / 0.1) ** 2), 5)
save("hiss_long", la * env(len(la), 0.3, 0.75, 1.3)[:, None])
# hand gather (P12): density rises as the grains gather, low-pass opens, held for the fade (2.6 s)
gth = granular(2.6, 1500, 8000, lambda u: 6000 * min(u / 0.4, 1) ** 1.2 * (0.8 + 0.2 * np.sin(9 * u)) + 300, 6,
               grain=(0.003, 0.009), swirl=0.4)
save("hiss_gather", gth * env(len(gth), 0.35, 0.98, 1.0)[:, None])

# ---- small sounds ----
def heel(seed, pitch=1.0):
    rng = np.random.default_rng(seed)
    n = int(0.16 * SR); t = np.arange(n) / SR
    click = rng.normal(0, 1, n) * np.exp(-t / 0.0015)
    ring = sum(a * np.sin(2 * np.pi * f * pitch * t) * np.exp(-t / d) for f, a, d in
               [(2150, 0.5, 0.035), (3420, 0.35, 0.025), (5300, 0.25, 0.015), (7900, 0.12, 0.01)])
    thump = 0.6 * np.sin(2 * np.pi * 115 * t) * np.exp(-t / 0.02)
    return bp(click, 1500, 12000, 2) * 0.8 + ring * 0.5 + thump


for k, p in enumerate([1.0, 0.97, 1.03, 0.94]):
    save(f"heel_glass_{k}", heel(10 + k, p))
save("heel_touch_soft", lp(heel(20, 0.92), 3500) * env(int(0.16 * SR), 0.05, 0.2, 1.0))
t = np.arange(int(0.03 * SR)) / SR
save("watch_tick", np.sin(2 * np.pi * 1500 * t) * np.exp(-t / 0.004) + 0.3 * np.random.default_rng(30).normal(0, 1, len(t)) * np.exp(-t / 0.001))
t = np.arange(int(0.22 * SR)) / SR
save("watch_tone", np.sin(2 * np.pi * 1760 * t) * env(len(t), 0.1, 0.5, 1.0) + 0.3 * np.sin(2 * np.pi * 2640 * t) * env(len(t), 0.1, 0.4, 1.5))
t = np.arange(int(0.42 * SR)) / SR                         # Jason: her watch should alert her before she checks it (P2)
a1 = np.sin(2 * np.pi * 1320 * t) * env(len(t), 0.02, 0.25, 1.4) * (t < 0.2)
a2 = np.sin(2 * np.pi * 1760 * t) * env(len(t), 0.02, 0.6, 1.4) * (t >= 0.18)
save("watch_alert", a1 + a2 + 0.25 * np.sin(2 * np.pi * 2640 * t) * (t >= 0.18) * env(len(t), 0.02, 0.5, 2))
t = np.arange(int(0.06 * SR)) / SR
save("rail_tick", np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.012) + 0.4 * np.sin(2 * np.pi * 3900 * t) * np.exp(-t / 0.008))
br = np.random.default_rng(40).normal(0, 1, int(1.1 * SR))
save("breath_soft", bp(br, 350, 2600, 2) * env(len(br), 0.35, 0.55, 1.6))

# ---- room tones (12 s, loopable by crossfade in the mix) ----
n = int(12 * SR); t = np.arange(n) / SR; rng = np.random.default_rng(50)
hum = 0.5 * np.sin(2 * np.pi * 55 * t) + 0.25 * np.sin(2 * np.pi * 110 * t) + 0.08 * np.sin(2 * np.pi * 165 * t)
pink = lp(rng.normal(0, 1, n), 380, 1)
vent = bp(rng.normal(0, 1, n), 300, 1400, 2) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * t))
moon = 0.35 * hum + 1.2 * pink + 0.5 * vent
save("room_moon", np.stack([moon, np.roll(moon, 2400)], 1))
brown = lp(np.cumsum(rng.normal(0, 1, n)) * 0.01, 600, 2)
traffic = np.zeros(n)
for k in range(7):                                         # distant cars passing behind the glass
    c, w = rng.uniform(0, 12), rng.uniform(1.5, 3.5)
    traffic += np.exp(-((t - c) / w) ** 2) * lp(rng.normal(0, 1, n), rng.uniform(250, 500), 2)
air = bp(rng.normal(0, 1, n), 2500, 7000, 2) * 0.05
city = brown * 3 + traffic * 1.5 + air
save("room_earth_dusk", np.stack([city, np.roll(city, 3600)], 1))
print("wrote", sorted(p.name for p in OUT.glob("*.wav")))

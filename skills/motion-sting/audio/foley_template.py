# TEMPLATE (from the coffee-brand brand-model promo v11): foley bed under music. Set CUT to the edit's cut times.
"""v5 foley bed under the music (15 s, 48 kHz stereo): grinder, pours, drips, glass clink, whoosh into the logo."""
import numpy as np, scipy.signal as ss, wave, sys

SR, DUR = 48000, 15.0
N = int(SR * DUR)
rng = np.random.default_rng(5)
out = np.zeros((2, N))
CUT = dict(open=0.0, grind=1.077, brew=2.323, drip=3.568, present=6.727, cup=9.85, match=10.484)

def tax(n): return np.arange(n) / SR
def sos(kind, f, order=2): return ss.butter(order, f, kind, fs=SR, output='sos')
def place(sig, t0, g=1.0, pan=0.0):
    a = (pan + 1) * np.pi / 4; i0 = int(t0 * SR); n = min(len(sig), N - i0)
    out[0, i0:i0+n] += sig[:n] * g * np.cos(a); out[1, i0:i0+n] += sig[:n] * g * np.sin(a)
def env(n, a, r):
    t = tax(n); d = n / SR
    return np.clip(t / a, 0, 1) * np.clip((d - t) / r, 0, 1)

# grinder: motor hum + burr grit, 0-2.3 s
L = int(2.4 * SR); t = tax(L)
hum = sum(np.sin(2*np.pi*f*t) * a for f, a in [(118, 1), (236, .5), (354, .25)])
grit = ss.sosfilt(sos('bandpass', [1200, 6000]), rng.standard_normal(L)) * (1 + .4*np.sin(2*np.pi*23*t))
L = int(1.35 * SR); t = tax(L)
hum = sum(np.sin(2*np.pi*f*t) * a for f, a in [(118, 1), (236, .5), (354, .25)])
grit = ss.sosfilt(sos('bandpass', [1200, 6000]), rng.standard_normal(L)) * (1 + .4*np.sin(2*np.pi*23*t))
place((hum * .25 + grit * .6) * env(L, .012, .3), CUT['grind'], 0.13, -0.2)
# grinder start: switch click + burr bite on frame 0
L = int(.25 * SR); t = tax(L)
place((ss.sosfilt(sos('bandpass', [800, 7000]), rng.standard_normal(L)) * np.exp(-t/.03) + np.sin(2*np.pi*90*t)*np.exp(-t/.06)), CUT['grind'], 0.18, -0.2)

# kettle pour (thin stream) under the frontal brew and the drip close-up
for t0, d, g in [(0.0, 1.1, .08), (CUT['brew'] + .05, 1.2, .07), (CUT['drip'], 3.1, .06)]:
    L = int(d * SR); t = tax(L)
    p = ss.sosfilt(sos('bandpass', [900, 5500]), rng.standard_normal(L)) * (1 + .2*np.sin(2*np.pi*6*t))
    place(p * env(L, .15, .4), t0, g, 0.05)
# drips into the server
for k in range(7):
    L = int(.18 * SR); t = tax(L); f = np.linspace(950, 1800, L)
    place(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/.035), CUT['drip'] + .25 + k * .32 + rng.random()*.08, .05, .15)
# glass server swirl + cup clink at the presentation
L = int(1.2 * SR); t = tax(L)
sw = ss.sosfilt(sos('bandpass', [300, 2000]), rng.standard_normal(L)) * np.sin(np.pi*t/1.2)**2
place(sw, CUT['present'] + .3, .05, -.1)
L = int(.8 * SR); t = tax(L)
cl = sum(np.sin(2*np.pi*f*t) * np.exp(-t/d) for f, d in [(2650, .25), (4120, .15), (5900, .08)])
place(cl * np.minimum(1, t/.002), CUT['present'] + 2.4, .05, .2)
# cup down + whoosh into the match cut
L = int(.35 * SR); t = tax(L)
c = (np.sin(2*np.pi*190*t)*.8 + np.sin(2*np.pi*420*t)*.3) * np.exp(-t/.05)
place(c, CUT['cup'] + .05, .12, -.1)
L = int(.7 * SR); t = tax(L)
w = ss.sosfilt(sos('bandpass', [300, 3000]), rng.standard_normal(L)) * (np.clip(t/.6, 0, 1)**3) * np.clip((.7 - t)/.1, 0, 1)
place(w, CUT['match'] - .6, .08)

out = ss.sosfilt(sos('highpass', 40), out)
out *= 0.5 / max(1e-9, np.abs(out).max())
path = sys.argv[1] if len(sys.argv) > 1 else 'foley_v5.wav'
with wave.open(path, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((np.clip(out.T, -1, 1) * 32767).astype('<i2').tobytes())
print('wrote', path)

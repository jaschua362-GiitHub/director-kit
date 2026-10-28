"""Worked example: the coffee-brand logo sting cue sheet (10 s, D major), built on sfxlib.

Pattern to copy for a new sting:
  1. Mirror the engine's timeline constants (T, key times, camera/snake timings) at the top.
  2. One block per story beat; derive envelopes, filter sweeps and pans from the SAME easing the
     picture uses (e.g. whoosh loudness = speed of the moving element, pan = its x position).
  3. Tonal elements share one key; chimes land on "closing" moments; the resolve chord carries the hold.
  4. m.render(), then python audio_check.py sfx.wav --sections ... to verify timing + balance.
Run:  python cues_example.py   → brand_sting_sfx.wav
"""
from sfxlib import *

m = Mix(dur=10.0)
DUR = m.dur

# ---------------------------------------------------------------- timeline (mirrors sting.js)
roast = (2.6, 4.05)
def roastP(t): return inout(seg(t, *roast))
def t_of_roast(p):
    lo, hi = roast
    for _ in range(50):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if roastP(m) < p else (lo, m)
    return lo
crackT = t_of_roast(.78)
SNAKE = dict(t0=3.98, dur=1.3, stagger=.07)
D = dict(D2=38, A2=45, D3=50, A3=57, D4=62, E4=64, Fs4=66, A4=69, B4=71, Cs5=73, D5=74, E5=76, Fs5=78,
         A5=81, B5=83, D6=86, E6=88, Fs6=90, A6=93, B6=95, D7=98)
F = {k: hz(v) for k, v in D.items()}

# ================================================================ 1. SEED (0.1–1.35)
n = secs(1.6); t = 0.0 + tax(n)
u = inout(seg(t, .10, 1.35))
speed = np.gradient(u) * SR; speed /= speed.max()
m.add(whoosh(300 + 2600 * u * speed + 200, speed ** 1.3 * .9, q=1.1), 0.0, gain=.55, pan=-.9 + .9 * u, rev=.35)
glint = osc(F['D5'] * 2 ** (u * 7 / 12) * (1 + .004 * np.sin(2 * np.pi * 5 * t)), n) * speed ** 1.5 * .5
m.add(glint, 0.0, gain=.12, pan=-.9 + .9 * u, rev=.5)
m.add(glass(F['A5'], 1.4, .5), 1.33, gain=.22, pan=0, rev=.55)                       # arrival ping
m.add(glass(F['D6'], 1.2, .4), 1.36, gain=.08, pan=.1, rev=.6)

# ================================================================ 2. BEAN OPENS (1.22–2.35)
n = secs(1.4); t = tax(n)
air = ss.sosfilt(ss.butter(2, 2500, 'hp', fs=SR, output='sos'), pink(n))
m.add(air * (np.minimum(1, t / .3) ** 2) * np.exp(-np.maximum(0, t - .3) / .35) * .5, 1.0, gain=.35, pan=0, rev=.5)
fan_notes = ['Fs6', 'A6', 'D6', 'B6', 'E6', 'A6', 'D7', 'Fs6', 'B6', 'E6', 'A6', 'D7']
for i, nm in enumerate(fan_notes):                                                 # one plink per meridian
    m.add(glass(F[nm], .8, .22), 1.40 + i * .048, gain=.055 * (1 - i / 20), pan=(-1) ** i * (.15 + .03 * i), rev=.6)
n = secs(.75); t = tax(n); e = inout(seg(t, 0, .6))                                # crease grows both ways
cr_env = np.sin(np.pi * clamp(t / .7)) ** 2
m.add(osc(F['A5'] * 2 ** (e * 7 / 12), n) * cr_env, 1.75, gain=.07, pan=.15, rev=.5)
m.add(osc(F['A5'] * 2 ** (-e * 5 / 12), n) * cr_env, 1.75, gain=.07, pan=-.15, rev=.5)

# ================================================================ 3. ROAST (2.2–4.3)
t0r, t1r = 2.2, 5.9
n = secs(t1r - t0r); t = t0r + tax(n)
p = roastP(t)
fillA = seg(t, 2.25, 2.8)
cut = 220 + 1300 * p ** 1.4                                                        # heat opens the filter
drone_amp = fillA * (1 - seg(t, 5.25, 5.85)) * (.7 + .3 * p)
drone = (saw_voice(F['D2'], n, cut) + .7 * saw_voice(F['A2'], n, cut) + .35 * saw_voice(F['D3'], n, cut * 1.2))
m.add(drone * drone_amp, t0r, gain=.21, pan=0, rev=.25)
# drum tumble: brown rumble amplitude-modulated by the drum's accelerating rotation
rot = np.cumsum(1.2 + 2.5 * p) / SR
rumble = ss.sosfilt(ss.butter(2, [45, 190], 'bp', fs=SR, output='sos'), brown(n))      # no sub below 45 Hz
rumble *= (1 + .35 * np.sin(2 * np.pi * rot)) * seg(t, 2.5, 3.0) * (1 - seg(t, 4.0, 4.5))
m.add(rumble / (np.abs(rumble).max() + 1e-9), t0r, gain=.13, pan=0, rev=.1)
sizzle = ss.sosfilt(ss.butter(2, 5000, 'hp', fs=SR, output='sos'), rng.standard_normal(n))
m.add(sizzle * p ** 2 * (1 - seg(t, 3.9, 4.3)) * .5, t0r, gain=.05, pan=0, rev=.2)

# baseline ticks (major ticks only) as the axis draws left → right
for i in range(9):
    frac = i * 200 / 1580
    tt_ = 2.45 + .6 * float(np.interp(frac, inout(np.linspace(0, 1, 400)), np.linspace(0, 1, 400)))
    m.add(pop(.03) * .6, tt_, gain=.05, pan=-.8 + 1.6 * frac, rev=.3)

# the roast curves, sonified: each line's value drives a soft tone, panned with its tip
def bt(u): return .08 + .5 * np.exp(-u / .05) + .74 * (1 - np.exp(-u / .45))
def et(u): return .74 - .07 * np.exp(-u / .1) + .12 * u + .012 * np.sin(u * 9)
def ror(u): return .06 + .62 * (1 - np.exp(-u / .05)) * np.exp(-u / .5)
n = secs(1.8); t = 2.55 + tax(n); uu = roastP(t)
son_env = seg(t, 2.55, 2.85) * (1 - seg(t, 3.95, 4.3))
for fn, base, g in ((bt, F['D4'], .07), (et, F['A4'], .035), (ror, F['D4'] / 2, .045)):
    fr = base * 2 ** (2 * (fn(uu) - fn(0.3)))
    tone = osc(fr, n) + .2 * osc(fr * 2, n)
    m.add(tone * son_env, 2.55, gain=g, pan=-.8 + 1.6 * uu, rev=.45)

# label blips as each roast stage is reached
for u_lab in (0.0, .3, .55):
    tl = 2.72 if u_lab == 0 else t_of_roast(u_lab)
    m.add(glass(F['E6'], .5, .08), tl, gain=.08, pan=(-790 + 1580 * u_lab) / 960 * .9, rev=.35)
m.add(glass(F['E6'], .5, .08), 4.02, gain=.07, pan=.85, rev=.35)                    # DROP

# heat-ring pulses
for st in (2.8, 3.15, 3.5, 3.85):
    n = secs(1.0); t = tax(n)
    m.add(osc(F['D3'] * (1 + .02 * t), n) * np.sin(np.pi * clamp(t / 1.0)) ** 2, st, gain=.04, pan=0, rev=.4)

# ================================================================ 4. FIRST CRACK
pre = [crackT - .12, crackT - .07, crackT - .035]
dense = crackT + np.sort(rng.gamma(1.4, .11, 34))
for tp in list(pre) + list(dense[dense < crackT + .7]):
    m.add(pop(), float(tp), gain=rng.uniform(.18, .42), pan=rng.uniform(-.6, .6), rev=.22)
n = secs(.9); t = tax(n)
m.add(osc(80 * (45 / 80) ** np.minimum(1, t / .15), n) * env_ad(n, .003, .22), crackT, gain=.55, pan=0, rev=.08)   # sub thump
puff = ss.sosfilt(ss.butter(2, [900, 4000], 'bp', fs=SR, output='sos'), rng.standard_normal((2, n)))
m.add(puff * env_ad(n, .005, .18) * .5, crackT, gain=.22, rev=.35)

# ================================================================ 5. LINES FLY + RINGS (3.95–5.6)
ring_close = []
for k, (base, bellnote, rho, phi0) in enumerate(((F['A3'], 'A4', 378, -np.pi / 2 - .45),
                                                  (F['D4'], 'D5', 270, -np.pi / 2),
                                                  (F['Fs4'], 'Fs5', 184, -np.pi / 2 + .45))):
    a = SNAKE['t0'] + k * SNAKE['stagger']; b = a + SNAKE['dur']
    ring_close.append(b)
    n = secs(b - a + .15); t = a + tax(n)
    h = 1 + 2 * inout(seg(t, a, b))
    w = clamp(h - 1); v = clamp(h - 2)
    bump = np.sin(np.pi * w) ** 2
    sp = np.gradient(h) * SR; sp /= sp.max()
    near = np.where(h < 2, bump, 0)
    amp = sp * (.25 + .9 * near) * (1 - .6 * (h >= 2))
    fc = 450 + 2600 * near + 700 * sp
    phi = phi0 - 2 * np.pi * v
    pan = np.where(h < 2, .85 - .6 * w, np.cos(phi) * rho / 450)                  # circles the stereo field
    m.add(whoosh(fc, amp, q=1.2), a, gain=.34, pan=pan, rev=.3)
    dop = np.gradient(bump) * SR                                                  # approaching → sharp, receding → flat
    whistle = osc(base * 2 * (1 + .035 * np.tanh(dop / 3)), n) * sp * (.3 + near) * (1 - seg(t, b - .1, b + .1))
    m.add(whistle, a, gain=.045, pan=pan, rev=.45)
    m.add(bell(F[bellnote], 3.2), b - .01, gain=.2, pan=np.cos(phi0) * .35, rev=.55)  # ring closes → chime

# ================================================================ 6. WIPE → CREAM, CUP (5.3–6.55)
n = secs(1.1); t = tax(n)
open_air = ss.sosfilt(ss.butter(2, 1200, 'hp', fs=SR, output='sos'), rng.standard_normal((2, n)))
m.add(open_air * np.sin(np.pi * clamp(t / 1.0)) ** 2 * .5, 5.25, gain=.12, rev=.5)
for i, (st, f0, f1) in enumerate(((5.36, 420, 1350), (5.51, 520, 1600), (5.66, 600, 1800))):
    m.add(droplet(f0, f1), st, gain=.28 * (1 - .25 * i), pan=(-.1, .12, -.05)[i], rev=.5)
n = secs(.08); t = tax(n)                                                         # handle "tock"
m.add((np.sin(2 * np.pi * 950 * t) * np.exp(-t / .012) +
     ss.sosfilt(ss.butter(2, [1500, 4000], 'bp', fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-t / .004) * .6),
    5.47, gain=.14, pan=-.35, rev=.3)
# pour: splash in, bubbly stream, pull-through swish, last drips
m.add(whoosh(np.linspace(3000, 1500, secs(.25)), env_ad(secs(.25), .01, .08), q=.8), 5.72, gain=.18, pan=0, rev=.35)
t_a, t_b = 5.75, 6.45
for tp in np.sort(rng.uniform(t_a, t_b, 110)):
    m.add(droplet(rng.uniform(700, 1600), rng.uniform(1700, 3200), .06), float(tp), gain=rng.uniform(.012, .03),
        pan=rng.uniform(-.2, .2), rev=.3)
n = secs(t_b - t_a); t = tax(n)
hiss = ss.sosfilt(ss.butter(2, [1800, 5000], 'bp', fs=SR, output='sos'), rng.standard_normal(n))
m.add(hiss * np.sin(np.pi * clamp(t / (t_b - t_a))) ** .5 * .5, t_a, gain=.05, pan=0, rev=.3)
n = secs(.4); t = tax(n)
m.add(whoosh(1000 + 4000 * inout(clamp(t / .3)), np.sin(np.pi * clamp(t / .3)) ** 2, q=1.4), 6.18, gain=.2,
    pan=.25 - .55 * clamp(t / .3), rev=.35)
for tp, f0 in ((6.5, 600), (6.64, 750)):
    m.add(droplet(f0, f0 * 2.8), tp, gain=.12, pan=0, rev=.5)

# ================================================================ 7. LOGO (6.5–10)
n = secs(.7); t = tax(n)
m.add(whoosh(3200 * (500 / 3200) ** clamp(t / .58), np.sin(np.pi * clamp(t / .58)) ** 1.5, q=1.0), 6.5, gain=.22,
    pan=-.1 * clamp(t / .58), rev=.35)
letters = [('C', 6.80, 'D5', -.32), ('F1', 6.86, 'E5', .12), ('F2', 6.92, 'Fs5', .3),
           ('N', 6.94, 'A5', -.45), ('A', 6.99, 'B5', -.28), ('T', 7.04, 'D6', -.1),
           ('U', 7.09, 'E6', .08), ('R', 7.14, 'Fs6', .26), ('E', 7.19, 'A6', .44)]
for i, (_, tl, nm, pn) in enumerate(letters):
    m.add(marimba(F[nm]), tl + .03, gain=.16 - .006 * i, pan=pn, rev=.4)
n = secs(1.4); t = tax(n)                                                          # landing: sub + bell
m.add(osc(F['D2'] * 2, n) * env_ad(n, .01, .45), 7.08, gain=.3, pan=0, rev=.15)
m.add(bell(F['D6'], 3.0), 7.1, gain=.1, pan=0, rev=.65)
for i in range(27):                                                                # tagline sparkle, left → right
    m.add(glass(rng.uniform(4200, 7200), .15, .04), 7.2 + i * .008 + rng.uniform(0, .01), gain=.018,
        pan=-.5 + i / 26, rev=.5)
t0c = 6.9; n = secs(DUR - t0c); t = t0c + tax(n)                                   # resolve chord, fades to silence
cenv = seg(t, 6.9, 7.6) ** 1.5 * (1 - seg(t, 8.2, 9.95)) ** 2
chord = sum(saw_voice(F[nm], n, 900 + 300 * np.sin(2 * np.pi * .15 * t), harmonics=10) * g
            for nm, g in (('D3', .38), ('A3', .4), ('D4', .4), ('Fs4', .32), ('E5', .18), ('A4', .25)))
m.add(chord * cenv, t0c, gain=.22, pan=0, rev=.5)
m.add(np.vstack([osc(F['D5'] * 1.002, n), osc(F['D5'] * .998, n)]) * cenv * .5, t0c, gain=.05, rev=.6)


m.render('brand_sting_sfx.wav')
print(f'crackT={crackT:.3f}s  rings close at {", ".join(f"{x:.2f}" for x in ring_close)}')

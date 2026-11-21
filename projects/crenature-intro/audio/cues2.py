"""Crenature intro v4+ ("light carves the dragon") - synthesised sound from the picture's timeline.

    python audio/cues2.py      -> audio/crenature_v4_sfx.wav

Blade sweep loudness = speed of the rim-light front along the dragon, pan = its screen x.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'build'))
from sfxlib import *          # noqa
import render2 as R           # noqa

m = Mix(dur=R.DUR)
reseed(11)
N = {'D1': 26, 'D2': 38, 'A2': 45, 'D3': 50, 'F3': 53, 'A3': 57, 'D4': 62, 'F4': 65, 'A4': 69,
     'D5': 74, 'A5': 81, 'D6': 86, 'E6': 88, 'A6': 93}
F = {k: hz(v) for k, v in N.items()}
A = R.Assets()
n = m.n; t = tax(n)

# light-front speed and screen x
tf = np.linspace(0, R.DUR, int(R.DUR * 240) + 1)
fr = np.array([R.front(x) for x in tf])
idx = np.clip(fr, 0, 1) * (len(A.P) - 1)
pts = A.P[idx.astype(int)]
sx = []
for x, (px, py) in zip(tf, pts):
    fx, fy, z, rot = R.camera(x, A)
    sx.append(R.W / 2 + ((px - fx) * np.cos(rot) - (py - fy) * np.sin(rot)) * 0.5 * z)
sx = np.array(sx)
spd = np.abs(np.gradient(fr, tf)); spd = spd / spd.max()
spd_a = np.interp(t, tf, spd)
pan_a = np.clip(np.interp(t, tf, sx) / R.W * 2 - 1, -.9, .9)
E = np.array([R.light_level(x) for x in tf]); E_a = np.interp(t, tf, E)

# 1. dark bed: low drone + air, ducks when the lights come up
drone = (osc(F['D1'], n) * .6 + osc(F['D2'] * 1.002, n) * .4) * seg(t, 0, .6) * (1 - .75 * E_a)
m.add(drone, 0, gain=.16, pan=0, rev=.15)
air = static(brown(n), 'lp', 500) * seg(t, 0, .5) * (1 - .6 * E_a)
m.add(air / np.max(np.abs(air)), 0, gain=.08, pan=0, rev=.2)

# 2. eye opens: breath swell + glass shimmer as it reaches full glow
nb = secs(.5); br = bp_sweep(pink(nb), np.linspace(300, 1400, nb), q=1.2) * np.sin(np.pi * np.linspace(0, 1, nb)) ** 2
m.add(br / np.max(np.abs(br)), R.T_EYE0, gain=.10, pan=.2, rev=.4)
m.add(glass(F['A5'], 1.4, .5), R.T_EYE1 - .04, gain=.12, pan=.25, rev=.65)
m.add(glass(F['E6'], 1.2, .4), R.T_EYE1 - .01, gain=.05, pan=.3, rev=.7)

# 3. the rim-light front: a metallic blade sweep (resonant high band) following its speed and x
blade = bp_sweep(pink(n), 2600 + 4200 * spd_a, q=6.0) * spd_a ** 1.2 * seg(t, R.T_TRACE0 - .05, R.T_TRACE0 + .1)
m.add(blade / np.max(np.abs(blade)), 0, gain=.22, pan=pan_a, rev=.35)
ring = osc(F['D6'] * (1 + .002 * np.sin(2 * np.pi * 6 * t)), n) * spd_a ** 2 * .5
m.add(ring, 0, gain=.05, pan=pan_a, rev=.5)

# 4. riser into the light burst, then a hard hit (sub + clack + bright burst)
nr = secs(.6); tr = tax(nr)
riser = bp_sweep(pink(nr), np.linspace(400, 5200, nr), q=1.8) * (tr / tr[-1]) ** 2.2
m.add(riser / np.max(np.abs(riser)), R.T_LIGHT_HIT - .6, gain=.28, pan=0, rev=.3)
m.add(sub_thump(85, 40, 1.1), R.T_LIGHT_HIT, gain=.42, pan=0, rev=.1)
m.add(tock(1800), R.T_LIGHT_HIT, gain=.30, pan=0, rev=.3)
nh = secs(.35); hit = static(pink(nh), 'hp', 2500) * np.exp(-tax(nh) / .06)
m.add(hit / np.max(np.abs(hit)), R.T_LIGHT_HIT, gain=.16, pan=0, rev=.5)

# 5. wordmark cuts: one crisp tick per letter, rising slightly in pitch, panned left -> right
for i in range(9):
    m.add(tock(2100 + 90 * i), R.T_TYPE0 + i * R.T_TYPE_STEP, gain=.12, pan=-.15 + .08 * i, rev=.2)

# 6. blink chime, glint shimmer in the hold
m.add(glass(F['D6'], .9, .3), R.T_BLINK + .14, gain=.12, pan=-.3, rev=.55)
for k, d, g in (('A5', 0, .09), ('D6', .03, .07), ('A6', .06, .04)):
    m.add(glass(F[k], 1.2, .45), R.T_GLINT + d, gain=g, pan=-.25, rev=.7)

# 7. low chord under the lit studio, decaying to silence inside the film
t0 = R.T_LIGHT_HIT + .05
for k, g in (('D3', .16), ('A3', .11), ('D4', .09), ('F4', .07)):
    b = bell(F[k], R.DUR - t0)
    b *= np.linspace(1, 0, len(b)) ** 1.5
    m.add(b, t0, gain=g, pan=0, rev=.5)

out = os.path.join(HERE, 'crenature_v4_sfx.wav')
m.render(out)
print('wrote', out)

"""Crenature intro - synthesised sound, cued from the picture's own timeline (D minor).

    python audio/cues.py            -> audio/crenature_sfx.wav

Whoosh loudness/brightness = the dragon head's real speed, pan = its screen x (from build/render.py).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'build'))
from sfxlib import *          # noqa
import render as R            # noqa  (chdirs to the project root)

m = Mix(dur=R.DUR)
reseed(7)
N = {'D2': 38, 'A2': 45, 'D3': 50, 'F3': 53, 'A3': 57, 'C4': 60, 'D4': 62, 'F4': 65, 'G4': 67, 'A4': 69,
     'C5': 72, 'D5': 74, 'F5': 77, 'G5': 79, 'A5': 81, 'D6': 86}
F = {k: hz(v) for k, v in N.items()}

# ---------------------------------------------------------------- motion data from the picture
A = R.Assets()
n = m.n; t = tax(n)
tf = np.linspace(0, R.DUR, int(R.DUR * 240) + 1)
hidx = np.array([A.head_index(x) for x in tf])
pos, _ = R.route_at(A, hidx)
z = np.array([R.camera(x)[0] for x in tf])
sx = (pos[:, 0] / 2 - R.W / 2) * z + R.W / 2                       # screen x (1x px)
spd = np.hypot(*np.gradient(pos, tf, axis=0).T) / 2                # px/s at 1x
on = (sx > -150) & (sx < R.W + 150)
spd_n = np.clip(spd / np.percentile(spd[on], 95), 0, 1.2) * on
spd_a = np.interp(t, tf, spd_n)
pan_a = np.clip(np.interp(t, tf, sx) / R.W * 2 - 1, -.95, .95)

# 1. air bed (0 - end): low brown noise, swells as the dragon arrives, fades into the hold
bed = static(brown(n), 'lp', 380) * (0.35 + 0.65 * seg(t, 0, .4)) * (1 - .6 * seg(t, 3.6, R.DUR))
m.add(bed / np.max(np.abs(bed)), 0, gain=.10, pan=0, rev=.2)

# 2. flight: body whoosh + scaly high hiss, both driven by the head's speed and x
m.add(whoosh(260 + 2200 * spd_a, spd_a ** 1.4, q=1.0), 0, gain=.62, pan=pan_a, rev=.3)
hiss = static(pink(n), 'hp', 5200) * spd_a ** 2
m.add(hiss / np.max(np.abs(hiss)), 0, gain=.05, pan=pan_a, rev=.25)
rum = osc(42 + 18 * spd_a, n) * spd_a ** 1.5
m.add(rum, 0, gain=.10, pan=0, rev=.1)

# eye glint as it appears (first on screen)
t_in = tf[np.argmax(on)]
m.add(glass(F['A5'], 1.2, .45), t_in, gain=.10, pan=float(np.interp(t_in, t, pan_a)), rev=.6)

# 3. coil locks (end of flight): tightening noise rise + click + sub thump
rise = bp_sweep(pink(secs(.5)), np.linspace(600, 3200, secs(.5)), q=2.0) * np.linspace(0, 1, secs(.5)) ** 2
m.add(rise / np.max(np.abs(rise)), R.T_FLY1 - .5, gain=.12, pan=-.45, rev=.3)
m.add(tock(1400), R.T_FLY1, gain=.25, pan=-.45, rev=.25)
m.add(sub_thump(70, 42, .9), R.T_FLY1, gain=.26, pan=0, rev=.1)

# 4. inflate to glossy 3D: soft glassy shimmer swell
nn = secs(1.0); tt = tax(nn)
sh = sum(osc(F[k] * (1 + .003 * np.sin(2 * np.pi * (4 + i) * tt)), nn) for i, k in enumerate(['D5', 'A5', 'D6']))
sh *= seg(tt, 0, .35) * np.exp(-np.maximum(tt - .35, 0) / .3)
m.add(sh / 3, R.T_INF0, gain=.07, pan=-.4, rev=.7)

# 5. blink + glint chime
m.add(glass(F['D6'], .9, .3), R.T_BLINK + .14, gain=.14, pan=-.3, rev=.55)

# 6. wordmark letters: rising marimba, D minor pentatonic, panned left -> right
scale = ['D4', 'F4', 'G4', 'A4', 'C5', 'D5', 'F5', 'G5', 'A5']
for i, k in enumerate(scale):
    m.add(marimba(F[k], .9), R.T_TYPE0 + i * R.T_TYPE_STEP + .04, gain=.11 - .004 * i, pan=-.1 + .1 * i, rev=.35)

# 7. resolve chord carries the hold to silence
t_res = R.T_TYPE0 + 8 * R.T_TYPE_STEP + .2
for k, g in [('D3', .20), ('A3', .14), ('D4', .12), ('F4', .09), ('A4', .06)]:
    m.add(bell(F[k], R.DUR - t_res + .2), t_res, gain=g, pan=0, rev=.5)

out = os.path.join(HERE, 'crenature_sfx.wav')
m.render(out)
print('wrote', out, '| flight speed peak at', round(float(tf[np.argmax(spd_n)]), 2), 's; eye on screen at', round(float(t_in), 2), 's')

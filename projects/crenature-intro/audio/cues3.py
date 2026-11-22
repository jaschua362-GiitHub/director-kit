"""Crenature intro v7+ - premium, restrained sound (no chimes, bells, marimba or clicks).

    python audio/cues3.py      -> audio/crenature_v7_sfx.wav

Texture, weight and air instead of musical "toys": a deep room tone and sub in the dark, a breath as
the eye opens, an airy grazing sweep that follows the rim-light, one slow open-voiced swell under the
sunrise landing on a soft sub boom, near-silent pen textures on the type, an air shimmer on the final
light pass. Timings come from build/render2.py.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'build'))
from sfxlib import *          # noqa
import render2 as R           # noqa

m = Mix(dur=R.DUR)
reseed(23)
n = m.n; t = tax(n)
A = R.Assets()
F = {k: hz(v) for k, v in dict(D1=26, D2=38, A2=45, E3=52, A3=57, D3=50).items()}

def norm(x): return x / (np.max(np.abs(x)) + 1e-9)

# rim-light front: speed + screen x (from the picture)
tf = np.linspace(0, R.DUR, int(R.DUR * 240) + 1)
fr = np.array([R.front(x) for x in tf])
pts = A.P[(np.clip(fr, 0, 1) * (len(A.P) - 1)).astype(int)]
sx = []
for x, (px, py) in zip(tf, pts):
    fx, fy, z, rot = R.camera(x, A)
    sx.append(R.W / 2 + ((px - fx) * np.cos(rot) - (py - fy) * np.sin(rot)) * 0.5 * z)
spd = np.abs(np.gradient(fr, tf)); spd /= spd.max()
spd_a = np.interp(t, tf, spd)
pan_a = np.clip(np.interp(t, tf, np.array(sx)) / R.W * 2 - 1, -.7, .7)
rise = np.interp(t, tf, [R.bg_level(x) for x in tf])            # sunrise 0..1

# 1. room tone + sub in the dark (barely there), thinning as the light rises
room = static(brown(n), 'lp', 260) * seg(t, 0, .8)
m.add(norm(room) * (1 - .7 * rise), 0, gain=.07, pan=0, rev=.1)
sub = (osc(F['D1'], n) + .35 * osc(F['D2'] * 1.003, n)) * seg(t, .1, 1.2) * (1 - .8 * rise)
m.add(sub, 0, gain=.055, pan=0, rev=.05)

# 2. the eye opens: a soft low inhale (filtered breath), no tone
nb = secs(.75); tb = tax(nb)
breath = bp_sweep(pink(nb), 250 + 650 * np.sin(np.pi * tb / tb[-1]) ** 2, q=.7) * np.sin(np.pi * tb / tb[-1]) ** 2
m.add(norm(breath), R.T_EYE0 - .1, gain=.09, pan=.15, rev=.45)

# 3. the rim-light grazes the body: an airy, high, soft sweep that follows the light (no ring)
graze = static(bp_sweep(pink(n), 2200 + 3800 * spd_a, q=.55), 'hp', 900) * spd_a ** 1.3
graze *= seg(t, R.T_TRACE0 - .05, R.T_TRACE0 + .25) * (1 - seg(t, R.T_TRACE1 - .2, R.T_TRACE1 + .1))
m.add(norm(graze), 0, gain=.085, pan=pan_a, rev=.5)
low_air = static(bp_sweep(pink(n), 180 + 260 * spd_a, q=.6), 'lp', 600) * spd_a
m.add(norm(low_air), 0, gain=.06, pan=pan_a * .5, rev=.3)

# 4. sunrise: one slow open-voiced swell (D, A, E, A - neither major nor minor), filter opening
t0, t1 = R.T_RISE0 - .5, R.DUR
ns = secs(t1 - t0); ts = tax(ns) + t0
after = np.maximum(ts - R.T_LIGHT_HIT, 0)
decay = np.exp(-after / 0.95)                                    # natural ease-out after the peak
cut = 180 + 1400 * np.interp(ts, tf, [R.bg_level(x) for x in tf]) ** 1.2 * np.exp(-after / 1.8)
env = np.where(ts < R.T_LIGHT_HIT, seg(ts, t0, R.T_LIGHT_HIT) ** 2.2, decay)
env *= 1 - seg(ts, R.DUR - .35, R.DUR) ** 2                      # nothing left at the end
pad = sum(g * saw_voice(F[k], ns, cut, harmonics=14, detune_cents=(-7, 0, 6))
          for k, g in (('D2', 1.0), ('A2', .8), ('E3', .55), ('A3', .4)))
m.add(norm(pad) * env, t0, gain=.20, pan=0, rev=.55)
# a breathy noise swell inside the pad, like air pressure building before the light settles
nr = secs(1.3); tr = tax(nr)
press = static(bp_sweep(pink(nr), np.linspace(300, 2400, nr), q=.6), 'lp', 3500) * (tr / tr[-1]) ** 3
m.add(norm(press), R.T_LIGHT_HIT - 1.3, gain=.10, pan=0, rev=.6)

# 5. the light settles: a deep, soft sub boom with a low body - no click
m.add(sub_thump(62, 32, 2.6), R.T_LIGHT_HIT, gain=.32, pan=0, rev=.18)
nt = secs(1.6); thud = static(brown(nt), 'lp', 160) * np.exp(-tax(nt) / .35)
m.add(norm(thud), R.T_LIGHT_HIT, gain=.12, pan=0, rev=.4)

# 6. type: near-silent pen strokes while each outline draws (soft filtered noise, no ticks)
act = np.zeros(n); fc = np.zeros(n)
for i in range(9):
    ts0 = R.T_TYPE0 + i * R.T_TYPE_STEP
    x = np.clip((t - ts0) / R.T_OUTLINE, 0, 1)
    w = np.sin(np.pi * x) ** 2 * (1 - .085 * i)
    act += w; fc += w * (3600 - 120 * i)
fc = np.where(act > 1e-4, fc / np.maximum(act, 1e-4), 3000)
act = ndimage_smooth = np.convolve(act, np.ones(secs(.05)) / secs(.05), 'same')
act *= np.exp(-np.maximum(t - (R.T_TYPE0 + .35), 0) / .55)      # the gesture eases out as the word completes
pen = static(bp_sweep(pink(n), fc, q=.8), 'hp', 1600) * act
m.add(norm(pen), 0, gain=.028, pan=np.clip(np.interp(t, [R.T_TYPE0, R.T_TYPE0 + .9], [-.3, .3]), -.3, .3), rev=.35)

# 7. the closing light pass: a soft high air shimmer travelling left -> right
t_sh = R.T_GLINT - .15
nh = secs(R.DUR - t_sh); th = tax(nh)
shenv = np.minimum(1, th / .18) ** 2 * np.exp(-np.maximum(th - .18, 0) / .5)
sh = static(bp_sweep(pink(nh), 6200 - 1800 * np.minimum(1, th / 1.2), q=1.0), 'hp', 2800) * shenv
m.add(norm(sh), t_sh, gain=.04, pan=np.clip(np.linspace(-.5, 1.2, nh), -.5, .5), rev=.65)

out = os.path.join(HERE, 'crenature_v7_sfx.wav')
mix = m.render(out, rt_tau=.85, predelay=.03)
# master ease-out: everything (dry, reverb, air) glides to true silence before the last frame
T_FADE0 = R.DUR - 1.3
x = np.clip((t - T_FADE0) / (R.DUR - 0.06 - T_FADE0), 0, 1)
mix = mix * (np.cos(np.pi / 2 * x) ** 2.2)[None, :]
write_wav24(out, mix)
print('wrote', out, '(eased out from', round(T_FADE0, 2), 's)')

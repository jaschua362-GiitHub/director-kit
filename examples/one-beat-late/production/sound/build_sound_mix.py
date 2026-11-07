"""Sound mix for the approved cut (music cut v08). See ../SOUND_PLAN.md and ../CUT_APPROVAL.json.

Every cue is placed from the v08 EDL: at(event, source_t) = record_in + (source_t - in_s), so it stays in sync with
the picture exactly as cut. Sources (all free):
  native  audio already in our takes: take A (his step, pivot, jacket), take B (his wince, his laugh), the P11 pilot
          finish (her laugh, and the faint watch laugh that take already contains, placed on the watch pulse).
  designed  sfx/*.wav from design_sfx.py: one arrival hiss reused for every arrival, the melt, the long P8 cue, the
          hand gather, heel clicks, watch ticks and tones, rail tick, breath, Moon and Earth room tone.
  music   the approved v08 music track, ducked about 5 dB under each hiss and laugh.
Room tone switches hard at each Moon/Earth cut. Everything fades to black with the picture; the first grain of a
new hiss then sits over the black. Loudness to -14 LUFS / -1.5 dBTP (ffmpeg loudnorm, two-pass).

Usage: python -I build_sound_mix.py  -> ../cuts/SOUND_EDIT_v01_480p.mp4 (+ stems/*.wav, mix report)
"""
import json, pathlib, re, subprocess
import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = pathlib.Path(__file__).parent
PROD = HERE.parent
EXP = PROD.parent
LAB = EXP.parents[1]
FF = str(LAB / "experiments/TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
SR = 48000
CUT = PROD / "cuts/MUSIC_EDIT_v13_480p"
OUT = PROD / "cuts/SOUND_EDIT_v11_480p.mp4"
STEMS = HERE / "stems"
STEMS.mkdir(exist_ok=True)

E = json.loads(CUT.with_suffix(".edl.json").read_text())
EV = E["events"]
TOTAL = E["total_s"]
BLACK = E["black_s"]
FADE = 1.6


def at(i, src_t):
    return EV[i]["record_in_s"] + (src_t - EV[i]["in_s"])


def load_media(path, start=None, dur=None):
    cmd = [FF, "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", str(path), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()


def sfx(name):
    sr, x = wavfile.read(HERE / "sfx" / f"{name}.wav")
    return x.astype(np.float32)


def db(g):
    return 10 ** (g / 20)


def edge_fade(x, ms=12):
    n = min(int(ms / 1000 * SR), len(x) // 2)
    x = x.copy()
    x[:n] *= np.linspace(0, 1, n)[:, None]
    x[-n:] *= np.linspace(1, 0, n)[:, None]
    return x


def pitch(x, factor):
    """small pitch/speed variation by resampling (reuse one hiss without it sounding copied)"""
    n = int(len(x) / factor)
    return signal.resample(x, n, axis=0).astype(np.float32)


N = int((TOTAL + 0.5) * SR)
stems = {k: np.zeros((N, 2), np.float32) for k in ("room", "foley", "hiss", "voice", "music")}
duck_events = []


def put(stem, x, t, gain_db=0.0, duck=False):
    i = int(round(t * SR))
    if i >= N:
        return
    x = x[: N - i] * db(gain_db)
    stems[stem][max(i, 0): i + len(x)] += x[max(0, -i):]
    if duck:
        duck_events.append((t, t + len(x) / SR))


# ---- room tone: hard switch at each Moon/Earth cut ----
EARTH = {3, 5, 8, 9, 10}                                          # P3, P5, P8, P9, P10 are his room
moon, earth = sfx("room_moon"), sfx("room_earth_dusk")
for ev in EV:
    p, t0, d = ev["panel"], ev["record_in_s"], ev["dur_s"]
    if p == 0:
        continue
    src = earth if p in EARTH else moon
    n = int(d * SR)
    reps = np.concatenate([src] * (n // len(src) + 2))
    off = int((t0 * 7.3 % 10) * SR)                              # different stretch of the loop per shot
    put("room", edge_fade(reps[off: off + n], 15), t0, -31 if p in EARTH else -33)

# ---- native audio from our takes ----
D = PROD / "video/drafts"
A = D / "A-d01-480p.mp4"
B = D / "B-d01-480p.mp4"
P11F = EXP / "pilot/native/P11-F02_d02_045c3cb8_1080p.mp4"
put("foley", edge_fade(load_media(A, 1.52, EV[2]["dur_s"])), EV[2]["record_in_s"], -6)            # P3: his step
put("voice", edge_fade(load_media(B, 1.0, EV[5]["dur_s"])), EV[5]["record_in_s"], -5, duck=True)  # P5: wince "ah"
put("voice", edge_fade(load_media(B, 3.6, EV[10]["dur_s"])), EV[10]["record_in_s"], -4, duck=True)  # P9: his laugh
put("foley", edge_fade(load_media(A, 4.2, EV[11]["dur_s"])), EV[11]["record_in_s"], -5)           # P10: pivot, swish
p11_in_cut = 1.38 - EV[12]["in_s"]                                 # the pilot finish starts this far into the P11 event
# Watch laugh. v02 used take B's laugh through a saturated tiny-speaker filter ("sudden Hurrzz"); v03 dropped the
# saturation but it still read as "a man hurrz sound". v05 uses the pilot take's own faint watch laugh (P11-F02 at
# about 1.7-2.1 s, inside the clip Jason approved by ear), placed on the watch pulse as the camera rises past her wrist.
wl = load_media(P11F, 1.65, 0.5)
put("voice", edge_fade(wl), EV[12]["record_in_s"] + p11_in_cut + (2.40 - 2.29), -1, duck=True)
put("voice", edge_fade(load_media(P11F, 3.3, 1.68)),   # runs on through the one-beat extension (same take)
    EV[12]["record_in_s"] + p11_in_cut + (3.3 - 2.29), 4, duck=True)  # her laugh

# ---- designed cues ----
hiss = sfx("hiss_arrival")
heels = [sfx(f"heel_glass_{k}") for k in range(4)]
put("hiss", hiss, at(0, 0.0), -15, duck=True)                     # P1 his print forms
put("foley", heels[0], 1.86, -14)                                  # P1 boot lands on beat 4
put("foley", sfx("watch_alert"), at(1, 0.42), -17)                # P2 her watch alerts her, before she lifts her wrist
# Jason: "she opens her mouth and said something ... if she didn't talk then is weird". Her whispered count
# (MiniMax Speech 2.8, USD0.00077). v09 placed the words from a motion measure that mixed head and lip movement
# ("it doesn't sync with her mouth"). v10: lip openings read frame by frame (composite/work/P02_mouth_strip.jpg):
# "one" opens at src 0.92 s (closed by 1.25), "two" at 1.67 s (closed by about 1.92). Each word is trimmed to its
# opening and lands on it; the watch ticks sit on the same moments, and the alert leads before she lifts her wrist.
# v11: REMOVED by Jason ("her mouth shape is not meant to say 1-2 ... let current sound fx tell a speechless story").
# The film stays wordless; the watch alert and its two ticks on her lip openings remain.
put("foley", sfx("watch_tick"), at(1, 0.92), -18)                 # tick with "one"
put("foley", sfx("watch_tick"), at(1, 1.67), -18)                 # tick with "two"
put("foley", heels[1], at(1, 2.85), -13)                          # P2 her step
put("foley", sfx("rail_tick"), at(1, 2.87), -24)                  # rail light: sent
put("hiss", pitch(hiss, 1.02), at(2, 3.47), -8, duck=True)       # P3 her print arrives, 2 beats late
put("hiss", sfx("hiss_melt"), EV[3]["record_in_s"], -26)          # P4 M1 melting away
put("foley", heels[2], at(3, 0.875), -15)                         # P4 her step
put("hiss", pitch(hiss, 0.98), at(3, 1.00), -10, duck=True)       # P4 F2 arrives
# (no F3 arrival: p04_comp only composites F0-F2; a hiss here had nothing on screen)
put("foley", sfx("heel_touch_soft"), at(3, (86 - 41) / 24), -17)  # P4 her pivot as she turns (src frame 86)
put("foley", heels[3], at(3, (102 - 41) / 24), -15)               # P4 her step back left (src frame 102)
put("hiss", pitch(hiss, 1.01), at(4, 0.12), -8, duck=True)       # P5 under his toe
for k, (tt, g) in enumerate([(0.10, -8), (0.35, -10), (0.62, -13)]):   # P6 backlog, thinning
    put("hiss", pitch(hiss, 1 + 0.03 * (k - 1)), at(6, tt), g, duck=True)
put("foley", sfx("watch_tone"), at(7, 3.00), -27)                 # P6 watch blinks, unanswered
put("foley", sfx("watch_tone"), at(7, 3.35), -28)
put("foley", sfx("breath_soft"), at(7, 3.05), -30)
put("hiss", sfx("hiss_melt"), at(8, 0.40), -23)                   # P7 F3 melts away
put("hiss", sfx("hiss_melt"), at(8, 2.91), -27)                   # P7 backlog starts to melt
put("foley", sfx("heel_touch_soft"), at(8, 1.60), -18)            # P7 one soft heel touch
put("hiss", sfx("hiss_long"), at(9, 0.35), -6, duck=True)         # P8 the long clear arrival (kept audible: the board's cue)
put("hiss", pitch(hiss, 0.97), at(12, 0.25), -8, duck=True)      # P11 spiral arrival under her boot
put("foley", sfx("heel_touch_soft"), at(14, 2.30), -20)           # P12 her sink
put("hiss", sfx("hiss_gather"), EV[15]["record_in_s"], -5)       # P12 grains gather under her hand

# ---- the hiss family sits back: 6 dB down, top softened above about 6.5 kHz (Jason, 5 Nov) ----
stems["hiss"] = (signal.sosfilt(signal.butter(2, 6500, "lowpass", fs=SR, output="sos"), stems["hiss"], axis=0) * db(-12)).astype(np.float32)   # v04: a further 6 dB down (Jason: "overall grain hiss still loud")

# ---- music, ducked under hisses and laughs ----
mus = load_media(CUT.with_suffix(".wav"))
stems["music"][: len(mus)] += mus[:N]
duck = np.ones(N, np.float32)
for a, b in duck_events:
    i0, i1 = int(a * SR), int(min(b, TOTAL) * SR)
    duck[i0:i1] = np.minimum(duck[i0:i1], db(-2.5))   # gentler: the hisses sit inside the scene
duck = signal.sosfiltfilt(signal.butter(1, 4, "lowpass", fs=SR, output="sos"), duck).astype(np.float32)   # smooth ramps
stems["music"] *= duck[:, None]

# ---- everything follows the picture's fade to black; then the first grain of a new hiss over the black ----
tt = np.arange(N) / SR
k = np.clip((tt - (BLACK - FADE)) / FADE, 0, 1)
fade = (1 - k * k * (3 - 2 * k))[:, None]
for s in ("room", "foley", "hiss", "voice"):
    stems[s] *= fade
# the first grain of his next answer: rises softly, then fades out fully inside the 2.0 s of black (v06: the v05
# grain was a 0.35 s ramp that stopped at full level when the film ended, "cut off too fast")
g = hiss[: int(1.2 * SR)].copy()
g *= np.concatenate([np.linspace(0, 1, int(0.3 * SR)) ** 1.5, np.linspace(1, 0, len(g) - int(0.3 * SR)) ** 2])[:, None]
put("hiss", g, BLACK + 0.25, -23)   # matched to the in-film hisses (added after the stem was turned down)

# ---- write stems, mix, loudness ----
report = {}
for s, x in stems.items():
    x = x[: int(TOTAL * SR)]
    wavfile.write(STEMS / f"{s}.wav", SR, x)
    report[s] = round(float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)), 1)
mix = sum(stems.values())[: int(TOTAL * SR)]
mix /= max(1.0, np.abs(mix).max() / 0.95)
raw = STEMS / "_mix_raw.wav"
wavfile.write(raw, SR, mix.astype(np.float32))
meas = subprocess.run([FF, "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                       "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", meas, re.S).group(0))
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
      "alimiter=limit=0.82:attack=2:release=40:level=false")   # true-peak safety at about -1.7 dBFS
final = STEMS / "mix_final.wav"
subprocess.run([FF, "-v", "error", "-y", "-i", str(raw), "-af", af, "-ar", str(SR), str(final)], check=True)
subprocess.run([FF, "-v", "error", "-y", "-i", str(CUT.with_suffix(".mp4")), "-i", str(final), "-map", "0:v", "-map",
                "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", str(OUT)], check=True)
chk = subprocess.run([FF, "-hide_banner", "-i", str(final), "-af", "loudnorm=I=-14:TP=-1.5:print_format=json", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
c = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", chk, re.S).group(0))
report.update({"final_LUFS": c["input_i"], "final_TP": c["input_tp"], "duck_events": len(duck_events), "out": str(OUT.name)})
(HERE / "mix_report.json").write_text(json.dumps(report, indent=1))
print(json.dumps(report))

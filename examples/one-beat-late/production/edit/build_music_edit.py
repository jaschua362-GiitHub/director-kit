"""Music cut: One Beat Late conformed to the chosen tune (M01 take 2, 92.3 bpm, beat 0.650 s). See ../MUSIC_PLAN.md.

Picture: each panel is a whole number of beats; in-points are chosen so the key contact lands on its beat
(boot landing, her step, his landing, the 2-beat-late arrivals, the spin landing on the cut into P11).
Music, built locally from the one track (nothing generated here):
  seg 1  track 0.081 s onward under P1-P6 insert. P1-P2 sound like a tiny watch speaker (band-pass), opening to
         the room at P3. P3 to the drop also carries a copy delayed 2 beats (1.30 s = the film's delay), so the
         tune rubs against itself: out of step. Drops out on the cut to her face in P6.
           Jason (5 Nov): "It can mellow down quietly but [not a] total cut off." So from the cut to her face in
           P6 the tune keeps playing, low (-13 dB) and muffled (low-pass), under her pondering (P6 face, P7, P8);
           on his laugh (P9) it opens up and swells into the return. P7-P9 are whole beats so the join is on a beat.
  seg 2  takes over on the downbeat at the cut into P10 (track 111.897 s, 0.25 s crossfade) and plays to the track's own last note
         (122.300 s, a downbeat) at black. Jason (5 Nov): the end is a FADE to black over the last 1.6 s of the hand
         close-up, and the music fades with it, ending at black.
Usage: python -I build_music_edit.py [--labels 1]  -> ../cuts/MUSIC_EDIT_v01_480p.mp4 (+ .wav, .edl.json)
"""
import argparse, json, subprocess, sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import build_draft_edit as B   # frame readers, paths, ffmpeg

BEAT = 0.650
D, S, C, EXP = B.D, B.S, B.C, B.EXP
MUSIC = B.PROD / "music/M01-take2_minimax-music-3.0_b94f2aa4.mp3"
SEG1_IN, SEG2_IN, LAST_NOTE = 0.081, 111.897, 122.300

# (panel, kind, source, in_s, beats, note) -- durations are whole beats
EDL = [
    (1, "clip", C / "P01-comp_v5_480p.mp4", 0.0, 4, "print forms beats 1-2; boot lands on beat 4"),
    (2, "clip", C / "P02-comp_v3_480p.mp4", 0.25, 5, "looks at his print, watch count; step + rail tick on beat 5"),
    (3, "clip", C / "P03-comp_v2_480p.mp4", 1.52, 4, "his landing on beat 2; her print arrives on beat 4 (2 beats late)"),
    (4, "clip", C / "P04-comp_v2_480p.mp4", 0.225, 4, "F3 lands beat 2; its print arrives beat 4"),
    (5, "clip", C / "P05-INS_v2_480p.mp4", 0.10, 1, "her print presses under his toe"),
    (5, "clip", D / "B-d01-480p.mp4", 1.0, 2, "grin slips"),
    (6, "clip", C / "P06-INS_v5_480p.mp4", 0.0, 2, "backlog arrives on the eighths"),
    (6, "clip", D / "P06-d02-480p.mp4", 2.7, 2, "MUSIC MELLOWS on this cut (quiet, muffled, never stops)"),
    (7, "clip", C / "P07-comp_v1_480p.mp4", 0.4, 4, "music low and muffled"),
    (8, "clip", C / "P08-INS_v3_480p.mp4", 0.05, 3, "music low and muffled"),
    (9, "clip", D / "B-d01-480p.mp4", 3.6, 2, "his laugh: the music opens up and swells"),
    (10, "clip", C / "P10-comp_v2_480p.mp4", 4.2, 4, "MUSIC RETURNS on this downbeat; spin lands on the cut to P11"),
    (11, "clip", EXP / "pilot/cuts/P11-insert-cut_v6_1080p.mp4", 0.17, 5, "pilot cut, first 0.17 s trimmed"),
    # Jason (5 Nov): "slightly extend more on this shot to allow her emotion to act out ... not to interfere with the
    # current edit". The pilot cut ends on frame 103 of its 1080p take; the same take continues to frame 120, so one
    # more beat follows seamlessly from frame 103. The approved pilot file itself is untouched. EXTEND adds one beat of
    # music at the same point, so everything after it (and the last note on black) stays in sync.
    (11, "clip", C / "P11-EXT_png/%04d.png", 0.0, 1, "EXTEND: her laugh, one more beat (same take)"),
    # v12: the take's frames 103-120, decoded with ffmpeg to lossless PNGs and colour-matched (per-channel gain and
    # offset fitted on frame 102 against the pilot cut's last frame). OpenCV's decode of the 10-bit HEVC, and any
    # re-encode, shifted the colour; v10 also started at frame 104, but the pilot cut ends on frame 102.
    (12, "clip", C / "P12-comp_v1_480p.mp4", 1.6, 3, "turn into the sink"),
    (12, "clip", C / "P12-HAND_v3_480p.mp4", 0.0, 4, "grains react; FADE to black over the last 1.6 s, music fades with it"),
    (0, "black", None, 0.0, None, "black (2.0 s): the grain of his next answer rises and fades"),
]
SILENT_DUR = {0: 2.0}   # Jason: longer black so the hiss grain can fade out fully
FADE = 1.6   # Jason: "We wanted a fade to black ... music can follow that fade to end"


def load_music():
    raw = subprocess.run([B.FF, "-v", "error", "-i", str(MUSIC), "-ac", "2", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy(), 48000


def ek_full(n, ek):
    """Pad the echo gain curve (fixed at its last value) to length n."""
    out = np.empty((n, 1), np.float32); out[:len(ek)] = ek; out[len(ek):] = ek[-1]
    return out


def bandpass_watch(x, sr):
    """Tiny watch speaker: 900-4500 Hz, a little saturation, mono."""
    from scipy import signal
    sos = signal.butter(4, [900, 4500], "bandpass", fs=sr, output="sos")
    m = signal.sosfilt(sos, x.mean(axis=1))
    m = np.tanh(m * 3) / 3
    return np.stack([m, m], axis=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", type=int, default=1)
    ap.add_argument("--out", default=str(C / "MUSIC_EDIT_v13_480p.mp4"))
    a = ap.parse_args()
    out = Path(a.out)

    # ---- picture ----
    tmp = out.with_suffix(".picture.mp4")
    p = subprocess.Popen([B.FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{B.W}x{B.H}", "-r",
                          str(B.FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(tmp)],
                         stdin=subprocess.PIPE)
    edl, t, marks, ideal = [], 0.0, {}, 0.0
    for panel, kind, src, t0, beats, note in EDL:
        dur = beats * BEAT if beats else SILENT_DUR[panel]
        n = round((ideal + dur) * B.FPS) - round(ideal * B.FPS)     # round cumulative beat time: no drift
        ideal += dur
        frames = ([np.zeros((B.H, B.W, 3), np.uint8)] * n if kind == "black" else B.clip_frames(src, t0, n))
        for j, f in enumerate(frames):
            f = f.copy()
            if "FADE" in note:
                k = np.clip(((j + 1) / B.FPS - (dur - FADE)) / FADE, 0, 1)
                f = (f.astype(np.float32) * (1 - k * k * (3 - 2 * k))).astype(np.uint8)
            if a.labels and panel:
                cv2.putText(f, f"P{panel}", (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            p.stdin.write(f.tobytes())
        if "MELLOWS" in note:
            marks["drop"] = t
        if "swells" in note:
            marks["swell"] = t
        if "RETURNS" in note:
            marks["return"] = t
        if kind == "black":
            marks["black"] = t
        if "EXTEND" in note:
            marks["extend"] = t
        edl.append({"panel": panel, "source": str(Path(src).relative_to(EXP)) if src else None, "in_s": t0,
                    "beats": beats, "dur_s": round(n / B.FPS, 3), "record_in_s": round(t, 3), "note": note})
        t += n / B.FPS
    p.stdin.close(); p.wait()
    total = t

    # ---- music ----
    x, sr = load_music()
    mix = np.zeros((int(total * sr) + sr, 2), np.float32)
    # seg 1: track from SEG1_IN, until the drop (short fade)
    d = marks["drop"]
    seg1 = x[int(SEG1_IN * sr): int((SEG1_IN + d) * sr)].copy()
    open_t = edl[2]["record_in_s"]                                   # P3 start: the watch opens to the room
    w = bandpass_watch(seg1, sr) * 1.6                                 # small but clearly audible
    k = np.clip((np.arange(len(seg1)) / sr - (open_t - 0.4)) / 0.8, 0, 1)[:, None]   # crossfade watch -> room
    seg1 = w * (1 - k) + seg1 * k
    lag = int(2 * BEAT * sr)                                         # the film's delay, as a 2-beat echo
    echo = np.zeros_like(seg1); echo[lag:] = x[int(SEG1_IN * sr): int(SEG1_IN * sr) + len(seg1) - lag]
    ek = np.clip((np.arange(len(seg1)) / sr - open_t) / 0.6, 0, 1)[:, None] * 0.45
    seg1 = seg1 + echo * ek
    # keep seg 1 running past the drop to the return, then: low and muffled from the drop, opening on his laugh
    r = marks["return"]
    seg1 = np.concatenate([seg1, x[int((SEG1_IN + d) * sr): int((SEG1_IN + r + 0.25) * sr)]])
    from scipy import signal
    lp = signal.sosfiltfilt(signal.butter(2, 650, "lowpass", fs=sr, output="sos"), seg1, axis=0).astype(np.float32)
    tt = np.arange(len(seg1)) / sr
    sw = marks["swell"]
    down = np.clip((tt - d) / 0.6, 0, 1)                             # 0.6 s settle into the low, muffled bed
    up = np.clip((tt - sw) / (r - sw), 0, 1) ** 1.5                  # opens across P9, fully open at the return
    muff = (down * (1 - up))[:, None]
    gain = (1 - down * (1 - 10 ** (-13 / 20)) * (1 - up))[:, None]
    gain = gain * (1 + 0.4 * up[:, None] * (tt < r)[:, None])        # a slight swell into the downbeat
    echo_off = np.clip((tt - d) / 0.4, 0, 1)[:, None]                # the out-of-step echo ends at "it hurts"
    echo_full = np.zeros_like(seg1); echo_full[:len(echo)] = echo
    dry = seg1 - echo_full * ek_full(len(seg1), ek) * echo_off
    seg1 = (dry * (1 - muff) + lp * muff) * gain
    xf = int(0.25 * sr); i_r = int(r * sr)
    n_xf = len(seg1[i_r: i_r + xf])
    seg1[i_r: i_r + n_xf] *= np.linspace(1, 0, n_xf)[:, None]        # hand over to seg 2 on the downbeat
    seg1[i_r + xf:] = 0
    mix[:len(seg1)] += seg1
    # seg 2: take over on the downbeat at P10, play to the last note + its natural decay
    tail_end = LAST_NOTE + 1.2
    seg2 = x[int(SEG2_IN * sr): int(tail_end * sr)].copy()
    fin = int(0.02 * sr); seg2[:fin] *= np.linspace(0, 1, fin)[:, None]
    ext_extra = 0.0
    if "extend" in marks:                                            # repeat the beat just before the extension point
        te, nb = int((marks["extend"] - r) * sr), int(BEAT * sr)
        rep = seg2[te - nb: te].copy()
        xf = int(0.012 * sr)
        rep[:xf] *= np.linspace(0, 1, xf)[:, None]
        seg2[te - xf: te] *= np.linspace(1, 0, xf)[:, None]
        tail = seg2[te:].copy(); tail[:xf] *= np.linspace(0, 1, xf)[:, None]
        seg2 = np.concatenate([seg2[:te], rep, tail])
        ext_extra = BEAT
    mix[int(r * sr): int(r * sr) + len(seg2)] += seg2[: len(mix) - int(r * sr)]
    last_note_edit = r + (LAST_NOTE - SEG2_IN) + ext_extra
    bk = marks["black"]
    tt = np.arange(len(mix)) / sr
    # Jason (5 Nov): "let the music flow over to the black and fade off together ... the music will preserve a
    # continuity". The picture still fades to black over FADE; the music carries on past the cut, its last note rings
    # into the black, and it fades out over the black (from 0.3 s before black to 1.8 s after).
    k = np.clip((tt - (bk - 0.3)) / 2.1, 0, 1)
    mix *= (1 - k * k * (3 - 2 * k))[:, None]
    peak = np.abs(mix).max()
    mix *= 0.89 / peak                                               # about -1 dBFS peak; loudness set in the finish
    wav = out.with_suffix(".wav")
    subprocess.run([B.FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-", str(wav)],
                   input=mix[: int(total * sr)].tobytes(), check=True)
    subprocess.run([B.FF, "-v", "error", "-y", "-i", str(tmp), "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a",
                    "192k", "-shortest", str(out)], check=True)
    tmp.unlink()
    info = {"total_s": round(total, 3), "bpm": 92.3, "beat_s": BEAT, "drop_s": round(d, 3), "return_s": round(r, 3),
            "last_note_edit_s": round(last_note_edit, 3), "black_s": round(marks["black"], 3), "events": edl}
    out.with_suffix(".edl.json").write_text(json.dumps(info, indent=1))
    print(f"total {total:.3f} s  drop {d:.3f}  return {r:.3f}  last note {last_note_edit:.3f}  black {marks['black']:.3f}")


if __name__ == "__main__":
    main()

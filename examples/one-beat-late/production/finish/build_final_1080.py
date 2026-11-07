"""One Beat Late finish: 1080p assembly on the approved music cut v13 EDL, then grade + fade + encode + mux.

Stage `assemble`: every event of cuts/MUSIC_EDIT_v13_480p.edl.json (same in-frames, same frame counts) with its source
swapped to the 1080p version, decoded with ffmpeg (auto colour matrix: bt709 for the tagged native HEVC takes, the
untagged x264 intermediates round-trip on the default), no labels, NO fade, NO grade -> lossless master (ffv1) plus
finish/assembly.json (per-frame event map).  Also writes a timing check against cuts/SOUND_EDIT_v11_480p.mp4.
Stage `final`: master -> per-room grade (finish/grade.json) -> the v13 fade (same smoothstep, same 1.6 s) -> x264
yuv420p bt709-tagged -> mux sound/stems/mix_final.wav (unchanged samples, AAC 320k).

Usage: python -I build_final_1080.py assemble | check | final [--grade NAME] [--out ...]
"""
import argparse, json, subprocess, sys
from pathlib import Path

import numpy as np

FIN = Path(__file__).resolve().parent
PROD = FIN.parent
EXP = PROD.parent
LAB = EXP.parents[1]
FF = str(LAB / "experiments/TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
W, H, FPS = 1920, 1080, 24
EDL = json.loads((PROD / "cuts/MUSIC_EDIT_v13_480p.edl.json").read_text())
V11 = PROD / "cuts/SOUND_EDIT_v11_480p.mp4"
MIX = PROD / "sound/stems/mix_final.wav"
MASTER = FIN / "ONE_BEAT_LATE_1080p_ungraded_master.mkv"
FADE = 1.6

# 480p source in the v13 EDL -> 1080p source, and a frame offset for native takes that lead their draft
NATIVE = {"production/video/drafts/B-d01-480p.mp4": ("production/video/native/B-F01_1080p.mp4", 0),
          "production/video/drafts/P06-d02-480p.mp4": ("production/video/native/P06-F02_1080p.mp4", 0)}
ALLOW_MISSING = "--trial" in sys.argv
OFFSETS = json.loads((FIN / "offsets.json").read_text()) if (FIN / "offsets.json").exists() else {}


def room(panel):
    """Moon (her) or Earth (him) room, for the per-room grade."""
    return {1: "moon", 2: "moon", 3: "earth", 4: "moon", 5: "earth", 6: "moon", 7: "moon", 8: "earth", 9: "earth",
            10: "earth", 11: "moon", 12: "moon", 0: "black"}[panel]


def map_source(src):
    s = src.replace("\\", "/")
    if s in NATIVE:
        p, off = NATIVE[s]
        return EXP / p, OFFSETS.get(Path(p).stem, off)
    if "pilot/" in s or "P11-EXT_png" in s:
        return EXP / s, 0                                   # already 1080p (approved pilot cut; lossless extension)
    if s.startswith("production/cuts/") and s.endswith("_480p.mp4"):
        p = PROD / "cuts/1080" / Path(s).name.replace("_480p.mp4", "_1080p.mp4")
        if not p.exists() and ALLOW_MISSING:              # trial assemblies only: the 480p cut stands in
            print("  TRIAL: 480p stand-in for", p.name)
            return EXP / s, 0
        return p, 0
    raise SystemExit(f"no 1080p mapping for {s}")


def read(path, start, n):
    """n frames from frame `start`, ffmpeg decode, area-scaled to 1920x1080 if larger; a short source repeats its
    last frame (as the 480p cut's reader did) and that is reported."""
    inp = ["-framerate", str(FPS), "-i", str(path)] if "%" in str(path) else ["-i", str(path)]
    vf = f"trim=start_frame={start}:end_frame={start + n},setpts=PTS-STARTPTS,scale={W}:{H}:flags=area"
    raw = subprocess.run([FF, "-v", "error", *inp, "-vf", vf, "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    short = n - len(fr)
    if short > 0:
        fr = np.concatenate([fr, np.repeat(fr[-1:], short, 0)])
    return fr[:n], max(short, 0)


def assemble():
    p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r",
                          str(FPS), "-i", "-", "-c:v", "ffv1", "-level", "3", "-pix_fmt", "bgr0", str(MASTER)],
                         stdin=subprocess.PIPE)
    events, frame_map, t = [], [], 0
    for k, e in enumerate(EDL["events"]):
        n = round(e["dur_s"] * FPS)
        if e["source"] is None:
            frames, short, src, start = np.zeros((n, H, W, 3), np.uint8), 0, None, 0
        else:
            src, off = map_source(e["source"])
            start = round(e["in_s"] * FPS) + off
            frames, short = read(src, start, n)
        for j in range(n):
            p.stdin.write(frames[j].tobytes())
            frame_map.append({"event": k, "panel": e["panel"], "j": j, "n": n, "fade": "FADE" in e["note"]})
        events.append({"event": k, "panel": e["panel"], "room": room(e["panel"]), "source": str(src.relative_to(EXP)) if src else None,
                       "start_frame": start, "frames": n, "record_in": t, "short_frames_repeated": short, "note": e["note"]})
        print(f"{k:2d} P{e['panel']:<2d} {n:3d} fr @ {t:3d}  {events[-1]['source']}  start {start}" + (f"  SHORT {short}" if short else ""))
        t += n
    p.stdin.close(); p.wait()
    (FIN / "assembly.json").write_text(json.dumps({"total_frames": t, "events": events, "frames": frame_map}, indent=1))
    print("total frames", t, "(v11: 828)")


def fade_gain(fm):
    """The v13 fade: smoothstep over the last FADE s of the event marked FADE (same smoothstep; the event length is its frame count / 24 = 2.583 s where v13 used 4 beats = 2.6 s, so fade levels differ by under 1 %; timing is unaffected)."""
    if not fm["fade"]:
        return 1.0
    dur = fm["n"] / FPS
    k = np.clip(((fm["j"] + 1) / FPS - (dur - FADE)) / FADE, 0, 1)
    return float(1 - k * k * (3 - 2 * k))


def frames_of(path, w, h):
    proc = subprocess.Popen([FF, "-v", "error", "-i", str(path), "-vf", f"scale={w}:{h}:flags=area", "-fps_mode", "passthrough", "-f", "rawvideo",
                             "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    sz = w * h * 3
    while True:
        b = proc.stdout.read(sz)
        if len(b) < sz:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)


def check(path=None, faded=False):
    """Per-frame structure match of the 1080p file (downscaled) against v11: for each frame, correlation of the
    mean-removed grey image (labels area masked) at offsets -2..+2; a shifted cut shows as a best offset != 0."""
    import cv2
    path = path or MASTER
    A = json.loads((FIN / "assembly.json").read_text())
    w, h = 426, 240
    a = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames_of(path, w, h)]).astype(np.float32)
    b = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames_of(V11, w, h)]).astype(np.float32)
    if not faded:
        g = np.array([fade_gain(fm) for fm in A["frames"]], np.float32)
        a = a * g[:, None, None]
    a[:, :20, :40] = 0; b[:, :20, :40] = 0                       # the "P#" label corner of the 480p cuts
    print("frames", len(a), "v11", len(b))
    rows, bad = [], []
    for i in range(min(len(a), len(b))):
        def corr(x, y):
            x = x - x.mean(); y = y - y.mean()
            d = np.sqrt((x * x).sum() * (y * y).sum())
            return float((x * y).sum() / d) if d > 1e-3 else 1.0
        c = {o: corr(a[i], b[i + o]) for o in range(-2, 3) if 0 <= i + o < len(b)}
        best = max(c, key=c.get)
        rows.append((i, round(c[0], 3), best, round(c[best], 3)))
    ev = {}
    for i, c0, best, cb in rows:
        fm = A["frames"][i]
        ev.setdefault(fm["event"], []).append((c0, best, cb))
    out = []
    for k, lst in ev.items():
        e = A["events"][k]
        c0 = [x[0] for x in lst]; nb = sum(1 for x in lst if x[1] != 0 and x[2] - x[0] > 0.02)
        # first and last frame of the event: the cut points
        out.append({"event": k, "panel": e["panel"], "frames": len(lst), "corr_mean": round(float(np.mean(c0)), 3),
                    "corr_min": round(float(np.min(c0)), 3), "first": lst[0], "last": lst[-1], "frames_better_shifted": nb})
        print(f"{k:2d} P{e['panel']:<2d} n {len(lst):3d}  corr mean {np.mean(c0):.3f} min {np.min(c0):.3f}  "
              f"first {lst[0]} last {lst[-1]}  better-shifted {nb}")
    (FIN / f"timing_check_{Path(path).stem}.json").write_text(json.dumps({"events": out, "per_frame": rows}, indent=0))


def final(grade_name, out):
    import cv2
    sys.path.insert(0, str(FIN))
    import grade as G
    A = json.loads((FIN / "assembly.json").read_text())
    params = json.loads((FIN / "grade.json").read_text())[grade_name]
    tmp = Path(out).with_suffix(".picture.mp4")
    p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                          "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-profile:v", "high", "-tune", "film",
                          "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                          "-movflags", "+faststart", str(tmp)], stdin=subprocess.PIPE)
    rng = np.random.default_rng(7)
    for i, f in enumerate(frames_of(MASTER, W, H)):
        fm = A["frames"][i]
        e = A["events"][fm["event"]]
        if e["room"] == "black":
            g = np.zeros_like(f)
        else:
            pe = dict(params[e["room"]]); pe.update(params.get("events", {}).get(str(fm["event"]), {}))
            g = G.grade(f, pe, rng)
            k = fade_gain(fm)
            if k < 1:
                g = (g.astype(np.float32) * k).astype(np.uint8)
        p.stdin.write(g.tobytes())
    p.stdin.close(); p.wait()
    subprocess.run([FF, "-v", "error", "-y", "-i", str(tmp), "-i", str(MIX), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", str(out)], check=True)
    tmp.unlink()
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["assemble", "check", "final"])
    ap.add_argument("--grade", default="G1")
    ap.add_argument("--file", default=None)
    ap.add_argument("--faded", type=int, default=0)
    ap.add_argument("--trial", action="store_true")
    ap.add_argument("--out", default=str(FIN / "ONE_BEAT_LATE_1080p_v01.mp4"))
    a = ap.parse_args()
    if a.stage == "assemble":
        assemble()
    elif a.stage == "check":
        check(a.file, bool(a.faded))
    else:
        final(a.grade, a.out)

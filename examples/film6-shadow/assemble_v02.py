"""Draft edit v03 (v02 + T17b earpiece retake + SFX layer): re-cut for action continuity (Jason: cuts didn't join, cloak not exciting, decoy missing; no 30 s cap).

Changes from v01: every action completes before the cut; cuts land on motion; new cloak take T05b (orbit) after the
wrist tap; new decoy scope take T19 at the turn; English subtitles burned in; hunter LOCK overlay; music bed with
dialogue ducking. Picture stays 480x854 / 24 fps (drafts).

Usage: python assemble_v02.py MUSIC.wav SUFFIX   (e.g. music/score_A.wav A)
"""
import json, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
FF = HERE.parent / "TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
FONT = "C\\:/Windows/Fonts/arialbd.ttf"

# take, in, out, native audio, subtitle (English, '' for none), overlay
EDL = [
    ("T01", 0.0, 3.0, True, "One at the exit.", None),
    ("T02", 0.2, 1.8, False, "", None),
    ("T03", 1.8, 3.4, False, "", None),
    ("T04", 0.0, 1.4, False, "Then I go faster.", None),
    ("T05", 0.6, 2.0, False, "Go.", None),
    ("T05b", 1.0, 4.2, False, "", None),
    ("T04", 2.0, 3.4, False, "", None),
    ("T06", 0.3, 2.1, False, "", None),
    ("T07b", 0.0, 2.4, False, "", None),
    ("T08", 0.4, 1.2, False, "", None),
    ("T09b", 0.0, 1.6, False, "", None),
    ("T10", 0.4, 3.2, False, "", None),
    ("T11", 1.2, 3.4, False, "", None),
    ("T12", 0.4, 2.4, False, "", None),
    ("T13", 1.0, 2.0, False, "", None),
    ("T14", 0.3, 2.1, False, "", "LOCK"),
    ("T19", 0.0, 3.6, False, "", None),
    ("T14", 2.6, 3.8, False, "", None),
    ("T15", 0.8, 2.8, False, "", None),
    ("T16", 0.0, 2.4, False, "", None),
    ("T17b", 2.4, 6.6, True, "Nice decoy.|That wasn't me.|Then who moved like me?", None),
    ("T18", 1.0, 4.5, False, "", None),
    ("T17b", 6.6, 8.0, True, "", None),
]


# SFX cues: (EDL row index, offset from that row's start in s, file in sfx/, volume)
SFX = [
    (0, 0.25, "goggles_click", 0.9),
    (4, 0.40, "cloak_shimmer", 0.9),
    (6, 0.15, "whoosh_deep", 0.8),
    (8, 0.45, "whoosh_airy", 0.8),
    (10, 0.05, "whoosh_deep", 0.9),
    (11, 0.30, "whoosh_airy", 0.7),
    (12, -0.25, "ninja_landing", 1.0),
    (13, 0.00, "hunter_fans", 0.7),
    (13, -0.40, "riser_fast", 0.45),
    (15, 0.40, "target_lock", 0.9),
    (16, 0.00, "glitch_tv", 0.8),
    (17, 0.00, "whoosh_deep", 0.8),
]


def esc(s):
    return s.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace(",", "\\,")


def vf_for(sub, overlay, dur):
    f = ["scale=480:854", "fps=24", "format=yuv420p"]
    if overlay == "LOCK":   # hunter targeting brackets + LOCK tag, amber, flashing in
        c = "0xFFB340"
        for x, y, w, h in ((170, 330, 40, 6), (170, 330, 6, 40), (270, 330, 40, 6), (304, 330, 6, 40),
                           (170, 494, 40, 6), (170, 460, 6, 40), (270, 494, 40, 6), (304, 460, 6, 40)):
            f.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color={c}@0.9:t=fill:enable='gt(t,0.3)'")
        f.append(f"drawtext=fontfile='{FONT}':text='LOCK':fontcolor={c}:fontsize=22:x=318:y=470:enable='gt(t,0.5)*lt(mod(t,0.4),0.28)'")
    if sub:
        parts = sub.split("|")
        span = dur / len(parts)
        for i, p in enumerate(parts):
            a, b = i * span + 0.1, (i + 1) * span - 0.05
            f.append(f"drawtext=fontfile='{FONT}':text='{esc(p)}':fontcolor=white:fontsize=24:borderw=2:bordercolor=black@0.7:"
                     f"x=(w-text_w)/2:y=h*0.70:enable='between(t,{a:.2f},{b:.2f})'")
    return ",".join(f)


def main():
    music, suffix = sys.argv[1], sys.argv[2]
    takes = json.loads((HERE / "DRAFT_JOBS.json").read_text(encoding="utf-8"))["takes"]
    picture = HERE / f"drafts/_v03_picture_{suffix}.mp4"
    out = HERE / f"drafts/DRAFT_EDIT_v03_{suffix}.mp4"
    t, rows, duck = 0.0, [], []
    with tempfile.TemporaryDirectory() as d:
        parts = []
        for i, (tid, a, b, keep, sub, ov) in enumerate(EDL):
            dur = b - a
            p = pathlib.Path(d) / f"{i:02d}.mp4"
            cmd = [str(FF), "-loglevel", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", str(HERE / takes[tid]["result"])]
            if keep:
                cmd += ["-map", "0:v:0", "-map", "0:a:0"]
                duck.append((t, t + dur))
            else:
                cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v:0", "-map", "1:a:0"]
            cmd += ["-vf", vf_for(sub, ov, dur), "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                    "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest", str(p)]
            subprocess.run(cmd, check=True)
            parts.append(p)
            rows.append(dict(take=tid, src_in=a, src_out=b, edit_in=round(t, 2), dur=round(dur, 2), native_audio=keep,
                             subtitle=sub, overlay=ov, draft_job_id=takes[tid]["draft_job_id"]))
            t += dur
        lst = pathlib.Path(d) / "list.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
        subprocess.run([str(FF), "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(picture)], check=True)
    # Music under everything (ducked 9 dB under native dialogue, tail fade) + SFX cues on the action.
    starts, acc = [], 0.0
    for r in EDL:
        starts.append(acc); acc += r[2] - r[1]
    duck_expr = "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in duck) or "0"
    inputs = ["-i", str(picture), "-i", str(HERE / music)]
    fc = [f"[1:a]atrim=0:{t:.2f},volume='if({duck_expr},0.35,1.0)':eval=frame,afade=t=out:st={t - 1.5:.2f}:d=1.5[m]"]
    mix = ["[0:a]", "[m]"]
    for k, (row, off, name, vol) in enumerate(SFX):
        inputs += ["-i", str(HERE / "sfx" / name)]
        ms = max(0, int((starts[row] + off) * 1000))
        fc.append(f"[{k + 2}:a]aresample=48000,volume={vol},adelay={ms}|{ms}[s{k}]")
        mix.append(f"[s{k}]")
    fc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.8[a]")
    subprocess.run([str(FF), "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{t:.2f}", str(out)], check=True)
    picture.unlink()
    (HERE / f"DRAFT_EDIT_v03_{suffix}_EDL.json").write_text(json.dumps(dict(runtime_s=round(t, 2), music=music, rows=rows), indent=2), encoding="utf-8")
    turn = next(r["edit_in"] for r in rows if r["take"] == "T19")
    print(out.name, "runtime", round(t, 2), "s; decoy turn at", turn, "s =", round(100 * turn / t), "%")


if __name__ == "__main__":
    main()

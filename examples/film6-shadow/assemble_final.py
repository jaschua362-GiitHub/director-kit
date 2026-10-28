"""FINAL 1080x1920 assembly of the locked v08 edit (Jason 27 Oct, FINISHING_PLAN.md).
Same EDL, cues and voices as v08; the picture is rebuilt at 1080x1920 from graded plates:
  - LOCAL cuts: finish/graded/<take>_<label>_1080x1920.mkv (Real-ESRGAN from the original take, 12-frame handles, E1N)
  - HD cuts: Seedance 1080p promotions of T01 / T17b (lip-synced in ChatCut when available), E1N
  - POV cuts keep their optic grade (ungraded upscale + HUD re-rendered at 1080); the H3 title keeps its own look
The audio is the v08 mix, copied bit-for-bit. Usage: python assemble_final.py -> drafts/SHADOW_FINAL_1080x1920.mp4

Draft edit v08 = v07 + Jason's title notes (27 Oct): heavier title hits (sub-boom, reverse swell, pre-hit gap,
louder cues) and a complete fade to full black instead of fading out on the last frame.

Draft edit v07 = v06 (approved draft edit, 27 Oct) + animated end title: MiniMax H3 kinetic build (black -> Jason's
codex-v03 poster as end frame), retimed to finish at 60.0 s, exact poster PNG crossfaded over the last second.

Draft edit v06 = v05 + Jason's v05 notes (27 Oct): Kaede stays silent on camera - her "Go" is a comm double-click
sent with the wrist tap; "Nice decoy" re-voiced for clarity; comm filter opened up.

Draft edit v05 = v04 + Jason's v04 notes (27 Oct): ending eases into the hold (no jerk); clear Japanese voices + lip sync.

v04 notes, still applied:

1 subtitles down to the bottom title-safe line; Aiko's comm lines in italics (off-screen voice, not Kaede's)
2 hunter POV rebuilt as machine vision (amber grade, scanlines, converging LOCK, telemetry) - hud.py
3 sound redesigned: rooftop ambience bed under everything, continuous hunter rotor, measured foley,
  POV perspective shift (music low-passed, world drops away inside the optics), loudness-normalised
4 the failed yaw replaced: TGT 02 alert motivates a committed whip (T14 3.5-4.9 at 1.6x) into the decoy track
5 ending holds Kaede's look and fades out with the music tail (room for the title card)
6 scan shot is Kaede's goggle view: red flash in, ruby spectrum, sweep reveals the approved hunter as a heat signature
also: T01 re-trimmed so her line (source 4.0-4.9 s) is in; cold open on sound design, score enters on the team shot.

Cues are keyed by EDL label, never by row number. Usage: python assemble_v08.py  -> drafts/DRAFT_EDIT_v08.mp4
"""
import json, os, pathlib, subprocess, sys, tempfile
import hud

HERE = pathlib.Path(__file__).resolve().parent
FF = hud.FF
FONT, FONT_I = "C\\:/Windows/Fonts/arialbd.ttf", "C\\:/Windows/Fonts/arialbi.ttf"
OUT = HERE / os.environ.get("DCL_OUT", "drafts/SHADOW_FINAL_1080x1920.mp4")
hud.configure(1080, 1920)
# title: H3 take D (round 2) at natural speed, 0.8-6.8 s + 1 s poster hold - no slow-down drag (Jason 27 Oct)

# subtitles: (text, start, end, italic=off-screen comm voice), times relative to the segment
EDL = [
    dict(label="hook", take="T01", a=0.0, b=1.45),
    dict(label="scan", take="T03", a=2.0, b=3.8, pov="kaede"),
    dict(label="report", take="T01ls", a=0.3, b=1.958, subs=[("One at the exit.", 0.4, 1.66, False)]),
    dict(label="team", take="T02", a=0.2, b=1.8),
    dict(label="perch", take="T04", a=0.0, b=1.4, subs=[("Then I go faster.", 0.05, 1.4, True)]),
    dict(label="go", take="T05", a=0.6, b=2.0),
    dict(label="cloak", take="T05b", a=1.0, b=4.2),
    dict(label="spring", take="T04", a=2.0, b=3.4),
    dict(label="sprint", take="T06", a=0.3, b=2.1),
    dict(label="vault", take="T07b", a=0.0, b=2.4),
    dict(label="lens", take="T08", a=0.4, b=1.2),
    dict(label="launch", take="T09b", a=0.0, b=1.6),
    dict(label="tuck", take="T10", a=0.4, b=3.2),
    dict(label="land", take="T11", a=1.5, b=4.96),   # Jason v04: end on her look up into the lens
    dict(label="rise", take="T12", a=0.4, b=2.4),
    dict(label="eye", take="T13", a=1.0, b=2.0),
    dict(label="lock", take="T14", a=0.3, b=2.1, pov="hunter_lock"),
    dict(label="whip", take="T14", a=3.5, b=4.9, speed=1.6, pov="hunter_whip"),
    dict(label="decoy", take="T19", a=0.0, b=3.6, pov="hunter_track"),
    dict(label="peel", take="T15", a=0.8, b=2.8),
    dict(label="door", take="T16", a=0.0, b=2.4, subs=[("Nice decoy.", 0.75, 2.4, True)]),
    dict(label="recog", take="T17bls", a=0.0, b=4.2,
         subs=[("…That wasn't me.", 1.3, 2.3, False), ("Then who moved like me?", 2.4, 4.2, True)]),
    dict(label="eyeturn", take="T18", a=1.0, b=4.5, subs=[("Then who moved like me?", 0.0, 1.2, True)]),
    dict(label="end", take="T17bls", a=4.2, b=5.56, ease=(0.5, 2.5, 0.35), fade=1.9),
    dict(label="title", take="TITLE_H3", a=0.8, b=6.8, tail=2.3, poster=(2.6, 0.4), fade=0.8, black=0.5),   # poster holds, then fades fully to black   # H3 title at natural speed; poster lands crisp
]

GRADE = {
    "hunter": "hue=s=0.18,colorchannelmixer=rr=1.08:gg=0.86:bb=0.55,eq=contrast=1.12:gamma=1.3,noise=alls=4:allf=t,"
              "vignette=angle=PI/4.2,drawgrid=w=iw:h=3:t=1:c=black@0.22",
    "kaede": "hue=s=0,colorchannelmixer=rr=0.95:gg=0.22:bb=0.28,eq=contrast=1.35:brightness=-0.04,noise=alls=3:allf=t,"
             "vignette=angle=PI/4",
}

# SFX cues: (label, offset s, file, volume, source in s, max dur s)
CUES = [
    ("hook", 0.55, "sfx/goggles_click", 0.45, 0.25, 0.6),
    ("scan", 0.0, "sfx2/visor_scan.mp3", 0.9, 0.6, 1.4),
    ("go", 0.3, "sfx2/comm_double_click.wav", 0.8, 0.0, 0.4),   # Kaede's silent "go": two clicks on the comm
    ("cloak", 0.0, "sfx2/cloak_activate.mp3", 1.0, 0.3, 2.7),
    ("spring", 0.45, "sfx2/cloth_whip.mp3", 0.35, 0.2, 0.9),
    ("sprint", 0.0, "sfx2/foley_run.mp3", 0.55, 0.1, 1.8),
    ("vault", 0.35, "sfx2/foley_vault_land.mp3", 0.5, 0.0, 0.7),
    ("lens", 0.0, "sfx2/optic_servo.mp3", 0.9, 0.3, 0.8),
    ("launch", 0.1, "sfx/whoosh_deep", 0.45, 0.2, 1.0),
    ("tuck", 0.3, "sfx2/cloth_whip.mp3", 0.3, 1.3, 0.6),
    ("land", -0.05, "sfx2/foley_vault_land.mp3", 0.7, 1.1, 1.2),
    ("eye", 0.0, "sfx2/optic_servo.mp3", 0.8, 0.6, 0.9),
    ("lock", 0.38, "sfx2/hud_lock.mp3", 0.4, 0.0, 0.7),
    ("lock", 1.25, "sfx2/target_alert.mp3", 0.5, 0.0, 0.85),
    ("whip", 0.0, "sfx/whoosh_deep", 0.6, 0.3, 0.9),
    ("decoy", 0.05, "sfx2/hud_lock.mp3", 0.25, 0.8, 0.5),
    ("peel", 0.2, "sfx/whoosh_airy", 0.45, 0.0, 0.8),
    # end title: the film's own sound family, synced to H3 take D's action (Jason: consistency with the main spot)
    ("title", 0.0, "sfx/glitch_tv", 0.75, 0.3, 0.6),
    ("title", 0.38, "sfx/whoosh_deep", 1.0, 0.3, 0.9),
    ("title", 0.41, "sfx2/cloth_whip.mp3", 0.6, 0.2, 0.9),
    ("title", 1.5, "sfx2/foley_vault_land.mp3", 1.1, 1.1, 1.0),
    ("title", 1.5, "sfx2/sub_thump.wav", 0.9, 0.0, 0.6),
    ("title", 2.4, "sfx/whoosh_airy", 0.65, 0.0, 0.8),
    ("title", 3.45, "sfx2/katana_slash.mp3", 1.2, 0.0, 1.4),
    ("title", 3.45, "sfx2/sub_thump.wav", 0.7, 0.0, 0.6),
    ("title", 3.82, "sfx2/rev_swell.wav", 0.9, 0.0, 0.8),   # swell rises into the slam
    ("title", 4.62, "sfx2/title_impact.mp3", 1.4, 0.0, 2.9),
    ("title", 4.62, "sfx2/sub_boom.wav", 1.0, 0.0, 1.8),
]

# v05 voices (official voices, chosen by Jason 27 Oct: Kaede = Thoughtful, Aiko = Vivi). Kaede's two on-camera lines are
# lip-synced (T01ls / T17bls are the lip-synced clips of T01 3.0-4.96 and T17b 2.4-7.96 with these exact tracks).
# (label, offset s, file, source in s, max dur s, treatment)
VOICES = [
    ("report", -0.3, "lipsync/L1_audio_K1.wav", 0.0, 1.958, "local"),
    ("perch", -0.1, "voice/A1_motto_hayaku.mp3", 0.2, 1.4, "comm"),
    ("door", 0.75, "voice/A2b_ii_otori_clear.mp3", 0.15, 2.0, "comm"),
    ("recog", 0.0, "lipsync/L2_audio_K3.wav", 0.0, 5.56, "local"),
    ("recog", 2.3, "voice/A3_dare_ga.mp3", 0.3, 3.1, "comm"),
]
VOICE_FX = {"comm": "highpass=f=280,lowpass=f=4600,acompressor=threshold=-22dB:ratio=4:attack=5:release=80,volume=2.4",
            "local": "highpass=f=90,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,volume=1.9"}
LOCAL_TAKES = {"T01ls": "lipsync/L1_T01_ls.mp4", "T17bls": "lipsync/L2_T17b_ls.mp4",
               "TITLE": "title/codex-v03-STILL/exports/The-Shadow-Apprentice-title-1080x1920.png",
               "TITLE_H3": "title/h3/H3_title.mp4"}
POSTER = HERE / "title/codex-v03-STILL/exports/The-Shadow-Apprentice-title-1080x1920.png"

SCORE, DROP, TAIL, LENGTH, GAP = "music/score_C_japanese_fusion.mp3", 9.0, 168.5, 187.0, 1.2


def starts():
    t, s = 0.0, {}
    for r in EDL:
        r["a"], r["b"] = (round(r[k] * hud.FPS) / hud.FPS for k in ("a", "b"))   # in/out on the source frame grid
        r["dur"] = (r["b"] - r["a"]) / r.get("speed", 1) + r.get("hold", 0) + (r["ease"][0] * (r["ease"][1] - 1) + r["ease"][2] if r.get("ease") else 0) + r.get("tail", 0)
        r["dur"] = round(r["dur"] * hud.FPS) / hud.FPS   # whole frames: fractional segments left timestamp gaps = held frames at cuts
        s.setdefault(r["label"], t)
        r["t0"] = t
        t += r["dur"]
    return s, t


def esc(s):
    return s.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace(",", "\\,")


def sub_filters(subs):
    out = []
    for text, a, b, ital in subs:
        out.append(f"drawtext=fontfile='{FONT_I if ital else FONT}':text='{esc(text)}':fontcolor=white:fontsize=52:"
                   f"borderw=2:bordercolor=black@0.5:shadowx=4:shadowy=4:shadowcolor=black@0.55:"
                   f"x=(w-text_w)/2:y=h*0.905-text_h:enable='between(t,{a:.2f},{b:.2f})'")
    return out


def render_segment(i, r, src, tmp):
    p = tmp / f"{i:02d}.mkv"   # mkv: no mp4 edit list, so the first frame is never dropped on decode
    dur = r["dur"]
    # rebase timestamps before fps: a seeked input otherwise repeats its first frame (a 1-frame hitch at every cut in v04)
    pre = [f"setpts=(PTS-STARTPTS)/{r.get('speed', 1)}", f"scale={hud.OW}:{hud.OH}:flags=lanczos", f"fps={hud.FPS}:start_time=0"]
    if r.get("hold"):
        pre += [f"tpad=stop_mode=clone:stop_duration={r['hold']}",
                f"scale=eval=frame:w='trunc({hud.W}*(1+0.035*t/{dur:.2f})/2)*2':h=-2", f"crop={hud.W}:{hud.H}"]
    if r.get("tail"):   # clone the last frame (hidden under the poster overlay)
        pre.append(f"tpad=stop_mode=clone:stop_duration={r['tail']}")
    if r.get("ease"):   # v05 ending: decelerate into the hold (motion-interpolated slow-down, short clone), sub-pixel push
        tail, k, pad = r["ease"]
        cut = r["b"] - r["a"] - tail
        n = round(dur * hud.FPS)
        ease = (f"split[ea][eb];[ea]trim=0:{cut:.3f},setpts=PTS-STARTPTS[e1];"
                f"[eb]trim={cut:.3f},setpts=(PTS-STARTPTS)*{k},minterpolate=fps={hud.FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
                f"tpad=stop_mode=clone:stop_duration={pad}[e2];[e1][e2]concat=n=2:v=1:a=0,"
                f"scale={hud.OW * 2}:{hud.OH * 2},zoompan=z='1+0.045*on/{n}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={hud.OW}x{hud.OH}:fps={hud.FPS}")
        pre.append(ease)
    pov = r.get("pov")
    ov = None
    if pov:
        pre.append(GRADE["kaede" if pov == "kaede" else "hunter"])
        pre.append("fade=t=in:st=0:d=0.12:color=0xff3040" if pov == "kaede" else
                   "fade=t=in:st=0:d=0.08:color=0xffb246" if pov == "hunter_lock" else "null")
        if pov == "hunter_whip":
            pre.append("rgbashift=rh=-5:bh=5")
        ov = tmp / f"hud_{r['label']}"
        if pov == "kaede":
            hud.render_kaede_scan(ov, dur, src, r["a"])
        elif pov == "hunter_lock":
            hud.render_hunter_lock(ov, dur)
        elif pov == "hunter_whip":
            hud.render_hunter_whip(ov, dur)
        else:
            hud.render_hunter_track(ov, dur, hud.amber_track(src, r["a"], r["b"]))
    pre.append(f"tpad=stop_mode=clone:stop=8,trim=end_frame={round(dur * hud.FPS)},setpts=N/({hud.FPS}*TB)")   # unique per-frame stamps   # exact frame count
    post = sub_filters(r.get("subs", []))
    if r.get("fade"):
        post.append(f"fade=t=out:st={dur - r['fade'] - r.get('black', 0):.2f}:d={r['fade']}")   # 'black': seconds of pure black after the fade
    post.append("format=yuv420p")
    if r.get("still"):
        lead, fin, fout = r["still"]
        pre.append(f"fade=t=in:st={lead}:d={fin},fade=t=out:st={dur - fout:.2f}:d={fout}")
        cmd = [str(FF), "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(hud.FPS), "-t", f"{dur + 0.1:.3f}", "-i", str(src)]
    else:
        cmd = [str(FF), "-loglevel", "error", "-y", "-ss", f"{r['a']:.3f}", "-t", f"{r['b'] - r['a'] + 0.1:.3f}", "-i", str(src)]
    if r.get("poster"):   # exact poster PNG fades in over the H3 end frame, so the final typography is the real art
        ov = POSTER
        cmd += ["-loop", "1", "-framerate", str(hud.FPS), "-t", f"{dur + 0.1:.3f}", "-i", str(POSTER)]
    elif ov:
        cmd += ["-framerate", str(hud.FPS), "-i", str(ov / "%04d.png")]
    cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    na = 2 if ov else 1
    fc = f"[0:v]{','.join(pre)}[p];"
    if r.get("poster"):
        pin, pfade = r["poster"]
        fc += (f"[1:v]scale={hud.OW}:{hud.OH}:flags=lanczos,format=rgba,fade=t=in:st={dur - pin:.2f}:d={pfade}:alpha=1,setpts=N/({hud.FPS}*TB)[pp];"
               f"[p][pp]overlay=0:0:shortest=1[q];[q]{','.join(post)}[v]")
    else:
        fc += f"[p][1:v]overlay=0:0:eof_action=pass[q];[q]{','.join(post)}[v]" if ov else f"[p]{','.join(post)}[v]"
    if r.get("audio"):
        fc += f";[0:a]aresample=48000,apad,atrim=0:{dur:.3f}" + (f",afade=t=out:st={dur - r['fade']:.2f}:d={r['fade']}" if r.get("fade") else "") + "[a]"
    else:
        fc += f";[{na}:a]anull[a]"
    # picture and sound leave as separate files with exact frame / sample counts, so the joins cannot drift
    cmd += ["-filter_complex", fc, "-map", "[v]", "-frames:v", str(round(dur * hud.FPS)), "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-bf", "0",
            "-an", str(p), "-map", "[a]", "-t", f"{dur:.5f}", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(p.with_suffix(".wav"))]
    subprocess.run(cmd, check=True)
    return p


LS = {"T01ls": ("finish/hd/L1_T01_HD_ls.mp4", "finish/hd/T01-1080p-70f1a537.mp4", 3.0),
      "T17bls": ("finish/hd/L2_T17b_HD_ls.mp4", "finish/hd/T17b-1080p-c8787281.mp4", 2.4)}
HD = {"T01": "finish/hd/T01-1080p-70f1a537.mp4", "T17b": "finish/hd/T17b-1080p-c8787281.mp4",
      # Jason 27 Oct (after the first final): landing close-up, jump and drone peel-away also go HD
      "T11": "finish/hd/T11-1080p-e40e3891.mp4", "T09b": "finish/hd/T09b-1080p-4894f6c3.mp4", "T15": "finish/hd/T15-1080p-d9c9cef0.mp4"}
POV_TAKES = {"T03", "T14", "T19"}
MISSING = []


def graded(path):
    g = HERE / os.environ.get("DCL_GRADED", "finish/graded") / (pathlib.Path(path).stem + ".mkv")
    return g if g.exists() else None


def resolve(r):
    """Map an EDL row to its finishing source; shift in/out into that file's own timeline."""
    take, a, b = r["take"], r["a"], r["b"]
    if take == "TITLE_H3":
        return HERE / LOCAL_TAKES[take], a, b
    if take in LS:
        ls, hd, off = LS[take]
        if (HERE / ls).exists():
            src = HERE / ls
        else:   # lip-sync on the HD take not done yet: HD picture without the mouth fix (flagged)
            MISSING.append(f"{r['label']}: lip-sync pending"); src, a, b = HERE / hd, a + off, b + off
        return graded(src) or src, a, b
    if take in HD:
        return graded(HERE / HD[take]) or HERE / HD[take], a, b
    up = HERE / f"finish/up/{take}_{r['label']}_1080x1920.mkv"
    meta = json.loads(pathlib.Path(str(up) + ".json").read_text(encoding="utf-8"))
    off = meta["used_out_offset"] / hud.FPS
    src = up if take in POV_TAKES else (graded(up) or up)
    if src == up and take not in POV_TAKES:
        MISSING.append(f"{r['label']}: ungraded")
    return src, off, off + (b - a)


def between(spans):
    return "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in spans) or "0"


def main():
    takes = json.loads((HERE / "DRAFT_JOBS.json").read_text(encoding="utf-8"))["takes"]
    takes.update({k: dict(result=v, draft_job_id=None) for k, v in LOCAL_TAKES.items()})
    st, total = starts()
    picture = OUT.with_name(OUT.stem + "_picture.mp4")
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d)
        parts = []
        for i, r in enumerate(EDL):
            src, r["a"], r["b"] = resolve(r)
            parts.append(render_segment(i, r, src, tmp))
        # picture: concat filter over video only, restamped by frame index (every part holds an exact frame count);
        # the copy demuxer dropped frames at joins and AAC padding made the a/v concat hold frames
        ins = [x for p in parts for x in ("-i", str(p))]
        fcat = "".join(f"[{k}:v]setpts=PTS-STARTPTS[c{k}];" for k in range(len(parts)))
        fcat += "".join(f"[c{k}]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0,setpts=N/({hud.FPS}*TB)[v]"
        subprocess.run([str(FF), "-loglevel", "error", "-y", *ins, "-filter_complex", fcat, "-map", "[v]", "-fps_mode", "passthrough", "-time_base", f"1/{hud.FPS}",
                        "-c:v", "libx264", "-crf", "17", "-preset", "fast", str(tmp / "pic.mp4")], check=True)
        ins = [x for p in parts for x in ("-i", str(p.with_suffix(".wav")))]
        fcat = "".join(f"[{k}:a]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[a]"
        subprocess.run([str(FF), "-loglevel", "error", "-y", *ins, "-filter_complex", fcat, "-map", "[a]", str(tmp / "dlg.wav")], check=True)
        subprocess.run([str(FF), "-loglevel", "error", "-y", "-i", str(tmp / "pic.mp4"), "-i", str(tmp / "dlg.wav"),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", str(picture)], check=True)
    if "--picture" in sys.argv:
        print("picture only", round(total, 2)); return
    # sound: the approved v08 mix, stream-copied (no re-mix, no re-encode)
    subprocess.run([str(FF), "-loglevel", "error", "-y", "-i", str(picture), "-i", str(HERE / "drafts/DRAFT_EDIT_v08.mp4"),
                    "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", str(OUT)], check=True)
    picture.unlink()
    rows = [dict(label=r["label"], take=r["take"], edit_in=round(r["t0"], 2), dur=round(r["dur"], 2)) for r in EDL]
    (HERE / "SHADOW_FINAL_EDL.json").write_text(json.dumps(dict(runtime_s=round(total, 2), audio="DRAFT_EDIT_v08.mp4 (copied)",
                                                                 pending=MISSING, rows=rows), indent=2, ensure_ascii=False), encoding="utf-8")
    print(OUT.name, "runtime", round(total, 2), "pending:", MISSING or "none")


def _unused_v08_mix(st, total, picture):   # kept for reference: the v08 mix is reused, not rebuilt
    pov = [(r["t0"], r["t0"] + r["dur"]) for r in EDL if r.get("pov")]
    hunter_pov = [(r["t0"], r["t0"] + r["dur"]) for r in EDL if str(r.get("pov", "")).startswith("hunter")]
    bay = [(r["t0"], r["t0"] + r["dur"]) for r in EDL if r["take"] in ("T01", "T01ls", "T05", "T17b", "T17bls", "T18")]
    dlg = [(st[l] + o + 0.3, st[l] + o + d) for l, o, f, a, d, k in VOICES]   # duck the score under every spoken line
    run, turn = st["spring"], st["decoy"]
    lead = max(0.0, run - DROP)                      # cold open: score enters so that its drop lands on the spring-off
    rest = total - turn - GAP
    t3 = max(0.0, min(LENGTH - rest - 0.5, LENGTH - 2))   # the tail now also carries the title card
    rise, peel_end = st["rise"], st["peel"] + 2.0
    slam = st["title"] + 4.62   # SHADOW slams in (H3 take D, source 5.42 s)

    inputs = ["-i", str(picture), "-i", str(HERE / SCORE), "-i", str(HERE / "sfx2/rooftop_amb.mp3"), "-i", str(HERE / "sfx2/hunter_rotor_loop.mp3")]
    fc = [
        # score: intro -> drop on the spring-off -> dead stop at the decoy -> track tail under the recognition
        f"[1:a]aresample=48000,atrim={max(0, DROP - run):.2f}:{DROP + turn - run:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=1.2,"
        f"afade=t=out:st={turn - lead - 0.06:.2f}:d=0.06,adelay={int(lead * 1000)}|{int(lead * 1000)}[m1]",
        f"anullsrc=r=48000:cl=stereo,atrim=0:{GAP}[mg]",
        f"[1:a]aresample=48000,atrim={t3:.2f}:{LENGTH:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=0.4[m3]",
        f"[m1][mg][m3]concat=n=3:v=0:a=1,apad,atrim=0:{total:.2f},afade=t=out:st={total - 2.1:.2f}:d=1.6,"
        f"volume='if({between(dlg)},0.28,1.0)*if(between(t,{slam - 0.35:.2f},{slam:.2f}),0.1,if(gte(t,{st['title']:.2f}),0.6,1))':eval=frame,"
        f"asplit[md][mw]",   # title: score sits under the hits, near-silence just before the slam
        # inside an optic the world drops away: score low-passed, ambience down
        f"[md]volume='if({between(pov)},0,1)':eval=frame[mdry]",
        f"[mw]lowpass=f=900,lowpass=f=900,volume='if({between(pov)},0.9,0)':eval=frame[mwet]",
        f"[2:a]aresample=48000,aloop=loop=-1:size={22 * 48000},atrim=0:{total:.2f},highpass=f=60,"
        f"volume='3.2*if({between(pov)},0.3,if({between(bay)},0.6,1))':eval=frame,afade=t=out:st={st['title'] - 1.6:.2f}:d=1.6[amb]",
        f"[3:a]aresample=48000,aloop=loop=-1:size={8 * 48000},atrim=0:{peel_end - rise:.2f},afade=t=in:d=1.4,"
        f"afade=t=out:st={peel_end - rise - 1.6:.2f}:d=1.6,adelay={int(rise * 1000)}|{int(rise * 1000)},"
        f"volume='0.55*if({between(hunter_pov)},0.55,1)':eval=frame[rot]",
    ]
    sfx = []
    for k, (lab, off, f, vol, a, du) in enumerate(CUES):
        inputs += ["-i", str(HERE / f)]
        ms = max(0, int((st[lab] + off) * 1000))
        fc.append(f"[{k + 4}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={a}:{a + du},asetpts=PTS-STARTPTS,"
                  f"afade=t=out:st={du - 0.12:.2f}:d=0.12,volume={vol},adelay={ms}|{ms}[s{k}]")
        sfx.append(f"[s{k}]")
    # one shared rooftop space for the spot effects (short early reflections), then the full mix is loudness-normalised
    fc.append(f"{''.join(sfx)}amix=inputs={len(sfx)}:normalize=0,aecho=0.8:0.6:35|60:0.14|0.08[sfx]")
    vox = []
    for j, (lab, off, f, a, du, kind) in enumerate(VOICES):
        inputs += ["-i", str(HERE / f)]
        ms = max(0, int((st[lab] + off) * 1000))
        k = len(CUES) + 4 + j
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={a}:{a + du},asetpts=PTS-STARTPTS,{VOICE_FX[kind]},"
                  f"adelay={ms}|{ms}[v{j}]")
        vox.append(f"[v{j}]")
    fc.append(f"{''.join(vox)}amix=inputs={len(vox)}:normalize=0[vox]")
    fc.append("[mdry][mwet][amb][rot][sfx][vox]amix=inputs=6:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.84:level=disabled[a]")
    subprocess.run([str(FF), "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.2f}", str(OUT)], check=True)
    picture.unlink()
    rows = [dict(label=r["label"], take=r["take"], src_in=r["a"], src_out=r["b"], edit_in=round(r["t0"], 2), dur=round(r["dur"], 2),
                 pov=r.get("pov"), speed=r.get("speed"), hold=r.get("hold"), native_audio=bool(r.get("audio")),
                 subs=r.get("subs"), draft_job_id=takes[r["take"]].get("draft_job_id")) for r in EDL]
    (HERE / "SHADOW_FINAL_EDL.json").write_text(json.dumps(dict(runtime_s=round(total, 2), music=SCORE, score_lead_in_s=round(lead, 2),
                                                                  cues=CUES, rows=rows), indent=2, ensure_ascii=False), encoding="utf-8")
    print(OUT.name, "runtime", round(total, 2), "s; decoy turn at", round(turn, 2), "s =", round(100 * turn / total), "%; score enters", round(lead, 2))


if __name__ == "__main__":
    main()

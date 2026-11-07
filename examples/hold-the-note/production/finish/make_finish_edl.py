"""Phase 5C frozen finish EDL (director, 6 Nov 2026). Every build step (picture, mix, subtitles, title join) reads
FINISH_EDL.json. Frames at 24 fps. 'take' frames index the ORIGINAL take (p4_takes / p5_retakes / pilot / native1080);
'src_offset' = take frame of the finish source's frame 0 (SeedVR2 runs used skip=N, so src frame = take frame - N)."""
import json
from pathlib import Path
T = "<LAB>/experiments/TEST-020-hold-the-note/"
P = T + "production/"
SV, SF, NA, TK, RT = P + "p5_finish/seedvr2/", P + "p5_finish/seedvr2_faces/", P + "p5_finish/native1080/", P + "p4_takes/", P + "p5_retakes/"

def shots(f):  # f = 'H' or 'V'
    face = lambda n, off: dict(src=SF + f"{n}{f}.mkv", src_offset=off, route="SeedVR2 from 480p draft (face replan)", draft=TK + f"{n}{f}.mp4")
    less = lambda n, off: dict(src=SV + f"{n}{f}.mkv", src_offset=off, route="SeedVR2 faceless", draft=TK + f"{n}{f}.mp4")
    S = [
        dict(shot=1, take_in=0, n=58, **less("01", 0), effects=(["E1 trickle (shot 1)"] if f == "H" else []),
             note=("" if f == "H" else "D5: 01V keeps the model's own grains; NO E1 on 01V")),
        dict(shot=2, take_in=0, n=62, src=SV + "02S.mkv", src_offset=0, route="SeedVR2 faceless, shared 1:1 take (1920x1920)", draft=TK + "02S.mp4",
             crop=("1920x1080 at (0,0) in SeedVR2 px" if f == "H" else "1080x1920 at (0,0) in SeedVR2 px"),
             push_in="100->104 % linear over the shot, anchored at (530,516) SeedVR2 px (= take (265,258) x2)"),
        dict(shot=3, take_in=10, n=72, **face("03", 7), pending="SeedVR2 face job queued; sheet-check before use"),
        dict(shot=4, take_in=24, n=62, **face("04", 21)),
        dict(shot=5, take_in=2, n=48, **less("05", 0), effects=["E1 shedding (shot 5)"],
             note="in-point moved 0->2: source take has a 4 grey-level exposure pop at frames 0-2 (in the draft too)"),
        dict(shot=6, take_in=36, n=85, src=(T + "pilot/final/S06H_routeA_d02_1080p.mp4" if f == "H" else NA + "06V.mp4"), src_offset=0,
             route="native 1080p (10-bit HEVC: bundled ffmpeg decode only)"),
        dict(shot="7a", take_in=24, n=38, **face("07", 21), note="F2: his face, no inset"),
        dict(shot="7b", n=34, src="E2 core: grain_fx.e2_frames() frames 2-35", src_offset=None,
             crop=("P07 crop x0,y0,w,h = 0,450,1440,810 -> 1920x1080" if f == "H" else "P07 crop 150,0,810,1440 -> 1080x1920"),
             route="F2 full-frame insert cut (approved)", note="as built in p5_fix/preview_fix_6_7.py"),
        dict(shot=8, take_in=14, n=72, **face("08", 11), pending="SeedVR2 face job queued; sheet-check before use"),
        dict(shot=9, take_in=7, n=53, **less("09", 1)),
        dict(shot=10, take_in=(24 if f == "H" else 0), n=52, src=P + "p5c_atlas/" + ("10H_r6a_HD.mp4" if f == "H" else "10V_r2_HD.mp4"), src_offset=0,
             route="native 1080p Seedance 2.5 HD (draft-complete) of a 5C regen draft (10-bit HEVC: bundled ffmpeg decode only)", draft=P + "p5c_atlas/" + ("10H_r6a.mp4" if f == "H" else "10V_r2.mp4"),
             note="5C regen (Jason notes 6 Nov): lips sealed on the blow hole; H r6a (start frame only, fingers lift on the holes) frames 24-75, flute rigid on every HD frame, V r2 frames 0-51 (re-grip ghosts at f52+)"),
        dict(shot=11, take_in=5, n=57, **less("11", 0), note="SeedVR2 batch rhythm checked at 100 %: stable"),
        dict(shot=12, take_in=19, n=78, **face("12", 16), pending="SeedVR2 face job queued; sheet-check before use"),
        dict(shot=13, take_in=7, n=114, src=NA + ("13H_r1.mp4" if f == "H" else "13V.mp4"), src_offset=0,
             route="native 1080p (10-bit HEVC: bundled ffmpeg decode only)", note=("13H_r1 replaces 13H" if f == "H" else "")),
        dict(shot=14, take_in=20, n=101, src=SV + f"14{f}_r1.mkv", src_offset=14, route="SeedVR2 to 4K (clean r1 take), E3 composited at 4K, 2D move, -> 1080",
             take=RT + f"14{f}_r1.mp4", pending="4K SeedVR2 job running", effects=["E3 release"],
             e3=dict(release_start_take=44, collars_reached_take=94, dribble_end_take=102,
                     note="no in-camera release (RIBBON_14r1.json): composite E3. Released region filled per frame from the live frame (never a held plate)."),
             move="2D rise/pull-back: crop window 1/1.12 of the 4K frame at local frame 0, bottom-aligned & centred horizontally -> full frame at local frame 100; smoothstep ease; continues through the dissolve",
             note="cut in at take frame 20 (flute lowered, D1). Last 24 frames (take 97-120) are under the title dissolve."),
    ]
    rec = 0
    for s in S:
        s["rec_in"] = rec; rec += s["n"]; s["rec_out"] = rec
        if s.get("take_in") is not None and s.get("src_offset") is not None:
            s["src_in"] = s["take_in"] - s["src_offset"]
    assert rec == 986, rec
    return S

def subs(f):
    return [
        dict(shot=6, text="Breathe! I'll hold the note!", rec_in=332, rec_out=399, note="F1: holds 0.5 s into shot 7"),
        dict(shot=12, text="You held on well.", rec_in=(740 if f == "H" else 741), rec_out=(769 if f == "H" else 770),
             note="1.2 s, under the 1.5 s minimum (take ends after the line; disclosed since phase 4)"),
        dict(shot=13, text="When did you learn to whistle?", rec_in=(834 if f == "H" else 842), rec_out=(883 if f == "H" else 885),
             note=("13H_r1 speech 2.95-4.67 s take time (energy onset)" if f == "H" else "13V line 3.25-4.85 s take time")),
        dict(shot=14, text="Forty years I've crossed this bridge. That's nothing.", rec_in=(890 if f == "H" else 886), rec_out=961,
             note="r1 speech 1.07/0.88-3.65 s take time; ends before the title dissolve (rec 962). Two lines if needed."),
    ]

edl = dict(
    version="p5c-4 (H shot 10 = r6a HD 24-75), 6 Nov 2026: shot 10 = Seedance HD of 5C regen drafts (H r3 14-65, V r2 0-51); shot 11 original",
    fps=24, total_frames=1190, runtime_s=round(1190 / 24, 3),
    title=dict(rec_in=962, rec_out=1190, n=228, dissolve="title_v3 frames 0-23 cross-dissolve (linear alpha 0->1) over shot 14 rec 962-985; then title frames 24-227 alone",
               src={"H": T + "title-motion/v3/title_v3_H.mp4", "V": T + "title-motion/v3/title_v3_V.mp4"},
               note="title clip has its own fade to black over its last 1.0 s (rec 1166-1190). No black anywhere else. Title clip audio is a TEMP bed: discard it."),
    formats={f: dict(size=("1920x1080" if f == "H" else "1080x1920"), shots=shots(f), subtitles=subs(f)) for f in "HV"},
    audio_cues_s=dict(whistle_in=16.275, flute_out=19.525, breath=20.325, flute_rejoin=24.453, both_stop=27.7,
                      line12_end=31.65, s9_enter=32.15, e3_release_start=(885 + 24) / 24, dissolve=(962 / 24, 986 / 24), end=1190 / 24,
                      note="cues for shots 1-11 are unchanged from the approved draft EDL (p4_edit/EDL.json audio_cues)"),
)
Path(__file__).with_name("FINISH_EDL.json").write_text(json.dumps(edl, indent=1), encoding="utf-8")
print("ok", edl["total_frames"])

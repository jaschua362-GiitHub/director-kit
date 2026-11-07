"""One Beat Late (DCL-20261030-BEAT): final delivery and social materials, per FINAL_DELIVERY_STANDARD.md
("Social materials beside every film", 27 Oct 2026). Adapted from experiments/TEST-013/closeout/package_social_materials.py.

approved/DCL-20261030-BEAT/video-landscape-v01/   approved final + APPROVAL.json (Jason 4 Nov 2026: "final")
FINAL_RENDERED/DCL-20261030-BEAT/
  video-landscape-v01/        library copy + APPROVAL.json + DELIVERY.json
  approved-art-v04/           exact copy of approved/DCL-20261030-BEAT/v04 (+ ARTWORK_DELIVERY_v04.json)
  social-materials/
    posters/                  the approved posters (POSTER_APPROVAL.json, 4 Nov "look good n approve")
    captions/SOCIAL_POSTS.md  the approved captions, copied byte for byte
    film-stills/              seven moments from the approved final at 1920x1080
    stills-2x/                2x local upscales of the 30 approved art stills (content unchanged)
    README.md, SOCIAL_MATERIALS.json
Catalogue: FINAL_RENDERED/INDEX.json, INDEX.md, ARTWORK_INDEX.json, APPROVED_ARTWORK.md. Idempotent.
Usage (Lab root): python -I experiments/TEST-019-one-beat-late/closeout/package_final_delivery.py [--skip-stills]
"""
import datetime, hashlib, json, pathlib, re, shutil, subprocess, sys, tempfile
import cv2, numpy as np
from PIL import Image

LAB = pathlib.Path(__file__).resolve().parents[3]
EXP = LAB / "experiments/TEST-019-one-beat-late"
PID, TITLE, REV = "DCL-20261030-BEAT", "One Beat Late", "video-landscape-v01"
ART = LAB / f"approved/{PID}/v04"
LIB = LAB / "FINAL_RENDERED"
FILM = LIB / PID
SRC_FINAL = EXP / "production/finish/ONE_BEAT_LATE_1080p_v01.mp4"
NAME = "ONE_BEAT_LATE_landscape_v01_1920x1080.mp4"
FF = str(LAB / "experiments/TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
ESR = LAB / "experiments/TEST-005/tools/realesrgan/realesrgan-ncnn-vulkan.exe"
APPROVAL_SRC = json.loads((EXP / "production/finish/FINAL_APPROVAL.json").read_text(encoding="utf-8"))
STILLS = [  # frame, name, note (frames of the 828-frame final; events from production/finish/assembly.json)
    (40, "01_his_print_arrives", "P1: his boot lands on Earth; on the Moon his print forms under the glass"),
    (110, "02_she_checks_the_delay", "P2: she reads her watch beside his print"),
    (300, "03_a_beat_behind", "P5: his grin slips as her print presses in under his toe"),
    (500, "04_his_laugh", "P9: his laugh, the music swells"),
    (550, "05_the_spin", "P10: the music returns on his spin"),
    (645, "06_her_laugh", "P11: her laugh, one beat late"),
    (750, "07_her_hand_answers", "P12: her hand impression answers in the grains"),
]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def now():
    return datetime.datetime.now().astimezone().isoformat()


def dump(p, d):
    p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_checked(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or sha(dst) != sha(src):
        shutil.copy2(src, dst)
    assert sha(dst) == sha(src), dst
    return sha(dst)


def probe(p):
    cap = cv2.VideoCapture(str(p))
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n, fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    info = subprocess.run([FF, "-hide_banner", "-i", str(p)], capture_output=True, text=True).stderr
    dec = subprocess.run([FF, "-v", "error", "-xerror", "-i", str(p), "-f", "null", "-"], capture_output=True, text=True)
    return dict(duration_seconds=round(n / fps, 3), frames=n, width=w, height=h, fps=f"{round(fps)}/1",
                video_codec="h264" if "Video: h264" in info else re.search(r"Video: (\w+)", info).group(1),
                audio_present="Audio:" in info), dec.returncode == 0


def video():
    assert sha(SRC_FINAL) == APPROVAL_SRC["sha256"], "final differs from the approved hash"
    media, decoded = probe(SRC_FINAL)
    assert decoded and media["width"] == 1920 and media["height"] == 1080 and media["audio_present"]
    approval = dict(
        schema_version=1, status="approved", approval_kind="production_video", approver="Jason", recorded_by="Claude",
        project_id=PID, revision=REV, artifact=f"{TITLE}, completed 16:9 picture and sound (1080p final v01)", file=NAME,
        sha256=APPROVAL_SRC["sha256"], approval_statement=APPROVAL_SRC["statement"],
        approved_at_local=APPROVAL_SRC["approved_at_local"], recorded_at_local=now(),
        timestamp_note="Recording time, not independent message time.",
        scope="Exact approved 16:9 1920x1080 picture and sound of the 1080p final v01 (sound cut v11 timing, approved mix, "
              "grade G1). Wordless; no title in the film (the title lives on the YouTube poster).",
        source_experiment_file=SRC_FINAL.relative_to(LAB).as_posix(),
        source_approval="experiments/TEST-019-one-beat-late/production/finish/FINAL_APPROVAL.json",
        earlier_approvals=["production/CUT_APPROVAL.json (music cut v08)", "production/SOUND_APPROVAL.json (sound cut v11)"],
        source_creative_approval=f"approved/{PID}/v04/APPROVAL.json",
        spec=dict(frames=media["frames"], fps=24, width=1920, height=1080, duration_s=media["duration_seconds"],
                  colour="Rec.709 SDR", audio="AAC stereo 48 kHz 320k of sound/stems/mix_final.wav, -14.9 LUFS, -1.1 dBTP after AAC"),
        grade="G1 gentle (production/finish/grade.json): per-shot black re-seat, small mid lift, mild S curve, light halation, "
              "vignette 0.10, grain 1.6; same base in both rooms",
        finishing=dict(
            native_1080p="every readable face (A-F01, B-F01, P02-F02, P06-F02, P07-F01, P12-F02, P11 pilot)",
            local_upscale="SeedVR2 3B on faceless shots only: P01 and P04 (1440p for crop headroom), P12 hand insert",
            composites="every under-glass print and grain effect is a local composite (production/composite/), re-run at 1080p",
            sound="native Seedance 2.5 audio from our takes (his step and pivot, his wince and laugh, her laugh, the watch laugh), "
                  "locally designed hiss, heel, watch and room sounds, MiniMax Music 3.0 take 2; no dialogue, no MiniMax Speech"),
        note=APPROVAL_SRC.get("note"))
    rec = {}
    for root in (LAB / f"approved/{PID}/{REV}", FILM / REV):
        h = copy_checked(SRC_FINAL, root / NAME)
        dump(root / "APPROVAL.json", approval)
        m2, d2 = probe(root / NAME)
        assert d2 and m2 == media
        rec[root] = h
    lib = FILM / REV
    delivery = dict(
        schema_version=1, status="approved_final_render", project_id=PID, title=TITLE, revision=REV, aspect="16:9", file=NAME,
        bytes=(lib / NAME).stat().st_size, sha256=rec[lib], approval_record="APPROVAL.json",
        approval_record_sha256=sha(lib / "APPROVAL.json"), source_file=f"approved/{PID}/{REV}/{NAME}",
        source_approval=f"approved/{PID}/{REV}/APPROVAL.json", approval_statement=APPROVAL_SRC["statement"], media=media,
        verification=dict(source_hash="passed", copied_hash="passed", metadata_probe="passed", full_decode="passed",
                          human_review="Existing Jason approval; no new artistic/motion/audio review asserted"),
        publication_authorized_by_library=False)
    dump(lib / "DELIVERY.json", delivery)
    return delivery


def art_copy():
    dst = FILM / "approved-art-v04"
    files = sorted(p for p in ART.rglob("*") if p.is_file())
    hashes, decoded = {}, []
    for p in files:
        r = p.relative_to(ART).as_posix()
        hashes[r] = copy_checked(p, dst / r)
        if p.suffix.lower() == ".png":
            with Image.open(dst / r) as im:
                im.load(); decoded.append(dict(path=r, width=im.width, height=im.height))
    approval = json.loads((ART / "APPROVAL.json").read_text(encoding="utf-8"))
    rec = dict(schema_version=1, status="approved_final_artwork", project_id=PID, title=TITLE, revision="v04",
               approval=approval, copied_at_local=now(), source_packet=f"approved/{PID}/v04",
               library_packet=f"{PID}/approved-art-v04", approval_sha256=sha(ART / "APPROVAL.json"),
               copied_file_hashes=hashes, decoded_images=decoded,
               copy_verification=dict(status="passed", files=len(hashes), pngs_decoded=len(decoded)),
               video_approval_is_separate=True, original_source_preserved=True, new_generation=False, publication_authorized=False)
    dump(FILM / "ARTWORK_DELIVERY_v04.json", rec)
    return len(hashes), len(decoded)


def still_sources():
    return sorted(list((ART / "images").glob("*.png")) + list((ART / "approved-faces/images").glob("*.png"))
                  + list((ART / "environments").rglob("*.png")))


def stills_2x(out):
    out.mkdir(parents=True, exist_ok=True)
    imgs = still_sources()
    made = {}
    todo = [p for p in imgs if not (out / (p.stem + "_2x.png")).exists()]
    if todo:
        with tempfile.TemporaryDirectory() as d:
            nat, ai = pathlib.Path(d) / "n", pathlib.Path(d) / "a"
            nat.mkdir(); ai.mkdir()
            for p in todo:
                shutil.copy2(p, nat / p.name)
            r = subprocess.run([str(ESR), "-i", str(nat), "-o", str(ai), "-m", str(ESR.parent / "models"), "-n", "realesrgan-x4plus",
                                "-s", "4", "-t", "256", "-f", "png"], cwd=ESR.parent, capture_output=True)
            assert r.returncode == 0, r.stderr[-400:]
            for p in todo:
                base = cv2.imread(str(nat / p.name)); h, w = base.shape[:2]; W, H = w * 2, h * 2
                b = cv2.resize(base, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
                u = cv2.resize(cv2.imread(str(ai / p.name)), (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
                assert u.mean() > 0.6 * b.mean(), f"dark AI output {p.name}"
                cv2.imwrite(str(out / (p.stem + "_2x.png")), np.clip(0.3 * b + 0.7 * u, 0, 255).astype(np.uint8))
    for p in imgs:
        o = out / (p.stem + "_2x.png")
        with Image.open(o) as im:
            size = list(im.size)
        made[o.name] = dict(source=p.relative_to(ART).as_posix(), source_sha256=sha(p), size=size, sha256=sha(o))
    return made


def film_stills(out, final):
    out.mkdir(parents=True, exist_ok=True)
    made = {}
    for f, name, note in STILLS:
        o = out / f"BEAT_{name}_1920x1080.png"
        if not o.exists():
            subprocess.run([FF, "-v", "error", "-y", "-i", str(final), "-vf", f"select=eq(n\\,{f})", "-fps_mode", "passthrough",
                            "-frames:v", "1", str(o)], check=True)
        made[o.name] = dict(source=f"approved final, frame {f} ({f / 24:.2f} s)", note=note, sha256=sha(o))
    return made


def social(skip_stills):
    sm = FILM / "social-materials"
    final = FILM / REV / NAME
    posters = {}
    pa = json.loads((EXP / "posters/POSTER_APPROVAL.json").read_text(encoding="utf-8"))
    for rel, use in [("returns/IG-9x16-a02.png", "Instagram 9:16 cover / Reel poster (no title)"),
                     ("returns/YT-16x9-final-B2-1920x1080.png", "YouTube thumbnail, full-quality PNG (title B2)"),
                     ("returns/YT-16x9-final-B2-1920x1080.jpg", "YouTube thumbnail JPG for upload (title B2)")]:
        src = EXP / "posters" / rel
        assert sha(src) == pa["files"][rel], f"poster differs from approval: {rel}"
        posters["posters/" + src.name] = dict(source=f"experiments/TEST-019-one-beat-late/posters/{rel}", use=use,
                                              sha256=copy_checked(src, sm / "posters" / src.name))
    cap_src = EXP / "closeout/SOCIAL_POSTS.md"
    captions = {"captions/SOCIAL_POSTS.md": dict(source="experiments/TEST-019-one-beat-late/closeout/SOCIAL_POSTS.md",
                                                  note="approved by Jason 4 Nov 2026; byte-for-byte copy, text unchanged",
                                                  sha256=copy_checked(cap_src, sm / "captions/SOCIAL_POSTS.md"))}
    fs = film_stills(sm / "film-stills", final)
    s2 = {} if skip_stills else stills_2x(sm / "stills-2x")
    rec = dict(schema_version=1, status="social_materials_from_approved_film", project_id=PID, created_at_local=now(),
               standard="FINAL_DELIVERY_STANDARD.md, social materials beside every film (27 Oct)",
               posters=dict(approval="experiments/TEST-019-one-beat-late/posters/POSTER_APPROVAL.json",
                            statement=pa["statement"], files=posters),
               captions=captions, film_stills=fs,
               stills_2x=dict(method="Real-ESRGAN x4plus (local) + Lanczos 70/30, output 2x of native (Lab stills recipe; "
                                     "SeedVR2 was used only for the film's faceless video shots)", files=s2),
               end_title="none: the film is wordless and has no title by direction; the title is on the YouTube poster",
               approved_art_exact_copy="../approved-art-v04 (see ../ARTWORK_DELIVERY_v04.json)",
               posting_kit="<artifact link, not in kit>",
               notes="Derived from approved material; no new generation, no new approval implied. Posting is Jason's decision.",
               publication_authorized=False)
    dump(sm / "SOCIAL_MATERIALS.json", rec)
    return len(posters), len(fs), len(s2)


def catalogue(delivery, n_img):
    idx_p = LIB / "INDEX.json"
    idx = json.loads(idx_p.read_text(encoding="utf-8"))
    entry = dict(delivery, library_file=f"{PID}/{REV}/{NAME}", delivery_record=f"{PID}/{REV}/DELIVERY.json")
    idx["entries"] = [e for e in idx["entries"] if not (e.get("project_id") == PID and e.get("revision") == REV)] + [entry]
    art_entry = dict(delivery_record=f"{PID}/ARTWORK_DELIVERY_v04.json", image_count=n_img, library_packet=f"{PID}/approved-art-v04",
                     project_id=PID, project_readme=f"{PID}/README.md", revision="v04", status="approved_final_artwork", title=TITLE)
    idx["artwork_entries"] = [e for e in idx["artwork_entries"] if e.get("project_id") != PID] + [art_entry]
    dump(idx_p, idx)
    ai_p = LIB / "ARTWORK_INDEX.json"
    ai = json.loads(ai_p.read_text(encoding="utf-8"))
    ai["entries"] = [e for e in ai["entries"] if e.get("project_id") != PID] + [art_entry]
    dump(ai_p, ai)
    d = delivery["media"]
    row = (f"| {TITLE} | {REV} / 16:9 | [Play]({PID}/{REV}/{NAME}) | {d['duration_seconds']:.2f}s / 1920×1080 | "
           f"[Record]({PID}/{REV}/APPROVAL.json) |")
    art_line = (f"- {TITLE} / v04: [all final art and handoff]({PID}/approved-art-v04/START_HERE.md) / "
                f"[film folder]({PID}/README.md).")
    md = (LIB / "INDEX.md").read_text(encoding="utf-8")
    if row not in md:
        anchor = "\n\n## Approved artwork and creative handoffs"
        md = md.replace(anchor, "\n" + row + anchor, 1)
    if art_line not in md:
        md = md.replace("\n\nEvery revision remains available.", "\n" + art_line + "\n\nEvery revision remains available.", 1)
    (LIB / "INDEX.md").write_text(md, encoding="utf-8")
    aa = (LIB / "APPROVED_ARTWORK.md").read_text(encoding="utf-8")
    line = (f"- {TITLE} v04: [{n_img} approved images, 2 environment sheets, 2 plans, synopsis and handoff]"
            f"({PID}/approved-art-v04/START_HERE.md) / [social materials]({PID}/social-materials/README.md) / "
            f"[film folder]({PID}/README.md).")
    if line not in aa:
        aa = aa.rstrip("\n") + "\n" + line + "\n"
    (LIB / "APPROVED_ARTWORK.md").write_text(aa, encoding="utf-8")


def main():
    skip = "--skip-stills" in sys.argv
    delivery = video()
    n_files, n_png = art_copy()
    n_post, n_fs, n_s2 = social(skip)
    catalogue(delivery, len(still_sources()))
    print(f"final {delivery['bytes']} B ok | art files {n_files} pngs {n_png} | posters {n_post} | film stills {n_fs} | stills-2x {n_s2}")


if __name__ == "__main__":
    main()

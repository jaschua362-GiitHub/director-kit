"""Film 6 social-material packaging (Jason 27 Oct: "put Higgsfield MiniMax end title animation into a sub folder in final
rendered folder, also all image assets approved still high res into folder ... for social post material").

FINAL_RENDERED/DCL-20261021-SHADOW/
  approved-art-v10/             exact copy of approved/DCL-20261021-SHADOW/v10 (catalogued in ARTWORK_INDEX like Films 3/4)
  ARTWORK_DELIVERY_v10.json     copied-file hashes + PNG decodes
  social-materials/
    end-title/                  H3 take D (2K original), the end title as cut in the approved final (with sound), title poster PNG
    stills-2x/                  2x local Real-ESRGAN upscales of the 39 approved stills (derived, content unchanged)
    SOCIAL_MATERIALS.json       hashes and provenance
Usage: python -I experiments/TEST-013/closeout/package_social_materials.py
"""
import datetime, hashlib, json, pathlib, shutil, subprocess, tempfile
import cv2, numpy as np
from PIL import Image

LAB = pathlib.Path(__file__).resolve().parents[3]
TEST = LAB / "experiments/TEST-013"
SRC = LAB / "approved/DCL-20261021-SHADOW/v10"
FILM = LAB / "FINAL_RENDERED/DCL-20261021-SHADOW"
FF = str(LAB / "experiments/TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")
ESR = LAB / "experiments/TEST-005/tools/realesrgan/realesrgan-ncnn-vulkan.exe"
FINAL = FILM / "video-portrait-v01/SHADOW_APPRENTICE_portrait_v01_1080x1920.mp4"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def now():
    return datetime.datetime.now().astimezone().isoformat()


def art_copy():
    dst = FILM / "approved-art-v10"
    if not dst.exists():
        shutil.copytree(SRC, dst)
    files = sorted(p for p in SRC.rglob("*") if p.is_file())
    hashes, decoded = {}, []
    for p in files:
        r = p.relative_to(SRC).as_posix()
        hs, hd = sha(p), sha(dst / r)
        assert hs == hd, f"copy mismatch {r}"
        hashes[r] = hd
        if p.suffix.lower() == ".png":
            with Image.open(dst / r) as im:
                im.load(); decoded.append(dict(path=r, width=im.width, height=im.height))
    approval = json.loads((SRC / "APPROVAL.json").read_text(encoding="utf-8"))
    rec = dict(schema_version=1, status="approved_final_artwork", project_id="DCL-20261021-SHADOW", title="The Shadow Apprentice",
               revision="v10", approval_statement=approval.get("art_approval_statement"),
               synopsis_approval_statement=approval.get("synopsis_approval_statement"), approval_date="2026-10-22",
               copied_at_local=now(), source_packet="approved/DCL-20261021-SHADOW/v10",
               library_packet="DCL-20261021-SHADOW/approved-art-v10", approval_sha256=sha(SRC / "APPROVAL.json"),
               copied_file_hashes=hashes, decoded_images=decoded,
               copy_verification=dict(status="passed", files=len(hashes), pngs_decoded=len(decoded)),
               video_approval_is_separate=True, original_source_preserved=True, new_generation=False, publication_authorized=False)
    (FILM / "ARTWORK_DELIVERY_v10.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(hashes), len(decoded)


def stills_2x(out):
    out.mkdir(parents=True, exist_ok=True)
    imgs = sorted((SRC / "images").rglob("*.png"))
    with tempfile.TemporaryDirectory() as d:
        nat, ai = pathlib.Path(d) / "n", pathlib.Path(d) / "a"
        nat.mkdir(); ai.mkdir()
        for p in imgs:
            shutil.copy2(p, nat / p.name)
        r = subprocess.run([str(ESR), "-i", str(nat), "-o", str(ai), "-m", str(ESR.parent / "models"), "-n", "realesrgan-x4plus",
                            "-s", "4", "-t", "256", "-f", "png"], cwd=ESR.parent, capture_output=True)
        assert r.returncode == 0, r.stderr[-400:]
        made = {}
        for p in imgs:
            base = cv2.imread(str(nat / p.name)); h, w = base.shape[:2]; W, H = w * 2, h * 2
            b = cv2.resize(base, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
            u = cv2.resize(cv2.imread(str(ai / p.name)), (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
            assert u.mean() > 0.6 * b.mean(), f"dark AI output {p.name}"
            name = p.stem + "_2x.png"
            cv2.imwrite(str(out / name), np.clip(0.3 * b + 0.7 * u, 0, 255).astype(np.uint8))
            made[name] = dict(source=p.relative_to(SRC).as_posix(), source_sha256=sha(p), size=[W, H], sha256=sha(out / name))
    return made


def end_title(out):
    out.mkdir(parents=True, exist_ok=True)
    h3 = TEST / "title/h3/H3_take_D_2c3d311a.mp4"
    poster = TEST / "title/codex-v03-STILL/exports/The-Shadow-Apprentice-title-1080x1920.png"
    shutil.copy2(h3, out / "SHADOW_end_title_MiniMaxH3_takeD_1440x2560_silent.mp4")
    shutil.copy2(poster, out / "SHADOW_title_poster_1080x1920.png")
    edl = json.loads((TEST / "SHADOW_FINAL_EDL.json").read_text(encoding="utf-8"))
    t = next(r for r in edl["rows"] if r["label"] == "title")
    clip = out / "SHADOW_end_title_as_in_film_1080x1920.mp4"
    subprocess.run([FF, "-v", "error", "-y", "-ss", f"{t['edit_in']:.3f}", "-i", str(FINAL), "-t", f"{t['dur']:.3f}", "-c:v", "libx264",
                    "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
                    str(clip)], check=True)
    subprocess.run([FF, "-v", "error", "-xerror", "-i", str(clip), "-f", "null", "-"], check=True)
    return {
        out.name + "/" + "SHADOW_end_title_MiniMaxH3_takeD_1440x2560_silent.mp4":
            dict(source="experiments/TEST-013/title/h3/H3_take_D_2c3d311a.mp4 (Higgsfield minimax_h3 job 2c3d311a-6460-4071-92e0-a9cc2538f94b)",
                 note="raw 8 s 2K generation, no sound; the film uses 0.8-6.8 s of it", sha256=sha(out / "SHADOW_end_title_MiniMaxH3_takeD_1440x2560_silent.mp4")),
        out.name + "/" + clip.name:
            dict(source=f"approved final {FINAL.name}, {t['edit_in']} s + {t['dur']} s", note="the end title exactly as in the approved film, with its sound design",
                 sha256=sha(clip)),
        out.name + "/SHADOW_title_poster_1080x1920.png":
            dict(source="experiments/TEST-013/title/codex-v03-STILL/exports/The-Shadow-Apprentice-title-1080x1920.png",
                 note="title poster still; the final frame of the approved film's title", sha256=sha(out / "SHADOW_title_poster_1080x1920.png"))}


def main():
    n_files, n_png = art_copy()
    sm = FILM / "social-materials"
    titles = end_title(sm / "end-title")
    stills = stills_2x(sm / "stills-2x")
    rec = dict(schema_version=1, status="social_materials_from_approved_film", project_id="DCL-20261021-SHADOW", created_at_local=now(),
               requested_by="Jason 27 Oct: end title animation + approved stills high res for social post material",
               end_title=titles, stills_2x=dict(method="Real-ESRGAN x4plus (local) + Lanczos 70/30, output 2x of native", files=stills),
               approved_art_exact_copy="../approved-art-v10 (see ../ARTWORK_DELIVERY_v10.json)",
               notes="Derived from approved material; no new generation, no new approval implied. Posting is Jason's decision.",
               publication_authorized=False)
    (sm / "SOCIAL_MATERIALS.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("art files", n_files, "pngs", n_png, "| stills 2x", len(stills), "| title files", len(titles))


if __name__ == "__main__":
    main()

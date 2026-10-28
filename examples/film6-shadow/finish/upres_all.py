"""Finish pass 1: local Real-ESRGAN upscale of every LOCAL cut in the locked v08 EDL (FINISHING_PLAN.md).

Each cut is upscaled from its ORIGINAL 480p draft take (never from the assembled picture), used range + 12-frame handles,
to 1080x1920 FFV1 via tools/upres_shot.py. HD cuts (T01 / T17b and their lip-synced versions) and the H3 title are skipped.
Resumable: finished outputs are kept. Usage: python -I finish/upres_all.py
"""
import json, pathlib, subprocess, sys

TEST = pathlib.Path(__file__).resolve().parents[1]
LAB = TEST.parents[1]
OUT = TEST / "finish/up"
SKIP = {"T01", "T01ls", "T17b", "T17bls", "TITLE_H3"}
FPS = 24


def main():
    takes = json.loads((TEST / "DRAFT_JOBS.json").read_text(encoding="utf-8"))["takes"]
    rows = json.loads((TEST / "DRAFT_EDIT_v08_EDL.json").read_text(encoding="utf-8"))["rows"]
    OUT.mkdir(parents=True, exist_ok=True)
    for r in rows:
        if r["take"] in SKIP:
            continue
        dst = OUT / f"{r['take']}_{r['label']}_1080x1920.mkv"
        if dst.exists() and pathlib.Path(str(dst) + ".json").exists():
            print("keep", dst.name); continue
        in_f = round(r["src_in"] * FPS)
        n_f = round(r["src_out"] * FPS) - in_f
        src = TEST / takes[r["take"]]["result"]
        subprocess.run([sys.executable, "-I", str(LAB / "tools/upres_shot.py"), str(src), str(in_f), str(n_f), str(dst),
                        "--handles", "12", "--size", "1080x1920"], check=True)
        print("done", dst.name, flush=True)
    print("ALL DONE")


if __name__ == "__main__":
    main()

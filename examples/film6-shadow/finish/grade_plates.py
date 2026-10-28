"""Finish pass 2: grade every photographic plate once, before overlays (colour-grade skill: grade the pre-grade picture,
grain once, last). Preset E1N = TEST-010 E1 with a night lift chosen on the 27 Oct still board (faces 42-44 %,
speculars ~95 %, blacks 2-3 %). POV plates (scan, lock, whip, decoy) keep their optic grade instead; the H3 title keeps
its approved look. Usage: python -I finish/grade_plates.py <in.mkv|mp4> [<in> ...]   -> finish/graded/<stem>.mkv
"""
import pathlib, subprocess, sys
import numpy as np, cv2

TEST = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TEST.parent / "TEST-010/work"))
import look   # noqa: E402

FF = TEST.parent / "TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
E1N = dict(look.PRESETS["E1"], ev=0.1, wp=1.15, gam=0.80, blk=0.03, vig=0.15, grain=1.0)   # grain 3.2 -> 1.0: Jason 27 Oct "too much"
OUT = TEST / "finish/graded"


def grade_file(src):
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / (pathlib.Path(src).stem + ".mkv")
    cap = cv2.VideoCapture(str(src)); W, H, fps = int(cap.get(3)), int(cap.get(4)), cap.get(5)
    o = subprocess.Popen([str(FF), "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps:g}",
                          "-i", "-", "-c:v", "ffv1", str(dst)], stdin=subprocess.PIPE)
    rng, n = np.random.default_rng(7), 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        o.stdin.write(look.grade(f, E1N, rng).tobytes()); n += 1
    o.stdin.close(); o.wait()
    print("graded", dst.name, n, "frames", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--grain"]:   # comparison grades, e.g. --grain 0 -> finish/graded_g0
        E1N["grain"] = float(args[1]); OUT = TEST / f"finish/graded_g{args[1]}"; args = args[2:]
    for s in args:
        grade_file(s)

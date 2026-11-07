"""Every-frame check of a 1080p composite against its accepted 480p version.
For the frames used in the cut: a sheet of [accepted 480p | 1080p] crops of the effect region, every frame, labelled,
plus per-frame structure correlation of the two (downscaled to 480p) inside the region; a pop or ghost shows as a dip.
usage: python -I every_frame.py NAME BOX(x0,y0,x1,y1 fractions) FIRST LAST [--cols 6]
  NAME e.g. P01-comp_v5 -> cuts/NAME_480p.mp4 and cuts/1080/NAME_1080p.mp4
"""
import argparse, subprocess
from pathlib import Path
import numpy as np, cv2

FIN = Path(__file__).resolve().parent; PROD = FIN.parent
FF = str(PROD.parents[1] / "TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe")


def frames(p, w, h):
    b = subprocess.run([FF, "-v", "error", "-i", str(p), "-fps_mode", "passthrough", "-vf", f"scale={w}:{h}:flags=area",
                        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, h, w, 3)


ap = argparse.ArgumentParser()
ap.add_argument("name"); ap.add_argument("box"); ap.add_argument("first", type=int); ap.add_argument("last", type=int)
ap.add_argument("--cols", type=int, default=4); ap.add_argument("--tile", type=int, default=440)
a = ap.parse_args()
x0, y0, x1, y1 = map(float, a.box.split(","))
lo = frames(PROD / f"cuts/{a.name}_480p.mp4", 1920, 1080)
hi = frames(PROD / f"cuts/1080/{a.name}_1080p.mp4", 1920, 1080)
X0, Y0, X1, Y1 = int(x0 * 1920), int(y0 * 1080), int(x1 * 1920), int(y1 * 1080)
tiles, cors = [], []
for i in range(a.first, a.last + 1):
    A, B = lo[i][Y0:Y1, X0:X1], hi[i][Y0:Y1, X0:X1]
    ga, gb = [cv2.resize(cv2.cvtColor(x, cv2.COLOR_BGR2GRAY), None, fx=0.444, fy=0.444, interpolation=cv2.INTER_AREA).astype(np.float32) for x in (A, B)]
    ga, gb = ga - ga.mean(), gb - gb.mean()
    cors.append(float((ga * gb).sum() / np.sqrt((ga * ga).sum() * (gb * gb).sum() + 1e-6)))
    t = np.hstack([A, B]); s = a.tile / t.shape[1]
    t = cv2.resize(t, (a.tile, int(t.shape[0] * s)), interpolation=cv2.INTER_AREA)
    cv2.putText(t, f"f{i} {i/24:.2f}s", (4, 14), 0, 0.4, (0, 255, 255), 1)
    tiles.append(t)
while len(tiles) % a.cols:
    tiles.append(np.zeros_like(tiles[0]))
sheet = np.vstack([np.hstack(tiles[r:r + a.cols]) for r in range(0, len(tiles), a.cols)])
out = FIN / f"every_frame_{a.name}.jpg"
cv2.imwrite(str(out), sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
c = np.array(cors); d = np.abs(np.diff(c))
print(a.name, "frames", a.first, "-", a.last, "corr mean %.3f min %.3f (f%d)  max step %.3f (f%d)" % (c.mean(), c.min(), a.first + c.argmin(), d.max(), a.first + 1 + d.argmax()), "sheet", out.name, sheet.shape[:2])

"""5C: 9:16 shot 4 = reframe of the APPROVED 16:9 shot 4 (Jason 6 Nov: "since 16x9 is approve why not use the same image but reframe for 9:16").
Source: SeedVR2 of the 04H draft at 1620 short side (2880x1620, skip 21) -> same take frames as 16:9 shot 4 (24-85) -> src 3-64.
Grade: the 16:9 shot 4 transform (gain/offset per channel, identical look to the approved 16:9). Crop 911x1620 centred on her face,
lanczos to 1080x1920 (x1.185). Writes shots/V/04.mkv (62 frames, FFV1). Bundled ffmpeg decode only.
usage: python build_04V_reframe.py [cx]   (cx = crop centre x in 2880 px, default 1736)"""
import sys, subprocess, numpy as np
from pathlib import Path
FF = r"<LAB>\experiments\TEST-001\tools\python-media\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
HERE = Path(__file__).parent; SRC = HERE.parent / "p5_finish/seedvr2_faces/04H_1620.mkv"
GAIN = np.array([0.9767, 0.9768, 0.9857], np.float32); OFF = np.array([1.86, 2.61, 1.03], np.float32)   # PICTURE_REPORT shots/H/4
W, H = 2880, 1620; CW = 911; cx = int(sys.argv[1]) if len(sys.argv) > 1 else 1736
x0 = max(0, min(W - CW, cx - CW // 2)); N0, N = 3, 62
raw = subprocess.run([FF, "-v", "error", "-i", str(SRC), "-vf", f"select='between(n\\,{N0}\\,{N0 + N - 1})',crop={CW}:{H}:{x0}:0",
                      "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, CW, 3)[:N].astype(np.float32)
assert len(fr) == N, len(fr)
fr = np.clip(fr * GAIN + OFF, 0, 255).astype(np.uint8)
out = HERE / "shots/V/04.mkv"
p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{CW}x{H}", "-r", "24", "-i", "-",
                      "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "ffv1", "-pix_fmt", "bgr0", str(out)], stdin=subprocess.PIPE)
p.stdin.write(fr.tobytes()); p.stdin.close(); p.wait()
print("BUILT V shot 4 reframe:", N, "frames, crop x0 =", x0, "->", out)

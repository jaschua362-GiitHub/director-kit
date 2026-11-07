"""Delivery checks for the One Beat Late 1080p final.
- stream facts (size, fps, frames, colour tags, audio), every frame decodes
- audio: decoded AAC vs sound/stems/mix_final.wav (alignment, level difference), loudness + true peak (ebur128)
- picture: structure timing vs cuts/SOUND_EDIT_v11_480p.mp4 (build_final_1080.check, faded file)
- approved-file hashes vs HASHES_before.json
usage: python -I verify_final.py FILE
"""
import sys, json, subprocess, hashlib, re
from pathlib import Path
import numpy as np

FIN = Path(__file__).resolve().parent; PROD = FIN.parent
sys.path.insert(0, str(FIN))
f = sys.argv[1]; sys.argv = sys.argv[:1]
import build_final_1080 as B
FF = B.FF
rep = {}
info = subprocess.run([FF, "-hide_banner", "-i", f], capture_output=True, text=True).stderr
rep["streams"] = [l.strip() for l in info.splitlines() if "Stream #" in l or "Duration" in l]
cnt = subprocess.run([FF, "-v", "error", "-i", f, "-map", "0:v", "-fps_mode", "passthrough", "-f", "null", "-", "-stats"], capture_output=True, text=True)
rep["decode_errors"] = cnt.stdout.strip() or None
rep["frames"] = int(re.findall(r"frame=\s*(\d+)", cnt.stderr)[-1])


def pcm(p):
    b = subprocess.run([FF, "-v", "error", "-i", str(p), "-map", "0:a", "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, 2)


a, m = pcm(f), pcm(B.MIX)
n = min(len(a), len(m))
lags = range(-2048, 2049, 1)
seg = slice(48000 * 5, 48000 * 15)
best = max(lags, key=lambda L: float(np.dot(a[seg.start + L: seg.stop + L, 0], m[seg, 0])))
aa = a[max(best, 0): n + min(best, 0)]; mm = m[max(-best, 0): n - max(best, 0)]
k = min(len(aa), len(mm)); aa, mm = aa[:k], mm[:k]
rep["audio"] = {"final_samples": len(a), "mix_samples": len(m), "lag_samples": best,
                "rms_diff_db": round(float(20 * np.log10(np.sqrt(np.mean((aa - mm) ** 2)) / np.sqrt(np.mean(mm ** 2)))), 1),
                "gain_ratio_db": round(float(20 * np.log10(np.sqrt(np.mean(aa ** 2)) / np.sqrt(np.mean(mm ** 2)))), 2)}
for name, p in [("final", f), ("mix_final.wav", B.MIX)]:
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(p), "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]; tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]
    rep["audio"][f"{name}_LUFS"] = float(I); rep["audio"][f"{name}_truepeak_dBTP"] = float(tp)
B.check(f, faded=True)
t = json.loads((FIN / f"timing_check_{Path(f).stem}.json").read_text())
rep["timing"] = {"events": [(e["panel"], e["corr_mean"], e["frames_better_shifted"]) for e in t["events"]],
                 "shifted_frames": [r for r in t["per_frame"] if r[2] != 0 and r[3] - r[1] > 0.02]}
before = json.loads((FIN / "HASHES_before.json").read_text())
changed = [k for k, h in before.items() if hashlib.sha256((PROD / k).read_bytes()).hexdigest() != h]
rep["approved_files_changed"] = changed
Path(f).with_suffix(".verify.json").write_text(json.dumps(rep, indent=1))
print(json.dumps({k: v for k, v in rep.items() if k != "timing"}, indent=1))
print("timing shifted frames:", rep["timing"]["shifted_frames"])

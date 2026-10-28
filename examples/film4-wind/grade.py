"""Shot colour unification + film grain (TEST-009 finish).
For each shot: partial Reinhard LAB transfer toward a reference frame (warm ending look), strength per shot,
then gentle filmic contrast + luminance grain. Output FFV1 intermediates in work/graded/.
usage: python -I work/grade.py <ref_png> <in.mp4> <out.mkv> <strength 0-1> [grain=3.0]
"""
import sys, subprocess, numpy as np, cv2
ref, src, out, k = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
grain = float(sys.argv[5]) if len(sys.argv) > 5 else 3.0
W, H = 1280, 720
def stats(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    return lab.reshape(-1, 3).mean(0), lab.reshape(-1, 3).std(0) + 1e-3
r = cv2.resize(cv2.imread(ref), (W, H)); rm, rs = stats(r)
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}',
                      '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
frames = []
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    frames.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
# shot-level statistics (median over sampled frames) so the grade is stable, no flicker
sm = np.median([stats(f)[0] for f in frames[::6]], 0); ss = np.median([stats(f)[1] for f in frames[::6]], 0)
gain = 1 + k * (rs / ss - 1); gain[0] = 1 + 0.5 * k * (rs[0] / ss[0] - 1)   # L contrast moved at half strength
shift = k * (rm - sm)
rng = np.random.default_rng(9)
o = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                      '-c:v', 'ffv1', out], stdin=subprocess.PIPE)
for f in frames:
    lab = cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32)
    lab = (lab - sm) * gain + sm + shift
    g = cv2.GaussianBlur(rng.normal(0, grain, (H, W)).astype(np.float32), (0, 0), 0.6)
    lab[..., 0] += g
    o.stdin.write(cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).tobytes())
o.stdin.close(); o.wait(); print(out, len(frames), 'frames', 'shift', shift.round(1), 'gain', gain.round(2))

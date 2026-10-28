"""Local Wan2.1 VACE-1.3B outpainting of the 9:16 bands for the extend shots (S3, S4, S14, S7) — free, RTX 3080 10 GB.
Run with the Wan venv:  F:/ai-tools/wan-venv/Scripts/python.exe work/vace_fill.py <shot_id> [--steps 40]
Input : work/vert/crop/%04d.png (the w x 1080 centre of each frame, exact approved pixels) + edits/vertical_plan_v02.json
Model : 480x832 canvas = centre (known) + top/bottom bands (mask=1, generated). Frame count padded to 4n+1 by
        repeating the last frame. Optional identity reference (S7: C04) is passed as a VACE reference image.
Output: work/vert/vace/<shot>/%04d.png (480x832, frame-aligned to the shot); the main pipeline uses ONLY the bands from
        these and keeps the original ESRGAN centre."""
import sys, os, json, math, random
from pathlib import Path
import numpy as np, torch, torch.nn.functional as F, cv2
from PIL import Image
WAN = Path('F:/ai-tools/Wan2.1'); sys.path.insert(0, str(WAN))
import wan
from wan.configs import WAN_CONFIGS
ROOT = Path(__file__).resolve().parent
PLAN = {s['id']: s for s in json.load(open(ROOT.parent / 'edits/vertical_plan_v02.json', encoding='utf-8'))['shots']}
sid = sys.argv[1]; steps = int(sys.argv[sys.argv.index('--steps') + 1]) if '--steps' in sys.argv else 40
s = PLAN[sid]; a, b = s['f']; n = b - a + 1; F_ = 4 * math.ceil((n - 1) / 4) + 1
CW, CH = 480, 832
PROMPTS = {
 'S3': "Cinematic photoreal close-up at floor level in a dark steel-and-bronze temple hall: two engraved bronze and steel mechanical armoured feet locked in heavy bolted clamps on a steel floor rail, a maroon coarse silk sash and segmented armoured shins above, a wet dark stone and iron floor with puddle reflections below, warm window light and haze, film grain.",
 'S4': "Cinematic photoreal action wide in a hazy steel-and-bronze Chinese temple hall with tall lattice windows and warm daylight shafts: a giant engraved studded iron hammer on a straight steel pendulum arm hanging from the dark bracketed ceiling slams into an armoured warrior bracing on a floor rail, sparks and water spray, dark wet reflective floor below, film grain.",
 'S14': "Cinematic photoreal over-the-shoulder shot in a dark hazy bronze temple hall: a giant engraved studded iron hammer on a straight steel arm from the ceiling rushing toward an armoured warrior with a braided topknot, water droplets frozen in the air, dark ceiling beams above, wet floor below, high-speed slow motion, film grain.",
 'S7': "Cinematic photoreal extreme close-up of a Chinese man about 38: weathered skin with pores and light sweat, dark brown eyes, black eyebrows, loose strands of black hair across the forehead, a small faceted glowing glass gem set in the centre of his forehead with fine red line marks, straight nose, short black moustache and goatee, warm window light, film grain.",
}
REF = {'S7': str(ROOT.parents[2] / 'approved/DCL-20261015-WIND/v02/images/C04-Ren-frontal-gem-master.png')}
NEG = "blurry, cartoon, CG render, smooth plastic skin, text, watermark, deformed, extra eyes, duplicated face, mirrored, frame border, black bars"

o = s['option_B']; w = o['w'][0]; h = w * 16 / 9
cy0 = (h - 1080) / 2 / h                                   # fraction of canvas height above the centre band
y0 = int(round(cy0 * CH)); y1 = CH - y0
frames, masks = [], []
for k in range(F_):
    i = a + min(k, n - 1)
    c = cv2.cvtColor(cv2.imread(str(ROOT / f'vert/crop/{i:04d}.png')), cv2.COLOR_BGR2RGB)
    canvas = np.full((CH, CW, 3), 127, np.uint8); canvas[y0:y1] = cv2.resize(c, (CW, y1 - y0), interpolation=cv2.INTER_AREA)
    m = np.ones((CH, CW), np.float32); m[y0 + 4:y1 - 4] = 0  # 4 px overlap into the known band for a cleaner seam
    frames.append(canvas); masks.append(m)
vid = torch.from_numpy(np.stack(frames)).permute(3, 0, 1, 2).float().div(127.5).sub(1)   # [3,F,H,W] in [-1,1]
msk = torch.from_numpy(np.stack(masks))[None]                                             # [1,F,H,W] in [0,1]
dev = torch.device('cuda:0')
cfg = WAN_CONFIGS['vace-1.3B']
pipe = wan.WanVace(config=cfg, checkpoint_dir='F:/ai-models/Wan2.1-VACE-1.3B', device_id=0, rank=0, t5_cpu=True)
pipe.vid_proc.set_area(CW * CH); pipe.vid_proc.set_seq_len(32760)
pipe.model.to(torch.bfloat16)   # 10 GB card: fp32 weights (7.1 GB) spill into shared memory; inference autocasts to bf16 anyway
torch.cuda.empty_cache()
refs = [None]
if sid in REF:
    r = torch.from_numpy(np.array(Image.open(REF[sid]).convert('RGB'))).permute(2, 0, 1).float().div(127.5).sub(1)
    sc = min(CH / r.shape[1], CW / r.shape[2]); nh, nw = int(r.shape[1] * sc), int(r.shape[2] * sc)
    r = F.interpolate(r[None], size=(nh, nw), mode='bilinear', align_corners=False)[0]
    can = torch.ones(3, 1, CH, CW); t, l = (CH - nh) // 2, (CW - nw) // 2; can[:, 0, t:t + nh, l:l + nw] = r
    refs = [[can.to(dev)]]
video = pipe.generate(PROMPTS[sid], [vid.to(dev)], [msk.to(dev)], refs, size=(CW, CH), frame_num=F_, shift=16,
                      sample_solver='unipc', sampling_steps=steps, guide_scale=5.0, n_prompt=NEG, seed=2026, offload_model=True)
out = ROOT / f'vert/vace/{sid}'; out.mkdir(parents=True, exist_ok=True)
v = ((video.clamp(-1, 1) + 1) * 127.5).byte().permute(1, 2, 3, 0).cpu().numpy()   # [F,H,W,3]
for k in range(n): cv2.imwrite(str(out / f'{a + k:04d}.png'), cv2.cvtColor(v[k], cv2.COLOR_RGB2BGR))
json.dump({'shot': sid, 'frames': [a, b], 'frame_num': F_, 'steps': steps, 'size': [CW, CH], 'band_rows': [y0, y1], 'w': w,
           'prompt': PROMPTS[sid], 'ref': REF.get(sid), 'seed': 2026, 'shift': 16, 'guide': 5.0}, open(out / 'settings.json', 'w'), indent=1)
print('ok', sid, n, 'frames ->', out)

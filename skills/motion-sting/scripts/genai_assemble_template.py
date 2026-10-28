"""TEMPLATE - AI-generated live-action promo edit (see references/genai-live-action.md).

Copied from the coffee-brand brand-model promo v11 (<PROJECTS>/<Brand>/Motion/brand-model-promo-10s/assemble_v5.py).
To reuse: copy into the project root, put clips in shots/, foley in audio/, then edit STING, SHOTS (beat-length
durations from audio/beats.py), CUP/DISC (measured), TOTAL. Special-cased clip names (W1 grinder push, W2
foreground-blur mask, V6c match-cut push) are examples - rename or generalise per project.
Usage: python genai_assemble_template.py <version> <music file>
"""
"""v5 (15 s): grind -> frontal brew -> drip close-up -> swirl & present -> overhead cup -> logo sting tail.

Clips from ChatCut (Seedance 2.0 / 2.5). Live grade: deband, espresso-brown floor, light temporal grain
(real-camera texture). Match cut: overhead cup (V6) pushes in onto the sting's disc (sting source 5.2 s);
the sting opens scaled to the cup and eases back. Audio: music M1 + foley + sting audio, -14 LUFS.
Usage: python assemble_v5.py [version] [music.wav]
"""
import subprocess, sys, os, re

V = sys.argv[1] if len(sys.argv) > 1 else 'v5'
MUSIC = sys.argv[2] if len(sys.argv) > 2 else None
ROOT = os.path.dirname(os.path.abspath(__file__))
STING = r'<PROJECTS>\<Brand>\Motion\logo-sting-8s\Brand_LogoSting_10s_v5_1080x1920_60fps_sound.mp4'
FPS, TOTAL = 60, 15.0   # v11: 60 fps so the sting keeps its native motion
# cut on the music's beats (beats.py on M1: 95.9 BPM; cuts 2.323, 5.459, 7.975, 11.089, match 11.723 = downbeat)
# (clip, in, dur[, z0, z1, ax, ay]) -- optional push/punch: zoom z0->z1 anchored at pixel (ax, ay)
SHOTS = [('W4c', 0.30, 1.077, 2.00, 2.10, 0, 1700),  # cold open: amber coffee swirling in the server (macro punch)
         ('W1', 1.40, 1.246),                          # grinder (special: push down-left, face out)
         ('W2', 2.70, 1.245, 1.36, 1.42, 540, 0),       # frontal brew, punched from the top: flat bag below frame
         ('W3', 0.80, 1.909, 1.15, 1.18, 0, 1920),     # drip, wide-ish, punched bottom-left (face clears)
         ('W3', 2.75, 1.250, 1.80, 1.88, 400, 950),   # macro: stream into the server, scale display out of frame
         ('W4c', 1.40, 1.878, 1.06, 1.08, 540, 1920),   # swirl, lamp cropped
         ('W4b', 3.30, 1.245, 1.20, 1.24, 540, 1920),   # cut-in offer
         ('V6c', 3.00, 0.634)]
XF = 8 / 60
LIVE = sum(sh[2] for sh in SHOTS)
STING_IN, STING_DUR = 5.2, TOTAL - (LIVE - XF)
CUP = (532, 952); DISC = (544, 956); Z0, Z1 = 1.02, 1.10   # V6c: white cup, rim ~605 px
S0 = 605 * Z1 / 665
LIFT = "curves=r='0/0.085 0.5/0.52 1/1':g='0/0.055 0.5/0.5 1/1':b='0/0.04 0.5/0.48 1/1'"
GRAIN = 'noise=c0s=7:c0f=t+u:c1s=2:c1f=t+u:c2s=2:c2f=t+u'

inputs, chains = [], []
for i, sh in enumerate(SHOTS):
    clip, tin, dur = sh[:3]
    PUSH = ''
    FLIP = ',hflip' if len(sh) > 7 and sh[7] == 'flip' else ''
    if len(sh) > 3:
        z0, z1, ax, ay = sh[3:7]
        zz = f'({z0}+({z1}-{z0})*(t/{dur}))'
        PUSH = FLIP + f",scale=w='trunc(1080*{zz}/2)*2':h='trunc(1920*{zz}/2)*2':eval=frame,crop=1080:1920:x='{ax}*({zz}-1)':y='{ay}*({zz}-1)'"
    inputs += ['-i', os.path.join(ROOT, 'shots', clip + '.mp4')]
    pre = (f'[{i}:v]trim=start={tin}:duration={dur + 0.2},setpts=PTS-STARTPTS,fps={FPS},trim=end_frame={round(dur * FPS)},'
           f'deband=1thr=0.015:2thr=0.015:3thr=0.015:range=20:blur=1,{LIFT}')
    if clip == 'V6c':
        z = f'({Z0}+({Z1}-{Z0})*pow(t/{dur},2))'
        b = 1.0
        chains.append(f"{pre},scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame,"
                      f"crop=1080:1920:x='{CUP[0] * b}*{z}-{DISC[0]}':y='{CUP[1] * b}*{z}-{DISC[1]}',"
                      f"{GRAIN},setsar=1,format=yuv420p[s{i}]")
    elif clip == 'W1':
        # hook: 8% push toward the grinder chute
        z = f'(1.20+0.08*(t/{dur}))'
        chains.append(f"{pre},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                      f"scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame,crop=1080:1920:x='200*({z}-1)':y='1500*({z}-1)',"
                      f"{GRAIN},setsar=1,format=yuv420p[s{i}]")
    elif clip == 'W2':
        # foreground depth of field: the near bags (AI-garbled label text) fall out of focus
        m = "255*clip(max((Y-1540)/140,(230-X)/70*between(Y,1240,1720)),0,1)"
        chains.append(f"{pre},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920{PUSH},split[f{i}a][f{i}b];"
                      f"[f{i}b]gblur=sigma=7,format=yuva444p,geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='{m}'[f{i}c];"
                      f"[f{i}a][f{i}c]overlay,{GRAIN},setsar=1,format=yuv420p[s{i}]")
    else:
        chains.append(f'{pre},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920{PUSH},{GRAIN},setsar=1,format=yuv420p[s{i}]')
n = len(SHOTS)
inputs += ['-ss', str(STING_IN), '-t', f'{STING_DUR:.4f}', '-i', STING]
inputs += ['-i', os.path.join(ROOT, 'audio', 'foley_v5.wav')]
if MUSIC: inputs += ['-i', MUSIC]
# v11: the sting plays untouched at its native 60 fps -- the old per-frame push (rounded to 2 px) made the forming wordmark jitter
chains.append(f"[{n}:v]fps={FPS},settb=1/{FPS},setpts=N,setsar=1,format=yuv420p[st]")
chains.append(''.join(f'[s{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0,settb=1/{FPS},setpts=N[live]')
chains.append(f'[live][st]xfade=transition=fade:duration={XF:.4f}:offset={LIVE - XF:.4f},trim=duration={TOTAL},format=yuv420p[vout]')
delay = int((LIVE - XF) * 1000)
chains.append(f'[{n + 1}:a]aresample=48000,volume=-4dB[fol]')
chains.append(f'[{n}:a]afade=t=in:d=0.08,adelay={delay}|{delay},aresample=48000,volume=-7dB[stA]')
if MUSIC:
    chains.append(f'[{n + 2}:a]aresample=48000,atrim=0:{TOTAL},afade=t=in:d=0.15,afade=t=out:st=14.25:d=0.75,volume=2dB[mus]')
    chains.append(f'[mus][fol][stA]amix=inputs=3:normalize=0,atrim=0:{TOTAL}[aout]')
else:
    chains.append(f'[fol][stA]amix=inputs=2:normalize=0,atrim=0:{TOTAL}[aout]')

tmp = os.path.join(ROOT, f'_tmp_{V}.mov')
out = os.path.join(ROOT, f'Brand_BrandModel_Promo_15s_{V}_1080x1920_60fps_sound.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(chains),
                '-map', '[vout]', '-map', '[aout]', '-r', str(FPS),
                '-c:v', 'libopenh264', '-b:v', '30M', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', tmp], check=True)

def lufs(path, af=''):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', (af + ',' if af else '') + 'ebur128=peak=true',
                        '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)[-1])

LIM = f'alimiter=limit={10 ** (-3.2 / 20):.4f}:attack=1:release=60:level=disabled'
I, _ = lufs(tmp); g = -14.0 - I
I2, _ = lufs(tmp, f'volume={g:.2f}dB,{LIM}')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-c:v', 'copy', '-af', f'volume={g + (-14.0 - I2):.2f}dB,{LIM}',
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', out], check=True)
os.remove(tmp)
print('wrote', out, 'final (LUFS, TP) =', lufs(out))

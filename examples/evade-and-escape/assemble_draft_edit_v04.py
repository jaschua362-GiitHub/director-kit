"""TEST-018 draft edit v04: A (D01-A) + B rebuilt as three single-action shots (D03-B1, D03-BINS, D03-B3) + C (D02-C) + existing Shadow end tag.
D02-B discarded (Kaede turned into a robot three times). 480p upscaled for review; no grade, no score."""
import subprocess, json, pathlib, hashlib
HERE = pathlib.Path(__file__).parent
FF = str(HERE.parent.parent/'TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe')
TAG = HERE.parent.parent/'TEST-017-aiko-fight/references/SHADOW-existing-end-tag-1080x1920.mp4'
OUT = HERE/'TEST018_draft_edit_v04_1080x1920.mp4'
dur = lambda p: float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]).decode())
SRC = [HERE/'d01/D01-A_0acf7754.mp4', HERE/'d03/D03-B1_3805e5f0.mp4', HERE/'d03/D03-BINS_d45ae5b6.mp4', HERE/'d03/D03-B3_564cc9df.mp4', HERE/'d02/D02-C_9a7dd774.mp4']
# (input, in, out): B1 landing -> block -> drone strobe; INS wrist press -> wave -> she darts off; B3 unseen kick -> cut -> decloak running
PIECES = [(0, 0, dur(SRC[0])), (1, 0.25, 3.25), (2, 0.6, 4.85), (3, 0, 5.6), (4, 0, dur(SRC[4]))]
fc, lab = [], ''
for k, (i, s, e) in enumerate(PIECES):
    fc.append(f'[{i}:v]trim=start={s}:end={e},setpts=PTS-STARTPTS,fps=24,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p[v{k}]')
    fc.append(f'[{i}:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{e - s:.4f}[a{k}]')
    lab += f'[v{k}][a{k}]'
n = len(PIECES)
fc.append(f'[{n}:v]fps=24,scale=1080:1920,setsar=1,format=yuv420p[vt]')
fc.append(f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo[at]')
fc.append(lab + f'[vt][at]concat=n={n + 1}:v=1:a=1[v][araw]')
fc.append('[araw]loudnorm=I=-16:TP=-1.5:LRA=11[a]')
cmd = [FF, '-v', 'error', '-y'] + sum((['-i', str(p)] for p in SRC + [TAG]), []) + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
       '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(OUT)]
subprocess.run(cmd, check=True)
names = ['D01-A', 'D03-B1', 'D03-BINS', 'D03-B3', 'D02-C']
t = 0; plist = []
for k, (i, s, e) in enumerate(PIECES):
    plist.append({'src': names[k], 'in': s, 'out': round(e, 3), 'edit_in': round(t, 3)}); t += e - s
info = {'file': OUT.name, 'duration_s': round(dur(OUT), 3), 'story_s': round(t, 3), 'pieces': plist,
        'tag': 'TEST-017/references/SHADOW-existing-end-tag-1080x1920.mp4', 'sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'note': 'Review copy: 480p drafts upscaled (lanczos), no grade, no score, native audio loudnorm -16 LUFS.'}
(HERE/'DRAFT_EDIT_v04.json').write_text(json.dumps(info, indent=1))
print(info)

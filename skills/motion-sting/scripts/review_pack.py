"""Evidence pack for the independent critic: measured from the delivered MP4, never from the live page.

    python review_pack.py <film.mp4> [--out <dir>] [--strips 3.4 6.1] [--auto-strips 3] [--loop]

Writes into <out> (default: <film dir>/review/<film name>/):
    contact.png   2 frames/s, timestamped                 -> pacing, variety, composition, hook
    phone.png     1 frame/s at 360 px wide (phone feed)   -> readability, line weight, type size
    strip_<t>.png 12 consecutive native frames around t   -> pops, overlaps, smear, one-frame glitches
                  (--strips times, plus the N fastest moments found by frame difference)
    report.md     frozen stretches, motion curve, loop seam, loudness/true peak

Only ffmpeg + numpy + pillow. Print output is ASCII (non-UTF-8 console code pages).
"""
import argparse, json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

FROZEN_DIFF = 0.35      # mean abs luma change (0-255) over 0.1 s below which a moment counts as near-still
                        # (same threshold + interval as business-motion-film/scripts/frozen-time.sh)
FROZEN_MIN = 0.5        # seconds; shorter still moments are holds, not freezes


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate',
                        '-show_entries', 'format=duration', '-of', 'json', path], capture_output=True, text=True)
    if r.returncode: sys.exit('ffprobe failed: ' + r.stderr)
    j = json.loads(r.stdout)
    v = next(s for s in j['streams'] if s['codec_type'] == 'video')
    n, d = map(int, v['r_frame_rate'].split('/'))
    return dict(w=v['width'], h=v['height'], fps=n / d, dur=float(j['format']['duration']),
                audio=any(s['codec_type'] == 'audio' for s in j['streams']))


def grab(path, width, height, fps=None, ss=None, frames=None, gray=False):
    vf = ([f'fps={fps}'] if fps else []) + [f'scale={width}:{height}:flags=area', 'format=' + ('gray' if gray else 'rgb24')]
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', f'{ss:.4f}'] if ss is not None else []) + ['-i', path]
    cmd += (['-frames:v', str(frames)] if frames else []) + ['-vf', ','.join(vf), '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    c = 1 if gray else 3
    a = np.frombuffer(raw, np.uint8)
    return a[: a.size // (width * height * c) * width * height * c].reshape(-1, height, width, c)


def sheet(frames, labels, cols, out, pad=4):
    n, h, w, _ = frames.shape
    rows = -(-n // cols)
    img = Image.new('RGB', (cols * (w + pad) + pad, rows * (h + pad) + pad), (40, 40, 40))
    d = ImageDraw.Draw(img)
    for i, (f, lab) in enumerate(zip(frames, labels)):
        x, y = pad + (i % cols) * (w + pad), pad + (i // cols) * (h + pad)
        img.paste(Image.fromarray(f), (x, y))
        d.rectangle([x, y, x + 7 * len(lab) + 6, y + 14], fill=(0, 0, 0))
        d.text((x + 3, y + 2), lab, fill=(255, 0, 255))
    img.save(out)


def runs(mask, dt):
    out, start = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and start is None: start = i
        if not m and start is not None:
            if (i - start) * dt >= FROZEN_MIN: out.append((start * dt, i * dt))
            start = None
    return out


def loudness(path):
    r = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', path, '-vn', '-af', 'ebur128=peak=true',
                        '-f', 'null', '-'], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind('Summary:'):]
    g = lambda k: (re.search(k + r':\s*(-?[\d.]+|-inf)', tail) or [None, 'n/a'])[1]
    return dict(I=g('I'), LRA=g('LRA'), peak=g('Peak'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('film')
    ap.add_argument('--out')
    ap.add_argument('--strips', type=float, nargs='*', default=[], help='times (s) to inspect frame by frame')
    ap.add_argument('--auto-strips', type=int, default=3, help='also strip the N fastest moments')
    ap.add_argument('--loop', action='store_true', help='film should loop: measure the last->first seam')
    a = ap.parse_args()
    film = os.path.abspath(a.film)
    name = os.path.splitext(os.path.basename(film))[0]
    out = os.path.abspath(a.out or os.path.join(os.path.dirname(film), 'review', name))
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):                     # stale strips from an earlier render of the same name mislead the critic
        if f.startswith('strip_') and f.endswith('.png'): os.remove(os.path.join(out, f))
    m = probe(film)
    portrait = m['h'] > m['w']
    even = lambda x: int(x) // 2 * 2

    # motion curve at 30 fps, small and grey
    aw = 320; ah = even(aw * m['h'] / m['w'])
    g = grab(film, aw, ah, fps=30, gray=True)[..., 0].astype(np.int16)
    diff = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))           # diff[i] = change from frame i to i+1
    d01 = np.abs(g[3:] - g[:-3]).mean(axis=(1, 2))                # change over 0.1 s
    frozen = runs(d01 < FROZEN_DIFF, 1 / 30)
    frozen_s = sum(b - a_ for a_, b in frozen)

    # contact sheet: 2 fps
    cw = 270 if portrait else 320; chh = even(cw * m['h'] / m['w'])
    c = grab(film, cw, chh, fps=2)
    sheet(c, [f'{i / 2:.1f}s' for i in range(len(c))], 10 if portrait else 6, os.path.join(out, 'contact.png'))

    # phone: 1 fps at 360 px wide (a 16:9 film in a portrait feed is also 360 wide)
    pw = 360; ph = even(pw * m['h'] / m['w'])
    p = grab(film, pw, ph, fps=1)
    sheet(p, [f'{i}s' for i in range(len(p))], 5, os.path.join(out, 'phone.png'))

    # strips: requested + fastest moments (peaks of the motion curve, >= 1 s apart)
    times = list(a.strips)
    order = np.argsort(diff)[::-1]
    for i in order:
        if len(times) >= len(a.strips) + a.auto_strips: break
        t = (i + 1) / 30
        if all(abs(t - u) >= 1 for u in times): times.append(round(t, 2))
    sw = 360 if portrait else 480; sh = even(sw * m['h'] / m['w'])
    strip_files = []
    for t in times:
        t0 = max(0.0, t - 6 / m['fps'])
        s = grab(film, sw, sh, ss=t0, frames=12)
        f = os.path.join(out, f'strip_{t:05.2f}s.png'.replace('.', '_', 1))
        sheet(s, [f'{t0 + k / m["fps"]:.3f}' for k in range(len(s))], 6, f)
        strip_files.append((t, os.path.basename(f)))

    seam = None
    if a.loop:
        first = grab(film, aw, ah, frames=1, gray=True)[0, ..., 0].astype(np.int16)
        seam = float(np.abs(g[-1] - first).mean())

    loud = loudness(film) if m['audio'] else None

    # motion curve per second (mean diff), for pacing at a glance
    per_s = [float(diff[int(s * 30): int((s + 1) * 30)].mean()) for s in range(int(np.ceil(len(diff) / 30)))]
    lines = [f'# Review pack: {name}', '',
             f'{m["w"]}x{m["h"]} @ {m["fps"]:.2f} fps, {m["dur"]:.2f} s, audio: {"yes" if m["audio"] else "no"}', '',
             '| file | use |', '|---|---|',
             '| contact.png | pacing, variety, composition, hook (2 fps, timestamped) |',
             '| phone.png | readability at 360 px wide (1 fps) |']
    lines += [f'| {f} | 12 native frames around {t:.2f}s |' for t, f in strip_files]
    lines += ['', '## Measurements', '',
              f'- Near-still (change < {FROZEN_DIFF} per 0.1 s for >= {FROZEN_MIN}s; a deliberate slow hold can land here, judge it): **{frozen_s:.2f}s of {m["dur"]:.1f}s**'
              + (': ' + ', '.join(f'{a_:.1f}-{b:.1f}s' for a_, b in frozen) if frozen else ''),
              '- Motion per second (mean luma change, 0-255): ' + ' '.join(f'{v:.1f}' for v in per_s),
              f'- Fastest moments: ' + ', '.join(f'{t:.2f}s' for t, _ in strip_files[len(a.strips):])]
    if seam is not None:
        lines.append(f'- Loop seam (last vs first frame, mean luma diff): **{seam:.2f}** (typical frame-to-frame: {np.median(diff):.2f})')
    if loud:
        lines.append(f'- Loudness: integrated **{loud["I"]} LUFS** (target -14), LRA {loud["LRA"]} LU, true peak **{loud["peak"]} dBFS** (target <= -1.5)')
    open(os.path.join(out, 'report.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'[review] {out}')
    print(f'[review] frozen {frozen_s:.2f}s, strips at {", ".join(f"{t:.2f}" for t, _ in strip_files)}'
          + (f', {loud["I"]} LUFS, peak {loud["peak"]}' if loud else ''))


if __name__ == '__main__':
    main()

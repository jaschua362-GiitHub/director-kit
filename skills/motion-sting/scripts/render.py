"""One-command export: frames (headless Chrome) → MP4 60/30 fps (+ ProRes) (+ audio).

    python render.py --project "F:/path/to/project" --name Brand_Sting_10s_v1 --fmt 16x9 9x16 --dur 10 \
                     [--audio audio/sfx.wav] [--prores] [--fps 60] [--sub 4] [--shutter .5] [--keep-frames]

Why this exists (lessons from the coffee-brand sting):
  * The Claude preview pane throttles when hidden (~5 s/frame). Headless Chrome with background
    throttling disabled runs ~7–10 frames/s.
  * The page renders deterministically: ?export=1 steps every frame and POSTs PNGs to server.js.
  * libx264 is often missing from Windows ffmpeg builds and old NVENC drivers fail; encoders are
    probed and the best available H.264 path is used (libx264 → libopenh264 @30 Mb/s).
  * Chrome is killed by process tree afterwards so no headless instances linger.
  * Motion blur (--sub N): the page averages N sub-frames per frame over the shutter (.5 = 180 deg) before
    posting the PNG. ~N x slower. Use --sub 1 for quick drafts, the default 4 for anything delivered.
"""
import argparse, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request, glob, platform

FORMATS = {'16x9': (1920, 1080), '9x16': (1080, 1920), '1x1': (1080, 1080), '4x5': (1080, 1350)}
CHROMES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'google-chrome', 'chromium', 'chromium-browser',
]


def log(*a): print('[render]', *a, flush=True)


def up(port):
    try:
        urllib.request.urlopen(f'http://localhost:{port}/', timeout=2); return True
    except Exception:
        return False


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0)); return s.getsockname()[1]


def find_chrome():
    for c in CHROMES:
        if os.path.isabs(c) and os.path.exists(c): return c
        if not os.path.isabs(c) and shutil.which(c): return shutil.which(c)
    sys.exit('No Chrome/Edge found — install Chrome or add its path to CHROMES.')


def kill_tree(p):
    if p.poll() is not None: return
    if platform.system() == 'Windows':
        subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
    else:
        p.kill()


def h264_args(bitrate):
    enc = subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
    if ' libx264 ' in enc:
        return ['-c:v', 'libx264', '-preset', 'slow', '-crf', '14']
    if ' libopenh264 ' in enc:
        return ['-c:v', 'libopenh264', '-b:v', bitrate]
    sys.exit('ffmpeg has no libx264/libopenh264 — install a full ffmpeg build.')


def ff(args):
    r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + args, capture_output=True, text=True)
    if r.returncode: sys.exit('ffmpeg failed:\n' + r.stderr)


def export_frames(project, fmt, total, port, chrome, sub=1, shutter=.5):
    frames = os.path.join(project, 'frames')
    # Windows can leave the previous format's folder pending deletion: reuse it and clear leftovers instead of failing
    shutil.rmtree(frames, ignore_errors=True); os.makedirs(frames, exist_ok=True)
    for f in glob.glob(os.path.join(frames, 'f_*.png')): os.remove(f)
    w, h = FORMATS[fmt]
    prof = tempfile.mkdtemp(prefix='sting-chrome-')
    url = f'http://localhost:{port}/?export=1' + ('' if fmt == '16x9' else f'&fmt={fmt}')
    if sub > 1: url += f'&sub={sub}&shutter={shutter}'
    p = subprocess.Popen([chrome, '--headless=new', f'--user-data-dir={prof}', f'--window-size={w},{h}',
                          '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
                          '--disable-backgrounding-occluded-windows', url],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0, last, last_change = time.time(), -1, time.time()
    try:
        while True:
            n = len(glob.glob(os.path.join(frames, 'f_*.png')))
            if n != last: last, last_change = n, time.time()
            if n >= total: break
            if time.time() - last_change > 60 * max(1, sub): sys.exit(f'Export stalled at {n}/{total} frames ({url}).')
            time.sleep(1)
    finally:
        kill_tree(p); shutil.rmtree(prof, ignore_errors=True)
    log(f'{fmt}: {total} frames x{sub} sub in {time.time() - t0:.0f}s')
    return frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--name', required=True, help='base file name, e.g. Brand_LogoSting_10s_v4')
    ap.add_argument('--fmt', nargs='+', default=['16x9'], choices=list(FORMATS))
    ap.add_argument('--dur', type=float, help='seconds; default = timeline.json dur when the project has one')
    ap.add_argument('--fps', type=int, default=60)
    ap.add_argument('--sub', type=int, default=4, help='motion-blur sub-frames per frame (1 = off, for drafts)')
    ap.add_argument('--shutter', type=float, default=.5, help='shutter as a fraction of the frame interval (.5 = 180 deg)')
    ap.add_argument('--audio')
    ap.add_argument('--prores', action='store_true')
    ap.add_argument('--keep-frames', action='store_true')
    a = ap.parse_args()
    project = os.path.abspath(a.project)
    tlp = os.path.join(project, 'timeline.json')
    if os.path.exists(tlp):                       # data-driven projects: the page exports round(dur * fps) frames
        import json
        tdur = json.load(open(tlp, encoding='utf-8'))['dur']
        if a.dur is not None and abs(a.dur - tdur) > 1 / a.fps: log(f'--dur {a.dur} != timeline dur {tdur}; using the timeline')
        a.dur = tdur
    if a.dur is None: sys.exit('--dur is required (no timeline.json in the project)')
    total = round(a.dur * a.fps)
    audio = os.path.join(project, a.audio) if a.audio and not os.path.isabs(a.audio) else a.audio
    engine_js = ''.join(open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(project, '*.js')))
    if a.sub > 1 and 'renderMB' not in engine_js:
        log('WARNING: this project engine predates motion blur (no renderMB): exporting without it.')
        log('         Copy the motion-blur block + export loop from the template sting.js to enable it.')
        a.sub = 1

    # always our own server on a free port: a server already on 8765 may be serving a different project
    port = free_port()
    server = subprocess.Popen(['node', 'server.js', str(port)], cwd=project,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        if up(port): break
        time.sleep(.2)
    else:
        kill_tree(server); sys.exit('server.js did not start (is node installed? is server.js in the project?)')
    chrome = find_chrome()
    vid = h264_args('30M')
    try:
        for fmt in a.fmt:
            frames = export_frames(project, fmt, total, port, chrome, a.sub, a.shutter)
            w, h = FORMATS[fmt]
            base = os.path.join(project, f'{a.name}_{w}x{h}')
            src = ['-framerate', str(a.fps), '-i', os.path.join(frames, 'f_%04d.png')]
            aud_in = ['-i', audio] if audio else []
            amap = ['-map', '0:v', '-map', '1:a'] if audio else []
            sfx = '_sound' if audio else ''
            ff(src + aud_in + amap + vid + ['-pix_fmt', 'yuv420p'] + (['-c:a', 'aac', '-b:a', '320k', '-shortest'] if audio else [])
               + ['-movflags', '+faststart', f'{base}_{a.fps}fps{sfx}.mp4'])
            if a.fps == 60:
                vid30 = [x if x != '30M' else '24M' for x in vid]
                ff(src + aud_in + amap + ['-vf', 'fps=30'] + vid30 + ['-pix_fmt', 'yuv420p']
                   + (['-c:a', 'aac', '-b:a', '320k', '-shortest'] if audio else []) + ['-movflags', '+faststart', f'{base}_30fps{sfx}.mp4'])
            if a.prores:
                ff(src + aud_in + amap + ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le']
                   + (['-c:a', 'pcm_s24le', '-shortest'] if audio else []) + [f'{base}_{a.fps}fps_ProRes422HQ{sfx}.mov'])
            if not a.keep_frames: shutil.rmtree(frames, ignore_errors=True)
            for f in sorted(glob.glob(base + '_*')):
                d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                                   capture_output=True, text=True).stdout.strip()
                log(f'{os.path.basename(f)}  {d}s  {os.path.getsize(f) / 1e6:.1f} MB')
    finally:
        kill_tree(server)


if __name__ == '__main__':
    main()

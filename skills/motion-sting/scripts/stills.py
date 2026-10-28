"""Exact stills + a labelled contact sheet from headless Chrome (works when the preview pane is hidden).

    python stills.py --project <project> --times 0.6 3.5 9.99 [--fmt 9x16] [--name beats] [--cols 6]

Why: the Claude preview pane throttles when hidden and DEFERS IMAGE DECODING, so TOOLS.sheet() hangs on any
project that draws footage. This starts its own server on a free port, screenshots `?t=<t>&solo=1` (canvas
only, 1:1 pixels) in headless Chrome with throttling off, and writes <project>/stills/<name>_<t>.png plus
<project>/stills/<name>.png (sheet with time labels). Frames are the page's own render(t), not the export's
motion-blurred average.
"""
import argparse, os, shutil, socket, subprocess, sys, tempfile, time, urllib.request
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import FORMATS, find_chrome, kill_tree, free_port, up

ap = argparse.ArgumentParser()
ap.add_argument('--project', required=True)
ap.add_argument('--times', type=float, nargs='+', required=True)
ap.add_argument('--fmt', default='16x9', choices=list(FORMATS))
ap.add_argument('--name', default='sheet')
ap.add_argument('--cols', type=int, default=0)
ap.add_argument('--cell', type=int, default=0, help='sheet cell width in px')
a = ap.parse_args()
proj = os.path.abspath(a.project); out = os.path.join(proj, 'stills'); os.makedirs(out, exist_ok=True)
w, h = FORMATS[a.fmt]
port = free_port()
server = subprocess.Popen(['node', 'server.js', str(port)], cwd=proj, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(50):
    if up(port): break
    time.sleep(.2)
chrome, prof = find_chrome(), tempfile.mkdtemp(prefix='stills-chrome-')
files = []
try:
    for t in a.times:
        f = os.path.join(out, f'{a.name}_{t:06.2f}.png')
        url = f'http://localhost:{port}/?t={t}&solo=1' + ('' if a.fmt == '16x9' else f'&fmt={a.fmt}')
        subprocess.run([chrome, '--headless=new', '--hide-scrollbars', f'--user-data-dir={prof}', f'--window-size={w},{h}',
                        '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
                        '--virtual-time-budget=8000', f'--screenshot={f}', url], capture_output=True, timeout=90)
        if not os.path.exists(f): sys.exit(f'no screenshot for t={t} ({url})')
        files.append((t, f))
finally:
    kill_tree(server); shutil.rmtree(prof, ignore_errors=True)
portrait = h > w
cols = a.cols or min(len(files), 6 if portrait else 4)
cw = a.cell or (270 if portrait else 480); ch = round(cw * h / w)
rows = -(-len(files) // cols)
sheet = Image.new('RGB', (cols * cw, rows * ch), (40, 40, 40)); d = ImageDraw.Draw(sheet)
for i, (t, f) in enumerate(files):
    im = Image.open(f).convert('RGB').resize((cw, ch), Image.LANCZOS)
    x, y = (i % cols) * cw, (i // cols) * ch
    sheet.paste(im, (x, y)); d.rectangle([x, y, x + 52, y + 16], fill=(0, 0, 0)); d.text((x + 3, y + 3), f'{t:.2f}', fill=(255, 0, 255))
sp = os.path.join(out, f'{a.name}.png'); sheet.save(sp)
print(f'[stills] {len(files)} frames -> {sp}')

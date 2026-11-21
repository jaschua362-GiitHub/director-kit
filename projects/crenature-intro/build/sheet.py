"""Contact sheet of PNG stills: python build/sheet.py <dir> <out.png> [cols]"""
import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
fs = sorted(glob.glob(f'{d}/*.png')); w = 480; h = 270
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
except Exception: font = ImageFont.load_default()
rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (w + 8) + 8, rows * (h + 34) + 8), (40, 40, 40)); dr = ImageDraw.Draw(sheet)
for i, f in enumerate(fs):
    x, y = 8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 34)
    sheet.paste(Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS), (x, y + 26))
    dr.text((x, y + 2), os.path.basename(f)[:-4].replace('t0', 't=').replace('t1', 't=1') + ' s', font=font, fill=(230, 230, 230))
sheet.save(out); print(out, sheet.size)

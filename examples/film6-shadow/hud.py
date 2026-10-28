"""Post-built POV overlays for draft edit v04 (Jason 27 Oct: scope shot amateur; scan shot unclear).

Two optics, two colour languages:
  hunter  - amber machine vision (HNT-02): converging lock brackets that snap, ticking telemetry, heading tape,
            new-target alert that motivates the whip, then a tracking box on the decoy.
  kaede   - ruby goggle spectrum: a scan bar sweeps down, the wall turns to structure lines and the approved
            two-fan hunter (P02 master) appears as a heat signature behind it, fans spinning.

Each render_* writes an RGBA PNG sequence (24 fps, 480x854, drawn at 2x and downsampled for antialiasing)
that assemble_v04.py overlays on the graded plate.
"""
import json, math, pathlib, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
FF = HERE.parent / "TEST-001/tools/python-media/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe"
HUNTER_ART = HERE.parents[1] / "approved/DCL-20261021-SHADOW/v10/images/props/P02-Hunter-Master.png"
W, H, S, FPS = 480, 854, 2, 24      # layout space stays 480x854; S = supersampling of the drawing canvas
OW, OH = W, H                         # output size of the PNG frames (configure() for the 1080 finish)


def configure(out_w, out_h):
    """Render the same layout at a higher output size (finish: 1080x1920). Draw at >= 2x the output, then downsample."""
    global S, OW, OH
    OW, OH = out_w, out_h
    S = -(-2 * out_w // W)   # integer supersampling (1080 -> 5)
AMBER, RUBY = (255, 178, 70), (255, 70, 80)
MONO = "C:/Windows/Fonts/consola.ttf"
MONO_B = "C:/Windows/Fonts/consolab.ttf"
JP = "C:/Windows/Fonts/YuGothM.ttc"


def font(path, px):
    return ImageFont.truetype(path, px * S)


def ease_out_back(x, k=1.6):
    x = min(max(x, 0.0), 1.0) - 1
    return 1 + (k + 1) * x ** 3 + k * x ** 2


def canvas():
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def save(im, path):
    im.resize((OW, OH), Image.LANCZOS).save(path)


def brackets(d, cx, cy, bw, bh, col, arm=14, t=1):
    x0, y0, x1, y1 = (cx - bw / 2) * S, (cy - bh / 2) * S, (cx + bw / 2) * S, (cy + bh / 2) * S
    a, lw = arm * S, t * S
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(x, y), (x + sx * a, y)], fill=col, width=lw)
        d.line([(x, y), (x, y + sy * a)], fill=col, width=lw)


def frame_furniture(d, col, f, mode, heading, rng, label="HNT-02  OPTIC A"):
    """Corner ticks, ID block, running timecode, heading tape, range ladder, centre cross."""
    c = col + (230,)
    dim = col + (120,)
    m, a = 18, 22
    for (x, y, sx, sy) in ((m, 64, 1, 1), (W - m, 64, -1, 1), (m, H - 96, 1, -1), (W - m, H - 96, -1, -1)):
        d.line([(x * S, y * S), ((x + sx * a) * S, y * S)], fill=c, width=S)
        d.line([(x * S, y * S), (x * S, (y + sy * a) * S)], fill=c, width=S)
    f9, f8 = font(MONO, 9), font(MONO, 8)
    d.text(((m + 6) * S, 72 * S), label, font=f9, fill=c)
    d.text(((m + 6) * S, 84 * S), f"MODE  {mode}", font=f9, fill=c)
    fr = 41 * 24 + 7 + f
    tc = f"02:47:{(13 + fr // 24 // 60) % 60:02d}:{fr // 24 % 60:02d}.{fr % 24:02d}"
    tw = d.textlength(tc, font=f9)
    d.text(((W - m - 6) * S - tw, 72 * S), tc, font=f9, fill=c)
    d.text(((W - m - 6) * S - d.textlength("IR  x4.0", font=f8), 84 * S), "IR  x4.0", font=f8, fill=dim)
    # heading tape
    y = (H - 112) * S
    for k in range(-30, 31):
        deg = math.floor(heading) + k
        x = (W / 2 + (deg - heading) * 5.5) * S
        if not (60 * S < x < (W - 60) * S):
            continue
        big = deg % 10 == 0
        d.line([(x, y), (x, y + (8 if big else 4) * S)], fill=c if big else dim, width=S)
        if big:
            s = f"{deg % 360:03d}"
            d.text((x - d.textlength(s, font=f8) / 2, y + 10 * S), s, font=f8, fill=dim)
    d.polygon([(W / 2 * S, y - 2 * S), ((W / 2 - 4) * S, y - 8 * S), ((W / 2 + 4) * S, y - 8 * S)], fill=c)
    # range ladder (right edge)
    xr = (W - m - 4) * S
    for k in range(-6, 7):
        yy = (H / 2 + k * 18 - (rng * 18) % 18) * S
        d.line([(xr - 6 * S, yy), (xr, yy)], fill=dim, width=S)
    s = f"RNG {rng:5.1f}"
    d.text((xr - 8 * S - d.textlength(s, font=f9), H / 2 * S - 6 * S), s, font=f9, fill=c)
    # centre cross
    cx, cy, g, l = W / 2 * S, H / 2 * S, 5 * S, 10 * S
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        d.line([(cx + dx * g, cy + dy * g), (cx + dx * (g + l), cy + dy * (g + l))], fill=dim, width=S)


def tag(d, x, y, text, col, solid=False, size=9):
    fnt = font(MONO_B if solid else MONO, size)
    tw = d.textlength(text, font=fnt)
    pad = 3 * S
    if solid:
        d.rectangle([x * S - pad, y * S - pad // 2, x * S + tw + pad, y * S + (size + 2) * S], fill=col + (235,))
        d.text((x * S, y * S), text, font=fnt, fill=(10, 8, 4, 255))
    else:
        d.text((x * S, y * S), text, font=fnt, fill=col + (230,))
    return tw / S


def render_hunter_lock(out, dur, target=(203, 512, 108, 280), lock_at=0.45, alert_at=1.25):
    """T14 hold on Aiko: acquire -> converge -> snap LOCK; then TGT 02 alert on the left edge."""
    out.mkdir(parents=True, exist_ok=True)
    n = round(dur * FPS)
    cx, cy, bw, bh = target
    for f in range(n):
        t = f / FPS
        im, d = canvas()
        frame_furniture(d, AMBER, f, "LOCK" if t >= lock_at else "ACQUIRE", 352.0 + 0.4 * math.sin(t * 2), 14.2 + 0.05 * math.sin(t * 7))
        p = ease_out_back((t - 0.08) / (lock_at - 0.08))
        sc = 2.6 - 1.6 * p
        jit = 0 if t >= lock_at else 3 * math.sin(f * 2.3)
        if t >= 0.08:
            locked = t >= lock_at
            brackets(d, cx + jit, cy - jit, bw * sc, bh * sc, AMBER + (255,), arm=12 if locked else 9, t=2 if locked else 1)
            if locked:
                d.line([((cx + bw / 2 + 4) * S, (cy - bh / 2) * S), ((cx + bw / 2 + 22) * S, (cy - bh / 2 - 18) * S)], fill=AMBER + (200,), width=S)
                x0, y0 = cx + bw / 2 + 24, cy - bh / 2 - 30
                tag(d, x0, y0, "LOCK", AMBER, solid=True, size=10)
                tag(d, x0, y0 + 16, "TGT 01  HUMAN", AMBER)
                tag(d, x0, y0 + 27, f"CONF  {min(99, 82 + int((t - lock_at) * 40))}%", AMBER)
            else:
                tag(d, cx - 30, cy + bh * sc / 2 + 6, "ACQUIRING", AMBER)
        if t >= alert_at and int((t - alert_at) * 8) % 2 == 0:
            tag(d, 30, H / 2 - 40, "<< TGT 02", AMBER, solid=True)
            tag(d, 30, H / 2 - 24, "MOTION  090", AMBER)
        save(im, out / f"{f:04d}.png")
    return n


def render_hunter_whip(out, dur):
    """Whip pan: heading tape races, brackets gone, REACQUIRE."""
    out.mkdir(parents=True, exist_ok=True)
    n = round(dur * FPS)
    for f in range(n):
        t = f / FPS
        im, d = canvas()
        frame_furniture(d, AMBER, f + 40, "SLEW", 352 - 95 * (t / dur) ** 0.7, 14.2 + 20 * t / dur)
        if int(t * 12) % 2 == 0:
            tag(d, W / 2 - 34, H / 2 + 30, "REACQUIRE", AMBER, solid=True)
        save(im, out / f"{f:04d}.png")
    return n


def amber_track(src, a, b):
    """Centroid + extent of the orange hologram per frame of T19 (in, out seconds)."""
    raw = subprocess.run([str(FF), "-v", "error", "-ss", f"{a}", "-t", f"{b - a}", "-i", str(src), "-vf", f"fps={FPS},scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(int)
    boxes = []
    for im in fr:
        r, g, bl = im[..., 0], im[..., 1], im[..., 2]
        m = (r > 170) & (g > 90) & (g < 215) & (bl < 120) & (r - bl > 110)
        m[:280] = False; m[H - 140:] = False; m[:, :110] = False; m[:, 400:] = False   # figure zone only: skip lamps, ring corners
        ys, xs = np.nonzero(m)
        if len(xs) > 40:
            boxes.append((float(np.median(xs)), float(np.median(ys)),
                          float(np.percentile(xs, 95) - np.percentile(xs, 5)), float(np.percentile(ys, 95) - np.percentile(ys, 5))))
        else:
            boxes.append(boxes[-1] if boxes else None)
    # smooth
    out, prev = [], None
    for bx in boxes:
        if bx is None:
            out.append(prev); continue
        prev = bx if prev is None else tuple(0.6 * p + 0.4 * q for p, q in zip(prev, bx))
        out.append(prev)
    return out


def render_hunter_track(out, dur, track):
    """T19: tracking box follows the decoy, velocity/range ticking, PURSUE."""
    out.mkdir(parents=True, exist_ok=True)
    n = round(dur * FPS)
    for f in range(n):
        t = f / FPS
        im, d = canvas()
        frame_furniture(d, AMBER, f + 80, "TRACK", 257 + 3 * math.sin(t), 22.0 - 2.5 * t)
        bx = track[min(f, len(track) - 1)]
        if bx:
            cx, cy, bw, bh = bx
            bw, bh = max(bw, 50) + 18, max(bh, 90) + 18
            p = ease_out_back(t / 0.3)
            sc = 1.8 - 0.8 * p
            brackets(d, cx, cy, bw * sc, bh * sc, AMBER + (255,), arm=10, t=2)
            x0, y0 = min(cx + bw / 2 + 8, W - 120), cy - bh / 2
            tag(d, x0, y0, "TGT 02", AMBER, solid=True)
            tag(d, x0, y0 + 15, "HUMAN", AMBER)
            tag(d, x0, y0 + 26, f"V {7.6 + 0.6 * math.sin(t * 5):4.1f} M/S", AMBER)
            if t > 0.5:
                tag(d, x0, y0 + 37, "PURSUE", AMBER)
        save(im, out / f"{f:04d}.png")
    return n


def hunter_sprite(px=176):
    """Heat-signature sprite of the approved two-fan hunter: key off the dark studio backdrop, map to white-hot core."""
    art = Image.open(HUNTER_ART).convert("RGB").crop((0, 300, 941, 1110))
    g = np.asarray(art.convert("L")).astype(float)
    m = np.clip((g - 45) / 50, 0, 1)                     # body is bright ivory, backdrop is near black
    heat = np.clip((g - 40) / 200, 0, 1) ** 1.3          # ruby palette: deep red -> ruby -> white-hot only on the hottest panels
    rgb = np.stack([110 + 145 * np.clip(heat * 1.6, 0, 1), 10 + 230 * np.clip(heat - 0.45, 0, 1) ** 1.2 * 1.8,
                    20 + 220 * np.clip(heat - 0.5, 0, 1) ** 1.2 * 1.8], -1).clip(0, 255)
    rows = 0.62 + 0.38 * (np.arange(g.shape[0]) % 6 < 4)[:, None]   # sensor line structure
    a = (m * rows * 200).astype(np.uint8)
    spr = Image.fromarray(np.dstack([rgb.astype(np.uint8), a]), "RGBA")
    k = px / spr.width
    fans = [(205 * k, (465 - 300) * k, 95 * k), (760 * k, (545 - 300) * k, 75 * k)]   # centre x, y, radius in sprite px
    return spr.resize((px, round(spr.height * k)), Image.LANCZOS), fans


def render_kaede_scan(out, dur, plate_src, a, at=(318, 250), sweep=(0.12, 0.85)):
    """T03 goggle view: ruby structure lines revealed by a downward scan bar, heat signature behind the wall."""
    out.mkdir(parents=True, exist_ok=True)
    n = round(dur * FPS)
    raw = subprocess.run([str(FF), "-v", "error", "-ss", f"{a}", "-t", f"{dur}", "-i", str(plate_src), "-vf", f"fps={FPS},scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    plates = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
    spr, fans = hunter_sprite()
    fj, fs = font(JP, 12), font(MONO_B, 9)
    for f in range(n):
        t = f / FPS
        g = Image.fromarray(plates[min(f, len(plates) - 1)]).filter(ImageFilter.GaussianBlur(1.2))
        edges = np.asarray(g.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))).astype(float)
        p = min(max((t - sweep[0]) / (sweep[1] - sweep[0]), 0), 1)
        ybar = int(H * (1 - (1 - p) ** 2))
        lay = np.zeros((H, W, 4), np.uint8)
        e = np.clip(edges * 2.2, 0, 255)
        lay[:ybar, :, 0] = 255; lay[:ybar, :, 1] = 90; lay[:ybar, :, 2] = 100
        lay[:ybar, :, 3] = (e[:ybar] * 0.75).astype(np.uint8)
        im = Image.fromarray(lay, "RGBA").resize((W * S, H * S), Image.BILINEAR)
        d = ImageDraw.Draw(im)
        if 0 < p < 1:      # the sweep bar itself
            for k, al in ((0, 230), (2, 120), (5, 50), (9, 20)):
                d.line([(0, (ybar - k) * S), (W * S, (ybar - k) * S)], fill=RUBY + (al,), width=S)
        cx, cy = at
        if ybar > cy - 40:                                # signature revealed once the bar has passed it
            rev = min(1, (ybar - (cy - 40)) / 60)
            bob = 3 * math.sin(t * 5.0)
            s2 = spr.copy()
            sd = ImageDraw.Draw(s2)
            for (fx, fy, fr) in fans:                     # spinning fans: hot blurred disc + two faint blades
                sd.ellipse([fx - fr, fy - fr * 0.45, fx + fr, fy + fr * 0.45], fill=(255, 120, 120, 70))
                for k in range(2):
                    ang = t * 26 + k * math.pi
                    sd.line([(fx, fy), (fx + fr * 0.9 * math.cos(ang), fy + fr * 0.4 * math.sin(ang))], fill=(255, 210, 210, 110), width=1)
            s2 = s2.resize((s2.width * S, s2.height * S), Image.LANCZOS)
            al = s2.getchannel("A").point(lambda v: int(v * rev))
            s2.putalpha(al)
            glow = s2.filter(ImageFilter.GaussianBlur(10 * S))
            pos = (int((cx - spr.width / 2) * S), int((cy - spr.height / 2 + bob) * S))
            im.alpha_composite(glow, pos); im.alpha_composite(s2, pos)
            if rev >= 1:
                bw, bh = spr.width + 16, spr.height + 16
                brackets(d, cx, cy + bob, bw, bh, RUBY + (255,), arm=10, t=1)
                lx, ly = cx - bw / 2, cy + bh / 2 + 6
                d.rectangle([(lx - 3) * S, (ly - 2) * S, (lx + 168) * S, (ly + 30) * S], fill=(0, 0, 0, 150))
                d.text((lx * S, ly * S), "熱源 1  ·  警備機", font=fj, fill=(255, 150, 155, 255))
                d.text((lx * S, (ly + 17) * S), "SENTRY x1  ALT 6.2M  HOLD", font=fs, fill=RUBY + (235,))
        d.text((24 * S, 70 * S), "SPECTRUM  THRU-WALL", font=fs, fill=RUBY + (220,))
        d.text((24 * S, 81 * S), f"DEPTH {min(p * 9.4, 9.4):3.1f}M", font=fs, fill=RUBY + (160,))
        save(im, out / f"{f:04d}.png")
    return n


if __name__ == "__main__":       # QC stills of each overlay
    import sys
    tmp = pathlib.Path(sys.argv[1])
    takes = json.loads((HERE / "DRAFT_JOBS.json").read_text(encoding="utf-8"))["takes"]
    render_hunter_lock(tmp / "lock", 1.8)
    render_hunter_whip(tmp / "whip", 0.9)
    render_hunter_track(tmp / "track", 3.6, amber_track(HERE / takes["T19"]["result"], 0.0, 3.6))
    render_kaede_scan(tmp / "scan", 1.8, HERE / takes["T03"]["result"], 2.0)
    print("ok")

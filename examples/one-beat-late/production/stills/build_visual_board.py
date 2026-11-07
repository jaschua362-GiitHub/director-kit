"""Visual board for Jason: each locked board panel beside the frames that will drive it.
Usage: python build_visual_board.py  -> work/VISUAL_BOARD_v01.jpg
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EXP = Path(__file__).parents[2]
B, R, P = EXP / "board/returns", Path(__file__).parent / "returns", EXP / "pilot/returns"
SB = {1: Image.open(B / "SB-1-a01.png").convert("RGB"), 2: Image.open(B / "SB-2-a01.png").convert("RGB")}

ROWS = [
    (1, "1 HOOK  2.2s  480p+SeedVR2", [("P01-SF-a01", "SF")], "Locked-off; boot enters and lands. Glyph composited before it lands. Slide added locally."),
    (2, "2 SHALL WE?  2.6s  native", [("P02-SF-a01", "SF"), ("P02-EF-a02", "EF a02")], "Near-frontal so the left-wrist watch reads. Sideways step to screen right. Rail tick local."),
    (3, "3 SAME COUNT  2.0s  take A", [("A-SF-a02", "A SF a02"), ("A-EF-a02", "A EF a02")], "Take A 7 s: step left (panel 3) ... flourish (panel 10). Her glyph forms beside his foot after the step."),
    (4, "4 ONE BEAT LATE  3.0s  480p+SeedVR2", [("P04-SF-a01", "SF")], "Locked-off overhead; rotation added locally. Glyphs 1-2-3 composited where she was."),
    (5, "5 STEPPING ON HER  1.8s  insert + take B", [("P05-INS-a01", "INS"), ("B-SF-a01", "B SF")], "RE-STAGE: insert (her glyph under his toe), then cut to MCU as his grin slips. Board had a low tilt."),
    (6, "6 IT HURTS  2.6s  insert + native", [("P06-INS-a01", "INS"), ("P06-SF-a02", "SF a02"), ("P06-EF-a02", "EF a02")], "Insert: late glyphs arrive round her still boots. Then push-in, eyes on the empty floor ahead."),
    (7, "7 ONE STEP, THEN WAIT  3.0s  native", [("P07-SF-a01", "SF"), ("P07-EF-a01", "EF")], "Facing screen right (board drawing slip corrected). Heel lowered onto the centre of the glass."),
    (8, "8 IT ARRIVES  1.6s  free insert", [("P08-INS-a01", "INS")], "Her glyph forms slowly; city-light flicker on the glass added locally."),
    (9, "9 HE GETS IT  1.4s  take B", [("B-SF-a01", "B SF"), ("B-EF-a01", "B EF")], "Take B 5 s: grin slips (panel 5) ... looks up, grin back, shoulders roll (panel 9)."),
    (10, "10 THE FLOURISH  2.8s  take A", [("A-SF-a02", "A SF a02"), ("A-EF-a02", "A EF a02")], "Spin lands near the centre of the glass beside her glyph (composited, matted)."),
    (11, "11 HIS ANSWER LANDS  DONE", [(P / "P11-INS-a01.png", "approved"), (P / "P11-EF-a01.png", "approved")], "Approved pilot cut v6, untouched."),
    (12, "12 IN HER OWN TIME  3.6s  native", [("P12-SF-a01", "SF"), ("P12-EF-a01", "EF")], "Same camera as panel 2. Grains begin to stir under her hand (local). Cut to black."),
]


def panel(n):
    sheet, k = (1, n) if n <= 6 else (2, n - 6)
    im = SB[sheet]
    sx, sy = im.width / 1400, im.height / 933  # grid measured on the 1400x933 review copy
    cols, rows = [(10, 462), (475, 925), (935, 1390)], [(88, 440), (500, 880)]
    (x0, x1), (y0, y1) = cols[(k - 1) % 3], rows[(k - 1) // 3]
    return im.crop((int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy)))


def main():
    f1, f2 = ImageFont.load_default(size=24), ImageFont.load_default(size=19)
    bw, tw, th = 380, 380, 214
    rh = th + 50
    out = Image.new("RGB", (bw + 3 * (tw + 5) + 25, rh * len(ROWS) + 60), (24, 24, 24))
    d = ImageDraw.Draw(out)
    d.text((14, 14), "One Beat Late - phase 3 visual board (free stills, 3 Nov 2026). Board panel | frames", fill="white", font=f1)
    for i, (n, title, ims, note) in enumerate(ROWS):
        y = 60 + i * rh
        d.text((14, y + 2), title, fill=(255, 200, 120), font=f1)
        d.text((bw + 20 + 120, y + 6), note, fill=(220, 220, 220), font=f2)
        out.paste(panel(n).resize((bw, th)), (10, y + 32))
        for j, (src, lab) in enumerate(ims):
            path = src if isinstance(src, Path) else R / f"{src}.png"
            t = Image.open(path).convert("RGB").resize((tw, th))
            dt = ImageDraw.Draw(t)
            dt.rectangle((0, 0, 110, 24), fill=0)
            dt.text((4, 1), lab, fill="white", font=f2)
            out.paste(t, (bw + 20 + j * (tw + 5), y + 32))
    out.save(Path(__file__).parent / "work/VISUAL_BOARD_v01.jpg", quality=84)
    print(out.size)


if __name__ == "__main__":
    main()

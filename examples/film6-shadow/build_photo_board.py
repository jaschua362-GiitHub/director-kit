"""Photoreal start-frame board: each locked drawn panel paired with the start frame that will drive its video take."""
import base64, io, pathlib
from PIL import Image
import build_drawn_board as drawn

HERE = pathlib.Path(__file__).resolve().parent
RET = HERE / "startframes/returns"
APPROVED = HERE.parents[1] / "approved/DCL-20261021-SHADOW/v10/images"

# (t_in, dur, beat, start frame, drawn panel (sheet, n) or None, note)
ROWS = [
    (0.0, 1.2, "HOOK", "SF01p", ("SB03", 1), "Goggles snap down; the drone's eye beside her."),
    (1.2, 1.8, "HOOK", "KS03p", ("SB05", 1), "The team: over Kaede down to Aiko across the gap."),
    (3.0, 1.6, "THREAT", "approved:states/SC04-Subjective-Wall-Scan-v10-a02.png", ("SB03", 3), "Scan through the wall. KAEDE: 出口に一機。"),
    (4.6, 1.0, "THREAT", "ST01p", ("SB02", 1), "Aiko perched. AIKO: なら、もっと速く。 KAEDE: 行って。"),
    (5.6, 1.4, "THREAT", "KS02p", ("SB05", 2), "Cloak from the wrist outward; the drone stays solid."),
    (7.0, 1.2, "ACTION", "SF04c", ("SB02", 2), "Explode into the sprint."),
    (8.2, 0.6, "ACTION", "VT01p", ("SB02", 3), "Kong vault."),
    (8.8, 0.6, "ACTION", "DL01p", ("SB05", 3), "Insert: the drone's lens reflects her vault. It's watching."),
    (9.4, 0.9, "ACTION", "SF05bp", ("SB02", 4), "Launch, full extension."),
    (10.3, 1.2, "ACTION", "SF10bp", ("SB02", 5), "Front tuck over the gap (safe fallback: a long-jump take)."),
    (11.5, 1.5, "ACTION", "LD01p", ("SB02", 6), "Three-point landing, eyes up."),
    (13.0, 1.2, "TRAP", "SF07p", ("SB05", 4), "The hunter rises over the door."),
    (14.2, 0.6, "TRAP", "HL01p", ("SB04", 2), "Amber eye flares."),
    (14.8, 1.0, "TRAP", "FD01p", ("SB04", 3), "Hunter POV plate; LOCK brackets added in post."),
    (15.8, 1.2, "TURN 52%", "FD01p", ("SB05", 5), "Same plate; glitch and the wireframe Aiko's same vault composited in post."),
    (17.0, 1.4, "TURN", "PA01p", ("SB04", 5), "The hunter peels away; Aiko puzzled."),
    (18.4, 1.6, "ESCAPE", "DR01p", ("SB04", 6), "Through the door; it seals."),
    (20.0, 4.5, "RECOGNITION", "RC01b", ("SB03", 5), "Cloak switches off, goggles up, untouched wrist. いい囮だったね。 / …私じゃない。 / じゃあ…誰が私みたいに動いたの？"),
    (24.5, 4.0, "RECOGNITION", "SF11p", ("SB03", 6), "The drone's eye turns to meet hers."),
    (28.5, 1.0, "RECOGNITION", "RC01b", ("SB05", 6), "Tail of her take: the wary half-smile; blink; black."),
]


def frame_path(ref):
    if ref.startswith("approved:"):
        return APPROVED / ref.split(":", 1)[1]
    return RET / f"{ref}-a01.png"


def b64(im, w):
    im = im.convert("RGB").copy(); im.thumbnail((w, w * 2))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=84)
    return base64.b64encode(buf.getvalue()).decode()


def main():
    sheets = {}
    cards = []
    for t, d, beat, ref, panel, note in ROWS:
        p = frame_path(ref)
        photo = (f'<img class="ph" src="data:image/jpeg;base64,{b64(Image.open(p), 360)}" alt="{ref}">' if p.exists()
                 else '<div class="ph miss">rendering…</div>')
        sketch = ""
        if panel and (RET / f"{panel[0]}-a01.png").exists():
            if panel[0] not in sheets:
                sheets[panel[0]] = drawn.panels(panel[0])
            sketch = f'<img class="sk" src="data:image/jpeg;base64,{b64(sheets[panel[0]][panel[1] - 1], 120)}" alt="drawn panel">'
        name = ref.split("/")[-1].replace("-v10-a02.png", "") if ref.startswith("approved:") else ref
        cards.append(f'<article><div class="wrap">{photo}{sketch}</div><div class="m"><b>{t:.1f}s</b> · {d:.1f}s · '
                     f'<span class="beat">{beat}</span> · {name}</div><p>{note}</p></article>')
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shadow Start Frames</title><style>
:root{{--bg:#0e0f12;--fg:#e9e6e1;--mut:#9a958d;--card:#17191e;--acc:#e0a040}}
@media (prefers-color-scheme: light){{:root:not([data-theme="dark"]){{--bg:#f4f2ee;--fg:#1b1b1d;--mut:#5d5a55;--card:#fff;--acc:#b5651d}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif}}
main{{max-width:1280px;margin:0 auto;padding:24px 16px 64px}} h1{{font-size:24px;margin:0 0 6px}} .lede{{color:var(--mut);max-width:860px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}}
article{{background:var(--card);border-radius:10px;overflow:hidden}} .wrap{{position:relative}}
.ph{{width:100%;display:block;aspect-ratio:9/16;object-fit:cover}} .miss{{display:flex;align-items:center;justify-content:center;color:var(--mut);background:#2224}}
.sk{{position:absolute;right:6px;bottom:6px;width:30%;border:2px solid #fff;border-radius:4px}}
.m{{padding:8px 10px 0;font-size:12px}} .beat{{color:var(--acc);font-weight:700}} article p{{margin:6px 10px 10px;font-size:13px}}
</style></head><body><main><h1>The Shadow Apprentice: photoreal start frames</h1>
<p class="lede">Built from the LOCKED hand-drawn board D2 and synopsis v2, regenerated with the approved photoreal fix (muted film grade, real skin, approved-only references). Each card shows the start frame that drives a video take, with its locked drawn panel inset. Graphics (the hunter's feed overlays and subtitles) are added in post. No video has been generated.</p>
<div class="grid">{"".join(cards)}</div></main></body></html>'''
    (HERE / "startframes_board.html").write_text(html, encoding="utf-8")
    print("cards", len(cards), "missing", sum(not frame_path(r[3]).exists() for r in ROWS))


if __name__ == "__main__":
    main()

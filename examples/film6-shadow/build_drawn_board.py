"""Hand-drawn storyboard D2: cut the panels out of the sketch sheets and lay them out in film order.

Rule (Jason, 27 Oct): the board stays hand-drawn until it is locked; photoreal frames come after.
"""
import base64, io, json, pathlib
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
RET = HERE / "startframes/returns"

# (sheet, panel 1-6, t_in, dur, beat, action, sound)
BOARD = [
    ("SB03", 1, 0.0, 1.2, "HOOK", "ECU: Kaede's ruby goggles snap down; her drone's amber eye beside her.", "servo snap; low tone"),
    ("SB03", 2, 1.2, 1.8, "HOOK", "THE TEAM: over perched Kaede's shoulder down to Aiko on the far parapet. One target across the gap.", "wind"),
    ("SB03", 3, 3.0, 1.6, "THREAT", "Kaede's scan through the solid wall: the hunter hiding above Aiko's exit door. KAEDE: 出口に一機。 (One at the exit.)", "sensor hum"),
    ("SB02", 1, 4.6, 1.0, "THREAT", "Aiko perched on the parapet, coiled. AIKO: なら、もっと速く。 (Then I go faster.) KAEDE: 行って。 (Go.)", "breath"),
    ("SB03", 4, 5.6, 1.4, "THREAT", "Kaede drops into a crouch and taps her wrist; refraction spreads; she vanishes. The drone stays solid.", "air shimmer"),
    ("SB02", 2, 7.0, 1.2, "ACTION", "Aiko EXPLODES into the sprint: ultra-low lens, camera tracks back.", "taiko in at 120 BPM; footfalls"),
    ("SB02", 3, 8.2, 1.0, "ACTION", "Kong vault over a low railing, body horizontal, left to right. v2 INSERT to draw: the drone's amber lens tracking her, her tiny figure reflected in the glass (0.6 s), the seed of 'it's learning'.", "hand slap on metal; tiny servo whirr"),
    ("SB02", 4, 9.2, 1.0, "ACTION", "LAUNCH off the edge, full extension; camera rises with her. Speed ramp.", "boot hit; music drops a beat"),
    ("SB02", 5, 10.2, 1.2, "ACTION", "FRONT TUCK over the 40-storey gap, seen from above.", "wind roar"),
    ("SB02", 6, 11.4, 1.6, "ACTION", "Three-point landing, dust burst; she springs up into a low guard, eyes up.", "impact hit"),
    ("SB04", 1, 13.0, 1.2, "TRAP", "Over her shoulder: the hunter RISES over the roofline above the door; downdraft whips her scarf.", "fan roar swells"),
    ("SB04", 2, 14.2, 0.6, "TRAP", "ECU: the hunter's amber eye flares. Amber flash frame.", "lock tone"),
    ("SB04", 3, 14.8, 1.0, "TRAP", "Hunter feed: target box locked on Aiko.", "lock tone holds"),
    ("SB04", 4, 15.8, 1.2, "TURN (52%)", "Feed tears: a second, wireframe Aiko sprints away on a far walkway with HER exact stride and vault; the box jumps to it.", "MUSIC CUTS; one glitch tone"),
    ("SB04", 5, 17.0, 1.4, "TURN", "The hunter banks hard and peels away over the gap, chasing nothing. Aiko watches, puzzled.", "doppler fans"),
    ("SB04", 6, 18.4, 1.6, "ESCAPE", "Aiko slips through the double door; it seals.", "door thunk; silence"),
    ("SB03", 5, 20.0, 4.5, "RECOGNITION", "Kaede de-cloaks, pushes her goggles up, stares at her untouched wrist. AIKO (comm): いい囮だったね。 (Nice decoy.) KAEDE: …私じゃない。 (That wasn't me.) AIKO: じゃあ…誰が私みたいに動いたの？ (Then who moved like me?)", "low drone pad"),
    ("SB03", 6, 24.5, 5.0, "RECOGNITION", "Over her shoulder, the drone hovers at eye level. Its amber eye slowly turns to meet hers. Back on Kaede: a wary half-smile. The eye blinks. Black.", "single gimbal servo; final music hit"),
]
TITLE = (29.5, 1.5, "THE SHADOW APPRENTICE - title on the music hit, no title SFX")


def runs(mask, min_len):
    """Spans where mask is True, at least min_len long."""
    out, a = [], None
    for i, v in enumerate(list(mask) + [False]):
        if v and a is None:
            a = i
        elif not v and a is not None:
            if i - a >= min_len:
                out.append((a, i))
            a = None
    return out


def panels(sheet):
    """Cut the 3x2 panels out of a sheet by finding the paper gutters between them."""
    im = Image.open(RET / f"{sheet}-a01.png").convert("RGB")
    g = np.asarray(im.convert("L"), dtype=np.float32) / 255
    H, W = g.shape
    gutter = g > 0.8                                # paper; artwork rarely has a column/row that is 80%+ paper
    top = slice(int(H * 0.02), int(H * 0.40))       # measure column gutters on the top row band
    cols = runs(gutter[top].mean(axis=0) < 0.75, W // 8)[:3]
    out = []
    bands = []
    for x0, x1 in cols:
        bands.append(runs(gutter[:, x0:x1].mean(axis=1) < 0.75, H // 8)[:2])
    for r in range(2):
        for c, (x0, x1) in enumerate(cols):
            y0, y1 = bands[c][r]
            out.append(im.crop((x0 + 3, y0 + 3, x1 - 3, y1 - 3)))
    return out


def b64(im, w=300):
    im = im.copy(); im.thumbnail((w, w * 2))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def main():
    cache = {}
    cards = []
    for sheet, n, t, d, beat, action, sound in BOARD:
        if sheet not in cache:
            cache[sheet] = panels(sheet)
        img = b64(cache[sheet][n - 1])
        cards.append(f'<article><img src="data:image/jpeg;base64,{img}" alt="{sheet} panel {n}">'
                     f'<div class="m"><b>{t:.1f}s</b> · {d:.1f}s · <span class="beat">{beat}</span></div>'
                     f'<p>{action}</p><p class="s">Sound: {sound}</p></article>')
    cards.append(f'<article class="title"><div class="tc">THE SHADOW<br>APPRENTICE</div>'
                 f'<div class="m"><b>{TITLE[0]:.1f}s</b> · {TITLE[1]:.1f}s · <span class="beat">TITLE</span></div><p>{TITLE[2]}</p></article>')
    sheets = "".join(f'<figure><img src="data:image/jpeg;base64,{b64(Image.open(RET / f"{s}-a01.png"), 640)}" alt="{s}"><figcaption>{s}</figcaption></figure>'
                     for s in ("SB03", "SB02", "SB04"))
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shadow Drawn Storyboard</title><style>
:root{{--bg:#f4f2ee;--fg:#1b1b1d;--mut:#5d5a55;--card:#fff;--acc:#b5651d}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0e0f12;--fg:#e9e6e1;--mut:#9a958d;--card:#17191e;--acc:#e0a040}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif}}
main{{max-width:1280px;margin:0 auto;padding:24px 16px 64px}} h1{{font-size:24px;margin:0 0 6px}} h2{{font-size:18px;margin:32px 0 10px}}
.lede{{color:var(--mut);max-width:860px}} .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px}}
article{{background:var(--card);border-radius:10px;overflow:hidden}} article img{{width:100%;display:block;aspect-ratio:9/16;object-fit:cover;background:#ddd}}
.m{{padding:8px 10px 0;font-size:13px}} .beat{{color:var(--acc);font-weight:700}} article p{{margin:6px 10px;font-size:13px}} p.s{{color:var(--mut);font-size:12px;margin-bottom:10px}}
.tc{{aspect-ratio:9/16;background:#000;color:#eee;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:700;letter-spacing:2px}}
table{{border-collapse:collapse;width:100%;font-size:13px;max-width:980px}} td,th{{border-bottom:1px solid #8884;padding:6px;text-align:left;vertical-align:top}}
.sheets{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}} figure{{margin:0}} figure img{{width:100%;display:block;border-radius:8px}} figcaption{{color:var(--mut);font-size:12px}}
</style></head><body><main>
<h1>The Shadow Apprentice: hand-drawn storyboard D2 (synopsis v2)</h1>
<p class="lede">9:16 · about 31 s · 18 panels in film order. Hand-drawn until Jason locks the board; photoreal start frames come only after the lock. <b>Not locked. No video has been generated.</b></p>
<p class="lede"><b>Synopsis v2, "the apprentice learns":</b> Kaede's drone watches Aiko's every move during the run; the false Aiko it plants in the hunter's feed moves exactly like her; "Then who moved like me?" The drone looks back. See SYNOPSIS_PROPOSAL_v2.md. <b>Dialogue in Japanese with English subtitles</b> (DIALOGUE.md).</p>
<p class="lede">Story: Kaede (recon) and Aiko (field) work as one team. Aiko gets the escape with the action from round 2. Kaede's drone plants the false Aiko on its own. The turn lands at 52%, and recognition plus the drone looking back take the last third.</p>
<div class="grid">{"".join(cards)}</div>
<h2>Sync with the approved synopsis</h2>
<table><tr><th>Approved synopsis</th><th>Where it is on the board</th></tr>
<tr><td>Aiko carries stolen intelligence through a guarded rooftop complex</td><td>The one-slit carrier at her right hip, visible in the perch, sprint and landing panels (4.6–13 s)</td></tr>
<tr><td>Kaede's AI spectrum optics locate danger beyond a solid wall</td><td>Goggles down (0 s), then the scan through the wall finds the hunter above the exit (3.0 s)</td></tr>
<tr><td>She conceals herself with the adaptive black membrane suit</td><td>The cloak (5.6 s)</td></tr>
<tr><td>Extraordinary tools, but escape depends on physical skill and mutual trust</td><td>The team shot plus Kaede's "Go." (1.2–4.6 s), then Aiko's sprint, vault, leap and landing (7–13 s)</td></tr>
<tr><td>Aiko crosses the break between buildings with a precise ninja leap</td><td>Launch and front tuck (9.2–11.4 s)</td></tr>
<tr><td>Security closes on her exit</td><td>The hunter rises over the door and locks on (13–15.8 s)</td></tr>
<tr><td>A false Aiko enters the hunter's sensor feed and draws it away</td><td>The feed glitch, the wireframe Aiko, and the hunter peeling away (15.8–18.4 s). It exists only in the feed</td></tr>
<tr><td>The real operative escapes with the intelligence</td><td>Through the door, which seals (18.4 s)</td></tr>
<tr><td>Kaede recognises the diversion was never her command</td><td>"Nice decoy." / "That wasn't me." Her hand never touched the controller (20 s)</td></tr>
<tr><td>Relief unsettled by curiosity and wary respect</td><td>The drone's eye turns to meet hers, then her wary half-smile (24.5–29.5 s)</td></tr>
<tr><td><b>Director change (labelled):</b> the synopsis leaves the "shadow intelligence" unseen</td><td>Synopsis v2: it lives in Kaede's own recon drone, which watches Aiko's run and builds the decoy from her exact movement. "Then who moves like me?" The drone looks back, and the apprentice is the machine. Everything else is unchanged</td></tr></table>
<h2>Source sheets</h2><div class="sheets">{sheets}</div>
</main></body></html>'''
    (HERE / "storyboard_drawn.html").write_text(html, encoding="utf-8")
    json.dump(dict(variant="D2-drawn", locked=False, panels=[dict(sheet=s, panel=n, t_in=t, dur=d, beat=b, action=a, sound=snd)
               for s, n, t, d, b, a, snd in BOARD], title=dict(t_in=TITLE[0], dur=TITLE[1])),
              open(HERE / "STORYBOARD_DRAWN.json", "w", encoding="utf-8"), indent=2)
    print("panels", len(BOARD))


if __name__ == "__main__":
    main()

"""Build the D1 storyboard (STORYBOARD.json + storyboard.html) for TEST-013.

Panels are 9:16 framings cropped from the approved v10 art (read-only). Panels marked
SF need a purpose-built start frame; the panel shows the nearest approved reference.
"""
import base64, io, json, pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "approved/DCL-20261021-SHADOW/v10/images"
OUT = pathlib.Path(__file__).resolve().parent

IMG = {
    "KSKIN": "characters/SC-KAEDE-Skin-Study-v08-a01.png",
    "SC01": "states/SC01-Kaede-Lowered-Optics-v10-a01.png",
    "SC02": "states/SC02-Kaede-Activating-v10-a01.png",
    "SC03": "states/SC03-Kaede-Cloaked-v10-a02.png",
    "SC04": "states/SC04-Subjective-Wall-Scan-v10-a02.png",
    "SC05": "states/SC05-Kaede-Recognition-v10-a01.png",
    "SC06": "states/SC06-Subjective-False-Track-v10-a01.png",
    "ACT01": "action/ACT01-Aiko-Poised-Stance-v10-a01.png",
    "ACT02": "action/ACT02-Aiko-Airborne-Leap-v10-a01.png",
    "ACT03": "action/ACT03-Aiko-Compressed-Landing-v10-a02.png",
    "ACT04": "action/ACT04-Aiko-Completed-Service-Exit-v10-a01.png",
    "DRONE": "props/P01B-Recon-Drone-v10-a01.png",
    "HUNTER": "props/P02-Hunter-Master.png",
    "CARRIER": "props/P01A-Intelligence-Carrier-v10-a01.png",
    "E105": "environment/ENV01/ENV01-05-West-Takeoff-Edge-v10-a01.png",
    "E106": "environment/ENV01/ENV01-06-East-Red-Door-Landing-v10-a01.png",
    "E104": "environment/ENV01/ENV01-04-East-Back-West-v10-a01.png",
    "E109": "environment/ENV01/ENV01-09-Overhead-Roof-Relation-v10-a01.png",
    "E208": "environment/ENV02/ENV02-08-Scan-View-Out-East-v10-a01.png",
}

# Generations: one continuous Seedance performance each. route = how it finishes.
GENS = [
    dict(id="G01", secs=5, start="SF01", start_note="Kaede MCU in recon bay, optics UP at forehead, black drone hovering at her right shoulder (amber gimbal), city beyond the open east side", route="PROMOTE_1080", why="face"),
    dict(id="G02", secs=4, start="SC04", start_note="approved as-is", route="DRAFT_UPSCALE_TEST", why="subjective POV, no face; first wide upscale test"),
    dict(id="G03", secs=5, start="SC02", start_note="approved as-is (first frame); prompt drives the cloak", route="PROMOTE_1080", why="hero effect; cloak must read in motion"),
    dict(id="G04", secs=5, start="SF04", start_note="Aiko mid-sprint on WEST roof toward the gap, low 3/4 front tracking, cyan pillar behind, carrier at RIGHT hip, eyes forward", route="PROMOTE_1080", why="face + hero costume"),
    dict(id="G05", secs=6, start="SF05", start_note="Aiko's lead foot planting on the west parapet, body launching forward, eyes on the EAST roof (fixes ACT02 backward eyeline). Fallback if one take can't hold foot-plant + overhead arc + landing: split into G05a leap (4s) and G05b landing (4s, ACT03 start)", route="PROMOTE_1080", why="hero stunt"),
    dict(id="G06", secs=4, start="ACT03", start_note="approved as-is", route="PROMOTE_1080", why="face rising into frame"),
    dict(id="G07", secs=8, start="SF07", start_note="Behind Aiko on the EAST roof, red door ahead; ivory two-fan hunter beginning to rise over the roofline above the door", route="DRAFT_UPSCALE_OR_720", why="machine + back of Aiko"),
    dict(id="G08", secs=5, start="SC06", start_note="approved as-is (hunter sensor view)", route="DRAFT_UPSCALE_TEST", why="graphic sensor feed"),
    dict(id="G09", secs=4, start="ACT04", start_note="approved as-is", route="DRAFT_UPSCALE_OR_720", why="medium-wide exit"),
    dict(id="G10", secs=8, start="SC05", start_note="approved as-is. One continuous performance: residual refraction clears to black; she pushes the ruby optics UP onto her forehead (on screen: optics are down C01-C06, up from here); looks at her wrist; line; glance to the drone (screen right); wary half-smile lit by a flicker of amber", route="PROMOTE_1080", why="key line close-up + final expression"),
    dict(id="G11", secs=6, start="SF11", start_note="Over Kaede's shoulder in the bay: black four-fan drone hovering at eye level, amber gimbal facing away toward the city", route="PROMOTE_1080", why="payoff"),
]

# Cuts in the edit. (src, cx, cy, zoom) frames the panel from the approved image.
CUTS = [
    ("C01", 0.0, 1.0, "G01", "ECU", "Ruby optics SNAP down over Kaede's eyes; red glass lights.", "micro push-in", "servo snap; low drone tone starts", "KSKIN", .50, .30, 2.4),
    ("C02", 1.0, 0.8, "G01", "INSERT", "Black drone at her shoulder: amber gimbal blinks once.", "rack focus to drone", "tiny fan whirr", "DRONE", .50, .55, 1.6),
    ("C03", 1.8, 1.2, "G01", "MCU", "Kaede behind red glass turns her head toward the east wall.", "slow arc left", "breath", "SC01", .50, .35, 1.5),
    ("C04", 3.0, 1.6, "G02", "POV", "Spectrum view THROUGH the intact wall: ivory hunter silhouette waiting above the red exit door.", "slow push", "sensor hum", "SC04", .55, .45, 1.15),
    ("C05", 4.6, 0.7, "G03", "INSERT", "Gloved finger taps the red/amber wrist controller.", "static, shallow focus", "tick", "SC02", .45, .50, 2.6),
    ("C06", 5.3, 1.7, "G03", "MS", "Black membrane ripples into refraction; Kaede vanishes; drone stays opaque.", "slow push", "air-pressure shimmer", "SC03", .50, .55, 1.1),
    ("C07", 7.0, 1.4, "G04", "LOW TRACK", "Aiko sprints the WEST roof toward the gap, cyan pillar whipping past, carrier bouncing at RIGHT hip.", "low fast track, handheld energy", "taiko enters 120 BPM; footfalls", "ACT01", .50, .60, 1.2),
    ("C08", 8.4, 0.9, "G04", "MCU TRACK", "Eyes fixed on the far roof; scarf snapping.", "tracking, same move", "breath", "ACT01", .52, .25, 2.2),
    ("C09", 9.3, 0.5, "G05", "CU FEET", "Lead foot plants on the parapet edge; speed ramp.", "ramp 100%->40%", "boot hit; music drops a beat", "ACT01", .60, .88, 2.6),
    ("C10", 9.8, 1.7, "G05", "HIGH VERTICAL", "Camera whips up and over: Aiko arcs across the 40-storey chasm, city lights far below.", "rise + tilt down, ramp back to 100%", "wind roar", "E109", .50, .50, 1.0),
    ("C11", 11.5, 0.6, "G05", "MS", "Hard landing on the DRY east roof; compression; dust puff.", "2-frame shake", "impact hit", "ACT03", .50, .60, 1.2),
    ("C12", 12.1, 0.9, "G06", "MCU", "She rises, looks up; breath fogs the mask edge.", "slow push", "breath", "ACT03", .50, .35, 1.9),
    ("C13", 13.0, 1.4, "G07", "OTS WIDE", "Over Aiko's shoulder: the ivory hunter rises over the roofline above the red door, two fans roaring.", "slow crane down", "fan roar swells", "E106", .50, .35, 1.0),
    ("C14", 14.4, 0.6, "G07", "ECU", "Hunter's amber optic locks. Amber flash frame.", "snap zoom", "lock tone", "HUNTER", .62, .45, 2.2),
    ("C15", 15.0, 1.0, "G08", "SENSOR", "Hunter feed: target box on Aiko - LOCK.", "feed jitter", "lock tone hold", "SC06", .50, .50, 1.0),
    ("C16", 16.0, 1.2, "G08", "SENSOR", "Glitch frame: a SECOND Aiko target sprints along the west walkway; reticle jumps to it.", "feed tear", "MUSIC CUTS; one glitch tone", "SC06", .40, .55, 1.3),
    ("C17", 17.2, 1.0, "G07", "WIDE", "The hunter swivels and peels away WEST over the gap.", "whip pan follow", "doppler fans", "E104", .50, .40, 1.0),
    ("C18", 18.2, 0.8, "G09", "MS", "Aiko - a half-beat of confusion - looks after it.", "static", "silence", "ACT04", .50, .30, 1.6),
    ("C19", 19.0, 1.0, "G09", "MS", "She slips through the red door; it closes FULLY.", "static", "door seal thunk", "ACT04", .55, .55, 1.0),
    ("C20", 20.0, 2.5, "G10", "MS", "Bay: refraction resolves - Kaede reappears and pushes her optics up, looking at her wrist. Her hand is nowhere near it. AIKO V.O.: \"Nice decoy.\"", "slow push", "low drone pad", "SC05", .50, .45, 1.1),
    ("C21", 22.5, 2.5, "G10", "CU", "KAEDE (quiet): \"That wasn't me.\"", "very slow push", "pad", "SC05", .50, .27, 2.0),
    ("C22", 25.0, 3.5, "G11", "OTS", "The drone hovers at eye level. Its amber gimbal slowly turns to meet her eyes.", "slow push past her shoulder", "single gimbal servo", "DRONE", .50, .55, 1.3),
    ("C23", 28.5, 1.0, "G10", "CU", "Back on Kaede (tail of her take): a wary half-smile as amber light flickers once across her face. Cut to black.", "hold", "final music hit", "SC05", .50, .27, 2.2),
    ("C24", 29.5, 1.5, "-", "TITLE", "THE SHADOW APPRENTICE - on the music hit, no title SFX.", "-", "music tail", None, 0, 0, 1),
]


def panel(key, cx, cy, zoom, w=270):
    h = w * 16 // 9
    if key is None:
        im = Image.new("RGB", (w, h), "black")
        ImageDraw.Draw(im).text((20, h // 2), "THE SHADOW\nAPPRENTICE", fill="white")
        return im
    src = Image.open(SRC / IMG[key]).convert("RGB")
    W, H = src.size
    cw = W / zoom
    ch = cw * 16 / 9
    if ch > H:
        ch = H; cw = ch * 9 / 16
    x0 = min(max(cx * W - cw / 2, 0), W - cw)
    y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)


def b64(im):
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=78)
    return base64.b64encode(buf.getvalue()).decode()


def main():
    gens = {g["id"]: g for g in GENS}
    cut_rows = []
    for (cid, t, d, gid, size, action, cam, snd, key, cx, cy, z) in CUTS:
        g = gens.get(gid)
        sf = bool(g and g["start"].startswith("SF"))
        cut_rows.append(dict(id=cid, t_in=t, dur=d, gen=gid, size=size, action=action, camera=cam, sound=snd,
                             panel_source=IMG.get(key), needs_built_start=sf, img=b64(panel(key, cx, cy, z))))
    total = round(CUTS[-1][1] + CUTS[-1][2], 2)
    gen_secs = sum(g["secs"] for g in GENS)
    data = dict(project="DCL-20261021-SHADOW", variant="D1", runtime_s=total, generations=GENS,
                generated_seconds=gen_secs, cuts=[{k: v for k, v in r.items() if k != "img"} for r in cut_rows])
    (OUT / "STORYBOARD.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    cards = []
    for r in cut_rows:
        badge = '<span class="sf">START FRAME TO BUILD</span>' if r["needs_built_start"] else ""
        cards.append(f'''<article class="card"><div class="ph"><img src="data:image/jpeg;base64,{r["img"]}" alt="{r["id"]}">{badge}</div>
<div class="meta"><b>{r["id"]}</b> · {r["t_in"]:.1f}s · {r["dur"]:.1f}s · {r["gen"]}<br><i>{r["size"]}</i></div>
<p>{r["action"]}</p><p class="s">Camera: {r["camera"]}<br>Sound: {r["sound"]}</p></article>''')
    grows = "".join(
        f'<tr><td>{g["id"]}</td><td>{g["secs"]}s</td><td>{g["start"]}</td><td>{g["start_note"]}</td><td>{g["route"]}</td><td>{g["why"]}</td></tr>'
        for g in GENS)
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shadow Apprentice Storyboard</title><style>
:root{{--bg:#0e0f12;--fg:#e9e6e1;--mut:#9a958d;--acc:#e0a040;--red:#c8323a;--card:#17191e}}
@media (prefers-color-scheme: light){{:root:not([data-theme="dark"]){{--bg:#f4f2ee;--fg:#1b1b1d;--mut:#5d5a55;--card:#ffffff}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:24px 16px 64px}}
h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:18px;margin:36px 0 10px}} .lede{{color:var(--mut);max-width:820px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}}
.card{{background:var(--card);border-radius:10px;overflow:hidden}} .ph{{position:relative}} .ph img{{width:100%;display:block;aspect-ratio:9/16;object-fit:cover}}
.sf{{position:absolute;left:6px;top:6px;background:var(--acc);color:#111;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px}}
.meta{{padding:8px 10px 0;font-size:13px}} .card p{{margin:6px 10px;font-size:13px}} .card p.s{{color:var(--mut);font-size:12px;margin-bottom:10px}}
table{{border-collapse:collapse;width:100%;font-size:13px}} td,th{{border-bottom:1px solid #3334;padding:6px;text-align:left;vertical-align:top}}
.wrap{{overflow-x:auto}} .beats{{display:flex;height:22px;border-radius:6px;overflow:hidden;font-size:11px}} .beats div{{display:flex;align-items:center;justify-content:center;color:#111;white-space:nowrap;overflow:hidden}}
svg{{max-width:560px;width:100%;height:auto}}
</style></head><body><main>
<h1>The Shadow Apprentice: storyboard D1</h1>
<p class="lede">9:16 · {total}s · {len(cut_rows)} cuts from {len(GENS)} Seedance generations ({gen_secs}s generated per draft round). Panels are framed from the approved v10 art. An amber badge means the shot needs a purpose-built start frame, and the panel shows the nearest approved reference. <b>Awaiting Jason's approval. No video has been generated.</b></p>
<p class="lede"><b>Placeholders:</b> C07, C09, C10, C13, C17 and C22 (the sprint, the leap, the hunter rising and the drone payoff) still show the nearest approved plate, not the real composition. Those come from the five start frames, which cost no video credits and can be made first so the board can be approved on real frames.</p>
<div class="beats" role="img" aria-label="Beat timeline">
<div style="flex:3;background:#7a8fa8">hook</div><div style="flex:4;background:#9aa7b8">threat + cloak</div><div style="flex:6;background:#e0a040">sprint · leap · land</div><div style="flex:3;background:#c8323a;color:#fff">trap</div><div style="flex:3;background:#f2c14e">TURN 53%</div><div style="flex:1;background:#999">exit</div><div style="flex:11;background:#5e6b5a;color:#fff">recognition · drone looks back · title</div></div>
<h2>Story change (director variant D1)</h2>
<p class="lede">The autonomous shadow intelligence lives in Kaede's own black four-fan recon drone. It creates the false Aiko in the hunter's feed without a command. The last image is the drone's amber eye turning to look at Kaede. The "apprentice" is the machine. Everything else in the approved synopsis is kept. See DIRECTOR_TREATMENT.md.</p>
<h2>Blocking (top-down)</h2>
<svg viewBox="0 0 560 300" role="img" aria-label="Top-down blocking map">
<rect x="10" y="40" width="230" height="220" fill="#2a2d33" stroke="#888"/><text x="20" y="60" fill="#ccc" font-size="13">WEST roof (higher)</text>
<rect x="300" y="60" width="250" height="200" fill="#25282d" stroke="#888"/><text x="310" y="80" fill="#ccc" font-size="13">EAST roof (~1.5 m lower)</text>
<text x="246" y="160" fill="#e0a040" font-size="12" transform="rotate(-90 254 160)">GAP ≈ 4.5 m</text>
<rect x="20" y="200" width="70" height="50" fill="#1b3a4a" stroke="#5ac"/><text x="24" y="230" fill="#9de" font-size="11">Kaede bay</text>
<circle cx="80" cy="212" r="6" fill="#111" stroke="#e0a040"/><text x="92" y="216" fill="#e0a040" font-size="10">drone</text>
<line x1="90" y1="225" x2="470" y2="110" stroke="#c8323a" stroke-dasharray="4 4"/><text x="300" y="185" fill="#c8323a" font-size="10">scan through wall</text>
<rect x="470" y="80" width="40" height="14" fill="#c8323a"/><text x="455" y="76" fill="#f99" font-size="10">red door</text>
<path d="M60 120 L230 120" stroke="#9de" stroke-width="3" marker-end="url(#a)"/><path d="M232 120 Q 265 95 320 125" stroke="#e0a040" stroke-width="3" fill="none" marker-end="url(#a)"/><path d="M322 125 L470 95" stroke="#9de" stroke-width="3" marker-end="url(#a)"/>
<text x="70" y="112" fill="#9de" font-size="11">Aiko sprint L→R</text><text x="250" y="92" fill="#e0a040" font-size="11">leap</text>
<ellipse cx="500" cy="55" rx="18" ry="8" fill="#ddd"/><text x="430" y="30" fill="#ddd" font-size="11">hunter rises, then peels WEST</text>
<path d="M480 58 Q 300 20 120 70" stroke="#ddd" stroke-dasharray="3 5" fill="none" marker-end="url(#a)"/>
<text x="110" y="88" fill="#f2c14e" font-size="11">false Aiko (feed only)</text>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#ccc"/></marker></defs></svg>
<p class="lede">Screen direction: Aiko always travels screen left→right (west→east). The hunter's escape heads right→left. Kaede's eyeline from the bay is screen right.</p>
<h2>Shots</h2><div class="grid">{"".join(cards)}</div>
<h2>Generations and finish route</h2><div class="wrap"><table><tr><th>Gen</th><th>Len</th><th>Start</th><th>Start frame</th><th>Finish</th><th>Why</th></tr>{grows}</table></div>
<p class="lede">PROMOTE_1080 = 480p draft first, then finalise the chosen take to native 1080p. DRAFT_UPSCALE_TEST = keep the 480p draft and upscale it locally, tried on one wide before it is relied on. Every promotion is a new take and is re-checked for identity, motion and sync.</p>
</main></body></html>'''
    (OUT / "storyboard.html").write_text(html, encoding="utf-8")
    print("cuts", len(cut_rows), "runtime", total, "generated_s", gen_secs)


if __name__ == "__main__":
    main()

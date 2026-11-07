# Builds REQUESTS_p4.json for the phase 4 batch (Hold the Note, TEST-020). Run: python -I build_requests.py
import json, uuid, pathlib
here = pathlib.Path(__file__).parent
U = dict(l.split("\t") for l in (here / "UPLOADS.tsv").read_text(encoding="utf-8").splitlines() if l.strip())
U = {k: v.strip() for k, v in U.items()}

S25 = "bytedance/seedance-2.5/image-to-video"
MINI = "bytedance/seedance-2.0-mini/image-to-video"

UP = ("GEOGRAPHY: camera on the UPSTREAM side. East (the timber chamber with the celadon fan roof) lies off screen to the LEFT and is NOT in frame; "
      "west (her granite slab) lies to screen RIGHT. He travels toward screen LEFT.")
EASTAXIS = ("GEOGRAPHY: camera on the EAST end looking back WEST along the ribbon toward her slab. The timber chamber is behind the camera and is NOT in frame. "
            "No timber building or roof anywhere in frame.")
WESTAXIS = ("GEOGRAPHY: camera just off the WEST collar, in front of her, looking at her; behind her is the west side of the gorge. "
            "No ribbon, no timber building or roof in frame.")
STILL = "the grain ribbon stays perfectly still: no grain moves, rolls, falls or flies at any moment"
BITE = "the ragged bite in the ribbon's upstream edge near mid-span stays exactly as in the image, same size and place"
END = "No text, no subtitles, no watermark, no cut."
PHOTO = "Photoreal live-action cinema, natural film grain; the same people, costume, light and place as the image{s}."

def head(dur, two):
    s = f"One continuous, unbroken {dur}-second live-action shot that starts exactly on the first image"
    return s + (" and ends exactly on the last image. " if two else ". ") + PHOTO.format(s="s" if two else "")

R = {}
def add(key, model, dur, start, prompt, end=None, audio=False, res=None, draft=False):
    p = {"image": U[start], "prompt": prompt, "duration": dur, "generate_audio": audio, "watermark": False}
    if model == S25: p["output_format"] = "mp4"
    if end: p["last_image"] = U[end]
    if draft: p["draft"] = True
    if res: p["resolution"] = res
    R[key] = {"model": model, "idempotency_key": str(uuid.uuid5(uuid.NAMESPACE_URL, "TEST020-p4-" + key)),
              "frames": [start] + ([end] if end else []), "params": p}

# ---------- face shots: Seedance 2.5 480p drafts (draft-complete to native 1080p in phase 5) ----------
for fmt, s, extra in [("H", "S03H_a01", "He is framed from the knees up, right of centre."),
                      ("V", "S03V_a01", "Tall frame: the ribbon is a dark band climbing up the frame; he is in the lower half, she is small at the top.")]:
    add(f"03{fmt}", S25, 4, s, f"""{EASTAXIS} LOOK: he walks TOWARD the lens; his face points at the camera. Far behind him she faces the camera too, the flute held level at her lips, extending to frame left.
{head(4, False)} Camera: 135 mm telephoto, eye height, f/4, locked off; no cut. {extra}
0-2s: the old courier walks steadily toward camera along the floating ribbon of dark pebbles, basket on his back, sharp; his boots set down calmly on the ridged grains.
2-4s: focus racks slowly from him to her: she becomes sharp, steady, playing a long held note; he softens but keeps walking.
Living world: mist drifts between them; her skirt and loose hair move in the wind; his sleeves stir.
Ribbon: crisp ridge bands, the edges intact, no damage anywhere; {STILL}, even under his boots. {END}""", draft=True)

for fmt, s, e, extra in [("H", "S04H_a01", "E04H_a01", "Her face frontal, the bamboo flute running across the lower frame at her lips, extending to frame LEFT (her right), fingers on the holes."),
                         ("V", "S04V_a01", "E04V_a01", "Tight vertical from her brow to her fingers; the flute crosses at her lips and exits frame LEFT; fingers in the lower third.")]:
    add(f"04{fmt}", S25, 4, s, f"""{WESTAXIS} LOOK: her eyes look just past the lens toward the bridge; she never turns her head.
{head(4, True)} Camera: 85 mm close-up, slightly low, f/2, a very slow push in. {extra}
0-1.5s: she holds a long steady note, lips on the blow hole, eyes focused.
1.5-4s: her breath is running out: her brows tighten, a small tremor runs through her fingers on the holes, her shoulders tense; she keeps playing and does not lower the flute.
Living world: loose strands of hair and her braid move in the wind; the misty gorge behind her stays soft. {END}""", end=e, draft=True)

add("06V", S25, 5, "S06V_a01_bite", f"""{UP} LOOK: he faces screen LEFT as he walks, then twists only his head and shoulders back so his face points to the RIGHT edge of the frame.
{head(5, True)} Same old Korean courier, costume, basket, light and place as both images. Camera: upstream side, 50 mm, chest height, framed from the knees up, locked off with only a barely perceptible drift; no cut.
0-1.5s: He takes his last step along the floating ribbon of dark pebbles toward screen LEFT and stops, both boots planted on the grains.
1.5-2.5s: Keeping his hips and boots facing screen LEFT, he twists only his head and shoulders back so his face points to the RIGHT edge of the frame, toward the far cliff behind him; the round basket stays on his back at the frame's RIGHT edge the whole time. He lifts one hand and cups it beside his mouth.
2.5-5s: He calls out loudly across the gorge, mouth wide, brows raised, voice carried by the wind, then holds the end pose of the last image. He shouts in Korean, an old man's rough, warm voice, every syllable clear: "숨 쉬어! 내가 불게!" <outdoor shout, wind>
Living world: his sleeves, robe hem, loose grey hair and the basket straps move in the steady wind; mist drifts slowly through the gorge below. Continuity and constraints: {STILL}; {BITE}, just ahead of his front foot. He never turns his whole body, never faces the camera, never looks toward screen left. No timber building or roof in frame. No text, no subtitles, no watermark.

Sound: wind across the gorge and his Korean shout only. No music, no other voices.""", end="E06V_a02_bite", audio=True, draft=True)

for fmt, s, e, extra in [("H", "S07H_a02", "E07H_a01", "85 mm close-up, three-quarter on his face."),
                         ("V", "S07V_a03", "E07V_a01", "Tight vertical close-up on his face, room below his chin.")]:
    add(f"07{fmt}", S25, 4, s, f"""{UP} LOOK: his body faces screen LEFT; he looks back over his left shoulder so his eyes and face point to the RIGHT edge of the frame the whole shot; the round basket shows at the frame's RIGHT edge behind his shoulder.
{head(4, True)} Camera: {extra} Static, f/2, no cut.
0-1.2s: lips relaxed and closed, eyes intent toward screen right; he draws a breath through his nose.
1.2-4s: he purses his lips and whistles one long steady note, cheeks slightly drawn in, eyes still intent toward screen right; he holds it.
Living world: his white beard, moustache and loose grey hair move in the wind; the basket strap shifts slightly; gorge mist soft behind. He never faces the camera and never looks toward screen left. No timber building or roof in frame. {END}""", end=e, draft=True)

for fmt, s, e, extra in [("H", "S08H_a01", "E08H_a01", "Framed from the waist up, a pine branch at the frame edge."),
                         ("V", "S08V_a03", "E08V_a01", "Tall frame, waist up; the flute comes down toward the bottom of the frame.")]:
    add(f"08{fmt}", S25, 4, s, f"""{UP} She stands on the west granite slab. LOOK: she faces screen LEFT toward the bridge in three-quarter LEFT profile (we see her left side) the whole shot; she never turns toward the camera or to screen right.
{head(4, True)} Camera: 85 mm, upstream side, eye level, f/2.8, a slow slight drift in. {extra}
0-1s: the flute at her lips, she hears something from the bridge: her eyes widen.
1-2.5s: she lowers the flute to waist height in both hands.
2.5-4s: she takes one big deep breath: chest rising, lips parted, eyes wide with relief, still facing screen LEFT.
Living world: her hair, ribbon tie and skirt move in the wind; the pine branch sways; mist drifts past the peaks behind. {END}""", end=e, draft=True)

for fmt, s, e, extra in [("H", "S10H_a01", "E10H_a01", "From her eyes down to her chin; the flute crosses the frame just below her lips and extends to frame LEFT."),
                         ("V", "S10V_a01", "E10V_a01", "Tall frame: her eyes at the top, lips at centre above the blow hole, the flute exits frame LEFT, fingers at lower left.")]:
    add(f"10{fmt}", S25, 4, s, f"""{WESTAXIS} LOOK: frontal; her eyes look just past the lens toward the bridge.
{head(4, True)} Camera: 100 mm macro extreme close-up, frontal, f/2.8, static. {extra}
0-1.5s: lips just parted after a deep breath, she brings them to the flute's blow hole.
1.5-4s: her lips settle on the blow hole, her fingers settle onto the holes, and a small smile shows in her eyes as she begins to play.
Living world: loose hair strands drift across her cheek in the wind. {END}""", end=e, draft=True)

for fmt, s, e, extra in [("H", "S12H_a01_bite", "E12H_a01_bite", "Her braid, silver hair pin and shoulder very soft in the LEFT foreground."),
                         ("V", "S12V_a01_bite", "E12V_a01_bite", "Her braid and hair pin soft down the LEFT side of the tall frame; him small and sharp in the upper middle.")]:
    add(f"12{fmt}", S25, 4, s, f"""GEOGRAPHY: camera behind HER on the WEST slab, looking EAST across the gorge to the timber chamber with the celadon fan roof, which is in frame where it is in the image. LOOK: he faces the camera (toward her); she is seen from behind and never turns around.
{head(4, True)} Camera: 200 mm telephoto, f/4, static, compressed. {extra}
0-1s: across the gorge he stands at the chamber entrance, turned toward her; in the soft foreground she slowly lowers her flute.
1-1.8s: he gives one small, clear nod.
1.8-4s: he calls one short line across the gorge, a warm old man's voice, distant, every syllable clear, in Korean: "잘 버텼네." <distant outdoor call, wind>
Living world: the celadon vessels hanging in the chamber stir and turn in the wind; her loose hair strands move; mist drifts in the gorge.
Ribbon: the empty ribbon between them is slack and at rest; {STILL}; {BITE}, a small notch on its left-hand edge mid-span. No text, no subtitles, no watermark, no cut.

Sound: wind across the gorge and his short Korean line only. No music, no other voices.""", end=e, audio=True, draft=True)

for fmt, s, e, extra in [("H", "S13H_a01", "E13H_a01", "She is framed from the waist up, mist and peaks compressed behind her."),
                         ("V", "S13V_a01", "E13V_a01", "Tall frame, waist up, misty peaks stacked behind her.")]:
    add(f"13{fmt}", S25, 5, s, f"""{EASTAXIS} LOOK: frontal on her across the gorge; she faces the camera (toward him) the whole shot.
{head(5, True)} Camera: 200 mm telephoto from the east landing, f/4, a slight drift. {extra} The flute held down at her side in her right hand.
0-1.5s: her tense face softens and breaks into a short breathless laugh, shoulders dropping with relief.
1.5-4.5s: still smiling, she calls her question across the gorge, a young woman's bright clear voice, every syllable clear, in Korean: "휘파람은 언제 배우셨어요?" <outdoor call, wind>
4.5-5s: she holds the end pose of the last image, smiling.
Living world: her hair, ribbon tie and skirt move in the wind; mist drifts behind her. No text, no subtitles, no watermark, no cut.

Sound: wind across the gorge, her short laugh and her Korean line only. No music, no other voices.""", end=e, audio=True, draft=True)

# ---------- faceless shots: 720p final takes (SeedVR2 to 1080p in phase 5) ----------
add("01H", S25, 4, "S01H_a01", f"""{EASTAXIS} The lens sits on the ribbon AHEAD of him, so he walks TOWARD the lens; the far (west) stone collar and cliffs are in the soft background.
{head(4, False)} Camera: 24 mm, 15 cm above the grains, f/2.8, locked off; focus on the ridge bands; no cut.
0-1.5s: his worn dark leather boot with its cloth leg wrap comes down toward the lens and lands flat on the ridged dark grains, stepping into focus.
1.5-4s: his weight settles onto the boot, then the heel begins to lift for the next step.
Living world: mist drifts slowly over the gorge in the soft background; his leg wrap stirs in the wind.
Ribbon: crisp ridge bands, intact; {STILL}, even under the boot: the sole presses down without moving a single grain. {END}""", res="720p")

add("01V", S25, 4, "S01V_a02", f"""{EASTAXIS} The lens sits at the ribbon's edge AHEAD of him, so he walks TOWARD the lens; below the ribbon's edge the gorge drops away to a white river far below.
{head(4, False)} Camera: tall frame, 24 mm, 15 cm above the grains at the edge, f/2.8, locked off; no cut.
0-1.5s: his worn dark leather boot comes down toward the lens and lands on the ridged grains in the top third of the frame.
1.5-4s: his weight settles onto the boot, then the heel begins to lift.
Living world: mist slides slowly through the long drop; the white river moves far below.
Ribbon: crisp, intact; {STILL}, even under the boot. {END}""", res="720p")

add("02S", MINI, 4, "S02S_a01", f"""GEOGRAPHY: true nadir: the camera points exactly straight down from about 80 m, no horizon, no sky. The ribbon crosses the square from top-left to bottom-right; she is the tiny figure on the granite slab at the TOP-LEFT end; he is the tiny figure on the ribbon one third of the way along, walking toward the BOTTOM-RIGHT.
{head(4, False)} Camera: drone, 35 mm, locked exactly overhead, almost still; no rotation, no cut.
0-4s: the tiny courier takes a few slow steps along the ribbon toward the bottom-right; she stands still at the top-left end.
Living world: the white river flows and foams below; thin mist slides slowly across the gorge.
Ribbon: {STILL}; its edges stay intact. {END}""", res="720p")

for fmt, s, extra in [("H", "S05H_a01", "The ribbon is a dark band across the upper middle of the frame."),
                      ("V", "S05V_a01", "Tall frame: the ribbon crosses the top; open sky below it down the frame.")]:
    add(f"05{fmt}", MINI, 4, s, f"""GEOGRAPHY: worm's-eye view from BELOW the bridge looking straight up into the pale dawn sky; the courier's boot toe overhangs the ribbon's near edge, the sole seen from below. No timber building or roof in frame.
{head(4, False)} Camera: 24 mm, f/5.6, locked off, completely still; no cut. {extra}
0-4s: the boot and the ribbon hold completely still; only the world around them moves.
Living world: thin mist wisps drift slowly across the sky; the pine silhouettes at the frame edges sway gently in the wind; the light flickers faintly through the moving haze.
Ribbon: {STILL}; the underside stays exactly as in the image. {END}""", res="720p")

for fmt, s, extra in [("H", "S09H_a02_bite", "Granite walls rise on both sides; the ribbon spans the sky high above."),
                      ("V", "S09V_a02_bite", "Tall frame: rock walls rise up both edges; the thin ribbon crosses high near the top.")]:
    add(f"09{fmt}", MINI, 4, s, f"""{UP} The camera is on the river rocks at the bottom of the gorge looking UP; the tiny courier with his round basket walks along the ribbon toward screen LEFT.
{head(4, False)} Camera: 18 mm, f/8, a very slow, slight upward tilt; no cut. {extra}
0-4s: the tiny courier walks steadily along the ribbon toward screen LEFT.
Living world: white water rushes over the wet boulders in the foreground, spray rising; mist drifts along the walls.
Ribbon: crisp; {STILL}; {BITE} (a notch in the ribbon's near edge at mid-span). {END}""", res="720p")

for fmt, s, extra in [("H", "S11H_a02_bite", "Large in the foreground beside a pale carved stone collar."),
                      ("V", "S11V_a02_bite", "Tall frame: the boot lands in the lower half; the ribbon recedes up the frame to her tiny figure.")]:
    add(f"11{fmt}", S25, 4, s, f"""{EASTAXIS} The camera sits on the granite of the east landing at ground level; the boot steps off the ribbon TOWARD the lens. Far behind, soft and tiny, she stands on the west slab.
{head(4, False)} Camera: 35 mm, ground level, f/4, locked off; no cut. {extra}
0-1.5s: his worn dark leather boot steps off the dark grains and comes down flat on the pale granite.
1.5-4s: his weight settles on the stone; the boot stays planted.
Living world: mist drifts across the gorge behind; her tiny skirt moves in the wind.
Ribbon: at rest; {STILL}; {BITE} (on the ribbon's right-hand edge about halfway across). {END}""", res="720p")

for fmt, s, extra in [("H", "S14H_a01_bite", "She stands small on the west slab at frame LEFT; the chamber sits on the east cliff at frame RIGHT, the courier small at its entrance."),
                      ("V", "S14V_a01_bite", "Tall frame: the gorge drops through the frame; she is small at the bottom-left on the slab; the chamber is top-right with the courier at its entrance.")]:
    add(f"14{fmt}", S25, 5, s, f"""GEOGRAPHY: camera on the DOWNSTREAM side, a little high, looking across the gorge. West (her slab) is screen LEFT; east (the timber chamber with the celadon fan roof) is screen RIGHT.
{head(5, False)} Camera: 35 mm, f/8, locked off, completely still; no camera move, no cut. {extra}
0-1s: both figures stand still, facing each other across the gorge.
1-3.5s: he calls his answer across the gorge, a warm old man's voice, distant and small, every syllable clear, in Korean: "사십 년째 건너는 다린데, 그쯤이야." <distant outdoor call, wind, gorge echo>
3.5-5s: he gives a small shrug and turns to go inside the chamber; she laughs softly, her shoulders lifting.
Living world: mist drifts slowly through the gorge; the river moves far below; the celadon vessels stir.
Ribbon: the empty ribbon stays exactly in place, slack and at rest, for the whole shot; {STILL}; {BITE}. No text, no subtitles, no watermark.

Sound: wind, the river far below, his distant Korean line and her soft laugh only. No music, no other voices.""", audio=True, res="720p")

(here / "REQUESTS_p4.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(R), "requests;", sorted(R))

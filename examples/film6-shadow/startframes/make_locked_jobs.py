"""After the board lock (27 Oct 2026): write the fix-sheet prompt and the remaining photoreal start-frame prompts, and add them to JOBS.json."""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P = HERE / "prompts"
AIKO = (P / "ST01.txt").read_text(encoding="utf-8").split("\n\nSHOT:")[0]
KAEDE = (P / "KS01.txt").read_text(encoding="utf-8").split("\n\nSHOT:")[0]

A = "approved/DCL-20261021-SHADOW/v10/images/"
R = "experiments/TEST-013/startframes/returns/"
AI = [A + "characters/AIKO-Front-v08-a01.png", A + "characters/AIKO-Profile-v08-a01.png", A + "characters/SC-AIKO-Skin-Study-v08-a01.png"]
K = [A + "characters/KAEDE-Front-v08-a01.png", A + "characters/KAEDE-Profile-v08-a01.png", A + "characters/SC-KAEDE-Skin-Study-v08-a01.png"]
DRONE = A + "props/P01B-Recon-Drone-v10-a01.png"
HUNTER = A + "props/P02-Hunter-Master.png"
CARRIER = A + "props/P01A-Intelligence-Carrier-v10-a01.png"

SB05 = """A professional live-action action-film storyboard page by a top storyboard artist, matching the attached storyboard sheets exactly in style: pencil and grey marker on off-white paper, energetic gestural drawing, bold camera-move arrows. SIX tall vertical 9:16 panels arranged 3 columns x 2 rows, thin black borders, panel numbers, short handwritten English captions. Characters from the attached references: KAEDE (no mask, high ponytail, ruby goggles on a forehead band, black membrane suit, scarf, wrist controller on her LEFT forearm, short sword sheathed on her back) with her small BLACK drone (four fans, one amber eye); AIKO (bob in a scarf hood, face mask, split-panel dress, sword sheathed on her back, small carrier with an amber slit on her RIGHT hip); the HUNTER (ivory wedge drone, two round fans, amber slit eye). Night rooftops of a neo-futuristic Japanese city. ALL floors DRY, no reflections.
1 "THE TEAM": high angle over perched Kaede's shoulder (she is on a ledge high on the near tower, drone at her shoulder) looking DOWN and ACROSS: far away and lower, Aiko crouches on the narrow parapet at the edge of the near roof, and beyond her a dark GAP and a lower roof with a double door.
2 "CLOAK": Kaede drops into a crouch and taps her left wrist; her body dissolves into wavy refraction lines from the arm outward; the drone stays solid; the floor is DRY matte concrete.
3 "IT'S WATCHING": extreme close-up of the black drone's round amber camera lens; tiny in the curved glass, a reflection of Aiko vaulting over a railing. Note "0.6s".
4 "IT RISES": from behind Aiko (carrier clearly on her RIGHT hip), the hunter rises over the roofline above the double door, downdraft whipping her scarf. Arrow: slow crane down.
5 "THE ECHO": hunter's sensor view with corner brackets; a dotted wireframe Aiko performs the SAME kong vault over a far railing, the target box jumping to it. Note "SAME MOVE".
6 "WARY": close-up of Kaede, goggles pushed up on her forehead, amber light flickering on her face, a guarded half-smile. Note "BLINK - BLACK".
Grey tones only, ruby accent on Kaede's goggles, amber accents on the drone eye, the carrier slit and the hunter eye."""

SHOTS = {
    "VT01": (AIKO, "KONG VAULT. Side-on camera at railing height, 24mm, tracking left-to-right with her: Aiko dives hands-first over a low dark metal railing on the WEST roof, both gloved hands planted on the top rail, body horizontal and fully airborne above it, knees tucking through between her arms, dress panels and scarf streaming behind, eyes forward. Background: the cyan light pillar and the lit city, motion-blurred. The carrier at her RIGHT hip faces camera."),
    "DL01": (KAEDE, "EXTREME CLOSE-UP INSERT of the black recon drone's round amber camera lens filling most of the vertical frame, hovering in the dark recon bay at night: precise machined black housing, a guarded fan edge blurred at frame corner, the curved glass lens glowing soft amber. Reflected small in the curved glass: a tiny distorted figure of a female ninja in black vaulting over a railing on a distant rooftop, city lights around her. Macro lens, very shallow depth of field. Uncanny, attentive, alive. Kaede herself is not in frame."),
    "HL01": (AIKO, "EXTREME CLOSE-UP of the attached IVORY security hunter drone's front: weathered matte ivory armour panels, the vertical amber slit optic FLARING bright, a small camera pod under the nose, the edge of one guarded fan blurred at frame edge. Night, cold rim light, faint downdraft haze. Camera slightly below, 85mm. Menacing, machine-precise. No people in frame."),
    "FD01": (AIKO, "HUNTER'S POINT OF VIEW plate (no overlay graphics; those are added later): high-angle drone view from about 6 metres above and in front of the red double door on the dry EAST roof, looking down at AIKO standing just after her landing, head tilted up toward camera, small in the vertical frame, long shadow from the door lamp. Slight wide-angle distortion and a cool, slightly desaturated security-camera look. The gap and the west tower's edge visible at the top of frame."),
    "PA01": (AIKO, "WIDE, low angle from the dry EAST roof: the attached IVORY two-fan hunter drone banks hard and peels away over the dark gap toward the west tower (moving frame right to left), tilted steeply, fan wash visible, amber optic streaking. In the lower right foreground, AIKO, small, half-turned, watching it go, puzzled, the red door with its warm lamp beside her. Big night sky and lit towers. 24mm."),
    "DR01": (AIKO, "Medium shot from slightly behind and to the side: AIKO slips through the red double door on the dry EAST roof, one door leaf pushed inward with her gloved hand, body already half inside the warm-lit doorway, head turned back over her shoulder for one last glance at the empty sky. Carrier at her RIGHT hip catching the door lamp. 35mm."),
    "RC01": (KAEDE, "RECOGNITION, medium close-up in the dark recon bay: Kaede crouched by the bay's counter, her cloak just switching off: faint residual refraction ripples still clinging to her shoulder and arm edges as the black membrane returns. Her ruby goggles are still LOWERED. She looks down at the red/amber controller on her LEFT forearm, and her right hand is held clear of it, nowhere near the controls. Cyan bar light from frame left, a soft amber glow from the drone hovering just out of frame right. 50mm, focus on her face and wrist."),
}

REFS = {
    "SB05": [R + "SB03-a01.png", R + "SB04-a01.png", K[0], A + "characters/AIKO-Rear-v08-a01.png"],
    "VT01": AI + [CARRIER, R + "SF04b-a01.png"],
    "DL01": [DRONE, R + "SF04b-a01.png"],
    "HL01": [HUNTER, R + "SF07-a01.png"],
    "FD01": AI[:2] + [R + "LD01-a01.png", A + "environment/ENV01/ENV01-06-East-Red-Door-Landing-v10-a01.png"],
    "PA01": [HUNTER, AI[0], R + "SF07-a01.png", A + "environment/ENV01/ENV01-04-East-Back-West-v10-a01.png"],
    "DR01": AI + [CARRIER, R + "SF07-a01.png"],
    "RC01": K + [A + "states/SC05-Kaede-Recognition-v10-a01.png", A + "environment/ENV02/ENV02-01-Neo-Recon-Bay-v10-a02.png"],
}

(P / "SB05.txt").write_text(SB05 + "\n", encoding="utf-8")
for sid, (base, shot) in SHOTS.items():
    (P / f"{sid}.txt").write_text(f"{base}\n\nSHOT: {shot}\n", encoding="utf-8")

jobs_path = HERE / "JOBS.json"
d = json.loads(jobs_path.read_text(encoding="utf-8"))
have = {j["id"] for j in d["jobs"]}
for sid, refs in REFS.items():
    if sid not in have:
        d["jobs"].append(dict(id=sid, prompt=f"prompts/{sid}.txt", aspect="2:3" if sid.startswith("SB") else "9:16",
                              refs=refs, out=f"returns/{sid}-a01.png"))
if "BOARD LOCKED" not in d["note"]:
    d["note"] += (" BOARD LOCKED 2026-10-27 14:17: SB05 fixes + photoreal start frames authorised "
                  "(SF01, KS02, KS03, SF11, VT01, DL01, HL01, FD01, PA01, DR01, RC01).")
jobs_path.write_text(json.dumps(d, indent=2), encoding="utf-8")
print(len(d["jobs"]), "jobs")

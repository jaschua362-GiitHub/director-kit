"""Write the six face-draft prompts (first + last frame, Seedance 2.5). Run: python build_face_prompts.py"""
from pathlib import Path

OUT = Path(__file__).parent / "prompts"

MOON_END = (
    "Continuity and constraints: single unbroken take, no cuts, no dissolve, no still hold, no freeze at any point. "
    "Her face stays the woman in both images throughout: the same narrow, delicate face and features, short layered "
    "black bob with ONE pale silver-blonde streak on her LEFT side, the small ivory watch on her LEFT wrist, the ivory "
    "teardrop pendant on a fine rose-gold chain, burgundy wrap top with ivory collar, charcoal trousers, black "
    "block-heeled ankle boots. The glass floor panel and the dark grey floor beneath it stay perfectly still and "
    "unchanged: no footprints, no marks, nothing moves under the glass. Nothing floats above the glass or in the air: "
    "no dust, no particles, no sparkles, no haze. Living background, nothing frozen: the small branch plant stirs "
    "faintly in vent air, the amber edge-rail lights pulse softly. Anything seen through the window is still grey "
    "lunar ground under a black sky, motionless (no air on the Moon). Lamp light steady and warm. No subtitles, no "
    "text, no logos.")
EARTH_END = (
    "Continuity and constraints: single unbroken take, no cuts, no dissolve, no still hold, no freeze at any point. "
    "His face stays the man in both images throughout: the same face, jaw and eyes, tousled black hair with the "
    "fringe over his forehead, deep navy jacket with cream collar panels and copper studs, black crew-neck top, small "
    "titanium capsule pendant on a dark cord, titanium watch on his LEFT wrist, charcoal trousers, black leather shoes "
    "with a pale sole edge. Earth gravity, natural balance and weight. The glass floor panel and the floor beneath it "
    "stay perfectly still and unchanged: no footprints, no marks, nothing moves under the glass. Nothing floats in the "
    "air: no dust, no particles, no haze. Living background, nothing frozen: through the window the dusk city is "
    "alive, far traffic lights moving, tower windows twinkling, terrace trees swaying gently. No subtitles, no text, "
    "no logos.")

HEAD = ("One continuous, unbroken {d}-second live-action shot on {place} that starts exactly on the first image and "
        "ends exactly on the last image: {what} Photoreal cinema, large-format camera, the same {who}, room, light and "
        "materials as both images. {cam}")

SHOTS = {
    "P02": (4, "the Moon", "a static wide of a woman in her lunar habitat counting under her breath and taking the first step of an old two-step dance across a glass floor panel.", "woman",
            "The camera is static with a tiny, slow drift in.", [
        '0-1.3s: She glances down at the watch on her raised LEFT wrist, lips silently counting "one, two". Two soft ticks from the watch. <two soft watch ticks>',
        "1.3-2.6s: On the count she drops her wrist and takes one light, confident sideways step to screen RIGHT across the glass: her left boot lands flat on the glass with a soft heel click, weight flowing onto it. Low gravity, one-sixth of Earth: the step floats a little; the ends of her bob and the hem of her top lift and settle late. <one heel click on glass>",
        "2.6-4s: She settles onto the new spot with a small private smile, looking ahead, hair and hem still drifting down slowly, and lands on the last image."],
        "quiet habitat hum, the watch ticks, the heel click", MOON_END),
    "A": (7, "Earth", "a static wide of a man in his dusk city apartment dancing on a glass floor panel, first one step, then a playful flourish.", "man",
          "The camera is static with a very slight follow.", [
        "0-0.6s: He stands on the glass near its right end, confident half-smile, nodding a silent count.",
        "0.6-2.4s: On the count he takes one confident sideways step to screen LEFT across the glass: his right shoe lands flat with a soft click, weight settling onto it. <soft shoe click on glass>",
        "2.4-3.6s: He looks down at the glass beside his planted foot, then up; the grin widens, he rolls his shoulders and shifts his weight, loosening up.",
        "3.6-6.4s: His answer: a playfully exaggerated turn, one arm sweeping wide, a full spin on the ball of one foot with his jacket swinging out, then his foot lands neatly flat on the glass near the centre of the panel. Realistic balance and momentum; the pivot foot turns in place and never skids. No bow. <jacket swish, shoe pivot on glass>",
        "6.4-7s: His arm finishes the sweep, the jacket hem settles, a broad delighted grin, eyes down at the glass beside his foot, landing on the last image."],
        "quiet room tone, city dusk faintly through the glass, the shoe click, the jacket swish and pivot", EARTH_END),
    "B": (5, "Earth", "a medium close-up of a man in his dusk city apartment whose grin slips, then comes back.", "man",
          "The camera pushes in slowly and continuously the whole time.", [
        "0-0.5s: Confident grin, eyes down toward the floor at his feet.",
        '0.5-1.5s: His grin slips: a small wince as if he has just trodden on someone\'s foot, a quick intake of breath, "ah", his shoulders lift as he shifts his weight back off one foot, brows pulling together, eyes still down. A sheepish, sorry look. <small wince, intake of breath>',
        "1.5-3.2s: He keeps looking down, rueful and thinking, small breaths, a slight sway; never frozen.",
        "3.2-5s: Something new catches his eye on the floor; he looks at it, then looks UP. The grin comes back, wider, eyebrows up, eyes bright, and he gives a short warm laugh and rolls his shoulders: game on. He lands on the last image mid-roll. <his short warm laugh>"],
        "quiet room tone, city dusk faintly through the glass, his wince, his short warm laugh", EARTH_END),
    "P06": (4, "the Moon", "a woman who has stopped dead in her lunar habitat, holding in hurt.", "woman",
            "The camera pushes in slowly and continuously from a medium shot to a medium close-up the whole time.", [
        "0-4s: She stands still, jaw set, lips gently pressed. Her eyes stay fixed past the camera toward screen right, on the empty floor ahead of her; she never looks into the lens and never looks down. One slow held breath, a small swallow; the hurt held in, not crying. Early in the shot the ivory watch on her LEFT wrist, low in the frame, blinks a small amber light, twice, unanswered; she does not look at it, and it leaves the frame as the camera pushes in. Low gravity, one-sixth of Earth: the teardrop pendant is still swinging slowly in a long arc, the ends of her bob drift slowly. She lands on the last image. <two faint watch tones, her slow breath>"],
        "quiet habitat hum, two faint watch tones, her breath", MOON_END),
    "P07": (5, "the Moon", "a low side view of a woman on a glass floor panel who places one deliberate step and waits.", "woman",
            "The camera drifts slowly sideways the whole time, low near the floor.", [
        "0-1s: She stands in side profile facing screen RIGHT. Her shoulders drop; a slow breath out.",
        "1-3s: She places ONE deliberate step: her front heel is lowered slowly onto the centre of the glass, a soft heel touch, weight following carefully. <one soft heel touch on glass>",
        "3-5s: She waits: hands loose at her sides, eyes on the floor ahead, a quiet decision in her face. Low gravity, one-sixth of Earth: the teardrop pendant swings slowly and comes almost to rest, the ends of her bob and the hem of her top settle late. Small breaths; she is still, but never frozen. She lands on the last image.",
        "Her RIGHT side faces the camera in this shot, so her watch wrist and her streak are on the far side; that is correct."],
        "quiet habitat hum, one soft heel touch, then room tone only", MOON_END),
    "P12": (5, "the Moon", "a wide of a woman on a glass floor panel answering a dance invitation in her own time.", "woman",
            "The camera drifts in slowly the whole time.", [
        "0-1s: She stands on the glass still glowing from a laugh, a soft open smile, eyes on the glass at her side.",
        "1-4s: She answers in her own time: a small, slow, graceful turn of her own on the glass. Low gravity, one-sixth of Earth: her bob and the hem of her top float outward with the turn and linger in the air longer than on Earth, drifting down late. Feet stay on the glass. <a soft heel pivot on glass>",
        "4-5s: The turn ends with her RIGHT hand held out, open, palm down, low over the empty glass beside her, inviting; a soft smile; her hair still settling. She lands on the last image."],
        "quiet habitat hum, the soft pivot", MOON_END),
}

# Restaged wides (4 Nov, Jason on draft edit v01): she stands IN the glass panel, and panel 2 opens on her seeing his
# footprint (composited beside her boots) so the hook connects to the wide.
ON_GLASS = "She stays standing ON the glass, well inside its edge rail, the whole time."
SHOTS["P02b"] = (4, "the Moon", "a static wide of a woman standing on a glass floor panel in her lunar habitat; she sees something in the glass at her feet, smiles, counts under her breath and takes the first step of an old two-step dance.", "woman",
                 "The camera is static with a tiny, slow drift in.", [
    "0-1.0s: She looks down at the glass just to screen-left of her boots, and a small, private, knowing smile spreads across her face, as if she has just recognised something there.",
    '1.0-2.0s: She lifts her LEFT wrist and glances at the watch, lips silently counting "one, two". Two soft ticks from the watch. <two soft watch ticks>',
    "2.0-3.0s: On the count she drops her wrist and takes one light, confident sideways step to screen RIGHT across the glass: her left boot lands flat on the glass with a soft heel click, weight flowing onto it. Low gravity, one-sixth of Earth: the step floats a little; the ends of her bob and the hem of her top lift and settle late. <one heel click on glass>",
    "3.0-4s: She settles onto the new spot with a small private smile, looking ahead, hair and hem still drifting down slowly, and lands on the last image.",
    ON_GLASS],
    "quiet habitat hum, the watch ticks, the heel click", MOON_END)
SHOTS["P12b"] = (5, "the Moon", "a wide of a woman standing on a glass floor panel answering a dance invitation in her own time.", "woman",
                 "The camera drifts in slowly the whole time.", [
    "0-1s: She stands on the glass still glowing from a laugh, a soft open smile, eyes on the glass at her side.",
    "1-3.6s: She answers in her own time: a small, slow, graceful turn of her own on the glass. Low gravity, one-sixth of Earth: her bob and the hem of her top float outward with the turn and linger in the air longer than on Earth, drifting down late. Feet stay on the glass. <a soft heel pivot on glass>",
    "3.6-5s: The turn flows into a slow, graceful sink at the knees, unhurried in the low gravity, as she reaches her RIGHT hand, open, palm down, LOW over the empty glass beside her, inviting. Her eyes go to the glass under her hand and stay there, a soft, expectant smile, waiting for his answer; her hair still settling. She lands on the last image.",
    ON_GLASS],
    "quiet habitat hum, the soft pivot", MOON_END)

for sid, (d, place, what, who, cam, beats, sound, end) in SHOTS.items():
    text = "\n\n".join([HEAD.format(d=d, place=place, what=what, who=who, cam=cam), "\n".join(beats),
                        f"Sound: {sound}. No music. No spoken words." if sid != "B" else f"Sound: {sound}. No music. No other words.",
                        end]) + "\n"
    (OUT / f"{sid}-VIDEO.txt").write_text(text, encoding="utf-8")
    print(sid, d, "s", len(text), "chars")

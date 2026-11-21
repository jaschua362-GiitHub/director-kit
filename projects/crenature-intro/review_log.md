# Review log: Crenature_Intro_5s_v1 (60 fps)

## Round 1, independent critic

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 5 | 0.0–0.4 s is an empty grey field; the brief's opening eye-glow is missing. At 0.5 s a flat black smear enters top right, with no tension yet. |
| 2 | Phone readability | 8 | phone.png 4 s: the wordmark and the horn and throat hairlines hold at 360 px. At 1 s the flying body reads as a blot. |
| 3 | Motion quality | 4 | 0.5–2.5 s: lumpy, wobbling outline with no taper. 1.07–1.2 s: the head makes a hairpin back up beside its own body. 1.33–1.5 s: the head crosses over the body (tangle). 2.53–2.62 s: the coil cross-fades into the SVG; the throat shard and tail spike fade in as ghosts. |
| 4 | Variety & pacing | 7 | A new beat roughly every second until 3.6 s. The hold (3.8–5.2 s) has motion 0.1–0.2 per second and the lockup width grows under 1 % per second, so it reads as nearly frozen. |
| 5 | Composition | 6 | 1.0–1.3 s: the body sits 80–120 px from the left edge. End lock is 78 % of frame width (brief: about 70 %), with margins of 195 and 223 px; the bounding box is 14 px left of centre. |
| 6 | Brand accuracy | 6 | The end geometry matches the approved SVG. Against final_look_3d.jpg the body is crushed black: no grey sheen on the big curve, no rim light, only thin specular streaks. |
| 7 | Sound sync | 6 | Whoosh at 0.35 s and the lock hit at 2.55 s are on cue. -13.5 LUFS passes. True peak -0.6 dBFS fails (limit -1.5). The coil (1.8–2.5 s) sits at about -30 dB, so the tightening tone is barely there, and the chord is cut off at 5.15 s. |

## Three biggest problems

1. **Flight is a lumpy blob that tangles (0.5–2.5 s).** Fix: build the body as one filled ribbon along a single route (the snake rule): a constant-width core that tapers to the tail, and a smooth contour with no noise displacement. Widen the U-turn at 1.1 s so the head never folds back beside the body. Route the 1.4 s loop so the head goes around the body, not across it. Keep the whole path at least 10 % from the frame edges.
2. **The lock is a cross-fade between two states, not a coil (2.53–2.62 s).** Fix: have the ribbon's final route equal the SVG spine, so that the body arrives already the exact mark. Then grow the throat shard and tail spike outward from their roots along their own tangents, starting after the body is clean (finish the morph before the parts land). No opacity fade-ins.
3. **The final look is cheaper than the reference (2.8–5.2 s).** Fix: raise the height-field roughness and add a broad grey softbox reflection on the big curve and a warm rim on the outer edge, so it matches environment-endcard-light.png. Scale the lockup to 70 %. Add a slow light sweep and a push of 3–5 % per second through the hold. Open on the eye glow at 0–0.4 s. Limit true peak to -1.5 dBFS, lift the coil tone by about 8 dB, and let the chord decay to silence before 5.2 s (or extend to about 5.6 s).

VERDICT: ANOTHER ROUND

## Round 2, independent critic (v2)

**Round 1 check**
- No eye-glow opening: PARTLY (no empty-field beat).
- Lumpy blob, no taper: STILL PRESENT (2.0 s).
- Hairpin at 1.1 s: FIXED.
- Tangle at 1.4 s: PARTLY (the head swivels under its loop).
- Cross-fade lock and ghost parts: STILL PRESENT.
- Edge hugging at 1.0–1.3 s: FIXED.
- Lockup at 78 %: FIXED (69.8 %).
- Lockup off-centre: STILL PRESENT (12.5 px left).
- Crushed black: PARTLY.
- Frozen hold: FIXED (a 3 %/s push).
- True peak: FIXED.
- Chord cut off: FIXED.
- Quiet coil tone: STILL PRESENT (-30 dB at 1.9 s).

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 5 | 0–0.4 s: the head sits parked 24 px from the right edge (0.07 change per frame). Then a stiff diagonal slab. |
| 2 | Phone | 8 | At 4 s the wordmark and horn hairline hold. At 1 s the body is a blot. |
| 3 | Motion | 4 | At 2.567 s the frame difference is 0.67 against about 0.1 around it, and the ink area jumps 12 % in one frame. |
| 4 | Pacing | 6 | 2.2–2.55 s: the coil stalls (0.09 change per frame). Push only after 3.7 s. |
| 5 | Composition | 7 | The end lock spans 277–1618 px, so it sits 12.5 px left. |
| 6 | Brand | 7 | The geometry matches the SVG. The surface reads as harder plastic than the reference. The letters fade in instead of a tail sweep. Faint background banding. |
| 7 | Sound | 7 | -14.6 LUFS and -2.5 dBTP pass, and the hit at 2.55 s lands on the lock. The coil is still quiet, and the 4.25 s hit has no visual event. |

**Three biggest problems**
1. **The lock pops (2.53–2.62 s).** The lumpy ink snaps to the clean mark in one frame, then a ghost tail arc lingers. Fix: drive the body from the SVG spine from 1.8 s so it converges with no swap. Grow the tail spike and throat shard from their roots after 2.6 s, with no opacity fades. Make the tighten land on the hit.
2. **Cheap flight body (0.4–2.5 s).** Fix: build one smoothed ribbon that tapers to a pointed tail. Turn the head with the tangent, never under its own loop. Bend the 0.5–1.0 s diagonal into an S.
3. **Opening and end lock (0–0.4 s, 2.8–5.6 s).** Fix: open on the empty field with the eye opening at least 10 % in from the edges, then bring the body in. Shift the lockup 15–20 px right. Add a light sweep and a blink on the 4.25 s hit. Soften the specular toward the satin of the reference. Dither the background, and raise the coil tone by 8 dB.

VERDICT: ANOTHER ROUND

## Round 3, independent critic (v3)

**Round 2 check**
- Lock pop: PARTLY. There is no one-frame spike now, but 2.35–2.55 s is a cross-dissolve (double contour at 2.45 s).
- Cheap flight body: PARTLY. The tail is pointed, but the outline is lumpy at 2.0–2.3 s and the head is a flat wedge.
- Diagonal bent into an S: PARTLY. At 1.0 s it is still a slab.
- Eye opening inset: PARTLY. It is a 6 px speck, then the body fades in mid-air at 0.37 s.
- Lockup shifted right: FIXED (+3 px).
- Sweep and blink on the hit: PARTLY. The blinks at 3.07 s and 4.35 s have no hit; the hit at 3.80 s has no event.
- Satin specular: FIXED.
- Dither: FIXED.
- Coil tone: FIXED (rises from -26 to -12 dB).

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 6 | 0–0.37 s: an empty field and a speck. |
| 2 | Phone | 8 | 3–5 s: the wordmark and hairlines hold. At 1 s the body is a blob. |
| 3 | Motion | 5 | 0.383 s: the change is 1.73 against 0.05, a fade-in pop. 0.7 s and 1.0 s: stepped blur ghosts. 1.33–1.38 s: the head swivels about 180° in 4 frames. 2.45 s: double contour. |
| 4 | Pacing | 7 | Motion is 0.3 per second from 2.6 s. 3.6–5.6 s has only a blink and the push. |
| 5 | Composition | 8 | The lock is 70.0 % wide, +3/-6 px from centre. At 1.0 s the head is 115 px from the bottom edge. |
| 6 | Brand | 7 | The end geometry matches the SVG. The gloss reads as rubber, not satin. 3.25 s: the wordmark is a soft gradient wipe, with no tail whip. |
| 7 | Sound | 6 | -14.0 LUFS and -2.4 dBTP pass. There is no lock click at 2.5 s. The loudest hit (3.80 s) lands on nothing. |

**Three biggest problems**
1. **Popping, cheap flight (0.37–2.4 s).** Fix: enter from off-screen right with no opacity ramp. Give the eye a real glow first. Use the SVG head throughout. Use 16 or more blur subframes. Smooth the spine by arc length. Slow the head turn.
2. **Dissolve lock (2.35–2.55 s).** Fix: morph matched arc-length points (or drive the ribbon from the SVG spine from 1.8 s) so one contour converges. Grow the shard and spike from their roots.
3. **Sound and wordmark disconnected (3.0–4.4 s).** Fix: put the 3.80 s hit on a blink and glint. Flick the tail at 3.0 s and drive a hard-edged reveal from its tip, with one note per letter. Add a travelling light sweep through the hold.

VERDICT: ANOTHER ROUND

## Round 4 (new direction)

Critic: independent pass on `out/Crenature_Intro_v4_1920x1080_60fps_sound.mp4`. Extra frames in `review/critic_4/`.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 5 | 0–2.3 s motion 0.2/0.6 per s; the "razor rim" at 1.6 s is a dim grey smear (body luma ~15–40), not a blade of light |
| 2 | Phone readability | 6 | phone.png 1 s: black dragon on black is invisible at 360 px; 3 s+ lockup reads well |
| 3 | Motion quality | 6 | No one-frame pops; but 2.38–2.57 s luma 8→240 in 10 frames as a flat disc wipe; hold 3.4–5.6 s frame diff ~0.1, push and 4.4 s glint don't register |
| 4 | Variety & pacing | 5 | Motion/s 0.2 0.6 7.9 0.3 0.2 0.2: all energy in one 0.2 s burst, 2.3 s of near-black before it and a 2.2 s static hold after |
| 5 | Composition | 7 | End lock 69.6 % wide, centre 963/539, margins 295/287 px, good; 1.5–2.8 s dragon parked at left third, 2/3 of frame empty |
| 6 | Brand & tone | 5 | Geometry and rigidity match the approved mark; finish is soft inflated rubber with blurry highlights, none of the crisp warm-grey specular edges in final_look_3d; eye is a flat dull orange at 5.5 s |
| 7 | Sound sync | 8 | Hit ~2.50 s on burst peak; 9 ticks 2.85–3.25 s at 50 ms match the letters; -14.5 LUFS, TP -2.5 dBFS; level dips to -21 dB at 2.40 s, so the riser doesn't build |

**Biggest problems**
1. **0.55–2.3 s: the carve isn't on screen.** Fix: a 1–3 px near-white specular rim (luma 200+) travelling the spine with a hot leading point and a short motion-blurred trail; body stays black; frame the pull-back so the mark lands centred, not parked left.
2. **2.38–2.57 s: the light burst is a 2D circular iris wipe** with a soft ring edge and macroblock smear on the dark side (lifted 2.43 s frame). This is the cheapest-looking moment. Fix: stage it as lighting. Strip lights snap on in 2–3 staggered steps (floor, then backdrop), with a 1–2-frame overexposure and bloom on the speculars and no geometric edge. Put the hit on the first light.
3. **2.6–5.6 s: final material and hold.** It reads as rubber, the eye is dull and the hold is dead. Fix: narrow, sharp highlights; warm-grey edge sheen on the big curve and tail; an emissive eye with small bloom; a visible specular streak at 4.4 s plus a 6–10-frame glint; a 3–4 % push. Also encode at 10–15 Mbps with dither or grain: the 0.6 s eye glow and vignette show stepped rings (2.9 Mbps now).

VERDICT: ANOTHER ROUND

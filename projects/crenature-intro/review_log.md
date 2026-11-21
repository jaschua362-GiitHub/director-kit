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

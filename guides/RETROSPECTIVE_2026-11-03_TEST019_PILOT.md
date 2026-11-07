# Retrospective: One Beat Late panel 11 pilot (TEST-019), 3 November 2026

Read after the TEST-018 retrospective, before planning a moving shot. Film: DCL-20261030-BEAT. Pilot shot: board panel 11, "His answer lands". It was approved by Jason on 3 Nov 2026 (approval (lab file, not in kit: `experiments/TEST-019-one-beat-late/pilot/PILOT_APPROVAL.json`), record (lab file, not in kit: `experiments/TEST-019-one-beat-late/pilot/README.md`)). It was directed by Claude Opus 5.5 on Atlas Seedance 2.5 and cost USD4.33: two 480p drafts plus one native 1080p `draft-complete`. All stills were free (Route B).

## What went wrong, and the rule

| What happened | Rule |
|---|---|
| The start frame showed her full figure with a face about 60 px tall. In first-frame mode the push to a medium close-up turned her into a broader, older woman. | **If a move ends on a readable face, give it a last frame.** Make a C01-F-based end frame (free) and run first + last frame (Atlas `last_image`). Draft 2 then held identity to the last frame. |
| Seedance piled the "grains under the glass" on top of the glass as a mound around her boots, twice, even with "sealed beneath the glass" in the prompt. | **Don't ask the generator for under-glass granular effects.** Plan them as a local composite on a clean plate from the start. |
| A 2D patch of frame-1 boots under a rising camera passed sampled checks, but jittered and doubled in playback. Jason: "glitch n jumping ghosting… cannot be accepted". | **Check composites on every frame and in playback, never on samples.** A flat paste cannot follow a 3D move. If the camera moves, don't patch the subject; cut around it. |
| The fix that passed was a free animated still insert (low on the glass, grains swirl, footprint presses in), then a cut to the untouched generated move after the problem area has left frame. | **Insert + cut beats patching.** Generated footage stays untouched, so it can't ghost. Keep the insert's push accelerating into the cut so the motion carries through. |
| A hand-built procedural footprint read as claw marks. | **Reuse approved art for effects.** E01-07's footprint relief, applied as low-frequency shading on the plate's own grain, read correctly at once. |

## Technical notes
- Atlas Seedance 2.5 image-to-video accepts `last_image` with `image`. `draft-complete` takes only `draft_id`; it returns 1920x1080 HEVC Main10, close to the draft but not pixel-identical. It cost USD2.98 for 5 s. Drafts were USD0.67 each.
- The ChatCut 100-credit pack is USD30 (USD0.30/credit). That's dearer per second than Atlas, so don't buy packs for video.
- Reusable local tools:
  - `experiments/TEST-019-one-beat-late/pilot/composite/insert.py` animates a still: accelerating push, grain vortex under glass with reflections protected, footprint relief, per-frame film grain.
  - `composite/glass_beat.py` is the in-place repair. Only use it when the camera barely moves.
- Panel 3.4 s vs Seedance minimum 4 s: generate 5 s and fix the trim window **before** timing any composite.

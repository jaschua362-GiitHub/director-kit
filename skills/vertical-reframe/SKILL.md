---
name: vertical-reframe
description: Plan, approve and render a 9:16 vertical cut of an approved 16:9 film — per-shot windows, camera moves, optional AI band extension. Use whenever a vertical/portrait/social cut of a horizontal film is requested. Written from the WIND v02 vertical (2026-10-16), where weak framing judgement cost four framing redos and about 2 h of re-rendering.
---

# Vertical Reframe (16:9 → 9:16)

A vertical is re-directed, not cropped. A 608 px window out of a 1920 px frame throws away two thirds of every shot,
so each shot needs a decision about **who the shot is about at its resting moment**. Lock every framing decision on
cheap previews before any upscale or AI fill is rendered.

## What went wrong on WIND (do not repeat)
| Shot | My first framing | Jason's correction | Rule it teaches |
|---|---|---|---|
| S4 impact | Rode the hammer; Ren cut at the right edge | Hero whole and central, hammer swings in | Hero first, prop second |
| S6a gears | 880 px pan in 1.5 s to "show more detail" | Too fast to read; drift a little or hold | Detail shots ≤ ~100 px/s |
| S7 third eye | Off-centre on one eye; then AI-extended face | Gem centred, both eyes at the edges, original pixels only | Never AI-extend faces; centre the iconic feature |
| S13 ready | Drifted right toward the gem/ear | Face centred by the end | Measure the subject; don't guess |
| S14 rush | Tracked the hammer | Over-the-shoulder on the hero | At the climax, the hero carries the frame |

Root causes: windows were set by eye from thumbnails instead of measured subject positions; I optimised for showing
the art/prop over the character; pan speed was never checked; the plan was shown as static start/mid/end tiles, so
motion problems only appeared after the full render; AI fill was rendered before framing was locked.

## Process
1. **Read the approved film + plan**, list shots with frame ranges. Work from the pre-grade picture (grade/grain once at the end).
2. **Measure, per shot**, the x-track of what matters (face centre, gem, hero body extents, prop) through the shot:
   colour masks, face detection or a hand-marked keyframe at start/mid/end. Record numbers in the plan JSON.
3. **Decide each window** with the rules below. Write `cx`, `w`, the move and the *why* per shot.
4. **Preview for approval before rendering anything expensive**: a real-time 540×960 preview MP4 with the approved
   audio (hatched bands where extension is needed) **and** a start/mid/end board. Jason judges motion in the MP4.
   Ask for notes on every shot in one round.
5. Only after the framing is approved: crops → Real-ESRGAN → AI band fill (if any) → composite → look → title → audio.
6. QC: seams at full size, colour match across the seam, all frames decode, audio packet MD5 equals the approved master.

## Framing rules
- **Hero first.** Keep the protagonist whole (no edge-cropped body at the action peak). Props enter the hero's frame, not the other way round.
- **Resting moment.** Each shot ends (or holds) with its subject centred: a face on the nose/eye line, an emblem like a gem dead centre.
- **One eased move per shot**, no reversal, no hold-move-hold. Speed caps in 1080-high source px: ≤ ~100 px/s over fine detail (mechanisms, textures, faces); ≤ ~300 px/s for motivated action follows (WIND S1 246 px/s and S5 312 px/s were accepted; S6a 587 px/s was rejected).
- **Two subjects too far apart** (> ~600 px): pan from cause to effect only if it is slow enough to read; otherwise pick the hero and let the other enter or exit frame.
- **Scale-down + AI extension** (w > 608): only when the extra height is background (floor, ceiling, hall, sky). Never for faces or character design detail (hair, facial hair, makeup, emblems) — use original pixels and choose the best 608 crop instead.
- Native-render titles and graphics at 1080×1920 rather than cropping them.

## AI band extension (local, $0) — what works
- Wan2.1 VACE-1.3B on the RTX 3080 10 GB: `experiments/TEST-010/work/vace_batch.py` (bf16, 480×832 canvas, 29-frame chunks with 5 known overlap frames, shift 16, guide 5, 40 steps, ~13 min/chunk). Run as one background job; no polling.
- Composite with `work/vert_composite.py`: ESRGAN the fill, per-band gain/offset matched to the approved centre at the seam (smoothed over 9 frames), 28 px feather. Darken invented objects into shadow rather than letting them read.
- Disclose AI-extended shots in the approval record.

## Cost discipline
Every re-render after a late framing note is wasted GPU time and Claude tokens. Steps 2–4 are cheap; spend there.

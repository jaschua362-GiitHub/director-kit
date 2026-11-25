# Production card

Read this when you start the production stage. Required reading: `DIRECTOR_CRAFT.md`, the three every-session cards, this card and your handoff. The Lab keeps a longer depth file behind this card; it is not in the kit.

## What this stage is for
Paid takes from approved plates: drafts, HD, retakes and finish routes. Jason judges motion, faces and hands at full size.

## What good looks like
- One anchor (the first frame) and one named, eased camera move per shot (The Unstitched).
- Alive to the last frame: every hand, flame, puppet and extra given an action; never "static", "holds" or "nothing else moves" in a prompt: "all elements need to be as real life as possible."
- Fix physics by regenerating; grades and crops fix only appearance (Tide: four rounds).

## Look for
- Every face at 100 % on the master, both formats. Hold the Note retakes: USD 38.
- Whole takes at normal speed. Contact sheets passed Hold the Note's morphs (USD 11).
- Crop background figures at 5-6 timestamps; each must move (House of Courtesy B10, USD 10.67).
- First and last 12 frames and every hand-prop overlap at 100 %. House of Courtesy B9, USD 7: "the book does cut through the hand and no agent spotted it".

## Let the script check
- First and last frames differ; nothing is frozen, whole frame and per region against the approved draft (hands, flame, faces at 0.7x or more): `tool: tools/craft_check.py anchors`, `motion`; per region `lab script, not in kit: life_audit.py`.
- Near-duplicate frames in every draft take before the cut; re-lay stutter with optical-flow in-betweens, never a blended slow-down: `lab script, not in kit: retime_flow.py`.
- Edge snaps; 100 % sheets of the first and last 12 frames: `tool: tools/craft_check.py edges`.

## How this stage runs
- Before any video prompt, a continuity sheet per shot (flame, light on the cloth, props, set, screen direction); deliver each 480p draft with that sheet and a verdict; HD only after his reply.
- HD of an approved draft is `bytedance/seedance-2.5/draft-complete` with `draft_id` (the draft's prediction id), never a fresh 1080p take; check it against its draft; frames match, so lock the cut at 480p.
- Sessions and models: the handoff card.

## Settled
- Route: any person in frame gets a Seedance 2.5 draft, then its draft-complete at 1080p; otherwise a cheap native model, Seedance after one failure.
- Anchors: first frame only; an end frame only when the end state must differ, or to join takes (`fight-sequence.md`). A pinned last frame freezes the actor (The Last Ferry B18 read as a still): pin it only when that pose is the point.
- Faces: every readable face native 1080p; short of money, cut runtime.
- Retakes: one carries every known fix; change method after two failures; a one-prompt take (one generation, many shots): one re-roll, then patch.
- Finish route: fixed per shot at the start-frame gate in the shot list (draft-complete, SeedVR2 faceless, or a named remaster); no candidate carries a 480p shot. A painterly film may finish on local SeedVR2 after single-frame close-up tests and his yes (Jason, The Last Ferry: "worth really trying the upscaling route"); its texture shimmers frame to frame and a temporal pass ghosts moving limbs, so a shot with a limb moving close in frame goes native. Kling remaster drifts a face (Ferry B17): faceless shots only.
- Model by shot importance (Jason, 16 Nov 2026): an unimportant shot may use a cheaper model, "strict on portrait realism". Kling with a face in frame went "cg toon like" (Courtesy, USD 18.92) and failed on hair (Fritter B15).
- Open: teasers follow the same no-upscaled-faces rule unless he restores his 5 Nov exception.

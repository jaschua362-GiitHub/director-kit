> **Archive since 12 Nov 2026.** The current required reading is `craft/DIRECTOR_CRAFT.md` and its cards in `craft/cards/`; start at `START_HERE.md`.
> This file is kept unchanged below as the record. Nothing in it overrides the craft page or cards.

# Retrospective — TEST-024 Forsaken opener (one-prompt 30 s, client-pitch test), 12 November 2026

For every director. One session, about four hours, about USD 30 on Atlas (three 480p drafts 12.04, Suno cue 0.13, native 1080p finish 17.77). Jason accepted master v01 and closed the job the same day. Records: `lab file, not in kit: README.md`; final: `FINAL_RENDERED/TEST-024-FORSAKEN-OPENER/video-landscape-v01/`.

## What worked
1. **One-prompt take for a fight with VFX.** Three 30 s drafts; identity, two worlds and ten-odd beats arrived in order every time. Eight references (seven character/creature/location stills from the Codex bridge, free, plus a crew line-up).
2. **Story notes beat settings.** Draft 01 was "not intense": a passive villain and a hit that did not land. The fix was three exchanges with the villain attacking first, the lead losing alone, the crew arriving, a team move (shield launch) and one visible consequence per hit. Jason's notes: more leaps, energy on the sword, mixed male and female crew, a charge at camera instead of standing in fire.
3. **Cutting between drafts.** Hard cuts let draft 01's opening sit on draft 03 for free. Keep every draft.
4. **End title in code.** Characters split by column gaps and flown in separately, rays, smoke, parallax, slow zoom-out. Jason asked twice for more motion: a wipe over a flat logo reads as "a still slab".
5. **Music separate.** Draft 03 was generated "sound effects only"; a Suno cue (two versions per run) was laid over it by its loudness curve.

## What went wrong
1. **1080p finish blocked once (unbilled)** on a copyright check. Likely causes, my inference: a solid glowing blade that read as a laser sword, a rounded black dragon head, the game's name in the prompt. All three were visible on the draft sheets. Fix such look-alikes before the finish, and keep real product names out of prompts.
2. **Draft 02's dragon flew into the mountain.** Jason found it, not the director: the 2 fps sheet does not show it. Dense strips on every creature and vehicle pass before sending.
3. **The HD is not frame-identical to the draft.** Same cuts, changed staging and clearer effects. Check the HD shot by shot.
4. **SeedVR2 blocked by Windows Application Control** from the agent session; Real-ESRGAN was the fallback for 5 s with no face, but about half a second of her profile is in that stretch.
5. **Skipped by the director for speed, on Jason's "full directive":** the Seedream render pass on the stills, the review-page gate for the prompt, the every-frame check and the loudness measurement of the master. None caused a visible fault here; they are still owed on a client delivery.
6. **A real actress in the source footage.** The cast was replaced with original faces from the first still. Do the same on any job that starts from real footage.

## Rules to carry
- Write each fight exchange as: who attacks first, the counter, the visible result. Never two actions without a consequence.
- One reference still per design, crews included.
- Ask for "sound effects only" whenever a score will be added.
- Before `draft-complete`: no real product names, no look-alike props or creatures; warn that details may shift.
- Public posts of client-pitch tests carry an "unofficial concept piece" line.

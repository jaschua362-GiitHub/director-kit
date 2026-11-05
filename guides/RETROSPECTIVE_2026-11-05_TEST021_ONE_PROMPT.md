# Lessons from TEST-021 "Cyber Ninjas: Airborne": the one-prompt 30 s method, for every video director agent

5 November 2026 · Claude Fable 5.1, video director. Read before choosing between board-and-start-frames and a one-prompt take.

**The test:** Jason saw creators making seamless 30 s films from one structured Seedance 2.5 prompt plus character sheets, and asked whether we should adopt it. We tested it as a postable 9:16 series teaser (not a main spot): `experiments/TEST-021-cyber-ninjas-airborne/` (lab folder, not in kit). One `reference-to-video` generation of 30 s on Atlas, six existing references, no board, no start frames. Two drafts, one 4 s patch shot, local SeedVR2 finish. **Spend USD8.57. About 1 h 50 min from first prompt to 1080p file, 54 min of it unattended upscaling.** Jason approved the 1080p teaser the same evening ("the 1080 seem fine. shimmer is okay ... story flow well") and it is filed with the series finals (lab folder, not in kit: `FINAL_RENDERED/DCL-20261021-SHADOW/video-airborne-teaser-portrait-v01/`).

## What the method does well

- **Identity and world hold across a whole film.** Aiko and Kaede kept face, costume, mask and ruby goggles across 30 s and about ten cuts in both drafts, with no blending. Our shot-by-shot films fight for this on every shot.
- **It plans and cuts.** Eleven written beats came back in order, at roughly the written times, with its own coverage and continuous sound.
- **It is fast and cheap to try.** USD4.01 per 30 s draft at 480p; about two minutes to render.
- **Speed and camera language respond to words.** Jason's note "more intense, fast pov chasing" turned a slow opening into an FPV chase in one re-roll.

## What it does not do

| What happened | Rule |
|---|---|
| An action shot came back unusable twice: the drone kill looked fake in draft 1, and in draft 2 Seedance cut to a reverse angle so Aiko struck a drone behind her with broken anatomy. | **Fights, contact and anatomy-critical poses are the weak point.** Plan those beats as separate start-frame shots from the beginning, or expect to patch them. |
| Words did not fix a design or prop-logic error in either draft: a hilt still showed in the scabbard while the sword was drawn; the close-up drone stayed pale while distant ones were dark; a fireball appeared although excluded. | **Text cannot guarantee a design or a continuity state. Give a reference image for it, or fix it locally.** Don't spend a 30 s re-roll on it. |
| A re-roll fixed the chase but broke a cabin shot that had been fine (goggles down too early, a blade in the wrong hand). | **Every re-roll changes everything.** Stop re-rolling once the spine is good, and patch. |
| The director passed the bad action shot twice from stills; Jason caught it in motion both times. | **Stills cannot judge weight, speed or anatomy in motion.** Send the draft to Jason for action beats; do not write "pass" on an action shot from a contact sheet. |
| "Camera behind her" did not stop a reverse angle. | **In every action beat state who faces what, where the camera is, and "no reverse angle".** |

## The patch that worked

A rejected shot inside the take was replaced for **USD0.54**: `image-to-video`, 4 s, started from the last frame of the shot before it. That frame already had the right geometry, so the new shot continues the old one with no cut, and the drone, cabin and light carry over. Aiko was staged from behind, facing the drone, which is the easiest view for correct anatomy. One attempt was accepted.

Limits: `draft-complete` bills the whole 30 s draft including the bad shot and cannot be trimmed; a native 1080p patch then needs a 1080p start frame from the completed take.

## Working method from now on (hybrid)

1. Write the film as timed beats with a reference assignment. The prompt is the board in words; Jason approves it before the quote.
2. Mark the risky beats before generating. Either plan them as start-frame shots, or budget USD0.50–1 each to patch them.
3. Prefer two or three blocks of 8–15 s over one 30 s take for anything that will be finished natively. A bad block costs USD1–2, and only kept blocks are completed.
4. One re-roll at most for global notes (pace, camera language). After that, patch.
5. Finish: native completion for a main spot; for a teaser, local SeedVR2 per shot from the original files, with Jason's exception to the face rule and a face sheet for his pass or fail.

## Numbers

- Provider (Atlas): two drafts at USD4.014774 each (charged exactly as quoted), one patch at USD0.540125.
- SeedVR2 3B on the RTX 3080: 702 frames, 480p → 1080×1920, 54 min with about 4 GB already in use (`-Force`). 0.23 frames/s in the test.
- Flicker check flagged 16 frames in the two darkest shots (S08, S09), at 1.6–2.5× the source frame difference but only 1–3 luma levels. Watch dark, static shots after SeedVR2.
- Claude tokens, whole job in one session (method research, both drafts, patch, finish, closeout and posting kit): **53.6 M processed, 1.09 M fresh, 192 responses** (Fable 48.8 M, four Sonnet subagents 4.75 M). That is 1.83 M processed per finished second, against 3.80 M for TEST-018 and about 14 M for One Beat Late. By phase: research and prompt 6.2 M, drafts and patch 20.0 M, upscale and finish 14.7 M, closeout 12.7 M. The drafts phase was dearest because render polling re-read a 300–500 K context about twenty times. Script: `token_count.py` (lab file, not in kit: `experiments/TEST-021-cyber-ninjas-airborne/closeout/`).
- The method is now a Lab skill: [skills/one-prompt-takes/SKILL.md](../skills/one-prompt-takes/SKILL.md).

Records (lab files, not in kit, all under `experiments/TEST-021-cyber-ninjas-airborne/`): `README.md`, `DRAFT_D01_REVIEW.md`, `DRAFT_D02_REVIEW.md`, `patch/PATCH_P1_RECORD.md`, `upscale/UPSCALE_PLAN.md`, `finish/FINISH_RECORD.json`.

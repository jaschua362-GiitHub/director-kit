# Directing lessons from Film 7 "Himmapan — The First Welcome": for every video director agent

29 October 2026. Read after the Film 6 retrospective, before planning shots. Film: DCL-20261026-HIMMAPAN, approved final video-portrait-v01 (lab file, not in kit: `FINAL_RENDERED/DCL-20261026-HIMMAPAN/README.md`), 9:16, 32.6 s, wordless first-person POV. Directed by Claude Opus 5.5 in `experiments/TEST-016-himmapan/`, on ChatCut Desktop Seedance 2.5 within a 75-credit cap.

## The workflow that worked

1. **Rough monochrome hand-drawn board, locked before any photoreal frame.** The board took two sheet rounds: the first came back as painted colour, so the prompt now carries a hard "pencil sketch only" lock. Jason then asked for boards to be quick black-and-white thumbnails from now on (VIDEO_DIRECTOR_BRIEF §2026-10-27 item 5).
2. **Long continuous moves with hidden joins.** Jason asked for as few cuts as possible. The film is five generated moves joined behind real foreground: a wing, a crest, a wall of white mist.
3. **Mixed resolution for a small budget.** Native 1080p only where a face or the hero creature fills the frame (Niran's last look, the Naga reveal); everything else is 720p plus local Real-ESRGAN.
4. **Free local fixes before regenerating.** Three frozen elephants were painted out instead of regenerated. A trim kept the good half of a take that cut or glowed.

## What went wrong, and the rule

| What happened | Rule |
|---|---|
| Pilot T1: background residents and a far elephant **froze** while only the camera moved. Jason spotted it. | **Every visible creature, near and far, gets its own continuous action line in the prompt.** Tiny distant creatures freeze: make them big enough to animate, or leave them out. |
| A creature was still frozen after that, and Jason spotted it again ("the elephant also freeze"). | **Before review, crop-check every creature across the whole clip, and run a detector sweep over every frame, not samples.** A frozen sprite that goes out of focus slips past a sharp-template tracker. |
| C2b T1 froze ALL residents once the hero settled and the camera held still. | **No still holds in a generated take.** Keep the hero acting and the camera drifting to the last frame; build any hold or fade in the edit. |
| Pilot T2 and C1 cut mid-clip despite "single unbroken take". | **In reference mode, use one composition reference plus design-only references.** Each extra composition reference reads as a shot the model will cut to. |
| A model added an elephant that the prompt excluded, because the reference image showed one. | **The reference image beats the prompt.** Remove unwanted elements from the reference, or expect to paint them out. |
| The first wing join faded the wing out with a dissolve. Jason: "very visible… not professional". | **A foreground wipe must carry through.** Let the object keep travelling in its direction of motion and clear the lens; never dissolve it away. |
| Two continuous scores (v02) "killed all the different stages of surprise… too smoothing". | **Design sound by stages.** Silence and natural sound first; the score arrives at the climax only. A recurring cue at each key beat (here a soft gong at each touch) ties the story together. Mix with real dynamics: v03 loudness range 10.7 LU, against v01's 3.2. |
| Credits ran low; Jason: "the 2nd time we wasted on regen, so be careful". | **Pre-submit checklist on every paid take.** Prefer a free local fix. A retake carries every known fix at once, and its cost is stated first. |

## Technical notes

- **ChatCut Desktop must be open** for paid jobs: with the app closed, the confirmation auto-resolves to "Deny".
- **Open-H3-Regenerate-2K** (NVIDIA Sana) needs about 150 GB of GPU memory, Linux and landscape input. It is not usable on the desktop.
- **Generated music ignores timestamps** and returns full 3–4 min pieces. Pick a window by measured loudness fit, and land on the track's own natural ending.
- **A generated SFX can come back near-silent** (a drone peaked at −60 dB). Measure every generated stem before mixing it.
- **Frozen-sprite paint-out tools,** reusable: `experiments/TEST-016-himmapan/production/paint_out_sprite.py`. It takes a hand-drawn polygon mask, template-tracks the sprite with focus matching, and uses optical-flow tracking where the sprite goes soft.

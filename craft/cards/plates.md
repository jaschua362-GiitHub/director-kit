# Plates card

Read this when you start the plates stage. Required reading: `DIRECTOR_CRAFT.md`, the three every-session cards, this card and your handoff. The Lab keeps a longer depth file behind this card; it is not in the kit.

## What this stage is for
Plates are the still start and end frames each video take grows from; the take inherits everything in them. Jason: "So I do a lot of remedy on the still frame part, as much as possible before going video gen." House of Courtesy's "approved" plates then took ten notes, eleven batches and 230 M tokens, mostly on prop scale and design consistency.

## What good looks like
- A purpose-made frame per shot, neighbours derived from one hero plate, never "disjoint" (The Unstitched).
- The frames decide the motion; the prompt only nudges. A start still shows the moment before the action, never the action done (The Last Fritter B17).

## Look for
1. A recurring prop at one size and design in every plate, measured into `plates/SCALE.md`. House of Courtesy, on the tea-server: "we need decide how big".
2. Fixed props on the same side, depth and mount in every pair and shot, all three named in prompts; a close-up's object is in the next wide. House of Courtesy's column appeared at 17 s.
3. The opening frame, and every local cleanup at 4x: no prop through a hand, no smudge. House of Courtesy B9: six takes, about USD 7.
4. Start and end agree on every prop and gaze; end poses shift slightly. Hold the Note's shorter flute: USD 6.40.
5. Camera side and eyelines against the board. Hold the Note: three wrong rounds, a USD 7.54 retake.
6. Mechanisms as real physics; faces and mirrored makeup against the identity sheet. Wind the Man's hinge: ten reshoots.

## Let the script check
- Start/end pair difference: fixed things stay dark; a derived pair changes well under 20 %. `tool: tools/frame_pair_check.py`

## How this stage runs
- Before any design frame, he names one accepted image as the look authority; measure every frame against it before he sees it (`lab script, not in kit: look_measure.py`). The Last Ferry lost three look rounds before this was fixed. A mood reference refines his art; it never replaces its surface.
- Design plates (native ImageGen, layout only), then photo plates (a Seedream 5.5 Edit render). Only photo plates feed video.
- Make the end frame first, derive the start, one change per edit, made in the image (a fixed design frame or a paste-up as image 1), not in the words; if an edit won't take, move the camera.
- After design lock: one quoted batch with a retake reserve, one yes.
- Before he sees a plate: put each recurring character and prop beside its approved design and check size, count, side and shape. A general "what is wrong?" look misses delicate parts; a named comparison does not. Jason, 12 Nov: "maybe the AI can't really differentiate it is wrong." Then your 2x verdict, a fresh no-context Opus critic on every batch (on The Last Ferry it caught faults the director had passed in every round), board changes stated; send only plates you would approve.
- Sessions and models: the handoff card.

## Settled
- First frame only by default; a distinct end frame aligned to the start when a face or end state must be locked; never one plate at both ends.

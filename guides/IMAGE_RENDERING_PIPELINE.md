# Image rendering pipeline — adopted 7 November 2026 (Jason: "Adopt pipeline")

Target: photoreal cinematography for every film from Small Cargo onward. Evidence: `reviews/IMAGE_REALISM_ADVISOR_2026-11-07/claude-review/REVIEW.md`, the comparison in `days/2026-11-04-small-cargo/realism-compare-v09-DRAFT/FINDINGS.md` (USD 1.03, 23 images, three rounds) and the proposal `reviews/IMAGE_REALISM_ADVISOR_2026-11-07/claude-review/WORKFLOW_PROPOSAL.md`. Every director and preparation agent follows this; it does not change approval gates, spend caps or the frozen-approval rules.

## Principle

**7 November 2026, Jason's clarification.** For every newly selected creative, Codex makes the first base images here in native ImageGen. This includes the first character, environment and look anchors. Establish the film’s look from the brief and any explicit style direction before making the base. A later model-specific casting study is an optional, separately authorised experiment.

Use the approved Small Cargo v10 plates as a reference for how light and materials behave. For a new film, establish original characters and world design. When a benchmark has a person or a distinctive object in it, transfer its lighting and material behaviour in words. For a comparable still, describe the motivated key, shadow separation, neutral whites where appropriate, quiet local practicals and fine dust visible in the light. Use the film’s own palette and atmosphere. See the approved photo plates (lab file, not in kit: `approved/DCL-20261104-CARGO/photo-plates-v10/START_HERE.md`) and Codex wrap note (lab file, not in kit: `reviews/IMAGE_REALISM_ADVISOR_2026-11-07/NOTE_TO_CODEX.md`).

## Stages

| Stage | Tool | Output | Notes |
|---|---|---|---|
| 0 Look and first base images | Native ChatGPT/Codex ImageGen after creative selection | First character, environment and look anchors | Use the selected brief and any explicit style direction. Record the intended look for REQUIREMENTS_LOCK. Inspect identity, composition and motivated lighting before expanding. |
| 1 Design and layout | Native ChatGPT/Codex ImageGen | Character sheets, 9-view environment coverage, props, blocking, lighting direction and design lock | Use the film’s own identity anchors. Describe what is in frame, the material behaviour and where the light comes from. Judge the image as a design plate. |
| 2 Rendering pass | Seedream 5.5 Edit (USD 0.02 per frame) on every approved frame; MAI-Image 2.6 Edit (USD 0.09) first on clean-product scenes | photo plates | one pass per model, fixed order: MAI (materials, only when needed) -> Seedream (rendering, colour, air) -> Nano Banana 2.1 masked fix (only when needed) |
| 3 Measure | local crops and patches | approval evidence | 2x face and material crops; white-patch means on the same patches each time; drift checklist |
| 4 Video | Seedance via ChatCut or Atlas | takes | from the photo plates, never the design plates; test one shot in motion before propagating |

## Rendering prompt template (Seedream and MAI)

```text
Image 1 is a CG render of an approved design. Re-photograph it as a live-action film still, keeping [every design lock by name: who, age, wardrobe, props, counts, contacts, composition] and its lighting direction [say it, at this strength]. Change only the rendering: [two to four sentences on materials and air specific to this scene]. The fine surface pattern in image 1 is an artefact of that image, not part of the design. White balance neutral; [warm practical] warm only inside the lamp. Focus on [subject]; [far plane] softer. 16:9.
```

Short and positive. Never "pores", "skin texture", "photoreal", "grain", "lens", or a list of things not to do. Pores are for close-ups only. Request the model's 2K 16:9 tier (Seedream `2048*1152`).

## Rules

1. Keep native prompts short and concrete. Describe the scene, material hierarchy and light direction. In Small Cargo, repeated texture instructions and stacked edits left an etched pattern across distinct materials. Inspect that cue before expanding the image set.
2. Never more than two stacked edits in one model. A retake restarts from the design plate plus the anchors, not from the last output.
3. First anchors come from native ImageGen and follow the film’s declared look. The rendering pass conforms to that look and preserves the chosen identity. Small Cargo’s photographic finish and One Beat Late’s stylised anatomy serve different films.
4. FLUX is a camera for new frames (casting, look plates), never an editor of locked designs; with references it paints with them.
5. Seedream will not change materials on an already-clean frame; use MAI first for that, then Seedream to conform colour.
6. Upscalers, SeedVR2 and photo-cleanup are not still-realism tools; they sharpen the fingerprint. Video upscale rules in VIDEO_DIRECTOR_BRIEF are unchanged.
7. Approve at gates, quote in batches: design lock, then photo-plate approval, then video. One Atlas quote per batch, one confirmation from Jason. Outputs, prompts, prediction ids, hashes and actual spend go in the revision's `GENERATION.json`; failed draws stay in the folder.
8. The all-in-one daily session stays: the same Codex or Claude Code session that makes the design plates runs stage 2 as one scripted batch (upload, quote, submit, download, crop sheet, ask once).

## Atlas fields that exist (do not invent others)

- Seedream 5.5 Edit: `prompt`, `reference_images[1..10]`, `size`, `output_format`, `background`.
- MAI-Image 2.6 Edit: `prompt`, `reference_images[1..5]`, `size` default/auto.
- Nano Banana 2.1 Edit: `prompt`, `reference_images[1..14]`, `aspect_ratio`, `resolution` 1k/2k/4k, `seed`, `temperature`, `top_p`, mask per schema.
- FLUX.2 Pro Edit: `prompt`, `images[1..8]`.
- Inputs are uploaded through the Atlas upload URL; local paths are not accepted. Identical parameters submitted twice are merged into one job; vary the prompt for a second draw.

## Open questions for the next film (record the answer, then update this file)

- ANSWERED 2026-11-07 (`days/2026-11-04-small-cargo/motion-test-v11-DRAFT/FINDINGS.md`): Seedance keeps whatever surface prior it is given. The photo-plate take held tonal skin and distinct materials through a 5 s push-in; the design-plate take carried the native crackle and camouflage emboss in every frame. Rule: every Seedance start frame and reference image is a photo plate from the rendering pass, never a native design plate.
- Optional casting experiment, if separately authorised. Does a FLUX-born anchor survive the native design stage, or does the native route re-impose its texture?
- Can a FLUX look plate as a second Seedream reference (light and material role only) nudge a clean frame without drifting design?

# Crenature — logo intro (brief)

Route: **2.5D in code** (`motion-sting` skill engine + a glossy shading pass), chosen with `motion-design-advisor` §1. The dragon moves facing camera and resolves to a 3D-looking finish; no AI video and no paid generation.

## Locked decisions (2026-11-21)

| Item | Decision |
|---|---|
| Logo source | Google Drive `foundation-lock/` → `source/LOCKED-creature.png`, `source/LOCKED-wordmark.png` (1254 px PNG, no vector master) |
| Source hashes (sha256) | creature `91e55a37…0067`, wordmark `67284262…1ac` |
| Vectors | `traced/creature_glyphs.js` (ink body + eye), `traced/wordmark_glyphs.js` (9 letters + dot), traced with `trace_logo.py`, checked side by side in `stills/compare_*.png` |
| Format | 16:9 only, 1920×1080, 60 fps + 30 fps export |
| Duration | short intro, about 5 s (3.6 s story + 1.4 s hold) |
| Ending | dragon mark + `crenature` wordmark lockup, resolving to the **glossy 3D look** of `refs/final_look_3d.jpg` |
| Route | **2.5D in code** (approved): the dragon moves and coils facing camera, then inflates from flat ink to glossy 3D (height field + studio shading, `lookdev/glossy_test.py`). It never turns sideways. |
| Wordmark | **plain geometric sans like the reference** (replaces the locked custom wordmark for this piece), set from a real font, never traced from the reference. Font to propose at build: an OFL geometric sans (e.g. Outfit / Lexend / Sora); Inter Display is installed as a fallback |
| Eye | **glowing diamond eye** like the reference (a change from the locked almond eye). Colour: hot core `#FFBE77` → amber `#FB8F18` → red-orange edge `#CF5D1F` (reference measures mean `#CF5D1F`, core `#FFBE77`) |
| Palette | ink `#101010`, background soft studio grey (reference about `#EEECEA` centre to `#D8D6D4` edges), glossy black body with warm-white highlights |
| Saving | user approved pushing everything (incl. logo files) to the public repo branch, 2026-11-21 |
| Sound | synthesised, cued from the timeline (default; confirm) |
| Music | none |

## Story beats (mirror of `T` in sting.js)

Dragon leads (user request 2026-11-21). Times are a starting point; may stretch to about 6 s.

| t (s) | beat | sound cue |
|---|---|---|
| 0.0–0.4 | Empty studio field, slow push already moving. The diamond eye opens alone and glows. | low air bed, soft swell |
| 0.4–1.8 | The dragon flies in head first from off-screen as one flat, tapering ink body, sweeping a wide loop. | whoosh following its speed and position |
| 1.8–2.6 | It coils into the spiral and locks into the exact mark (tail last); horns flick up. | tightening tone, small click on lock |
| 2.6–3.0 | The head dips into the final pose; the body inflates from flat ink to glossy 3D, a light sweep runs across it, the floor shadow fades in. Blink + glint. | chime on the blink |
| 3.0–3.8 | The tail whips right; its sweep reveals the `crenature` wordmark. | rising notes per letter |
| 3.8–5.0 | Hold on the full lockup, still drifting slowly. | resolve chord to silence |

## Craft targets (from `references/craft-rules.md`)

- Final lockup sized like the reference (about 70 % of frame width), optically centred and measured. The kit default of 25 % is overridden by the approved reference.
- Lines are filled ribbons with C1-smooth joins; no decorative sparks.
- Motion blur on the delivered render; type drawn after the blur pass.
- Independent critic pass: every score ≥ 8 before the version is called final.

## Environment note

Built in a cloud session. Code, preview stills and the headless-Chrome export run here; nothing here needs your GPU. The container is temporary, so keep the project by committing it or by downloading the MP4s.

## Look development

- `stills/lookdev_board_v1.png`: A reference, B code glossy finish (v2), C flat start state. Shown to the user 2026-11-21.
- To do at build: more grey sheen on the big curve (closer to A), diamond eye, real-font wordmark.

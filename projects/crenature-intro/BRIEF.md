# Crenature — logo intro (brief)

Route: **2.5D in code** (`motion-sting` skill engine + a glossy shading pass), chosen with `motion-design-advisor` §1. The dragon moves facing camera and resolves to a 3D-looking finish; no AI video and no paid generation.

## Locked decisions (2026-11-21)

| Item | Decision |
|---|---|
| Logo master | **`source/identity/approved-white-lockup.svg`** (Drive, `2026-10-28-crenature-identity` work): true vector, arc-built dragon with diamond eye + the approved wordmark, one `<g data-letter>` per letter. Supersedes the traced PNGs |
| Look references | `refs/final_look_3d.jpg` (user, glossy black, horizontal), `source/identity/environment-endcard-light.png` (Drive, 3840x2160, same glossy black dragon, stacked), `source/identity/horizontal.png` (Drive, white matte 3D dragon on dark) |
| Earlier sources | `foundation-lock/` → `source/LOCKED-creature.png`, `source/LOCKED-wordmark.png` (1254 px PNG; older almond-eye / creature-c version, not used) |
| Source hashes (sha256) | creature `91e55a37…0067`, wordmark `67284262…1ac` |
| Vectors | `traced/creature_glyphs.js` (ink body + eye), `traced/wordmark_glyphs.js` (9 letters + dot), traced with `trace_logo.py`, checked side by side in `stills/compare_*.png` |
| Format | 16:9 only, 1920×1080, 60 fps + 30 fps export |
| Duration | short intro, about 5 s (3.6 s story + 1.4 s hold) |
| Ending | dragon mark + `crenature` wordmark lockup, resolving to the **glossy 3D look** of `refs/final_look_3d.jpg` |
| Route | **2.5D in code** (approved): the dragon moves and coils facing camera, then inflates from flat ink to glossy 3D (height field + studio shading, `lookdev/glossy_test.py`). It never turns sideways. |
| Wordmark | the **approved wordmark from the SVG master** (plain geometric sans with notched `e`/`r` details, as in the reference). No font needed |
| Eye | **diamond eye** from the SVG master, approved colour **`#FF6A24`**, with a glow (hot core about `#FFBE77`, as measured in the reference) |
| Palette | approved logo cream `#FFFDF7` (white lockup), ink `#101010` for the glossy black version, background soft studio grey (reference about `#EEECEA` centre to `#D8D6D4` edges), glossy black body with warm-white highlights |
| Saving | user approved pushing everything (incl. logo files) to the public repo branch, 2026-11-21 |
| Sound | synthesised, cued from the timeline (default; confirm) |
| Music | none |

## Direction change (2026-11-21, after v3)

Client note on v1-v3: "too toon-like in the action; the dragon animation looks like a cartoon ink worm, which loses the premium and edgy creative branding."
New direction (approved): **light carves the dragon**. The mark never bends or deforms; it is the rigid glossy 3D dragon from the first frame. Mood: **dark to light**.
Renderer: `build/render2.py` (v4+). `build/render.py` (flying-worm version, v1-v3) is kept for the record only.

| t (s) | beat (v4) | sound |
|---|---|---|
| 0.00-0.55 | Near-black. Tight close-up on the head; the amber eye opens and glows. | low air, breath swell, glass shimmer on the eye |
| 0.55-2.25 | A razor rim-light runs along the dragon from horns and head, down the neck, around the big coil, into the tail spiral, carving the glossy body out of the dark. The camera pulls back from the eye to the full mark. | metallic "blade" sweep following the light front |
| 2.30-2.70 | The studio lights rise: the black field flips to the warm off-white studio, the dragon stands in full glossy light, the floor shadow lands. | riser into a hard hit |
| 2.85-3.30 | `crenature` cuts in hard, letter by letter (crisp slices, no fades). | one crisp tick per letter |
| 3.30-5.60 | Hold: blink, then a light sweep and eye glint around 4.4 s; slow push. | blink chime, glint shimmer, low chord decaying to silence |

## Story beats (v1-v3, superseded)

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
- To do at build: rebuild the look from the SVG master (not the traced PNG), more grey sheen on the big curve (match `environment-endcard-light.png`), diamond eye.
- Note: the approved identity also has a white-on-dark version (`horizontal.png`). This intro uses the black-on-light look the user chose.

# Engine map — template/sting.js (the coffee-brand sting v5, working reference; v4 kept in the project's v4\)

One file, pure function of time: `render(t)` draws frame *t* on a 2D canvas. Same code serves the live
player, stills (`?t=3.5`), frame export (`?export=1`), the 9:16 cut (`?fmt=9x16`) and a logo-alignment
overlay (`?debug`, multiplies `src/logo_src.jpg` over the wordmark).

World space is always 1920×1080 design units; formats differ only by camera + backgrounds.

| Section (search for) | What it is | Reuse |
|---|---|---|
| `PORTRAIT`, `W/H/DUR/FPS` | format switch, duration | keep; add formats in the same pattern |
| `palette` `C`, `LINE` | brand colours | **replace per brand** |
| `helpers` `E` (easings), `ramp`, `rng` | easing library, colour ramps, seeded RNG | keep |
| `grain` | dither pattern (α .025 in `render`) | keep |
| `blob`, `glowDot` | soft radial light, glowing dot | keep |
| `timeline` `T` | every beat's [start, end] — the single source of truth (sound cues mirror it) | **rewrite per story** |
| `camera` `ZK`, `hermiteKeys`, `camera()` | per-scene zoom keys + drift (drift settles in 9:16 hold) | keep, retune keys |
| `wordmark` `WM`, `wmS`, `G()` | traced glyphs placement + settle scale | keep; map glyph ids |
| `cup icon geometry` `ICON`, `leafTop/leafBot`, `cupState`, `withCup` | brand icon rebuilt as exact geometry | **per brand** |
| `bean` … `crackBurst`, `seed`, `heatRings`, `crease` | the coffee brand scene beats | examples of the patterns below |
| `LINES`, `gX/gY`, `GV/TS/LWS` | data lines (value fns), graph frame, portrait stretch/type/line scale | pattern |
| `proj`, `SNAKE`, `headOf`, `pathPt` | **snake path**: σ∈[0,3] graph → 3D swoop (bezier + sin² depth/twist) → ring | **key pattern** for "lines become shapes" |
| `ribbon`, `lines3D` | **filled variable-width ribbons**, taper, front/back runs | **key pattern** for all hero lines |
| `graphFrame` | axis, ticks, event labels, area fill | pattern |
| `cup + latte art` | pour stream, bloom mask, pull-through cut | pattern for "liquid draws the mark" |
| `wordmark()` | whole-glyph builds (letters), tracking-in (tagline); v4's radial sweep + masked rise read as shards | keep |
| `portrait layout` `PS`, `layoutFocus`, `OPT`, `darkBGP/lightBGP` | 9:16 scale keys, tip-tracking camera with lead room, cup-group shift, optical-centre offset, screen-space backgrounds | keep, retune |
| `render()` | draw order: bg → wipe → back lines → scene → front lines → wordmark → dither | keep |
| `motion blur` `renderMB` | export frame = average of `sub` sub-frames over the shutter (`?export=1&sub=4&shutter=.5`); sub-frames render with `TEXT='none'`, then type is drawn once, sharp, with `render(t, f, 'only')` | keep |
| `TEXT` guards in `graphFrame` / `lines3D` | which draws are type (`!== 'none'`) vs geometry (`!== 'only'`) — add the same guards to any new label | keep |
| `wipeFeather`, `lightLayer` | colour wipe on an offscreen layer, radial-gradient mask feathered by edge speed (capped 40 px); `ctx` is `let` for this swap | keep for any fast reveal edge |
| `zoomAt` (explicit after 6.45 s) | logo phase: pull out while the cup lands, then constant-speed push to the last frame (no Hermite turnaround in the hold) | keep, retune times |
| `holdLight` | warm light sweeping behind the end lock (large-area motion; the logo alone reads as near-still) | keep |
| `targetRings`, seed ring pulses | hook: rings + pulses + glow on frame 0 (frame 0 is the Reels thumbnail) | pattern |
| `wordmark()` `build` | whole-glyph letter build (fade + scale from own centre + short rise) — approved by Jason v5 | keep |
| `pathPt` lift / `hf` head taper | swoop: lines rise into wide nested U-turns; the head thins to nothing inside its turn (no J) — Jason's v5 choice | keep |
| `modes` | `?t=`, `?export=1`, `?debug`, keyboard player | keep |

## Patterns worth lifting into any new sting
1. **Snake path** — any line that must travel and become a shape: define one parametric route,
   draw the window [head−1, head]; head eased 1→3. Continuous by construction.
2. **Ribbon renderer** — offsets ± half-width along normals, filled once; width fn per point gives
   taper and perspective thickness for free.
3. **sin² bumps** — any temporary offset (depth, twist, pull) that must start and end invisibly.
4. **Hermite keyframes** — camera zoom/scale keys with continuous velocity.
5. **Morph via shared geometry** — bean ellipse rx/ry → cup radius; circle wipe radius = a ring's radius.
6. **Masked reveals** for type; radial-sweep clip for round letters.

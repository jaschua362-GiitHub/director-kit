# Craft rules — Jason's standards, learned on the coffee-brand sting (Sep 2026)

Each rule cost a feedback round once. Build v1 to these and the first review starts at "polish".

## Brief & concept
- **Borrow the reference's language, not its colours.** Didomi → glowing dot + trailing hairline,
  wireframe ring fans, concentric circles, soft gradients. Rendered in the client's own palette.
- **Narrate in brand symbols.** For a roaster: seed → bean → roast → cup → logo. The logo's own
  shapes are the payoff (the coffee brand's yellow leaf-halves = bean *and* latte art).
- **No black** on the coffee brand work — darkest is espresso brown. Brand colours come from their files
  (`<PROJECTS>\<Brand>\Social\2026-07 July menu\source-portrait.html`), never guessed.

## Motion
- **Nothing ever freezes.** Keyframed per-scene zoom (Hermite keys, alternate in/out, ~5–15%),
  plus a tiny drift (±7 px, ±0.25°). A barely-perceptible push was rejected — it must be visible.
- **Lines are one continuous path.** Each travelling line is a "snake" whose body is always the last
  N units of a single route (graph → 3D swoop → ring). Never blend between separate states — it tangles.
- **Joins are C1-smooth.** Leave a curve along its own tangent; arrive on a circle along the circle's
  direction; depth/twist offsets use sin² bumps (zero value *and* zero slope at both ends).
- **No hairpins; wide U-turns.** Enter a ring in the direction the line is already travelling; give
  the longest-travelling line a wider turn.
- **Taper ends while travelling;** fade the taper to 0 as the shape closes so the final ring is even.
- **No decorative head sparks** on travelling lines — read as clutter.
- **Finish morphs before lines land on them** (bean → circle done before rings arrive).
- **Depth sells 3D:** perspective-scale width (and slightly brightness) by projected depth.

## Rendering
- **Lines = filled ribbons** (variable-width polygon), never chunked strokes — chunks show joints,
  beads (round caps under alpha) and ticks at pass switches.
- **Front/back switching happens once, off-screen** (e.g. at the graph's end), not per segment.
- **No visible grain.** Dither only (overlay noise α ≈ 0.025) to stop gradient banding in H.264.
  If a gradient still bands, go flat colour — Jason prefers flat over grainy.
- Soft halo/glow on lines: keep subtle (α ≈ 0.1); on dark brown it can read as a shadow.
- **Motion blur on every delivered render** (`render.py` default `--sub 4`, 180° shutter). Fast moves
  (wipes, swoops, the camera) strobe without it; static content stays sharp. Added Oct 2026.
- **Type is never motion-blurred.** Sub-frame blur ghosts fast thin text into 3-4 copies (more sub-frames
  made it worse). Draw labels in a separate pass over the averaged frame (v5 engine: `render(t, f, 'only')`
  after `renderMB`'s average; sub-frames render with `'none'`).
- **Very fast large edges need an analytic feather.** A wipe moving ~100 px/frame bands into hard rings
  under sub-frame blur; mask it with a radial gradient whose width = edge speed x shutter (v5 `lightLayer`).
- **Measure the hold, don't trust the keys.** Hermite scale keys can bulge after the last move and sink
  back through the hold, cancelling the push (v5 9:16: 4% instead of 12%). Measure the end lock's width
  at 8 / 9 / 10 s with `TOOLS.measure`; it must keep changing ~5%/s to read as alive. The review pack's
  near-still metric under-reads a small logo on a flat background; a slow light sweep behind it helps both.
- **Lines that reverse direction:** tune the turn offline against the frame edges for both formats
  (9:16 at a wide pull needs ~2x taller turns). A head inside its turn always reads as a J for a few frames.

## Logo resolve
- **Hold ≥ 2 s** on the finished logo (8 s story + 2 s hold = 10 s), still slowly moving.
- **Settle, don't fill.** 16:9 final ≈ 25% of frame width (v1 at ~50% was "too huge").
  9:16 final ≈ 50% of frame width.
- **Build while settling:** letters reveal while the lockup scales down to its final size.
- **Optical centring, verified by measurement** (`TOOLS.measure`), not by bounding box:
  centre on visual weight (heavy rows pull the eye), lift ~2% of H above centre in 9:16, settle
  pan drift to 0 during the hold. Same for grouped icons (cup + handle is one unit).
- Screenshots from a video player may be cropped by its controls — measure the rendered frame.

## Vertical (9:16) cut
- **Don't shrink wide scenes to fit.** Zoom out only enough to feel full, stretch graphs vertically
  (×2–2.5), and **track the action with the camera** (lead room: moving tip held ~70% across).
- Type ×1.6, lines ×1.4 for phone legibility. Keep labels clear of the frame edges.
- Backgrounds laid out in screen space (no bands top/bottom); anything "from the sky" starts above
  the taller frame; camera eases back to centre for the logo.
- Clarify "16x9 vs 9x16" once if the request is ambiguous — Jason said 16x9 meaning vertical.

## Sound
- Synthesised, cued from the engine's own timeline; one key (the coffee brand: D major).
- Movement → filtered-noise whoosh whose loudness = the element's speed, pan = its x; closeness → brighter.
- Closing/landing moments → chimes; letters → rising marimba notes; resolve chord carries the hold to silence.
- Make a concept audible when it's cheap (roast curves sonified) — "interesting" beats generic.
- −14 LUFS, peak −1.5 dBFS; watch the low end in dense sections. Verified by spectrogram — say so; he
  listens on headphones.

## Captions
- The motion is a **brand metaphor**, not a tutorial. Lead with brand essence (the coffee brand: farm-direct
  organic green from partner farms, roasting craft, gratitude to supporters), then shop link + hashtags.
- EN + TH versions. Flag claims that need backing (e.g. "organic" = certified?).

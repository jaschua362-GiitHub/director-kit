# Real footage in a code-built film

Pattern from the "high-end product video" prompt (Opus 5.5 prompt collection, Oct 2026), built into the
engine so any sting, brew guide or business film can cut real clips without losing determinism.

## Pipeline
1. **Pick moments** with a contact sheet: `ffmpeg -i clip.mp4 -vf "fps=2,scale=160:-2,tile=12x4" sheet.png`
   (frame k = start + k/2 s). Write `clips.json`: `[{"id", "src", "in", "out"}]` in clip seconds.
2. **Extract**: `python scripts/extract_clips.py --project <p> [--fps 30] [--max 1080]` → `footage/<id>/f_00001.jpg…`
   + `footage/manifest.json`. JPEG sequences, not `<video>`: video seeking is async and approximate.
3. **Draw**: include `footage.js`; `await FOOT.init()` at boot; before each export frame
   `await FOOT.prepare([{id, t}, …])` for every sub-frame time; inside `render(t)` call
   `FOOT.draw(ctx, id, clipT, x, y, w, h, {fx, fy, r, alpha})` (cover-fit, focus point, rounded clip).
   Expose `window.beforeRender = t => …prepare…` so `TOOLS.still/sheet` decode first.
4. **Check** with `scripts/stills.py` (headless). The preview pane defers image decoding while hidden, so
   in-pane sheets hang on footage projects.

## Craft rules
- A clip plays at natural speed; never stretch below ~0.6× (reads as accidental slow-motion); hold the last
  frame instead. A slow push (≈5% over the shot) keeps held frames alive.
- Cut on story beats (a pour starting, a step changing); dissolve ≤ 0.2 s between shots of the same scene.
- **Match cuts:** measure positions at runtime (e.g. the dripper's rim in both shots) rather than guessing.
- Do not set opacity/filter on a 3D (preserve-3d) element; fade its wrapper (HTML/CSS builds).
- **Sound effects from files:** `python audio/place_sfx.py cues.json out.wav --dur <s>` puts each file's
  measured PEAK on its event (a whoosh peaks 0.2-0.5 s after its start; placing by file start feels late).
  Then `audio/mix.py` with music → -14 LUFS.
- **Rights:** only his footage or licensed footage; record the source in BRIEF.md. Commercial-use licences
  for music/SFX.

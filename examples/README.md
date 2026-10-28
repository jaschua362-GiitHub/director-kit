# Examples

Real scripts from two finished films. They show how each step was actually done. Their paths, take IDs and file names belong to those films, so read and adapt them; they will not run as-is.

## film6-shadow — The Shadow Apprentice (9:16, 58.9 s, Seedance 2.5 + ChatCut)

| File | Pattern |
|---|---|
| `build_drawn_board.py`, `build_storyboard.py`, `build_photo_board.py` | Contact-sheet boards: drawn first, photoreal after the lock |
| `startframes/make_locked_jobs.py` | Turn a locked board into image jobs (JOBS.json + prompts) |
| `assemble_final.py` (+ `assemble_v02.py`, `hud.py`) | Frame-exact 24 fps assembly; MKV intermediates; designed machine-POV HUD |
| `music/make_bed.py` | Ambience/music bed under the whole film |
| `finish/grade_plates.py`, `finish/upres_all.py` | Per-shot grade and local upscale driver |
| `finish/chatcut_call.py` | Calling ChatCut's MCP launcher from a script |
| `title/make_kanji_matte.py`, `title/codex-v02-DRAFT/*.mjs`, `title/blade-dance-16x9/render_layers.mjs` | HTML/JS title rendered frame-by-frame with Playwright, and a render verifier |
| `closeout/package_social_materials.py` | Title clip, poster, stills and captions for the final folder |

## film4-wind — Wind the Man (16:9 + 9:16, Seedance 2.5 + MiniMax H3)

| File | Pattern |
|---|---|
| `look.py`, `grade.py`, `luma_report.py` | Look preset and measured grade (faces, highlights, blacks) |
| `title_slam.py` | Title slam with synced hit |
| `gem_sfx.py` | Procedural SFX cue |
| `vertical_preview.py`, `vertical_finish.py` | 9:16 reframe: real-time preview first, then the finish |
| `sheet.py` | Frame contact sheet for review |
| `vace_fill.py` | Wan VACE fill experiment (needs the `wan` package; advanced) |

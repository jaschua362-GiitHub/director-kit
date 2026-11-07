# Examples

Real scripts from six finished films. They show how each step was actually done. Their paths, take IDs and file names belong to those films, so read and adapt them; they will not run as-is. `<LAB>` in a script stands for the original lab root, and the bundled ffmpeg path (`experiments/TEST-001/tools/python-media/...`) is the lab's own ffmpeg build: substitute yours.

## hold-the-note — Hold the Note (16:9 and 9:16, 49.6 s, Korean dialogue, Atlas Seedance 2.5, November 2026)

The most complete workflow. Read with [guides/GUARDRAILS_HOLD_THE_NOTE.md](../guides/GUARDRAILS_HOLD_THE_NOTE.md), [guides/RETROSPECTIVE_2026-11-06_TEST020.md](../guides/RETROSPECTIVE_2026-11-06_TEST020.md) and [guides/PIPELINE_SIMULATION_2026-11-07_TEST020.md](../guides/PIPELINE_SIMULATION_2026-11-07_TEST020.md).

| File | Pattern |
|---|---|
| `effects/grain_fx.py` | Physics-based local effects (gravity, shutter, wind), deterministic, tested on clean plates and approved before production |
| `production/p4_atlas/build_requests.py` | A batch of Atlas image-to-video requests: camera side and look direction written into every prompt, first + last frame per face shot |
| `production/finish/make_finish_edl.py` | A frozen finish EDL that every build step (picture, mix, subtitles, title) reads; take frames, source offsets and the route per shot |
| `production/finish/face_sheet.py` | 100 % face crops, upscaled against draft, same frame, on one sheet: the face audit |
| `production/finish/flute_track.py` | Phase-correlation tracking of a prop across every frame of the HD file, to catch a slow morph the eye misses |
| `production/finish/build_04V_reframe.py` | The 9:16 shot as a crop of the approved 16:9 take (free), with the same grade |
| `production/finish/epigraph_overlay.py` | A hand-set text overlay (vertical column plus English line) with an opacity schedule, never image-model lettering |
| `closeout/make_poster.py` | Posters from a text-free plate with the approved title art set by hand (SVG paths), two variants, eyes open |

## one-beat-late — One Beat Late (16:9, 34.5 s, wordless, Atlas Seedance 2.5, November 2026)

Read with the [pilot](../guides/RETROSPECTIVE_2026-11-03_TEST019_PILOT.md) and [phase 3](../guides/RETROSPECTIVE_2026-11-05_TEST019_PHASE3.md) retrospectives.

| File | Pattern |
|---|---|
| `pilot/composite/insert.py` | Insert + cut: animate a still locally (eased push, protected reflections, per-frame grain) instead of patching a moving subject |
| `production/stills/build_visual_board.py` | The visual board: each locked board panel beside the frames that will drive it, for approval before any video spend |
| `production/video/build_face_prompts.py` | First + last frame prompts for face shots: continuity block, living background, restaged wides after notes |
| `production/edit/build_music_edit.py` | Picture conformed to measured beats; a tune delayed by two beats to make the concept audible; fade and black timed with the music |
| `production/music/analyze_music.py` | Measure a generated music take before using it: tempo, stability, beat phase, per-bar loudness, the natural ending |
| `production/sound/design_sfx.py` | Locally designed SFX family (one arrival hiss reused, room tones, ticks), deterministic |
| `production/sound/build_sound_mix.py` | Cues placed from the EDL so they stay in sync as cut; native, designed and music layers; two-pass loudness |
| `production/finish/build_final_1080.py` | 1080p assembly on the approved EDL, then grade, fade, encode, mux; `-fps_mode passthrough` on frame-exact pipes |
| `production/finish/every_frame.py` | Every-frame check of a 1080p composite against its accepted 480p version, with per-frame structure correlation |
| `production/finish/measure.py` | Per-event luma of the delivered file (faces, highlights, blacks) plus a still per event |
| `production/finish/verify_final.py` | Delivery checks: streams, every frame decodes, audio alignment and loudness, timing against the approved cut, approved-file hashes |
| `closeout/package_final_delivery.py` | Final folder with social materials, idempotent, re-verifies hashes |

## airborne — Cyber Ninjas: Airborne (9:16, one-prompt 30 s teaser, Atlas Seedance 2.5, November 2026)

| File | Pattern |
|---|---|
| `finish/checks.py` | Pre-assembly checks: frame counts, dark-frame guard, flicker, per-shot luma |
| `finish/skin_measure.py` | Skin luma on named face boxes, before and after upscale |

## evade-and-escape — Cyber Ninjas: Evade and Escape (9:16, 27.9 s, Atlas Seedance 2.5, November 2026)

| File | Pattern |
|---|---|
| `assemble_draft_edit_v04.py` | A draft edit rebuilt as single-action shots after identities blended in a dense fight shot, with the series end tag |

## film7-himmapan — Himmapan: The First Welcome (9:16, 32.6 s, ChatCut Seedance 2.5, October 2026)

| File | Pattern |
|---|---|
| `paint_out_sprite.py` | Paint a frozen background creature out of a take: template tracking with focus matching, one inpaint placed in every frame |

## film6-shadow — The Shadow Apprentice (9:16, 58.9 s, Seedance 2.5 + ChatCut, October 2026)

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

## film4-wind — Wind the Man (16:9 + 9:16, Seedance 2.5 + MiniMax H3, October 2026)

| File | Pattern |
|---|---|
| `look.py`, `grade.py`, `luma_report.py` | Look preset and measured grade (faces, highlights, blacks) |
| `title_slam.py` | Title slam with synced hit |
| `gem_sfx.py` | Procedural SFX cue |
| `vertical_preview.py`, `vertical_finish.py` | 9:16 reframe: real-time preview first, then the finish |
| `sheet.py` | Frame contact sheet for review |
| `vace_fill.py` | Wan VACE fill experiment (needs the `wan` package; advanced) |

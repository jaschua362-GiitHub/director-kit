---
name: motion-sting
description: Design and produce a short brand motion graphic (logo sting / brand reel / animated logo reveal) end to end — reference study, logo vectorisation, a code-driven canvas animation engine, 16:9 + 9:16 exports, synced procedural sound design, and the social caption. Use whenever the user asks to animate a logo, make a motion graphic / motion design / brand video / sting / intro / outro / reel "in the style of" a Behance/Vimeo/Dribbble reference, to make a vertical or square cut of an animation, to add sound design to one, or to start "a new similar motion project" — even if they don't say "sting". Built from the coffee-brand logo sting (Sep 2026).
---

# Motion sting

A deterministic canvas engine (`render(t)` is a pure function of time) previewed live in the browser
pane, exported frame-exact by headless Chrome, encoded with ffmpeg, with sound synthesised from the same
timeline. The reference project is the coffee-brand sting:
`<PROJECTS>\<Brand>\Motion\logo-sting-8s\` (10 s, v5, 16:9 + 9:16, with sound; passed the critic gate
in 8 rounds — `review_log.md` there shows what each critic caught).

`<SKILL>` = this skill's own folder.

**Read `references/craft-rules.md` before designing anything.** It is Jason's standard, distilled from
four feedback rounds; v1 should already meet it. `references/engine-map.md` says where every pattern
lives in `template/sting.js`.

**Effort:** run a new sting at **xhigh** effort (**max** for a flagship/launch piece); medium is enough for
re-renders and small fixes. If the session is lower, say so in one line before starting a new film.

## 0 · Kickoff — one round of questions, then work
Ask only what can't be defaulted (AskUserQuestion, one batch):
- Formats → default **both** 16:9 (1920×1080) and 9:16 (1080×1920). If he writes "16x9" but talks
  about fitting a wide graph into a frame, he means 9:16 — confirm in one line.
- Duration → default **8 s story + 2 s logo hold**.
- Sound → default yes, synthesised. If he supplies a **music track**, the picture is cut to it (step 7b).
  Caption → default EN + TH, brand-essence led.
- Logo source → ask for a **vector (SVG/AI/PDF)** first; else the largest raster.
Everything else (palette, fonts, brand rules) comes from the brain + brand files, not questions.
Brand/business context: read the brand's brief and guidelines first.

## 1 · Study the reference (≈10 min)
Open the link in the browser pane; collect every project image into one grid (inject a CSS grid of the
page's `project_modules` images and screenshot it). Write down the **visual language** (e.g. glowing dot
+ hairline trail, wireframe ring fans, concentric circles, soft gradient fields) — not the colours.

**If the reference is a video** (file or downloadable link), study its timing too, not only its look:
```
ffmpeg -i ref.mp4 -vf "fps=2,scale=320:-2,tile=6x5" refs/ref_sheet_%02d.png     # 1 frame per 0.5 s
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"   # cut times
```
Write `refs/style_guide.md`: palette (hex), type (family, weight, tracking), shot lengths (from the cut
times), transition types, camera moves, how text enters and exits, texture. Take the **grammar, never
the content** (no logos, characters, layouts). Show Jason the style guide in 5–8 lines and wait for his
OK before any code — it is cheaper to correct a misread here than after the build.

## 2 · Scaffold + brand assets
```
python <SKILL>/scripts/new_project.py --dest "<PROJECTS>/<Brand>/Motion/<idea-name>"
python <SKILL>/scripts/trace_logo.py <logo.png> --palette brown=#... olive=#... --out <project>/glyphs.js
```
- `trace_logo.py` uses colour unmixing (no anti-alias halos), groups glyphs into rows, writes
  `glyphs_preview.svg` labelled with ids → map ids to letters in the scene code.
- Rebuild simple geometric marks (circles, cups, leaves) as exact geometry; confirm alignment with
  `?debug` (multiply overlay of the original — misalignment shows as double edges).
- Project gets a preview entry in `<workspace>/.claude/launch.json` → `preview_start` by that name.

## 3 · Storyboard
Write beats as brand symbols with times into `BRIEF.md` and `T` in `sting.js`. Show Jason the beat
list in 5–8 lines before building if the concept is new; skip if he has already given the story.

## 4 · Build
Adapt `sting.js`: palette `C`, timeline `T`, scene functions, `ZK` zoom keys, wordmark mapping, portrait
`PS` keys. Keep the engine's patterns (snake paths, ribbons, sin² bumps, Hermite camera, masked reveals).

**Real footage** (his clips inside the film): follow `references/footage.md` — `scripts/extract_clips.py` →
`template/footage.js` (frame-exact image sequences), `audio/place_sfx.py` for file-based effects.
**Recipe / brew-guide videos** have their own skill (a brew-guide skill, not included in this kit).
**Worked example (one brand, not a rule):** that brand's 2026 spots all end on a shared season end card — `<PROJECTS>\<Brand>\Motion\end-card-2026\`
(README = entry spec + rules; play untouched at 60 fps).
**AI-generated live action** (photoreal people/product shot by Seedance etc., cut to music, ending on a sting): follow
`references/genai-live-action.md` — defaults from Jason's feedback, ChatCut driving + costs, realism prompts,
compositing real labels, beat-cut edit template `scripts/genai_assemble_template.py` (+ `audio/foley_template.py`),
and the rule that the approved sting plays untouched at 60 fps.

## 5 · Self-check loop (while building)
In the browser pane on `http://localhost:<port>/?t=0` (and `?fmt=9x16&t=0`), javascript tool:
```
await TOOLS.sheet([ ...beat times... ], 'beats', {cross: true})   // → <project>/stills/beats.png
await TOOLS.still(3.5, 'crack')                                     // full-res frame
TOOLS.measure(9.99)                                                 // final logo: margins + weight offset
```
Read the PNGs. Check against craft-rules: continuity of lines, joins, no freezes, framing in 9:16,
final logo optically centred (weight offset ≈ 0, lift in 9:16). `TOOLS.still(t, name, {sub: 8})` shows a
frame with export motion blur, for judging smear on fast moves.
If the preview pane is hidden (or the project draws footage), use `python <SKILL>/scripts/stills.py --project <p>
--times … [--fmt 9x16]` instead: headless, exact, and it does not hang on image decoding.
This is the builder's check only — it does not replace the critic in step 6b. Don't screenshot the pane — it times out;
stills via `TOOLS` are exact and full resolution. Tell Jason what you're checking in one line while
the loop runs; he likes progress notes.

## 6 · Export (one command per cut)
```
python <SKILL>/scripts/render.py --project <project> --name <Brand>_Sting_10s_v1 --fmt 16x9 9x16 --dur 10 [--audio audio/sfx.wav] [--prores] [--sub 1]
```
**Motion blur is on by default** (`--sub 4`: 4 sub-frames averaged per frame over a 180° shutter, done in
the page before each PNG). It removes the strobing of fast code motion; static content stays sharp. ~3.6×
slower (10 s 16:9: 75 s → 270 s). Use `--sub 1` for drafts inside the critic loop, the default for
anything Jason sees. Projects scaffolded before Oct 2026 lack `renderMB` — `render.py` warns and exports
unblurred; copy the motion-blur block + export loop from `template/sting.js` to upgrade them.
Starts its own server on a free port, headless Chrome (unthrottled — never export via the pane),
encodes 60 + 30 fps H.264 (libx264 → libopenh264 fallback) and optional ProRes 422 HQ, muxes audio,
cleans frames, kills Chrome. Move superseded versions into `vN/`.

## 6b · Independent critic (gate before every version Jason sees)
Follow `references/critic.md`: `scripts/review_pack.py` builds the evidence from the MP4 (contact sheet,
360 px phone sheet, frame strips at the fastest moments, near-still stretches, loudness), then a **fresh**
critic agent scores 7 criteria 1–10 into `<project>/review_log.md`. Ship at **every score ≥ 8**; otherwise
fix its 3 biggest problems and run a new critic. Report scores to Jason in one line per round.

## 7 · Sound (synthesised)
Copy the beat times from `T` into `audio/cues.py` (starts as the coffee-brand example), then:
```
python audio/cues.py                     # seconds, not minutes
python <SKILL>/audio/audio_check.py audio/<sfx>.wav --sections 0:2:intro ...
```
Read the spectrogram + RMS table: cues on their beats, energy follows the story, low end under control.
Then re-run `render.py … --audio`. Say plainly that the mix was verified visually, not by ear.

## 7b · Supplied music → cut the picture to it
```
python <SKILL>/audio/beats.py audio/track.wav > audio/beats.json      # any format ffmpeg reads
```
`beats.json`: `bpm`, `beats` (state changes), `downbeats` (big moments: cuts, landings, logo lock),
`hits` (strong onsets → SFX accents). Build `T` from these numbers instead of round seconds; start the
story on a downbeat and land the logo on one. Tested to ~2 ms on steady-tempo music (60–180 BPM); it
does not follow tempo changes. Checks: the tempo it prints is plausible (a WARNING means half/double is
ambiguous → tap along, re-run with `--bpm`); the **bar phase is a guess** from kick energy — confirm a
bar-1 by ear or spectrogram and pass `--downbeat <sec>` if it is off.
SFX are then sparse accents under the music (synthesised as in step 7, cued on `hits`/`downbeats`). Mix:
```
python <SKILL>/audio/mix.py audio/track.wav audio/sfx.wav audio/mix.wav [--sfx-db -4]
```
(measured gain + true-peak limiter → −14 LUFS / ≤ −1.5 dBTP; single-pass `loudnorm` misses by ~3 LU on
short files) and pass `--audio audio/mix.wav` to `render.py`. Music licence: ask Jason where the track is from and
note it in `BRIEF.md`.

## 8 · Deliver
- Only after the critic gate (6b) passes. Send the final scores + `review/…/contact.png` with the film.
- `SendUserFile` the 60 fps MP4 (render) after each version; name files `<Brand>_<Piece>_<dur>_v<N>_<WxH>_<fps>[_sound]`.
- Caption per craft-rules (brand essence, not a literal explanation of the animation; EN + TH; link +
  hashtags; flag claims needing proof). Save to the brand's `Social\<YYYY-MM> <piece>\caption.md`.
- Log each version in the project notes (what changed, where the files are).
- Nothing is posted without Jason.

## Known environment facts (this desktop)
- ffmpeg lacks libx264; NVENC driver too old → libopenh264 @ 30 Mb/s (visually clean). ProRes works.
- The console code page may not be UTF-8 (e.g. cp874): keep script `print` output ASCII.
- Python 3.14 with numpy, scipy, pillow, potracer installed; node 24; Chrome at the default path.

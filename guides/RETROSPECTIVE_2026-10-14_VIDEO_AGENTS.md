# Three films, one lesson set: video-agent retrospective

2026-10-14, local time. Written by the film-3 video agent (Claude Code, claude-opus-5-5) at Jason's request, so the next video agent starts from everything films 1–3 learned. Read this after verifying the approved packet, before planning shots.

> **Jason on film 3:** "after 3 round this was the most well done spot despite the 1st round was a failure. i allow you to open up n increase duration and you did a very good job expanding the still frame into a emotional well acted spot."

| Film | Project | Video agent / route | Result | Evidence |
|---|---|---|---|---|
| 1 | The Tide Remembers (DCL-20261012-TIDE) | GPT-6.1 in Codex; ChatCut Desktop, Seedance 2.5 | 10 s. Approved v04 after 4 fix rounds | `RETROSPECTIVE_2026-10-12.md`, `experiments/TEST-001…006` |
| 2 | Solar Etiquette (DCL-20261013-SOLAR) | Opus 5.5 in Claude Code; ChatCut Desktop via computer use, Seedance 2.5 | 10 s, 2 shots. Approved v05 after 5 revisions | `experiments/TEST-007` |
| 3 | The Unstitched (DCL-20261014-WEFT) | Opus 5.5 in Claude Code; **ChatCut hosted MCP plugin**, Seedance 2.5 | **25 s, 7 shots, music.** Approved v04 master + 9:16 | `experiments/TEST-008` (failed baseline), `experiments/TEST-009` (director cut) |

## 1. How each film failed first, and what it taught

- **Film 1: the physics was undefined, then patched.**
  - The prompt never defined the water medium, the bubble origin or the listener perspective.
  - The fixes were cosmetic (crop, tint, overlays), and Jason rejected them.
  - A source-video regeneration finally fixed it.
  - **Lesson:** classify the defect before choosing the fix. Dynamics need regeneration; a grade or crop never fixes motion.
- **Film 2: the keyframes overruled the prompt.**
  - Start and end frames came from separate edits, so their backgrounds ghosted.
  - The end frame pinned the cars' direction, so they flew backwards.
  - The end pose locked the women's eyeline away from the fan.
  - **Lesson:** design motion, eyelines and direction into the keyframes. PLAYBOOK §8 has the keyframe-first rules.
- **Film 3, round 1: overcorrected into safety.**
  - Both shots had exact start *and* end frames from the same camera. That gives zero ghosting and a **locked camera**.
  - The cut was a same-axis jump cut.
  - There was no establishing shot and no misdirection, and the reveal was ~100 px wide in a medium shot with no reaction shot.
  - The character's art direction was wasted at medium size, there was no music, and the start frame had an odd hand pose.
  - Jason: "dry n boring".
  - **Lesson:** avoiding artefacts is not directing. Technically clean and cinematically dead still fails.

## 2. What made film 3 work: do this

1. **Story arc before shot list.**
   - Use world → beauty → tension/misdirection → **reveal** → reaction → flight → payoff → closing beat.
   - A surprise needs a beat where the audience expects the opposite (the seam-ripper looks about to ruin the embroidery). It also needs a reaction shot (her eyes) so the audience feels it.
2. **Treat the approved stills as the world, not the shot list.**
   - Build purpose-made start frames per shot: an establishing wide, a beauty close-up, a macro of the action, an extreme close-up of the eyes, a medium, and a close payoff.
   - Close shots are where the art direction (makeup, hair ornaments, material texture) finally gets the pixels it deserves.
3. **One anchor per shot, one camera move per shot.**
   - Use first-frame-only mode, plus one continuous eased move named in the prompt: dolly along the window, arc around the face, push-in on the macro, rise with the reveal, orbit with the flight, push-in on the payoff.
   - Use first + last frame only when an end state *must* be locked. Two endpoints from the same camera position lock the camera.
4. **Cuts that gel.**
   - Every cut changes size by two or more steps or the angle by 30° or more.
   - Every cut is motivated by an action (the thread snap), a reaction (eyes → macro) or a state (standing butterfly → medium), or is a match on action.
5. **Duration serves the story.** Ten seconds could not hold setup + reveal + reaction + payoff. When the film needs more, ask Jason for latitude. Here 25 s was right, and he explicitly allows it now when it serves the piece.
6. **Music first.**
   - Generate 2–3 beds and let Jason pick by ear (he chose C: strings + shakuhachi).
   - Cut to the bed. Duck it for a held breath under the tension (7.3–11.3 s here).
   - Put SFX on causes: snap, cloth, flutter. Discard native generator audio.
7. **Give the creature or object an intention at the climax.** Jason's note, a sudden fast "talking" flutter on her fingertip followed by her laugh, turned a nice shot into the moment the film is about. Look for the one beat where the fantasy element *communicates*.
8. **Look continuity is decided in the start frames, not the grade.**
   - Derive neighbouring shots' start frames from the same hero frame (the flight start frame was built from the payoff and the beauty close-up).
   - A grade can only unify. Pushing a cool daylight shot toward a warm reference turned it orange. Sky-only tweaks still read as stormy.
   - What worked: regenerate the *window view* in the start frame, then match its colour statistics locally to the reference shots.
   - **Show Jason a start-frame-vs-world colour comparison before paying for video** when the look is in question. He asked for exactly this.
9. **Check anatomy and identity at full resolution, mid-motion.**
   - Check hands, faces, mirrored asymmetric makeup and ornaments on full-res crops, not 400-px contact sheets.
   - On long orbits Seedance mirrored her makeup once the head turned frontal, so trim before the drift.
10. **Image models behaved differently, one sample each, not a ranking:**
    - **gpt-image-2.5-sunburst** obeyed pose and region edits while keeping the base frame. Use it to edit a good frame.
    - **nano-banana** gives good new compositions but drifts: a stylised other character, a CG geisha with scar-like stitching, mirrored makeup. Check every output against the identity reference.

## 3. Avoid
- Shipping a film whose only virtue is "no artefacts".
- Fixing a world or lighting mismatch with a grade.
- Pasted 2D composites, cosmetic overlays for physics, or an enlarged crop to hide a defect (films 1 and 2).
- Spending on video before the start frame's colour, hands and identity pass.
- Baking grain in before upscaling: Real-ESRGAN smears it. Add grain after.
- Hold → move → hold reframes, or a reframe across a cut (film 2).
- Treating a frame-sheet review as a normal-speed review. Say what wasn't watched or heard.

## 4. The process that worked (film 3, ~4 h)
1. Verify the approved packet, read it, run the free pre-checks (absdiff, sleeve and hand continuity), then plan, estimate cost, and **ask for one credit cap**.
2. Write a self-critique plus shot list with a camera move per shot and a cost, and get the cap.
3. Batch the start frames and music beds, then QC the start frames at full resolution and reject freely.
4. Generate video, up to **3 concurrent jobs** (ChatCut limit). QC each take while the others render.
5. Assemble locally (`experiments/TEST-009/assemble.py`) as several music versions. Jason picks by ear.
6. Apply targeted fixes only, one hypothesis each: the "talking" flutter, the flight shot's world, the opening's sky and buildings.
7. **Freeze the approved master** (`approved/<project>/video-director-v04/APPROVAL.json`).
8. Do the 1080p finish: Real-ESRGAN x4 on grain-free frames, 70/30 blend with native, grain after, audio stream-copied (`finish_1080.py`).
9. Make the 9:16 by reframing from the 4× frames, previewing a contact sheet of the window per shot first, with one eased move per shot (`reframe_portrait.py`). Where a shot can't hold both subjects, move from the action to the reaction.
10. Build the delivery folder with covers, posting copy (IG/X/LinkedIn), the efficiency comparison and hashes. No ZIP, no publishing.

## 5. Efficiency

Full table in `delivery/DCL-20261014-WEFT-2026-10-14/COMPARISON_FILM01_02_03.md`.

| Metric | Film 2 | Film 3 | Change |
|---|---:|---:|---:|
| Tokens processed | 151.8 M | 116.1 M | −24% |
| Tokens per finished second | 15.2 M | 4.6 M | −70% |
| Uncached tokens | 3.17 M | 1.50 M | −53% |
| Wall time | ~16 h | ~4 h | |
| ChatCut credits | 48.6 | 75.6 (2.5× the film) | |

**Main drivers:**
- the ChatCut **plugin** instead of computer-use typing
- direct asset downloads plus local ffmpeg/OpenCV QC
- reused scripts, with each revision a config change
- parallel jobs
- start-frame QC before paid video

## 6. Reusable tools

All under `experiments/`:
- `TEST-009/assemble.py`: N-shot trim and concat + music/SFX mix with ducking + two-pass loudnorm.
- `TEST-009/work/grade.py`: shot-level partial LAB transfer to a reference + optional grain, no flicker.
- `TEST-009/finish_1080.py`: Real-ESRGAN 1080p finish, grain after, audio payload check.
- `TEST-009/reframe_portrait.py`: 9:16 from the 4× frames, per-shot eased centres, `--preview` contact sheet.
- `TEST-008/work/build_b0c.py`: ECC-align a derived frame and composite only the changed region over exact base pixels (background lock).
- `TEST-009/work/dl.py`: download a ChatCut asset by asset UUID and filename.

## 7. Jason's taste, confirmed across three films
- **Look:** photoreal, never CG-smooth. Film grain helps skin read as photographed. Continuous eased camera with depth and parallax; locked or static shots read as boring.
- **Story and performance:** clear story beats, a real surprise, well-acted emotion, eyelines on the subject. Show the character's beauty on screen.
- **Continuity:** one consistent world across shots, including the colour of sky, buildings and skin. He will spot an orange or stormy outlier.
- **Sound and length:** music matters. Duration can grow when it serves the piece.
- **Delivery:** "We shouldn't deliver unpolished work."

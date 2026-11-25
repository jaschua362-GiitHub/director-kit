# Director Kit — start here

A starter package for new film and motion directors. It collects what we learned making AI-assisted short films, spots and brand motion pieces from October to November 2026: the director's craft set, the guides, the agent skills, the tools that worked, and real scripts from finished films. Start from this instead of from zero.

**Read first:** [craft/DIRECTOR_CRAFT.md](craft/DIRECTOR_CRAFT.md), then the card for the stage you are in ([craft/](craft/README.md) explains which). That is the required reading; everything in `guides/` is the archive behind it.

**Local setup only:** run the kit on your own Windows desktop, not in a cloud or web agent session. [SETUP.md](SETUP.md) explains why.

**Setup:** [SETUP.md](SETUP.md) (software) and [PLUGINS.md](PLUGINS.md) (agent plugins and services).
**Using an AI agent?** Point it at [AGENTS.md](AGENTS.md).

## What changed in this update (25 November 2026)

Seven more films and spots since the last update (Small Cargo, House of Courtesy, the Forsaken opener, The Last Fritter, the FAI reveal, the Neo Siam film, The Last Ferry). The lessons had grown to about 95,000 words across retrospectives, and directors stopped absorbing them: one film repeated 18 faults that a written rule already covered. So the experience was rewritten by **when a director needs it**, not by the date it was learned.

1. **The craft set replaces the reading list.** [craft/DIRECTOR_CRAFT.md](craft/DIRECTOR_CRAFT.md) (about 900 words: who the director is, what a good film is, the six costliest lessons) plus fourteen 500-word cards in [craft/cards/](craft/cards/): three for every session (handoff and sessions, money and approvals, working with the creative lead) and one per stage (story and prep, board, plates, pilot, production, fight sequence, cut, sound, vertical, title and poster, closeout and social). A new lesson replaces or merges a card line; no dated blocks.
2. **Look before the creative lead does.** Watch every shot at normal speed, then step every frame on faces, hands and joins, and write a verdict per shot. Never send a shot you would not approve; a weak measurement is a stop, not a footnote.
3. **Compare with the design feature by feature,** at the still, where a fix costs cents rather than dollars.
4. **One director, few hands; hand off by about 250 K context** on the one-page [HANDOFF_FORM.md](craft/HANDOFF_FORM.md), which names the next stage's card by path.
5. **A cap is a cap.** One quote per gate, a typed yes that names the amount, drafts before HD. The money card now carries a standing per-film budget and the cost per finished second of recent films.
6. **A toolbox by need.** [craft/TOOLBOX.md](craft/TOOLBOX.md) lists the proven routes (board and start frames, one-prompt takes, the new [graphic-spot-method](skills/graphic-spot-method/SKILL.md) skill for 15 s motion-graphics spots, environment continuity, vertical reframe, colour grade, art review). The handoff says which were taken and why.
7. **Let the script check.** [tools/craft_check.py](tools/craft_check.py) runs the mechanical checks each card lists (spend against cap, HD against its draft, motion, sound transients, frame anchors, edges, context size), so a director does not have to remember them.

New in `guides/`: the [Small Cargo retrospective](guides/RETROSPECTIVE_2026-11-09_TEST022.md) and the [Forsaken opener retrospective](guides/RETROSPECTIVE_2026-11-12_TEST024_FORSAKEN_OPENER.md). The older guides now open with an archive banner.

## Earlier update (7 November 2026)

Four more films were finished since the first release, and they changed the workflow more than the first six did. The short version:

1. **Lock every requirement before production.** Music, sound effects, end title, epigraph, typography, finish route and every item the source deferred are answered row by row at the board gate, with a rough local preview. [REQUIREMENTS_LOCK_TEMPLATE.md](guides/REQUIREMENTS_LOCK_TEMPLATE.md). Hold the Note cost four times its token target because these arrived during the finish.
2. **Decide post before production.** Effects are tested on clean plates and approved, continuity rules for persistent effects are written down, and the ending is decided, before the first paid take. [GUARDRAILS_HOLD_THE_NOTE.md](guides/GUARDRAILS_HOLD_THE_NOTE.md).
3. **Draft, approve the draft edit, then complete the approved draft natively.** On Atlas the completion keeps motion, staging and faces, so approving the draft edit approves the final content. Drafts are made with audio off. [RETROSPECTIVE_2026-11-03_TEST018_DIRECTING.md](guides/RETROSPECTIVE_2026-11-03_TEST018_DIRECTING.md), [PLATFORM_COMPARISON_2026-11-03.md](guides/PLATFORM_COMPARISON_2026-11-03.md).
4. **The finish route for a face is set by its size.** Under about 60 px in the final frame means native 1080p from the start. SeedVR2 is for faceless shots and for faces that pass a 100 % crop on the finished master. [RETROSPECTIVE_2026-11-06_TEST020.md](guides/RETROSPECTIVE_2026-11-06_TEST020.md) §11.
5. **First + last frame for every face shot, and a frame-pair check before paying.** A prop or gaze that disagrees between the frames forces a morph in every take. [tools/frame_pair_check.py](tools/frame_pair_check.py).
6. **Insert + cut, never a patch on a moving subject.** Composites are checked on every frame and in playback. [RETROSPECTIVE_2026-11-03_TEST019_PILOT.md](guides/RETROSPECTIVE_2026-11-03_TEST019_PILOT.md).
7. **Stills get a rendering pass.** Native ImageGen designs the plates; a Seedream edit pass turns them into photo plates; video starts only from photo plates. [IMAGE_RENDERING_PIPELINE.md](guides/IMAGE_RENDERING_PIPELINE.md), [SKIN_REALISM.md](guides/SKIN_REALISM.md), [STILL_TO_VIDEO_QUALITY.md](guides/STILL_TO_VIDEO_QUALITY.md).
8. **Phase sessions.** One agent session per gate, handed off by about 250 K context; retake loops in a fresh small session; one batch of notes per review; a token line in every gate message. [PIPELINE_SIMULATION_2026-11-07_TEST020.md](guides/PIPELINE_SIMULATION_2026-11-07_TEST020.md) shows the same film replayed with these rules: about four times fewer tokens and a quarter less credit, no quality step cut.
9. **Dialogue in the film's own language gets a speech-to-text pass on every take.** A line the speech model mishears is a line the audience cannot hear; change the line before spending more takes.
10. **Measure generated music before choosing a take** (tempo, beat phase, pitch class, natural ending), then cut the picture to it. Sound by stages: silence and natural sound first, the score at the climax.

## What is in the kit

| Folder | What it holds | How to treat it |
|---|---|---|
| [craft/](craft/README.md) | The craft page, fourteen cards, the handoff form and the toolbox | Required reading. Current rules, one line per lesson |
| [guides/](guides/) | Playbooks, director brief, retrospectives film by film, the requirements lock, guardrails, the rendering pipeline, lessons | Archive: open for the full story behind a card line |
| [skills/](skills/) | Nine agent skills (Claude Code / Codex) | Install, then the agent uses them |
| [tools/](tools/) | Ready-to-use scripts: image jobs, frame-pair check, per-shot upscale (Real-ESRGAN, SeedVR2), token counter | Copy into your project's `tools\` folder |
| [examples/](examples/) | Real scripts from six films | Study and adapt. Paths inside are project-specific |
| [MANIFEST.json](MANIFEST.json) | Source path and hash of every copied file | For refreshing the kit later |

The guides are working records from the lab. Project IDs such as `DCL-20261021-SHADOW` name films that are not included, and links marked "lab file, not in kit" point at lab folders outside the kit. Read past them for the lesson. The lab's own director is called Jason in these pages; where a guide says "Jason judges", read "the human director judges".

## Learning path

Work through it in order. Each step names what to read and what to practise.

1. **How we direct.** Start with [DIRECTOR_CRAFT.md](craft/DIRECTOR_CRAFT.md) and the three every-session cards. For the history behind them: [VIDEO_DIRECTOR_BRIEF.md](guides/VIDEO_DIRECTOR_BRIEF.md), then the retrospectives in order: [films 1–3](guides/RETROSPECTIVE_2026-10-14_VIDEO_AGENTS.md), [Film 5](guides/RETROSPECTIVE_2026-10-20_FILM5_DIRECTING.md), [Film 6](guides/RETROSPECTIVE_2026-10-27_FILM6_DIRECTING.md), [Film 7](guides/RETROSPECTIVE_2026-10-29_FILM7_DIRECTING.md), [Evade and Escape](guides/RETROSPECTIVE_2026-11-03_TEST018_DIRECTING.md), [One Beat Late pilot](guides/RETROSPECTIVE_2026-11-03_TEST019_PILOT.md) and [phase 3](guides/RETROSPECTIVE_2026-11-05_TEST019_PHASE3.md), [one-prompt takes](guides/RETROSPECTIVE_2026-11-05_TEST021_ONE_PROMPT.md), [Hold the Note](guides/RETROSPECTIVE_2026-11-06_TEST020.md). Hold the Note and its [simulation](guides/PIPELINE_SIMULATION_2026-11-07_TEST020.md) hold the current workflow; Film 6 still has the best board-and-start-frame walkthrough.
2. **Story.** [STORY_FOUNDATION.md](guides/STORY_FOUNDATION.md): a synopsis plus concept art is the foundation; the director develops the storyboard and pacing. Price the hard beats first with the story risk list (crossing paths, small hand-held objects, on-screen text, mirrors, a light change inside one shot, three actions in a row). [OPTIONAL_CRAFT_TOOLS.md](guides/OPTIONAL_CRAFT_TOOLS.md) has scene and take diagnostics to use when a scene feels flat.
3. **Concept art that can move.** [CONCEPT_TO_MOTION.md](guides/CONCEPT_TO_MOTION.md), the [cinematic-art-review](skills/cinematic-art-review/SKILL.md) skill, and [environment-continuity](skills/environment-continuity/SKILL.md) (nine consistent views of each location). Then the [rendering pipeline](guides/IMAGE_RENDERING_PIPELINE.md): design plates, a rendering pass to photo plates, measured crops. Prepare image prompts as jobs that can run by hand or by agent: [IMAGE_JOBS_FORMAT.md](tools/IMAGE_JOBS_FORMAT.md).
4. **Board, requirements lock and rough preview.** Draw the board and get it locked before you spend credits on photoreal frames or video. Fill in the [requirements lock](guides/REQUIREMENTS_LOCK_TEMPLATE.md) and send it with the board and a rough local preview (board frames timed as the cut, with the planned sound, subtitles and title). Read the [guardrails](guides/GUARDRAILS_HOLD_THE_NOTE.md). Examples: [build_drawn_board.py](examples/film6-shadow/build_drawn_board.py), [build_storyboard.py](examples/film6-shadow/build_storyboard.py), [make_locked_jobs.py](examples/film6-shadow/startframes/make_locked_jobs.py), [build_visual_board.py](examples/one-beat-late/production/stills/build_visual_board.py).
5. **Start frames.** Camera side, look direction and eye-line written into every prompt; a last frame for every move that ends on a readable face; props identical between start and end frames. Run [frame_pair_check.py](tools/frame_pair_check.py) on every pair before a paid job. Example prompts: [build_face_prompts.py](examples/one-beat-late/production/video/build_face_prompts.py), [build_requests.py](examples/hold-the-note/production/p4_atlas/build_requests.py).
6. **Video generation.** [PRODUCTION_PLAYBOOK.md](guides/PRODUCTION_PLAYBOOK.md), [FORMAT_AND_RESOLUTION_WORKFLOW.md](guides/FORMAT_AND_RESOLUTION_WORKFLOW.md) and the [platform comparison](guides/PLATFORM_COMPARISON_2026-11-03.md). Cheap drafts with audio off for blocking and the whole edit; one quote per gate; then complete the approved drafts natively where a face reads. Shared takes can cover two board panels. For teasers, series fillers and flowing sequences, the second route is the [one-prompt-takes](skills/one-prompt-takes/SKILL.md) skill: one structured prompt and reference images make a take of up to 30 s, then you patch the shots that miss. Dense multi-character shots blend identities: give each character their own shot.
7. **Edit.** Frame-exact assembly on a frozen EDL: [assemble_final.py](examples/film6-shadow/assemble_final.py) (with [assemble_v02.py](examples/film6-shadow/assemble_v02.py) and [hud.py](examples/film6-shadow/hud.py)), [make_finish_edl.py](examples/hold-the-note/production/finish/make_finish_edl.py). Measure the music first ([analyze_music.py](examples/one-beat-late/production/music/analyze_music.py)), then conform the picture to it ([build_music_edit.py](examples/one-beat-late/production/edit/build_music_edit.py)). Review the cut as a first-time viewer: a close-up's object must reappear in the next wide, and the film ends on a motivated closing beat.
8. **Sound.** By stages: silence and natural sound first, the score at the climax, a recurring cue per key beat, about −15 LUFS with real dynamics. Designed layers sit quieter than feels right. [design_sfx.py](examples/one-beat-late/production/sound/design_sfx.py), [build_sound_mix.py](examples/one-beat-late/production/sound/build_sound_mix.py), [make_bed.py](examples/film6-shadow/music/make_bed.py), [gem_sfx.py](examples/film4-wind/gem_sfx.py), the business-motion-film [audio notes](skills/business-motion-film/references/audio.md) and the motion-sting [audio kit](skills/motion-sting/audio/). Record the true source of every layer at sound approval.
9. **Effects and composites.** Insert + cut over patching a moving subject; effects read as a physical reaction to a force, scaled against a body part in frame, tested at 2 s on a clean plate and approved before production. Check every frame, in playback, inside the cut with its fades on. [insert.py](examples/one-beat-late/pilot/composite/insert.py), [grain_fx.py](examples/hold-the-note/effects/grain_fx.py), [every_frame.py](examples/one-beat-late/production/finish/every_frame.py), [paint_out_sprite.py](examples/film7-himmapan/paint_out_sprite.py).
10. **Finish.** Route per shot by face size: native 1080p under about 60 px, [seedvr2.ps1](tools/seedvr2.ps1) for faceless shots, [upres_shot.py](tools/upres_shot.py) where detail will not read. Audit every face at 100 % on the finished master ([face_sheet.py](examples/hold-the-note/production/finish/face_sheet.py)) and track props across the HD file ([flute_track.py](examples/hold-the-note/production/finish/flute_track.py)). Then [colour-grade](skills/colour-grade/SKILL.md) by measurement, grain once after grading. [build_final_1080.py](examples/one-beat-late/production/finish/build_final_1080.py), [measure.py](examples/one-beat-late/production/finish/measure.py), [verify_final.py](examples/one-beat-late/production/finish/verify_final.py), [grade_plates.py](examples/film6-shadow/finish/grade_plates.py), [look.py](examples/film4-wind/look.py).
11. **Vertical cut.** [vertical-reframe](skills/vertical-reframe/SKILL.md): measure subject positions, cap pan speed, never AI-extend faces, approve a real-time framing preview before upscaling. When a 16:9 shot is approved and its subject sits inside the centre column, reframe it instead of generating a second performance: [build_04V_reframe.py](examples/hold-the-note/production/finish/build_04V_reframe.py), [vertical_preview.py](examples/film4-wind/vertical_preview.py), [vertical_finish.py](examples/film4-wind/vertical_finish.py).
12. **Titles, text and motion graphics.** Decide the route first with [motion-design-advisor](skills/motion-design-advisor/SKILL.md). Then build with [motion-sting](skills/motion-sting/SKILL.md) (code-driven logo stings and brand motion) or [business-motion-film](skills/business-motion-film/SKILL.md) (commercials with an independent-critic loop). On-screen text is set locally, never by an image model: [epigraph_overlay.py](examples/hold-the-note/production/finish/epigraph_overlay.py), [title_slam.py](examples/film4-wind/title_slam.py), [render.mjs](examples/film6-shadow/title/codex-v02-DRAFT/render.mjs).
13. **Delivery and social.** [FINAL_DELIVERY_STANDARD.md](guides/FINAL_DELIVERY_STANDARD.md), [package_final_delivery.py](examples/one-beat-late/closeout/package_final_delivery.py), [package_social_materials.py](examples/film6-shadow/closeout/package_social_materials.py). Posters from a text-free plate with the title set by hand ([make_poster.py](examples/hold-the-note/closeout/make_poster.py)). Post copy is approved before any kit is built, in one voice per platform.
14. **Keep learning.** [LESSONS.md](guides/LESSONS.md) is the running evidence log. Count your tokens at every gate with [token_count.py](tools/token_count.py) and compare your film with the [simulation](guides/PIPELINE_SIMULATION_2026-11-07_TEST020.md). Add your own lessons the same way: dated, with what failed and the rule it taught.

## Rules that cost us the most to learn

- **Judge visuals, not text.** Show a drawn board or key frames before generating any video.
- **Lock every requirement before production.** Music, SFX, end title, epigraph, typography, finish route, ending and every deferred item, answered row by row. A blank row is not a yes, and "deferred" never means "dropped".
- **Approved art is a style guide.** Re-stage frames for the shot you want; keep identity, costume and world consistent.
- **Check the physics and the blocking before a paid video call.** Where is everyone, what moves, what is the light doing? Then run the frame-pair check.
- **A move that ends on a readable face gets a last frame.** Props and gaze must agree between start and end frames, or every take morphs.
- **Faces under about 60 px are generated at native 1080p.** Upscalers invent features on small faces. Audit every face at 100 % on the finished master.
- **Complete each action before the cut and cut on motion.** A camera move commits, or the shot goes.
- **One action per shot in dense scenes.** Several characters in one frame blend identities.
- **Put the twist on screen.** If the story turns on what a character or machine sees, show their point of view.
- **Climax around the middle of the story** (before 60% of the runtime). Protect the payoff and end on a motivated closing beat, then black.
- **Review as a first-time viewer.** A close-up's object reappears in the next wide; a persistent effect has a written continuity rule.
- **Check the take you already paid for.** Strip it at 6–8 fps before you regenerate; the fix is often already in the clip.
- **One re-render is a new take.** Keep every take and record its prompt and settings. A retake carries every known fix at once.
- **Insert + cut, never a patch on a moving subject.** Check composites on every frame and in playback.
- **Upscale each shot from its original clip,** never an assembled lower-resolution edit. Compare luma against the source.
- **Grade by measurement** (faces 35–45%, highlights 90–97%, blacks 1–3%), then re-measure the delivered file. A house look is a starting point, not a rule.
- **Design the sound by stages.** Silence and natural sound first, the score at the climax, a recurring cue per key beat. Measure generated music and SFX before using them. Title hits come from the film's own sound family.
- **Get one independent critique** before calling a cut final, and watch the whole cut yourself at phone size with sound on.
- **Phase sessions, one batch of notes per review.** Hand off at each gate or by about 250 K context. Token rules cut waste, not quality steps.

## Not included

- Third-party binaries and models (ffmpeg, Real-ESRGAN, SeedVR2, Dreamina CLI): install them per [SETUP.md](SETUP.md).
- Vendor plugins and services (ChatCut, Atlas Cloud, Remotion): install or connect them per [PLUGINS.md](PLUGINS.md) so they stay up to date.
- Approved film art, reference images, finished films and benchmark captures: they belong to their projects and their original authors.
- Brand assets: the motion-sting `template/glyphs.js` is an empty placeholder. Trace your own logo with `scripts/trace_logo.py`.

# Director Kit — start here

A starter package for new film and motion directors. It collects what we learned making six AI-assisted short films and a set of brand motion pieces (October 2026): the guides, the agent skills, the tools that worked, and real scripts from finished films. Start from this instead of from zero.

**Setup:** [SETUP.md](SETUP.md) (software) and [PLUGINS.md](PLUGINS.md) (agent plugins and services).
**Using an AI agent?** Point it at [AGENTS.md](AGENTS.md).

## What is in the kit

| Folder | What it holds | How to treat it |
|---|---|---|
| [guides/](guides/) | Playbooks, director brief, retrospectives, lessons | Read. Dated entries; the newest entry wins |
| [skills/](skills/) | Seven agent skills (Claude Code / Codex) | Install, then the agent uses them |
| [tools/](tools/) | Ready-to-use scripts: image jobs, per-shot upscale | Copy into your project's `tools\` folder |
| [examples/](examples/) | Real scripts from Film 4 and Film 6 | Study and adapt. Paths inside are project-specific |
| [MANIFEST.json](MANIFEST.json) | Source path and hash of every copied file | For refreshing the kit later |

The guides are working records from the lab. Project IDs such as `DCL-20261021-SHADOW` name films that are not included, and links into `days/`, `approved/`, `experiments/` or `FINAL_RENDERED/` point at lab folders outside the kit. Read past them for the lesson.

## Learning path

Work through it in order. Each step names what to read and what to practise.

1. **How we direct.** [VIDEO_DIRECTOR_BRIEF.md](guides/VIDEO_DIRECTOR_BRIEF.md), then the retrospectives in order: [films 1–3](guides/RETROSPECTIVE_2026-10-14_VIDEO_AGENTS.md), [Film 5](guides/RETROSPECTIVE_2026-10-20_FILM5_DIRECTING.md), [Film 6](guides/RETROSPECTIVE_2026-10-27_FILM6_DIRECTING.md). Film 6 holds the current best workflow.
2. **Story.** [STORY_FOUNDATION.md](guides/STORY_FOUNDATION.md): a synopsis plus concept art is the foundation; the director develops the storyboard and pacing.
3. **Concept art that can move.** [CONCEPT_TO_MOTION.md](guides/CONCEPT_TO_MOTION.md), the [cinematic-art-review](skills/cinematic-art-review/SKILL.md) skill, and [environment-continuity](skills/environment-continuity/SKILL.md) (nine consistent views of each location). Prepare image prompts as jobs that can run by hand or by agent: [IMAGE_JOBS_FORMAT.md](tools/IMAGE_JOBS_FORMAT.md).
4. **Board before video.** Draw the board and get it locked before you spend credits on photoreal frames or video. Examples: [build_drawn_board.py](examples/film6-shadow/build_drawn_board.py), [build_storyboard.py](examples/film6-shadow/build_storyboard.py), [make_locked_jobs.py](examples/film6-shadow/startframes/make_locked_jobs.py).
5. **Video generation.** [PRODUCTION_PLAYBOOK.md](guides/PRODUCTION_PLAYBOOK.md) and [FORMAT_AND_RESOLUTION_WORKFLOW.md](guides/FORMAT_AND_RESOLUTION_WORKFLOW.md). Cheap drafts for blocking and the whole edit; promote only hero shots and faces to native 1080p.
6. **Edit.** Frame-exact assembly: [assemble_final.py](examples/film6-shadow/assemble_final.py) (it imports [assemble_v02.py](examples/film6-shadow/assemble_v02.py) and [hud.py](examples/film6-shadow/hud.py), a designed machine-POV overlay).
7. **Sound.** Ambience bed first, then cues on measured motion peaks, about −15 LUFS. [make_bed.py](examples/film6-shadow/music/make_bed.py), [gem_sfx.py](examples/film4-wind/gem_sfx.py), the business-motion-film [audio notes](skills/business-motion-film/references/audio.md) and the motion-sting [audio kit](skills/motion-sting/audio/).
8. **Finish.** [colour-grade](skills/colour-grade/SKILL.md) (measure faces, highlights and blacks; never darken the whole film to hide a CGI look), per-shot upscale with [upres_shot.py](tools/upres_shot.py), grain once after grading (1.0 for 9:16 phone delivery). Grade examples: [look.py](examples/film4-wind/look.py), [luma_report.py](examples/film4-wind/luma_report.py), [grade_plates.py](examples/film6-shadow/finish/grade_plates.py).
9. **Vertical cut.** [vertical-reframe](skills/vertical-reframe/SKILL.md): measure subject positions, cap pan speed, never AI-extend faces, approve a real-time framing preview before upscaling. Examples: [vertical_preview.py](examples/film4-wind/vertical_preview.py), [vertical_finish.py](examples/film4-wind/vertical_finish.py).
10. **Titles and motion graphics.** Decide the route first with [motion-design-advisor](skills/motion-design-advisor/SKILL.md). Then build with [motion-sting](skills/motion-sting/SKILL.md) (code-driven logo stings and brand motion) or [business-motion-film](skills/business-motion-film/SKILL.md) (commercials with an independent-critic loop). Film title examples: [title_slam.py](examples/film4-wind/title_slam.py), [render.mjs](examples/film6-shadow/title/codex-v02-DRAFT/render.mjs).
11. **Delivery.** [FINAL_DELIVERY_STANDARD.md](guides/FINAL_DELIVERY_STANDARD.md) and the social-materials packager [package_social_materials.py](examples/film6-shadow/closeout/package_social_materials.py) (title clip, poster, stills, captions).
12. **Keep learning.** [LESSONS.md](guides/LESSONS.md) is the running evidence log. Add your own lessons the same way: dated, with what failed and the rule it taught.

## Rules that cost us the most to learn

- **Judge visuals, not text.** Show a drawn board or key frames before generating any video.
- **Approved art is a style guide.** Re-stage frames for the shot you want; keep identity, costume and world consistent.
- **Check the physics and the blocking before a paid video call.** Where is everyone, what moves, what is the light doing?
- **Complete each action before the cut and cut on motion.** A camera move commits, or the shot goes.
- **Put the twist on screen.** If the story turns on what a character or machine sees, show their point of view.
- **Climax around the middle of the story** (before 60% of the runtime). Protect the payoff and end on a hold, not a hard stop.
- **Check the take you already paid for.** Strip it at 6–8 fps before you regenerate; the fix is often already in the clip.
- **One re-render is a new take.** Keep every take and record its prompt and settings.
- **Upscale each shot from its original clip,** never an assembled lower-resolution edit. Compare luma against the source.
- **Grade by measurement** (faces 35–45%, highlights 90–97%, blacks 1–3%), then re-measure the delivered file.
- **Design the sound.** Bed, then sparse cues on motion peaks, all in one acoustic space. Title hits come from the film's own sound family.
- **Get one independent critique** before calling a cut final.

## Not included

- Third-party binaries and models (ffmpeg, Real-ESRGAN, Dreamina CLI): install them per [SETUP.md](SETUP.md).
- Vendor plugins (ChatCut, Remotion): install them per [PLUGINS.md](PLUGINS.md) so they stay up to date.
- Approved film art, reference images and benchmark captures: they belong to their projects and their original authors.
- Brand assets: the motion-sting `template/glyphs.js` is an empty placeholder. Trace your own logo with `scripts/trace_logo.py`.

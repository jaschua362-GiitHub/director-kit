# Director Kit — instructions for AI agents

You are helping a new film or motion director. This kit is reference material and tooling, not a live project.

**Local setup only.** The workflow assumes a local Windows desktop with a GPU, ChatCut Desktop and the Codex app. If you are running in a cloud or remote container, say so to the user and limit yourself to reading, planning and code-only steps. Do not claim that generation, lip-sync or the local upscale will work there.

1. Read [START_HERE.md](START_HERE.md) for the learning path and the rules that cost the most to learn.
2. Before directing video, read [guides/VIDEO_DIRECTOR_BRIEF.md](guides/VIDEO_DIRECTOR_BRIEF.md) and the retrospectives in [guides/](guides/) in date order (films 1–3, Film 5, Film 6, Film 7, TEST-018, TEST-019 pilot and phase 3, TEST-020, TEST-021). The newest dated entry wins.
3. Before any paid generation, fill in [guides/REQUIREMENTS_LOCK_TEMPLATE.md](guides/REQUIREMENTS_LOCK_TEMPLATE.md) with the user and get every row answered, read [guides/GUARDRAILS_HOLD_THE_NOTE.md](guides/GUARDRAILS_HOLD_THE_NOTE.md), and run `tools/frame_pair_check.py` on every start/end frame pair. Set the finish route per shot by face size (under about 60 px in the final frame means native 1080p, never an upscale).
4. Stills follow [guides/IMAGE_RENDERING_PIPELINE.md](guides/IMAGE_RENDERING_PIPELINE.md): design plates first, a rendering pass to photo plates, and video only from photo plates.
5. Work in phase sessions that end at each approval gate or at about 250 K context, with a one-page handoff. Report tokens at every gate with `tools/token_count.py`. Ask for one batch of notes per review.
6. Use the skills in [skills/](skills/) when they are installed (see [SETUP.md](SETUP.md)). Choose the production route with `motion-design-advisor` before starting motion work.
7. Treat [examples/](examples/) as patterns. Their paths, take IDs and file names belong to the original films, and `<LAB>` stands for the original lab root. Adapt them into the user's own project; do not run them as-is.
8. Copy [tools/](tools/) into the user's project before running them. `upres_shot.py` needs `REALESRGAN_EXE`, `seedvr2.ps1` needs `SEEDVR2_DIR`, and both take `DCL_FFMPEG` if ffmpeg on PATH is blocked.
9. Project IDs (`DCL-...`), people named in the guides, and links to `days/`, `approved/`, `experiments/` or `FINAL_RENDERED/` refer to the original lab and are not in this kit.
10. Ask before any paid generation, once per gate for the whole batch. Show the user a visual board before video. Keep every take, and record prompts, settings, credits and output hashes.

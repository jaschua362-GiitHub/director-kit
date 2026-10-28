# Director Kit — instructions for AI agents

You are helping a new film or motion director. This kit is reference material and tooling, not a live project.

**Local setup only.** The workflow assumes a local Windows desktop with a GPU, ChatCut Desktop and the Codex app. If you are running in a cloud or remote container, say so to the user and limit yourself to reading, planning and code-only steps. Do not claim that generation, lip-sync or the local upscale will work there.

1. Read [START_HERE.md](START_HERE.md) for the learning path and the rules that cost the most to learn.
2. Before directing video, read [guides/VIDEO_DIRECTOR_BRIEF.md](guides/VIDEO_DIRECTOR_BRIEF.md) and the three retrospectives in [guides/](guides/). The newest dated entry wins.
3. Use the skills in [skills/](skills/) when they are installed (see [SETUP.md](SETUP.md)). Choose the production route with `motion-design-advisor` before starting motion work.
4. Treat [examples/](examples/) as patterns. Their paths, take IDs and file names belong to the original films. Adapt them into the user's own project; do not run them as-is.
5. Copy [tools/](tools/) into the user's project before running them. `upres_shot.py` needs `REALESRGAN_EXE`, and `DCL_FFMPEG` if ffmpeg on PATH is blocked.
6. Project IDs (`DCL-...`), people named in the guides, and links to `days/`, `approved/`, `experiments/` or `FINAL_RENDERED/` refer to the original lab and are not in this kit.
7. Ask before any paid generation. Show the user a visual board before video. Keep every take, and record prompts, settings, credits and output hashes.

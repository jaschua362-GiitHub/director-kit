# Director Kit

A starter package for new film and motion directors working with AI tools. It holds what we learned making eleven AI-assisted short films and spots and a set of brand motion pieces (October to November 2026):

- the playbooks and directing retrospectives, film by film;
- the requirements lock, guardrails and image rendering pipeline that every film now starts with;
- eight agent skills for Claude Code and Codex;
- the tools that worked, including the checks that run before money is spent;
- real scripts from six finished films.

**Updated 7 November 2026.** New since the first release: five retrospectives (Himmapan, Evade and Escape, One Beat Late pilot and phase 3, Hold the Note), the requirements lock, the Hold the Note guardrails, the image rendering pipeline, a platform comparison, the token simulation, three tools (frame-pair check, SeedVR2 runner, token counter) and four new example folders. [START_HERE.md](START_HERE.md) lists what changed in the workflow.

> **Local setup only.** The kit is built for a local Windows desktop with a GPU, the ChatCut Desktop app and the Codex app. It is not supported in Claude Code cloud/web sessions or other remote containers. Those have no GPU for the local upscaler, no desktop apps for voices, lip-sync and the image bridge, and no lasting storage for video files.

**Start here:** [START_HERE.md](START_HERE.md). It has a 12-step learning path and the rules that cost us the most to learn.

- Setup: [SETUP.md](SETUP.md) · Plugins and services: [PLUGINS.md](PLUGINS.md) · For AI agents: [AGENTS.md](AGENTS.md)
- `guides/`: how we direct, from story to delivery
- `skills/`: install into your agent
- `tools/`: image jobs, the frame-pair check, per-shot upscaling (Real-ESRGAN and SeedVR2) and the token counter
- `examples/`: scripts from six finished films, to read and adapt

The guides are dated working records from our lab. Project IDs and links marked "lab file, not in kit" refer to material that is not published here.

## License

Code (`.py`, `.js`, `.mjs`, `.ps1`, `.sh`, `.html`) is under the [MIT License](LICENSE). Writing and documentation (`.md`) are under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit "Jason Chua — Director Kit". Third-party services and tools named here keep their own terms.

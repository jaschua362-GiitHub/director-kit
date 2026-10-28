# Setup

**Local setup only.** Install and run the kit on your own computer: Windows 11, with a GPU that supports Vulkan for the local upscaler. Claude Code cloud/web sessions and other remote containers are not supported, for three reasons:
- They have no GPU, so `upres_shot.py` cannot run.
- They cannot reach desktop apps: ChatCut Desktop (voices, lip-sync, local projects) and the Codex app (image bridge).
- They do not keep large video files between sessions.

The planning documents and code-only steps can be read anywhere. The production workflow assumes a local machine. On macOS or Linux, most Python and ffmpeg steps work with path changes. The Codex bridge (`.ps1`) and the ChatCut workflow need Windows.

## 1. Core software

| Need | Used by | Install |
|---|---|---|
| Python 3.11+ | every `.py` script | python.org, then `pip install numpy opencv-python pillow scipy` |
| ffmpeg 7.x | assembly, finishing, audio | `winget install Gyan.FFmpeg`, or any static build |
| Node.js 18+ | HTML/JS title renders (`*.mjs`) | nodejs.org, then in the title folder: `npm install playwright sharp` and `npx playwright install chromium` |
| Chrome or Edge | motion-sting `scripts/render.py` (headless capture) | Usually already installed |
| potracer | motion-sting `scripts/trace_logo.py` | `pip install potracer` (imports as `potrace`) |

If your organisation blocks the ffmpeg on PATH (Windows Application Control did on one of our machines), install a build that runs and put it first on PATH. `tools/upres_shot.py` also accepts an explicit path:

```powershell
$env:DCL_FFMPEG = "C:\path\to\ffmpeg.exe"
```

## 2. Local upscaler (no credits)

`tools/upres_shot.py` needs Real-ESRGAN ncnn-vulkan:

1. Download the Windows release zip of `realesrgan-ncnn-vulkan` from the Real-ESRGAN GitHub releases (xinntao/Real-ESRGAN).
2. Unzip it, keeping the `models\` folder next to the exe.
3. Set the path:

```powershell
$env:REALESRGAN_EXE = "C:\path\to\realesrgan-ncnn-vulkan.exe"
python -I tools\upres_shot.py take.mp4 <in_frame> <n_frames> out.mkv --size 1920x1080
```

The script stops if the GPU returns dark frames. Still compare each upscaled shot's brightness with its source.

## 3. Image jobs (stills)

Read [tools/IMAGE_JOBS_FORMAT.md](tools/IMAGE_JOBS_FORMAT.md). Copy `tools\` into your project root; the scripts treat the folder that contains `tools\` as the project root.

- **Route A (by hand):** `python tools\make_manual_sheet.py <pack>` writes a paste-ready sheet for the ChatGPT app.
- **Route B (agent):** needs the OpenAI Codex app signed in to a ChatGPT plan with image generation. `tools\run_jobs.ps1 -Pack <pack>` calls `codex_imagegen.ps1` once per job and skips jobs already done.

## 4. Agent skills

Copy each folder in [skills/](skills/) to where your agent loads skills:

- **Claude Code:** `%USERPROFILE%\.claude\skills\<skill>\` (all projects) or `<project>\.claude\skills\<skill>\` (one project).
- **Codex:** `%USERPROFILE%\.codex\skills\<skill>\`.

Skills in this kit:
- `cinematic-art-review`: self-review of concept art before export.
- `environment-continuity`: nine-view environment coverage.
- `colour-grade`: measured grading targets.
- `vertical-reframe`: 9:16 cuts.
- `motion-design-advisor`: choose the production route.
- `motion-sting`: code-built brand motion.
- `business-motion-film`: commercials with a critic loop.

Some skill text still names the lab's own paths, such as `<PROJECTS>\<Brand>\...` or a reference project that is not included. Treat those as examples of where your own files go.

## 5. Paid services

Video generation, voices and lip-sync go through the plugins in [PLUGINS.md](PLUGINS.md) and spend credits. Run one short face-acceptance test (about 4 s) before committing a film to a provider, and draft at low resolution until the edit is approved.

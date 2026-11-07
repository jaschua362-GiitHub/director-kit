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

## 2b. SeedVR2 (optional, the better upscaler)

`tools/seedvr2.ps1` runs the SeedVR2 3B one-step diffusion upscaler through the standalone CLI from `numz/ComfyUI-SeedVR2_VideoUpscaler` (Apache-2.0). It re-synthesises detail, so it is for shots without readable faces, and for medium or close faces that pass a 100 % crop afterwards. Small faces (under about 60 px in the final frame) get invented features; those shots are generated at native 1080p instead.

1. Clone the upstream repository into `<SEEDVR2_DIR>\upstream\`.
2. Make a Python 3.12 environment at `<SEEDVR2_DIR>\.venv\` with a CUDA build of torch and the upstream requirements (we used `uv`; nothing global).
3. Download into `<SEEDVR2_DIR>\models\`: `seedvr2_ema_3b-Q8_0.gguf` (Hugging Face `AInVFX/SeedVR2_comfyUI`) and `ema_vae_fp16.safetensors` (`numz/SeedVR2_comfyUI`). Record their SHA-256.
4. Set the folder and run:

```powershell
$env:SEEDVR2_DIR = "D:\tools\seedvr2"
./tools/seedvr2.ps1 -In take.mp4 -Out take_1080x1920.mkv -Short 1080
```

Measured on an RTX 3080 (10 GB): about 5–8 min per 48 frames at a 1080 short side, about 17 min per 5 s clip at 1620; 2160 failed. The script refuses to start while other apps hold more than 3.5 GB of VRAM (`-MaxUsedMiB`, `-Force`). Batches of 5 frames mean temporal consistency is per batch: check for shimmer between batches.

## 2c. Checks that run before money is spent

- `python -I tools\frame_pair_check.py START.png END.png OUT_DIR` before every paid first/last-frame video job: an overlay, a difference heat map and the grid cells that changed. Anything that should stay fixed (walls, props, cup size, sky) must not light up; a prop that differs between the frames forces a morph in every take.
- `python -I tools\token_count.py "<film title>" --budget 150` at every approval gate, from the project folder you open Claude Code in. It reads the local Claude Code transcripts (read-only) and prints processed tokens per session, flagging sessions that passed 250 K context. Session titles must contain the film name.

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
- `one-prompt-takes`: multi-shot Seedance takes of up to 30 s from one prompt.
- `motion-design-advisor`: choose the production route.
- `motion-sting`: code-built brand motion.
- `business-motion-film`: commercials with a critic loop.

Some skill text still names the lab's own paths, such as `<PROJECTS>\<Brand>\...` or a reference project that is not included. Treat those as examples of where your own files go.

## 5. Paid services

Video generation, voices and lip-sync go through the plugins and services in [PLUGINS.md](PLUGINS.md) and spend credits. Run one short face-acceptance test (about 4 s) before committing a film to a provider, draft at low resolution until the edit is approved, and read [guides/PLATFORM_COMPARISON_2026-11-03.md](guides/PLATFORM_COMPARISON_2026-11-03.md) for how the providers compared on real films.

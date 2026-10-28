# Image jobs: one format, two routes

Jason, 2026-10-20: "we have 2 ways to do it, A and B. When Claude is running low on tokens I can do the A way, but your prompt needs to be ready."

**Every image job is prepared once, and either route can run it.**

## The format (per pack, e.g. `bible/pack-a/`)
```
<pack>/
  JOBS.json          list of jobs: id, prompt file, references, aspect, output name
  prompts/<id>.txt   the full prompt, self-contained, ready to paste
  RUN_MANUALLY.md    generated from JOBS.json: the Route A sheet
  returns/           where every image is saved, whichever route made it
```
`JOBS.json` entry:
```json
{ "id": "PA-YAN-01", "prompt": "prompts/PA-YAN-01.txt", "aspect": "2:3",
  "refs": ["bible/source-masters/C01-Ren-full-body-master.png"],
  "out": "returns/PA-YAN-01-a01.png" }
```
Reference paths are relative to the series root; `prompt` and `out` are relative to the pack folder.

## Route A: by hand in the ChatGPT app (fewest tokens on both sides)
Open `RUN_MANUALLY.md`. For each job: start a new chat → attach the listed images → paste the prompt file's text → generate → save as the listed name into `returns/`. Then tell Claude "pack X returns are in".

## Route B: Claude runs the Codex bridge (no manual effort)
```powershell
.\tools\run_jobs.ps1 -Pack "bible\pack-a"            # all jobs not yet generated
.\tools\run_jobs.ps1 -Pack "bible\pack-a" -Only PA-YAN-01
```
Each job calls `codex_imagegen.ps1` (lean mode). A job whose output already exists is skipped, so the routes can be mixed freely, with some jobs done by hand and the rest by the bridge. It uses Codex agent tokens (≈40k measured for one image before lean mode) plus the ChatGPT image allowance.

## Make the Route A sheet
```powershell
python .\tools\make_manual_sheet.py "bible\pack-a"
```

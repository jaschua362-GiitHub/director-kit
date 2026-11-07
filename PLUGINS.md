# Plugins and services

The kit lists these instead of copying them. They are maintained by their vendors, and a copied snapshot goes stale.

## ChatCut (video, voice, lip-sync, music, motion graphics)

Our main production surface for Films 4–6.

- **Install:** the ChatCut Desktop app, then its Agent Plugin for Claude Code or Codex (in the app's settings, or see ChatCut's docs).
- **Skills the plugin brings that we used most:**
  - `chatcut-video-gen`: Seedance 2.x, MiniMax H3 and Gemini Omni; text-, image- and first/last-frame-to-video.
  - `chatcut-voice`: TTS voices and placing narration.
  - `chatcut-lipsync`: sync mouths to final speech.
  - `chatcut-music`: score and beds.
  - `chatcut-create-motion-graphics`: code-built MG in the timeline.
  - `chatcut-visual-analysis`: shot-by-shot review.
  - `chatcut-transcription`: captions and subtitles.
- **Lessons:**
  - Lip-sync needs the project open in the Desktop app.
  - Generated assets land in the local project folder (`%APPDATA%\ChatCut\projects\...`). Copy them into your experiment folder and record their hashes.
  - See the Film 6 retrospective in [guides/](guides/) for the full workflow.

## Atlas Cloud (Seedance 2.5 pay-as-you-go, plus the still rendering pass)

Our video route from TEST-018 on (November 2026), through its MCP connector. See [guides/PLATFORM_COMPARISON_2026-11-03.md](guides/PLATFORM_COMPARISON_2026-11-03.md) for the numbers.

- **Why:** no subscription, an exact quote before every job, and `draft-complete` turns an approved 480p draft into native 1080p with the same motion, staging and faces. Approving the draft edit approves the final content.
- **Lessons:**
  - A call without a confirmation token is free and returns a quote. Each paid batch needs the user's explicit yes to that quote, typed in the session that holds it; "continue" does not count. Quote one batch per gate, not per take.
  - Media is kept 7 days: download at once.
  - Make drafts with `generate_audio: false` and build sound in the finish; a copyright-filtered draft audio cannot be fixed at completion.
  - Identical requests are merged into one job; vary the prompt for a second draw.
  - `draft-complete` keeps every defect in the draft, so identity-check drafts as if they were finals. The HD file is not frame-identical to the draft: measure the HD file.
  - MiniMax music returns a full song, not a timed cue; pick a window by measured loudness and pitch. There is no sound-effects model; SFX, voice and lip-sync stay on ChatCut.
  - Image models for the rendering pass ([guides/IMAGE_RENDERING_PIPELINE.md](guides/IMAGE_RENDERING_PIPELINE.md)): Seedream 5.5 Edit, MAI-Image 2.6 Edit, Nano Banana 2.1 Edit. Use only the fields the schema lists.

## Higgsfield (Seedance draft → HD promotion)

Used on Film 6, no subscription since November 2026 (see the platform comparison). Kept for the record:
- Draft at 480p for blocking and the whole edit.
- Promote approved takes to native 1080p by draft job ID, resending the exact prompt, start image and parameters.
- Check the cost preflight: it assumes 5 s unless you pass a duration.

Connect it as an MCP connector in your agent.

## OpenAI Codex app (still images)

Route B for image jobs ([tools/IMAGE_JOBS_FORMAT.md](tools/IMAGE_JOBS_FORMAT.md)). It uses a ChatGPT subscription's image allowance plus Codex agent tokens. Route A is the same prompts pasted by hand into ChatGPT.

## Remotion (React-based motion graphics)

An alternative code route for data-driven or templated motion. Install the Remotion agent skills from Remotion's documentation (remotion.dev, "AI" section) so they stay current.

## Dreamina CLI (optional)

A command-line client for Dreamina image and video generation that the lab tested. Download it from Dreamina / CapCut's official site; the kit does not ship the binary.

## Before any paid call

- Show the board first, with the requirements lock filled in and every row answered ([guides/REQUIREMENTS_LOCK_TEMPLATE.md](guides/REQUIREMENTS_LOCK_TEMPLATE.md)).
- Run the physics and blocking check, and the frame-pair check on every start/end pair.
- Make one short acceptance test per new provider.
- Quote the gate's whole batch once, including a retake allowance, and get one yes.
- Record every take: its prompt, settings, credits spent and output hash.

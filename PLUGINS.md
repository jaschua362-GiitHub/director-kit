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

## Higgsfield (Seedance draft → HD promotion)

Used on Film 6:
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

- Show the board first.
- Run the physics and blocking check.
- Make one short acceptance test per new provider.
- Record every take: its prompt, settings, credits spent and output hash.

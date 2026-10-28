# Directing lessons from Film 6 "The Shadow Apprentice": for every video director agent

27 October 2026. Read this after the [films 1–3 retrospective](RETROSPECTIVE_2026-10-14_VIDEO_AGENTS.md) and the [Film 5 retrospective](RETROSPECTIVE_2026-10-20_FILM5_DIRECTING.md), before planning shots.

**Film:** DCL-20261021-SHADOW, approved final video-portrait-v01 (lab file, not in kit: `FINAL_RENDERED/DCL-20261021-SHADOW/README.md`). It is 9:16, 58.9 s, the longest film so far, with Japanese dialogue and English subtitles. It was directed by Claude Opus 5.5 in `experiments/TEST-013/`.

**Source:** Jason's notes from draft edits v01–v08, the title rounds and the 1080p finish, plus the director's own measurements. Token and cost figures are in TOKEN_AND_COST_COMPARISON.md (lab file, not in kit: `experiments/TEST-013/closeout/TOKEN_AND_COST_COMPARISON.md`).

## The workflow that worked: reuse it

1. **Hand-drawn board until locked.** Jason judges visuals, not text, and "don't waste credit on actual image gen" before the board is locked.
   - Push the action and stances on the sketch.
   - Then make photoreal start frames, from approved art only. Generated frames fed back as references drifted toward comic/CGI.
2. **Face-acceptance test first.** One 4 s draft, 12 credits, before buying into a provider.
3. **Seedance 2.5 draft workflow (Higgsfield).**
   - **Drafts:** 480p at 3 cr/s for blocking, timing and the whole edit.
   - **After the draft edit is approved:** promote by `draft_job_id` to 1080p at 16 cr/s of the *whole take*. Resend the exact draft prompt, start image and params; the backend requires them.
   - **Cost preflight:** it assumes 5 s unless you pass `duration`.
4. **Finish policy (Jason): "if scene can use draft then upscale ourself… hero scene regen in HD".**
   - **Local Real-ESRGAN** (`tools/upres_shot.py`) held up for wides, motion, masked faces, and the cloak refraction.
   - **Native 1080p** went only to unmasked speaking faces and the shots Jason saw go soft (jump, drone): 5 of 24 cuts.
   - **Test before costing:** run one wide and one face through the local upscale first.
5. **Check the take you already paid for.** Twice the fix was already in the clip:
   - the landing look into the lens was at 3.5–5 s of T11;
   - the whip pan was at 3.7–5.4 s of T14.

   Strip a take at 6–8 fps before regenerating.

## What Jason corrected, and the rule

| Note | Rule |
|---|---|
| "Cuts don't join up… wasted the action." Excitement 50%. | **Complete every action before the cut and cut on motion.** Spring → sprint → vault → launch → tuck → land must read as one run. |
| The cloak needed "more excitement". | **A set piece gets its own purpose-built shot** (an orbit as the refraction sweeps), not a trim of a static take. |
| "The scope should capture the decoy running." | **The twist must be on screen.** If the story turns on what a machine sees, show its point of view. |
| "Talking through an empty hand." | **Motivate every gesture.** An earpiece made the comm line read. |
| "Subtitles can go a lot lower." | **Subtitles sit near the bottom title-safe line** (about 0.90 h), clear of the faces. |
| "Scope shot and SFX very amateur." | **Machine POV is designed, never a template overlay:** amber grade, scanlines, converging brackets that snap, live telemetry. Each character's optic gets its own colour language (Kaede ruby, hunter amber). Build it in post (PIL HUD frames), never ask the video model for HUD. |
| | **Sound is designed:** an ambience bed under everything first, then a few cues placed on measured motion peaks, all in one acoustic space. Inside a POV, the world drops away (score low-passed). Normalise to about −15 LUFS. |
| "This tilt shot looks incomplete or a mistake." | **A camera move commits or the shot goes.** Here a TGT-02 alert now motivates a full whip pan. |
| "Not obvious what it's trying to narrate" (scan). | **Tie a POV to whoever is looking:** cut from her goggle flare into the view, sweep the scan, label the target. |
| Ending "sudden", then "the extension is jerky". | **End on a hold plus fade, with room for the title.** Ease into a hold with interpolated slow-down. A push-in must be sub-pixel: zoompan on a 2–4× upscaled frame. Even-pixel `scale` steps jitter every 8 frames. |
| AI-native Japanese speech unclear; weak lip-sync. | **Use clear TTS voices that Jason picks, then lip-sync on-camera lines** (ChatCut, preserve-video). Comm voices get a radio filter. |
| "If she said something her mouth should be moving." | **On a stealth mission, a character on camera need not speak.** Kaede's "Go" became two comm clicks on her wrist tap. |
| Landing should end "looking into the film camera". | **Give the hero a look into the lens at the peak of the run.** |
| Music: score D "too happy". | **Cyber-ninja = cyberpunk fused with Japanese instruments,** in a minor, menacing key. Add the digital and ninja texture through the SFX layer, not a brighter score. |
| Title: "same angle and scale zoom-in", "draggy". | **Animated titles need choreography and scale changes:** spin-ins, crouch, full-body reveal. Use them at natural speed, never slowed to fill time. |
| Title sound: "our own sound design… consistency with our main spot", "more impactful". | **Title hits come from the film's own sound family,** frame-synced, with a sub layer, a reverse swell and a pre-hit silence. End on a complete fade to black, not a fade that stops on the last frame. |
| "Noise / film grain too much." | **Grain 1.0, not 3.2, for 9:16 phone delivery.** Instagram's compression turns heavy grain into mush. Keep a little to avoid a plastic look and banding. |
| Frames "go blurry" in the jump and drone shots. | **Hero motion can be promoted to HD too,** not only faces. |

The climax landed at 55% of the 58.9 s runtime including the title, and 64% of the 50.6 s story. The Film 5 rule (before 60%) held only because the title was added. Plan the turn near 50% of the story runtime.

## Technical lessons: these cost time, so don't rediscover them

- **Frame-exact assembly** (`experiments/TEST-013/assemble_final.py`):
  - Snap in and out points to the 24 fps grid, force an exact frame count per segment, and restamp each frame by index (`setpts=N/(24*TB)`).
  - Use MKV intermediates (MP4 edit lists drop a first frame on decode).
  - Join picture and sound separately; AAC padding makes an a/v concat hold a frame at every cut.
  - Verify with packet counts and a frame-difference scan.
- **Real-ESRGAN GPU fault:** once, the AI frames came back black mid-batch, and the 30% Lanczos blend hid it as a dark shot. `tools/upres_shot.py` now stops on a dark AI frame. **Still compare every upscaled shot's luma with its source.**
- **ChatCut Desktop:**
  - After an app update, an agent session's tools go stale. `chatcut doctor` plus the local launcher (`experiments/TEST-013/finish/chatcut_call.py`) works.
  - Lip-sync needs the project **open in the app**.
  - A source video needs its own audio track.
  - A job that failed for lack of credits needs a new `requestId` once credits are topped up.
- **MiniMax H3 (Higgsfield):**
  - 2K, 4–15 s, 2 cr/s.
  - An `end_image` needs a `start_image`.
  - Land on the approved poster as the end frame, then crossfade the exact PNG over the last second; H3 garbles type mid-motion.
- **PATH ffmpeg/ffprobe are blocked by Application Control.** Use the bundled ffmpeg. `experiments/TEST-013/finish/publish_with_bundled_ffmpeg.py` runs the delivery helper unchanged.
- **Grade:** E1N (E1 plus a night lift) put faces at 42–44% and highlights at about 95%. Plain E1 measured too dark for a phone.

## Token budget for the next film

- **Fresh input plus output per finished second was the best so far:** 32 K/s, against Film 5's 50 K/s.
- **Total processed tokens were high:** 305 M, against Film 5's 67 M, because one 9-hour session re-read its cached history on every one of 694 responses.
- **Split the work into phase sessions with a one-page handoff:** boards locked → draft edit approved → final approved.
- **Use background waits instead of polling.**
- **Reuse the toolchain above.** Details are in TOKEN_AND_COST_COMPARISON.md (lab file, not in kit: `experiments/TEST-013/closeout/TOKEN_AND_COST_COMPARISON.md`).

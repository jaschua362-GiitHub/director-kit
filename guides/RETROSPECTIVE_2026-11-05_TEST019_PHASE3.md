# Retrospective: One Beat Late (TEST-019), phase 3 through final delivery, 3–5 November 2026

**Status:** Jason approved the final on 4 Nov 2026 ("final"). It is delivered to FINAL_RENDERED/DCL-20261030-BEAT (lab file, not in kit: `FINAL_RENDERED/DCL-20261030-BEAT/README.md`). The finish, closeout, spend and token totals are covered [at the end](#finish-and-closeout).

Read after the TEST-018 and TEST-019 pilot retrospectives, before planning shots, music or sound for any film. Film: DCL-20261030-BEAT. Director: Claude Opus 5.5. Phase 3 took the remaining 11 panels from a priced plan to an approved picture cut (music cut v08, plus the later P11 extension) and approved sound (sound cut v11, 34.5 s at 480p). About USD26.3 was spent on Atlas against a USD27.13 cap. Records are in `experiments/TEST-019-one-beat-late/production/`: shot plan (lab file, not in kit: `experiments/TEST-019-one-beat-late/production/SHOT_PLAN.md`), print ledger (lab file, not in kit: `experiments/TEST-019-one-beat-late/production/PRINT_LEDGER.md`), music plan (lab file, not in kit: `experiments/TEST-019-one-beat-late/production/MUSIC_PLAN.md`), sound plan (lab file, not in kit: `experiments/TEST-019-one-beat-late/production/SOUND_PLAN.md`), spend log (lab file, not in kit: `experiments/TEST-019-one-beat-late/production/video/README.md`).

## What worked
- **Shared takes.** One generation covered two board panels twice: panels 3+10, and 5+9. That saved about USD3.7 and kept the plan inside the balance.
- **Free stills, then a visual board, then drafts.** Jason corrected staging on stills before any video money was spent (he stood behind the glass; she stared into the lens).
- **First+last frame for every face shot.** Identity held in all six face takes. `draft-complete` gave native 1080p with no re-roll.
- **Insert plus cut for every under-glass effect.** No generated footage was patched, and nothing ghosted.
- **Music measured, then the picture cut to it.** Tempo and the track's own last note were measured, then panels were conformed to whole beats. The film's 1.3 s delay is exactly 2 beats at 92 bpm, so the concept became audible: a 2-beat echo while they're out of step.
- **Free sound.** Native audio from takes generated with sound on (footsteps, laughs) plus one designed hiss reused for every arrival. Voice was quoted at USD0.0008; nothing else was paid for.

## What went wrong, and the rule
| What happened | Rule |
|---|---|
| A wide's low camera put her on the rim, in front of the glass; the hook print never reappeared. Jason: "if I'm 1st time viewer I will not get why a footprint started." | **Review the cut as a first-time viewer.** Stage wides so the key relationship (on the glass, beside the print) reads at a glance, and carry the close-up's object into the next shot. |
| The last shot "stopped dead". | **End on a motivated closing beat** (a bookend insert, a cue for the next action), then black. Give the music room to ring out over black. |
| Jason asked if prints should still be on the glass. The board never said what happens to a print. | **Write the continuity rule for any persistent effect before compositing,** then trace every instance shot by shot (here, the print ledger: hold 5 s, melt 2 s). |
| Prints came out child-sized in one room and man-sized in the other, and dark stamps on pale grains. | **Scale every print against a body part in the same frame** (boot, shoe, hand), and match shading strength to the floor's brightness, not one value for both rooms. |
| A reaction effect peaked on the last frame of a shot that fades to black, so every version looked faint. | **Check an effect inside the cut, with its fades on, at phone size.** Front-load anything that must read. |
| A hand seen edge-on can only project a strip, so ten parameter sweeps never made a hand. | When parameter tweaks don't converge, **question the method.** Here a real photo relief (Route B, free) applied like the footprints worked at once; procedural shapes read as claw marks. |
| A spiral read as "unnatural ... obvious swirl"; the original swirl even unwound mid-shot. | **Effects should look like a physical reaction to a force,** not a graphic. Check direction: rotations must build one way. |
| An extension cut from the native take looked "stretched and redder". OpenCV decoded the 10-bit HEVC with a different colour conversion from ffmpeg, and a re-encode added more. The join also skipped a frame. | **Decode source clips with the same tool that built the approved cut, match colour on an overlapping frame, avoid extra encodes, and verify the exact join frame.** |
| Generated audio blocked by the provider's copyright filter can't be fixed at `draft-complete`, which inherits the draft's audio. | **Make every draft with `generate_audio: false`**; build sound in the finish. |
| A whispered count was synced twice and still didn't fit. Her lips weren't forming those words. | **Don't add dialogue to a generated face after the fact.** Let the sound design carry it, or generate the line with the performance. |
| A saturated "watch speaker" filter turned a laugh into a "hurrz". The first hiss mix was too loud, twice. | **Mix the designed layers quieter than feels right,** and check each cue against the music under it, by measured level. |

## Process notes
- **Paid confirmations:** each batch was quoted, and Jason typed yes in this session. Pre-authorising "resubmit with audio off at the same price" saved round trips.
- **Sonnet subagents** built the composites well from tight specs, including measured checks and every-frame sheets. One stopped at the usage limit and resumed cleanly from its saved work.
- **Session length:** this session ran very long. Per the token rule, the finish (1080p and grade) should start in a fresh session from the handoff.

## Finish and closeout
The finish ran in a fresh session from the handoff (lab file, not in kit: `experiments/TEST-019-one-beat-late/production/NEXT_PHASE_HANDOFF_FINISH.md`); its record is finish/README.md (lab file, not in kit: `experiments/TEST-019-one-beat-late/production/finish/README.md`). Nothing was paid for. The final is 1920×1080, 828 frames (34.5 s), grade G1, with the approved mix.

| What happened | Rule |
|---|---|
| Before touching anything, the finish hashed every approved file and proved the 1080p flags by re-running each composite at 480p: the output was bit-identical to the accepted cut. | **Prove the higher-resolution re-run is the same recipe** with a bit-identical low-resolution re-run. Keep script edits backward-compatible, and hash approved inputs before and after. |
| ffmpeg `trim` piped to rawvideo inserted a repeated frame every 25 frames. | **Pass `-fps_mode passthrough`** on frame-exact pipes, and check timing against the approved cut frame by frame (828 = 828, offset 0 per event). |
| The Lab's E1 grade made faces 50–54% and blacks 7–10% here. | **Grade per film against the measured targets.** A house look is a starting point, not a rule. |
| AAC encoding raised the true peak from −1.3 to −1.1 dBTP. | **Leave about 0.5 dB more true-peak headroom** than the delivery target, or measure after encoding. |
| SeedVR2 needed the GPU cleared: 5.4 GB was in use against a 3.5 GB limit. P01 and P04 were upscaled to 1440p for crop headroom on the slide and the rotation. | **Ask Jason to close GPU apps at the start of a finish.** Upscale above 1080 wherever a local camera move crops in. |
| Draft caption notes said the ambience came from the "ChatCut library". In fact every room tone and Foley sound was designed locally, because ChatCut was unavailable. | **Write the true source of every sound layer into the sound approval** (native / designed / library / generated voice), so caption AI lines can be checked against it rather than remembered. |

**Closeout.** The film folder follows the social-materials standard. It holds:
- the approved final;
- the approved v04 art copy;
- the approved posters;
- the approved captions (byte copy);
- seven film stills;
- 2× upscales of the 30 approved stills.

package_final_delivery.py (lab file, not in kit: `experiments/TEST-019-one-beat-late/closeout/package_final_delivery.py`) rebuilds and re-verifies the folder.

### Final spend (Atlas, pay-as-you-go)
| Phase | USD |
|---|---|
| Panel 11 pilot (2 drafts + 1 finish) | 4.33 |
| Phase 3 video (drafts, retakes, six 1080p finishes, P12 hand take) | about 25.96 (one top-up hid a charge, so about 5.37 of this is an estimate from its 5.51 quote) |
| Music (MiniMax Music 3.0, 2 takes) | 0.30 |
| Voice test (MiniMax Speech, removed from the film) | 0.0008 |
| Stills, posters, composites, SeedVR2, sound design, grade, closeout | 0 (Codex Route B and local) |
| **Film total** | **about 30.6** |

Phase 3 stayed inside its USD27.13 cap (about 26.26).

### Claude Code tokens (from the session transcripts, subagents included)
| Session | Output | Cache write | Cache read | Models |
|---|---|---|---|---|
| Video direction (coordinator) | 143 k | 1.82 M | 49.7 M | Opus |
| Panel 11 pilot | 176 k | 0.41 M | 55.7 M | Opus |
| Phase 3 director (this retrospective) | 884 k | 3.77 M | 320.5 M | Opus 553 k + Sonnet subagents 331 k output |
| 1080p finish | 193 k | 0.60 M | 47.0 M | Opus 105 k + Sonnet 88 k output |
| **Total** | **1.40 M** | **6.60 M** | **472.9 M** | |

Uncached input was about 3 k tokens. Codex usage (Route B stills and posters) is not counted here.

**Takeaway:** about 68% of the cache reads came from the one long phase 3 session. Each turn re-reads the whole context, so cost grows roughly with the square of the session length. Phase sessions should end at each approval gate (board, cut, sound, finish) and hand off through a file.

## Token debrief (Jason, 4 Nov 2026): read before planning a film

Jason: the film looked easy, but the footprint rounds burned a lot of tokens. The full report (lab file, not in kit: `experiments/TEST-019-one-beat-late/closeout/TOKEN_REPORT.md`) has the numbers. One Beat Late used 487 M processed tokens: 4× Evade and Escape (118 M) and 1.5× Himmapan (326 M). Subagents were only 12%, and the cheapest work per step. The cost came from one 60-turn phase 3 session whose context grew from 257 K to 960 K. About 45% of that session went on footprint, grain and melt rounds that were designed during the edit.

Rules for every director:
1. **Approve locally built effects before production:** a one-page effect sheet (sizes per person, shape, timing, what persists or melts) plus a 2-second test clip, approved once.
2. **Ask Jason for one batch of notes per review.** Each separate note re-reads the whole session.
3. **Break sessions at every approval gate,** or once context passes about 300 K, with a one-page handoff.
4. **Subagent hand-backs are one contact sheet plus a pass/fail line.** The director reviews only that.
5. **Posters, captions and the posting kit go in a fresh Sonnet session,** not the director's.
6. **One spend approval per gate, not per generation** (Jason, 4 Nov). Quote the gate's whole batch, including a retake allowance within the cap. His yes covers every take in it. Subagents and phase sessions never message Jason; they report to the director, who brings him one message per gate. The Atlas connector still needs a user confirmation on every quote, so batch quotes into a single "submit all".


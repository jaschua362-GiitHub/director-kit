# Directing lessons from TEST-018 "Cyber Ninjas: Evade and Escape", for every video director agent

3 November 2026. Read after the Film 7 retrospective, before you plan shots or spend anything.

**The film:** a 9:16 Cyber Ninjas side spot, wordless, 27.9 s of story plus the series end tag. Directed by Claude Opus 5.5 in `experiments/TEST-018-cyber-ninjas-escape/` on **Atlas Cloud Seedance 2.5** (480p drafts, then `draft-complete` to native 1080p), with a USD25 cap that included audio. It finished at USD22.29 and was approved on 3 Nov; the Instagram Reel is scheduled for 18:00 that day.

**Records:** platform comparison (lab file, not in kit: `experiments/TEST-018-cyber-ninjas-escape/closeout/PLATFORM_COMPARISON.md`) · token breakdown (lab file, not in kit: `experiments/TEST-018-cyber-ninjas-escape/closeout/TOKEN_BREAKDOWN.md`) · Atlas provider test (lab file, not in kit: `experiments/TEST-018-cyber-ninjas-escape/closeout/PROVIDER_TEST_ATLAS.md`).

## The workflow that worked

1. **Free price check at the board lock.** Quote-only calls cost nothing, so the budget was checked against real per-second prices before any spend. The plan and its guard were written down too: "if completion costs more than 0.60/s, finish only the climax natively".
2. **Draft → draft edit → native completion of the approved draft.** Atlas `draft-complete` returned the approved draft's motion, staging and faces exactly at 1080p. **Approving the draft edit therefore approved the final content.** The finish had no re-roll risk and no re-review loop.
3. **Native 1080p for every readable face.** SeedVR2 handled the one shot that didn't need it (it passed even with a face in it, as a reviewed exception). The quality bar held and the cap held.
4. **Sound by stages.** The drafts' native Foley carried A and B. One MiniMax cue came in at lift-off and faded out *before* the series end tag, which kept its original sound.
5. **One session per phase.** Board, drafts and finish each ran in a fresh session with a one-page handoff. This film used the fewest processed tokens per finished second so far: 3.8 M, against 5.2 M on Film 6 and 10.0 M on Film 7.

## What went wrong, and the rule

| What happened | Rule |
|---|---|
| D01-B and D02-B: Kaede **turned into the enemy robots** in a dense fight shot. Jason: "why is Kaede becoming the enemy robot yet the next scene she is herself". Segment B had to be rebuilt as three single-action shots: 3 extra drafts and the most expensive token phase (16%). | **Seedance blends identities in dense multi-character shots, especially a transparent or camouflaged character.** At the board stage, give that character a shot of their own and keep each shot to one action. Don't fix this by trimming. |
| The camouflage switch "didn't add any action" and then looked "rushed, not refined". | **A power that matters gets screen time and a consequence.** Give the switch its own beat, long enough to read, then show what it achieves (here the step around and the kick). |
| Draft C ran through the wall. | **Check every wall, rail and door frame frame by frame for pass-through** before the draft edit goes to review. |
| The finish route changed three times mid-phase: upscale faces, then test SeedVR2 on faces, then spend the balance on HD. | **Fix the finish route at the draft-edit approval:** a per-shot table of native / SeedVR2 / Real-ESRGAN with costs, approved once. |
| A paid confirmation relayed from another session was refused, costing a round trip. | **Paid confirmations are typed in the session that holds the quote.** Relay the quote to Jason, not his "yes" back to the session. |
| The drafts session stopped at the usage limit for 2 h 20 m and reloaded its whole context on resume (about 0.4 M fresh tokens). | **When a limit is close, write the handoff first,** then resume in a fresh small session. Don't wait in a long one. |
| Closeout, posting kit and Metricool ran inside the long Opus finish session: **20% of all tokens, more than the finishing itself.** | **End the finish session once the final is approved.** Do the post copy, kit and scheduling in a fresh Sonnet session that reads only the closeout folder. |
| A Haiku subagent's Atlas research came back unusable (no schemas, prices without units). | Give Haiku **narrow look-ups only, with exact tool names and the expected output format.** Use quote-only calls for prices and parameter names. |
| Kaede's ruby goggles drifted to a clear visor in A's close-up, and `draft-complete` carried it into the final. | **Completion keeps every defect in the draft.** Identity-check the draft as if it were the final before you approve the draft edit. |

## Provider and cost notes

- **Atlas Seedance 2.5:** draft USD0.134/s; `draft-complete` about 0.611/s, billed on the **full** draft length (you can't trim first). Charges came in 3–4% under quote. Our photoreal faces were accepted. **Media is kept 7 days, so download immediately and finish within 7 days of the drafts.**
- **Quote protocol:** a call without a token is free and returns a quote. Each paid batch needs Jason's new, explicit confirmation of that exact quote; "continue" doesn't count.
- **Music:** MiniMax music-3.0 (USD0.15) returns a full song, about 133 s, not a timed cue. Pick a window by measured loudness and end it before the end tag. Captions need an AI-generated disclosure line. Don't use Suno (its rights through Atlas are unverified).
- **Atlas has no dedicated sound-effects model.** Sound effects, voice and lip-sync stay on ChatCut.
- **Route for the next film** (see the platform comparison):
  1. ChatCut Plus monthly credits first, with a `fromDraft` 1080p test on the first face shot.
  2. Atlas for overflow, for any film before 12 Nov, or if `fromDraft` fails.
  3. Decide the route per film at the board lock, because Atlas can only complete its own drafts.
  4. No annual plans, no Higgsfield subscription.

# Hold the Note re-run through the improved pipeline: a simulation

Jason, 7 Nov 2026: "simulate if we can create the exact but better pipeline n lesser budget spend and token we should improve it next time".

This takes the **same film at the same final quality** (v03: Korean dialogue, a real flute phrase, the modern-sageuk cue, the epigraph, native-HD distant faces, both formats) and replays it through the rules adopted on 6 and 7 Nov. Actual figures are measured (`tools/token_count.py`, `closeout/TOKEN_REPORT.md`, P5_STATUS). Simulated figures are estimates, built from the reply counts and context sizes below. Read them as a plan, not a promise.

## How the tokens are made

Every reply re-reads the whole session context, so **tokens ≈ replies × average context**.
- **Phase 5C actual:** 634 replies × about 310 K average context ≈ 196 M in the main session.
- **The same work at about 300 replies × 150 K** comes to about 45 M.

The saving comes from two levers, and neither removes a quality step:
1. **Fewer replies.** Requirements are locked up front, notes come in one batch per review, and there are no relays.
2. **Smaller context.** Hand off by about 200 K, and run loops in fresh small sessions.

## Phase by phase

| Phase | Actual tokens | Actual credits | What wasted it | Improved pipeline | Sim. tokens | Sim. credits |
|---|---:|---:|---|---|---:|---:|
| 1. Board and coordination | 67.3 M (incl. 7 Nov posts and relays) | 0 | Relaying status pings; post rewrites done in the coordinator | Board plus **requirements lock** (16 rows) plus a **rough local preview** with temp music, flute phrase, epigraph and title. No relays. | 25 M + 10 M coordinator | 0 |
| 2. Start frames, effects, subtitle frame | 56.6 M | 0 | Three rounds with the camera side or look direction wrong; two subagent rounds per effect; long waits | Camera side **and eye-line** written in every prompt; frame-pair overlay check; each subagent spec sent once with pass criteria; submit and end the turn | 18 M | 0 |
| 3. Dialogue pilot | 35.4 M | 6.29 | 이을게 failed speech-to-text only after the paid pilot | TTS + speech-to-text check of every line at the lock (free) catches 이을게 → 불게 before the pilot | 10 M | 5.00 |
| 4. Drafts and edit, both formats | 62.8 M | 22.10 | D1/D2 retakes | Frame-pair check before paid first/last-frame jobs | 28 M | 18.35 |
| 5. Sound, finish, grade, title (5, 5B, 5C) | 304.7 M | 21.07 | Music, flute phrase, title motion, black, caps and epigraph all arrived during the finish; shot 10 prop morph and its retake loop; about 15 republishes, one note at a time; 5C at 712 K peak | Everything already locked; **face route set by size at the finish gate** (under about 60 px means native 1080p, one batch quote); retakes in a fresh Sonnet session; one batch of notes per review; three sessions of 200 K or less | 65 M | 42.00 |
| 6. Closeout and posts | 31.4 M | 0 | Additions mid-run; kit only local | Post voice per platform known up front, every platform drafted at once, kit published as an Artifact first time | 12 M | 0 |
| 7. v03 distant-face retake | 112.6 M | 37.80 | SeedVR2-first on small faces, found only at full-size viewing; the shot 13 eye-line was in the approved start frame; the director's audit passed 12V | **Doesn't exist.** The native face takes move into phase 5, and the eye-line is fixed at phase 2 | 0 | 0 |
| **Total** | **670.7 M** | **USD 87.26** | | | **about 168 M** (range 150–190) | **about USD 65** |

Simulated phase 5 credits, built up:

| Item | USD |
|---|---:|
| Dialogue completes | 9.19 |
| Audio | 0.55 |
| About 12 native face takes (as in v03, including 12V) | about 30 |
| One HD for shot 10, frames matched first | about 2.30 |
| **Total** | **about 42** |

Shot 13's 7.54 retake and the shot 10 regenerations disappear.

## What changes, and what doesn't

**About 4× fewer tokens and about 25 % less credit, for the same film.** The credit saving is smaller because most of the credit was necessary: the native faces cost the same whether they are bought in phase 5 or phase 7. What disappears is buying twice:
- the SeedVR2 route, then native;
- shot 13 twice;
- shot 10's loop;
- the D1/D2 retakes.

**A further option, a creative call at the lock:** reframe the 9:16 from the 16:9 take on shots where staging allows. That worked for shot 4. Two or three more shots would save about USD 5–8, bringing the credits to about USD 57–60. It is only a saving where the faces still pass at 100 % after the crop.

**Nothing on the quality list is cut:**
- three board versions;
- the Korean line check;
- the dialogue pilot;
- the flute phrase, the score and the epigraph;
- native-HD faces;
- every-frame composite checks;
- the cold critique;
- Jason's review at every gate.

## Where the estimate could be wrong

- **Jason's own new ideas still arrive late sometimes,** and they're welcome. The rough preview is meant to surface them early, but it can't catch everything. Each late item costs its reopen, which the director quotes before doing it.
- **The 200 K handoff was a rule on this film and still wasn't followed:** all 10 sessions went past 250 K. The simulation depends on it being followed. The gate token line (brief §2026-11-06 rule 8, peak context per session) is how a miss gets seen at the gate instead of at closeout.
- **Model behaviour varies.** A new morph or failed take still costs a retake. The rules make that one retake, not a loop.

## The checklist for the next director

1. Requirements lock plus rough preview at the board gate. Every row answered, including deferred source items.
2. TTS + speech-to-text check of every dialogue line before the paid pilot.
3. Start frames: camera side, look direction and eye-line in words in every prompt; frame-pair overlay before any paid first/last-frame job.
4. Finish route by face size at the finish gate: under about 60 px means native 1080p in one batch quote. SeedVR2 for faceless shots and for faces that pass at 100 %.
5. Final face audit: 100 % crops of every face on the master, both formats.
6. Hand off by about 200 K context. Retake loops go in a fresh Sonnet session. One batch of notes per review. No relays.
7. A token line with peak context in every gate message.
8. Closeout: all platforms drafted at once in the agreed voice; kit published as an Artifact.

Related:
- `RETROSPECTIVE_2026-11-06_TEST020.md` §1–11
- `VIDEO_DIRECTOR_BRIEF.md` §2026-11-06 and §2026-11-07
- `REQUIREMENTS_LOCK_TEMPLATE.md`
- `experiments/TEST-020-hold-the-note/closeout/TOKEN_REPORT.md`

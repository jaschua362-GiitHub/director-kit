# Directing lessons from Film 5 "After You" — for every video director agent

20 October 2026. Read this after the [films 1–3 retrospective](RETROSPECTIVE_2026-10-14_VIDEO_AGENTS.md) and before planning shots. Jason asked for this to be shared with all video director agents, whatever model or platform runs them.

**Source:** Claude Opus 5.5's critique of the approved Film 5 v04 (DCL-20261019-AFTER, directed by GPT-6.1 in Codex), plus Jason's own notes from v01–v04. The full critique is at reviews/DCL-20261019-AFTER-claude-2026-10-20/CRITIQUE.md (lab file, not in kit: `reviews/DCL-20261019-AFTER-claude-2026-10-20/CRITIQUE.md`) (lab-only link).

**Evidence limits:** the critique was made from stills and process records, with no sound and no normal-speed playback. These are directing rules, not a model ranking. Some Film 5 choices (added dialogue, the "no pause" rule, the quick "Thank you" ending, 16:9 only) were Jason's; the rules below are about what the director owns.

## What Film 5 did well — keep doing it

- Identity of the character and robots held across every shot.
- Exposure stayed in a normal key; nothing was darkened to hide CGI.
- Budget was respected, and provider failures were diagnosed instead of blindly resubmitted.
- A failed experiment (standalone lip-sync) was rejected honestly and kept out of the film.
- A 9:16 version that would have needed 65% AI-generated canvas was correctly declined.

## What went wrong, and the rule that prevents it

| Film 5 fault | Rule |
|---|---|
| The surprise started at 23.8s of 34s (70%) and got about 5s. Most of the runtime was logistics: UI, walk, talk, passage, door. | **Climax before 60% of runtime. Payoff and reaction get at least a third of the film.** Hook the viewer within 3s with action or a question, not a label shot. |
| A 10-second, six-line conversation played as one locked two-shot. The title line had no close-up, and the protagonist was cramped at the frame edge, face turned away. | **Dialogue gets coverage: at least 3 setups, cut on lines.** The key line gets a close-up. The speaker's face is readable. |
| The door passage and closing took 8.9s in two static wides. | **Necessary logistics are compressed through cutting and camera movement.** One reverse angle can often show several continuity facts at once (door sealed, robots inside, Wen outside). |
| The visible cause of the bow from the synopsis (light climbing the pillar) was dropped, so the bow just happened. | **Keep the cause-and-effect link visible.** If the surprise is a consequence, show what triggers it, with sound as well as picture. |
| The roof reveal was a cut to a 1.8s wide with a small movement. | **Reveals are motivated.** The character's eyeline leads the camera to the surprise, the surprise is held long enough to read, and the motion is big enough to see on a phone. |
| The approved emotional turn (bow back → realise she bowed to a building → laugh) was replaced by an upward smile. | **Protect the approved payoff.** When a user note seems to conflict with it, propose a version that satisfies both before dropping it. A reflexive bow is continuous action, so it doesn't break a "no pause" rule. |
| At 14.8s → 15.0s the carrier appears inside, then back at the threshold, and passes through again. Nobody flagged it. | **Check object state across every cut**: who is inside or outside, which hand is on what, how far the action has progressed. |
| Jason caught most continuity faults across three revision rounds: UI-to-door link, door not fully closed, robot positions, distance from the door, eyeline, environment morph, static roof, arrival too brief, face too short. | **The director catches these before review.** See the checklist below. |
| Fixes were trims and optical-flow slow-downs (arrival stretched 31 → 45 frames) instead of new shots. | **Reshoot a missing beat; retime only for polish.** A shot that has to be slowed down to register was never planned to carry that beat. |
| No geography plan or timed animatic existed before paid motion, and the plan wasn't rebuilt when dialogue was added mid-production. | **Plan before credits** (next section). Re-plan whenever the story changes. |
| Status reports were dense ledger language ("34.4 reserved from39 anchor,4.6 uncommitted"). | **Review notes for Jason are 5 plain lines**: what changed, what to watch, at what timecode. Hashes and budgets stay in the JSON files. |

## Before any paid video generation

1. **Top-down blocking map:** door hinge and swing, glass and walls, inside/outside zones, every character's position per beat, numbered camera positions, screen direction and eyeline targets.
2. **Timed animatic:** keyframe stills plus temp voice, cut to time. Use it to check where the climax lands, how long each beat lasts and whether each shot has a purpose. This is a self-check, not a new approval gate; share it only if useful.
3. **One world:** derive every first frame from the blocking map and one master environment plate per camera axis. When two shots share continuous action, seed the next clip from the last frame of the previous one.
4. **Vertical intent at the storyboard stage:** if the film will be a Reel, frame the hero shots vertical-safe now. Don't try to reframe a finished 16:9 film later.

## Before Jason sees a review — director-owned checklist

- [ ] Climax before 60% of runtime; first 3s give a reason to keep watching.
- [ ] Every dialogue line has a readable face; the key line has a close-up.
- [ ] Object/character state matches across every cut (inside/outside, door state, hands, positions).
- [ ] Doors, gestures and movements complete; motion continues across cuts in the same phase and direction.
- [ ] Eyelines aim at the actual target (robot, roof, object), with head and pupils both.
- [ ] Frozen-element scan: region-based frame-difference at full frame rate on every clip (catches a static roof or a stalled object).
- [ ] Morph scan: dense full-resolution background sheets per shot plus ±6 frames around every cut (gradual morphs don't spike in a difference scan).
- [ ] The surprise movement is clearly visible at phone size.
- [ ] The final expression gets enough time before the fade.
- [ ] The approved emotional turn is present, or the departure is labelled a director variant with a reason.
- [ ] The review note is 5 plain lines with timecodes.

If any box can't be ticked, fix it or name it in the review note. Don't hand the check to Jason as "normal-speed perception remains user review".

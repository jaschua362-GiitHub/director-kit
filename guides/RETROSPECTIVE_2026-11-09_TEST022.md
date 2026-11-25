> **Archive since 12 Nov 2026.** The current required reading is `craft/DIRECTOR_CRAFT.md` and its cards in `craft/cards/`; start at `START_HERE.md`.
> This file is kept unchanged below as the record. Nothing in it overrides the craft page or cards.

# Retrospective: Small Cargo (TEST-022, DCL-20261104-CARGO), 9 Nov 2026

For every director agent. Read it before planning a film. Written at closeout by the board-gate session from `experiments/TEST-022-small-cargo/` (`REQUIREMENTS_LOCK.md`, `DIRECTOR_TREATMENT.md`, `PHASE2_LOG.md`, `PHASE3_LOG.md`, `CLOSEOUT_HANDOFF.md`, the three Codex critiques in `reviews/`) and the seven session transcripts. Token and credit figures: `lab file, not in kit: TOKEN_REPORT.md`.

The film: 45.5 s (39.5 s picture, 0.5 s black, 5.5 s end title), 16:9 master and a 9:16 reframed from it, English dialogue with a light Singaporean-inflected accent spoken by the video model, four utterances on three shots, 15 shots. Source frozen 7 Nov (photo-plates-v10), board locked 7 Nov night, 16:9 master approved 8 Nov ("all approve"), 9:16 approved 9 Nov ("All approved"), poster and copy approved 8 Nov, Instagram Reel scheduled for 10 Nov. About two days from board gate to delivery. Spend about USD 55 against a USD 58 cap; 715 M processed tokens against 135 M.

## 1. The board gate held; the lock mostly held

What worked, and should stay:
- **Three critique rounds before the lock** (Codex on v02, v03, v05) each found something real: one continuous cassette, movement proving life, the viewer arm's travel, shot 10 restaged so face, arm and beam share one 9:16 window, the acceptance test with dialogue muted. Jason's own notes (frontal low arrival, a living organism as the hook, a space-style title in Aboro) shaped v02 to v04.
- **Framing specified at the storyboard stage** (lens, position, side, move, focus, 9:16 window per shot, with a vertical mock on every card). The 9:16 phase measured the master and changed nine window centres, each with a reason, but no shot had to be restaged.
- **The REQUIREMENTS_LOCK with every row answered.** Only one row was deferred (music) and it was tracked. The rows that were answered did not come back: title, SFX plan, finish routes, formats, typography, captions (then withdrawn by Jason, section 10), ending, deferred items.
- **Approvals at gates, one batch quote, typed yes.** Every paid job had a live quote and his yes; expired quotes were re-quoted at the same price and his yes asked again; the permission classifier blocked one submit that had no explicit yes (round 34), correctly.

What the lock did not hold: music (section 5), shot 7's length (4.4 s to 5.0 s, because HIM-B's line runs 3.4 s) and the title length (4.0 s to 5.5 s, Jason's request after seeing the motion). All three were amended in writing on 8 Nov.

## 2. Tokens: 715 M, and one session that ran six gates

Phase 2D opened as the pilot-batch review and finished with the approved master: pilot gate, 12 drafts, finish, fifteen cuts, music, the shot 5 retakes. 918 replies, 397.6 M processed, peak context 966 K. Every session on the film peaked above 250 K; the board session alone reached 641 K.

The rule existed twice over (VIDEO_DIRECTOR_BRIEF 6 Nov, Hold the Note retrospective section 2) and was reported as missed at the pilot gate, then ignored. The handoff file for the next phase was written and the same session continued past it.

**Rules (replacing the soft version):**
- **A gate is a session boundary.** The session that quotes a gate writes the next handoff and stops. Jason's yes starts a new session from the handoff. No session runs two gates.
- **A retake loop is its own small session** with the take's files only.
- **One review page version per batch of notes.** Ask for all notes before republishing. The pilot page reached 35 versions.
- **Budget 9:16 and closeout realistically.** They took 182 M against 20 M (section 9 and 10 explain why).
- **Mechanical batches go to subagents** (downloads, hashes, scans, sheets). Small Cargo used 0.9 M in subagents; Hold the Note used far more and its main contexts were smaller for it.

Quality was not traded for tokens: no check was skipped. The waste was context, as in every film before it.

## 3. Credits: USD 55 under a USD 58 cap, the first film under its cap

Why it held:
- **480p drafts first, native 1080p only on approval**, and every face or hand shot native (lock row 11). SeedVR2 was tried on faces once more (shot 5, a 25-px face) and invented spectacles; the native rule stands.
- **Cheap models for calm wides.** Vidu Q3-Turbo at USD 0.27 per 1080p shot replaced SeedVR2 upscales that Jason read as CGI. Three wides and the hangar retake for about USD 2 total.
- **Free local work where a model would have been bought:** the shot 11 roots (three versions), the shot 7 tail fix, the title motion (three versions), the shot 11 and title sound, the suspense underscore that was later replaced, the film finish, the 9:16 reframe (USD 0.23 for six stills).
- **Seed Audio SFX billed USD 0.09** for eight cues against 2.29 quoted: Atlas did not charge the cues that failed on concurrency and were resubmitted. Check the bill, not the quote.

Where it went: Seedance about USD 45 (drafts 7, finish 20, pilots 9, retakes 9); shot 5 alone about USD 12 (section 4).

## 4. Shot 5: USD 12 and seven drafts for a living dock

The courier's walk off the ramp through the busy dock was the film's most expensive shot by far: drafts D2 to D7, three HDs, a Vidu and a Kling retake, a Seedream end-frame edit. Each round answered one of Jason's observations: he walks on the spot; his head leaves frame; the background crew and vehicles are frozen; the right side is frozen while the left moves; a second spacesuited figure appears; the hangar reads CGI; the hangar's contrast does not match its neighbours.

What was learned, measured:
1. **Background life in image-to-video comes from concrete, person-sized actions in the prompt**, not from the end frame. The hypothesis that the end frame pinned the extras was tested (end frame edited with the crew moved on) and disproved: the short-prompt draft had less motion than the long-prompt one.
2. **Distant vehicles never drive.** Three models, seven drafts: the carrier stayed parked every time. Do not promise a moving vehicle in a wide; cut around it or put a person in front of it.
3. **A 25-px face cannot be carried by a 480p draft or by SeedVR2.** Anchor identity with an end frame (the approved close, registered to the start geometry) and buy native 1080p.
4. **Show every draft before its HD, even inside an approved batch.** Jason: "Should have show me draft before proceeding." A right-side motion score of 1.1 against 5.8 on the left was played down and cost an HD. Memory `show-drafts-before-hd`.
5. **His viewing overrides the tile metric.** D7 measured less motion than D5 and he accepted it: "Moving is better then anything is freeze." Report the number plainly and let him judge the picture.
6. **Collect all notes on the cut before quoting a batch.** Jason: "lets handle all new request before Q all to rerender." The two rerender batches that followed were cheaper than the one-at-a-time rounds before them.

## 5. Music was decided by ear, four times

The board said "no music, sound effects and acting carry the film" (Jason, v03). At the lock he was unsure, so row 4 was deferred to an A/B at the rough cut. Then: B, a sparse cue under 12-15; then "need a subtle music throughout as is felt quite silent ... build suspense from start"; then the synthesised underscore plus the Suno resolution felt "very disconnected and not cohesion"; then "the music is too smoothing n classic ... should be more build suspense sci exploration feel"; then one Suno sci-fi take, "Take 1 work. but it need to be sync the sound intensity according to the scene build up"; then approved with a per-scene intensity curve. Six cuts, two Suno quotes, USD 0.26.

What it shows:
- **A "no music" call made on a storyboard does not survive hearing the cut.** Deferring the decision to the rough cut was right; the A/B offered the wrong pair. Offer three: none, one sparse cue, one continuous line, and put the continuous line in the rough cut so the silence is a choice heard against music, not imagined.
- **One real cue riding an intensity curve beats layered synthesised stages.** The "sound by stages" rule (silence, natural sound, score at the climax) was realised as one continuous Suno line whose level follows the scene (space barely audible, building to the hook, a second peak on his breath, the take's own fade under the title), not as separate pieces. The stitched version read as disconnected.
- **Measure the take before choosing it**: take 1 C minor with a natural fade, take 2 G major ending loud. Pitch class and ending decided it, as on Hold the Note.
- **The title had a sound design because he asked for one** ("design a end title sound design"), built only from the film's sound world and then mellowed ("abit too sharp ... as is in space"); the film cue continues under it. The Lab's "no title SFX" rule is his default, not his law: lock row 7 should ask the question outright.

## 6. Seedance snaps at both ends: scan every take

Every Seedance take with a start or end frame snapped into or out of the design frame within its first or last 2 to 4 frames, sometimes anisotropically (shot 7's last frames squeezed about 1 % horizontally and not vertically; shot 11's field narrowed 5 px; shot 3's first frame stretched 1.3 %). Jason saw each one as "the footage compress width" or "the frame stretch horizontally".

**Rules:**
- Run a consecutive-frame background affine scan on every take before review (`finals/scan_geometry.py`, whole cut). Never use frame 0 or the last 2 to 4 frames of a start/end take: trim, or resample the tail into the last stable frame's geometry (`finals/s07_fix/fix_ends.py`).
- A take acceptance test, as the Hold the Note retrospective asked for, now exists and worked: the scan found shot 3 and shot 11 before he did.
- **Two false alarms cost rounds.** A review clip that spliced the opening onto the ending at half speed read as a jump cut in the shot; a coarse template track read a natural eased head raise as a one-frame snap. Never splice non-adjacent ranges without a visible separator (Jason scrubs frame by frame), and check the velocity profile over plus or minus five frames before calling a one-frame jump.

## 7. The image pipeline and the dialogue route worked

- **Codex design frames (free) re-photographed on Seedream 5.5 Edit with the approved photo plates as identity and material anchors** (IMAGE_RENDERING_PIPELINE stage 2) gave start frames Jason accepted at the first pass for 14 of 15 shots. No Codex frame was ever a Seedance input. Shot 1 went straight to Seedream from the plates when the design read as CGI.
- **The 2x check caught continuity before any video was bought:** a bare glowing capsule where the cassette should be, two look-alike cases on the carrier, a flat glove, a bare hand, and a microscope base that stood left of the cradle in the start and right in the end (Jason found that one). **Rule added:** check that a fixed prop's mount and anchor agree across every start/end pair, not only poses and hand props.
- **Native Seedance speech with the accent in the prompt beat TTS plus lip-sync.** Twelve TTS auditions and nine older-voice retries were cheaper than one lip-sync pass and still lost to the native take. Speech-to-text on every spoken take (word-perfect on the finals); her voice on shots 10 and 12 matched to shot 7 by F0 (147 and 152 Hz; the 195 Hz draft was checked by ear). The last line of shot 7 L-cuts 0.31 s into shot 8 by his choice.
- **Short, plain prompts for the shot; long, concrete prompts only for background life.** The same lesson as Hold the Note's shot 10.

## 8. Calm wides: cheap native beats upscaled drafts

SeedVR2 on the 480p drafts of shots 1, 4, 8 and 15 passed the 100 % check and Jason still rejected the look: "is sharp but had that CGI look." A one-shot bake-off (Vidu Q3-Turbo USD 0.27, Kling 3.0 Pro 0.71, against Seedance draft plus HD 3.02) picked Vidu as the most photographic. Kling was the most naturally lit but drifted identity and, on the hangar, mismatched its neighbours' contrast; the hangar went back to Seedance 2.5 HD.

**Rules:** for a wide with no readable face, quote a cheap native 1080p model first and the Seedance HD second; SeedVR2 is a fallback, not a route. Match the colour statistics of a cheap-model shot to its neighbours before judging it (`hue s=` and the L/sat/b table in the log). Vidu clips can carry repeated frames (shot 1, steps 24 and 48) and an audio track: retime with flow interpolation and drop the audio.

## 9. The 9:16: reframe-and-extend, with the extension done as stills

Jason chose reframe-and-extend over Hold the Note's native vertical takes on 7 Nov ("might need to reframe from 16x9 and extend"), for cost and for one performance across formats. Asked at closeout why the workflow changed, the record is: his note after the v02 critique, taken into lock row 1; the director's reasons for agreeing were credits (GPU hours instead of a second set of paid takes, speech and organism takes), continuity (the same acting in both formats) and the two-shot fix by wider source windows. The trade-off is that extension can only invent background, so the Reel is bounded by what the 16:9 take holds.

What happened: the framing preview was approved after one round of his window notes (shots 2, 6, 8, 10, 15, with A/B options on 2 and 10). Wan VACE per-frame band fill then ran about six hours and failed on three of five shots: an invented woman walking down a corridor under shot 7, a blank slab and a giant ceiling fixture on shot 12, a cabin roof sliding against parallax on shot 2. Jason's fix: "the camera is a lock shot ... extension in seedream ... post crop composite top n bottom. As a still." Six Seedream stills (USD 0.23), each tracked to the background with per-column correction at the join, heads crossing the join handled with caps over an empty-room plate, took the 9:16 to approval in seven drafts.

**Rules (memory `vertical-extension-still-method`):** on locked or slow wides, extend with one generated still per shot, tracked locally; per-frame video fill is the fallback for real camera moves only. Reframe pans faster than about 7 px per frame at 24 fps strobe on a phone: add a 180-degree shutter blur. A locked-off hold that stops the flow (shot 8) can take a continuous push-in in the vertical. Audit the extension at 100 % on the join and at 200 % where heads cross it, in motion, before showing it.

## 10. Closeout: key art, no captions, copy shortened

- **The poster is the main character.** Three scenic lockups were built from the brief; Jason chose none of them: "i prefer using the old courier in the spaceship as characters design is one of the keyart we would want to post in IG." Lockup D (the approved cockpit plate, title under the case, the plate extended by one masked outpaint for USD 0.15) was approved in three rounds. Memory `poster-key-art-main-character`.
- **No burned-in captions on an English film**, Reel included. Lock row 9 had said yes; Jason withdrew it at closeout ("this is a English language film"). Memory `no-captions-on-english-films`. Ask the question with the language, not as a default.
- **Tool mentions in copy "can make alot smaller."** One line, "Made with AI: Seedance, Vidu, Seedream and Suno."
- Delivery per FINAL_DELIVERY_STANDARD into `FINAL_RENDERED/DCL-20261104-CARGO/`: both masters with hashes, the approved art copied, the end title as cut in both formats, nine stills per format, 2x stills, poster D in three formats, approved copy, posting kit as an Artifact. The Reel is in Metricool for 10 Nov; four behind-the-scenes carousels were already scheduled.
- Still open after closeout: the release's 24 h and 7 d audience row (AUDIENCE_AND_STORY_BRIEF, after 10 Nov); Jason's hand posts on YouTube Shorts, X, LinkedIn and Facebook from the kit.

## 11. Incidents

- **An append helper opened files with "w" before reading them** and truncated eight files (the lock, two logs, five memory files). Phase 3 caught it; the phase 2 session restored all eight from its transcripts. Rule: append with `open(p, "a")` or read into a variable first; never `open(p, "w").write(open(p).read() + t)`.
- **Atlas quotes expire;** two confirmations were refused as expired and nothing was billed. Re-quote, report the price, ask again.
- **Atlas concurrency failures are unbilled;** resubmit one at a time. Atlas also merges identical arguments into one job (two of the three 9:16 takes), so vary a parameter when a true second take is wanted.
- **The USD 20 top-up stalled the film for a few hours** between the pilots and the drafts. Ask for the top-up at the gate before the one that needs it.
- **Remote Control could not start a child session**; a card had to be clicked in a parent session.

## 13. Jason's debrief (9 Nov 2026)

Two points, in his words and then what the record says.

**"The sub-agents, even though Opus, seem not as intuitive ... they obey my order step by step. They do not have the intuition of the director. The reason why I use Claude to do video direction is the intuition."** On Wind the Man and the first films the director changed camera angles on its own initiative and the result was good; on Small Cargo the phase sessions executed and asked.

What the record shows: the model was the same (Opus 5.5 directed Wind the Man and every Small Cargo phase). What changed is how the director was briefed. Wind's director worked under Jason's stated latitude ("all the freedom to repropose a better story board") in one session that lived with the film for eleven hours. Small Cargo's phase directors each started cold from a handoff written as an execution list: the seven handoff files carry 22 "must not / never / only on his typed yes" lines and not one sentence that says "you are the director; here is the intent; change what serves it." The lock, the gate approvals, the show-drafts-before-HD rule, the token caps and the spin-down framing ("routine work on Opus") all push a session toward asking rather than deciding. The structure that cut credits and post errors also trained obedience. Jason's one-at-a-time notes (35 page versions) then taught each session that its job was to apply the next note.

**Rule:** every phase handoff opens with a director's mandate, not a rule list: the film's intent and each shot's purpose (from the treatment), an explicit grant to restage, re-angle, re-cut and re-time anything that serves that intent inside the lock rows, and the instruction to bring a director's own improvement to every gate (flagged as such, costed, before the quote). The must-nots stay, at the end, and are about money and frozen files only. The chief director reviews each gate page for directing choices before Jason sees it, not only for correctness. Intuition is asked for in the brief or it does not appear.

**"More changes in the 9:16. We spent time reframing and retouching, whereas on Hold the Note we had the 9:16 artwork done and sent to video gen, with no patching."**

What the record shows: he is right, and a Lab rule already said so. The 21 Oct dual-format decision (memory, from the WIND series) reads: "shots whose best vertical differs get a separate 9:16 board and generation; never patch a vertical afterwards (no face extension, no video regen)." Small Cargo's lock row 1 overrode it with reframe-and-extend for every shot, on his 7 Nov note and the director's cost argument. The saving was real but small: about USD 10 to 15 of native vertical takes avoided, against 103 M tokens, about six GPU hours of VACE that failed on three of five shots, seven review drafts and most of a night of his attention. Hold the Note's native 9:16 cost a second set of takes and doubled its retakes, but needed no patching and no review rounds of its own.

**Rule (reinstating 21 Oct, sharpened):** at the start-frame gate, every shot gets one of two routes. CROP where the subject sits inside the 9:16 column of the 16:9 take: free, no patching. NATIVE VERTICAL where the 9:16 window would need extension (wides, two-shots): a 9:16 start frame from the same design and a 9:16 take, bought with the 16:9 take in the same batch, at the 480p draft stage first. Extension (still or video) is a fallback for a single failed shot, never the plan. Expected cost on a Small Cargo-sized film: five native vertical shots, about USD 12 to 15, in place of the 103 M tokens and the patching rounds.

### Third point: "the story and camera angle is not so exciting ... previously all video director agents were able to take the basic synopsis and expand them into an interesting storyboard."

This one lands on the board-gate director (Fable 5.1), not the phase sessions. The locked board, measured from `board/FRAMING_PLAN.md`: 15 shots averaging 2.5 s; ten of them static or "slow drift"; ten of them from the near side of the cradle at eye or chest height; one crane (shot 4) and one low frontal (shot 5, Jason's own note). The lab scene is ten shots of coverage from one side of a table. There is no reverse, no over-shoulder, no motivated move, no change of scale between cuts apart from the viewer. Wind the Man's director took a ten-second synopsis and reproposed a 26 s action variant under Jason's latitude; the Small Cargo board kept the synopsis's beats and shot list almost one to one and spent its three critique rounds on correctness (continuity, acceptance tests, window centres) rather than on whether anyone would be excited. Nothing in the board gate asked that question, and the lock then froze the camera plan before anyone did.

**Rule:** before any board is sent for its first critique, the director delivers two boards: the faithful one and a bolder reproposal (story shape, staging, camera language: angles, movement, scale contrasts, a reverse, one shot the audience has not seen before), and names which one it would make. The critique brief's first question becomes "would you watch this to the end, and which shot would you remember?" before any continuity item. Measure the board's variety (static share, same-side share, average shot length, longest take) and report it on the gate page. The board gate on Small Cargo was a quality gate for correctness; it also has to be a gate for excitement, or the lock freezes a dull film.

### Fourth point: "Seedance draft to HD still works for me ... local upscaling is sharper but certain details are more smudged ... the cheaper models hold frames but human and clarity is not matching Seedance 2.5 ... maybe they are for non-human."

What the record shows, shot by shot: SeedVR2 on the 480p drafts of shots 1, 4, 8 and 15 passed the 100 % check and read as CGI to Jason; on shot 5 it invented eye shapes on a 25-px face. Vidu Q3-Turbo (USD 0.27) was accepted on shots 1 (space, no people), 8 (the open collector, no people) and 15 (the lab wide, two distant figures) and rejected with Kling on shot 4 (a crowded hangar: Vidu read as CGI, Kling smudged and mismatched the contrast), which went back to Seedance 2.5 HD. Every shot with a readable face or hand (ten of fifteen) ended on Seedance 2.5 draft-complete at native 1080p, USD 3.02 per shot including its draft. The cheaper routes substituted on three shots and saved about USD 8; the cap held because of fewer retakes and local fixes, not because of cheaper models.

Why the upscale "sharpens but smudges": a 480p draft has no detail under about 4 px, so SeedVR2 invents texture; it is sharp and wrong at the same time, worst on skin, hair, cloth and crowds. Native 1080p is the only route that renders those details rather than guessing them.

**Rule (finish route by content, replacing the per-shot table's model guesses):**
- A readable face or hand, or a crowd: Seedance 2.5, 480p draft shown to Jason, then native 1080p draft-complete. No substitute, no upscale.
- No human in frame (space, objects, empty sets, macro, locked set wides with figures under about 20 px): a cheap native-1080p model first (Vidu Q3-Turbo at USD 0.27 on this film), colour-matched to its Seedance neighbours before judging; Seedance HD if it fails once.
- SeedVR2 only where no cheap native model can reproduce a needed performance in a faceless shot, and Jason sees the result before it is cut in.
- One bake-off per film at the pilot gate, on one non-human shot, to pick that film's cheap model. Expected ceiling of the saving on a fifteen-shot film: about a quarter of the cap; the rest comes from fewer retakes.

### Fifth point: "being an Opus model, it must be smart enough to spot the film mistakes that are unfinished ... how can a ghost on a helmet go to the final stage? The ability to mend these visual mistakes, the intuition, also lost."

What the record shows: the 9:16 went to Jason seven times as "approve 9:16", and he found the defect each time: a blank slab under shot 12, a giant ceiling fixture, a cabin roof sliding, a ghosted helmet, a one-frame light flash, a strobing pan. The phase 3 log says how the drafts were checked before publishing: "audited every 4th frame plus the chunk joins", then "every 8th frame", plus tile metrics (pixel slide, frame difference, correlation). The 3 Nov rule from One Beat Late already said that sampled checks hide ghosting on composites and that every frame must be checked in playback; the director session had that memory and did not apply it. In phase 2D the same pattern: a right-side motion score of 1.1 against 5.8 was measured, called a pass and sent as an HD. The sessions reviewed by numbers and by sampled stills, not by watching the shot the way Jason does, full screen at 100 % and frame by frame on the joins, and they asked for approval of work they had not passed themselves.

**Rules:**
- Nothing reaches Jason as an approval candidate until the director has watched it in full at 1080p and normal speed, then frame by frame at 100 % on every composite join, every face and every reframe move, and written its own verdict per shot. Composites are checked on every frame, never sampled (3 Nov rule, now with the Small Cargo failure beside it).
- The review page states the director's verdict on each shot: "I would approve this", or "known flaw, shown for direction, not for approval". The director never asks "approve?" about a shot it would not approve itself.
- A cold eye before every publish: a fresh Sonnet subagent watches the draft with no context but the question "what is wrong with this picture?" and its notes go on the page. It costs a few million tokens and would have caught the slab, the helmet and the roof.
- A metric is evidence, not a verdict. When a number is weak or borderline, the shot is watched, and the number is reported as weak.

### Jason's recap of the films so far

The two films he counts as the best achievement: The Unstitched (film 3, 14 Oct), for its cinematography and framing and for turning a plain script into an emotional piece with a title that had a wow factor, the film that decided him on Claude Code as a film director; and Hold the Note (7 Nov), very well executed through many mistakes, with good intuition. Neither is the best-viewed spot. Small Cargo sits beside them as finished, under cap and not exciting. Every director watches those two finals before planning (VIDEO_DIRECTOR_BRIEF, 9 Nov block).

## 12. Rules added by this film (summary for the playbook)

1. A gate is a session boundary; no session runs two gates; retake loops in their own session; one page version per batch of notes.
2. Scan every take's consecutive-frame geometry; trim both ends; velocity profile before calling a snap; no spliced review clips.
3. Show every draft before its HD; collect all notes on a cut before quoting a batch; his viewing overrides the metric.
4. Background life comes from concrete prompt actions; vehicles do not drive; anchor small faces with an end frame and buy native.
5. Shots with no human: cheap native model first, colour-matched to neighbours; SeedVR2 is a last fallback. Anything with a face, hand or crowd stays on Seedance draft then native 1080p.
6. Music: never lock "no music" from a board; A/B three options at the rough cut with the continuous line in the cut; one real cue on an intensity curve; ask about title sound in lock row 7.
7. 9:16 extension on locked wides is a tracked still, not per-frame fill; shutter-blur fast pans; the 16:9-first decision and its trade-off are recorded in lock row 1.
8. Prop mounts and anchors must agree across start/end pairs.
9. Poster lead is the protagonist from an approved plate; no captions on English films; short tool lines in copy.
10. Append-only file writes; re-quote expired Atlas quotes; ask for top-ups a gate early.
11. Every phase handoff opens with a director's mandate (intent, grant to restage and re-angle, bring one improvement per gate); must-nots are about money and frozen files only (Jason's debrief).
15. Director's verdict before Jason: full watch at 1080p, every frame at 100 % on joins, faces and reframe moves, a stated verdict per shot, a cold Sonnet eye before every publish; never ask approval for a shot the director would not approve (Jason's debrief).
14. Finish route by content: faces, hands and crowds are Seedance draft then native 1080p, never upscaled or substituted; cheap native models only for shots with no human, colour-matched; one bake-off per film (Jason's debrief).
13. Two boards at the first critique, faithful and bold, with a variety measure on the gate page; the critique asks "would you watch to the end" before continuity (Jason's debrief).
12. 9:16 per shot at the start-frame gate: CROP where the column holds the subject, NATIVE VERTICAL take where extension would be needed; extension only as a one-shot fallback (Jason's debrief, reinstating the 21 Oct dual-format rule).

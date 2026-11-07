# Retrospective: Hold the Note (TEST-020, DCL-20261102-NOTE), 6 Nov 2026

For every director agent. Read it before planning a film. Written at closeout by the phase 6 session from `experiments/TEST-020-hold-the-note/production/P5_STATUS.md`, `GUARDRAILS.md`, `subtitles/KOREAN_LINE_CHECK.md`, `production/p5_sound/SOUND_LOG_P5.md`, `production/p5c_build/CRITIQUE_5C.md` and the session transcripts. Token and spend figures: `experiments/TEST-020-hold-the-note/closeout/TOKEN_REPORT.md`.

The film: 49.6 s, native 16:9 and 9:16, Korean dialogue with English subtitles. Both finals approved by Jason on 6 Nov ("all final approved"). Spend about USD 49 on Atlas; about 500 M processed tokens against a target of 80 M.

## 1. Front-loaded post decisions: did they work?

**Mostly yes for what they covered, no for what they did not.**
- Worked: the three grain effects were tested on clean plates and approved before production, with a written ledger, so no effect was redesigned in the edit. The subtitle frame, the title (title-v08 art, kinetic grain build), the finish route per shot and the "no black before the title" ending were all fixed at the gates. Jason's final-gate notes contained none of TEST-019's post errors (props that never reappear, dead ending, wrong scale, faint effects).
- Did not cover: **what the video generator does inside a take.** Every note Jason sent at the final gate was about a generated take or the sound ending: the shot 10 hand and flute morphs, the whistle not matching his mouth, the flute cutting off into silence, the 25 s ghosting. No effect sheet could have caught these.
- The token budgets did not hold (section 2). Front-loading cut judgement errors in post. It did not cut the cost of regenerating takes.

**Rule:** keep front-loading post. Add a front-loaded **take acceptance test** for every generated face or prop shot: a sharpness-dip and ghost scan on every take (the every-frame spike scan cannot see slow cross-fades of the same shot), and the whistle, blow or lip onset checked on a mouth crop, not by cue arithmetic.

## 2. The phase 2 token overrun

Phase 2 was budgeted at 12 M. The 5 Nov note recorded about 25 M. Measured from the transcripts afterwards, **phase 2 used about 57 M processed**, 33 M in the main session and 24 M in two subagents. See `TOKEN_REPORT.md`; the report says how sessions were matched.

Causes, as already written in GUARDRAILS and still true:
- long waits inside one growing session;
- two subagent rounds per effect;
- three rounds of frames with the gorge side and look direction wrong;
- a cold critique skipped, then run later.

The bigger lesson: **the later phases overran too**, and the largest by far was phase 5C at about 192 M, the session that built the finish, regenerated shot 10 several times and republished the review page about fifteen times. Phase 5 as a whole came to about 309 M against 20 M. The "hand off at 300 K context" rule was followed. The sessions were still long because each regeneration loop re-read a large context.

**Rules:**
- Count budgets in the same unit the report uses (processed, subagents included) and check them at each gate. The overrun was reported at about half its real size.
- A regeneration loop (retake, preview, note, retake) runs in a fresh small session with the take's files only, not inside the finish session.
- Ask Jason for one batch of notes per preview. In 5C they arrived one at a time, and each one triggered a republish.

## 3. The Korean line check, and the 이을게 → 불게 change

No native speaker was available. The substitute check was three free sources: Claude's review, a blind GPT second opinion, and back-translation. It improved two lines: 숨 쉬어! 내가 이을게! and 사십 년째 건너는 다린데, 그쯤이야. Jason adopted both.

Then **speech-to-text, run on every generated Korean take, misheard 이을게** in both dialogue routes (이룰게 / 이길게). A third draft used 숨 쉬어! 내가 불게! ("I'll blow it"), which sets up his whistle in the next shot, and Jason chose that take. The English subtitle stayed "Breathe! I'll hold the note!".

What it shows:
- The text check cannot stand in for a native ear on naturalness, but the **speech-to-text pass found the intelligibility problem the text check could not.** Keep it on every Korean take. It cost fractions of a cent.
- When a line is misheard by the speech model, change the line before spending more takes on it. A word the model cannot say is a word the audience cannot hear.
- Words fixed by hand: typing Hangul in tool calls picked up one wrong character once (텐 for 텼); load Korean from a JSON file.
- Still unchecked by a native speaker. If a Korean speaker comments after posting, take the note.

## 4. The SeedVR2-first face exception: 12 of 12 passed

TEST-020 ran the exception recorded in memory "No upscaled faces": faces on the 480p Seedance drafts were finished with SeedVR2 first, and a native 1080p completion was bought only where it visibly failed. All twelve face shots (04, 07, 10, 03, 08 and 12, each in 16:9 and 9:16) passed the phone-size and 100 % crop sheets: crisp, identity matching, no shimmer. Shot 12 is small (about 30 px face in 16:9) and passed too, with the 9:16 mouth-open frame watched in playback. Native face completions bought as a result: none. The USD 14.74 cap went unused for faces.

Shot 10 ended on native HD anyway (USD 6.40), but only because it needed a regeneration for the morphs (section 6); SeedVR2 did not fail on it.

**Open decision for Jason, asked in the closeout message: does SeedVR2-first for faces become the Lab default?** Evidence for: 12 of 12, USD 2.45 to 3.06 per native completion avoided (about USD 30 if all twelve had been bought), and the 480p drafts are also what the edit is cut on. Evidence against: one film, one face set, faces that never fill the frame. Until he decides, the memory rule stands and this film remains the one exception.

## 5. 4K SeedVR2 failing on the 3080; 1620 works

The 2160 (4K) SeedVR2 run for shot 14 failed twice, silently: `seedvr2.ps1` throws and the runner dies before its retry. RAM was not the cause (96 GB, 67 GB free). The 1620 working size ran fine, about 17 minutes per 5 s clip, then resampled with Lanczos to the 4K grid the compositor expects. The 112 → 100 % move downsamples at least 2,571 px of detail to 1,920, so no pixel is enlarged past native. Atlas's video upscaler (about USD 0.018/s) was on standby and not needed.

**Rule:** on the 3080, plan SeedVR2 at 1620 and treat 2160 as unsupported until the runner's failure is found. Make the runner retry on a thrown error, and log to a UTF-8 file so a silent death is visible.

## 6. Shot 10: three lessons

Shot 10 is the beat where she lifts the flute and the two notes meet. It cost five regeneration rounds and USD 6.40 of native HD, and Jason caught the morph four times by playback.

1. **An end frame that disagrees with the start frame on a prop forces a morph in every take.** The approved end frame E10H showed a shorter flute than S10H, so Seedance shrank the flute to land on it. Check prop continuity between start and end frames before any image-to-video job.
2. **Measure the HD file, not its draft.** The HD re-render is not frame-identical to its draft; the morph moved about 6 frames later. A band-by-eye check on small tiles missed it. Track the flute rows with phase correlation (`flute_track`, zero drift over the shot) on the HD file.
3. **Short, plain prompts.** Emphasised motions were over-performed. The prompt that worked (r6a) was short: lips on the hole, hands still, one fingertip lifting at a time.

Also: Atlas deduplicates identical requests to the same job, so two "independent runs" with identical arguments are one charge.

## 7. 9:16 shot 4 taken as a reframe of the approved 16:9

The 9:16 shot 4 kept putting her mouth at the edge of the flute. Jason asked: "Since 16x9 is approve why not use the same image but reframe for 9.16?" The 9:16 shot became a crop of the approved 16:9 take (SeedVR2 at 1620, crop 911×1620, scaled ×1.19 to 1080×1920, with the 16:9 grade). It cost nothing, kept the approved performance, and the face was crisp at 100 %.

**Rule:** when a 16:9 shot is approved and its subject sits inside the centre 9:16 column, reframe it instead of generating a second performance. Decide this at the start-frame gate with the finish route table, not after two failed 9:16 takes. This is the free-route extension of the TEST-019 "shared take reframed only where both formats truly read the same" rule.

## 8. The critic's E1 note

The cold critique (Sonnet, one pass over contact sheets) said that the E1 grain fall in shot 5 reads as long straight motion-blur needles, closer to hair or rain streaks than gravity-fed grains. It was kept as approved: it matched the approved effect test and Jason did not flag it. The prepared free option, shorter trails with the velocity biased vertical, was not used and still works if he raises it later.

Lesson: an effect test approved at 2 s on a clean plate can still look wrong inside the cut at phone size. Add a "seen in the cut" check at the first assembly, with the effect on, next to the neighbouring shots. A fresh critique caught what the approved test did not, which is the reason to keep the cold critique mandatory and cheap.

## 9. The modern-sageuk end cue and her real flute phrase

The end cue is a modern K-drama sageuk-style ensemble (Suno chirp-v6, 20 s, resolving on C) with **her own flute phrase laid over it as the melody**, so the title's music is the note she held. The pieces:
- Her flute is a Suno phrase in C-major pentatonic, home C5. Take a was rejected on pitch class (minor-leaning); take b was chosen after measuring the pitch classes with an FFT f0 track.
- The cue was chosen because C dominates it and it resolves on C within the right length.
- The flute stays in its natural register (C5), his whistle is shifted to C6, one octave above. In shot 10 they meet in octaves, which reads as one note.
- Her closing figure (D E F E D C) plus a steady C5 sits two dB under the cue and lands its C5 at 43.48 s on the cue's own resolve, under the title. There is no title sound effect.
- True sources of every layer were logged at the mix, as GUARDRAILS A.6 required, and drive the AI line in the captions.

Lessons: (a) **measure the pitch of generated music before choosing a take; do not trust the prompt.** (b) Seedance's native dialogue carried steady tones; they were notched per source (6V 999 Hz; 13V/14V 601, 800, 999, 1198 Hz). The "2.1 kHz" tone suspected earlier was not present. (c) The ending sound needs a gradual release, not a cut: Jason flagged the flute and whistle cutting into silence, and the fix was a 1.4 s release with a gorge ring-off. (d) Check a whistle onset on a mouth crop: the first onset had been placed by cue arithmetic and was 0.7 s early.

## Other points worth keeping

- **Review pages and kits go out as Artifact links** (Remote Control cannot open local HTML). The final-gate page went through about fifteen versions at one URL; that worked well, and the cost was the notes arriving one by one.
- **Closeout inside the delivery standard worked from the pattern of TEST-019**, with two changes: nothing was written to `approved/` or `handoff/`, and the poster is built from a text-free plate with the approved title art set locally. A poster frame needs a check for closed eyes: the first poster of the flautist used a frame with her eyes closed, and Jason said it was not appealing. Pick a frame where the eyes are open.
- The v09 source packet was never registered as an `approved/` snapshot, so the library copy records it with `SOURCE_APPROVAL.json`. Register the snapshot when a film is approved, so closeout has one packet to copy.

## 10. A deferred item was dropped at the board gate: the epigraph

The classical epigraph 合之然後有聲, "Only when joined does sound arise." (Samguk Yusa 三國遺事, Manpasikjeok passage; the English is the Lab's own translation) was **deferred in the source handoff** (`days/2026-11-02-hold-the-note/title-design/v02-DRAFT/RESEARCH.md`). The phase 1 rule "no poem or extra title" then closed it off, so it never reached the board, and Jason asked for it only at closeout. Both finals had to be re-finished to carry it, text only, with the picture fixed, after the final approval. Where it appears and how it is credited was settled late.

**Rule:** a deferred item in a source handoff is an **open question until someone decides it**, not a closed one. List every deferred item (titles, epigraphs, credits, languages) as open at the board gate and ask for a yes or no on each, before production. A phase rule that says "no X" must not silently cover something the source deferred. Call the epigraph an excerpt, never a poem, in every caption and credit.

## 11. Close-out addendum, 7 Nov 2026: the v03 face retake, social copy and the final numbers

**What happened.** The day after the "final yes", Jason watched the finals full screen and wrote: "i cannot accept a few shot quality, the far away shots the facial is all smudge n distortion. if upscale dont work lets regen in seeddance real HD". Phase 7 retook every distant-face shot at native 1080p:
- shots 2, 3, 9, 11, 12 and 14 in 16:9, and 2, 3, 9, 11 and 14 in 9:16;
- then two more fixes from his v03 notes: the old man's face in 9:16 shot 12, and her eyes rolling right in shot 13, in both formats.

All eleven first-batch takes passed at 100 % on the first try. He approved v03 ("v03 yes"), and v03 replaced v02 in tonight's Reel. Phase 7 cost USD 37.80 in credits (cap 39.50) and about 112 M tokens across two sessions.

**Root causes and the rules they add:**
1. **SeedVR2-first doesn't hold for small faces.** It passed 12 of 12 at phone size and on 100 % crops of medium faces (section 4). It fails on any face that is only 10–30 px tall in the draft: there is no detail to restore, so it invents features (the porter's "beak" in shot 2). **Rule:** at the finish-route gate, measure the face height in the draft. Under about 60 px in the final frame, the route is native 1080p from the start. SeedVR2 is for faceless shots and for medium or close faces that pass at 100 %. The open question "should SeedVR2-first become the Lab default?" is answered: **no**, only per shot, by this measure.
2. **Judge at Jason's viewing size.** He reviews full screen at 1080p. The director's audit passed 12V, and he then rejected it. **Rule:** the final face audit is a 100 % crop of every face in every shot in both formats, checked against the finished master and not the draft. One contact sheet per format.
3. **Eye-line belongs in the start frames.** Shot 13's approved start frame already turned her gaze right, and the take followed it. **Rule:** the start-frame contact sheet also checks eye-line and look direction against the board, alongside camera side (GUARDRAILS, phase 2 overrun).
4. **STT on every take, every format.** The 13V retake's voice failed speech-to-text (휴파랑), so the 9:16 reuses the 13H voice.

**Social close-out lessons (Jason's notes, 7 Nov):**
- **Posting kits go out as Artifact links.** A local HTML kit can't be opened over Remote Control, and he couldn't find it. Rebuild the kit whenever the finals change: when v02 was moved to the Recycle Bin, its file list was left pointing at deleted files. Re-pull the film stills from the current masters.
- **Post voice per platform:**
  - conversational paragraphs, never numbered points;
  - no runtime in any post;
  - LinkedIn is the professional production process and tools, not personal lessons;
  - X is a short thread of three posts under 280 characters each, written to teach other video-gen artists;
  - personal Facebook is written in his own voice (model: the One Beat Late LinkedIn post he rewrote): the history, the concept and the idea first, then "Claude Code ran the pipeline as the director agent, with a review at every stage";
  - Instagram and YouTube carry a short version of the source legend.
- **Scheduled captions can be edited** through Metricool's `updateScheduledPost` before posting. The post's id changes and the uuid stays.
- **Clock:** in Git Bash, `TZ=<zone> date` printed UTC. The director told Jason "11½ hours to 18:00" when it was 4½. **Rule:** compute local time from the UTC offset in Python, never from `TZ=` in Git Bash.

**Final numbers for the film:**
- **Tokens:** 670.7 M processed over 10 sessions (`tools/token_count.py "Hold the Note"`). That is 4.5× the 150 M realistic target and 8.4× the original 80 M. Every session peaked above 250 K context (320–712 K); the handoff rule was written but not followed. Phase 5C (232 M) and the v03 collect session (96 M) were the largest.
- **Credits:** about USD 49 to the 6 Nov final, plus USD 37.80 for phase 7, so about USD 87.
- **The avoidable part:** phase 7's tokens and credits are the cost of the SeedVR2-first decision. On a film with distant faces it would have been cheaper to quote native 1080p at the finish gate.

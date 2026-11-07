# Requirements lock — fill in before any production spend

Jason, 6 Nov 2026, after Hold the Note: "Director need to make sure music, SFx endtitle any additional requirements be fore starting, this will safe the repeating work."

**Why.** Hold the Note took 502 M tokens against an 80 M target. A large share was rework, because each of these arrived after the finish had started:
- music;
- her real flute phrase;
- the title motion;
- the change to no black before the title;
- the all-caps English;
- the epigraph.

Each one reopened the finish. Every item was a good creative call. The fault was asking too late.

**How to use it.**
1. Copy this file into the experiment folder as `REQUIREMENTS_LOCK.md` at the **board gate**.
2. Fill in every row with the director's proposal.
3. Send it to Jason in the same message as the board, as an Artifact link.
4. Get a yes, a no or a change on **every row**. A blank row is not a yes.
5. **No paid generation starts until every row is answered.**
6. **Supervisor check at every later gate (adopted 2026-11-07, Jason: "All four").** Before each gate message, run a Sonnet subagent at low effort with only this file, the source handoff's deferred-items list and Jason's messages in this film. It answers one question: which rows or requests are not yet honoured, or were changed without his yes? Paste its answer into the gate message as "Supervisor: ..." or "Supervisor: nothing open". It is read-only and never messages Jason itself. On Hold the Note the epigraph was deferred at the board gate and then dropped; this step exists to catch that.

**Pre-fill every row with the director's proposal,** so Jason can reply "all as proposed" and only change what matters.

**Send a rough preview with the lock (free, local).**
- Use the board frames, timed as the cut, with the planned sound under them: music where it enters, the instrument as it will actually play, the key SFX and silences, and the dialogue, as temp TTS or simply written on screen.
- Put the subtitles, the epigraph or quote, and the end title over the frames in their real positions and at their real times. Use the actual approved title art.
- About 30–60 s, both formats if both are planned. Publish it as an Artifact link.
- Jason reacts to what he sees and hears, not to tables. On Hold the Note the single flute tone, the missing music and the missing epigraph only surfaced once he watched a cut.
- Keep it rough. It's a sketch for judging the plan, not a deliverable. Don't polish it, and don't spend tokens on it beyond one build and one contact sheet.

A new requirement after the lock is still welcome, but the director says what it reopens and what it costs before doing it.

| # | Item | What to decide | Director's proposal | Jason |
|---|---|---|---|---|
| 1 | **Formats** | 16:9, 9:16 or both; native or reframed per shot | | |
| 2 | **Runtime** | Target length, and whether the end title and epigraph add to it | | |
| 3 | **Language and dialogue** | Language, lines, register, native-speaker or substitute check, subtitle language(s) on screen | | |
| 4 | **Music** | None, by stages, or a score. Where it enters and ends, its style or idiom, and its source (generated, local or a recording) | | |
| 5 | **On-screen instruments and performance** | What each instrument actually plays (phrase or held note), and whether fingers and mouth must match | | |
| 6 | **SFX and ambience** | Layers, the source of each, where silence falls, and anything banned (the Lab default is no title SFX) | | |
| 7 | **End title** | Which approved art; static or motion (style, both formats); black or no black before it; the timing | | |
| 8 | **Epigraph, quote, poem, opening card** | Whether there is one; exact text and source; placement (before or after the title, centre or side); script and orientation; English styling, e.g. all caps like the title | | |
| 9 | **Typography on screen** | Subtitle style frame, title-matching fonts, caps, position clear of faces and UI zones | | |
| 10 | **Effects** | Each effect with its 2 s local test (GUARDRAILS A1) | | |
| 11 | **Finish route per shot** | Native 1080p, SeedVR2 or a reframe. Measure each face's height: under about 60 px in the final frame means native 1080p (Hold the Note v03). Name the audit: 100 % crops of every face on the master | | |
| 12 | **Ending** | The last image, the last sound, the fades | | |
| 13 | **Deferred items in the source handoff** | List every item the handoff deferred (titles, epigraphs, credits, languages, series identity). Each gets a yes or no here. "Deferred" never means "dropped". | | |
| 14 | **Social and closeout extras** | Posters, platforms (Instagram, YouTube, X thread, LinkedIn, personal Facebook) and the voice for each (brief §2026-11-07), the schedule window, and the kit as an Artifact link | | |
| 15 | **Anything else Jason wants** | Ask in one line: "Anything else that must be in the film?" | | |
| 16 | **Spend and token plan** | Credit cap per gate; token budget per phase, including subagents | | |

Related: `experiments/TEST-020-hold-the-note/GUARDRAILS.md` (decide post before production, judgement checks, token budget) and `RETROSPECTIVE_2026-11-06_TEST020.md`.

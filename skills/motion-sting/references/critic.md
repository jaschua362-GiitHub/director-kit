# Independent critic — motion-sting

The builder never grades its own film. Self-checks with `TOOLS` (step 5) catch construction bugs while
building; this round judges the **delivered render** and is the gate before Jason sees a version.

## 1 · Evidence pack (from the MP4, not the live page)
```
python <SKILL>/scripts/review_pack.py <project>/<Name>_1920x1080_60fps_sound.mp4 [--strips <beat times>] [--loop]
python <SKILL>/scripts/review_pack.py <project>/<Name>_1080x1920_60fps_sound.mp4 [--strips ...]
```
→ `<project>/review/<file>/`: `contact.png`, `phone.png` (360 px wide), `strip_*.png` (12 native frames
around the fastest moments + any times you name), `report.md` (near-still stretches, motion per second,
loop seam, LUFS / true peak). `--loop` only when the piece is meant to loop.

## 2 · Spawn a fresh critic
`Agent` (general-purpose), a **new one every round**. Give it only: the pack folders, the MP4 paths,
`BRIEF.md`, `references/craft-rules.md`, Jason's own feedback words so far, and (from round 2) the previous
`review_log.md` entry. Never your reasoning or a list of what you think you fixed.

```
You are an independent, harsh motion director. You did not make this; judge the pixels and the numbers,
not intentions. Be a critic, not a proud author.

Film: <MP4 paths> — <one line: brand + what the sting must make the viewer feel>.
Brief: <project>/BRIEF.md. House standard (mandatory): <SKILL>/references/craft-rules.md.
Client's words so far: "<Jason's feedback, verbatim>".
Evidence: <pack folders> (read report.md first, then every PNG). You may extract more frames with
ffmpeg into <project>/review/critic_<round>/ if something needs a closer look.
<Round 2+: Previous review: <project>/review_log.md, round N-1. Mark each item FIXED / PARTLY / STILL PRESENT.>

Score 1-10, one line of evidence each (timestamp + what you saw):
 1 Hook — first 2 s earn attention
 2 Phone readability — phone.png: type, hairlines, logo at 360 px wide
 3 Motion quality — easing, continuity of lines, joins, no pops / one-frame glitches (strips), blur
   where fast, nothing "sliding"
 4 Variety & pacing — something new every 2-4 s, no dead beat (report: near-still, motion per second)
 5 Composition & framing — both formats; 9:16 tracks the action, nothing hugging edges
 6 Brand accuracy — palette (no black on the coffee brand), type, logo geometry, optical centring of the end lock
 7 Sound sync — cues on visual events, -14 LUFS, peak <= -1.5 dBFS (report). N/A if silent.

Hunt specifically for: text overlapping during swaps, corner labels / frame borders, centred-title-on-
gradient shots, blurry scaled type, line tangles or hairpins, visible grain or banding, a stutter at
the loop seam, a logo that looks off-centre.

Write to <project>/review_log.md (append, round N): the scores, the 3 biggest problems with timestamps,
each with a concrete fix, then VERDICT: SHIP (every score >= 8) or ANOTHER ROUND. Under 400 words.
```

## 3 · Gate
- Every score **≥ 8** → deliver. Otherwise fix the 3 listed problems (largest gap first — don't average a
  weak hook away with strengths elsewhere), re-render (drafts `--sub 1` are fine mid-loop; the delivered
  render uses the default blur), new pack, **new** critic that verifies the previous list item by item.
- Stop at the gate, when the remaining items are sub-frame/cosmetic, or when Jason says stop — usually
  2-4 rounds. Tell Jason in one line per round: scores, what's being fixed.
- On delivery, show the final scores and say honestly what was measured vs. judged by eye, and that the
  sound was judged from numbers and spectrogram, not heard.
- When a critic finding generalises (it would apply to the next sting too), add it to `craft-rules.md`.

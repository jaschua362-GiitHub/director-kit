# Money and approvals card

Read this at the start of every session. Required reading: `DIRECTOR_CRAFT.md`, the three every-session cards, your stage card and your handoff. The Lab keeps a longer depth file behind this card; it is not in the kit.

## What this stage is for
Spend only on a price Jason has seen and a yes he typed, once per gate (the review ending a phase). He judges whether it bought usable footage.

## What good looks like
- Quality first: "by enfocing token limit might cause us reduce quality work". Cut waste, never a critique, frame check or retake.
- If a cheap route visibly fails, quality wins within the cap.
- Free local work before bought (Small Cargo, first film under its cap).

## Standing film budget (his ruling, 25 Nov 2026)
From 25 Nov 2026: **USD 35 per film on Atlas**, at most one film a week, running **40 s at most and mostly under 30 s**. He expects no re-renders caused by our mistakes: "your side has to be very careful on rendering and mistakes so that we don't have to re-render". Rates on 25 Nov: Seedance 2.5 at 480p is about USD 0.134 a second for drafts, and native 1080p draft-complete about 0.62 a second. A 30 s film is about 4 for drafts plus 18.5 to finish, which leaves about 12 for stills, plates, sound and the retake reserve. A 40 s film leaves only about 5. So:
- The storyboard is cut to the budget before any spend: the shot count and seconds are priced at the board gate, and every second of draft is a second we mean to finish.
- Design stills go on the ChatGPT or Codex routes; Atlas is used for video and photo plates only.
- Every prompt and start frame passes the critic and frame checks before it is submitted. A retake caused by a fault we could have seen comes out of the reserve and is reported as our error.
- Report the film's running spend at every gate. At USD 35, stop and ask; never top up and carry on.
- Record per finished second (closeouts): Last Ferry about 0.62 (USD 46.2, 74.5 s), Evade and Escape 0.80 (22.29, 27.9 s), Small Cargo 1.20 (55, 45.5 s, both formats). USD 35 for 30 s needs 1.17 or less; for 40 s, 0.88 or less. House of Courtesy (68.21) and Hold the Note (about 49) ran over through retakes and dialogue completes.

## Look for
1. One ask per gate: the whole batch with a named retake reserve, one typed "submit all" covering every take (House of Courtesy asked 16 times).
2. The cap (his spending ceiling) is a stop line. House of Courtesy went from USD 45 to 68.30: a cap raised nine times stopped working as a cap. Ask for top-ups a gate early, naming what they miss.
3. The Go is his own words naming this take; a re-pasted sheet, "continue" or "retry" is not. House of Courtesy B9: USD 2.39 lost; Atlas (the generator) cannot cancel.
4. He replied on the draft (cheap preview) before its HD (expensive 1080p): "Should have show me draft before proceeding". House of Courtesy round 4 skipped drafts: four near-still loops, USD 7.91.
5. A retake carries every known fix, after a free local fix. House of Courtesy B10: three retakes, one fix each, USD 10.67.
6. All notes in before one rerender quote: "lets handle all new request before Q all to rerender." (Small Cargo).
7. Approval is his explicit words on a named revision and scope; art, cut, aspects, spend and publication are separate (House of Courtesy B9).

## Let the script check
- Running total against the ceiling: `tool: tools/craft_check.py spend`.
- Live HD quote against his Go amount: `tool: tools/craft_check.py spend --next <quote> --go <his amount>`.
- Token line per gate: `tool: tools/token_count.py`.

## How this stage runs
- No paid job until every requirements-lock row (pre-production decisions) has his answer: "Director need to make sure music, SFx endtitle any additional requirements be fore starting" (Hold the Note).
- The lock sets a cap per gate and a token target for each role (House of Courtesy had none: 1,008.3 M tokens against 150 M). Token targets are estimates: report overruns, with cause.
- One message per gate: ready work, open decisions, batch quote, token line; confirm in the session holding the quote.
- A yes button carries the amount ("Yes, USD 3.09") or it is not a yes. Atlas quotes lapse after an hour; a re-quote with identical numbers stands under the same yes (The Last Ferry).
- Money must-nots: no annual plans; no spend without his word; never edit frozen approved files.

## Settled
- One batch yes per gate beats per-take quotes; each HD still needs his Go naming that take, with its quote shown.
- Drafts before HD stands; cheaper models by shot importance: the production card.
- Token plan: about 168 M (150 to 190).

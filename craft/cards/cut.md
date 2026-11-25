# Cut card

Read this when you start the cut stage. Required reading: `DIRECTOR_CRAFT.md`, the three every-session cards, this card and your handoff. The Lab keeps a longer depth file behind this card; it is not in the kit.

## What this stage is for
Edit, grade and finish the approved takes into a film a first-time viewer follows on a phone. Jason watches as an audience member, not against the board.

## What good looks like
- Each cut motivated by an action, eyeline or reaction, landing on motion after the action completes; in and out points chosen per shot, never first frames at board lengths: "Cuts don't join up… wasted the action." (Shadow Apprentice)
- Each shot's story action is obvious: "we should make it obvious" (House of Courtesy B7).
- The ending is an action (a walk-out, a bookend), then picture and music fade together.

## Look for
1. Near-still shots; land every beat on movement, a cut or sound. Courtesy's near-still loops cost USD 7.91 plus 3.96: "basic video production error that are easy to spot".
2. Every frame at 100 % on joins, faces, composites and moves, after one full watch. Sampling sent Small Cargo's 9:16 back seven times.
3. A weak metric: watch the shot, report it weak. Courtesy published an audit's "near-still" note.
4. The close-up's object in the next shot. One Beat Late lost its footprint.
5. Every background figure moving, near and far. Courtesy's still attendant cost USD 2.20 a retake.
6. Effects and reveals inside the cut at phone size. One Beat Late's effect read faint.
7. Every face at 100 % on the master, one sheet per format (Hold the Note).

## Let the script check
- Motion: median frame difference under 0.1 at 320 px is frozen. `tool: tools/craft_check.py motion`
- Start/end snaps (jumps where a take meets its given frame): drop frame 0 and the last 3-4. `lab script, not in kit: fix_ends.py`
- Measure the HD itself, not its draft. `tool: tools/craft_check.py hd`
- Every source in one colour standard (BT.709 video range, tagged) before the first preview; grade: low-key faces 35-45 %, speculars 90-97 %, blacks 1-3 %. `lab script, not in kit: luma_report.py`; colour: `build_story_master.py colour()` (TEST-025 finish).

## How this stage runs
- Effects and finish are decided in the lock; the edit assembles. One Beat Late lost 45 % of a session designing effects there.
- Before each gate, find the faults yourself: a first-viewer watch (real time, phone, sound on, both formats), then one cold Opus critique (a context-free reviewer). Say what each review watched and heard.
- Show every draft before its HD, even inside an approved batch; Courtesy skipped it twice, USD 9.67.
- One spend approval per gate, with a named retake reserve.
- Sessions and models: the handoff card.
- Grade with `skills/colour-grade/SKILL.md`; freeze the approved master's SHA-256.

## Settled
- Endings: live movement, a held look at the lead, then picture and music fade together.
- 9:16 follows each shot's crop-or-native-vertical plan from the start-frame gate.
- Upscale the original shots, upscaler chosen per shot; grain last.

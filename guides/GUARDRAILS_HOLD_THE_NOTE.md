# Hold the Note — guardrails against One Beat Late's mistakes

Jason, 5 Nov 2026: "Let's not make the mistake of previous job of excessive error in post production judgement and token burn."

Evidence:
- `experiments/TEST-019-one-beat-late/closeout/TOKEN_REPORT.md`: 487 M processed tokens. 45% of the phase 3 session went on footprint and grain effects designed during the edit; notes arrived one at a time inside a context of 500–960 K tokens.
- `RETROSPECTIVE_2026-11-05_TEST019_PHASE3.md`: post errors Jason caught himself (print never re-appears, dead ending, print scale, faint effects, unnatural swirl, colour shift on the extension, mix too loud, dubbed whisper).

Every phase session reads this page before working.

## A. Decide post BEFORE production (all free, at the visual-board gate)

Nothing below may be designed or redesigned inside the edit.

1. **Effect sheet + 2 s local tests** for the three grain effects, each on a clean plate in 16:9 and 9:16:
   - E1 edge shedding (shots 1, 5);
   - E2 bands re-sharpening under the whistler (shot 7 inset);
   - E3 the ribbon's release (shot 14).

   Each test is judged as a **physical reaction to a force**: grains fall with gravity, scatter in the wind and sit at a believable scale against the boot. A graphic pattern fails. Jason approves the sheet and the tests together with the start frames. Effects then get built only to that spec.
2. **Grain continuity ledger** (`production/GRAIN_LEDGER.md`), written before compositing. For every shot it records:
   - ribbon state: crisp, softening, shedding, re-forming or released;
   - where the fallen grains go;
   - how much edge is missing after shot 5 (the same in shots 6–11).

   Grain scale is checked against the boot in the same frame.
3. **First-viewer continuity, checked on the start frames:**
   - the boot from 1 is the boot in 5;
   - the edge damage from 5 is still visible in 6 and 9;
   - the flute she lowers in 8 is the one she lifts in 10;
   - the empty ribbon in 14 matches what's left after 11.

   Every object in a close-up re-appears in the next wide.
4. **Finish route per shot per format**, fixed in a table at the start-frame gate:
   - native 1080p for every readable face;
   - SeedVR2 for faceless wides;
   - a shared take reframed only where both formats truly read the same.

   No route changes during the edit.
5. **Subtitle style**: one frame per format, approved at the visual board. Size, position (clear of faces and the 9:16 UI zones), Korean timing.
6. **Sound decisions up front:**
   - one pitch for the note, chosen and sketched (SOUND_PLAN);
   - the dialogue route chosen from the shot 6 pilot, then fixed for 12, 13 and 14;
   - drafts with `generate_audio: false` except the dialogue-route test;
   - designed layers mixed quieter than feels right and measured against the bed;
   - the true source of every layer recorded at sound approval.
7. **Ending is decided:** shot 14's release, the river ringing out over black, then the title fades up. It is checked inside the cut with its fades on, at phone size.

## B. Judgement checks before anything goes to Jason

- **Watch as a first-time viewer:** the whole cut, real-time, phone size, sound on, both formats. Write down what was actually watched and heard.
- **One independent critique per cut:** a cold Sonnet subagent with stated coverage. Fix what it finds before the gate, not after Jason finds it.
- **Composites:** insert + cut. Never patch a moving subject. Check every frame in playback, never on samples.
- **Decode and colour:** use the bundled ffmpeg for every decode and the cut. No OpenCV on 10-bit HEVC. Match colour on an overlapping frame. Verify exact join frames. Use `-fps_mode passthrough` on frame-exact pipes.
- **When parameter sweeps don't converge after two tries, change the method** (e.g. a real photo relief instead of procedural shapes).

## C. Token budget

The target for the whole film is ≤ 80 M processed (hero ≤ 60 M, plus 20 M for the second native format), against One Beat Late's 487 M.

| Phase session | Gate it ends at | Budget |
|---|---|---|
| 1. Board (done) | board lock | (this session) |
| 2. Start frames, effect tests, subtitle frame, visual board | visual-board approval | ≤ 12 M |
| 3. Shot 6 dialogue pilot | pilot approval | ≤ 10 M |
| 4. Drafts and picture edit, both formats | draft-edit approval | ≤ 25 M |
| 5. Sound, 1080p finish, grade, title | final approval | ≤ 20 M |
| 6. Closeout and posting kit (Sonnet) | captions approved | ≤ 6 M |

Rules:
- **Hand off at every gate, or at about 300 K context, whichever comes first.** Never continue a phase past its gate in the same session.
- **One message to Jason per gate,** with all decisions together and the batch quote. Ask him for **one batch of notes per review**, not notes one at a time.
- **Subagents (Sonnet, low or medium effort)** do batch jobs, contact sheets, composites from tight specs and every-frame checks. Each hands back **one contact sheet plus a pass/fail line**. The director looks at that one image.
- **Images in context are the costliest input:** review on contact sheets, never frame by frame, and never re-open a sheet you've already judged.
- No polling: submit batches and wait once in the background.
- **Review pages go out as Artifact links** (Remote Control can't open local HTML).
- At closeout, record the actual tokens per session beside the credit spend.

## Phase 2 overrun (5 Nov 2026): about 25 M against a 12 M budget

Causes and the rules they add, for every later phase:
- **Long waits inside one growing session.** Submit a batch, end the turn, and resume when it finishes. Never wait or review in a context that keeps growing.
- **Two subagent rounds per effect.** The spec goes to the subagent once, complete, with the pass criteria written out (for example the minimum visible density at phone size). Any further round must be justified in one line.
- **Three rounds of frames with the gorge side or look direction wrong.** Put the camera side and the look direction **in words in every prompt** (for example "the gorge drops away on the right side of the frame; he looks screen right"), and check them on the contact sheet before judging anything else.
- **Cold critique skipped to save tokens.** Not allowed. Run a cheap one instead: a Sonnet subagent, low effort, one contact sheet.

## Phase 1 note (honest)

This board session went through three board versions:
- v01 wordless;
- v02 Korean dialogue;
- v03 cinematography in both formats.

On top of that came three fix sheets. Each version followed a real note from Jason, but the session is long. It ends here, at the board lock.

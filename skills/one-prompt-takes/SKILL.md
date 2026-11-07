---
name: one-prompt-takes
description: Direct a multi-shot sequence of up to 30 s from one structured Seedance 2.5 reference-to-video prompt plus reference images, with no board or start frames. Covers when to use it against the board route, the prompt template, the gates, patching a shot and finishing. Use for teasers, series fillers, chase or travel sequences and mood pieces, and as flowing blocks in a hybrid main film.
---

# One-prompt takes (Seedance 2.5 reference-to-video)

Adopted 5 November 2026 after TEST-021 "Cyber Ninjas: Airborne". Jason asked to implement the method from that exercise. Read [RETROSPECTIVE_2026-11-05_TEST021_ONE_PROMPT.md](../../guides/RETROSPECTIVE_2026-11-05_TEST021_ONE_PROMPT.md) for the evidence.

**What it is:** Seedance plans, shoots and cuts a multi-shot sequence of up to 30 s from one structured prompt plus reference images. No storyboard frames and no start frames. The director writes the film as timed beats, then patches the shots that miss.

**It does not replace the board route.** It is a second route. Source approval, spending approval per gate, the physics and living-world rules, the grade, the final delivery standard and post-copy approval all still apply.

## When to use which route

| Situation | Route |
|---|---|
| Teaser, series filler, social test, chase or travel sequence, mood piece | One-prompt take, up to 30 s |
| Main film that needs exact compositions, a locked board, or a title choreography | Board and start frames, as before |
| Main film with flowing scenes between a few exact shots | **Hybrid:** one-prompt blocks of 8–15 s for the flow, start-frame shots for the exact moments |
| Fights, contact, hands on props, two people touching | Start-frame shot, or a planned patch. Never trust the take for these |
| Dialogue that must be right (any language) | TTS and lip-sync as before. Native dialogue is untested by us; the reference creators report weak intonation |
| The film needs both 16:9 and 9:16 | Board route. Two generations are two different films |

## Steps and gates

1. **Beat sheet (free).** One line per 2–4 s: what happens, which shot, who is in frame. Climax before about 65%. Mark every risky beat (see the table above and the story risk list in [STORY_FOUNDATION.md](../../guides/STORY_FOUNDATION.md), 2026-11-07: crossing paths, small hand-held objects, on-screen text, mirrors, asymmetric features, a light change inside one shot, three actions in a row, a face hidden by a high angle, more than two or three supporting characters).
2. **References (free).** Use existing approved art: front and rear or profile per character, one state image per changing prop or costume state, one design still per vehicle or creature. Six to eight images is enough. A design with no reference image will drift between shots.
3. **Prompt.** Use the template below. **Gate 1: Jason approves the prompt on a review page.** The prompt is the board in words.
4. **Quote, then his typed yes. Draft at 480p** (`draft: true`), about USD0.134/s. Download at once; the provider keeps media 7 days.
5. **Check.** Contact sheet at 2 fps for order, identity and props. Dense strips (10–12 fps) for action beats. **Send the draft to Jason: stills cannot judge motion, weight or anatomy.** Never write "pass" on an action shot from a sheet.
6. **Gate 2: his notes.** One re-roll at most, and only for global notes (pace, camera language, tone). A re-roll changes everything, including what worked.
7. **Patch what remains** (below). Each patch has its own quote and yes.
8. **Finish.** Main spot: native 1080p. Teaser: local SeedVR2 per shot from the original files, with Jason's exception to the no-upscaled-faces rule and a face sheet for his pass or fail.
9. **Close out** by the final delivery standard. Post copy is approved before the kit changes.

## Prompt template

Plain text in six blocks. Not JSON.

```
<TITLE> — <N>-SECOND <GENRE>

FORMAT AND STYLE
<N> seconds, <ratio>. Photoreal live-action look, materials, light sources, time of day.
How flight / chase / handheld is shot. Real time or where slow motion is allowed.
"The one-second ranges below describe continuous action; cut only where a line begins with 'Cut'."

REFERENCE ASSIGNMENT AND CONTINUITY
Image 1 = <CHARACTER>, front. Image 2 = the SAME <character>, rear. <identity and costume list>.
Image N = <state>. State rules: what never changes, what changes and when.
Image N = <vehicle/prop>, with sizes in metres. "Use it for the <thing> only; ignore <other content>."
"Use the images as appearance references only. Exactly ONE <A> and ONE <B>; never duplicate or blend."
Who owns which weapon or power.

ENEMY / OTHER DESIGNS WITHOUT A REFERENCE
One fixed description, with size, colour and "identical in every shot, near or far".

LOCATION AND LIVING WORLD
Place, light, what keeps moving in the background.

SECOND-BY-SECOND ACTION AND CAMERA
00-03s: <start on action; where the camera is; who faces what>
03-06s: Cut to <...>
...
For every action beat: who faces what, camera position, "no reverse angle", hands and feet placement,
one motion only, what the contact looks like, what happens to the thing that was hit.

AUDIO
"No music, no dialogue" unless wanted. List the natural sounds in order.

EXCLUSIONS AND CONSISTENCY
No text or HUD. Weather and time locks. No duplicates. No pass-through of <named solid objects>.
No scale changes. Each failure seen in an earlier draft, named plainly.
```

Rules that came from the test:
- State sizes in metres and repeat them in wide shots.
- Do not ask for a hard physical move on camera (sheathing a sword, climbing in). Stage around it.
- Give a power its own beat and a visible consequence.
- Keep the enemy non-human if a character could blend into it.
- Words alone will not hold a prop state ("the scabbard is empty") or a design. Use a reference image or fix it locally.

## Patching a shot (about USD0.55 a try)

1. Find the bad shot's first and last frame (scene detection misses cuts in fast blur; confirm on a frame strip).
2. Take the **last frame of the shot before it** as the start frame, if its geometry suits the action. The patch then continues that shot with no cut, and the cast, set and light carry over.
3. `image-to-video`, 4–5 s, `draft: true`, `ratio: adaptive`. Prompt: "Continue this exact shot with no cut and no change of camera angle", then who faces what, one action, the consequence, the sound.
4. Stage the actor from behind or side-on, facing what she acts on. It is the easiest view for correct anatomy.
5. Cut the patch in by frame number from the original files. Trim its tail if the last frames go soft.
6. If no neighbouring frame suits, make a start frame the usual way (Codex ImageGen) and treat it as a start-frame shot.

Limits: `draft-complete` bills the whole draft, bad shots included, and cannot be trimmed. A native 1080p patch needs a 1080p start frame taken from the completed take. For a natively finished film, generate in blocks so only kept blocks are completed.

## Cost and effort (TEST-021, 29 s teaser)

- Provider spend: USD8.57 (two 30 s drafts at USD4.01, one patch at USD0.54). SeedVR2 finish free, 54 min.
- Agent tokens: 53.6 M processed tokens for the whole job, method research and closeout included, against 105.9 M for TEST-018 and about 487 M for One Beat Late.
- Token hygiene still applies. In TEST-021 the drafts phase cost the most (20 M) because render polling re-read a large context about twenty times. Run drafts in a fresh session after the prompt is approved, and give page builds, filing and the posting kit to Sonnet subagents.

## Records to keep in the experiment folder

Prompt versions as sent, each quote and approval, draft files with SHA-256, a check file per draft, a patch record, the cut list by frame numbers, the finish record, and a token count.

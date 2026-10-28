# Video production playbook

2026-10-12 — Rules learned from The Tide Remembers. Read after verifying the approved foundation and before the first paid video call. Keep provider/model choice open; one successful session is not a universal ranking.

## 1. Start with a small, complete directing packet

Use the exact approved revision, selected reference IDs and hashes, shot intent, locked framing/style, sound perspective, delivery settings and a usable credit/attempt allowance. Start a fresh production context after provider research when possible. Carry the compact checkpoint, not the entire research discussion. Read only needed tool schemas and batch independent inspections.

## 2. Establish world physics before generating

Write a short interaction brief: medium (air/water/vacuum), gravity/drag, material response, particle type, emission origin and listener perspective. Specify positive motion behaviour and forbidden category mistakes. For submerged scenes: trapped sediment can form a cloud, but its dispersion must feel water-damped; exhaust bubbles originate outside a dry helmet and rise separately from the sediment. Avoid cosmetic surface rings as a substitute for volumetric interaction. Preserve deliberate fantasy while making the chosen physical rules coherent.

State character identity, the meaning of left/right, single-contact timing, continuity and current camera locks. If Jason likes the first shot, keep its framing, camera and performance while fixing the defect.

## 3. Inspect the first take for the actual failure mode

Before polishing or making aspect variants, inspect the first/middle/end and a short contact/emission sequence. Check identity, geometry, action order, physical medium, bubble/particle origin and continuity. A completed job, good thumbnail, different colour or isolated frame is not a passed motion check. Use normal-speed human playback/listening where host media perception is unavailable; state that limit rather than inventing an audition.

## 4. Choose the correction route by the defect

- Appearance/colour: local finishing or a targeted appearance edit may suffice.
- New dynamics/interaction: use a source-video motion edit or regeneration with the actual source/identity anchors. A tint, small overlay or reframing cannot establish water drag or change the underlying fluid motion.
- Framing: change it only to serve the requested adaptation or an authorized staging change. Do not hide a physics fault behind an unexpected enlarged cut.
- Sound: define the listener perspective; use a controllable stem when needed, replace the old attack instead of doubling it, and align to the inspected contact.

Make one hypothesis-led retry. If it misses the requested change, report the exact fault and switch strategy only within the approved attempt/credit allowance. Do not spend a series of cosmetic passes on a dynamics problem. The local Omni edit failed here; the later Seedance source edit gave a visible exterior exhaust while retaining the chosen medium framing. Future providers still need live capability/cost verification.

## 5. Validate inputs and tool arguments before submission

Use current schemas. Known pitfalls from this session: ratio versus explicit canvas dimensions are alternatives; fromItemId cannot be combined with type/assetId; sourceIn is microseconds while timeline positions/durations are frames. Level aliases on cloned-item adds were rejected before clone resolution—use explicit typed adds or update the created item. Set/read the actual project FPS before calculating trims.

Decode prepared media and verify its frame count, dimensions and duration before importing/submitting. An audio-length or container-duration field alone did not prove a four-second video handle. For the final Seedance input, 78 source frames plus 18 held frames at 24fps passed the 96-frame check. Check the active model's minimum source length. The SFX service rejected a prompt above 450 characters in this session; check current limits and measure the prompt before submission.

## 6. Approve the horizontal master, then adapt

Read [FORMAT_AND_RESOLUTION_WORKFLOW.md](FORMAT_AND_RESOLUTION_WORKFLOW.md) for the 2026-10-12 cost/pixel comparison and daily-versus-showcase decision. Plan both frame paths before generation; preview portrait coverage during first-take QC and lock it before one upscale finish. Mini→another model is a new take, not a guaranteed high-resolution copy. For moving portrait windows, enhance fixed overscan before panning; reuse finish scripts rather than authoring a new pipeline for each note. Higher landscape resolution improves detail but does not resolve poor portrait staging.

Plan the portrait pixel budget before generation. A full-height 9:16 crop of a 1280×720 landscape source contains only about 405×720 native pixels; exporting it at 720×1280 or 1080×1920 does not restore detail. When both formats are requested, choose a source-resolution/native-portrait strategy or reserve a genuine super-resolution finishing pass, then inspect the whole portrait clip at delivery size. Keep the daily resolution/budget preference in force; do not automatically pay for 4K. On 2026-10-12 a local Real-ESRGAN x4plus pass was used on all native portrait frames, with conservative blending and no separate face restoration. Framewise enhancement can estimate texture and shimmer; inspect consecutive face/bubble frames, not just a thumbnail. Preserve the approved sound by stream copying and verify its compressed payload.

Finish one horizontal picture/sound master and get Jason's explicit approval of its identifiable revision. Freeze its bytes, approval scope and SHA-256. Derive the vertical/social versions from that approved master so crops cannot move a live bubble overlay into the helmet or alter the approved mix. Check crop readability at the strike, valve release, whale reveal and ending. Aspect changes may need editorial reframing; do not regenerate by default.

## 7. Close with evidence and a compact handoff

Deliver a self-contained folder directly (Jason preference, 2026-10-12). Include final media, posting copy, a README with the selected filenames and approval/review scope, manifest hashes and production records. Link the actual folder and files. Do not create ZIPs automatically; Jason will zip manually if needed. Existing ZIPs remain historical outputs, and older dated packaging scripts are not the future delivery default. Approval verification and frozen source snapshots remain required independently of archive packaging.

Preserve raw takes, failed attempts and earlier exports. Save the actual prompts/jobs, chosen reference roles, source-edit versus finishing changes, output hashes, approval scope and unresolved perception limits. Distinguish credits estimated, allowed and actually billed. Track generated jobs separately from exports; resizing is not another generated take. Record a short next-agent checkpoint, posting copy and actual deliverables. Do not publish without publication authorization.

These steps reduce avoidable loops; they do not guarantee one-take success or exact generative preservation. Bold creative exploration remains welcome within the approved foundation and session limits.

## 8. Keyframe-first rules (2026-10-14, from Solar Etiquette)

Learned on DCL-20261013-SOLAR (Claude Opus 5.5 + ChatCut Seedance 2.5): five revision rounds and about 13 credits of avoidable retries. These rules hold for any first/last-frame video model, any agent and any app. Evidence: experiments/TEST-007/RESULTS.md, COMPARISON_FILM01_vs_FILM02.md and LESSONS.md (2026-10-14 entry).

**Before the first paid submission, check the keyframes, not just the prompt.** The frames decide motion; the prompt only nudges it.

1. **Final acting lives in the end frame.** Eyelines, head turns and the closing pose must already be in the last frame. Characters look AT the subject that motivates them (the giant fan), never into empty air, and hold that gaze to the end.
2. **Moving objects take their direction from the keyframes.** The end frame must show each object (cars, creatures, vehicles) further along its intended path. The model interpolates endpoints, so "left to right" in the prompt loses to frames that say otherwise.
3. **Start and end frames must share one background.** Separate image edits redraw small details (plants, steps, props), and the model cross-dissolves them into visible ghosting. Composite the changed foreground over the start frame's exact background, or derive one frame from the other.
4. **Change only what should animate.** Derive the start frame from the end frame, or the reverse, so object geometry and orientation match. Mismatched geometry makes the model invent bridging motion, such as a fan flipping edge-on or light running backwards.
5. **Light must follow its cause.** State when the occluder covers the light, then check mid-shot luminance on the first take. The shadow may arrive only after its cause, never before, and never brighten again.
6. **Camera moves:** image editors barely move the camera when asked for an orbit offset. Get depth from a real first-frame-only move or from foreground parallax, not from a derived offset still.
7. **Repairs:** fix motion at the source, by regenerating with corrected keyframes. Never paste 2D cutouts of moving objects: no haze, wrong light, wrong texture, a mask that clips the background. If a local fix is unavoidable, re-place the model's own per-frame renders and keep them clear of complex backgrounds.
8. **Reframes and edits:** cut on an eyeline (show what the character looks at), and use one continuous eased camera move per shot. Hold → move → hold, reversals, or a reframe across a cut read as jumps.
9. **QC every take at mid-shot, not just first/last frames:** ghosting, doubled props, object direction, gaze target, shadow timing. Then do normal-speed playback with Jason.
10. **Ops:**
    - Wait for an output file newer than the submission.
    - Verify the encoder with ffprobe.
    - Read the credit balance before and after each job.
    - Agent-mode chat turns can bill credits.
    - Prefer an installed integration over screenshot-driven typing, which is token-heavy.

Jason's bar: "we shouldn't deliver unpolished work." Polish means correct motion and acting, not only resolution.

## 9. Director-mode rules (2026-10-14, film 3, The Unstitched)

Details: [RETROSPECTIVE_2026-10-14_VIDEO_AGENTS.md](RETROSPECTIVE_2026-10-14_VIDEO_AGENTS.md). Film 5 additions (2026-10-20): [RETROSPECTIVE_2026-10-20_FILM5_DIRECTING.md](RETROSPECTIVE_2026-10-20_FILM5_DIRECTING.md) — blocking map and timed animatic before paid motion, and the director-owned pre-review checklist.

1. **No locked-camera films.** Frames mode with same-camera endpoints gives zero ghosting and zero cinema. Default to first-frame-only shots, each with one named, eased camera move.
2. **Build coverage.** Generate per-shot start frames. Derive neighbouring shots from one hero frame so the world matches. Prefer an edit model (gpt-image-2.5-sunburst) for changes to a good frame. Check every nano-banana output for identity or style drift and mirrored makeup.
3. **A grade unifies; it doesn't relight.** For a world mismatch (time of day, sky, buildings), regenerate that region of the start frame, then match its colour statistics locally. Show Jason a start-frame-vs-world comparison before paying for video.
4. **QC at full resolution, mid-motion:** hands, faces, asymmetric makeup and ornaments. Trim takes before orbit drift mirrors features.
5. **Music first.** Offer 2–3 beds, let Jason pick by ear, duck for tension, put SFX on causes.
6. **Finishing order:**
   - Approve and freeze the master.
   - Real-ESRGAN on grain-free frames, then grain.
   - 9:16 from the 4× frames with a preview sheet first.
   - Reuse `experiments/TEST-009/{assemble.py, finish_1080.py, reframe_portrait.py, work/grade.py}`.
7. **Ops:**
   - Use the ChatCut hosted MCP plugin, not computer use: about 70% fewer tokens per finished second.
   - Max 3 concurrent video jobs.
   - New ChatCut timelines default to 30 fps.
   - Read the balance in the editor header (account menu → Credits history).

## Shared final-render closeout — added 2026-10-14

Read [FINAL_DELIVERY_STANDARD.md](FINAL_DELIVERY_STANDARD.md). Every video agent must deliver the exact approved finished MP4 to `FINAL_RENDERED/PROJECT-ID/video-REVISION/`, with README, approval statement/scope/hash and DELIVERY.json provenance. Verify source/copy SHA-256 equality, actual media properties and full decoding; preserve sources and older finals. Update `FINAL_RENDERED/INDEX.md`/`INDEX.json` and return shared-library/exact-video links. Reviews and authorised but unapproved aspect derivatives stay in experiments/delivery with their actual scope; do not silently treat them as approved. No automatic ZIP/publication. Root closeout rule applies to future sessions using older frozen packets without altering those packets. Include this standard alongside directing guides in future portable review/approved handoffs, linked from START_HERE.md.

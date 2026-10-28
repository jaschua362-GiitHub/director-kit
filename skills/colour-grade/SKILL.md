---
name: colour-grade
description: Final colour grade and exposure protocol for every film and its social cuts (16:9, 9:16, titled/untitled) — measure, grade to colourist targets, match deliverables, QC before render and delivery. Use whenever a film is finished, graded, regraded, or adapted to another aspect ratio. Written from WIND (2026-10-17), whose approved v07 had to be regraded because it was too dark.
---

# Colour Grade — film colourist protocol

A grade is checked with measurements, not by eye on one monitor. Viewers mostly watch on phones in daylight, so a mood
that looks right on a dark desktop screen reads as "too dark" there. Grade for Rec.709 SDR (gamma 2.4 mastering,
watched at ~2.2), and keep the mood with contrast and colour, not by pulling down the whole exposure.

## What went wrong on WIND
- v03 looked "too bright / CGI". I fixed it by darkening everything: −0.6 EV and a filmic curve whose white point was never reached.
- The approved v07 measured: faces ~25%, the brightest highlights capped at ~80%, overall picture level 23% (16:9) and 19% (9:16). Feedback: "a bit dark".
- Fix (v08 / vertical v03, approved): look preset **E1** — faces ~35%, speculars 92–95%, blacks 2–3%, APL 33% / 29%.
- Lesson: a CGI look is fixed with highlight roll-off, halation, texture, grain and contrast shape. Lowering exposure only adds a second problem.

## Targets (BT.709 luma, % of full scale, measured on the delivered file)
| Measure | Target | WIND E1 |
|---|---|---|
| Black (p2 of a shot) | 1–3%; never clipped flat, never milky above ~5% | 2–3% |
| Skin, median of face pixels | 35–45% low-key drama; 45–55% normal key; lit side up to ~60% | ~35% |
| Speculars (p99.9: sparks, gems, window light) | 90–97%; no large flat clipped areas | 92–95% |
| Average picture level (whole film) | 25–35% for a moody piece; below 20% reads dark on a phone | 33% |
| Darkest shot APL | ≥ ~18% unless it is a deliberate black beat | ~21% |
| Shot-to-shot skin match within a scene | within ±3 points | — |

Night or black-beat shots may sit outside these numbers on purpose. Write down why for each one.

## Process
1. **Work from the pre-grade picture.** Never grade on top of a graded file: grain and curves would stack. Upscale (ESRGAN) before grain; add grain once, last.
2. **Measure the current state.** `experiments/TEST-010/work/luma_report.py <video>` gives per-shot mean, p2, p50, p98, p99.9 and APL. `work/grade_tune.py '<presets json>'` grades one frame per shot for both formats and reports APL, skin median, p2 and peaks for each candidate.
3. **Grade in this order:**
   1. exposure, so the face lands on target
   2. white point, so speculars reach ~92–95%
   3. mid lift (display gamma)
   4. re-seat black to 1–3%
   5. contrast shape and highlight desaturation
   6. halation
   7. vignette, ≤ 0.20 on 16:9 so it isn't heavy on phones
   8. grain

   Start from preset `E1` in `work/look.py` (`ev -0.15, k 1.12, wp 1.3, gam 0.82, blk 0.025, vig 0.20, grain 3.2`); preset A is history.
4. **Compare on stills before rendering video.** Make one board: the current grade plus two candidates, the same frames in 16:9 and 9:16, including a face, a highlight-heavy shot and the darkest shot. Pick the one that hits the targets with solid blacks.
5. **Match deliverables on skin, not on APL.** 9:16 crops drop bright backgrounds, so their APL is naturally lower. Lift the 9:16 slightly (WIND: `E1V`, +0.07 EV) until faces match the 16:9.
6. **Titles and graphics keep their approved design.** Copy title frames unchanged instead of re-grading them.
7. **Render, then re-measure the delivered files** with `luma_report.py`. Check:
   - all frames decode
   - the audio packet MD5 equals the approved master
   - the before→after numbers are written in the approval record

## Delivery
- A grade change to an approved film is a new revision (for example v07 → v08). It needs Jason's explicit approval, and the previous final stays as history.
- Every final's APPROVAL.json states the grade preset and its measured face, highlight and black levels.
- Before asking for approval, tell Jason to check the film on a phone.

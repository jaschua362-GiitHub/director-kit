# Vertical card

Read this when you start the vertical stage. Required reading: `DIRECTOR_CRAFT.md`, the three every-session cards, this card and your handoff. The Lab keeps a longer depth file behind this card; it is not in the kit.

## What this stage is for
The 9:16 Reel is what most viewers see. It tells the same story, hero readable on a phone. Jason judges framing in motion, and cost.

## One format per film (his ruling, 25 Nov 2026)
"Agree, default 9:16 vertical". Each film is built in **one** format, fixed at the story gate in lock row 1 before boarding, and every board, plate and take is made for that format only. This is part of the USD 35 film budget (`money-and-approvals.md`); building two formats is part of what pushed Small Cargo to USD 1.20 a second.
- **Default: native 9:16.** It goes to Reels, Shorts and TikTok as one master. Board for vertical from the start: one subject per frame, height and depth, faces, falling or rising action. A horizontal idea squeezed into 9:16 reads cheap.
- **16:9 only when the story needs width** (landscapes, chases across the frame, two characters facing off, a YouTube main, Behance or client piece), and only with his yes at the story gate.
- **A 16:9 film buys no native vertical takes.** Its Reel is a letterbox in 9:16 with the title in the bands (free), or free local crops where the action fits the 608 px window. The crop and native rules below apply only to a film he has chosen as 16:9; for those, natives now need his separate yes inside the USD 35.
- **A 9:16 film gets no 16:9 version.** It can't be widened well; don't offer one.

## What good looks like
- The hero whole and central, props swinging into her frame, centred at each shot's end. *Wind the Man.*
- Action staged inside the centre 32 % of the 16:9 frame, so most shots become free crops. *House of Courtesy.*
- One eased window move per shot, in one direction.
- Faces keep original pixels; only floor, ceiling or sky is extended. *Wind the Man: he rejected an extended face.*

## Look for
1. Face, prop and second figure measured against the 608 px window (the 9:16 slice of 1920x1080) at start, middle and end. *House of Courtesy B9 cut the doll: "Abit more right so doll can be seen but not cutting off her face".*
2. Every cropped face at 100 %, then the whole Reel at phone size. Crops enlarge 1.78x: report softness plainly. *House of Courtesy B7; The Tide Remembers.*

## Let the script check
- Crop width = source height x 9/16 (608 px from 1080p). `not built: do it by hand`
- Pan speed under 100 px/s over detail, 300 for action. `not built: do it by hand`
- Shutter blur above 7 px/frame at 24 fps. `lab script, not in kit: build_vertical.py`

## How this stage runs
- **Route:** each shot is a CROP of its approved 16:9 take; NATIVE VERTICAL (its own 9:16 start frame and take) only where the action spans wider than the 608 px window. *House of Courtesy: natives quoted USD 7.23; only B5 needed one (USD 0.64): "reuse 16x9 scene if possible unless scene absolutely cannot fit the composition".*
- Decide routes at the start-frame gate (where video start frames are approved), in lock row 1 (the format row). Natives are quoted in that gate's one batch; show each 480p draft before its HD. *Small Cargo decided late: 103 M tokens; House of Courtesy natives skipped drafts, came back near-still.*
- The edit handoff carries each shot's route and crop window. *House of Courtesy: "we had plan the framing for 9x16 but the edit didnt follow it".*
- Before rendering, show a real-time 540x960 preview with audio; take all notes in one round. *Wind the Man: four framing redos.*
- Extension rescues one failed shot: one Seedream still, tracked locally. *Small Cargo.*
- Sessions and models: the handoff card.

## Settled
- Crop by default; native only where the action cannot fit.
- Natives are bought with the 16:9, not after the master.
- Band fill is one tracked still, not per-frame video fill.
- Cropped faces stay plain crops; a failing face goes native.

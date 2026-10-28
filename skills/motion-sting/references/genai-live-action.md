# AI-generated live-action promo — the process (photoreal people + product, cut to music, ending on a sting)

Distilled from the coffee-brand brand-model promo (2026-10-09; 11 versions; v11 approved: "very natural now").
Reference project: `<PROJECTS>\<Brand>\Motion\brand-model-promo-10s\` (`BRIEF.md`, `assemble_v5.py`,
`audio/foley_v5.py`, `review_log.md`). Script templates: `<SKILL>/scripts/genai_assemble_template.py`,
`<SKILL>/audio/foley_template.py`.

**The lesson in one line:** v4 looked like an AI showreel of beautiful but unconnected inserts. v11 works because it
follows a real **process with people in it**: real gear, real props, focused hands, a smile only at the payoff,
music, and cuts on the beat.

---

## 0 · Defaults (don't re-ask Jason these)
His standing direction for brand and brewing films (from the brand's promo-film preferences note, not included):
- **Realism over polish.** Ask for documentary, handheld, natural light and real imperfection. Grade afterwards.
- **Real pro gear, by name, with reference images:** Mahlkönig EK43 ("EK47" = EK43), Fellow Stagg kettle, ceramic
  UFO dripper, glass server, black scale.
- **Light roast for filter:** grounds are light tan; the brew is clear amber/tea-red, never black.
- **Acting:** eyes on the work while brewing, a calm focused face, no smile at camera. Smile only at the payoff.
- **Framing:** one frontal brewing shot, plus counter-height three-quarter shots in the style of World Brewers Cup coverage.
- **Props:** several of the brand's coffees, scattered like a working counter. A neat lineup reads as fake. No hard sell.
- **People:** a second barista working in the background.
- **Story = process:** grind → brew → drip → swirl → present → logo.
- **Music is expected.** Cut on the beats.
- **Length:** 15 s (≈ 10.5 s live + ≈ 4.5 s sting, logo held ≥ 2 s).
- **Ending = the 2026 season end card** (Jason, 2026-10-09): `<PROJECTS>\<Brand>\Motion\end-card-2026\`
  (sting v5 from 5.2 s, 4.8 s, 60 fps, 9:16 + 16:9, ProRes masters). Enter it with an overhead-cup match cut; the spec
  is in its README.

## 1 · Pre-production (no credits)
1. **Character bible** in `BRIEF.md`: face, hair, wardrobe (locked), manner, set, kit, hero products. Give her a
   working name. Every generation references `refs/model_ref.png` and the **character sheet**.
2. **Reference study.** For a YouTube link, the video layer won't screenshot. Pull its **storyboard thumbnails**
   instead: in the page, `ytInitialPlayerResponse.storyboards.playerStoryboardSpecRenderer.spec` → level-3 sheets
   `https://i.ytimg.com/sb/<id>/storyboard3_L3/M<n>.jpg?sqp=…&sigh=<sig>` (320×180 tiles, one per 5 s). Read only
   the relevant section (Jason: "just a few scenes"). Write down the framing grammar, not the content.
3. **Refs folder:** gear photos (transparent PNG fine), every product bag from `<brand product images>\`,
   and the model. Give them simple names; the asset names become words in your prompts.
4. **Shot list with beats.** 6–8 shots, each 1–3 s, plus the sting. Decide which shot carries each brief point.

## 2 · Tools and money
- **Generation:** ChatCut desktop app (Jason's credits), driven by computer use. Driving notes are in memory
  `chatcut-desktop-driving`: type in **≤ 15-character chunks**; never paste; navigate the file dialog by clicking.
  Assets land in `%APPDATA%\ChatCut\projects\<id>\project.chatcutproject\assets\{image,video,audio}\` —
  copy from there, never export.
- **Higgsfield MCP** is connected but had 0 credits (free plan) in Oct 2026. Same model family; Plus is $39–49/mo.
- **Costs (ChatCut, Oct 2026):**

  | Item | Credits |
  |---|---|
  | Nano Banana still / edit | ~1.5–2.5 |
  | Seedance 2.0 1080p 5 s | ~6.6 |
  | Seedance 2.5 1080p 5 s | ~11.1 |
  | Kling Pro 1080p (quoted 0.8 cr/s) | failed on ChatCut's side twice → don't plan on it |
  | Music (16 s requested; you get a ~3 min track) | small |
  | **Whole spot incl. retakes** | **≈ 180** |

  Budget **~120 credits** for a first-time-right 15 s spot.
- **Model choice:** Seedance 2.5 for faces and hero shots (frontal brew, presentation); Seedance 2.0 for hands,
  gear, liquids and overheads. Generate 5 s and use 1–2 s of it.
- **Approve each job individually** (per-job "Allow" with its credit estimate). Check every keyframe before paying for its video.

## 3 · Generation — what worked
- **Keyframes first** (Nano Banana, 9:16, 2K), one per shot. References: character sheet + gear + bag images.
  Put this **realism line** in every prompt: *"shot on ARRI Alexa, 35mm, natural available light, real-world
  imperfections, real skin texture, slight handheld framing, documentary feel, nothing too perfect or glossy;
  must look like a real photo, not AI."*
- **Video prompts:** *"real camera footage, natural real-time motion, subtle handheld camera breathing, no morphing,
  faces and labels stable"* plus **one clear action** per clip. Put the action you need in the first 2 s
  ("from the first frame she…"). A soft verb like "gently swirls" produced no swirl twice; "a SWIRL… the coffee spins
  in a visible vortex… for three seconds" worked.
- **Edits drift.** A Nano Banana edit asked to "change only X" can repaint the set and the face (G2c: white walls,
  different woman), or change nothing at all (G2d). After one failed edit, **composite locally** with the real
  product photo: key out the background, erode the alpha 2 px, kill colour spill, warm-grade it and darken it toward
  the window light, blur it ~1.4 px, add a contact shadow, and restore foreground objects (the towel) over its base.
  The label then reads exactly as the real one.
- **Label text** on generated bags garbles. Either composite the real label, or put the near bags in shallow-focus blur
  in the edit (a feathered `gblur` mask). Never let garbled text sit sharp.
- **Mirrored or garbled digits** (scale displays) are baked in. Frame them out with a crop.
- **Match-cut plate:** the overhead cup must be a **true 90° top-down**, centred, with nothing but counter around it
  (no hands, no kettle blob), and its contents must match the story (white cup, amber coffee). Brief this in the keyframe.

## 4 · Edit (local, ffmpeg — not ChatCut's timeline)
Template: `scripts/genai_assemble_template.py`. It is data-driven: a `SHOTS` list of
`(clip, in, dur[, z0, z1, ax, ay[, 'flip']])` entries:
- **Cut on the music.** Run `audio/beats.py` on the track, then make shot durations whole numbers of beats (0.626 s at
  96 BPM) and land the match cut on a downbeat. Fade the music on a bar line before the end.
- **Push/punch per shot:** zoom z0→z1 anchored at pixel (ax, ay); `x = ax·(z−1)`, `y = ay·(z−1)`.
  - Anchoring at the top (`ay = 0`) pushes foreground clutter out of the caption zone.
  - Anchoring at the bottom (`ay = 1920`) crops a lamp or ceiling.
  - Anchoring bottom-left removes a face slice at the top-right.
  - To centre a macro on point (cx, cy) at zoom z: `ax = (cx·z − 540)/(z−1)`, and likewise for y.
- **Grade for realism** (live shots only):
  - `deband`;
  - an espresso-brown floor: `curves r 0/0.085, g 0/0.055, b 0/0.04` (the no-black rule);
  - light temporal grain: `noise c0s=7 t+u`.
- **Match cut into the sting:**
  - Measure the cup rim on a frame: centre and diameter, using the bright-rim pixel percentiles inside a central ROI.
  - Push the overhead shot so the rim diameter equals the sting disc (665 px, centre 544,956) on the last frame.
  - Then a **4-frame (0.13 s) dissolve** into the sting at source 5.2 s.
- **The sting is sacred:** play it **untouched at native 60 fps**. No push, no scaling: a per-frame scale rounded to
  2 px made the forming wordmark jerk (Jason caught it in v10). Export the whole film at 60 fps.
- **Hook:** frame 0 is the Reels thumbnail. Open on the most kinetic, non-repeated image (v11: a macro of amber
  coffee swirling in the server). Don't reuse a later shot's framing for the cold open.
- **Sound:**
  - Music (−4…+2 dB) + foley (`audio/foley_template.py`, cues = the cut times) + sting audio at −7 dB.
  - Loudness: two-pass gain to −14 LUFS, then `alimiter` at −3.2 dB; AAC then lands at ≈ −2.8 dBTP. A −1.8 limit overshot after AAC.

## 5 · Review (critic gate)
Run `references/critic.md` with the brief points pasted verbatim. Add an 8th criterion, **Realism**. Expect 3–6 rounds.

Checklist of what the critics caught, so v1 avoids it:

| Problem | Fix |
|---|---|
| Brown mug of black coffee vs "light roast" | Brief cup colour and liquid colour in the keyframe |
| Frozen grin / mannequin-still lead | Ask for blinks, a glance down then up; trim holds to ≤ 2 beats |
| No swirl | Explicit vortex prompt (above) |
| Face sliced by a frame edge | Punch away from it |
| Bags in the caption zone (y > 0.80) | Top-anchored punch or blur |
| Same framing used twice (cold open = later shot) | Use a different source or angle |
| Same-size jump cut | Punch the second shot ≥ 15 % |
| Logo held < 2 s | Shorten live shots by whole beats |
| Lamp pops on between cut-in shots | Crop it out of the second shot |

The critic is harsh on AI realism (it stopped at 7s). Jason's verdict is the real gate: v10/v11 at critic 7–9 was
approved. Stop when the remaining items need regeneration and the budget is gone, and say so plainly.

## 6 · IG post (part of the deliverable, not an afterthought)
Write it in the same session as the film. Template: `<PROJECTS>\<Brand>\Social\2026-10 Brand model promo\caption.md`.
- **Angle:** brand awareness first, not a sale. Jason: "more friendly, heart-warming… to taste the final brew from our
  farm-direct partner". Tell the journey the film shows (farmer → our roast → the pour → *your* first sip) and
  hand the last step to the viewer ("The last step is yours").
- **Voice:** from the Sept 2026 sting caption: "From farm to cup, with heart", farm-direct partner farms, gratitude to
  supporters, sign-off "<Brand> · <tagline>". Bilingual: English plus the local language. Polite particles and honorifics must match who is speaking.
- **No hard sell:** no prices and no product list in the caption body. Bean names and the shop link go in an optional
  first comment.
- **Package:**
  - cover frame (the warmest moment, e.g. the cup offer);
  - alt text;
  - hashtags (brand + farm-to-cup + origin region, both languages);
  - a story/poll idea;
  - a "before posting" list: AI label, music licence, farm claims to confirm, local-language tone.
- **Show it in chat:** paste the EN caption, local-language caption, first comment and alt text as separate copy-paste code blocks in the reply (Jason posts from the chat, not the folder).

## 7 · Deliver
## 7 · Deliver
- **Upload file = 30 fps** (`assemble … --ig`): Reels plays 30 fps; a 60 fps 24 Mb/s file stuttered at the logo after IG re-encoded it. Use the sting's native 30 fps master, ~10 Mb/s (`-maxrate` same), `-g 30` keyframes. This machine's ffmpeg has no working High-profile H.264 (libx264 absent; nvenc/qsv/amf fail; h264_mf = Baseline) — Baseline at 30 fps / 10 Mb/s uploads fine. Keep the 60 fps file as a master in `masters\`.
- `Brand_<Piece>_<dur>_v<N>_1080x1920_60fps_sound.mp4` → `<PROJECTS>\<Brand>\Social\<YYYY-MM> <piece>\`,
  with `caption.md` (EN + TH), a cover frame and the character sheet. Superseded versions go into `superseded\`.
- Caption notes to flag:
  - the AI-generated people and set (Instagram AI label);
  - the music licence (ChatCut AI track);
  - product names currently on sale (no prices unless taken from the brand's official price list);
  - label typos found on the real artwork ("ACHI COFFE FARM").
- Log in the project notes. Never post without the creative lead's approval.

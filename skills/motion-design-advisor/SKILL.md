---
name: motion-design-advisor
description: Decide HOW to make a motion / video / CG piece before production starts — which route (code-built motion, 3D via Blender, AI video generation, real footage, or a hybrid), which tools, what it costs and what the licensing risk is — then hand off to the production skill. Use whenever the user asks "how should we make this", "what workflow for…", "can Claude do this", "is <tool> worth it", shares a post/video/workflow and asks if it's useful, or starts any new motion, commercial, product, character, robot or cinematic short-film job for a brand or client — even if they don't say "advisor".
---

# Motion design advisor

Pick the cheapest route that can actually deliver the shot, reuse what is already built, and only pay for a
tool when a specific shot needs it. Decisions below were researched with Jason (Oct 2026) — don't re-research
them unless the question is about something newer; do re-check prices before any purchase.

## 1 · Route by what the shot must DO
| The shot needs… | Route | Production skill / tool |
|---|---|---|
| Logo, type, graphs, UI, icons, illustrative motion, recipe/data explainers | **Code engine** (deterministic canvas, motion blur, synced sound, critic loop) | `motion-sting`, a brew-guide skill (not included), `business-motion-film` |
| A still brought to life: push, parallax, glow, HUD, particles, light sweeps | **Image → layers → code (2.5D)** | image gen + `motion-sting` engine |
| An object/character that **turns, walks, moves limbs, transforms**, camera orbits, same subject across many angles | **3D route** (below) | Blender connection + code engine for VFX |
| Organic chaos that is slow to animate: smoke, liquid, cloth, crowds, people acting | **AI video gen** for those shots only | ChatCut (Seedance) / one multi-model platform |
| Real product, real place, real process (pours, roasting, farm) | **Real footage** first — free and authentic | footage layer (`motion-sting/references/footage.md`), ChatCut for edits |
A flat image can never rotate in 3D: if the subject must move in space, it is the 3D route or video gen, not code.

## 2 · The 3D route (image → 3D → Blender → code VFX)
Source: @studio_oneroom (10 Oct 2026) made a robot film with NO video-gen AI — image → Tripo (image-to-3D) →
Blender animation → After Effects text/FX, most steps done by Opus 5.5. Every step stays adjustable; the author's
caveat: quality depends on the maker's skill — pure video gen still looks better out of the box today.
Our version (no AE needed):
1. **Look:** generate the design image (Midjourney / any image model); front-ish view, clean silhouette, plain bg.
2. **Image → 3D:** Blender MCP `generate_3d` (1-3 min, may cost a credit) — or Tripo for higher fidelity.
   Size it with the reported bounding box; check topology/textures in `look` renders before animating.
3. **Animate in Blender via MCP** (`execute_blender_code`): camera moves, rotations, simple rig/IK, lights, HDRI
   (Poly Haven via `search_assets`). Tested: "BLOCK BRAWL" fight scene, 2026-10-08 (safe mode: no lambdas,
   no `time` import). Render EXR/PNG sequence (Cycles for photoreal, Eevee for speed).
4. **Finish in code:** footage layer brings the render in; add titles, HUD, glows, motion blur, synthesised
   sound; review pack + independent critic (`motion-sting/references/critic.md`). AE only if Jason wants to
   hand-tweak final layers.
Strengths: total control, consistency across shots, cheap retakes. Weakness: realism ceiling = model + animation.

## 3 · Tool decisions (Oct 2026)
- **Higgsfield / Katana:** NOT needed. Katana = Claude Opus + Higgsfield presets + paid credits; our skills
  cover the motion side. Account is free / 0 credits; MCP generation needs a paid plan. Only buy one month if a
  project needs Higgsfield-specific generation.
- **ChatCut:** the cheap generation + edit option, account exists (~180 credits after 2026-10-08). Seedance 2.5
  ≈ 0.9 cr/s 720p, 2.2 cr/s 1080p; Seedance 2.0 mini 0.12 cr/s 720p. It generated without a price prompt —
  always estimate seconds x rate and confirm with Jason first. Switch its agent to the ChatCut agent (default
  Codex hit limits). Driving notes: memory `chatcut-desktop-driving`.
- **Multi-model platform for client work:** pick ONE (OpenArt looked cheapest per clip: Seedance 2.0 720p 5 s ≈
  $0.45 vs Higgsfield $0.76 vs Magnific $0.98); others pay-per-project. Filmera free tier to compare models.
- **Models by shot:** Veo 3.1 = hero single shots + audio (≈8 s); Seedance 2.x = character continuity across
  shots; Kling 3.0 = directed multi-shot/action, cheapest; Sora 2 = physics/camera.
- **Finishing:** Magnific (now Freepik's whole platform; upscale, relight, video upscale) — one month per batch.
  Topaz Video (~$299/yr) skip unless heavy restoration.
- **Blender:** free, installed (5.2, RTX 3080), MCP connected — default for photoreal product/hero CG.
- **Remotion:** installed, unused (canvas pipeline chosen). **HyperFrames:** not installed — only worth it for
  text/UI-heavy SaaS-style client films (`business-motion-film` assumes HTML/GSAP). **fframes** (Rust/SVG GPU
  renderer): parked — too new; instead speed up our renderer (parallel Chrome, draft mode, variant gallery —
  plan in `MEMORY/daily/2026-10-10.md`).

## 4 · Client / commercial licensing
Only native Adobe Firefly carries IP indemnity (partner models inside Firefly do not); Sora API/business and
Runway Enterprise offer some. Free tiers usually forbid commercial use. Pure AI output is likely not copyrightable
(US) — Jason's protectable work is the edit, motion, compositing, sound. Always: paid tier, per-shot generation
ledger (tool, plan, date, prompt), save terms on the day, clear likenesses/trademarks; Firefly-native when a client
contract needs indemnity. Not legal advice.

## 5 · Style library
`references/style-library.md` — Jason's recurring looks (coffee-brand warm craft, recipe explainer, live-action
brewing promo, SaaS/UI launch, CG robot/character, hand-drawn/anime) with status, reference file, route, tools and
a starting move. When he names a style ("in the robot style"), start from its entry; when a new look ships, add one.

## 6 · How to answer
1. Ask only what changes the route: what must the subject DO, how many shots/angles, real footage available,
   client or own work, deadline/budget.
2. Recommend ONE route (table §1) with the cheapest tool set, what we already have, and any spend with a number.
3. If he shares a post/workflow: read it, say what it really does, compare against §1-3, and give a verdict
   (adopt / adapt into a skill / skip) with the reason. Log new decisions here (small edits, dated).
4. Hand off to the production skill; production quality gates live there (critic loop, craft rules).

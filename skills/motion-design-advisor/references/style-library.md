# Style library — Jason's recurring looks

One entry per look: status, reference, route, tools, rules, how to start. "Proven" = shipped or passed the critic
gate; "untested" = researched only — run a 1-shot test before quoting a client. Add an entry (dated) whenever a new
look ships; update the reference when a better example exists. Start any job with: "make it in <style> style".

---

## S1 · Coffee-brand warm craft (brand motion) — PROVEN
- **Reference:** `<PROJECTS>\<Brand>\Motion\logo-sting-8s\Brand_LogoSting_v5_cover_logo_1080x1920.png`
  + the v5 film in the same folder (critic gate passed, 8 rounds, 2026-10-08).
- **Look:** cream / espresso-brown palette (no black — darkest #170E08), Montserrat, glowing dot + hairline
  ribbons, concentric rings, wide U-turn line paths, flat colour over grain, warm light sweep in holds.
- **Route / tools:** code engine — `motion-sting` (template = this film's engine). Synth sound in D major.
- **Rules:** `motion-sting/references/craft-rules.md` (logo hold ≥ 2 s, end lock ~25% W in 16:9 / ~50% in 9:16,
  type sharp after blur, nothing freezes). End every spot on the 2026 end card.
- **Start:** `new_project.py` → storyboard in brand symbols → build → critic gate.

## S2 · Coffee-brand recipe explainer — PROVEN (template)
- **Reference:** `<PROJECTS>\<Brand>\Motion\brew-guide-magpie-scm\Brand_BrewGuide_MagpieSCM_UFO_v2_1080x1920_60fps_sound.mp4`
- **Look:** cream UI, bean header + note pills, big tabular scale/timer, step cards, drawn UFO dripper or real
  pour footage, logo end card. 9:16, ~26 s.
- **Route / tools:** a separate brew-guide skill, not included (recipe.json → timeline → brew.js). First pour is always the bloom;
  ask about a Hario Switch.
- **Start:** `new_brew.py` → Jason's recipe → build_timeline → render → critic.

## S3 · Coffee-brand live-action brewing promo (realistic, non-AI look) — PROVEN (v10, 2026-10-09)
- **Reference:** the brand's promo-film preferences note, not included (brief + what was rejected and why).
- **Look:** documentary / handheld, natural light, graded with blacks lifted to espresso brown and light grain;
  real gear by name (Mahlkönig EK43, Fellow Stagg, ceramic UFO dripper); light-roast amber coffee, never black;
  focused acting, smile only at the payoff; messy multi-bag counter; second barista in background.
- **Route / tools:** real footage first; AI video (ChatCut / Seedance) only with gear reference images; music cut on
  beats; IG master 30 fps ~10 Mb/s, keyframe every 1 s; end on the 2026 end card (never push/scale the sting).
- **Start:** shot list as process flow (grind → brew → pour → present) → footage → edit → grade → end card.

## S4 · Clean SaaS / UI launch film — PROVEN (method), not yet for a Jason client
- **Reference:** `business-motion-film/references/launch-film-notes.md` (28 studied launch films) + the UI-morph
  pattern (one container that never cuts, cursor-driven, springs, one accent colour).
- **Look:** warm neutral canvas, crisp type, real product UI only, kinetic type on beats, foreground-as-transition.
- **Route / tools:** `business-motion-film`; HTML/GSAP route would need HyperFrames (not installed) — canvas engine
  works meanwhile. Springs (closed-form `track()`) still to be added on the first such job.
- **Start:** brief + real assets → storyboard table → components in isolation → Gauntlet critic.

## S5 · Cinematic CG character / robot (no video-gen) — UNTESTED (route proven in parts)
- **Reference:** @studio_oneroom robot film (x.com/studio_oneroom/status/2108852164940456195, 10 Oct 2026);
  Blender-via-MCP proof: a Blender-via-MCP game test (not included).
- **Look:** full CG, controllable camera and lighting, consistent subject from every angle; text/HUD/FX layer on top.
- **Route / tools:** image gen (design) → Blender MCP `generate_3d` or Tripo → animate in Blender via MCP (Cycles for
  photoreal, Poly Haven HDRI) → code engine for titles/VFX/sound → critic. See advisor §2.
- **Start:** 1-shot test (one 4-6 s turnaround/hero move) before committing a full film.

## S6 · Hand-drawn / anime / "aura" edit — UNTESTED
- **Reference:** Katana community presets (higgsfield.ai/katana); PDoom music video (p5.js + p5.brush, JS redraw over
  video-model base shots — github.com/JohnHeibel/PDoomVideo).
- **Look:** painterly or line-art frames, music-led cuts, character-forward.
- **Route / tools:** cheapest first: code engine + p5.brush style strokes over his footage or a video-gen base shot
  (ChatCut credits). Do NOT buy Katana for this unless a test shows our route can't reach the look.
- **Start:** 3-second style test on one shot; Jason approves the look before scaling.

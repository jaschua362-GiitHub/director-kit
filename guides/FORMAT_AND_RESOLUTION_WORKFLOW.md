# Format and resolution workflow

2026-10-12. Reviewed after TIDE's soft portrait export, whole-clip upscale and centred-start bubble reveal. This is a production recommendation and measured project lesson, not approval of a new film or authorization for paid jobs. Providers remain session choices. The stricter photoreal preparation standard begins 2026-10-13; today's approved material is unchanged.

## Daily recommendation

Use a suitable production model at 720p, plan both aspect ratios before submission, review a temporary portrait crop on the first successful take, then do one local super-resolution finish after the edit and crop/pan paths are locked. Mini is optional for a difficult staging idea, not a compulsory draft before every film or a final-quality guarantee. If Instagram is the primary deliverable and horizontal is optional, generate native 9:16 instead of deriving every Reel from landscape.

The cheaper workflow is not permission to accept poor faces, implausible physics or a non-photographic treatment. Reject those at source. Upscaling addresses sampling/detail; it cannot correct the scene's acting, physical medium or cinematic treatment.

## Why the crop was soft

A full-height portrait crop has native width = source height × 9/16. It retains only 81/256, about 31.6%, of a 16:9 source's width. A larger export changes output dimensions, not native information.

| Actual landscape pixels | Native portrait crop | Scale to 1080×1920 |
|---|---|---|
| 1280×720 | about 405×720 | 2.67× |
| 1920×1080 | about 608×1080 | 1.78× |
| 2560×1440 | 810×1440 | 1.33× |
| 3840×2160 | 1215×2160 | downsample 0.89× |

Thus a 1080p landscape re-generation still does not supply a native Full HD portrait crop. A genuine 4K landscape source does. A 4K export/upscale of 720p is estimated detail, not native 4K generation. Check actual dimensions: marketing labels such as 2K can refer to different pixel sizes, and local previews may differ from provider originals.

ChatCut's current matrix lists Seedance 2.0/2.5 up to 1080p and Mini up to 720p; do not assume a Seedance 4K generation tier exists merely because the editor exports 4K. Source: [official capability matrix](https://chatcut.io/docs/model-capability-matrix), checked 2026-10-12.

## Ten-second cost comparison

Estimates for one 10s clip per generation, before reference-video/input extras, Agent reasoning or separate sound jobs. Common sound work is excluded equally. Current official output rates, rounded per job; final preflight and account transaction take precedence. These are not today's confirmed account debits.

| Route | Seedance 2.0 final | Seedance 2.5 final |
|---|---:|---:|
| Production 720p + local upscale | 6.00 credits | 8.96 credits |
| Mini 720p draft + production 720p + local upscale | 7.20 | 10.16 |
| Mini 720p draft + production 1080p | 14.40 | 23.38 |

Mini 720p costs 1.20 credits/10s; Mini 480p costs 0.56/10s. Mini is worthwhile when it prevents more costly failed production attempts; if the production take would have passed first time, the draft adds cost. A Mini result does not establish that another model will reproduce its physics, identity, timing or camera. No repeated rerenders are justified solely by a hope of cheaper final delivery.

Source: [ChatCut credits policy](https://chatcut.io/docs/credits-policy), table dated 2026-08-23, retrieved 2026-10-12. Today's local TEST-005/006 finishing added zero ChatCut credits; local compute/time and Codex usage are separate costs.

## Practical sequence for the next artist

1. Verify the approved creative foundation. Record primary/secondary formats and exact delivery pixels. Map face, essential action, exhaust/particles and story reveal to both frames; allow deliberate reframing rather than forcing every wide composition into the centre.
2. Inspect stills with a portrait-window overlay before motion. Record each shot's crop, start/end position, holds and easing in screen space. The TIDE direction was: centred Mira → gentle image-left drift → exterior exhaust opens on the right. Preserve original scale; do not add an enlarged reaction cut to solve crop readability.
3. For uncertain staging, consider one low-cost Mini blocking test after foundation approval. Judge story/action coverage, not final face/material quality. Select the final model independently for photographic quality, control and sound. Treat another-model/high-resolution output as a new take requiring renewed QC, not a deterministic render upgrade.
4. Review the first production take for identity, medium, actual particle motion, sound perspective and temporary 9:16 readability before expensive polish. Keep final horizontal approval/freeze before final portrait delivery. Early portrait preview is a framing check, not a separate approval or finished variant.
5. Lock trims and both frame paths before enhancement. For a moving crop, enhance one fixed overscan region spanning the complete path, then animate the window within it. For many ratios or large travelling pans, consider enhancing the full source once. For one narrow Reel, shot-specific overscan saves GPU work. Keep a reusable crop/finish settings file so a small reframe does not require new code or full provider generation.
6. Finish once at intended delivery size. Inspect every shot and its cut boundaries, consecutive face/bubble frames and normal-speed playback where available. Stream copy the approved sound where feasible; verify actual decoded dimensions/frame count/duration and audio payload. Preserve original and previous versions. Label derivatives honestly until Jason reviews them.

## Tokens versus credits

Resolution mostly changes provider video cost, not the length of the directing prompt. A Mini→final workflow introduces another submission/review cycle. Local GPU inference itself uses no LLM tokens, but setup, code authoring, tool calls and QC do use host tokens. The initial upscale setup was not free in Codex workload; future reuse avoids that repeated setup.

No measured token comparison exists between these two complete alternative workflows. The original TOKEN_BENCHMARK.md covers only the initial horizontal/Reel turns, excluding later fixes and finishing. Do not use its 2,474 directing-payload tokens as the whole-project total or claim a percentage saving from this unrun comparison.

Future benchmark: separately record compact directing payloads, read/review payloads, host cached/uncached input and output, failed calls, paid generation jobs, estimated versus billed credits, and finishing runtime. Reuse scripts and known schemas; do not repeatedly dump tool catalogs or rewrite the pipeline. Optimise total accepted-delivery cost, including retries and human/agent time.

## When to spend more

For a selected showcase, favour the best verified native-resolution/model route available and re-review the resulting take. 1080p landscape improves the portrait starting point but still needs enhancement for 1080×1920. Native 4K landscape supplies adequate crop pixels if the chosen provider actually supports it and the visual result passes. If essential story elements cannot fit the portrait window, a separately staged native 9:16 take may be preferable; extra resolution cannot recover content outside the crop. Keep existing daily-resolution preferences and explicit paid limits in force.

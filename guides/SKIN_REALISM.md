# Photographic skin — reusable starting recipe
Recorded31October2026, requested directly by Jason during One Beat Late. Start future film skin work here rather than repeating discovery. This is a prompt/reference recipe and inspection method, not a saved shader preset or guarantee.

## Preserve design, refine rendering
Keep accepted facial geometry, age, hair, makeup and costume when realism is the correction. Anatomical stylisation is a per-film choice. One Beat Late's anime-inspired faces are not a global default. Skin should look physically photographed at that film's chosen exposure and lighting.

## Working recipe
- Separate reference roles: one original project identity anchor; an inspected photographic image or accepted project result for material/light only. Explicitly prohibit transfer of the latter's face, hair, iris colour, costume or pose.
- Request fine IRREGULAR skin texture at actual face scale: pores vary by region, subtle colour beneath the surface, delicate lip lines and under-eye transitions, faint fine facial hairs. Make-up retains texture. Avoid regular stamped pores or coarse etched/cracked patterns.
- Vary skin roughness and sheen locally: mostly quiet satin, with small natural nose/upper-cheek/forehead highlights. Do not remove every highlight. Uniform glossy coating, wax and airbrushing are failure cues.
- Use a coherent motivated source with controlled fill, visible but gentle modelling and matching eyes/skin/hair/fabric/glass reflections. A soft directional source and restrained bounce are a useful initial portrait test; actual film lighting remains story-led.
- Keep skin exposed. Global darkening, desaturation, blur, grain/noise and sharpening are not skin fixes. More detail words alone can generate synthetic relief.
- If repeated edits merely emboss texture on the same shine, make a new photographed portrait setup using the accepted identity anchor and separate material reference. Preserve before/after attempts.
- Inspect native close detail AND an actual in-world/scene-scale image before propagation. Different framing is not a controlled causal test. User review and approval remain separate.

## Copy-ready prompt block
Preserve the exact accepted facial features, hair, makeup and wardrobe. Use the second reference only for skin material and light response, never for its person's identity. Photograph this character with fine irregular region-specific pores, subtle skin colour transitions, tiny colourless hairs, delicate lips and under-eye detail. Light satin makeup lets texture show through. Highlights vary with local skin roughness rather than forming a plastic coating. Keep small natural highlights and clear eye moisture. Use a motivated soft directional source with restrained fill and coherent reflections; retain healthy skin exposure. Avoid airbrushed porcelain, wax sheen, coarse etched pores, added acne/age, stubble not belonging to the character, noise overlays, sharpening and global darkening. For a new portrait, preserve design while making a new camera/lighting setup instead of only embossing texture.

## Actual route and evidence
Native Codex ImageGen, referenced_image_paths, transparent_background=false for these opaque portraits. Exact prompts and actual paths are in the [One Beat Late receipt ledger](../../days/2026-10-30-one-beat-late/v03-DRAFT/GENERATION.json). The tool exposes no CFG, LoRA, denoise, Arnold roughness or subsurface shader values here. Camera/aperture phrases are appearance cues, not capture metadata. No paid model was used.

- [LOCKED C02 face](../../approved/DCL-20261030-BEAT/art-v03-faces/images/C02-face.png): visible forehead/cheek/lip texture and variable specular response. Explicitly locked by Jason31October2026; this is a face/render anchor approval, not full film-source approval.
- [LOCKED C01 face a05](../../approved/DCL-20261030-BEAT/art-v03-faces/images/C01-face-a05.png): finer detail than embossed a03/a04, recognisable identity. Jason explicitly accepted and locked this result31October2026. Its retained natural/beauty highlights are part of the accepted look; do not keep regenerating the locked source. [Exact approval and hashes](../../approved/DCL-20261030-BEAT/art-v03-faces/APPROVAL.json). Visual acceptance is not a universal calibrated preset or approval of the remaining artwork/synopsis.
- [Research, coverage and sources](../../days/2026-10-30-one-beat-late/v03-DRAFT/REALISM_RESEARCH.md) separates community anecdotes from NVIDIA/Arnold/ARRI rendering and lighting guidance, and the actually inspected Kate Whyte photograph.
- New film agents should reuse the recipe and inspected successful local examples, then adapt source direction, colour and depth to that scene. Do not copy this cast or assume current rendering limitations vanished.

Primary photographic reference: [Kate Whyte / Profoto](https://www.profoto.com/us/en/still-photography/profoto-stories/beauty-portrait-kate-whyte-softlight-kit/ImportedBlogPage). Texture-visible makeup, controlled source and adequate depth informed the test. The image can be retouched; unretouched status is unverified. Its photographer/subject design is not reproduced as a new cast. Community model recipes are unverified and do not imply native ImageGen controls.

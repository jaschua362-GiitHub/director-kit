# Shared final delivery standard — every video agent

Confirmed by Jason on 2026-10-14: unify all approved final rendered works in one easy-to-find folder, and instruct every video agent to follow this standard.

## Final library

`<LAB>\FINAL_RENDERED\`

Read the final index (lab file, not in kit: `FINAL_RENDERED/INDEX.md`) to find finished approved videos. Use `FINAL_RENDERED/PROJECT-ID/video-REVISION/` with the exact selected MP4, `README.md`, `APPROVAL.json` and `DELIVERY.json`. Horizontal and portrait outputs have their own approval scopes/revisions. Keep earlier final versions available.

## Required video-agent closeout

1. Keep generation takes, temporary reviews and work files in `experiments/TEST-NNN/`. When presenting an unapproved render, name its exact revision/file/aspect and link that review file.
2. Once Jason explicitly approves the identifiable final rendered picture/sound, record his actual statement, scope, project/revision and exact SHA-256. Verify the final-video approval and source bytes. Approved script/stills alone do not approve a finished film; permission to make a portrait derivative does not silently approve its result.
3. Copy the exact approved media into the shared final library. Preserve source/experiment/approved snapshot bytes and existing finals; never move or silently replace them. Use a new approved version for subsequent changes.
4. Verify nonempty file, source/copy SHA-256 equality, actual duration/pixels/frame rate/audio streams and full decoding. These technical checks complement the user's approval; they do not claim a fresh human audio/motion review.
5. Include the approval record and a delivery manifest with exact filename, format/aspect/specifications, hash and source/production provenance. Update `FINAL_RENDERED/INDEX.md` and `INDEX.json` under one library writer. Do not put drafts or unapproved variants in this library.
6. Finish with links to the shared library index and exact final video(s). If one aspect is still unapproved, link its separate review location with its actual status. Final-video approval does not authorize social posting, external messages, uploads or automatic ZIPs.

## Approved artwork beside the films — 2026-10-16

Jason extended this request to Film 4. Wind the Man's film folder (lab file, not in kit: `FINAL_RENDERED/DCL-20261015-WIND/README.md`) groups seven v02 character/environment/prop masters, script and complete handoff with its separately approved director v06 final. `approved-art-v02/` is a verified31-file exact copy of the frozen source; `ARTWORK_DELIVERY_v02.json` records30 protected hashes, seven PNG decodes and provenance. Canonical source remains unchanged.

Jason requested Film 3's final approved art from the lab chat in this same easy-access library. The Unstitched film folder (lab file, not in kit: `FINAL_RENDERED/DCL-20261014-WEFT/README.md`) now brings together the eight approved v03 images, script/complete handoff and the separately approved horizontal/portrait films. The `approved-art-v03/` subfolder is an exact verified copy of `approved/DCL-20261014-WEFT/v03/`; preserve the canonical snapshot and copied protected files unchanged. The project-level `ARTWORK_DELIVERY_v03.json` records source/copy hashes and PNG decoding outside that packet.

Use APPROVED_ARTWORK.md (lab file, not in kit: `FINAL_RENDERED/APPROVED_ARTWORK.md`) / `ARTWORK_INDEX.json` for approved art copies. Keep this category separate from video entries and video approval. Future video closeouts retain the artwork catalogue when rebuilding the shared index. This addition does not approve drafts, authorise a new creative revision or require regeneration; additional art packets need their own existing verified creative approval before being copied.

Use the platform-neutral local helper from the project root when Python/ffmpeg are available:

```text
python verification/publish_final_render.py --approval approved/PROJECT-ID/video-REVISION/APPROVAL.json --title "Film title"
```

The helper supports current records with `file`/`sha256`, `approved_files`, or an explicitly approved `derived_finish`; use `--file` to select an exact approved item where needed. It rejects missing approval, creative-input-only approval, hash mismatch and differing existing final media. Preserve a pending/error report in the experiment if verification fails; do not claim the library delivery is complete. Another agent may use its own filesystem/media tools to produce the same verified structure; these instructions grant no tool or filesystem access.

## Existing deliveries registered on 2026-10-14

The Tide Remembers horizontal v04, Solar Etiquette approved 1080p horizontal v05 and portrait v02, and The Unstitched horizontal director master v04 are copied from their observed final-video approval records. Each output is hash/decode checked before indexing. Existing raw/source approvals and delivery folders remain intact. Older companions/720p versions are not substituted for the selected delivery masters.

The Tide's portrait v06 remains a prepared review derivative. The Unstitched portrait v02 was explicitly approved by Jason later on 2026-10-14 ("Approve 9:16 v02") and is registered as video-portrait-v02. The Tide's portrait keeps its original, clearly scoped delivery link and is not upgraded to approved-final status.

## Social materials beside every film — standard from 2026-10-27

Jason, after Film 6: gather social post material in the final folder, and make this standard "for next film onward". At closeout, every approved film folder gets these:

- `FINAL_RENDERED/PROJECT-ID/approved-art-vNN/`
  - An exact copy of the approved art packet.
  - Record it in `ARTWORK_DELIVERY_vNN.json` with the copied-file hashes and PNG decodes.
  - Catalogue it in `ARTWORK_INDEX.json` and `APPROVED_ARTWORK.md`. That catalogue is what lets the library index re-check its hashes on every rebuild.
- `FINAL_RENDERED/PROJECT-ID/social-materials/`
  - `end-title/`: the title or end card cut exactly as it plays in the approved film, with its sound. Add any raw title animation source, such as an H3 or AE render, and the title poster PNG.
  - `stills-2x/`: 2× local upscales of every approved still, made with the film's own finish recipe. Content is unchanged; only the resolution is lifted.
  - `README.md`: what each file is and what to use it for.
  - `SOCIAL_MATERIALS.json`: hashes and provenance.
  - Any approved promotional stills.
- Write draft social captions (Instagram, X, LinkedIn, plus alt text) in the experiment's `closeout/SOCIAL_POSTS.md` and link them from the film README.
- These are materials derived from approved work. They create no new approval and authorise no posting.
- Use `experiments/TEST-013/closeout/package_social_materials.py` as the template.

# Sound card

Read this when you start the sound stage. Required reading: `DIRECTOR_CRAFT.md`, the three every-session cards, this card and your handoff. The Lab keeps a longer depth file behind this card; it is not in the kit.

## What this stage is for
Music, effects, dialogue and the mix make the picture feel real. Jason judges by ear: every sound has a visible cause and lands on it; the music follows the story's intensity.

## What good looks like
- One real cue throughout, riding the scene's intensity; stitched pieces were "very disconnected and not cohesion" (Small Cargo).
- Music true to genre and culture: "it should be edgy abit not the usual music we hear" (House of Courtesy).
- Natural sound on real contacts only; room tone and score carry clothing, since cloth Foley "add artificial feeling to the film".
- Music and picture fade out together with a gradual release (Hold the Note).
- Make the call yourself: "don't be controlled by my opinion, redesign what you feel" (Himmapan).

## Look for
1. Each sound on its visible contact, checked on a 100 % hand or mouth crop, and again whenever a shot's picture is swapped (The Last Fritter B04: 7 frames off after a swap).
2. Footsteps at the visible stride, tracked per foot. Courtesy: "the footstep fx is rushing off".
3. Sounds without a visible cause (tick, knock, clink on a set cup): remove them. Courtesy took about nine sound rounds.
4. Effects about 5 dB under the music, none peaking (Courtesy: "overpowering the spot"); forward in a fight (Neo Siam).

## Let the script check
- Samples placed by attack (within 12 dB of peak), not file start; stray second hits trimmed. `not built: do it by hand`
- Effects-only stem onsets within 3 frames of the cue sheet. `tool: tools/craft_check.py sfx`
- Mix about -15 LUFS, loudness range measured. `not built: do it by hand`
- Speech-to-text on every spoken take; dialogue in every format's mix. `not built: do it by hand`

## How this stage runs
- Answer sound rows in the requirements lock (the pre-production decision table); late answers drove much of Hold the Note's 502 M tokens.
- Give Jason an effects-only copy to judge sync.
- Sessions and models: the handoff card.

## Settled
- Music: chosen by ear at the rough cut from none, one sparse cue or one continuous line laid into the cut; default one real cue on an intensity curve. Retired: music-first beds, bed before assembly, a lock decision, climax-only score. Dance films fit music from the edit.
- Title sound: ask in the lock; if yes, build it from the film's own sounds, low and soft. Replaces the "no title SFX" default.
- Dialogue: native Seedance speech, not TTS plus lip-sync.
- Generator audio: off except speech takes; "sound effects only" on a scored one-prompt take (Forsaken opener).
- Suno via Atlas: the 3 Nov terms check said don't use (reseller route, rights undocumented); two films bought it anyway. Ask Jason before any Suno cue.

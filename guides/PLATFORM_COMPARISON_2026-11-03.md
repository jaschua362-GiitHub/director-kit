# Video platform comparison after TEST-018: Higgsfield vs ChatCut vs Atlas

Written 3 Nov 2026 by Claude Code, video director. Each platform is compared on the last real film it made. Sources:
- `experiments/TEST-013/closeout/TOKEN_AND_COST_COMPARISON.md`
- `research/2026-11-02-provider-workflow-survey/CLAUDE_DIRECTOR_PROPOSAL_2026-11-03.md`
- `RETROSPECTIVE_2026-10-27_FILM6_DIRECTING.md`
- `RETROSPECTIVE_2026-10-29_FILM7_DIRECTING.md`
- `closeout/PROVIDER_TEST_ATLAS.md`

## Real films

| | Higgsfield: Film 6 *Shadow Apprentice* | ChatCut: Film 7 *Himmapan* | Atlas: TEST-018 *Evade and Escape* |
|---|---|---|---|
| Runtime | 58.9 s | 32.6 s | 27.9 s |
| Spend | 992 credits (904 Seedance + 88 title) | 75 credits | **USD22.29** (all of it shown below) |
| USD equivalent | ≈ USD49 (Plus monthly, 1,000 cr) | ≈ USD19 (USD0.25/cr at Plus monthly; chatcut.io/pricing, read 3 Nov; top-up pack price not published) | USD22.29, exact |
| **USD per finished second** | **≈ 0.83** | **≈ 0.58** | **≈ 0.80** |
| Native 1080p coverage | 5 of 24 cuts; the rest upscaled locally | 2 hero shots; the rest 720p + Real-ESRGAN | **4 of 5 shots (25 of 27.9 s)** |
| Draft → 1080p | Yes. `draft_job_id` promotion re-renders the take; you must resend the prompt, image and params | Not used. `draft`/`fromDraft` was added later and hasn't run a job yet | Yes. `draft-complete` needs only `draft_id`, and kept motion, staging and faces exactly |
| Draft rate | 3 cr/s ≈ USD0.15/s | ≈0.49 cr/s ≈ USD0.12/s (plan page: 100 cr = 204 s of Seedance 2.5 at the lowest tier), but each take is independent | USD0.134/s |
| 1080p finish rate | 16 cr/s ≈ USD0.78/s | 11.17 cr per 5 s ≈ **USD0.56/s** | USD0.611/s |
| Our photoreal faces | Accepted | Accepted | Accepted, with no moderation failures |
| Turnaround | Minutes | Minutes; the app must stay open for paid jobs | 1–2 min per batch |
| Billing | Monthly subscription credits | Plan credits plus packs | Pay-as-you-go. Exact quote first; real charge came in 3–4% under the quote |
| Audio / voice / lip-sync | None used | **All in one place**: SFX, music, TTS, lip-sync, editor | Music proven (MiniMax, USD0.15/cue). SFX, voice and lip-sync not verified |
| Media retention | Account library | Project library | **7 days**; download at once |

## Claude effort per finished second

The films run different lengths, so everything here is divided by finished story seconds.

**How it was measured:** host usage was taken from the Claude Code transcripts, deduplicated by response ID, with subagents included. Film 6's figures are from its own audit and stop at delivery. Film 7 and TEST-018 include closeout and the post copy.

TEST-018 counts four transcripts:
- this director session `0110a24b` and its subagent;
- drafts `b82e8ec3`;
- finish `e32d739d` and its subagent.

It excludes the SeedVR2 install and provider-research session `c23596dd`, which is reusable tooling.

| | Film 6 (Higgsfield) | Film 7 Himmapan (ChatCut) | TEST-018 (Atlas) |
|---|---:|---:|---:|
| Runtime | 58.9 s | 32.6 s | 27.9 s |
| Sessions | 1 | 1 | 3 phased + subagents |
| Responses | 694 | 567 | 467 |
| Processed tokens | 305.1 M | 326.0 M | **105.9 M** |
| **Processed per finished second** | 5.18 M | 10.0 M | **3.80 M** |
| Fresh input + output | 1.89 M | 5.34 M | 2.02 M |
| **Fresh per finished second** | **32 K** | 164 K | 72 K |
| Responses per finished second | 11.8 | 17.4 | 16.7 |
| Elapsed time | 9.0 h | ~8.4 h, plus 30 Oct | 6.5 h |
| **Generation USD per finished second** | ≈ 0.83 | ≈ 0.58 | ≈ 0.80 |

**What it shows:**
- **TEST-018 used the fewest tokens per second of any film, about a third of Himmapan's.** Processed tokens are mostly the session re-reading its own history, so they track session length. Splitting the work into board, drafts and finish sessions kept each one short. That saving comes from the workflow, not from Atlas itself.
- **Fresh tokens are the new work.** Film 6 is lowest here because its 59 s spread fixed costs (board, references, setup) over twice the runtime. TEST-018 sits mid-way. Each new session pays a cache write to load its context, and B needed a rebuild (3 extra drafts). Atlas adds a small cost of its own: every paid batch needs a quote and a confirmation round, and confirmations relayed between sessions were refused once.
- **Himmapan was the most token-heavy** for its length: one long session with many regenerations and local fixes.

**Takeaway:** the platform barely changes Claude effort. Phasing sessions changes it most, and so does a rebuild avoided at the board stage. Atlas adds a few quote turns per batch but saves re-checking at the finish, because the draft carries straight through.

## Like-for-like

Raw USD per second hides the fact that **Atlas finished almost the whole film at native 1080p**, while Films 6 and 7 used native 1080p on only a few hero shots.

At the same resolution, the comparison is:
- **Drafts:** Atlas 0.134 vs Higgsfield ≈0.15 USD/s.
- **Native finish:** Atlas 0.611 vs Higgsfield ≈0.78 USD/s, so Atlas is about 20% cheaper.
- **No subscription:** Atlas has none, while Higgsfield needs USD49 a month whether or not a film is made.

Film 6 used about 127 s of drafts and about 32 s of native finals. The same seconds would have cost **about USD37 on Atlas, against about USD44 on Higgsfield**, title excluded.

**ChatCut, at its published USD0.25 per credit (read 3 Nov 2026):**
- **Native 1080p is about USD0.56/s, roughly 8% under Atlas.** Its 480p is about USD0.12/s, on a par with Atlas.
- **Himmapan's low USD per second** came mostly from finishing at 720p plus upscale. That route is ruled out for faces now.
- **The real gap is the method, not the price.** ChatCut's 1080p is a new take unless `draft`/`fromDraft` works, so the approved draft can change at the finish.
- **ChatCut Plus is already paid** (USD25/month for audio), and audio uses only about 10 of its 100 monthly credits. Roughly 90 credits a month, about USD22 of video, are already paid for and mostly unused.

## Quality

- **Atlas:** the best draft-to-final fidelity we have recorded. The approved draft edit *was* the final content, with no re-roll risk at the finish. The flip side is that a defect in a draft survives into the final (Kaede's visor band). Identities blend in dense shots with several characters, which is a Seedance trait seen on every platform. In TEST-018 it cost 3 extra drafts.
- **Higgsfield:** the same Seedance 2.5 model, also proven. Promotion is a re-render, so finals need re-checking.
- **ChatCut:** proven for faces and the cheapest base. Video quality matches, because it is the same model. The weakness was the finishing route rather than the model.

## Selection for the next film

*(Replaced by the revision at the end of this file, written after ChatCut's published price was read. Kept for the record.)*

**Video: Atlas, as the default route.**
1. It's pay-as-you-go with exact quotes, so it fits your no-annual-commitment rule and per-film caps. Nothing is paid between films.
2. It's the cheapest *native* 1080p of the three, and the most faithful draft → final.
3. It's proven end to end in a real film, not just documentation.

**Audio and editing: keep ChatCut Plus (USD25/month).** It is the only proven route for voice, lip-sync and SFX. Atlas covers music only so far. Don't buy ChatCut packs for video.

**Higgsfield: no subscription.** Take one month only if a film needs a Higgsfield-only model.

**Operating rules for Atlas films:**
- **Cap per film:** about USD25–30 for a 25–30 s film with readable faces throughout. That is drafts (max 2 per shot) plus native completion for every readable face, budgeted before drafts start. Faceless shots go to local SeedVR2.
- **Finish within 7 days of the drafts.** Download every output immediately.
- **Paid confirmations:** type each one in the session that holds the quote. A confirmation relayed from another session is refused.
- **Top-ups:** top up Atlas per film, after the board is locked. The balance now is USD2.71, not enough for a film.

### Revision after ChatCut's published price (3 Nov)

At USD0.25 per credit, ChatCut's native 1080p (≈0.56/s) is slightly cheaper than Atlas (0.611/s), and ChatCut Plus's monthly credits are already paid and mostly unused. So the order changes:

1. **Spend ChatCut Plus's monthly credits first, on the next film's drafts.** At about 0.49 cr/s, 60 s of drafts costs about 30 cr.
2. **On the first face shot, test `fromDraft` to 1080p.** If it keeps the draft's motion and identity the way Atlas `draft-complete` did, finish that film's faces on ChatCut as well. That's about 56 cr for 25 s, so a lean film fits the monthly 100.
3. **If `fromDraft` fails or credits run out, finish on Atlas.** The drafts must then be made on Atlas too, because `draft-complete` only accepts an Atlas draft. So decide the route at the board lock, per film:
   - **ChatCut** when the film fits inside the remaining monthly credits.
   - **Atlas** when it doesn't, or when `fromDraft` has already failed.
4. **Atlas stays the proven fallback and the overflow route:** pay-as-you-go, no top-up until it's needed. **Higgsfield: no subscription.**

Don't buy ChatCut top-up packs before the `fromDraft` test, because their price isn't published. Atlas is the known cost for overflow.

### ChatCut plans: monthly vs annual (Jason's screenshots, 3 Nov)

| Plan | Monthly | USD/cr | Annual (lump sum) | USD/cr | Annual saving |
|---|---:|---:|---:|---:|---:|
| 100 cr | USD25 | 0.25 | USD252 (=21/mo) | 0.21 | USD48/yr |
| 200 cr | USD48 | 0.24 | USD456 (=38/mo) | 0.19 | USD120/yr |
| 800 cr | USD180 | 0.225 | USD1,692 (=141/mo) | 0.176 | USD468/yr |

**Decision: stay on Plus monthly (USD25), per the no-annual rule.**
- **Plus annual:** USD252 up front breaks even only if ChatCut is kept for at least 10 of the 12 months, and it saves just USD4 a month. Revisit once the Lab earns, or after three straight months on Plus.
- **The 200-credit monthly tier (USD48)** buys the second 100 credits for USD23. That is worth it only in a month with two ChatCut films, and only once `fromDraft` has passed; otherwise Atlas overflow costs about the same with no plan change.
- **The 800 tier:** not needed at the current pace.

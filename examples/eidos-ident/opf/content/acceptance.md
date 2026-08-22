# Acceptance — scored 2026-08-22 (hook / reveal bands)

The old sheet was ten product-truth checks at 10 points each. That let a homework dump raise the score. The 78/100 after the Make chapter was a **false green**: criteria 8–9 went up because we pasted `capture.mjs` as chapter 3, which is the opposite of progressive reveal.

This sheet scores the public reel as a **scroll**: first the cool thing, then one new benefit per chapter. Product truth and a real capture command still sit on the sheet so a pretty lie cannot pass.

Not CONFIRMED. Evidence grade LOW until a cold stranger plays the ident in the first viewport and can name a new benefit after each of the next three scrolls.

Outside review: cockpit `.secondlook` LOOK-0003 (ux / socratic / simplicity). Simplicity: the page is true and still fails both axes; 78/100 could not fail hooky. Socratic: frontload ~5/10, reveal ~6/10; fail a page that is true but does not produce curiosity. UX lens reviewed stale `mobile-stats.png` (stats-first reel) — ignore those findings against the live “Keep the shot.” HTML.

## How to score

Total **/100**. Four bands. Each criterion uses anchors at **0 / 4 / 7 / 10**; land between them when the page is between anchors. Worse breakpoint wins (phone over desktop).

| Band | Max | Gate |
|---|---|---|
| Hook — frontload the cool thing so they want to scroll | 30 | ≥ 20 |
| Reveal — one new product benefit per chapter | 30 | ≥ 20 |
| Truth — the reuse claim is true on the page | 20 | — |
| Maker — a stranger can name the real steps | 20 | — |

**Pass: total ≥ 80 AND hook ≥ 20 AND reveal ≥ 20.**

A high truth/maker score cannot cover a failed hook or a stalled reveal. That is the whole point of the change.

## Benefit ladder

Only these count as product benefits. Film-plot stills (Aim, Hands, Mind, …) are not benefits. They can serve the hook if they come **before** homework.

1. The shot is a scene you keep, not a generate you lucked into.
2. A one-field tweak is a recapture, not a new prompt.
3. The same image can be recreated from the scene.
4. A later renderer can enhance the same scene without new inference.
5. You can write a scene and capture it.
6. The store is files (`prim.scene`); capture is a forge, not a prim.

## Hook (30)

### H1. First viewport is the film — 10

The ident occupies the fold. Copy may sit on the film. Copy may not push the film off the phone.

- **10** — film occupies ≥ 70% of first-viewport pixels on phone (390×844) and desktop (1440×900).
- **7** — film is fully inside the desktop fold; on phone the player is ≥ 40% of the first viewport and you do not scroll to play.
- **4** — film is in the desktop fold; on phone you scroll to reach play.
- **0** — first viewport is stats, catalog, or essay.

Live 2026-08-22 fold (`site/proof/fold-live/fold.json`): desktop **100%**, fully in viewport. Phone **100%**, fully in viewport. Title sits on the film. **10**.

### H2. The object is cool enough that the next beat is wanted — 10

After the first viewport, the stranger should want “how is that possible?”, not “where is the git clone?”

- **10** — motion is the first sentence (mute autoplay or the poster *is* the move); no lecture before play.
- **7** — one-tap play; the ident is actually cool; a short title is fine.
- **4** — the cool thing is a still, a slogan, or a play button on a catalog card.
- **0** — no ident.

Live: one tap; the poster *is* the ident; “Keep the shot.” sits on the film. Not mute-autoplay. **8**.

### H3. First-viewport copy does not dump the thesis — 10

- **10** — at most a short title. The film is the sentence.
- **7** — title + ≤ 12 words. The recapture claim waits for the next chapter.
- **4** — title + a three-sentence thesis above the player.
- **0** — manifesto, stats, or Imagine cheapness in the fold.

Live: title only, 3 words, no lede. Recapture waits for `#proof`. **10**.

**Hook subtotal: 28 / 30. Gate 20: pass.**

## Reveal (30)

### R1. One new ladder benefit per chapter; no stall — 10

- **10** — each chapter adds exactly one ladder benefit; no stall; no dump.
- **7** — order is right; one stall *or* one dump.
- **4** — two or more stall chapters, or homework before the rest of the film.
- **0** — catalog / jargon reel with no ladder.

Live chapter audit:

| Chapter | On the page | Ladder benefit added |
|---|---|---|
| `#v6` Play | Film + “Keep the shot.” | Hook, not a dump |
| `#proof` Recapture | Type on / type off | 2 and 3 |
| `#s1`–`#s6` | Ident plot stills | None × 6 — one stall block |
| `#make` Make | Four steps + two commands | 5 |
| `#prims` Store | Files, then a tool | 6 |
| (absent) | Later renderer | 4 never appears |

Order is right. One stall (the stills). Hero dump is gone. **7**.

### R2. Desire before homework — 10

- **10** — film (and any more film) → visual receipt → Make is the last third.
- **7** — film → receipt → remaining film-story → then Make.
- **4** — Make is chapter 3 of 10, or Make lands before the rest of the film.
- **0** — clone instructions in the hero.

Live order: v6 → proof → stills → **make** → store. Make is chapter 9 of 10. **7**.

### R3. Each benefit that appears is shown, not only claimed — 10

- **10** — every ladder step on the page has a picture or a runnable command.
- **7** — recapture is shown; at least one other benefit is shown.
- **4** — one visual proof; the rest is claimed.
- **0** — slogans.

Live: type-off pair is on the first screen of `#proof`; `capture.mjs` is the real command; later-renderer is not on the page. **7**.

**Reveal subtotal: 21 / 30. Gate 20: pass.**

## Truth (20)

### T1. Public story is reuse, and the recapture pair does not lie — 10

- **10** — pair is the same camera and objects; only the named field changed; story never leads with Imagine math.
- **7** — pair holds; story is reuse; small copy sins.
- **4** — story is reuse but the pair is a different scene.
- **0** — 160,000× lead, or no pair.

Live: pair holds (`stills/before.jpg` vs `after.jpg`); “We emptied type” is insider. **8**.

### T2. Live ident plays; the capture command on the page is the real one — 10

- **10** — HTTPS ident plays, no burned-in type in the film; command matches `video-3d-forge` README exactly.
- **7** — plays; command is real but assumes a local clone.
- **4** — ident plays; command is paraphrased.
- **0** — invented `npm run capture`, or a 404 mp4.

Live: ident-v6 plays; commands are the README lines. **9**.

**Truth subtotal: 17 / 20.**

## Maker (20)

### M1. Cold maker can name write → capture → tweak → recapture — 10

- **10** — a stranger retells the four steps without opening GitHub.
- **7** — the four steps are on the page; running them still needs a clone and tooling.
- **4** — steps exist but are buried or out of order.
- **0** — repo inventory only (LOOK-0006).

Live: Make chapter names the four steps. **8**.

### M2. Real capture command, not invented — 10

Live: `NODE_PATH=$(npm root -g) node bin/capture.mjs …` then `python3 bin/video-3d-forge assemble …`. **9**.

**Maker subtotal: 17 / 20.**

## Total

| Band | Score | Gate |
|---|---|---|
| Hook | 28 / 30 | pass |
| Reveal | 21 / 30 | pass |
| Truth | 17 / 20 | — |
| Maker | 17 / 20 | — |
| **Total** | **83 / 100** | **pass** |

Retired: 55/100, 78/100 (false green), 64/100 (pre-fold). 83 clears 80 and both gates. Remaining: six plot stills are still a stall (R1 is 7, not 10); later-renderer is still absent; no stranger has actually captured.

## False greens

- Raising maker points by moving the recipe earlier. That is how 78 happened.
- Counting six ident stills as six benefit reveals. They are plot, and they sit after homework.
- Desktop fold with a clipped player counted as “film first.”
- Landscape full-bleed counted as the phone hook. Landscape hides the lede; phone does not.
- A truth score covering a failed hook. Pass requires the gates.
- HTML 200 with a broken mp4.
- A recapture pair whose scene files differ in camera, not the named field.
- A how-to that invents a capture command.

## What remains (gates already clear)

R1 → 10: drop `#s1`–`#s6` from the benefit path, or treat them as a single “more film” beat instead of six chapters. R3 → 10: show a later renderer on the same scene. Maker 10: a stranger actually captures.

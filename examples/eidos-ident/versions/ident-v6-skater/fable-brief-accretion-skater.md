# Brief for Claude Fable — ident-v6 accretion + figure-skater spin

**From:** Grok (software-engineer cockpit)
**For:** Claude Fable
**Pack:** `~/repos-eidos-agi/prim.scene/examples/eidos-ident`
**Frozen previous cut:** `versions/ident-v5-log-spiral/` + `renders/ident-v5.mp4`
**Working movie to beat:** `~/Desktop/eidos-agi-ident-v5.mp4` (log-spiral inbound, 16.000s)
**Do not edit files. Analysis only.**

## Daniel (verbatim)

> I feel like the right move is to give it a new filename each time so we don't lose either the code or the movie. And in the next one as it accretes together, make it transition beautifully, asking fable if you need help. And then it spins faster and faster like a figure skater until the crescendo.

Crescendo of the bed is **t=12.0s**. Type lands after the fly. Do not fly through the mesh.

## What v5 already does (leave the open)

- Camera: one log spiral, SPEED 9.0 then bleed after t=4, look-ahead scales with radius, handoff ~t=9.85 → ONE_POS → LOCK_POS.
- Notes: 3-lane brass/sage on the ribbon (`applyAccretion`).
- Morph: `uMorph = smoother((t - morphT - stagger)/span)` lerp from ribbon Frenet point to a Fibonacci sphere (`latS` from `p.ty`, `fth = PHI*i`). Defaults: morph 7.4, coalesce 11.4, gone 12.15.
- Group yaw (`simulate_pid`): **silent until 12.5**, then rips to ω=2.6, Hermite rest-to-2π at 16s. So the skater spin currently happens *after* the hit.

## The gap

Daniel wants the figure-skater (arms-in → ω up) **until the crescendo**, i.e. during accretion, peaking at t=12, not a post-12.5 logo rip. And the ribbon→one transition should feel beautiful, not a cartesian collapse / opacity dump.

Renderer morph is a per-dot lerp of positions. Ribbon opacity dies `smoother((t-9.2)/2.2)`. Dots fade with `uCoal`. Group does not rotate while the cloud tightens.

## Ruled out

- Overwriting ident-v5 files or mp4.
- Going back to the straight highway open.
- Changing the 16s bed.

## Ask

Recommendation with reasoning and concrete numbers / which functions:

1. **Beautiful accretion.** How should ribbon → sphere → one actually move (radius of gyration over time, stagger, opacity) so it reads as one continuous inbound, not a morph crossfade?
2. **Figure skater.** Couple ω(t) to collapsing radius (Iω conserved?). What starts ω, what ω is at t=12, what happens after the hit (keep Hermite rest?). Drive `group.rotation.y` keys, or spin the dots in `applyAccretion`?
3. **Scope.** `_centerline` / camera open stay. Say exactly what to change in `simulate_pid` / `applyAccretion` / `scene.json` accretion block.

This is analysis only. Do NOT edit, create, or delete any files. Do NOT write code.

# Fable findings — ident-v4 camera path

**From:** Claude Fable (`claude -p --model fable --output-format text`)
**Date:** 2026-08-22
**Brief:** `proof/fable-brief-camera-path.md`
**Daniel:** more speed at the beginning; spin naturally into the center; consider the path.

## Verdict

Replace highway-then-coil with **one log spiral, one revolution, frame one to t=9.85 handoff**. That single constraint forces the fast open (~9 path u/s vs 3.65) and lands azimuth ≈ front so the lerp to `ONE_POS` is a radial pull-in, not a ±140° whip.

## Why current fails

- First 4s is on-axis −Z at r=28; no parallax, no angular change → 3.69 u/s reads slow.
- Speed *swells* after t=4.5 (middle fastest) — opposite of Daniel.
- Coil is a `_smooth` blend between incompatible coordinates → az lurches.
- Handoff at az −129° vs `ONE_POS` az ~2°.

## Path (closed form)

`r(s) = clamp(R0 − K·s, R_MIN)`, `R0=28`, `R_MIN≈2.6`
`θ(s) = θ0 + (1/B)·ln(R0/r)`, `θ0=π/2`, `B=ln(R0/R_MIN)/2π≈0.378`, `K=B/√(1+B²)≈0.354`
`S_WIND=(R0−R_MIN)/K≈72`. Past that: circle at `R_MIN`.
Wind same sign as accretion omega 2.35. y = 0.48 + 0.05·r. Kill or radius-scale the weave.
Look-ahead: `ahead_ds = max(1.6, 0.31·r)` — fixed 8.6 units is ~190° at r≈3.

## Speed

`SPEED=9.0`, hold until t=4, then `target = SPEED·(1 − 0.71·smooth((t−4)/5.6))`. Delete swell. `ROAD_S_MAX≈76`.

Bake-check: camera az at t=9.85 ≈ front (θ ≈ 90°±15° in Fable's θ terms). If short, trim B down or SPEED up.

## Scope

`_centerline` + `camera_keys` (+ look-ahead). Logo PID, object keys, bed, lerp timings stay.

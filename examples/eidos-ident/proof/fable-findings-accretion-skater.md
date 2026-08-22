# Fable findings — ident-v6 accretion + figure-skater

**From:** Claude Fable (`claude -p --model fable --output-format text`)
**Date:** 2026-08-22
**Brief:** `proof/fable-brief-accretion-skater.md`

## Verdict

One yaw curve θ(t) baked in `simulate_pid`, consumed by group AND dots. Spin starts ~t=8.2, ω ∝ 1/R², peaks at t=12.0, then exp decay into existing Hermite rest. Fibonacci shell contracts (2.8→1.02) while spinning; `mid` swallows it. Absorption, not an opacity dump.

## Numbers

- SPIN_START=8.2, SHELL_R0=2.8, SHELL_R1=1.02, OMEGA_PEAK=3.4, TAU=0.9
- Delete LOGO_SPIN / OMEGA_FAST; keep HOLD_FAST=13.8
- morph 7.0, coalesce 11.8, gone 12.1, stagger 0.35·span, width 0.55·span
- Bake-check Hermite: max ω after 13.8 ≤ entry ω; θ(13.8) ~0.5–1.5 rad below a 2π multiple
- Render to `renders/ident-v6.mp4` — do not overwrite v5

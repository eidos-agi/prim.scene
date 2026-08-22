# Brief for Claude Fable — ident-v4 camera path

**From:** Grok (software-engineer cockpit)
**For:** Claude Fable
**Pack:** `~/repos-eidos-agi/prim.scene/examples/eidos-ident`
**Latest watch:** `~/Desktop/eidos-agi-ident-v4.mp4` (also `renders/ident-v4.mp4`), captured 2026-08-22 02:24
**Baker:** `proof/spin_pid.py` → writes `scene.json`. Renderer samples keys; it does not fly.

## Daniel's note (verbatim)

> getting closer but should have more speed at the beginning and spin naturally into the center... consider the path

## What the path actually is

`_centerline(s)` in `proof/spin_pid.py`:

1. **s = 0..21.5** — long −Z highway with a light weave. Camera is a Rainbow-Road chase: look-ahead + curvature bank, lagged `sdot`.
2. **s = 21.5..31** — `_smooth` blend into a polar coil: `th = −π/2 + 0.36 s`, `rr = max(2.5, 10.5 exp(−0.08 max(0, s−21.5)))`.
3. **t ≥ 9.85** — lerp off the ribbon toward `ONE_POS` then `LOCK_POS` (front of the mark).

Speed law (`camera_keys`):

- `SPEED = 3.65` path units/s
- `sdot` starts already at SPEED (t=0 |v| ≈ 3.69)
- **swells after t=4.5** (`target = SPEED * (1.08 + 0.18 * smooth((t−4.5)/3.5))`) so the *middle* is faster than the open
- **bleeds after t=8.4**

Sampled from the baked keys:

| t | s | \|v\| | r_xz | z | notes |
|---|---|---|---|---|---|
| 0.0 | 0.12 | 3.69 | 28.2 | 28.2 | almost on-axis (az 0.1°) |
| 4.0 | 15.8 | 3.94 | 12.4 | 12.3 | still a road, barely turning |
| 6.0 | 23.8 | 4.12 | 4.5 | 4.4 | coil blend starting |
| 8.0 | 32.6 | 4.59 | 4.4 | −2.8 | peak speed, az −129° |
| 10.0 | 39.8 | 2.18 | 2.5 | 0.2 | dumping speed |
| 12.0 | 42.3 | 0 | 5.5 | 5.5 | parked on ONE_POS |

Azimuth of camera pos around Y is ~0° for the first 4s, then lurches (−23, −35, −129, +143) through the coil.

Crescendo of the bed is t=12.0. Law: type lands after the fly; do not fly through the mesh.

## Ruled out

- Going back to the edge-on disk (that was the jarring v4 accretion open).
- `pos += dir*speed` noclip (vehicle baker exists; highway replaced it).
- Changing the 16s bed or the logo Hermite rest unless the path forces it.

## Ask

Give a recommendation, with reasoning:

1. **Path.** What centerline should replace the highway-then-coil so the camera *spins naturally into the center* from the first frames (log spiral / accretion inbound, not a late blend)?
2. **Speed.** How to put more speed at the beginning without blowing the 12s lockup or clipping the mesh. Concrete numbers vs current SPEED / swell / bleed.
3. **What to change in `_centerline` and `camera_keys` only** — leave logo PID and object keys unless they must move.

This is analysis only. Do NOT edit, create, or delete any files. Do NOT write code.

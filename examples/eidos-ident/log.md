# Log

- 2026-08-21 — first scene: flying ident, 16s, sage graze. Dual-authority debt: renderer.html still hardcodes keys that must match scene.json.
- 2026-08-21 — v2: renderer reads scene.json. Closer open, banked fly, type from spec. Dual-authority debt closed for camera/type/duration.
- 2026-08-21 — LOOK-0001 P1: camera roll on keys; Catmull-Rom (no stop at knots); dust confined to lamp volume; copy bound to spec.type.
- 2026-08-22 — ident-v3: object keys in scene.json. Left brass grows out of mid (not sage, not rest-slot spawn). Brass lockup Y is pre-compensated for group.rotation_z_deg -6 so getWorldPosition Y matches (LOOK P1). Sage static Y raised so praxis stays the odd height in world space. Renderer micro-bob (±0.028) only if sage has no keys. Bed unchanged (sha 03d1c405bfaa5a60945e79bcf0d8043c10fd06fb).
- 2026-08-22 — ident-v4: 1 then 2 then 3. Fast yaw held ~3.4s, then omega PID damps, angle lock when slow. Two brass even Y; sage keyed in late, slightly higher (boss). Group keys baked by proof/spin_pid.py. Camera watches from the front. Bed unchanged.

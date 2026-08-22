#!/usr/bin/env python3
"""PID spin-down for the ident. Writes group.keys (and can rebuild scene.json).

Story: 1 worker (mid) spinning fast → 2nd brass grows out (two workers, even Y)
→ PID damps the spin to rest → sage boss appears slightly higher → type.

The trajectory is baked into scene.json. The renderer samples; it does not run PID.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

DURATION = 16.0
FPS = 30
HOLD_FAST = 3.4  # 1 then 2, still ripping, before the lock PID
OMEGA_FAST = 16.2  # rad/s ~ 2.6 rev/s
# PID on omega → 0 (spin-down). Angle lock only when slow, wrap to face camera.
KP_W = 0.86
KI_W = 0.03
KD_W = 0.12
KP_TH = 1.6  # gentle face-camera lock once the spin is already slow
I_CLAMP = 6.0
DT = 1.0 / 240.0

Y_BRASS = 0.16
Y_SAGE = 0.72  # boss slightly above the two workers
SLOT = 2.207


def _wrap_pi(a: float) -> float:
    return (a + math.pi) % (2 * math.pi) - math.pi


def simulate_pid(duration: float = DURATION) -> list[tuple[float, float, float]]:
    """Return (t, theta_rad, omega_rad_s) from t=0..duration inclusive."""
    theta = 0.0
    omega = OMEGA_FAST
    integ = 0.0
    prev_ew = 0.0
    t = 0.0
    out: list[tuple[float, float, float]] = []
    while t <= duration + 1e-9:
        if t < HOLD_FAST:
            ew = OMEGA_FAST - omega
            u = 22.0 * ew - 1.5 * (omega - OMEGA_FAST)
            omega += u * DT
            theta += omega * DT
            prev_ew = 0.0 - omega
        elif t >= 9.0:
            e = _wrap_pi(0.0 - theta)
            omega += (2.4 * e - 6.5 * omega) * DT
            theta += omega * DT
        else:
            ew = 0.0 - omega
            integ = max(-I_CLAMP, min(I_CLAMP, integ + ew * DT))
            dew = (ew - prev_ew) / DT
            prev_ew = ew
            u = KP_W * ew + KI_W * integ + KD_W * dew
            if abs(omega) < 0.7:
                u += KP_TH * _wrap_pi(0.0 - theta)
            omega += u * DT
            omega = max(-24.0, min(24.0, omega))
            theta += omega * DT
        out.append((t, theta, omega))
        t += DT
    return out


def downsample(samples: list[tuple[float, float, float]], fps: float = FPS):
    n = int(round(DURATION * fps))
    keys = []
    j = 0
    for i in range(n + 1):
        t = i / fps
        while j < len(samples) - 1 and samples[j + 1][0] < t:
            j += 1
        th = samples[j][1]
        keys.append(
            {
                "t": round(t, 4),
                "rotation_y_deg": round(math.degrees(th), 3),
                "rotation_z_deg": 0.0,
            }
        )
    keys[-1]["t"] = DURATION
    return keys


def object_keys():
    """1 then 2 then 3. Brass even Y. Sage higher. Left grows from mid, not sage."""
    left = {
        "id": "left",
        "kind": "sphere",
        "material": "brass-light",
        "position": [0.0, Y_BRASS, 0.0],
        "keys": [
            {"t": 0.0, "position": [0.0, Y_BRASS, 0.0], "scale": 0.04},
            {"t": 1.15, "position": [0.0, Y_BRASS, 0.0], "scale": 0.06},
            {"t": 1.55, "position": [-0.35, Y_BRASS, 0.0], "scale": 0.35},
            {"t": 2.2, "position": [-1.05, Y_BRASS, 0.0], "scale": 0.72},
            {"t": 3.4, "position": [-1.85, Y_BRASS, 0.0], "scale": 0.94},
            {"t": 5.0, "position": [-SLOT, Y_BRASS, 0.0], "scale": 1.0},
            {"t": DURATION, "position": [-SLOT, Y_BRASS, 0.0], "scale": 1.0},
        ],
    }
    mid = {
        "id": "mid",
        "kind": "sphere",
        "material": "brass",
        "position": [0.0, Y_BRASS, 0.0],
        "keys": [
            {"t": 0.0, "position": [0.0, Y_BRASS, 0.0], "scale": 1.0},
            {"t": DURATION, "position": [0.0, Y_BRASS, 0.0], "scale": 1.0},
        ],
    }
    sage = {
        "id": "right",
        "kind": "sphere",
        "material": "sage",
        "position": [SLOT, Y_SAGE, 0.0],
        "note": "Boss — monitors the two workers, slightly above, like the mark",
        "keys": [
            {"t": 0.0, "position": [SLOT, Y_SAGE, 0.0], "scale": 0.001},
            {"t": 8.6, "position": [SLOT, Y_SAGE, 0.0], "scale": 0.001},
            {"t": 9.15, "position": [SLOT, Y_SAGE, 0.0], "scale": 0.28},
            {"t": 10.4, "position": [SLOT, Y_SAGE, 0.0], "scale": 0.85},
            {"t": 11.3, "position": [SLOT, Y_SAGE, 0.0], "scale": 1.0},
            {"t": DURATION, "position": [SLOT, Y_SAGE, 0.0], "scale": 1.0},
        ],
    }
    floor = {
        "id": "floor",
        "kind": "plane",
        "material": "ink",
        "position": [0.0, -1.02, 0.0],
    }
    return [left, mid, sage, floor]


def camera_keys():
    """Watch the spin from the front; pull back as 2 then 3 appear. Roll -6 at lockup (logo stamp)."""
    return [
        {"t": 0.0, "pos": [0.15, 1.05, 6.4], "look": [0.0, 0.18, 0.0], "fov": 38, "roll": 0},
        {"t": 2.2, "pos": [0.4, 1.0, 7.6], "look": [-0.4, 0.18, 0.0], "fov": 36, "roll": 0},
        {"t": 5.0, "pos": [0.2, 0.92, 9.2], "look": [0.0, 0.22, 0.0], "fov": 34, "roll": 0},
        {"t": 8.4, "pos": [0.05, 0.78, 10.4], "look": [0.0, 0.28, 0.0], "fov": 33, "roll": 0},
        {"t": 11.2, "pos": [0.0, 0.68, 11.5], "look": [0.15, 0.32, 0.0], "fov": 32, "roll": 0},
        {"t": 16.0, "pos": [0.0, 0.62, 12.0], "look": [0.0, 0.28, 0.0], "fov": 32, "roll": 0},
    ]


def build_scene() -> dict:
    samples = simulate_pid()
    return {
        "format": "prim.scene",
        "version": "0.2.0",
        "scene_id": "scene:eidos-agi:ident-v4",
        "title": "Eidos ident v4",
        "duration": DURATION,
        "fps": FPS,
        "size": [1920, 1080],
        "intent": (
            "Reveal 1 worker (mid brass) spinning fast, then the second worker grows out of it. "
            "PID damps the spin to rest on an even floor. Then the sage boss appears slightly above, "
            "monitoring — the mark: two even, one raised."
        ),
        "camera": {"keys": camera_keys()},
        "objects": object_keys(),
        "group": {
            "rotation_z_deg": 0,
            "keys": downsample(samples),
            "cites": (
                f"PID yaw: hold omega={OMEGA_FAST} rad/s until t={HOLD_FAST}s, "
                f"then omega PID Kp={KP_W} Ki={KI_W} Kd={KD_W} plus angle lock Kp={KP_TH} when slow"
            ),
        },
        "type": [
            {"id": "word", "in": 12.0, "full": 12.9, "text": "Eidos AGI"},
            {
                "id": "lede",
                "in": 13.2,
                "full": 14.2,
                "text": "Software for agents. Governance for reality.",
            },
        ],
        "audio": {
            "file": "audio/bed.m4a",
            "cites": "track 1 last 16s, 1s fade in, 2.2s fade out on the song's decay",
        },
    }


def main() -> None:
    samples = simulate_pid()
    at = {round(s[0], 2): s for s in samples}

    def nearest(t):
        return min(samples, key=lambda s: abs(s[0] - t))

    for t in (0.0, 0.5, 2.0, 4.0, 6.0, 8.0, 10.0, 16.0):
        tt, th, om = nearest(t)
        print(f"t={t:5.2f}  theta={th:8.2f} rad ({math.degrees(th):8.1f} deg)  omega={om:7.3f} rad/s")
    scene = build_scene()
    dest = Path(__file__).resolve().parents[1] / "scene.json"
    dest.write_text(json.dumps(scene, indent=2) + "\n")
    print("wrote", dest, "group.keys", len(scene["group"]["keys"]))


if __name__ == "__main__":
    main()

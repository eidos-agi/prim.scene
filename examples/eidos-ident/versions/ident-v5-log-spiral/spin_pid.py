#!/usr/bin/env python3
"""Ident baker: log-spiral inbound → accretion → logo.

Three lanes of brass/sage notes sit on a ribbon. Camera follows one
equiangular spiral (look-ahead scaled with radius, banked on curvature,
fast open then bleed). Notes wrap onto one at 12s, then the mark.
Baked into scene.json. The renderer samples; it does not fly.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

DURATION = 16.0
FPS = 30
CRESCENDO = 12.0
LOGO_SPIN = 12.5
HOLD_FAST = 13.8
OMEGA_FAST = 2.6
KP_W = 1.55
KI_W = 0.04
KD_W = 0.22
KP_TH = 2.2
I_CLAMP = 5.0
DT = 1.0 / 240.0

Y_BRASS = 0.16
Y_SAGE = 0.72
SLOT = 2.207

LOCK_POS = [0.0, 0.62, 12.0]
LOCK_LOOK = [0.0, 0.28, 0.0]
LOCK_FOV = 32.0
LOCK_ROLL = 0.0
ONE_POS = [0.18, 0.82, 5.5]
ONE_LOOK = [0.0, 0.16, 0.0]
ONE_FOV = 40.0

LANE_X = (-1.08, 0.0, 1.08)
# Log spiral, one revolution open→handoff (Fable 2026-08-22).
R0 = 28.0
R_MIN = 2.6
B_SPIRAL = math.log(R0 / R_MIN) / (2.0 * math.pi)  # ~0.378
K_SPIRAL = B_SPIRAL / math.sqrt(1.0 + B_SPIRAL * B_SPIRAL)  # ~0.354
S_WIND = (R0 - R_MIN) / K_SPIRAL  # ~72
TH0 = math.pi / 2.0
ROAD_S_MAX = 76.0
SPEED = 9.0  # fast open; bleed after t=4 so ~one rev by t=9.85


def _smooth(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * u * (u * (u * 6 - 15) + 10)


def simulate_pid(duration: float = DURATION) -> list[tuple[float, float, float]]:
    """Logo yaw. Silent until LOGO_SPIN, rip, then rest-to-face at 16s."""
    theta = 0.0
    omega = 0.0
    t = 0.0
    th0 = w0 = target = None
    t_hold = HOLD_FAST
    T_rest = duration - HOLD_FAST
    a = b = c = d = 0.0
    out: list[tuple[float, float, float]] = []
    while t <= duration + 1e-9:
        if t < LOGO_SPIN:
            omega = 0.0
            theta = 0.0
        elif t < HOLD_FAST:
            omega += (28.0 * (OMEGA_FAST - omega)) * DT
            theta += omega * DT
        else:
            if target is None:
                th0, w0 = theta, omega
                t_hold = HOLD_FAST
                T_rest = max(1e-6, duration - HOLD_FAST)
                natural = th0 + w0 * T_rest / 2.0
                target = 2 * math.pi * math.ceil((natural - 0.15) / (2 * math.pi))
                if target < th0 + 0.4:
                    target += 2 * math.pi
                a, b = th0, w0
                c = (3.0 * (target - th0) - (2.0 * w0) * T_rest) / (T_rest * T_rest)
                d = (2.0 * (th0 - target) + w0 * T_rest) / (T_rest * T_rest * T_rest)
            u = min(T_rest, max(0.0, t - t_hold))
            theta = a + b * u + c * u * u + d * u * u * u
            omega = b + 2.0 * c * u + 3.0 * d * u * u
            if t >= duration - 1e-9:
                theta = target
                omega = 0.0
        out.append((t, theta, omega))
        t += DT
    return out


def group_keys(samples: list[tuple[float, float, float]], fps: float = FPS) -> list[dict]:
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


def _vadd(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def _vmul(a, s):
    return [a[0] * s, a[1] * s, a[2] * s]


def _vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _vcross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def _vlen(a):
    return math.sqrt(_vdot(a, a))


def _vnorm(a):
    n = _vlen(a)
    if n < 1e-12:
        return [0.0, 0.0, -1.0]
    return [a[0] / n, a[1] / n, a[2] / n]


def _centerline(s: float) -> list[float]:
    """Equiangular log spiral, one revolution, then a holding circle.

    r decreases linearly with arc length so θ(s) is closed form. Camera
    starts at (0, ·, +R0) and winds inbound; no highway-to-coil blend.
    """
    if s < S_WIND:
        r = max(R_MIN, R0 - K_SPIRAL * s)
        th = TH0 + (1.0 / B_SPIRAL) * math.log(R0 / max(r, 1e-9))
    else:
        r = R_MIN
        th = TH0 + (1.0 / B_SPIRAL) * math.log(R0 / R_MIN) + (s - S_WIND) / R_MIN
    weave = 0.30 * math.sin(0.4 * s) * (r / R0)
    # Radial weave in the disk plane, perpendicular to the radius vector.
    x = r * math.cos(th) - weave * math.sin(th)
    z = r * math.sin(th) + weave * math.cos(th)
    y = 0.48 + 0.05 * r
    return [x, y, z]


def _frame(s: float):
    p = _centerline(s)
    q = _centerline(s + 0.18)
    tang = _vnorm([q[i] - p[i] for i in range(3)])
    right = _vcross(tang, (0.0, 1.0, 0.0))
    if _vlen(right) < 1e-4:
        right = _vcross(tang, (1.0, 0.0, 0.0))
    right = _vnorm(right)
    up = _vnorm(_vcross(right, tang))
    return p, tang, right, up


def _bank(s: float, speed: float) -> float:
    _, t0, right, _ = _frame(s)
    _, t1, _, _ = _frame(s + 0.35)
    d = [t1[i] - t0[i] for i in range(3)]
    lat = _vdot(d, right)
    return max(-28.0, min(28.0, -math.degrees(math.atan2(lat * speed, 2.8))))


def road_samples(step: float = 0.16) -> list[dict]:
    n = int(ROAD_S_MAX / step)
    out = []
    for i in range(n + 1):
        s = i * step
        p, tang, right, up = _frame(s)
        out.append(
            {
                "s": round(s, 4),
                "p": [round(p[0], 4), round(p[1], 4), round(p[2], 4)],
                "t": [round(tang[0], 4), round(tang[1], 4), round(tang[2], 4)],
                "r": [round(right[0], 4), round(right[1], 4), round(right[2], 4)],
                "u": [round(up[0], 4), round(up[1], 4), round(up[2], 4)],
            }
        )
    return out


def camera_keys(fps: float = FPS) -> list[dict]:
    n = int(round(DURATION * fps))
    keys = []
    s = 0.0
    sdot = SPEED
    for i in range(n + 1):
        t = i / fps
        # Fast open, single long bleed, no swell (Fable).
        target = SPEED
        if t > 4.0:
            target = SPEED * (1.0 - 0.71 * _smooth((t - 4.0) / 5.6))
        sdot += (target - sdot) * (1.0 - math.exp(-4.2 / fps))
        s += sdot / fps
        p, tang, right, up = _frame(s)
        r_now = max(R_MIN, R0 - K_SPIRAL * min(s, S_WIND))
        ahead, *_ = _frame(s + max(1.6, 0.31 * r_now))
        pos = [
            p[0] + up[0] * 0.92 - tang[0] * 0.28,
            p[1] + up[1] * 0.92 - tang[1] * 0.28,
            p[2] + up[2] * 0.92 - tang[2] * 0.28,
        ]
        look = [
            ahead[0] - up[0] * 0.35,
            ahead[1] - up[1] * 0.35,
            ahead[2] - up[2] * 0.35,
        ]
        vel = _vmul(tang, sdot)
        roll = _bank(s, sdot)
        fov = 66.0 + 14.0 * min(1.0, sdot / (SPEED * 1.25))
        pose = {
            "t": round(t, 4),
            "pos": [round(pos[0], 4), round(pos[1], 4), round(pos[2], 4)],
            "look": [round(look[0], 4), round(look[1], 4), round(look[2], 4)],
            "fov": round(fov, 3),
            "roll": round(roll, 3),
            "vel": [round(vel[0], 4), round(vel[1], 4), round(vel[2], 4)],
            "s": round(s, 4),
        }
        u1 = _smooth((t - 9.85) / 2.15)
        u2 = _smooth((t - 12.15) / 2.6)
        if t < 12.15:
            tgt_p, tgt_l, tgt_f, tgt_r = ONE_POS, ONE_LOOK, ONE_FOV, 0.0
            u = u1
        else:
            pose["pos"] = list(ONE_POS)
            pose["look"] = list(ONE_LOOK)
            pose["fov"] = ONE_FOV
            pose["roll"] = 0.0
            pose["vel"] = [0.0, 0.0, 0.0]
            tgt_p, tgt_l, tgt_f, tgt_r = LOCK_POS, LOCK_LOOK, LOCK_FOV, LOCK_ROLL
            u = u2
        if u > 0:
            pose["pos"] = [pose["pos"][k] + u * (tgt_p[k] - pose["pos"][k]) for k in range(3)]
            pose["look"] = [pose["look"][k] + u * (tgt_l[k] - pose["look"][k]) for k in range(3)]
            pose["fov"] = pose["fov"] + u * (tgt_f - pose["fov"])
            pose["roll"] = pose["roll"] + u * (tgt_r - pose["roll"])
            pose["vel"] = [pose["vel"][k] * (1.0 - u) for k in range(3)]
        keys.append(pose)
    keys[-1]["t"] = DURATION
    keys[-1]["pos"] = list(LOCK_POS)
    keys[-1]["look"] = list(LOCK_LOOK)
    keys[-1]["fov"] = LOCK_FOV
    keys[-1]["roll"] = LOCK_ROLL
    keys[-1]["vel"] = [0.0, 0.0, 0.0]
    return keys


def object_keys():
    left = {
        "id": "left",
        "kind": "sphere",
        "material": "brass-light",
        "position": [0.0, Y_BRASS, 0.0],
        "keys": [
            {"t": 0.0, "position": [0.0, Y_BRASS, 0.0], "scale": 0.001},
            {"t": 12.1, "position": [0.0, Y_BRASS, 0.0], "scale": 0.001},
            {"t": 12.4, "position": [-0.5, Y_BRASS, 0.0], "scale": 0.4},
            {"t": 13.0, "position": [-1.2, Y_BRASS, 0.0], "scale": 0.82},
            {"t": 13.7, "position": [-SLOT, Y_BRASS, 0.0], "scale": 1.0},
            {"t": DURATION, "position": [-SLOT, Y_BRASS, 0.0], "scale": 1.0},
        ],
    }
    mid = {
        "id": "mid",
        "kind": "sphere",
        "material": "brass",
        "position": [0.0, Y_BRASS, 0.0],
        "keys": [
            {"t": 0.0, "position": [0.0, Y_BRASS, 0.0], "scale": 0.001},
            {"t": 10.75, "position": [0.0, Y_BRASS, 0.0], "scale": 0.001},
            {"t": 11.4, "position": [0.0, Y_BRASS, 0.0], "scale": 0.48},
            {"t": 12.0, "position": [0.0, Y_BRASS, 0.0], "scale": 1.0},
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
            {"t": 13.5, "position": [SLOT, Y_SAGE, 0.0], "scale": 0.001},
            {"t": 14.0, "position": [SLOT, Y_SAGE, 0.0], "scale": 0.35},
            {"t": 14.8, "position": [SLOT, Y_SAGE, 0.0], "scale": 1.0},
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
            "Log-spiral inbound (one revolution, fast open). Three-lane brass/sage "
            "notes ride the ribbon. Wrap onto one at 12s, then two workers and a sage "
            "boss. Mark Hermite-rests to face-camera at 16s."
        ),
        "camera": {
            "keys": camera_keys(),
            "cites": (
                "log spiral one-rev inbound; look-ahead scales with radius; "
                "fast open then bleed; not highway-then-coil, not noclip"
            ),
        },
        "objects": object_keys(),
        "group": {
            "rotation_z_deg": 0,
            "keys": group_keys(samples),
            "cites": (
                f"logo yaw from t={LOGO_SPIN}s omega={OMEGA_FAST} "
                f"hold until {HOLD_FAST}s then Hermite rest-to-2π at 16s"
            ),
        },
        "road": {
            "width": 2.55,
            "lanes": 3,
            "lane_x": list(LANE_X),
            "samples": road_samples(),
            "cites": "centerline + Frenet frames; notes live in 3 lanes; seekable",
        },
        "accretion": {
            "n": 2700,
            "seed": 7,
            "outer": 14.5,
            "inner": 1.45,
            "height": 2.2,
            "omega": 2.35,
            "dot_r": 0.14,
            "stream_until": 5.8,
            "morph": 7.4,
            "tighten": 9.0,
            "coalesce": 11.4,
            "gone": 12.15,
            "cites": "3-lane GH notes on the ribbon; wrap onto the one at crescendo",
        },
        "type": [
            {"id": "word", "in": 12.2, "full": 13.05, "text": "Eidos AGI"},
            {
                "id": "lede",
                "in": 14.5,
                "full": 15.3,
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

    def nearest(t):
        return min(samples, key=lambda s: abs(s[0] - t))

    for t in (0.0, 6.9, 12.0, 12.5, 13.75, 14.5, 15.5, 16.0):
        _, th, om = nearest(t)
        print(f"t={t:5.2f}  logo_yaw={math.degrees(th):8.1f} deg  omega={om:7.3f} rad/s")
    scene = build_scene()
    cam = scene["camera"]["keys"]
    print("-- spiral --")
    for t in (0.0, 1.9, 4.0, 6.0, 8.8, 9.85, 11.2):
        k = min(cam, key=lambda x: abs(x["t"] - t))
        p = k["pos"]
        az = math.degrees(math.atan2(p[0], p[2]))
        print(
            f"t={t:5.2f}  p=({p[0]:6.2f},{p[1]:5.2f},{p[2]:6.2f})  "
            f"az={az:6.1f}  |v|={math.sqrt(sum(v*v for v in k.get('vel',[0,0,0]))):5.2f}  "
            f"s={k.get('s', 0):5.1f}"
        )
    print("road n", len(scene["road"]["samples"]), "S_WIND", round(S_WIND, 1))
    dest = Path(__file__).resolve().parents[1] / "scene.json"
    dest.write_text(json.dumps(scene, indent=2) + "\n")
    print("wrote", dest, "cam", len(cam), "group", len(scene["group"]["keys"]))


if __name__ == "__main__":
    main()

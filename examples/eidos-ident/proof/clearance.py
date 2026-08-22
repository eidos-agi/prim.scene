#!/usr/bin/env python3
"""Min camera-to-sphere clearance at every camera key t. Cwd: prim.scene repo root
   python3 examples/eidos-ident/proof/clearance.py examples/eidos-ident/scene.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path


def lerp(a, b, u):
    return a + (b - a) * u


def sample_obj(obj, t):
    keys = obj.get("keys")
    if not keys:
        return list(obj["position"]), float(obj.get("scale") or 1)
    if t <= keys[0]["t"]:
        k = keys[0]
        return list(k["position"]), float(k.get("scale", 1))
    if t >= keys[-1]["t"]:
        k = keys[-1]
        return list(k["position"]), float(k.get("scale", 1))
    i = 0
    while i < len(keys) - 1 and t > keys[i + 1]["t"]:
        i += 1
    a, b = keys[i], keys[i + 1]
    u = (t - a["t"]) / (b["t"] - a["t"])
    pa, pb = a["position"], b["position"]
    pos = [lerp(pa[j], pb[j], u) for j in range(3)]
    sa = float(a.get("scale", 1))
    sb = float(b.get("scale", 1))
    return pos, lerp(sa, sb, u)


def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: clearance.py <scene.json>", file=sys.stderr)
        return 2
    scene = json.loads(Path(argv[1]).read_text())
    spheres = [o for o in scene["objects"] if o.get("kind") == "sphere"]
    radius = 1.0
    worst = None
    for ck in scene["camera"]["keys"]:
        t = ck["t"]
        cam = ck["pos"]
        for o in spheres:
            pos, scale = sample_obj(o, t)
            d = dist(cam, pos)
            need = radius * scale + 0.4
            row = (d - need, d, t, o["id"], pos)
            if worst is None or row[0] < worst[0]:
                worst = row
            print(f"t={t:.2f} {o['id']:6s} clearance={d:.3f} need={need:.3f} center={pos}")
    assert worst is not None
    print(f"min_clearance {worst[1]:.3f} at t={worst[2]} object={worst[3]} (margin {worst[0]:.3f})")
    if worst[0] <= 0:
        return 1
    if worst[1] < 1.4:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

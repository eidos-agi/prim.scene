#!/usr/bin/env python3
"""Locks for ident: 1 then 2 then 3, PID spin, even brass, raised sage."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate import validate  # noqa: E402

PACK = ROOT / "examples" / "eidos-ident"
sys.path.insert(0, str(PACK / "proof"))
from spin_pid import HOLD_FAST, OMEGA_FAST, simulate_pid  # noqa: E402


def _scale_at(obj, t):
    keys = obj["keys"]
    if t <= keys[0]["t"]:
        return keys[0]["scale"]
    if t >= keys[-1]["t"]:
        return keys[-1]["scale"]
    i = 0
    while i < len(keys) - 1 and t > keys[i + 1]["t"]:
        i += 1
    a, b = keys[i], keys[i + 1]
    u = (t - a["t"]) / (b["t"] - a["t"])
    return a["scale"] + u * (b["scale"] - a["scale"])


class IdentLocks(unittest.TestCase):
    def test_live_pack_validates(self):
        errs = validate(PACK)
        self.assertEqual(errs, [], msg=errs)

    def test_reveal_one_then_two_then_three(self):
        s = json.loads((PACK / "scene.json").read_text())
        self.assertEqual(s["scene_id"], "scene:eidos-agi:ident-v4")
        by = {o["id"]: o for o in s["objects"]}
        left, mid, sage = by["left"], by["mid"], by["right"]
        self.assertGreaterEqual(_scale_at(mid, 0.0), 0.9)
        self.assertLess(_scale_at(left, 0.0), 0.15)
        self.assertLess(_scale_at(sage, 0.0), 0.05)
        self.assertGreater(_scale_at(left, 3.5), 0.85)
        self.assertLess(_scale_at(sage, 8.0), 0.05)
        self.assertGreater(_scale_at(sage, 16.0), 0.95)
        self.assertGreaterEqual(next(t["in"] for t in s["type"] if t["id"] == "word"), 12.0)

    def test_even_brass_raised_sage(self):
        s = json.loads((PACK / "scene.json").read_text())
        by = {o["id"]: o for o in s["objects"]}
        ll = by["left"]["keys"][-1]["position"]
        ml = by["mid"]["keys"][-1]["position"]
        rl = by["right"]["keys"][-1]["position"]
        floor = by["floor"]["position"][1]
        self.assertLess(abs(ll[1] - ml[1]), 0.01)
        self.assertGreaterEqual(rl[1] - ll[1], 0.35)
        self.assertGreater(ll[1], floor + 1.0)

    def test_pid_fast_then_slow(self):
        samples = simulate_pid()
        def near(t):
            return min(samples, key=lambda s: abs(s[0] - t))
        self.assertGreater(near(0.5)[2], 10.0)
        self.assertGreater(near(HOLD_FAST - 0.05)[2], 10.0)
        self.assertGreater(near(4.0)[2], 5.0)
        self.assertLess(abs(near(16.0)[2]), 0.08)
        self.assertGreater(OMEGA_FAST, 10.0)
        yaw = [k["rotation_y_deg"] for k in json.loads((PACK / "scene.json").read_text())["group"]["keys"]]
        self.assertGreater(max(yaw) - min(yaw), 720.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

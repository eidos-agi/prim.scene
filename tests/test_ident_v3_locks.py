#!/usr/bin/env python3
"""Numeric locks for ident-v3 against shipped validate() + scene.json."""
from __future__ import annotations

import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate import validate  # noqa: E402

PACK = ROOT / "examples" / "eidos-ident"


class IdentV3Locks(unittest.TestCase):
    def test_live_pack_validates(self):
        errs = validate(PACK)
        self.assertEqual(errs, [], msg=errs)

    def test_growth_and_equal_float(self):
        s = json.loads((PACK / "scene.json").read_text())
        self.assertEqual(s["scene_id"], "scene:eidos-agi:ident-v3")
        self.assertEqual(s["duration"], 16.0)
        self.assertEqual(s["size"], [1920, 1080])
        word = next(t for t in s["type"] if t["id"] == "word")
        self.assertGreaterEqual(word["in"], 12.0)
        by = {o["id"]: o for o in s["objects"]}
        left, mid, right, floor = by["left"], by["mid"], by["right"], by["floor"]
        self.assertTrue(left.get("keys"))
        self.assertTrue(mid.get("keys"))
        self.assertFalse(right.get("keys"))
        l0, m0 = left["keys"][0], mid["keys"][0]
        ll, ml = left["keys"][-1], mid["keys"][-1]
        dist0 = sum((l0["position"][i] - m0["position"][i]) ** 2 for i in range(3)) ** 0.5
        self.assertTrue(dist0 < 0.15 or l0.get("scale", 1) < 0.15)
        self.assertNotEqual(l0["position"], right["position"])
        self.assertFalse(l0["position"] == [-2.207, ll["position"][1], 0.0] and l0.get("scale", 1) == 1)
        theta = math.radians(-6.0)
        def world_y(x, y):
            return x * math.sin(theta) + y * math.cos(theta)
        wy_l = world_y(ll["position"][0], ll["position"][1])
        wy_m = world_y(ml["position"][0], ml["position"][1])
        wy_r = world_y(right["position"][0], right["position"][1])
        self.assertLess(abs(wy_l - wy_m), 0.01)
        self.assertGreater(wy_l, floor["position"][1] + 1.0)
        self.assertGreaterEqual(abs(wy_r - wy_l), 0.15)
        self.assertEqual(s["audio"]["file"], "audio/bed.m4a")
        self.assertTrue((PACK / "audio" / "bed.m4a").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Drive shipped validate() for optional object motion keys."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate import validate  # noqa: E402


def _minimal(objects: list) -> dict:
    return {
        "format": "prim.scene",
        "version": "0.2.0",
        "scene_id": "scene:test:object-keys",
        "title": "object-keys fixture",
        "duration": 16.0,
        "fps": 30,
        "size": [1920, 1080],
        "intent": "fixture for validate()",
        "camera": {
            "keys": [
                {"t": 0.0, "pos": [0, 1, 8], "look": [0, 0, 0], "fov": 40},
                {"t": 16.0, "pos": [0, 1, 8], "look": [0, 0, 0], "fov": 40},
            ]
        },
        "objects": objects,
    }


def _pack(scene: dict) -> Path:
    d = Path(tempfile.mkdtemp(prefix="prim-scene-keys-"))
    (d / "index.md").write_text("---\nprofile: scene\n---\n")
    (d / "scene.json").write_text(json.dumps(scene, indent=2))
    return d


class ObjectKeysValidate(unittest.TestCase):
    def test_well_formed_object_keys_empty_errors(self):
        pack = _pack(
            _minimal(
                [
                    {
                        "id": "left",
                        "kind": "sphere",
                        "position": [0.0, 0.0, 0.0],
                        "keys": [
                            {"t": 0.0, "position": [0.0, 0.08, 0.0], "scale": 0.08},
                            {"t": 16.0, "position": [-2.207, 0.42, 0.0], "scale": 1.0},
                        ],
                    }
                ]
            )
        )
        errs = validate(pack)
        self.assertEqual(errs, [], msg=errs)

    def test_last_object_key_not_duration_names_object(self):
        pack = _pack(
            _minimal(
                [
                    {
                        "id": "left",
                        "kind": "sphere",
                        "position": [0.0, 0.0, 0.0],
                        "keys": [
                            {"t": 0.0, "position": [0.0, 0.0, 0.0], "scale": 0.1},
                            {"t": 15.5, "position": [-2.207, 0.42, 0.0], "scale": 1.0},
                        ],
                    }
                ]
            )
        )
        errs = validate(pack)
        self.assertTrue(errs, "expected non-empty errors for last t != duration")
        blob = " ".join(errs)
        self.assertIn("left", blob)
        self.assertTrue("15.5" in blob or "duration" in blob)

    def test_static_objects_without_keys_empty_errors(self):
        pack = _pack(
            _minimal(
                [
                    {"id": "left", "kind": "sphere", "position": [-2.207, 0.0, 0.0]},
                    {"id": "mid", "kind": "sphere", "position": [0.0, 0.0, 0.0]},
                ]
            )
        )
        errs = validate(pack)
        self.assertEqual(errs, [], msg=errs)

    def test_reversed_object_key_times_fail(self):
        pack = _pack(
            _minimal(
                [
                    {
                        "id": "mid",
                        "kind": "sphere",
                        "position": [0.0, 0.0, 0.0],
                        "keys": [
                            {"t": 0.0, "position": [0.0, 0.0, 0.0]},
                            {"t": 8.0, "position": [0.0, 0.2, 0.0]},
                            {"t": 4.0, "position": [0.0, 0.3, 0.0]},
                            {"t": 16.0, "position": [0.0, 0.42, 0.0]},
                        ],
                    }
                ]
            )
        )
        errs = validate(pack)
        self.assertTrue(errs)
        self.assertTrue(any("mid" in e and "strictly increasing" in e for e in errs), errs)


if __name__ == "__main__":
    unittest.main(verbosity=2)

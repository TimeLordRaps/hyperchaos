"""Actual command-line routes and malformed JSON boundary checks."""

import json
from pathlib import Path
import subprocess
import sys
import unittest
import hyperchaos as h


ROOT = Path(h.__file__).resolve().parent


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", "-u", str(ROOT / "hyperchaos.py"), *args],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                              timeout=5, check=False)

    def test_supplied_frame_executes_the_actual_cli(self):
        result = self.run_cli("--input", "examples/balanced-divergence.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["direction"], "HYPERCHAOS")
        self.assertFalse(report["iterated_divergences"][0]["pattern_variation"])

    def test_examples_cover_the_six_semantic_controls(self):
        result = self.run_cli("--examples")
        self.assertEqual(result.returncode, 0, result.stderr)
        reports = json.loads(result.stdout)
        self.assertEqual(len(reports), 6)
        self.assertEqual(reports["redirected-orderly-trajectory"]["direction"], "ORDINARY_DIVERGENCE")
        self.assertEqual(reports["divergence-resolving-into-order"]["direction"], "HYPERORDER")

    def test_duplicate_json_keys_are_not_silently_overwritten(self):
        result = self.run_cli("--input", "tests/fixtures/ambiguous-frame.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate JSON key", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_unrelated_descriptor_is_not_misread_as_a_frame(self):
        result = self.run_cli("--input", "FIELD.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("FRAME REJECTED", result.stderr)


if __name__ == "__main__":
    unittest.main()

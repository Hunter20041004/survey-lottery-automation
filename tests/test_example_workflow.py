import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ExampleWorkflowTests(unittest.TestCase):
    def test_example_runs_through_real_file_and_process_boundaries(self):
        completed = subprocess.run(
            [
                sys.executable,
                "examples/run_lottery.py",
                "--seed",
                "2026",
                "--winners",
                "2",
            ],
            cwd=PROJECT_ROOT,
            env={**os.environ, "PYTHONPATH": "src"},
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        output_lines = completed.stdout.strip().splitlines()
        audit_record = json.loads(output_lines[0])
        self.assertEqual(2, len(audit_record["winner_ids"]))
        self.assertEqual(2, len(set(audit_record["winner_ids"])))
        self.assertTrue(all("dry-run" in line for line in output_lines[1:]))


if __name__ == "__main__":
    unittest.main()

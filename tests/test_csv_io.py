import tempfile
import unittest
from pathlib import Path

from survey_lottery.csv_io import load_participants
from survey_lottery.domain import Participant


class CsvInputTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)

    def write_csv(self, content: str) -> Path:
        path = Path(self.temp_directory.name) / "responses.csv"
        path.write_text(content, encoding="utf-8")
        return path

    def test_loads_real_csv_file(self):
        path = self.write_csv(
            "participant_id,eligible\nP-001,true\nP-002,FALSE\n"
        )

        participants = load_participants(path)

        self.assertEqual(
            (Participant("P-001", True), Participant("P-002", False)),
            participants,
        )

    def test_missing_required_columns_are_rejected(self):
        path = self.write_csv("participant_id\nP-001\n")

        with self.assertRaisesRegex(ValueError, "Missing CSV columns: eligible"):
            load_participants(path)

    def test_invalid_boolean_names_the_csv_row(self):
        path = self.write_csv("participant_id,eligible\nP-001,yes\n")

        with self.assertRaisesRegex(ValueError, "row 2"):
            load_participants(path)

    def test_blank_participant_id_names_the_csv_row(self):
        path = self.write_csv('participant_id,eligible\n"   ",true\n')

        with self.assertRaisesRegex(ValueError, "row 2"):
            load_participants(path)


if __name__ == "__main__":
    unittest.main()

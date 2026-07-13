import json
import unittest
from datetime import datetime, timezone

from survey_lottery.audit import build_audit_record
from survey_lottery.domain import DrawResult, Participant


class AuditRecordTests(unittest.TestCase):
    def test_builds_traceable_audit_record(self):
        participants = (
            Participant("P-001", True),
            Participant("P-002", False),
            Participant("P-003", True),
        )
        result = DrawResult(
            winners=(Participant("P-003", True),),
            seed=2026,
            winner_count=1,
            total_count=3,
            eligible_count=2,
        )

        record = build_audit_record(
            result,
            participants,
            datetime(2026, 7, 12, tzinfo=timezone.utc),
        )

        self.assertEqual("2026-07-12T00:00:00+00:00", record["timestamp_utc"])
        self.assertEqual(["P-003"], record["winner_ids"])
        self.assertEqual(64, len(record["input_sha256"]))

    def test_audit_exposes_only_approved_privacy_safe_fields(self):
        participants = (Participant("P-001", True),)
        result = DrawResult(
            winners=participants,
            seed=2026,
            winner_count=1,
            total_count=1,
            eligible_count=1,
        )

        record = build_audit_record(
            result,
            participants,
            datetime(2026, 7, 12, tzinfo=timezone.utc),
        )

        self.assertEqual(
            {
                "timestamp_utc",
                "seed",
                "winner_count",
                "total_count",
                "eligible_count",
                "winner_ids",
                "input_sha256",
            },
            set(record),
        )
        serialized = json.dumps(record).lower()
        for forbidden_term in ("email", "name", "student", "message"):
            self.assertNotIn(forbidden_term, serialized)


if __name__ == "__main__":
    unittest.main()

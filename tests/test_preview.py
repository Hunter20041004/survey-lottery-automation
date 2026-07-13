import unittest

from survey_lottery.domain import Participant
from survey_lottery.preview import build_notification_previews


class NotificationPreviewTests(unittest.TestCase):
    def test_builds_local_id_only_previews(self):
        previews = build_notification_previews((Participant("P-003", True),))

        self.assertEqual(
            ("Winner P-003: notification ready (dry-run)",),
            previews,
        )


if __name__ == "__main__":
    unittest.main()

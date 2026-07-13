import unittest

from survey_lottery.domain import Participant
from survey_lottery.draw import draw_winners, run_draw


class DrawWinnersTests(unittest.TestCase):
    def test_same_seed_returns_same_winners(self):
        participants = tuple(
            Participant(f"P-{index:03d}", True) for index in range(1, 7)
        )

        first = draw_winners(participants, winner_count=2, seed=2026)
        second = draw_winners(participants, winner_count=2, seed=2026)

        self.assertEqual(first, second)
        self.assertEqual(2, len(set(first)))

    def test_ineligible_participants_are_never_selected(self):
        participants = (
            Participant("P-001", True),
            Participant("P-002", False),
        )

        winners = draw_winners(participants, winner_count=1, seed=7)

        self.assertEqual((Participant("P-001", True),), winners)

    def test_duplicate_participant_ids_are_rejected(self):
        participants = (
            Participant("P-001", True),
            Participant("P-001", True),
        )

        with self.assertRaisesRegex(ValueError, "Duplicate participant_id"):
            draw_winners(participants, winner_count=1, seed=7)

    def test_winner_count_must_fit_eligible_population(self):
        participants = (Participant("P-001", True),)

        for count in (0, 2):
            with self.subTest(count=count), self.assertRaisesRegex(
                ValueError, "winner_count"
            ):
                draw_winners(participants, winner_count=count, seed=7)

    def test_run_draw_summarizes_the_population(self):
        participants = (
            Participant("P-001", True),
            Participant("P-002", False),
            Participant("P-003", True),
        )

        result = run_draw(participants, winner_count=1, seed=2026)

        self.assertEqual(2026, result.seed)
        self.assertEqual(1, result.winner_count)
        self.assertEqual(3, result.total_count)
        self.assertEqual(2, result.eligible_count)
        self.assertTrue(result.winners[0].eligible)


if __name__ == "__main__":
    unittest.main()

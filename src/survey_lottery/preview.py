from collections.abc import Sequence

from .domain import Participant


def build_notification_previews(
    winners: Sequence[Participant],
) -> tuple[str, ...]:
    return tuple(
        f"Winner {winner.participant_id}: notification ready (dry-run)"
        for winner in winners
    )

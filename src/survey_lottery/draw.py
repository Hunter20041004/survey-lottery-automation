import random
from collections.abc import Sequence

from .domain import DrawResult, Participant


def draw_winners(
    participants: Sequence[Participant], winner_count: int, seed: int
) -> tuple[Participant, ...]:
    participant_ids = [participant.participant_id for participant in participants]
    if len(participant_ids) != len(set(participant_ids)):
        raise ValueError("Duplicate participant_id values are not allowed")

    eligible_participants = tuple(
        participant for participant in participants if participant.eligible
    )
    if winner_count < 1 or winner_count > len(eligible_participants):
        raise ValueError(
            "winner_count must be positive and no greater than the eligible population"
        )

    return tuple(random.Random(seed).sample(eligible_participants, winner_count))


def run_draw(
    participants: Sequence[Participant], winner_count: int, seed: int
) -> DrawResult:
    participants = tuple(participants)
    winners = draw_winners(participants, winner_count, seed)
    return DrawResult(
        winners=winners,
        seed=seed,
        winner_count=winner_count,
        total_count=len(participants),
        eligible_count=sum(participant.eligible for participant in participants),
    )

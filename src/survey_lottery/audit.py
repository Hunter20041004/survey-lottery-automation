import hashlib
from collections.abc import Sequence
from datetime import datetime

from .domain import DrawResult, Participant


def build_audit_record(
    result: DrawResult,
    participants: Sequence[Participant],
    timestamp: datetime,
) -> dict[str, object]:
    ordered_ids = "\n".join(
        participant.participant_id for participant in participants
    ).encode("utf-8")
    return {
        "timestamp_utc": timestamp.isoformat(),
        "seed": result.seed,
        "winner_count": result.winner_count,
        "total_count": result.total_count,
        "eligible_count": result.eligible_count,
        "winner_ids": [winner.participant_id for winner in result.winners],
        "input_sha256": hashlib.sha256(ordered_ids).hexdigest(),
    }

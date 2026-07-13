from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Participant:
    participant_id: str
    eligible: bool


@dataclass(frozen=True, slots=True)
class DrawResult:
    winners: tuple[Participant, ...]
    seed: int
    winner_count: int
    total_count: int
    eligible_count: int

import csv
from pathlib import Path

from .domain import Participant


def load_participants(path: str | Path) -> tuple[Participant, ...]:
    with Path(path).open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {"participant_id", "eligible"}
        missing_columns = sorted(required_columns - set(reader.fieldnames or ()))
        if missing_columns:
            raise ValueError(f"Missing CSV columns: {', '.join(missing_columns)}")

        participants = []
        for row_number, row in enumerate(reader, start=2):
            participant_id = row["participant_id"].strip()
            if not participant_id:
                raise ValueError(f"Blank participant_id at row {row_number}")

            eligible_value = row["eligible"].strip().lower()
            if eligible_value not in {"true", "false"}:
                raise ValueError(
                    f"Invalid eligible value at row {row_number}; expected true or false"
                )
            participants.append(
                Participant(
                    participant_id=participant_id,
                    eligible=eligible_value == "true",
                )
            )
        return tuple(participants)

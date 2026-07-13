import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from survey_lottery.audit import build_audit_record
from survey_lottery.csv_io import load_participants
from survey_lottery.draw import run_draw
from survey_lottery.preview import build_notification_previews


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a reproducible lottery against synthetic survey data."
    )
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--winners", type=int, required=True)
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "sample_responses.csv",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    participants = load_participants(arguments.input)
    result = run_draw(participants, arguments.winners, arguments.seed)
    audit_record = build_audit_record(
        result,
        participants,
        datetime.now(timezone.utc),
    )

    print(json.dumps(audit_record, separators=(",", ":")))
    for preview in build_notification_previews(result.winners):
        print(preview)


if __name__ == "__main__":
    main()

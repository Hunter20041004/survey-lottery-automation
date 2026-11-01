# Details

Back to [README](../README.md).

## Data contract

The public CSV accepts exactly two required fields:

| Field | Meaning | Example |
| --- | --- | --- |
| `participant_id` | Unique opaque identifier | `P-001` |
| `eligible` | Case-insensitive `true` or `false` | `true` |

No contact field is part of the public contract. A private deployment can map selected IDs back to contact details outside this repository.

## Audit record

Each draw records:

- UTC timestamp;
- caller-supplied seed;
- requested winner count;
- total and eligible population counts;
- selected synthetic IDs;
- SHA-256 digest of the ordered input IDs.

The audit record never includes names, email addresses, student IDs, spreadsheet URLs, credentials, or message bodies.

## Testing

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The suite exercises business rules and real boundaries: temporary CSV files, a subprocess CLI workflow, notebook JSON, and tracked-file secret scanning. It does not rely on mocked Google or SMTP responses.

## Repository structure

```text
data/                   Synthetic sample responses
examples/               Runnable command-line workflow
notebooks/              Google Colab walkthrough
src/survey_lottery/     Tested application modules
tests/                  Unit, contract, and safety tests
PRIVACY.md              Public/private data boundary
```

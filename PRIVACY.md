# Privacy and Security Boundary

This repository is a public, privacy-safe reconstruction of a real survey workflow.

## Included

- Synthetic participant IDs such as `P-001`.
- Synthetic eligibility values.
- Reproducible draw metadata and ID-only audit output.
- Local notification previews that make no network connection.

## Never included

- Real survey responses.
- Names, email addresses, phone numbers, or student IDs.
- Google Sheet or Drive identifiers from the original workflow.
- Service-account files, app passwords, access tokens, or environment files.
- Real notification copy or outbound SMTP functionality.

## Private deployment guidance

A production adaptation should keep contact data in a private system and expose only opaque IDs to the draw engine. Resolve selected IDs to contact details after the draw, outside this repository. Store credentials in a managed secret store, Colab Secrets, or environment variables; never place credentials in notebook cells or committed files.

The included safety test scans public text artifacts for credential-shaped content and identifiers associated with the unsafe original pattern. This is a regression guard, not a replacement for secret rotation or repository access controls.

## Reporting

If you find private data or a credential in this repository, do not copy or reuse it. Report the file and path through a private channel to the repository owner.

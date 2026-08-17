# Selected fixture evidence

This directory contains a minimized, human-readable projection of a deterministic Arbiter demonstration. It is intentionally not the complete private evidence bundle.

The scenario proves the distinction between CI success and independent assurance:

- Candidate 1 passed the application-owned engineering checks.
- Independent authentication validation detected that a protected endpoint returned success without a bearer token.
- Arbiter created a critical blocking finding and did not mark the candidate ready.
- A scoped remediation produced Candidate 2 as a new historical candidate.
- The complete 15-check suite reran against Candidate 2 and passed.
- Evidence and audit integrity verified.
- Arbiter reached `READY_TO_APPROVE`; the human decision stayed `PENDING`.

See [`run-summary.json`](run-summary.json) and [`finding-summary.json`](finding-summary.json).

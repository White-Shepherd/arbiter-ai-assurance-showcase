# Reproducibility guide

This repository supports reproduction of the **public documentation and demonstrations**. The private Arbiter implementation is not included, so this repository cannot independently rerun the Trust Loop engine.

## Review the static walkthrough

1. Clone this repository.
2. Open `site/index.html` in a modern browser.
3. Navigate the overview, change, validation, evidence, history, and human-decision sections.
4. Confirm the bundled walkthrough video plays with its WebVTT captions.

No build step or network service is required.

## Review the video series

The seven MP4 files in `media/videos` correspond one-for-one with the caption files in `media/captions`. `media/manifest.json` records the published sequence.

## Review the selected evidence

Read `evidence/sample-run/README.md` and the adjacent JSON summaries. Confirm the demonstrated causal sequence:

1. Candidate 1 passes ordinary engineering checks but fails independent authentication validation.
2. A critical blocking finding is retained.
3. Remediation creates Candidate 2 rather than overwriting Candidate 1.
4. The full validation suite reruns and passes.
5. Arbiter reaches `READY_TO_APPROVE` while the human decision remains `PENDING`.

## Review the Mission Control publication

Read `docs/architecture/mission-control-companion.md` and confirm that it keeps the following boundaries explicit:

1. Mission Control is a separate observability companion, not part of Arbiter's Phase 1 Trust Loop implementation.
2. Demo and Live Local providers share canonical presentation models.
3. Live Local access remains loopback-only, allowlisted, GET-only, and read-only.
4. Observed, derived, Demo, and unavailable evidence remain distinguishable.
5. The published validation counts describe a repository-controlled synthetic profile, not a production deployment.

The Mission Control implementation and complete validation corpus are not included in this public showcase, so the stated implementation checks cannot be rerun from this repository.

## Limits

The selected evidence is a minimized explanatory projection of a deterministic fixture run. It is not a substitute for the complete hashed evidence manifest, append-only audit ledger, protected controls, or an independent execution of the private implementation.

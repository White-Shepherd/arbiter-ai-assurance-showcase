# Arbiter AI Assurance — Public Showcase

Arbiter is an independent assurance layer for AI-assisted software changes. It separates the agent that proposes a change from the controls that inspect the resulting Git candidate, preserve evidence, route remediation, and present a decision to a human approver.

This public repository is a curated, view-only companion to the private engineering repository. It contains product explanations, architecture, demonstration media, selected fixture evidence, and a reproducibility guide. It intentionally does **not** contain Arbiter's implementation, protected validators, private operational records, credentials, or customer data.

## Start here

- [Business use cases](docs/business/business-use-cases.md)
- [System architecture](docs/architecture/system-architecture.md)
- [Trust Loop walkthrough](docs/architecture/trust-loop-walkthrough.md)
- [Security model](docs/architecture/security-model.md)
- [Validation model](docs/validation/validation-model.md)
- [Evidence and audit model](docs/validation/evidence-and-audit.md)
- [Selected demonstration evidence](evidence/sample-run/README.md)
- [Reproducibility guide](REPRODUCIBILITY.md)
- [Publication boundaries](PUBLICATION-SCOPE.md)

## Demonstrations

Open [`site/index.html`](site/index.html) for the guided static walkthrough. Screenshots are under [`site/assets`](site/assets), and the complete captioned video series is under [`media`](media).

The demonstration uses deterministic fixtures. Fixture results illustrate Arbiter's behavior; they are not claims about a live customer system or production deployment.

## Current status

The private Phase 1 implementation has passed its independent acceptance workflow on a clean Windows checkout. This showcase documents that design and presents selected results, but it cannot reproduce the private implementation by itself.

## Rights

This repository is public for inspection and evaluation. No open-source license is granted yet. See [RIGHTS.md](RIGHTS.md).

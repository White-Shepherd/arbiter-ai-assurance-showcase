# Arbiter AI Assurance — Public Showcase

Arbiter is an independent assurance layer for AI-assisted software changes. It separates the agent that proposes a change from the controls that inspect the resulting Git candidate, preserve evidence, route remediation, and present a decision to a human approver.

This public repository is a curated, view-only companion to the private engineering repository. It contains product explanations, architecture, demonstration media, selected fixture evidence, and a reproducibility guide. It intentionally does **not** contain Arbiter's implementation, protected validators, private operational records, credentials, or customer data.

The showcase also documents Mission Control, a separate read-only observability companion for repository-driven engineering workflows. Mission Control is not presented as part of Arbiter's Phase 1 implementation, and no direct Arbiter integration is claimed.

## Start here

- [Business use cases](docs/business/business-use-cases.md)
- [System architecture](docs/architecture/system-architecture.md)
- [Mission Control companion observability](docs/architecture/mission-control-companion.md)
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

Mission Control's repository-controlled synthetic profile currently passes 31 automated tests, lint, type check, build, 13 representative GET routes, 52 mutation-method rejection probes, non-mutation verification, and freshness verification. These are validation results for the companion interface—not evidence of a production deployment or a completed Arbiter integration.

## Rights

This repository is public for inspection and evaluation. No open-source license is granted yet. See [RIGHTS.md](RIGHTS.md).

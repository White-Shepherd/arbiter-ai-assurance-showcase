# Evidence and audit

## Purpose

Evidence answers **what exact observation supports this check, finding, or decision?** Audit answers **what happened, in what order, and under which domain identities?** Neither independently decides the product verdict.

## Portable run layout

```text
runs/RUN-…/
  authorization/
  baseline/
  agent-runs/
  candidates/
  validation/
  findings/
  approval/
  evidence/EVID-…/
    artifact-or-result
    metadata.json
  evidence-manifest.json
  audit.jsonl
```

Paths persisted in metadata are run-relative and use forward slashes. Absolute, drive-qualified, UNC, and parent-traversal paths are rejected.

## Evidence creation

1. Receive a structured or file-backed observation.
2. Redact configured token values and recognized credential fields.
3. Allocate an immutable evidence ID.
4. Write the exact artifact bytes.
5. Compute lowercase SHA-256 and byte size.
6. Write strict schema-valid metadata.
7. Bind check/finding references to the durable ID.
8. Include the item in the run manifest.

Create-only semantics prevent an existing evidence or domain identity from being overwritten.

## Canonical serialization

Generated JSON uses UTF-8, lexicographically sorted object keys at every depth, two-space indentation, and one trailing line feed. Array order is preserved. The bytes written are the bytes hashed.

The manifest is ordered by evidence ID. Its hash is computed over the canonical object without `manifestSha256`; that field is then added to the persisted document.

## Audit ledger

Audit events are strict schema-valid JSON objects appended one per line to `audit.jsonl`. Verification checks:

- Valid JSON and schema
- Unique event IDs
- Nondecreasing timestamps
- No absolute-path leakage in metadata
- Consistency with domain records and readiness

Typical events include authorization, baseline capture, agent execution, candidate creation, validation start/completion, finding creation, remediation, readiness, and human decision.

## Verification

`verifyRunEvidence` verifies:

- Manifest structure and self-hash
- Presence, SHA-256, and byte size of every artifact
- Evidence metadata
- Audit syntax, IDs, chronology, and path safety
- Domain-record schemas and referential integrity

The aggregate result is `EVIDENCE_VERIFIED` or `EVIDENCE_INVALID`; it is not the Arbiter product verdict.

```sh
npm run evidence:verify -- RUN-example
```

## Reconstruction

The inspector rebuilds state from persisted records and audit history:

```sh
npm run trust-loop:inspect -- RUN-example
```

It identifies the current candidate, orders candidates and validations causally, retains historical findings, verifies evidence, and recovers the Arbiter verdict and human decision. It rejects impossible combinations instead of guessing.

## Checkout portability

`.gitattributes` marks top-level `runs/**` and archived `docs/validation/runs/**` as `-text`. Git therefore treats evidence as opaque bytes and cannot rewrite line endings on Windows checkouts.

## Integrity limits

Phase 1 is tamper-evident, not tamper-proof. It detects changed or missing artifacts, manifest changes, malformed audit data, duplicate events, chronology regressions, and invalid domain records. A privileged attacker able to rewrite every artifact, metadata record, manifest, and audit entry can manufacture a new internally consistent directory.

Phase 1 does not provide signatures, trusted timestamps, hardware-backed keys, independent witnesses, immutable cloud storage, or comprehensive secret detection.

See [evidence storage](../architecture/evidence-storage.md) and ADR-014 through ADR-018.

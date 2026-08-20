# Security and trust model

## Security objective

Arbiter is designed to prevent the producer of an AI-generated change from unilaterally defining its authorization, candidate identity, protected controls, validation outcome, evidence integrity, and final approval.

## Trusted authorities

| Authority | Trusted for | Not trusted for |
|---|---|---|
| Human task author | Task objective and delegated scope | Candidate facts or validation result |
| Git repository | Commits, ancestry, and changed paths | Product correctness |
| Policy configuration | Allowed/protected boundaries | Repository mutation |
| Independent validator | Check observations and validation verdict | Human approval or remediation |
| Evidence store | Artifact persistence and integrity verification | Product verdict |
| Orchestrator | Ordering, routing, and invariant enforcement | Reimplementing validation |
| Human reviewer | Final approval or rejection | Rewriting historical records |

## Threats addressed in Phase 1

- Agent claims a different candidate than Git contains
- Agent changes files outside authorization
- Agent changes protected validation or policy
- Agent updates its own tests to conceal a regression
- Remediation fixes one failure while adding another
- Failed candidate or finding disappears after remediation
- Validation checks or findings point to nonexistent evidence
- Evidence artifact, manifest, or audit history is modified or missing
- Approval request targets a stale candidate or validation
- Automated readiness is confused with human approval
- Invalid target is mislabeled as a product failure

## Fail-closed behavior

Arbiter blocks rather than guesses when it encounters wrong target, dirty baseline, missing required checks, command infrastructure failure, invalid candidate ancestry, protected or unauthorized paths, evidence persistence failure, integrity failure, contradictory reconstruction, remediation exhaustion, or stale/duplicate decisions.

## Secret handling

Structured evidence passes through a redaction hook for configured token values and recognized credential fields. Error responses omit raw exceptions, stacks, environment details, and absolute paths. React renders diagnostic content as escaped text.

This is not a comprehensive secret scanner. Operators must not submit secrets, complete environments, hidden model reasoning, or unrelated sensitive files as evidence.

## Authentication boundary

The canonical demo validates bearer-token behavior using exact parsing and timing-safe comparison. This proves protected application behavior; it is separate from Arbiter user authentication.

Phase 1 human actors are asserted non-empty strings. Arbiter does not yet authenticate the reviewer or enforce RBAC. This is the highest-priority Phase 2 trust gap.

## Isolation boundary

Phase 1 enforces logical separation using distinct executor/validator roles and run IDs plus protected ownership. It does not claim cryptographic identity or process/container isolation. Production runners must add disposable workspaces, pinned images, resource limits, network policy, secret isolation, and verifiable runner identity.

## Storage boundary

File-backed evidence is portable and tamper-evident. Filesystem permissions are environmental. Production storage should add tenant isolation, encryption, independent audit durability, retention policy, backup/recovery, and key management.

## Dependency and supply-chain boundary

The policy package detects manifest changes and lockfile inconsistency heuristically. It does not perform package reputation or vulnerability scoring. npm audit and dependency update tooling remain maintenance inputs rather than product verdict authorities.

## Reporting a vulnerability

Do not open a public issue containing exploit details or secrets. Use GitHub's private vulnerability reporting or contact the repository owner through a private channel. Include affected commit, reproduction steps, expected/observed behavior, and whether evidence or authorization boundaries are affected.

The private engineering repository retains the operational `SECURITY.md` and detailed trust-boundary specification; they are intentionally outside this public showcase.

# System architecture

## Design principle

Arbiter separates **change production** from **change acceptance**. No component is allowed to both create a candidate and certify it.

## Component flow

```text
Human task authority
      │
      ▼
TaskAuthorization ───────► Policy and protected paths
      │                              │
      ▼                              ▼
Clean Git baseline ──────► Change Agent executor
                                     │ commit
                                     ▼
                            Read-only Git inspection
                                     │ Candidate
                                     ▼
                            Independent validation
                              │              │
                         ValidationRun     Findings
                              │              │
                              └──────┬───────┘
                                     ▼
                         Evidence + audit persistence
                                     │
                      FAIL ──────────┴────────── PASS
                       │                              │
                 bounded remediation          verify + reconstruct
                       │                              │
                  new Candidate                 READY_TO_APPROVE
                                                      │
                                                      ▼
                                            Human decision command
```

## Architectural layers

### Contracts

`@arbiter/schemas` defines strict runtime objects for authorization, baselines, candidates, validation, findings, evidence, audit events, and approvals. Generated JSON Schemas make the same contracts portable outside TypeScript.

### Domain logic

`@arbiter/core` owns lifecycle invariants and verdict derivation. It does not inspect repositories or persist evidence.

### Repository facts and policy

`@arbiter/git` reads Git without mutation. `@arbiter/policy` combines those facts with authorization and organizational policy. Git facts outrank agent claims.

### Independent validation

`@arbiter/validation` executes a stable check registry. `protected-validation/` contains checks owned outside the demo application. The engine emits results, findings, evidence payloads, and event intents; it does not persist or remediate.

### Evidence authority

`@arbiter/evidence` creates immutable records and hashed artifacts. It verifies integrity but never derives a product verdict.

### Orchestration

`@arbiter/orchestration` sequences execution, binds temporary validator references to durable evidence IDs, routes remediation, reconstructs state, and enforces the human-decision command boundary. It consumes validator verdicts rather than recalculating them.

### Presentation

`@arbiter/arbiter-ui` renders Overview, Change, Validation, Evidence, and History. Read models are derived server-side from persisted records. React never reads the filesystem, derives readiness, or writes approval records directly.

## Source-of-truth rules

| Question | Authority |
|---|---|
| What task was authorized? | `TaskAuthorization` |
| What repository state preceded the work? | `RepositoryBaseline` and Git |
| What exact change is being evaluated? | Candidate commit verified by Git |
| Were changed paths allowed? | Policy evaluation over Git-derived paths |
| Did a check pass? | `ValidationCheck` from the independent validator |
| What is the product validation verdict? | Core verdict logic applied by validation |
| What artifact supports a claim? | Evidence item and manifest |
| Is the run internally intact? | Evidence, audit, and domain verification |
| Is the candidate ready for human review? | Persisted Arbiter verdict |
| Was it approved or rejected? | Immutable human decision record |

## State model

The nominal sequence is:

```text
AUTHORIZED
→ BASELINE_CAPTURED
→ CHANGE_IN_PROGRESS
→ CANDIDATE_READY
→ VALIDATING
→ REMEDIATION_REQUIRED
→ REMEDIATING
→ CANDIDATE_READY
→ VALIDATING
→ READY_TO_APPROVE
```

Wrong target, dirty baseline, infrastructure errors, remediation exhaustion, evidence failure, audit failure, and contradictory persisted state block the run.

## Architectural constraints

- Candidates, validations, findings, evidence, manifests, and approvals are immutable snapshots.
- Every remediation creates a new candidate and complete validation run.
- Protected-path precedence overrides authorization matches.
- Required checks cannot silently disappear.
- Evidence references must resolve within the same run.
- Readiness requires a verified evidence package and audit ledger.
- Approval requires current candidate and validation identities plus immediate integrity reverification.

The private engineering repository retains the full ADR set, trust-boundary specification, and domain model; they are intentionally outside this public showcase.

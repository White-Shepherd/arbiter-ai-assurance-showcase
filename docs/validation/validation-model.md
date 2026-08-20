# Validation model

## Validation classes

Arbiter distinguishes an invalid validation target from a product failure. This prevents a validator pointed at the wrong repository from creating misleading product findings.

| Classification | Meaning |
|---|---|
| `INVALID_VALIDATION_RUN` | Target identity is wrong; only VAL-000 executes |
| `PRODUCT_VALIDATION` | Target is valid and the required product checks execute |

## Runtime registry

The Phase 1 runtime engine executes 15 checks:

| Test | Purpose | Typical severity |
|---|---|---|
| VAL-000 | Validation target identity | Blocking intake |
| VAL-002 | Clean working tree and baseline | Blocking |
| VAL-007 | Candidate commit integrity | HIGH |
| VAL-005 | Authorized scope compliance | Blocking |
| VAL-006 | Protected path enforcement | CRITICAL |
| VAL-015 | Protected-test manipulation | CRITICAL |
| VAL-014 | Dependency policy | HIGH |
| VAL-008 | Build | HIGH |
| VAL-009 | Lint/typecheck | MEDIUM |
| VAL-010 | Unit tests | Blocking |
| VAL-011 | Integration tests | Blocking |
| VAL-012 | Protected API contract | HIGH |
| VAL-013 | Authentication preservation | CRITICAL |
| VAL-016 | Independent validator separation | CRITICAL |
| VAL-019 | Full-revalidation readiness | Blocking |

The complete acceptance catalog defines VAL-000 through VAL-025. Some catalog items are meta-tests or Stream 8 acceptance activities rather than per-candidate runtime checks. For example, VAL-017 evaluates finding quality and VAL-025 is the Stranger Test.

## Execution behavior

- VAL-000 always executes first.
- Wrong identity stops immediately without creating product findings.
- A valid target runs the stable required registry.
- Ordinary candidate defects do not stop subsequent diagnostics.
- A missing required registry entry raises `CHECK_NOT_REGISTERED`.
- A protected check that cannot execute produces blocking ERROR.
- Commands use explicit argument arrays, working directories, and timeouts.
- Protected HTTP service cleanup occurs in `finally`.
- Validation creates results and payloads but does not persist or remediate.

## Verdict derivation

Verdict logic is centralized in `@arbiter/core`:

```text
Any blocking failed/error check or unresolved blocking finding → FAIL
Only non-blocking findings                                  → PASS_WITH_FINDINGS
All required checks pass and no blocking finding           → PASS
```

The trust verdict becomes `READY_TO_APPROVE` only for a valid PASS with no unresolved blocking finding. Validation never produces `APPROVED`.

## Protected validation

Protected validators live outside `apps/demo-service`:

- `protected-validation/api-contract/validator.ts`
- `protected-validation/security/validator.ts`
- `protected-validation/scope/required-paths.json`

The authentication validator independently checks missing token, invalid token, valid token, and public health behavior. Application tests cannot redefine these expectations without also touching a protected control.

## Finding requirements

A material failed check produces a structured finding with:

- Stable finding ID
- Candidate and validation-run IDs
- Severity and blocking state
- Expected and observed behavior
- Why the failure matters
- Repository-relative affected files
- Persisted evidence IDs
- Immutable timestamps and status

The evidence-binding layer rejects missing or duplicate correlation references before persistence.

## Negative-path coverage

Tests cover wrong target, dirty baseline, unauthorized/protected changes, candidate mismatch, protected-check manipulation, remediation regression, remediation exhaustion, infrastructure failure, missing evidence, tampering, contradictory reconstruction, stale decisions, duplicate decisions, and invalid actors.

The private engineering repository retains the machine-readable test catalog and validation-engine contract; they are intentionally outside this public showcase.

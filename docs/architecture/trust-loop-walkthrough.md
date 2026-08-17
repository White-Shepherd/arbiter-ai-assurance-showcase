# Step-by-step Trust Loop

This walkthrough describes the canonical execution order and the authority at each step.

## 1. Authorize

A `TaskAuthorization` names the project, objective, requirements, authorized paths, protected paths, prohibited actions, and required checks. The task cannot broaden organizational policy. Paths unmatched by effective authorization are denied.

## 2. Confirm the validation target

VAL-000 compares expected and observed product identity, repository type, and validation profile. It always runs first. A mismatch yields `INVALID_VALIDATION_RUN / WRONG_VALIDATION_TARGET`, a pending product verdict, and no product findings.

## 3. Capture the baseline

Arbiter reads repository root, branch, HEAD, status, and tracked-file facts. Phase 1 requires a clean baseline. It never cleans, stashes, or resets user work automatically.

## 4. Execute the change producer

The `ChangeAgentExecutor` receives the original authorization, baseline, repository root, mode, and—during remediation—the current candidate and blocking findings. The executor declares whether it is `REAL` or `FIXTURE`. Its statements are recorded but are not candidate truth.

## 5. Derive the candidate from Git

Git inspection verifies commit existence and ancestry, computes changed files and statistics, identifies dependency-file changes, and creates a candidate bound to an immutable commit. A mismatch between claimed and observed commit fails validation.

## 6. Evaluate scope

Policy evaluates every changed path, including the old and new sides of a rename. The precedence is:

```text
PROTECTED > AUTHORIZED > UNAUTHORIZED
```

Protected or unauthorized paths remain violations even if the agent reports success.

## 7. Run full independent validation

The validator executes the stable registry in order. Ordinary product failures do not stop later checks, which preserves diagnostic value. Required checks cannot silently skip; missing registration or infrastructure failure becomes an explicit error.

The canonical first candidate passes ordinary build, lint, unit, integration, contract, scope, integrity, and separation checks. The protected authentication validator independently observes `/api/profile` returning 200 without credentials instead of the required 401.

## 8. Create findings and evidence payloads

Failed checks flow through one deterministic finding factory. Findings contain stable identity, candidate/run bindings, severity, expected and observed behavior, rationale, affected paths, blocking state, and references to supporting runtime payloads.

## 9. Persist immutable records

Orchestration allocates durable evidence IDs, maps every temporary validator reference exactly once, binds checks and findings, then persists artifacts, domain records, and audit events. Missing, duplicate, or dangling references fail closed.

## 10. Route remediation

A blocking product failure routes to remediation under the original authorization. Phase 1 allows at most two automatic remediation iterations. Every attempt creates a new agent run, commit, candidate, validation run, and evidence set.

## 11. Revalidate everything

Candidate 2 reruns the complete 15-check suite. Arbiter does not test only the previously failed check. This guards against remediation that fixes authentication while introducing a different regression.

## 12. Verify evidence and reconstruct state

The evidence manifest, every artifact, audit chronology, and domain record are verified. Reconstruction reads persisted state rather than trusting an in-memory or UI status. Contradictions fail closed.

## 13. Reach readiness

`READY_TO_APPROVE` requires:

- Current immutable candidate
- Final validation bound to that candidate
- Validation verdict PASS
- No open blocking findings for the final validation
- Persisted evidence references
- Verified manifest and audit ledger
- Consistent reconstructed state

The approval snapshot remains `humanDecision: PENDING`.

## 14. Record a human decision

The human-facing command submits exact run, candidate, and validation IDs plus decision, actor, and optional rationale. The server re-resolves current state and reverifies integrity immediately before writing a new immutable approval snapshot and exactly one audit event.

Phase 1 requires a non-empty asserted actor but does not authenticate that identity. Authentication and RBAC are Phase 2 work.

## Reproduce locally

```sh
npm ci
npm run lint
npm run build
npm test
npm run fixture:verify
npm run trust-loop:demo -- RUN-walkthrough
npm run evidence:verify -- RUN-walkthrough
npm run trust-loop:inspect -- RUN-walkthrough
```

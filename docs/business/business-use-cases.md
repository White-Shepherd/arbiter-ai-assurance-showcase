# Business use cases

## Product outcome

Arbiter helps an organization answer: **Should a human trust this exact AI-generated engineering change, and can the organization reconstruct why?**

It does not replace source control, CI, code review, or human release authority. It connects those controls around an immutable candidate and independently preserved evidence.

## Primary users

| User | Need | Arbiter value |
|---|---|---|
| Platform engineering | Standardize how AI changes are authorized and validated | Versioned task boundaries, stable validation profiles, reproducible runs |
| Application security | Protect security behavior outside the change agent's control | Protected validators, protected paths, fail-closed findings |
| Engineering leadership | Increase AI development velocity without weakening release controls | Bounded remediation and evidence-backed readiness |
| Developer productivity | Give coding agents a clear path from task to reviewable candidate | Explicit scope, deterministic failure feedback, immutable candidate history |
| Risk and governance | Reconstruct who changed what, what was tested, and why a decision was made | Portable evidence, manifests, audit chronology, human-decision records |
| Release reviewer | Approve or reject the exact validated candidate | Freshness checks, integrity reverification, explicit human boundary |

## CI-green security regression

An AI agent modifies an authenticated endpoint and updates application-owned tests so CI remains green. An independent protected validator observes that an unauthenticated request now returns HTTP 200 instead of 401.

Arbiter binds validation to the candidate, runs protected checks outside application-owned tests, creates a blocking evidence-linked finding, routes remediation under the original authorization, creates a new candidate, reruns the complete suite, and retains the failed history after the new candidate passes.

This is the canonical Phase 1 demonstration.

## Scope containment for agent changes

A task author allows changes under `apps/service/**` while protecting validation and policy directories. Arbiter derives changed paths from Git rather than the agent's claim. Unauthorized and protected changes become blocking results, including both sides of a rename.

Business value: teams can delegate implementation without silently delegating authority to broaden the task.

## Controlled automated remediation

A candidate fails a blocking check. Arbiter passes the original authorization and relevant findings to a remediation executor, limits automatic iterations, creates a distinct candidate for every attempt, and reruns the full validation suite.

Business value: remediation can remain fast without converting an autonomous loop into an unbounded release authority.

## Evidence-backed human approval

An automated run reaches `READY_TO_APPROVE`. A reviewer submits an approval or rejection against authoritative run, candidate, and validation IDs. Arbiter rechecks freshness, open findings, evidence integrity, and audit integrity before recording the decision.

Business value: the organization can distinguish machine advice from accountable human action.

## Audit and incident reconstruction

After a release or incident, an operator can reconstruct authorization, baseline, candidates, validation history, findings, remediation, evidence, readiness, and human decision from the portable run directory.

Business value: decisions remain explainable even when the original processes are gone.

## Design-partner evaluation

A prospective customer selects one repository, one AI workflow, and one protected control ordinary CI could miss. The pilot measures setup effort, validation time, false-positive burden, remediation clarity, reviewer effort, and evidence usefulness.

The pilot should produce a gap register and deployment recommendation, not a premature enterprise-wide rollout claim.

## Where Arbiter is not the right tool yet

Phase 1 is not a production multi-tenant SaaS platform, identity provider, generic CI replacement, secret scanner, policy marketplace, compliance certification engine, or cryptographic attestation service. These distinctions are part of the product's trustworthiness.

# Mission Control integration roadmap

## Product direction

The intended experience is a single operator entry point: select a program, open its overview, inspect its active AI-agent hierarchy, and deliberately start or intervene in governed work. Primary agents may delegate bounded tasks to sub-agents that use different model providers when the program policy permits it.

This is a future direction, not a description of current product behavior. The validated Mission Control snapshot remains read-only, and this showcase does not claim a completed Arbiter integration.

## Architectural principle

Mission Control should present and request work, an orchestration control plane should execute it, and Arbiter should independently validate consequential outputs. The component that directs an agent must not be the sole authority deciding whether that agent's work is trustworthy.

```text
Mission Control operator interface
             │
     intent + human authority
             ▼
Governed orchestration control plane
      ┌──────┼────────┐
      ▼      ▼        ▼
 primary  primary   primary agents
  agent    agent     agent
   │                   │
   ├─ sub-agent/model A└─ sub-agent/model C
   └─ sub-agent/model B
             │
       candidates + events
             ▼
Arbiter independent assurance
             │
 evidence + findings + readiness
             ▼
Mission Control + human decision
```

## Core contracts

### Program

A program is the top-level operating boundary. It identifies repositories, environments, policies, budgets, allowed model providers, protected resources, responsible humans, and the agent definitions authorized to participate.

### Agent definition

An agent definition declares its role, instructions, tools, accessible resources, model policy, delegation permissions, concurrency limit, budget, and required assurance gates. Runtime agent instances reference an immutable definition version.

### Delegation

Every parent-to-child delegation should be an explicit record containing the parent instance, bounded objective, authorized inputs and paths, allowed tools and models, budget, deadline, expected outputs, and completion state. Sub-agents receive no ambient authority from their parent beyond that record.

### Model adapter

Provider-specific APIs should sit behind a common adapter contract for invocation, streaming, cancellation, usage, tool calls, and normalized errors. Model selection is policy-driven and recorded per invocation so a run remains reconstructable even when agents use different providers.

### Run and evidence event

The control plane emits append-only lifecycle events. Arbiter consumes candidate and evidence references through a versioned contract, performs independent validation, and returns findings and readiness without becoming the task scheduler.

## Operator experience

The program overview should answer five questions immediately:

1. What programs and runs need attention?
2. Which agents and sub-agents are active, blocked, waiting, or complete?
3. Which models, tools, budgets, and authorities are they using?
4. What evidence supports the reported state?
5. Where is a human decision or intervention required?

Starting an agent should require a deliberate launch dialog showing objective, scope, model policy, budget, tool access, approval gates, and expected evidence. Pause, cancel, retry, and reassign controls should operate on the control plane—not directly on provider processes from the browser.

## Delivery sequence

### Phase 1 — Shared read model

- Define versioned program, agent, delegation, run, evidence, finding, and approval schemas.
- Add a read-only adapter that maps Arbiter evidence into Mission Control provenance models.
- Display agent hierarchies and assurance state using deterministic fixtures before connecting execution.
- Preserve the current `OBSERVED`, `DERIVED`, `DEMO`, and `UNAVAILABLE` semantics.

Exit criterion: one program overview reconstructs the same read-only state from versioned fixtures and real Arbiter evidence.

### Phase 2 — Governed single-agent launch

- Introduce an authenticated local control-plane service separate from the GET-only observer API.
- Add RBAC, idempotent commands, audit events, budgets, cancellation, and explicit approval gates.
- Launch one primary agent through one model adapter with no delegation.
- Route its candidate to Arbiter and return findings to Mission Control.

Exit criterion: a human can launch, observe, stop, validate, and reconstruct one bounded agent run without granting the browser direct execution authority.

### Phase 3 — Hierarchical multi-model delegation

- Add versioned agent definitions and bounded parent-child delegation records.
- Support multiple model adapters under program policy.
- Enforce depth, fan-out, concurrency, cost, time, tool, and repository limits.
- Visualize the agent tree and surface blocked or over-budget branches.

Exit criterion: every sub-agent action traces to a parent delegation, policy decision, model invocation, evidence set, and final disposition.

### Phase 4 — Operational hardening

- Add remote identity, secrets management, tenant isolation, durable queues, recovery, and observability.
- Threat-model prompt injection, confused-deputy delegation, credential leakage, runaway recursion, provider failure, and compromised evidence producers.
- Add policy simulation, emergency stop, retention controls, and independent security testing.

Exit criterion: the control plane meets an explicitly documented deployment assurance target; it is not promoted solely because the demonstration workflow succeeds.

## Non-negotiable controls

- Human authority for consequential approvals.
- Immutable agent-definition and policy versions per run.
- Explicit delegation boundaries; no inherited ambient credentials.
- Depth, concurrency, time, token, and monetary limits.
- Provider and model identity recorded for every invocation.
- Idempotent commands and append-only audit events.
- Independent Arbiter validation of exact candidates and material evidence.
- Visible partial, stale, unavailable, and contradictory states.
- A program-level emergency stop that prevents new work and cancels authorized active work.

## First implementation slice

The smallest credible integration slice is not a fully autonomous agent swarm. It is one program, one repository, one primary agent, one model adapter, one launch command, one cancellation path, and one Arbiter validation result displayed in Mission Control. Building this vertical slice first proves the contracts and authority boundaries that hierarchical multi-model agents will depend on.

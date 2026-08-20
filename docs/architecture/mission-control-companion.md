# Mission Control companion observability

## Purpose

Mission Control is a separate, read-only observability interface for repository-driven, multi-agent engineering workflows. It helps an operator inspect projects, current runs, findings, artifacts, agents, lessons, standards, governance recommendations, activity, logs, and source provenance without turning the dashboard into an orchestration or approval authority.

Mission Control is not part of Arbiter's Phase 1 Trust Loop implementation. No direct Harbor Ridge or Arbiter integration is claimed in this showcase. The systems share assurance principles—authoritative evidence, explicit provenance, preserved history, and human authority—but retain separate repositories, contracts, and security boundaries.

## Current capabilities

- Deterministic Demo Mode for a clearly labeled synthetic workflow.
- Live Local Mode for explicitly allowlisted repositories.
- A loopback-only, GET-only local API.
- A read-only GitHub collector for configured repositories.
- Normalized project, run, finding, artifact, agent, lesson, standard, governance, activity, and log views.
- Provenance that distinguishes `OBSERVED`, `DERIVED`, `DEMO`, and `UNAVAILABLE` information.
- Partial and unavailable states that retain usable evidence without silently substituting Demo data.
- Refresh behavior that observes external fixture changes without restarting the reader.
- Responsive navigation, keyboard-accessible dialogs, visible source state, and disabled live governance controls.

## Architecture

```text
Mission Control UI
        │
MissionControlDataProvider
        │
ProjectDataService
   ┌────┴───────────┐
Demo provider   Local API provider
                       │
              GET-only API client
                       │
             Application service
               ┌───────┴────────┐
       Local providers     GitHub collector
          │
  path security + parsers
          │
 authoritative repository evidence
```

The presentation layer consumes canonical Mission Control models. Environment selection, Demo data, Live Local aggregation, HTTP transport, application routing, filesystem providers, path security, and provenance construction are separate boundaries.

## Read-only security boundary

Mission Control accepts logical project IDs resolved through a server-owned allowlist. The path boundary rejects traversal, encoded traversal, absolute paths, drive switching, UNC paths, and canonical junction or symlink escape.

The local API binds to loopback, supports GET only, and rejects mutation methods. Source files are opened read-only. Browser-facing failures omit absolute paths, stack traces, and raw filesystem errors.

Mission Control cannot start or resume a real run, execute an agent, modify a repository, approve a governance recommendation, or record an Arbiter human decision.

## Validation profile

The current repository-controlled validation profile covers:

- 31 automated tests;
- 13 representative GET routes;
- 52 rejected `POST`, `PUT`, `PATCH`, and `DELETE` attempts;
- zero fixture mutations during representative API reads;
- lint, type check, and production build;
- fixture freshness after an external state change;
- Demo, healthy Live Local, partial, and unavailable source states;
- path-boundary, provenance, provider, API, and UI lifecycle contracts.

These results validate the repository-controlled synthetic profile. They do not represent a production deployment, authenticated multi-user environment, or completed Arbiter integration.

## Deliberate limits

- No write API or runner control.
- No authentication, RBAC, or remote multi-user access.
- No automatic approval or governance mutation.
- No direct Arbiter or Harbor Ridge integration in the published scope.
- No claim that a hosted browser can access a workstation loopback API.
- No replacement for source control, CI, independent validation, or human release authority.

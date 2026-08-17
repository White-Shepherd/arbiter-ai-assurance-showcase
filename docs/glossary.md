# Glossary

| Term | Meaning |
|---|---|
| Agent Run | One identified INITIAL_CHANGE or REMEDIATION execution by a real or fixture change executor |
| Arbiter verdict | Automated trust advice, currently `READY_TO_APPROVE` or `NOT_READY` |
| Approval Record | Immutable snapshot binding candidate, validation, evidence manifest, Arbiter verdict, and human decision |
| Authorization | Human-defined objective, requirements, allowed paths, protected paths, prohibited actions, and required checks |
| Baseline | Clean repository state and commit captured before change execution |
| Candidate | Immutable Git-derived description of a proposed commit and its changed files |
| Evidence Item | Immutable metadata plus an exact hashed artifact |
| Evidence Manifest | Deterministic index binding all evidence artifacts to a run |
| Finding | Structured diagnostic tied to a candidate, validation run, affected paths, and evidence |
| Full validation | Execution of the complete required registry, including after remediation |
| Human decision | Explicit `PENDING`, `APPROVED`, or `REJECTED` state, separate from the Arbiter verdict |
| Protected control | Validation or path authority the change agent is not allowed to modify or own |
| Stranger Test | Independent reproduction using repository-local instructions and artifacts |
| Trust Loop | Authorization → baseline → candidate → validation → evidence/remediation → readiness → human decision |
| Validation Run | Immutable set of check results and findings for one candidate |

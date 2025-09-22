# Phase 0 — Program Spin-Up & Foundations Checklist

| Field | Details |
| --- | --- |
| **Timeline** | Weeks 0–2 |
| **Dependencies** | None |
| **Phase Gate** | Governance council kickoff review |
| **Objective** | Establish governance, infrastructure, and planning artifacts that enable execution of the REFRACTOR program. |

## Workstreams & Tasks

### Governance & Operating Model
- [ ] Ratify the program charter covering scope, metrics, decision forums, and escalation paths. *(Draft: `inbox/Phase_0_Program_Charter.md`)*
- [ ] Approve the RACI matrix for architecture, infrastructure, retrieval, MoE, safety, and program management roles. *(Draft: `inbox/Phase_0_Governance_RACI.md`)*
- [ ] Publish recurring ceremonies (standups, phase reviews, risk triage, calibration syncs) with calendar invites. *(Schedule: `inbox/Phase_0_Governance_Ceremony_Schedule.md`)*
- [ ] Stand up a shared documentation space referencing `specification/` artifacts and program glossary. *(Plan: `inbox/Phase_0_Governance_Documentation_Space.md`)*
- [ ] Collect stakeholder approvals (engineering, research, product, safety) on charter, RACI, and ceremony cadence. *(Tracking: `inbox/Phase_0_Governance_Approvals_Log.md`)*

### Engineering Foundations
- [ ] Initialize repository layout (src/, tests/, tools/, docs/) with coding standards and contribution guidelines.
- [ ] Configure formatting, linting, type-check tooling, and security scanners aligned with target implementation languages.
- [ ] Implement CI pipelines executing formatting, lint, unit-test smoke suite, artifact build, and docs link checks.
- [ ] Provision secrets management and environment configuration templates for local and CI execution.
- [ ] Create baseline telemetry ingestion (metrics/logging exporters) verifying heartbeat metrics reach monitoring stack.

### Planning, Risk, & Finance
- [ ] Build work breakdown structure linked to phases, owners, and estimates.
- [ ] Seed backlog tickets for Phase 1 scope with story sizing, dependencies, and acceptance criteria.
- [ ] Establish risk register capturing top technical, scheduling, and operational risks with mitigation owners.
- [ ] Stand up SLA dashboard skeleton covering latency, availability, retrieval precision, and safety metrics.
- [ ] Define budget tracking cadence (compute, storage, tooling) with finance sign-off.

### Change Management & Communications
- [ ] Document inbox/outbox workflow policy and communicate to teams.
- [ ] Publish communication plan (async updates, decision logs, stakeholder readouts) aligned with governance cadence.
- [ ] Configure collaboration tooling (issue tracker projects, shared whiteboards, chat channels) with access controls.
- [ ] Archive onboarding materials (architecture primer, spec map) in documentation space.

## Validation & Telemetry
- [ ] CI pipelines run automatically on merge requests with clean baseline results.
- [ ] Telemetry exporters verified by sending test metrics and confirming dashboards ingest signals.
- [ ] Risk register reviewed during weekly triage with mitigation status captured.

## Exit Criteria
- [ ] CI pipelines pass on baseline repository build and test invocations.
- [ ] Governance artifacts (charter, RACI, ceremonies) formally approved by stakeholders.
- [ ] SLA dashboard skeleton populated with placeholder signals from telemetry heartbeat.
- [ ] Phase 1 checklists reviewed, signed off, and stored in `inbox/` for execution.
- [ ] Inbox/outbox workflow documented, communicated, and trialled with sample checklist move.
- [ ] Checklist archived to `outbox/` with link to supporting artifacts after approval.

# Phase 0 — Program Spin-Up & Foundations Checklist

**Timeline:** Weeks 0–2  
**Dependencies:** None  
**Objective:** Establish governance, infrastructure, and planning artifacts that enable execution of the REFRACTOR program.

## Governance & Operating Model
- [ ] Draft program charter outlining scope, success metrics, decision forums, and escalation paths. *(Draft: `inbox/Phase_0_Program_Charter.md`)*
- [ ] Produce RACI matrix covering architecture, infrastructure, retrieval, MoE, safety, and program management roles. *(Draft: `inbox/Phase_0_Governance_RACI.md`)*
- [ ] Schedule recurring ceremonies (standups, phase reviews, risk triage) with calendar invites sent. *(Schedule draft: `inbox/Phase_0_Governance_Ceremony_Schedule.md`)*
- [ ] Stand up shared documentation space referencing `specification/` artifacts and program glossary. *(Plan: `inbox/Phase_0_Governance_Documentation_Space.md`)*
- [ ] Collect stakeholder approvals (engineering, research, product, safety) on charter and RACI. *(Tracking: `inbox/Phase_0_Governance_Approvals_Log.md`)*

## Engineering Foundations
- [ ] Initialize repository structure (src/, tests/, tools/, docs/) consistent with coding standards.
- [ ] Configure formatting, linting, and type-check tooling aligned with target implementation languages.
- [ ] Implement CI pipelines executing formatting, lint, unit-test smoke suite, and artifact build steps.
- [ ] Provision secrets management and environment configuration templates for developers.
- [ ] Create baseline telemetry ingestion (metrics/logging endpoints) verifying heartbeat metrics reach monitoring stack.

## Planning & Risk Management
- [ ] Build comprehensive work breakdown structure linked to phases and owner teams.
- [ ] Populate initial backlog tickets derived from Phase 1 scope with sizing and dependencies.
- [ ] Establish risk register capturing top technical, scheduling, and operational risks with mitigation owners.
- [ ] Draft SLA dashboard skeleton covering latency, availability, retrieval precision, and safety metrics.
- [ ] Document inbox/outbox workflow policy and communicate to teams.

## Exit Criteria
- [ ] CI pipelines pass on baseline repository build and test invocations.
- [ ] Governance artifacts (charter, RACI, ceremonies) formally approved by stakeholders.
- [ ] SLA dashboard skeleton populated with placeholder signals from telemetry heartbeat.
- [ ] Phase 1 checklists reviewed, signed off, and stored in `inbox/` for execution.
- [ ] Archive this checklist to `outbox/` after sign-off with link to supporting artifacts.

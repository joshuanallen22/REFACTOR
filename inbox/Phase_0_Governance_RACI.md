# REFRACTOR Phase 0 RACI Matrix

| Workstream | Task Cluster | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|------------|--------------|-----------------|-----------------|---------------|--------------|
| Governance | Program charter & decision forums | Program Director | Executive Sponsor | Chief Architect, Product Lead, Safety Lead | Steering Committee |
| Governance | RACI maintenance & stakeholder mapping | Program Director | Executive Sponsor | Module Leads, HR Partner | All contributors |
| Governance | Inbox/outbox workflow policy | Program Director | Chief Architect | Ops Lead, QA Lead | All teams |
| Planning | Phase work breakdown structure | Program Director | Chief Architect | Module Leads | Steering Committee |
| Planning | Risk register creation | Safety Lead | Program Director | Retrieval Lead, MoE Lead, Ops Lead | All phase leads |
| Planning | SLA dashboard skeleton | Ops Lead | Program Director | Telemetry Lead, QA Lead | Steering Committee |
| Engineering Foundations | Repo initialization & tooling | Infra & Ops Lead | Chief Architect | QA Lead, Security Lead | Engineering org |
| Engineering Foundations | CI/CD pipeline | Infra & Ops Lead | Chief Architect | QA Lead | All developers |
| Engineering Foundations | Secrets & environment templates | Infra & Ops Lead | Program Director | Security Lead | Engineering org |
| Telemetry | Baseline telemetry ingestion | Telemetry Lead | Ops Lead | Safety Lead | Steering Committee |
| Retrieval | Retrieval precision policy | Retrieval Lead | Chief Architect | Safety Lead, Data Governance | Steering Committee |
| MoE Routing | Router load management policy | MoE Lead | Chief Architect | Program Director, Ops Lead | Steering Committee |
| Safety | Tool/retrieval safety gates | Safety Lead | Program Director | Retrieval Lead, Legal Liaison | All stakeholders |
| Product | Success metrics validation | Product Lead | Program Director | QA Lead, Data Science | Steering Committee |

## Role Definitions
- **Executive Sponsor:** VP Applied Research overseeing budget and strategic alignment.
- **Program Director:** Senior Staff PM orchestrating governance, timeline, and artifact lifecycle.
- **Chief Architect:** Distinguished Engineer accountable for architectural integrity and spec conformance.
- **Infra & Ops Lead:** Staff SWE responsible for developer experience, CI/CD, and operational readiness.
- **Telemetry Lead:** Staff SWE/ML responsible for metrics/logging pipelines.
- **Safety Lead:** Staff Safety Scientist driving safety policies, compliance, and risk mitigation.
- **Retrieval Lead:** Staff ML Engineer owning episodic store and retrieval metrics.
- **MoE Lead:** Staff ML Engineer responsible for expert routing performance and anti-collapse safeguards.
- **Product Lead:** Principal PM validating user value and success metrics.
- **QA Lead:** Staff QA Engineer covering validation suites and regression analysis.
- **Legal Liaison:** Counsel ensuring compliance with policy and privacy requirements.
- **Module Leads:** Phase-specific technical owners (Reframer, Distinction Engine, etc.).

## Maintenance Plan
- Review matrix during Phase Readiness Review; update responsibilities as teams evolve.
- Capture changes in shared documentation space with versioned history.
- Log approvals or updates in `inbox/Phase_0_Governance_Approvals_Log.md`.


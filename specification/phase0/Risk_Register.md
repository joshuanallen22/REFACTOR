# Phase 0 Risk Register

| Risk ID | Category | Description | Impact | Likelihood | Mitigation | Owner | Trigger/Review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | Technical | CI pipeline instability due to immature tooling integrations. | High | Medium | Establish staging pipeline, enforce pre-merge dry runs, and document rollback steps. | Infrastructure Lead | Review after first CI dry run completion. |
| R-002 | Schedule | Delays in charter approval extending beyond Week 1. | Medium | Medium | Pre-brief stakeholders with draft charter, collect async feedback before formal review. | Program Manager | Trigger if approval not secured by Day 5. |
| R-003 | Operational | Secrets management onboarding blocked by security approvals. | High | Low | Use temporary vault namespace with audit logging; escalate to security weekly. | Infrastructure Lead | Trigger if templates not delivered by Week 1. |
| R-004 | Technical | Telemetry heartbeat failing to reach monitoring stack. | Medium | Medium | Implement synthetic heartbeat test and alert; pair telemetry and ops engineers during setup. | Telemetry Lead | Trigger if heartbeat offline >2 hours. |
| R-005 | Dependency | Phase 1 backlog lacks size/dependency clarity causing downstream sprint churn. | Medium | Medium | Conduct joint backlog refinement with architecture and program management; maintain dependency tracker. | Program Manager | Review backlog completeness at Week 1.5. |
| R-006 | Safety | Mask legality tests uncover systemic rule gaps late in Phase 1. | High | Medium | Engage safety team during Phase 0 backlog seeding, add property tests as entry criteria. | Safety Lead | Trigger if safety sign-off missing during backlog review. |
| R-007 | Resource | Key owners over-allocated across phases reducing delivery focus. | Medium | Medium | Create RACI with backup delegates, monitor utilization via weekly sync. | Program Manager | Trigger when owners report >120% allocation. |
| R-008 | External | Vendor telemetry endpoint SLA below requirements. | High | Low | Negotiate contractual SLAs, implement fallback metrics ingestion path. | Ops Lead | Review vendor report weekly. |

## Risk Management Cadence

- Risks reviewed in weekly risk triage; updates captured in this register.
- High-impact risks escalated to program steering committee within 24 hours.
- Mitigation status reflected in sprint demo notes and linked to relevant backlog items.

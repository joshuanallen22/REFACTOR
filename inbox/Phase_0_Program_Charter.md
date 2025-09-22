# REFRACTOR Program Charter

## 1. Purpose
Establish a unified governance and delivery framework for REFRACTOR v1.0 that aligns research, engineering, product, and safety stakeholders around a single sequence architecture roadmap.

## 2. Scope
- **In scope:** Architecture and systems defined in `specification/REFRACTOR_SPEC.md`, implementation phases 0–7, supporting tooling, telemetry, deployment, and operational workflows.
- **Out of scope:** Downstream product integrations beyond initial pilot tenants, third-party marketplace distribution, speculative research unrelated to the v1.0 deliverables.

## 3. Success Metrics
- **Execution:** Each phase checklist exits inbox on schedule with required artifacts stored in outbox and production baselines meeting SLAs.
- **Quality:** Retrieval precision@k ≥ 0.75, router entropy within 0.4–0.8, zero tolerance safety scope breaches in validation environments.
- **Operational:** ≥ 99.9% service availability during canary rollout, telemetry coverage ≥ 95% for required probes, governance actions tracked with <48h latency.

## 4. Decision Forums
| Forum | Cadence | Purpose | Chair | Members |
|-------|---------|---------|-------|---------|
| Steering Committee | Bi-weekly | Resolve cross-phase tradeoffs, approve major scope changes | Program Director | Executive Sponsor, Chief Architect, Retrieval Lead, MoE Lead, Safety Lead, Product Lead |
| Architecture Review Board | Weekly | Review design changes impacting spec-compliant interfaces | Chief Architect | Module Leads, Infra Lead, QA Lead |
| Risk & Compliance Triage | Weekly (or ad-hoc) | Evaluate emerging risks, compliance issues, and incident responses | Safety Lead | Program Director, Legal Liaison, Ops Lead |
| Phase Readiness Review | End of each phase | Validate exit criteria, move artifacts to outbox | Program Director | Steering Committee |
| Budget & Capacity Sync | Monthly | Track spend, hiring, and vendor dependencies | Program Director | Finance Partner, Team Leads |

## 5. Escalation Paths
1. **Operational blockers (<24h impact):** Notify Ops Lead and Program Director via incident channel; escalate to Steering Committee if unresolved within 1 business day.
2. **Spec deviations:** Raise with Architecture Review Board; if urgent, Program Director may call emergency session.
3. **Safety/retrieval policy breaches:** Immediate notification to Safety Lead, suspend affected capabilities, convene Risk & Compliance Triage.
4. **Resource conflicts:** Program Director mediates between teams; unresolved conflicts escalate to Executive Sponsor.
5. **Budget overruns:** Program Director informs Executive Sponsor and Finance; mitigation plan due within 3 business days.

## 6. Roles & Responsibilities
| Role | Primary Owner | Responsibilities |
|------|---------------|------------------|
| Executive Sponsor | VP Applied Research | Funding oversight, unblock strategic escalations |
| Program Director | Senior Staff PM | Own roadmap, governance artifacts, inbox/outbox hygiene |
| Chief Architect | Distinguished Engineer | Maintain spec integrity, approve architecture deviations |
| Retrieval Lead | Staff ML Engineer | Own episodic store, retrieval precision metrics |
| MoE Lead | Staff ML Engineer | Ensure router efficacy, manage expert parallelism |
| Safety Lead | Staff Safety Scientist | Safety masks, tool gating, risk register maintenance |
| Infra & Ops Lead | Staff SWE | CI/CD, telemetry, deployment SLO compliance |
| Product Lead | Principal PM | Align user requirements, define success criteria |
| QA & Validation Lead | Staff QA Eng | Run evaluation suites, regression gates |
| Finance Partner | Finance Manager | Track spend, ensure budget adherence |

## 7. Timeline & Milestones
- **Phase 0 completion:** Governance artifacts approved, CI scaffolding live, risk register baselined.
- **Phase 1 kickoff:** Reframer/tokenization backlog ready; dependencies cleared.
- **Phase 3 checkpoint:** MoE routing/regret instrumentation validated in staging.
- **Launch target:** Phase 7 exit with production readiness sign-off.
- **Quarterly refresh:** Roadmap and budget review aligning with telemetry learnings.

## 8. Communication Plan
- Weekly status reports distributed to Steering Committee and archived in shared space.
- Daily async standup updates in #refactor-standup channel; blockers flagged.
- Monthly executive summary for leadership, focusing on metrics and risks.
- Dedicated risk updates channel for high-severity items with <4h response expectation.

## 9. Governance Artifacts Lifecycle
1. Draft artifact in inbox directory referencing specification sections.
2. Review and annotate within shared documentation space with tracked comments.
3. Capture approvals in `inbox/Phase_0_Governance_Approvals_Log.md`.
4. Upon exit criteria satisfaction, move finalized artifact to `outbox/` with immutable version tag and change log.

## 10. Change Control
- Maintain decision log enumerating approved deviations from spec with rationale and mitigation.
- Require dual sign-off (Program Director + relevant domain lead) for scope changes impacting timeline or SLAs.
- Perform retro for any emergency change within 5 business days, logging corrective actions in inbox/outbox system.

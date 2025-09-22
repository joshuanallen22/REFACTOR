# Phase 3 — Transformation Core & Mixture-of-Experts Checklist

| Field | Details |
| --- | --- |
| **Timeline** | Weeks 10–14 |
| **Dependencies** | Phase 2 relation fabric, retrieval integration |
| **Phase Gate** | Core model readiness review |
| **Objective** | Implement attention blocks, FFN/MoE layers, and routing policies with observability and safety controls. |

## Workstreams & Tasks

### Attention & Block Structure
- [ ] Implement pre-norm attention blocks with residual connections mirroring spec sequencing.
- [ ] Validate RMSNorm implementation with numerical parity tests and μP scaling hooks.
- [ ] Integrate tri-tier attention module from Phase 2 with block scheduling and gating.
- [ ] Add EMA weights path with configuration toggles for evaluation snapshots.

### FFN & MoE Architecture
- [ ] Implement dense FFN baseline and MoE-FFN variant with configurable expert counts and hidden sizes.
- [ ] Build gating network with temperature controls, top-k selection, and load-balancing loss terms.
- [ ] Integrate regret regularization using bandit-style reward tracking per expert.
- [ ] Ensure expert parallelism sharding metadata is captured for deployment tooling.

### Routing & Tool Interfaces
- [ ] Implement router telemetry logging expert usage, entropy, regret, and rejection reasons.
- [ ] Add tool router scaffolding with policy enforcement, budgets, and latency quotas.
- [ ] Provide calibration utilities for router temperature and load balancing parameters.

### Validation & Testing
- [ ] Unit tests for gating selection, load balancing invariants, and regret updates.
- [ ] Numerical parity tests comparing dense vs MoE outputs on canonical fixtures.
- [ ] Integration tests verifying tool router gating respects allow-lists and budgets.

### Documentation & Operations
- [ ] Document configuration surfaces for MoE (experts, top-k, temperatures, loss weights) in `specification/` updates.
- [ ] Provide runbook for diagnosing expert collapse, overloading, or routing starvation.
- [ ] Outline rollback procedures to disable MoE or tool routing under incident response.

## Telemetry & Guardrails
- [ ] Dashboards show router entropy, expert usage distribution, and regret metrics with alert thresholds.
- [ ] Alerts trigger when router entropy leaves 0.4–0.8 band for >1k steps.
- [ ] Tool router instrumentation reports call volume, denial reasons, and latency budgets.

## Exit Criteria
- [ ] Core model stack passes integration tests with MoE enabled and dense fallback validated.
- [ ] Router calibration produces balanced usage across experts under representative workloads.
- [ ] Documentation and runbooks published with approval from reliability and safety stakeholders.
- [ ] Checklist archived to `outbox/` with references to tests, dashboards, and configuration guides.

# Phase 3 — Transformation Core & MoE Routing Checklist

**Timeline:** Weeks 8–14  
**Dependencies:** Phases 0–2  
**Objective:** Build decoder layers with RMSNorm, attention integration, FFN/MoE modules, and router telemetry for specialization and tool routing.

## Decoder Layer Infrastructure
- [ ] Implement configurable layer stack (attention + residual + FFN/MoE) respecting μP scaling defaults.
- [ ] Validate RMSNorm implementation against reference with numerical precision tests.
- [ ] Integrate tri-tier attention modules from Phase 2 via configuration injection.
- [ ] Add support for optional geometric heads with gating toggles and unit coverage.
- [ ] Create profiling harness comparing dense vs. MoE layer latency and memory usage.

## Dense FFN Baseline
- [ ] Implement GELU-based FFN with configurable hidden size and activation checkpointing.
- [ ] Add regression tests ensuring dense FFN parity with pre-existing Transformer baselines.
- [ ] Capture baseline perplexity metrics on pilot dataset for later comparison.

## MoE Implementation
- [ ] Implement expert weights storage with sharding hooks (tensor/expert parallel compatibility).
- [ ] Build top-k gating with temperature control, deterministic tie-breaking, and batching efficiency.
- [ ] Encode load-balancing loss (entropy + KL) and regret regularization with configurable weights.
- [ ] Track router usage EMA, entropy, and regret metrics; export to telemetry with alert thresholds.
- [ ] Ensure expert under/over-utilization triggers mitigation actions in simulation (e.g., temperature adjustment).

## Tool Router (Optional Module)
- [ ] Design tool capability registry with allow-lists, budgets, and latency quotas.
- [ ] Implement tool gating logic integrated with policy loop and telemetry.
- [ ] Create sandboxed execution stubs and failure handling pathways for unsupported tools.
- [ ] Validate safety gating prevents unauthorized tool triggers in adversarial tests.

## Testing & Validation
- [ ] Develop unit tests covering top-k stability, load balancing, and regret updates across random seeds.
- [ ] Run dense vs. MoE evaluation comparing perplexity, throughput, and expert utilization (≤2% quality regression).
- [ ] Stress router entropy to <0.2 and >0.9 in simulations; confirm alerts fire and mitigation scripts execute.
- [ ] Document configuration templates enabling dense-only fallback and MoE-enabled modes.

## Exit Criteria
- [ ] Decoder layers pass CI unit/integration suites including geometric head toggles.
- [ ] Router telemetry dashboards show stable usage distribution with alerting validated.
- [ ] Benchmark report demonstrating dense vs. MoE tradeoffs approved by architecture lead.
- [ ] Tool router (if enabled) passes safety review or is explicitly deferred with rationale documented.
- [ ] Checklist archived to `outbox/` with references to benchmarks, dashboards, and approvals.

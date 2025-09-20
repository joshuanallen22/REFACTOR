# Phase 5 — Training Stack & Optimization Checklist

**Timeline:** Weeks 16–24  
**Dependencies:** Phases 0–4  
**Objective:** Deliver end-to-end training pipeline, data processing, evaluation suites, and monitoring aligned with REFRACTOR objectives.

## Data Pipeline
- [ ] Implement ingestion framework supporting multi-source datasets with deduplication (MinHash/LSH).
- [ ] Configure quality filters (language ID, perplexity bands, heuristic quality scores) with audit logs.
- [ ] Build curriculum scheduler expanding context lengths (2k → 8k → 128k) and mixing retrieval tasks.
- [ ] Set up domain mixing via temperature sampling; validate distribution against targets.
- [ ] Automate data validation tests ensuring schema compliance and provenance tracking.

## Training Orchestration
- [ ] Implement training CLI reading YAML configs (Section 12.1) with overrides for scale tests.
- [ ] Integrate optimizer (AdamW/Adafactor) with warmup + cosine decay schedule satisfying Robbins–Monro criteria.
- [ ] Add mixed-precision support (bf16) with FP32 master weights and dynamic loss scaling if needed.
- [ ] Configure gradient clipping (global norm 1.0) and checkpointing with EMA weights.
- [ ] Implement auxiliary losses for retrieval precision, router load balance/regret, safety conformance, and long-range tasks.

## Parallelism & Scaling
- [ ] Provide launcher scripts for tensor, expert, and pipeline parallelism across multi-node clusters.
- [ ] Validate activation checkpointing and gradient accumulation parameters for memory efficiency.
- [ ] Benchmark throughput vs. scaling factor to determine optimal parallel configuration.
- [ ] Document hardware requirements and scaling limits for training phases.

## Evaluation & Testing
- [ ] Develop regression suite covering perplexity benchmarks, retrieval precision@k, long-range tasks, and safety tests.
- [ ] Automate evaluation runs triggered nightly and on major merges with report generation.
- [ ] Ensure telemetry captures optimization metrics (loss, grad norm, LR), router usage, retrieval precision, and safety counters.
- [ ] Establish alerting for instability (NaNs/overflows, loss spikes, entropy collapse) with pager routing.

## Monitoring & Dashboards
- [ ] Build dashboards for SLA metrics (latency, retrieval precision, safety incidents) sourced from training telemetry.
- [ ] Integrate with SLA dashboard skeleton from Phase 0; confirm metric availability and retention.
- [ ] Provide drill-down views for MoE expert utilization and retrieval guard rejections.

## Documentation & Handover
- [ ] Write operator runbooks for launching, monitoring, and pausing training jobs.
- [ ] Document evaluation dataset provenance and access controls.
- [ ] Produce troubleshooting guide for common training failures (instability, divergence, throughput regression).

## Exit Criteria
- [ ] Pilot end-to-end training run completes without instability; logs captured and reviewed.
- [ ] Evaluation suite gates merges via CI and reports archived with checklist.
- [ ] SLA dashboards populated with live training metrics and alert tests validated.
- [ ] Auxiliary losses converge to target ranges documented in specification Appendix B.
- [ ] Checklist archived to `outbox/` including runbooks, benchmark reports, and evaluation artifacts.

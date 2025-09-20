# Phase 2 — Relation Fabric & Retrieval Pipeline Checklist

**Timeline:** Weeks 5–10  
**Dependencies:** Phases 0–1  
**Objective:** Implement tri-tier attention backbone and retrieval services integrated with distinction outputs and guard policies.

## Attention Backbone
- [ ] Implement sliding/dilated/local attention kernels with configurable window, stride, and dilation parameters.
- [ ] Add dense parity tests comparing sparse kernels against reference attention on small contexts (≤2k tokens).
- [ ] Integrate grouped/multi-query projections with configuration-driven head sharing.
- [ ] Provide benchmarking harness measuring throughput/memory for 4k, 16k, and 64k contexts.
- [ ] Document kernel configuration options and scaling tradeoffs in developer docs.

## Global Summary Modules
- [ ] Implement summary token generation (mean, max, attention pooling) per block with projection layers.
- [ ] Validate summary participation as keys/values through integration tests with local attention.
- [ ] Ensure summaries respect mask constraints and segment boundaries.
- [ ] Capture telemetry on summary utilization (attention weights, entropy) and expose dashboards.

## Retrieval Cross-Attention
- [ ] Build retrieval KV projection path consuming episodic records into attention layers.
- [ ] Enforce precision thresholds (`sigma_min`, `trust_min`, `t_max_s`) with rejection logging.
- [ ] Implement guard policies (allow lists, copy/tool permissions) affecting cross-attention masks.
- [ ] Create integration tests combining retrieval results with token streams verifying mask conformance.
- [ ] Instrument telemetry for retrieval call budgets, precision@k, and rejection reasons.

## Memory Backends (Phase 2 scope)
- [ ] Implement episodic store service with ANN index (HNSW/IVF) and filter predicates.
- [ ] Stub schema memory API to support upcoming safety workflows.
- [ ] Provide data ingestion and pruning jobs honoring TTL and provenance constraints.
- [ ] Develop load tests simulating concurrent upsert/search workloads.

## Tooling & Interfaces
- [ ] Expose REST/gRPC endpoints for retrieval `search` and `upsert` with authentication hooks.
- [ ] Generate API documentation and usage examples for downstream teams.
- [ ] Automate deployment manifests (Helm/Terraform) for retrieval services in staging.

## Exit Criteria
- [ ] Attention kernels achieve ≤1e-5 relative error versus dense baseline and benchmarks captured for 4k/16k/64k contexts.
- [ ] Retrieval precision@k on labeled fixtures meets or exceeds configured threshold; reports stored with checklist.
- [ ] Guarded retrieval integration tests confirm disallowed sources/tool invocations are blocked.
- [ ] Telemetry dashboards for attention entropy, retrieval precision, and call budgets live with alert thresholds tested.
- [ ] Checklist archived to `outbox/` following architecture review sign-off.

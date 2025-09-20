# Phase 4 — Memory System & Long-Term Stores Checklist

**Timeline:** Weeks 12–18  
**Dependencies:** Phases 0–3  
**Objective:** Deliver KV Cache++, episodic memory, and schema store with compression, TTL enforcement, and safety-controlled writes.

## KV Cache++
- [ ] Implement chunking strategy with configurable chunk size, compression ratio, and eviction policy.
- [ ] Encode compression codec (FP16 + blockwise quantization) with accuracy benchmarks (≤1e-3 relative error).
- [ ] Integrate cache API (`put`, `get`, `compress`) with decoder stack and ensure compatibility with linear attention switch.
- [ ] Simulate long-context inference verifying cache hit rates and eviction stability.
- [ ] Instrument telemetry for cache utilization, compression ratio, and latency; add alerts on degradation.

## Episodic Store
- [ ] Implement persistent ANN index (HNSW/IVF) with support for upsert, search, and prune operations.
- [ ] Enforce precision filters: cosine similarity threshold, provenance trust floor, source allow-list, and TTL.
- [ ] Build ingestion pipeline for retrieval records, including provenance signature verification.
- [ ] Provide background jobs for TTL expiration, low-trust pruning, and compaction.
- [ ] Develop integration tests ensuring retrieval outputs obey policy filters.

## Schema Memory
- [ ] Design deterministic key-value schema with JSON validation and TTL handling.
- [ ] Implement safety controller gating writes with audit logging.
- [ ] Create API for scoped reads/writes ensuring tool and safety masks align with policy.
- [ ] Test concurrent write scenarios for conflict detection and rollback.

## Integration & Observability
- [ ] Run end-to-end tests combining cache, episodic store, and schema memory during long-context generation.
- [ ] Validate telemetry dashboards for cache hit rates, compression error, retrieval recall, and schema write approvals.
- [ ] Ensure failover procedures for memory subsystems are documented and rehearsed.
- [ ] Update incident response playbooks to include memory-system specific diagnostics.

## Exit Criteria
- [ ] Cache simulations meet memory footprint target (≤0.7 GB per layer per 4k tokens) and results recorded.
- [ ] Episodic store passes precision/retention test suite with audit logs retained.
- [ ] Schema memory write path approved by safety/governance reviewers with signed records.
- [ ] Integrated memory telemetry dashboards operational with alert tests captured.
- [ ] Checklist archived to `outbox/` with benchmark data, audit logs, and documentation links.

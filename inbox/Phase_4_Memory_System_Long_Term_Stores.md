# Phase 4 — Memory System & Long-Term Stores Checklist

| Field | Details |
| --- | --- |
| **Timeline** | Weeks 14–18 |
| **Dependencies** | Phases 1–3 ingestion, attention, routing |
| **Phase Gate** | Memory system operational review |
| **Objective** | Build KV Cache++, episodic store, and schema memory with compression, policy enforcement, and observability. |

## Workstreams & Tasks

### KV Cache++
- [ ] Implement hierarchical chunking with compression ratio configuration and blockwise quantization.
- [ ] Provide APIs for put/get operations with chunk ID tracking and rope state persistence.
- [ ] Build cache eviction policies with telemetry on hit rate, compression error, and chunk age.
- [ ] Validate compatibility with streaming and batch inference modes.

### Episodic Store
- [ ] Stand up vector database (HNSW/IVF-Flat) with embedding dimension alignment to model outputs.
- [ ] Implement upsert/search/prune endpoints with TTL, trust, and source filters enforced.
- [ ] Add background maintenance jobs (index rebuild, compaction, trust decay) with monitoring.
- [ ] Integrate retrieval precision filters with audit logging for rejected records.

### Schema Memory
- [ ] Implement deterministic key-value store with TTL, scope tagging, and policy checks for writes.
- [ ] Build safety controller enforcing approvals before schema memory updates.
- [ ] Provide change log and rollback mechanisms for schema entries.

### Telemetry & Operations
- [ ] Expose metrics for cache compression ratio, hit rate, eviction reasons, and error bounds.
- [ ] Monitor episodic store latency, precision, stale record counts, and policy rejects.
- [ ] Track schema memory write attempts, approvals, and violation alerts.

### Documentation & Runbooks
- [ ] Document memory interfaces, retention policies, and compression codecs in `specification/` addenda.
- [ ] Provide operational guide for cache eviction tuning, episodic index maintenance, and schema memory audits.
- [ ] Outline incident response for memory corruption or policy breach events.

## Validation & Telemetry
- [ ] Round-trip tests verify KV compression error ≤ 1e-3 relative on representative tensors.
- [ ] Integration tests confirm episodic search honors filters and returns precision within targets.
- [ ] Schema memory policy tests enforce approvals and deny unauthorized writes.

## Exit Criteria
- [ ] Memory system interfaces integrated with model serving paths and retrieval pipeline.
- [ ] Telemetry dashboards live for cache, episodic store, and schema memory metrics with alerting.
- [ ] Documentation reviewed by infra and safety stakeholders.
- [ ] Checklist archived to `outbox/` with references to APIs, dashboards, and runbooks.

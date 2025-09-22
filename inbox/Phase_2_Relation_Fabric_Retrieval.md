# Phase 2 — Relation Fabric & Retrieval Enablement Checklist

| Field | Details |
| --- | --- |
| **Timeline** | Weeks 6–10 |
| **Dependencies** | Phase 1 ingestion, telemetry baseline |
| **Phase Gate** | Model architecture review |
| **Objective** | Deliver tri-tier attention fabric with retrieval fan-in, precision controls, and observability hooks. |

## Workstreams & Tasks

### Attention Topology
- [ ] Implement configurable local/sparse backbone supporting window, dilation, stride, and pattern parameters per layer.
- [ ] Build global summary generation (pooling heads) with projection into shared attention context.
- [ ] Integrate retrieval cross-attention module with gating by precision thresholds and max fan-in.
- [ ] Provide fallbacks to linear/kernelized attention when context exceeds `L_switch` with parity tests on small cases.

### Retrieval Integration
- [ ] Implement episodic store API (upsert/search/prune) with HNSW or IVF-Flat index configuration.
- [ ] Encode precision filters (similarity, trust, age, source allow-list) and enforce at query time with unit tests.
- [ ] Build guarded retrieval pipeline returning policy-compliant results and telemetry on filter rejects.
- [ ] Instrument retrieval latency, precision@k, and rejection reasons in telemetry stream.

### Masking & Safety Alignment
- [ ] Extend mask compiler to generate retrieval and safety scope masks for retrieved spans.
- [ ] Add constrained decoding hooks preventing unsafe token generation within safety scopes.
- [ ] Validate retrieval payload tagging integrates with policy enforcement and downstream routers.

### Telemetry & Diagnostics
- [ ] Log attention entropy per tier, retrieval precision histograms, and mask utilization metrics.
- [ ] Build dashboards correlating retrieval calls with acceptance, rejection, and similarity scores.
- [ ] Configure alerts when precision@k drops below thresholds or retrieval latency exceeds budgets.

### Documentation & Change Control
- [ ] Document configuration interfaces for attention topology, retrieval filters, and linear-mode switches.
- [ ] Provide migration guidance for adding new retrieval sources or mask classes.
- [ ] Record troubleshooting guide for common retrieval failures (index desync, low precision, policy rejection).

## Validation & Telemetry
- [ ] Unit tests cover mask compiler retrieval classes and constrained decoding invariants.
- [ ] Integration suite exercises retrieval fan-in with synthetic and labeled datasets measuring precision.
- [ ] Performance benchmarks validate attention kernels across supported context lengths.

## Exit Criteria
- [ ] Architecture review approves relation fabric and retrieval integration design.
- [ ] Telemetry dashboards demonstrate stable retrieval precision@k and attention entropy within guardrails.
- [ ] Documentation published with upgrade procedures and change log.
- [ ] Checklist archived to `outbox/` with links to tests, dashboards, and API references.

# Phase 1 — Reframer, Tokenization & Distinction Engine Checklist

| Field | Details |
| --- | --- |
| **Timeline** | Weeks 2–6 |
| **Dependencies** | Phase 0 foundations |
| **Phase Gate** | Architecture + safety design review |
| **Objective** | Deliver ingestion pipeline converting requests into validated token streams with masks, gating features, and telemetry. |

## Workstreams & Tasks

### Reframer Service
- [ ] Finalize JSON schemas for inbound requests, roles, and constraint metadata with example fixtures.
- [ ] Implement schema validation with descriptive error reporting and golden-path/negative tests.
- [ ] Encode constraint extraction logic (tool budgets, safety flags, retrieval policies) with coverage on boundary cases.
- [ ] Build protocol tag parser translating annotations into role + mask hints and persistence metadata.
- [ ] Expose reframer API endpoints with OpenAPI documentation and contract tests.

### Tokenizer / Codec
- [ ] Select base vocabulary and implement extensible tokenizer supporting reserved protocol tokens and reversible byte alignment.
- [ ] Provide encode/decode APIs with fuzz tests ensuring round-trip safety for UTF-8 payloads and binary attachments (stubs for image/audio).
- [ ] Integrate tokenizer stats logging (token counts, segmentation) into telemetry stream.
- [ ] Benchmark tokenization throughput across representative document sizes and capture regression guardrails.

### Distinction Engine
- [ ] Implement RoPE configuration (theta, scaling) with regression tests for extrapolation accuracy.
- [ ] Build role embedding module with fixtures for default role set and extensibility tests.
- [ ] Develop mask compiler pipeline ingesting YAML rules, generating per-class tensors, and ensuring deterministic builds.
- [ ] Create property-based tests ensuring no illegal edges for causal, segment, tool, safety, and retrieval scopes.
- [ ] Validate gating feature propagation into downstream routers with integration tests touching retrieval/tool routers.

### Telemetry & Alerting
- [ ] Emit mask entropy, invalid edge counts, and role distribution metrics to monitoring stack with dashboards.
- [ ] Configure alert thresholds for mask entropy collapse (<0.1 median) and invalid edge spikes, verifying notifications.
- [ ] Track tokenizer throughput, schema error rates, and average request size in operations dashboards.

### Documentation & Change Management
- [ ] Document configuration knobs (YAML) for roles, mask classes, gating features, and RoPE parameters in `specification/` updates.
- [ ] Provide developer guide for extending protocol tags and adding modalities.
- [ ] Capture runbook for troubleshooting schema validation failures, mask compiler errors, and telemetry anomalies.

## Validation & Telemetry
- [ ] Integration tests demonstrate zero illegal mask edges and correct role propagation across fixtures.
- [ ] Load test to confirm ingestion pipeline sustains target throughput without schema error regressions.
- [ ] Telemetry dashboards show live mask entropy and invalid edge metrics with alerts validated in dry run.

## Exit Criteria
- [ ] Architecture and safety reviewers approve reframer and tokenizer APIs with schema samples.
- [ ] Performance benchmarks meet throughput targets and regressions checked into CI.
- [ ] Documentation published in shared space with change log for subsequent phases.
- [ ] Checklist archived to `outbox/` with links to docs, tests, and dashboards upon approval.

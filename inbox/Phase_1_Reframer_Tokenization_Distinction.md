# Phase 1 — Reframer, Tokenization & Distinction Engine Checklist

**Timeline:** Weeks 2–6  
**Dependencies:** Phase 0 foundations  
**Objective:** Deliver ingestion pipeline converting requests into validated token streams with masks, gating features, and telemetry.

## Reframer Service
- [ ] Finalize JSON schemas for inbound requests, roles, and constraint metadata.
- [ ] Implement schema validation with descriptive error reporting and golden fixtures.
- [ ] Encode constraint extraction logic (tool budgets, safety flags, retrieval policies) with unit coverage.
- [ ] Build protocol tag parser translating annotations into role + mask hints.
- [ ] Expose reframer API endpoints with contract tests and OpenAPI documentation.

## Tokenizer / Codec
- [ ] Select base vocabulary and implement extensible tokenizer supporting reserved protocol tokens.
- [ ] Provide reversible encode/decode ensuring byte-aligned round-trips for UTF-8 payloads.
- [ ] Add hooks for optional image/audio stubs with placeholder unit tests.
- [ ] Integrate tokenizer stats logging (token counts, segmentation) into telemetry stream.
- [ ] Benchmark tokenization throughput across representative document sizes.

## Distinction Engine
- [ ] Implement RoPE configuration (theta, scaling) with regression tests for extrapolation accuracy.
- [ ] Build role embedding module with fixtures for default role set and extensibility tests.
- [ ] Develop mask compiler pipeline ingesting YAML rules, generating per-class tensors.
- [ ] Create property-based tests ensuring no illegal edges for causal, segment, tool, safety, and retrieval scopes.
- [ ] Validate gating feature propagation into downstream routers with integration tests.

## Telemetry & Alerting
- [ ] Emit mask entropy, invalid edge counts, and role distribution metrics to monitoring stack.
- [ ] Configure alert thresholds for mask entropy collapse (<0.1 median) and invalid edge spikes.
- [ ] Dashboard ingestion metrics (requests/min, schema errors, tokenization latency) with drill-downs.

## Documentation & Handover
- [ ] Document configuration knobs (YAML) for roles, mask classes, and gating features in `specification/` updates.
- [ ] Provide developer guide for extending protocol tags and adding modalities.
- [ ] Capture runbook for troubleshooting schema validation failures and mask compiler errors.

## Exit Criteria
- [ ] Integration tests demonstrate zero illegal mask edges and correct role propagation across fixtures.
- [ ] Telemetry dashboards show live mask entropy and invalid edge metrics with alerts validated in dry run.
- [ ] Reframer and tokenizer APIs approved by architecture and safety reviewers.
- [ ] Performance benchmarks meet throughput targets and regressions checked into CI.
- [ ] Checklist archived to `outbox/` with links to docs, tests, and dashboards upon approval.

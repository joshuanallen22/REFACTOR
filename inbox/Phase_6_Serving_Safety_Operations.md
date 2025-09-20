# Phase 6 — Serving, Safety Enforcement & Operations Checklist

**Timeline:** Weeks 20–28  
**Dependencies:** Phases 0–5  
**Objective:** Harden system for production inference with safety enforcement, deployment automation, and operational readiness.

## Serving Infrastructure
- [ ] Implement REST APIs (`/v1/generate`, retrieval admin endpoints) with authentication, rate limiting, and schema validation.
- [ ] Integrate KV Cache++ for streaming inference with fallback to linear attention beyond `L_switch`.
- [ ] Build batching/streaming controllers for interactive and batch serving modes.
- [ ] Containerize serving stack with reproducible builds and supply-chain attestations.
- [ ] Develop infrastructure-as-code (Terraform/Helm) for staging and production clusters.

## Safety & Policy Enforcement
- [ ] Implement constrained decoding enforcing safety masks and forbidden token lists.
- [ ] Integrate retrieval kill-switch and tool gating automation triggered by telemetry thresholds.
- [ ] Conduct adversarial prompt tests covering schema violations, tool misuse, and retrieval poisoning scenarios.
- [ ] Establish incident response workflows for safety breaches, including automatic disable mechanisms.
- [ ] Audit logging for tool calls, retrieval decisions, and safety interventions with retention policy.

## Performance & Reliability
- [ ] Execute latency benchmarks across serving modes (interactive, batch, ultra-long) on reference hardware (8×H100).
- [ ] Validate memory footprint per layer per 4k tokens meets ≤0.7 GB target under load.
- [ ] Implement autoscaling policies based on request rate, latency, and GPU utilization.
- [ ] Run chaos and failover drills (node loss, retrieval outage, tool service unavailability).

## Telemetry & Observability
- [ ] Finalize production dashboards covering latency, throughput, error rates, retrieval precision, and safety events.
- [ ] Integrate alert routing to on-call rotations with runbooks for each alert class.
- [ ] Verify PII scrubbing in telemetry payloads and compliance with privacy requirements.
- [ ] Ensure logs/metrics are exportable via Prometheus/OpenTelemetry endpoints documented in runbooks.

## Documentation & Operational Readiness
- [ ] Produce runbooks/playbooks for deployments, rollback, calibration, and incident response.
- [ ] Conduct readiness review with cross-functional stakeholders (infra, safety, product, support).
- [ ] Train support staff on API usage, rate limits, and troubleshooting flows.
- [ ] Prepare customer-facing changelog and SLA documentation referencing production metrics.

## Exit Criteria
- [ ] P95 latency ≤30 ms/token achieved on target hardware; benchmark report approved.
- [ ] Safety kill-switch and retrieval/tool disable flows validated during drills with logs retained.
- [ ] Operations review sign-off recorded with runbooks/playbooks version-controlled.
- [ ] Production monitoring and alerting tested end-to-end with paging confirmations.
- [ ] Checklist archived to `outbox/` with links to readiness review notes, benchmark data, and incident drill reports.

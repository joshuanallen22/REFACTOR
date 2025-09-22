# SLA Dashboard Skeleton

| Metric Category | Metric | Target | Placeholder Data Source | Notes |
| --------------- | ------ | ------ | ----------------------- | ----- |
| Latency | P95 end-to-end inference latency | ≤ 450 ms | Telemetry heartbeat (synthetic) | Replace with production metrics in Phase 6 |
| Availability | Request success rate | ≥ 99.5% | Heartbeat success ratio | Define alert at 99.0% |
| Retrieval Precision | Precision@k for retrieval responses | ≥ 0.85 | Placeholder fixture results | Integrate with retrieval service in Phase 2 |
| Safety | Tool invocation compliance rate | ≥ 0.98 | Synthetic compliance log | Align with safety enforcement in Phase 6 |
| Telemetry | Mask entropy within bounds | 0.2 ≤ H ≤ 0.9 | Mask entropy stub | Derived from Distinction Engine metrics |

## Dashboard Hosting Plan
- Hosted in observability platform with program-level access controls.
- Metrics updated via CI-driven data pushes until live telemetry is available.
- Alert routing configured to #refactor-ops channel and on-call rotation.

# SLA Dashboard Skeleton

This skeleton defines the initial layout and placeholder metrics for the REFRACTOR program SLA dashboard. Placeholder data sources use telemetry heartbeat exporters until production signals are available.

## Dashboard Tabs

1. **Latency & Availability**
   - Widgets:
     - P50/P95 request latency (ms) by request type.
     - Weekly uptime percentage with SLO target (≥99.5%).
   - Data Source: Telemetry heartbeat synthetic span (`telemetry.heartbeat.latency`).
   - Alerts: Slack channel `#refractor-ops` when P95 > target for 2 consecutive intervals.

2. **Retrieval Precision**
   - Widgets:
     - Precision@k trend (k=5, 10) with threshold line (≥0.92).
     - Retrieval call budget utilization (% of daily quota).
   - Data Source: Placeholder counter `telemetry.heartbeat.retrieval_precision` seeded at 0.90.
   - Alerts: PagerDuty on-call when precision falls below 0.88 for >30 minutes.

3. **Safety Metrics**
   - Widgets:
     - Mask legality violations per 1k requests.
     - Tool usage safety override count.
   - Data Source: Placeholder metric `telemetry.heartbeat.safety_events` seeded at zero.
   - Alerts: Email distribution when violations exceed 0.5/1k for two intervals.

4. **System Health**
   - Widgets:
     - CI pipeline success rate (past 24h).
     - Telemetry heartbeat status indicator.
   - Data Source: CI webhook summary `ci.baseline.success_rate` (placeholder 1.0) and heartbeat boolean.
   - Alerts: Slack notification if CI success <0.9 or heartbeat offline >5 minutes.

## Implementation Notes

- Dashboard hosted in Grafana with folders aligned to program phases.
- Placeholder metrics sourced from heartbeat exporters defined during Phase 0 telemetry setup.
- Each widget annotated with owning team and runbook link (to be populated during Phase 1).
- Dashboard configuration stored as code in `ops/telemetry/dashboard/phase0.json` (to be created in Phase 1).

# Phase 1 Backlog Seed

This backlog translates Phase 1 scope into actionable tickets with preliminary sizing and dependencies. Estimates use t-shirt sizing (S=≤3 days, M=≤1 week, L=≤2 weeks).

| Ticket ID | Summary | Owner Team | Size | Dependencies | Notes |
| --- | --- | --- | --- | --- | --- |
| P1-ING-001 | Implement schema validation for Reframer ingestion service. | Architecture | M | Phase 0 Repo Bootstrap (0.5) | Blocker for ingestion API contract. |
| P1-ING-002 | Build constraint extraction pipeline with rule definitions. | Architecture | M | P1-ING-001 | Requires YAML rule ingestion scaffolding. |
| P1-ING-003 | Implement role tagging component with unit fixtures. | Architecture | S | P1-ING-001 | Shares vocabulary with tokenizer. |
| P1-TOK-001 | Design extensible tokenizer vocabulary configuration. | Infrastructure | M | Phase 0 Tooling Baseline (0.6) | Seeds codec interface. |
| P1-TOK-002 | Implement tokenizer encoder/decoder with text baseline. | Infrastructure | L | P1-TOK-001 | Coordinate with distinction masks. |
| P1-TOK-003 | Add property tests for tokenizer detokenization parity. | Infrastructure | M | P1-TOK-001 | Integrate into CI smoke suite. |
| P1-DST-001 | Implement RoPE positional module with configurable scaling. | Architecture | M | Phase 0 Repo Bootstrap (0.5) | Must align with downstream decoder stack. |
| P1-DST-002 | Build role embedding loader with golden fixtures. | Architecture | S | P1-DST-001 | Dependent on telemetry hooks. |
| P1-DST-003 | Implement mask compiler with YAML rule ingestion and validation. | Architecture | L | P1-DST-001, P1-ING-002 | Ensure support for all mask classes. |
| P1-DST-004 | Add mask legality property tests and invalid edge fixtures. | Safety | M | P1-DST-003 | Telemetry to track violations. |
| P1-TEL-001 | Instrument telemetry hooks for mask entropy and invalid edges. | Telemetry & Ops | S | P1-DST-004 | Feed into SLA dashboard. |
| P1-OPS-001 | Draft deployment checklist for Phase 1 services. | Program Management | S | Phase 0 Inbox/Outbox Policy (0.13) | Stored in `inbox/` pending approval. |

## Backlog Grooming Cadence

- Weekly backlog refinement during Phase 1 standups.
- Story map updated as dependencies resolve; integrate with risk register when blockers persist beyond one sprint.

# REFRACTOR Implementation Program

This phased plan translates the REFRACTOR v1.0 engineering specification into a coordinated implementation roadmap. Each phase ends with a review that moves completed checklists from the `inbox/` (planned/active work) to the `outbox/` (completed artifacts). All specification assets reside in `specification/`. Phase summaries below capture goals, scope, key deliverables, dependencies, validation gates, and governance checkpoints.

## Phase 0 — Program Spin-Up & Foundations (Weeks 0-2)
- **Goals:** Establish governance, environment, and backlog to support the program.
- **Scope:** Form core teams (architecture, infrastructure, retrieval, MoE, safety); stand up repo structure, coding standards, CI/CD scaffolding, telemetry ingestion pipelines; build planning artifacts (work breakdown structure, risk register, SLA dashboard skeleton); define budget and communication cadences.
- **Deliverables:** Program charter, RACI matrix, ceremony schedule, documentation space plan, approvals log, CI baseline with lint/format/type/unit checks, initial telemetry exporters, inbox/outbox operating guide.
- **Dependencies:** None (kick-off phase).
- **Validation & Governance:** CI pipelines green on skeleton builds; telemetry heartbeat visible; governance artifacts approved by stakeholders; risk register reviewed in steering committee; backlog seeded for Phase 1.

## Phase 1 — Reframer, Tokenization & Distinction Engine (Weeks 2-6)
- **Goals:** Implement ingestion pipeline that converts raw requests into token streams with masks and gating features.
- **Scope:** Reframer service (schema validation, constraint extraction, role tagging); tokenizer/codec with extensible vocabulary and reversible byte handling; Distinction Engine modules (RoPE, role embeddings, mask compiler with YAML rule ingestion); telemetry hooks for mask entropy and invalid edge detection; documentation for protocol extensibility.
- **Deliverables:** Reframer/tokenizer libraries, mask compiler with property tests, integration fixtures, OpenAPI definitions, telemetry dashboards for ingestion metrics, updated spec appendices covering configuration knobs.
- **Dependencies:** Phase 0 infrastructure and governance.
- **Validation & Governance:** Integration tests show zero illegal mask edges; load tests confirm ingestion throughput; telemetry dashboards/alerts validated; architecture and safety reviews sign off on APIs; checklist archived to `outbox/` after approvals.

## Phase 2 — Relation Fabric & Retrieval Pipeline (Weeks 6-10)
- **Goals:** Deliver tri-tier attention backbone plus retrieval services integrated with the Distinction Engine.
- **Scope:** Local/sparse attention kernels, global summary modules, retrieval cross-attention, episodic store backend (ANN index with filters), schema memory API skeleton, retrieval guard enforcement, constrained decoding alignment, telemetry counters for precision and latency.
- **Deliverables:** Attention kernel library with dense parity tests, retrieval service with search/upsert/prune APIs, policy enforcement modules, dashboards correlating retrieval calls with acceptance metrics, operations runbook for retrieval incidents.
- **Dependencies:** Phases 0–1 (token/mask availability; CI & telemetry).
- **Validation & Governance:** Attention kernels meet parity thresholds; retrieval precision@k ≥ target on labeled fixtures; safety scopes enforced in integration tests; architecture review approves topology; gating metrics monitored with alerting.

## Phase 3 — Transformation Core & MoE Routing (Weeks 10-14)
- **Goals:** Build decoder stack with RMSNorm, tri-tier attention integration, FFN/MoE modules, routing telemetry, and tool router scaffolding.
- **Scope:** Layer scaffolding with μP scaling compatibility; dense + MoE FFN modules; routing networks with load balancing, regret regularization, and calibration utilities; tool router budgets/policies; telemetry instrumentation for entropy, usage, regret, and tool invocations.
- **Deliverables:** Configurable layer modules, router auxiliary loss implementation with tests, calibration scripts, dashboards for routing metrics, rollback playbooks for disabling MoE/tool routing.
- **Dependencies:** Phases 0–2 (attention modules, masks, retrieval signals).
- **Validation & Governance:** MoE routing passes unit/integration tests; dense vs MoE parity within 2% perplexity on pilot datasets; telemetry alerts verified; safety + architecture sign-off for routing policies.

## Phase 4 — Memory System & Long-Term Stores (Weeks 14-18)
- **Goals:** Implement KV Cache++, episodic memory, and schema store with compression, TTL, and safety policies.
- **Scope:** KV cache chunking/compression APIs, episodic store persistence with precision filters, schema memory CRUD with safety controller, integration with retrieval and serving pipelines, telemetry for cache hit rate/compression error/retention health.
- **Deliverables:** Memory subsystem library with async I/O, compression benchmarks, TTL/pruning automation, operational runbooks, dashboards for cache/episodic/schema metrics.
- **Dependencies:** Phases 0–3 (core model, retrieval services, telemetry).
- **Validation & Governance:** Cache performance meets memory footprint targets; episodic store honors filters; schema memory policy tests pass; operations review approves retention & compliance posture.

## Phase 5 — Training Stack & Optimization (Weeks 18-24)
- **Goals:** Deliver full training pipeline with objectives, data processing, distributed scheduling, and auxiliary losses.
- **Scope:** Data deduplication/filtering/curriculum, optimizer schedules (warmup, cosine decay, gradient clipping), distributed launchers (tensor/expert/pipeline parallel), activation checkpointing, EMA weights, auxiliary objectives (retrieval contrastive, router load balance/regret, safety conformance), telemetry for optimization and routing metrics.
- **Deliverables:** Training CLI/config templates, data governance documentation, monitoring dashboards, hyperparameter sweep automation, regression suite gating merges, incident runbooks for pipeline failures.
- **Dependencies:** Phases 0–4 (model components, telemetry, memory).
- **Validation & Governance:** End-to-end pilot run without instability; KPI dashboards live with alerting; auxiliary losses converge to targets; training readiness review approves go-live.

## Phase 6 — Serving, Safety Enforcement & Operations (Weeks 24-28)
- **Goals:** Harden system for production inference with safety enforcement, deployment automation, and telemetry SLOs.
- **Scope:** Serving modes (interactive, batch, ultra-long) with KV Cache++ integration, API contracts (`/v1/generate`, retrieval admin endpoints), safety enforcement (constrained decoding, allow-lists, kill-switch automation), deployment tooling (containerization, rollout strategy, checkpoint versioning), observability for latency/throughput/memory, incident response playbooks.
- **Deliverables:** Serving binaries/images, infrastructure-as-code for deployment, runbooks and playbooks, automated latency/precision regression benchmarks, customer-facing SLA documentation.
- **Dependencies:** Phases 0–5 (complete model, training outputs, telemetry streams).
- **Validation & Governance:** P95 latency ≤ 30 ms/token on reference hardware; safety drills validate kill-switch and retrieval disable; production readiness review sign-off; operations dashboards/alerts in place; artifacts archived to `outbox/`.

## Phase 7 — Post-Launch Evolution & Versioning (Weeks 28+)
- **Goals:** Operate continuous improvement loop, manage version upgrades, and plan roadmap evolution.
- **Scope:** Versioned interfaces for checkpoints/index formats/KV codecs, experimentation backlog (e.g., geometric heads, modality expansion), telemetry-driven prioritization, customer feedback integration, governance cadence for roadmap updates.
- **Deliverables:** Versioning policy and migration playbooks, experimentation templates with graduation criteria, telemetry review cadence documentation, quarterly roadmap updates.
- **Dependencies:** Successful Phase 6 launch.
- **Validation & Governance:** Baseline SLAs met for sustained production window; change management workflows exercised; governance forums capture decisions/action items; backlog maintained with future-looking initiatives.

---

### Working Lists & Folder Usage
- **`inbox/`** — Active checklists, RFCs, and tasks awaiting completion.
- **`outbox/`** — Completed checklists and approvals archived per phase.
- **`specification/`** — Master specification (`REFRACTOR_SPEC.md`), implementation plan, and related design artifacts.

All new checklists start in `inbox/` and move to `outbox/` during phase exit reviews. Future documents should reference the relevant phase, link to associated telemetry dashboards, and include approval metadata before archiving.

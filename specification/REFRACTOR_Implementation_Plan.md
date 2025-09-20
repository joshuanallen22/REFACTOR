# REFRACTOR Implementation Program

This phased plan translates the REFRACTOR v1.0 engineering specification into a coordinated implementation roadmap. Each phase ends with a review that moves completed checklists from the `inbox/` (planned/active work) to the `outbox/` (completed artifacts). All specification assets reside in `specification/`.

## Phase 0 — Program Spin-Up & Foundations (Weeks 0-2)

**Goals**
- Establish governance, environment, and backlog to support the program.

**Scope**
- Form core teams (architecture, infrastructure, retrieval, MoE, safety).
- Stand up repo structure, coding standards, CI/CD scaffolding, and telemetry ingestion pipelines.
- Build planning artifacts: work breakdown structure, risk register, and SLA dashboard skeleton.

**Deliverables**
- Program charter and RACI matrix (`specification/`).
- CI baseline with lint, formatting, type checks, unit-test harness.
- Initial telemetry exporters capturing heartbeat metrics.

**Dependencies**
- None (kick-off phase).

**Completion Criteria**
- CI pipelines green on skeleton builds.
- Governance artifacts approved by stakeholders.
- Inbox seeded with next-phase checklists.

## Phase 1 — Reframer, Tokenization & Distinction Engine (Weeks 2-6)

**Goals**
- Implement ingestion pipeline that converts raw requests into token streams with masks and gating features.

**Scope**
- Reframer service implementing schema validation, constraint extraction, and role tagging.
- Tokenizer/codec with extensible vocab handling text baseline (image/audio stubs optional).
- Distinction Engine modules: RoPE positioning, role embeddings, mask compiler (with YAML rule ingestion and property tests).
- Telemetry hooks for mask entropy and invalid edge detection.

**Deliverables**
- Library packages for reframer, tokenizer, and mask compiler.
- Property-based tests for mask legality; golden fixtures for role embeddings.
- Deployment checklist in `inbox/`; upon completion archive to `outbox/`.

**Dependencies**
- Phase 0 infrastructure and governance.

**Completion Criteria**
- Conformance tests show zero illegal mask edges and correct role propagation.
- Mask compiler supports all classes (`CAUSAL`, `SEGMENT`, `TOOL_SCOPE`, `SAFETY_SCOPE`, `RET_SCOPE`).
- Telemetry reports operational with alert thresholds defined.

## Phase 2 — Relation Fabric & Retrieval Pipeline (Weeks 5-10)

**Goals**
- Deliver tri-tier attention backbone plus retrieval services integrated with the Distinction Engine.

**Scope**
- Local/sparse attention kernels with sliding/dilated patterns and benchmark harness.
- Global summary generation and projection modules.
- Retrieval cross-attention implementation, including precision threshold enforcement and guard policies.
- Episodic store backend (ANN index with filters), schema memory API skeleton, and retrieval guard service.
- Telemetry counters for retrieval precision, call budgets, and mask conformance.

**Deliverables**
- Attention kernel library with dense parity tests.
- Retrieval service with search/upsert APIs and policy filters.
- Benchmark reports for 4k/16k/64k token contexts.

**Dependencies**
- Phases 0–1 (token/mask availability; CI & telemetry).

**Completion Criteria**
- Attention kernels pass numerical parity (≤1e-5 relative error) on small fixtures.
- Retrieval precision@k on labeled fixtures ≥ configured threshold.
- Guarded retrieval blocks disallowed sources in integration tests.

## Phase 3 — Transformation Core & MoE Routing (Weeks 8-14)

**Goals**
- Build the main decoder stack with RMSNorm, attention integration, FFN/MoE modules, and routing telemetry.

**Scope**
- Layer scaffolding with pre-norm residual flow aligned with μP scaling.
- Dense FFN baseline followed by switchable MoE FFN (top-k routing, load balancing, regret regularization).
- Tool router interface (gating logic, policy budget checks) behind feature flag.
- Router logs and probes (usage, entropy, regret metrics) flowing to telemetry.

**Deliverables**
- Layer modules composable via configuration (YAML-driven).
- Router auxiliary loss implementation with tests for load balancing invariants.
- Simulation harness producing router entropy/usage dashboards.

**Dependencies**
- Phases 0–2 (attention modules, masks, retrieval signals).

**Completion Criteria**
- MoE routing passes unit tests for top-k selection stability and load balancing.
- Dense/MoE parity benchmarks within 2% perplexity on pilot dataset.
- Telemetry alerts firing when entropy leaves [0.2, 0.9] in stress tests.

## Phase 4 — Memory System & Long-Term Stores (Weeks 12-18)

**Goals**
- Implement KV Cache++, episodic memory, and schema store with compression, TTL, and safety policies.

**Scope**
- KV cache chunking, compression codec, and API integration with decoder stack.
- Episodic store persistence, TTL pruning, and provenance enforcement.
- Schema memory CRUD with safety controller hooks.
- Integration tests for cache hit rates, compression error bounds, and retrieval interplay.

**Deliverables**
- Memory subsystem library with async I/O support.
- Compression benchmarks demonstrating ≤1e-3 relative error.
- Automated tests covering TTL pruning and provenance trust filters.

**Dependencies**
- Phases 0–3 (core model, retrieval services, telemetry).

**Completion Criteria**
- Cache performance meets memory footprint targets (≤0.7 GB per layer per 4k tokens in simulations).
- Episodic store passes precision filters and retention policies.
- Schema memory write path validated by safety gating tests.

## Phase 5 — Training Stack & Optimization (Weeks 16-24)

**Goals**
- Deliver full training pipeline with objectives, data processing, and scaling strategies.

**Scope**
- Data ingestion: deduplication, filtering, curriculum scheduler for context expansion.
- Training loop supporting mixed precision, gradient clipping, EMA weights, and MoE/retrieval auxiliaries.
- Evaluation suite (perplexity, retrieval precision, long-range tasks, safety tests).
- Multi-node launcher scripts with tensor/expert/pipeline parallel configurations.

**Deliverables**
- Training CLI and configuration templates (aligned with Section 12.1).
- Monitoring dashboards for losses, entropy, retrieval metrics, and safety counters.
- Regression suite gating merges via CI for representative tasks.

**Dependencies**
- Phases 0–4 (model components, telemetry, memory).

**Completion Criteria**
- End-to-end training run on pilot dataset completes without instability (no NaNs/overflows).
- SLA dashboard populated with live metrics and alert thresholds.
- Retrieval and routing auxiliary losses converge to spec targets.

## Phase 6 — Serving, Safety Enforcement & Operations (Weeks 20-28)

**Goals**
- Harden system for production inference with safety, deployment automation, and telemetry SLOs.

**Scope**
- REST APIs (`/v1/generate`, retrieval admin endpoints) with auth, rate limiting, and schema validation.
- Safety enforcement: constrained decoding, tool gating, retrieval kill-switch automation.
- Deployment tooling: containerization, rollout strategy (canary, traffic shifting), checkpoint management.
- Performance benchmarking across serving modes (interactive, batch, ultra-long) with linear attention switch.

**Deliverables**
- Serving binaries/images ready for staging.
- Runbooks and playbooks (incident response, calibration procedures) stored in `specification/`.
- Automated precision/latency regression benchmarks integrated into CI.

**Dependencies**
- Phases 0–5 (complete model, training outputs, telemetry streams).

**Completion Criteria**
- P95 latency ≤ 30 ms/token in target hardware environment (8×H100 reference).
- Safety kill-switch validated in drills (retrieval disable, tool revoke).
- Production readiness review sign-off; final checklists archived to `outbox/`.

## Phase 7 — Post-Launch Evolution & Versioning (Weeks 28+)

**Goals**
- Establish continuous improvement loop, handling version upgrades and experimentation.

**Scope**
- Versioned interface process for checkpoints, index formats, and KV codecs.
- Experiment backlog (e.g., geometric heads, image/audio modality expansion).
- Impact analysis framework for representation changes and schema migrations.

**Deliverables**
- Versioning policy documentation and migration playbooks.
- Experimentation templates in `inbox/` with graduation criteria.
- Telemetry-driven review cadence (monthly) with guardrail thresholds.

**Dependencies**
- Successful Phase 6 launch.

**Completion Criteria**
- Baseline SLAs met for one month of production traffic.
- Change management workflows exercised on at least one minor upgrade.
- Inbox/outbox workflow routinely used for new initiatives.

---

### Working Lists & Folder Usage

- **`inbox/`** — Active checklists, RFCs, and tasks awaiting completion.
- **`outbox/`** — Completed checklists and approvals archived per phase.
- **`specification/`** — Master specification (`REFRACTOR_SPEC.md`), implementation plan, and related design artifacts.

All new checklists start in `inbox/` and move to `outbox/` during phase exit reviews. Future documents should reference the relevant phase and link to associated telemetry dashboards.

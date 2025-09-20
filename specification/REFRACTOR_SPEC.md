# REFRACTOR v1.0 — Engineering Specification

*A production-ready neural sequence architecture and system, suitable as a successor to Transformers. This document defines components, interfaces, algorithms, data schemas, control policies, metrics, tests, and SLAs. It is self-contained; an engineering team can implement it without additional guidance.*

---

## 0. Scope & Goals

**Objective.** Build a scalable, long-context, retrieval-capable sequence model with controllable specialization (experts/tools), robust memory, and quantitative guardrails for representation changes.
**Primary modalities.** Text (required), images (optional module), audio (optional module).
**Usage.** Pretraining + finetuning + online adaptation; batch and interactive inference.

**Key properties required:**

* Sub-quadratic attention at long context lengths.
* Retrieval-augmented inference with precision/recall controls.
* Mixture-of-Experts (MoE) specialization with anti-collapse controls.
* Short-term and long-term memory with explicit write/read policies.
* Robustness to prompt/protocol format; schema-constrained generation.
* Built-in telemetry for optimization stability and routing/retrieval quality.
* Reconfiguration capability for tokenization/format/schema with impact reports.
* Safety gating for tool calls and retrieval content.

---

## 1. System Architecture Overview

**Top-level pipeline (inference/time-step):**

1. **Reframer**: converts request into internal representation and constraints.
2. **Tokenizer/Codec**: encodes inputs into token IDs and auxiliary tags.
3. **Distinction Engine**: compiles positional encodings, masks, and gating features.
4. **Relation Fabric**: computes read neighborhoods (sparse/local, global summaries, retrieval).
5. **Transformation Core**: attention + MLP/Geometric + MoE writes per position.
6. **Memory System**: updates KV cache; reads/writes episodic/schema stores.
7. **Policy Loop**: collects probes and adapts router/retrieval/schedules (if enabled).

**Top-level training loop:**

* Pretraining (unsupervised or instruction-style).
* Optional preference optimization (e.g., DPO/RL-free objectives).
* Finetuning/adapters; periodic router and retriever calibration.

---

## 2. Data Representations & Schemas

### 2.1 Token Stream

* **Input token record** (per position):

  * `id: int32` — vocabulary index.
  * `pos: int32` — absolute index (0..L-1).
  * `seg: int16` — segment ID (conversation/document section).
  * `role: uint8` — {system, user, assistant, tool, code, data} (configurable enum).
  * `mask_bits: uint32` — bitfield of mask classes (see 3.3).
  * `gate_feat: float32[K_g]` — optional gating features for routers/tools.
  * `aux: map<string, bytes>` — optional per-token metadata (e.g., provenance).

### 2.2 Retrieval Record

* `key: float32[D]` — embedding.
* `val: bytes` — retrieved content payload (UTF-8 text; optional binary).
* `source: string` — source identifier.
* `timestamp: int64` — unix time seconds.
* `provenance: {signature?: bytes, trust: float32 in [0,1]}`.
* `policy: {allow_tools: bool, allow_copy: bool, ttl_s: int32}`.

### 2.3 KV Cache Entry

* `layer: int16`, `head_group: int16`, `chunk_id: int64`
* `K: float16[H, Ck]`, `V: float16[H, Cv]` (grouped or multi-query format)
* `rope_state: optional bytes` (for extrapolation/rescaling states)

### 2.4 Router Log Entry

* `token_pos: int32`
* `gate_logits: float32[E]`, `topk_idx: int32[K]`, `topk_prob: float32[K]`
* `load_norm: float32` — normalized expert load.
* `action: {accepted: bool, reason?: enum}`

---

## 3. Distinction Engine

### 3.1 Positional Encoding

* **Default:** Rotary position embedding (RoPE) with base parameter `θ_base`.
* **Context extension:** RoPE scaling factor `α ∈ (0, 1]` for extrapolation.
* **Config:**

  * `d_model: int`
  * `rope_theta_base: float` (e.g., 1e6)
  * `rope_scaling_alpha: float` (e.g., 0.75 for extension)
  * `rope_dim: int` (≤ d_model)

### 3.2 Token Roles & Protocol Tags

* Role vocabulary configurable via JSON.
* Role embeddings: `E_role ∈ R^{|roles| × d_model}` added to token embeddings.
* Protocol tags (e.g., `<tool:calc>`) compiled into `role` + `mask_bits`.

### 3.3 Mask Compiler

* Accepts a set of **mask rules**; outputs per-token binary masks per class:

  * Classes: `CAUSAL`, `SEGMENT`, `TOOL_SCOPE`, `SAFETY_SCOPE`, `RET_SCOPE`.
* Mask rules format (YAML):

  ```yaml
  - name: tool_scope
    when:  role == "tool"
    allow_read_from: ["system", "user", "assistant"]
    allow_write_to: ["assistant"]
    causal: true
  ```
* Compiler produces attention mask tensors:

  * `M_attn ∈ {0, -∞}^{L×L}` additive mask (broadcast per head).
  * `M_role ∈ {0, -∞}^{L×L}` role constraint mask.
  * Final mask: `M_total = M_attn + M_role + M_class_bits`.

---

## 4. Relation Fabric

### 4.1 Attention Topology (Tri-tier)

**(A) Local/Sparse Backbone**

* Patterns: sliding window `w`, dilation `d`, stride `s`.
* Complexity: O(L·w) per layer.
* Parameterization per layer:

  * `window: int` (e.g., 512)
  * `dilation: int` (1 default)
  * `stride: int` (1 default)
  * `pattern: enum {sliding, dilated, block, hybrid}`

**(B) Global Summaries**

* Summarize blocks of `B` tokens into `S` summary tokens via pooling-attention head.
* Per-layer options:

  * `block_size: int` (e.g., 128)
  * `summaries_per_block: int` (1–4)
  * `summary_type: enum {mean, max, attn_pool}`
  * Summaries participate as additional keys/values for all tokens.

**(C) Retrieval Cross-Attention**

* Retrieval fan-in `R` per step (0..R_max).
* Cross-attention keys/values computed from retrieved records.
* Guarded by **precision threshold** (see 7.3).
* Per-layer or per-block insertion points (configurable).

### 4.2 Multi-/Grouped-Query Attention (MQA/GQA)

* Keys/values shared across head groups:

  * `num_heads: H`, `num_kv_heads: H_kv` with `H_kv ≤ H`.
* Projections:

  * `Q: R^{L × H × Cq}`, `K: R^{L × H_kv × Ck}`, `V: R^{L × H_kv × Cv}`.
* **Complexity reduction:** memory ~ O(L·H_kv·(Ck + Cv)).

### 4.3 Linear/Kernalized Attention Mode (optional)

* Kernel feature map `ϕ(x)`; compute `Attn(Q,K,V) = ϕ(Q)(ϕ(K)^T V)`.
* Enabled when `L > L_switch`.
* Provide two kernels: elu+1, FAVOR+.

---

## 5. Transformation Core

### 5.1 Block Structure (per layer)

1. **Pre-Norm** (RMSNorm)
2. **Attention** (tri-tier)
3. **Residual Add**
4. **Pre-Norm**
5. **MLP or MoE-FFN** (gated)
6. **Residual Add**

### 5.2 RMSNorm

* `y = x * (a / sqrt(mean(x^2) + ε))`, learnable scale `a`.
* Default `ε = 1e-6`.

### 5.3 FFN / MoE-FFN

* **Dense FFN:** `GELU(W2 * GELU(W1 * x))`.
* **MoE-FFN:**

  * `E` experts; top-`k` routing (`k = 2` default).
  * Gating: `softmax(W_g x)` with temperature `τ_g`.
  * Load-balancing loss: `λ_lb * (H(P_gate) + ||usage - 1/E||^2)`.
  * **Regret regularization:** maintain per-expert bandit estimates; add penalty when persistent underutilization occurs.
* **Expert shapes:**

  * `d_hidden = 4 * d_model` (dense), `≈ 2.5–3.5×` for MoE experts acceptable.

### 5.4 Geometric Heads (optional)

* **Hyperbolic or graph attention** modules for hierarchical data.
* Toggle per layer via config:

  * `geo_head: {type: "hyperbolic", curvature: -1.0}`

### 5.5 μP Scaling & EMA

* Parameterization compatible with μP (base width multipliers defined).
* Exponential moving average (EMA) of weights for eval:

  * `ema_decay = 0.999–0.9999`.

---

## 6. Memory System

### 6.1 KV Cache++

* Hierarchical chunks of size `C` tokens; compress older chunks to `r` ratio.
* API:

  * `put(layer, chunk_id, K, V, rope_state?)`
  * `get(layer, range) -> list<chunk>`
  * Compression codec: FP16 + blockwise quantization (per 64 elements).

### 6.2 Episodic Store (Vector DB)

* Embedding dimension `D_embed`.
* ANN index with HNSW or IVF-Flat; persistent on disk.
* API:

  * `upsert(doc_id, key[D], val, source, timestamp, provenance, policy)`
  * `search(query[D], k) -> list<RetrievalRecord>`
  * `prune(predicate)` (e.g., TTL or low trust)
* **Precision filters:** min cosine similarity `σ_min`, allow-list by `source`, max age `T_max`.

### 6.3 Schema Memory (Key–Value)

* Deterministic map for structured facts,

  * `put(key_str, value_json, ttl_s, scope)`
  * `get(key_str) -> value_json?`
* Writes only permitted through safety-checked controller.

---

## 7. Retrieval & Safety

### 7.1 Retrieval Pipeline

1. Build query embedding from current hidden states (learned projection).
2. Execute ANN `search(q, k)`, apply filters:

   * `cos(q, key) ≥ σ_min`
   * `timestamp ≥ now - T_max`
   * `source ∈ allow_list`
   * `provenance.trust ≥ t_min`
3. Rank by similarity; select top-`R`.
4. Project retrieved values into cross-attention K/V.

### 7.2 Safety Masks

* Retrieved spans receive **safety scope** masks:

  * Forbid writing to certain roles; forbid tool invocation tokens if not whitelisted.
* Constrained decoding (beam/sampling restricted away from unsafe tokens within scope).

### 7.3 Precision Targets

* During training and eval:

  * `precision@k ≥ p_min` on labeled retrieval tasks.
  * Penalize fetches below `σ_min` or with rejected provenance.

---

## 8. Routing (MoE & Tools)

### 8.1 MoE Router

* Top-`k` selection with `k ∈ {1,2,4}` (default 2).
* Load balancing:

  * Running usage `u_e = EMA(count_e / total_tokens)`.
  * Loss `L_lb = λ1 * KL(u_e || 1/E) + λ2 * entropy(gate)`.
* **Bandit Regret:**

  * Maintain expert reward estimates from token-level validation loss improvement.
  * Add `λ_regret * (regret_e)` to loss when an expert is over/under-selected relative to reward.

### 8.2 Tool Router (optional module)

* Similar gating for tool calls (calculator/code execution/DB).
* Policies:

  * allow-lists by domain.
  * budget per request (max tool calls).
  * latency quotas.

---

## 9. Training

### 9.1 Objectives

* **Language modeling:** next-token cross-entropy.
* **Instruction tuning:** supervised next turn/action.
* **Retrieval auxiliary:** contrastive loss on query–doc pairs; precision@k targets.
* **Routing auxiliary:** load balance + regret regularization.
* **Safety:** mask-conformance loss (penalize illegal cross-scope attention/outputs).
* **Long-range tasks:** synthetic and real tasks requiring >80% of signal beyond local window.

### 9.2 Optimization

* Optimizer: AdamW or Adafactor.
* Schedules:

  * Warmup `5k–20k` steps; cosine decay to floor `lr_min`.
  * Robbins–Monro-style: ensure decays sum to ∞ while squares sum < ∞ (piecewise approximation acceptable).
* Gradient clipping: global norm `1.0`.
* Mixed precision: bfloat16 recommended; FP32 master weights.

### 9.3 Data

* Deduplication (MinHash/LSH).
* Quality filtering (language ID, perplexity bands, heuristic quality).
* Domain mixing with temperature scaling.
* Curriculum: progressive context (`L = 2k → 8k → 128k`), inject retrieval tasks throughout.

### 9.4 MoE & Retrieval Training

* MoE experts sharded (tensor + expert parallel).
* Router auxiliary losses scaled to maintain target entropy.
* Retrieval trained with in-loop negatives (hard negative mining per batch).

---

## 10. Inference & Deployment

### 10.1 Serving Modes

* **Interactive:** single-turn or streaming generation with KV Cache++.
* **Batch:** offline scoring with fixed maximum latency window.
* **Ultra-long:** switch to linear attention mode when `L > L_switch`.

### 10.2 Latency/Memory Targets (reference)

* Decoder-only model, `d_model=4096`, `H=32`, `H_kv=8`, `L=32k`:

  * P95 token latency: ≤ 30 ms/token on 8×H100.
  * Memory per layer per 4k tokens: ≤ 0.7 GB (w/ GQA).
* Retrieval call budget:

  * ≤ 2 calls / 256 tokens, each `k ≤ 10`.

### 10.3 Checkpointing

* Periodic EMA snapshots.
* Router and retriever states versioned separately.
* KV compression codec versioned (backward-compatible decode).

---

## 11. Telemetry & Probes

**Mandatory per-batch logs:**

* Optimization: loss, grad-norm, LR, β1/β2 effective.
* Attention: per-layer attention entropy (mean/std), fraction of masked edges activated.
* Routing: expert usage `u_e`, entropy, regret metrics.
* Retrieval: precision@k on labeled batches, similarity histograms, rejection counts by filter.
* Memory: KV compression ratio, cache hit rates, chunk eviction stats.
* Stability: overflow/NaN counters, activation outlier rates.

**Alert thresholds (examples):**

* Router entropy < 0.2 or > 0.9 for 1k steps → alert.
* Retrieval precision@k < target for 3 evals → disable retrieval until re-calibrated.
* Attention entropy collapse (< 0.1 median) → reduce sparsity or increase summaries.

---

## 12. APIs

### 12.1 Configuration (YAML)

```yaml
model:
  d_model: 4096
  n_layers: 48
  n_heads: 32
  n_kv_heads: 8
  ffn: {type: "moe", experts: 64, topk: 2, hidden: 12288}
  norm: {type: "rmsnorm", eps: 1e-6}
  rope: {theta: 1000000.0, alpha: 0.75, dim: 4096}
relation:
  local: {window: 512, pattern: "sliding"}
  global: {block_size: 128, summaries_per_block: 2, type: "attn_pool"}
  retrieval: {fan_in: 8, sigma_min: 0.45, t_max_s: 604800, trust_min: 0.6}
  linear_mode: {enabled: true, L_switch: 65536, kernel: "elu+1"}
memory:
  kv: {chunk: 512, compress_ratio: 0.5}
  episodic: {embed_dim: 1536, index: "hnsw", M: 32, efSearch: 64}
router:
  gate_temp: 1.0
  lb: {lambda_ent: 0.01, lambda_kl: 0.05}
  regret: {lambda: 0.02, horizon: 1024}
safety:
  masks: [ ... rules ... ]
  constrained_decoding: {enabled: true, max_bad_tokens: 0}
train:
  optimizer: {type: "adamw", lr: 2.0e-4, beta1: 0.9, beta2: 0.95, wd: 0.1}
  schedule: {warmup_steps: 8000, cosine: {min_lr: 1.0e-5}}
  grad_clip: 1.0
  mixed_precision: "bf16"
```

### 12.2 Inference

* `POST /v1/generate`

  * Request:

    ```json
    {
      "inputs": [{"role": "system", "content": "..."}, {"role":"user","content":"..."}],
      "max_tokens": 512,
      "temperature": 0.7,
      "top_p": 0.9,
      "tools": [{"name":"calc"}],
      "retrieval": {"enabled": true, "k": 6}
    }
    ```
  * Response:

    ```json
    {
      "output": "text...",
      "usage": {"prompt_tokens": 1234, "completion_tokens": 512},
      "telemetry": {"retrieval_calls": 2, "precision_at_k": 0.83}
    }
    ```

### 12.3 Retrieval Index

* `POST /v1/retrieval/upsert` — batch ingestion.
* `POST /v1/retrieval/search` — returns records with filters applied.

### 12.4 Admin

* `GET /v1/metrics` — exposes telemetry streams (Prometheus/OpenTelemetry).
* `POST /v1/router/calibrate` — triggers bandit re-estimation.
* `POST /v1/retrieval/calibrate` — adjusts `sigma_min` to hit precision targets.

---

## 13. Algorithms (pseudocode)

### 13.1 Tri-tier Attention (per layer)

```python
def tri_tier_attention(X, mask_total, cfg):
    # Precompute summaries
    S = global_summaries(X, cfg.global)  # [L/B * S, d_model]
    # Local sparse attention
    Y_local = sparse_attention(X, X, X, mask_total.local, cfg.local)
    # Retrieval cross-attention (optional)
    if cfg.retrieval.enabled:
        K_ret, V_ret = retrieval_kv(X)  # shape [R, d_k], [R, d_v]
        Y_ret = cross_attention(X, K_ret, V_ret, mask_total.ret)
    else:
        Y_ret = 0
    # Global summaries cross-attention
    K_glob, V_glob = project(S)
    Y_glob = cross_attention(X, K_glob, V_glob, mask_total.global)
    return Y_local + Y_glob + Y_ret
```

### 13.2 MoE Routing (token-wise)

```python
def moe_ffn(X, experts, gate_w, k, state):
    logits = X @ gate_w.T      # [L, E]
    p = softmax(logits / state.temp)
    topk = top_k(p, k)         # indices and probs
    Y = 0
    loads = zeros(E)
    for i, (idxs, probs) in enumerate(zip(topk.idx, topk.prob)):
        y_i = 0
        for e, w in zip(idxs, probs):
            y_i += w * experts[e](X[i])
            loads[e] += 1
        Y[i] = y_i
    state.update_usage(loads)
    return Y, aux_losses(loads, p, state)
```

### 13.3 Retrieval Guard

```python
def guarded_retrieval(query, k, policy):
    cand = index.search(query, k_max=policy.k_max)
    filt = [r for r in cand
            if cos(query, r.key) >= policy.sigma_min
            and now()-r.timestamp <= policy.t_max_s
            and r.source in policy.allow_list
            and r.provenance.trust >= policy.trust_min]
    return filt[:policy.k]
```

---

## 14. Evaluation & Testing

### 14.1 Unit & Integration

* Mask compiler: property tests (no illegal edges).
* Attention kernels: numerical parity vs dense on small cases.
* Router: load balancing invariant tests; regret counters update correctly.
* Retrieval: filter predicates enforced; precision/recall on fixtures.
* Memory: KV compression roundtrip error ≤ 1e-3 relative on norms.

### 14.2 Performance

* Throughput/latency benchmarks per context length (4k, 16k, 64k, 128k).
* Memory footprint per layer; VRAM allocation stable (no fragmentation growth).

### 14.3 Quality

* Perplexity on standard corpora.
* Instruction task suites (accuracy/F1).
* Long-range tasks (needle-in-haystack variants, multi-hop QA).
* Retrieval precision@k and ablations (with/without retrieval).
* MoE efficiency: tokens-per-second vs dense with matched quality.

### 14.4 Robustness & Safety

* Schema conformance tests (no cross-scope leakage).
* Tool misuse prevention (negative prompts).
* Retrieval poisoning tests (simulated low-trust sources rejected).

---

## 15. Deployment & Ops

### 15.1 Parallelism

* Tensor parallel for projections/MLP.
* Expert parallel for MoE layers.
* Pipeline parallel across blocks.
* Activation checkpointing for memory control.

### 15.2 Rollout

* Canary routing (small traffic slice).
* Telemetry SLO gates: if router entropy or retrieval precision falls below thresholds, auto-disable MoE or retrieval per-request until next calibration.

### 15.3 Logging & Privacy

* PII scrubbing on telemetry payloads.
* Provenance kept in hashed form where required.

---

## 16. Configuration Limits & Defaults

* `d_model`: 1024–8192 (default 4096)
* `n_layers`: 24–80 (default 48)
* `n_heads`: 16–64 (default 32)
* `n_kv_heads`: 4–16 (default 8)
* `context_max`: 32k–256k (default 64k; linear mode beyond 64k)
* `experts`: 16–128 (default 64)
* `topk`: 1–4 (default 2)
* `retrieval.k`: 0–16 (default 8)
* `sigma_min`: 0.35–0.6 (default 0.45)

---

## 17. SLAs & SLOs (reference targets)

* **Availability:** 99.9% monthly.
* **Latency (P95):** ≤ 30 ms/token (interactive target model), ≤ 300 ms/query for retrieval calls.
* **Quality:** Retrieval precision@k ≥ 0.75 on labeled eval; router entropy 0.4–0.8 window.
* **Safety:** 0 tolerance for schema violations in protected scopes; automated kill-switch on breach.

---

## 18. Deliverables & Artifacts

* **Core library** implementing modules in sections 3–7.
* **Training scripts** with configs in 12.1; multi-node launchers.
* **Serving binaries** with REST APIs in 12.2–12.4.
* **Telemetry exporters** (OpenTelemetry/Prometheus).
* **Benchmark suite** (perf, quality, safety).
* **Documentation**: API, config, deployment playbooks, runbooks with alert responses.

---

## 19. Open, Versioned Interfaces

* **Model checkpoints:** semantic versioning; changes to attention topology or MoE count bump minor; breaking changes bump major.
* **Index format:** versioned schema for episodic store; migration tools included.
* **KV codec:** version field; decoder must support last two versions.

---

## 20. Security Considerations

* Signed retrieval sources; reject unsigned if policy requires.
* Sandboxed tool execution with resource limits.
* Strict CORS and auth on admin endpoints.
* Rate limits per tenant for retrieval and tool calls.

---

### Appendix A: Reference Shapes (d_model=4096)

* `Cq=Ck=Cv=128` per head group, `H=32`, `H_kv=8`
* FFN hidden size dense: 16384; MoE expert hidden: 12288
* Global summaries: `B=128`, `S=2` per block → ≤ L/64 summary tokens

### Appendix B: Default Loss Weights (tune per dataset)

* LM CE: `1.0`
* Retrieval contrastive: `0.2`
* Router load-balance: `0.05`
* Router regret: `0.02`
* Safety conformance: `0.1`
* Long-range tasks auxiliary: `0.1`

---

**End of REFRACTOR v1.0 Specification.**

# Phase 1 — Reframer Service Specification

This document captures the functional contracts, schemas, and validation strategy for the Phase 1 Reframer Service. It fulfills the Phase 1 checklist items associated with JSON schema finalization, constraint extraction coverage, protocol tag parsing, and API surface definition.

---

## 1. Overview

The Reframer Service ingests heterogeneous client requests and produces validated internal representations that downstream tokenizer and distinction engine modules consume. Responsibilities include:

- Verifying request payloads against strongly typed JSON schemas.
- Normalizing role annotations and protocol tags into canonical enums and mask hints.
- Extracting constraint metadata (tool budgets, safety flags, retrieval policies) into structured fields with deterministic defaults.
- Emitting descriptive validation diagnostics and recording golden fixtures for regression.
- Providing a well-defined HTTP API with OpenAPI documentation for integration partners.

---

## 2. Data Schemas

All schemas are versioned (current `reframer_schema_version = "1.0.0"`) and packaged under `specification/phase1/fixtures/`. Each schema file includes `$id` anchors to enable reuse.

### 2.1 Inbound Request Schema (`reframer_request.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://refactor.ai/schema/reframer/request",
  "type": "object",
  "required": ["request_id", "created_at", "channels", "payload"],
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "type": "string",
      "const": "1.0.0"
    },
    "request_id": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_-]{8,64}$"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "tenant": {
      "type": "string",
      "minLength": 1
    },
    "channels": {
      "type": "array",
      "minItems": 1,
      "items": { "$ref": "#/$defs/channel" }
    },
    "payload": {
      "type": "object",
      "required": ["messages"],
      "additionalProperties": false,
      "properties": {
        "messages": {
          "type": "array",
          "minItems": 1,
          "items": { "$ref": "#/$defs/message" }
        },
        "attachments": {
          "type": "array",
          "items": { "$ref": "#/$defs/attachment" }
        },
        "context_window": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "constraints": { "$ref": "https://refactor.ai/schema/reframer/constraints" }
  },
  "$defs": {
    "channel": {
      "type": "object",
      "required": ["channel_id", "role"],
      "additionalProperties": false,
      "properties": {
        "channel_id": { "type": "string", "minLength": 1 },
        "role": { "$ref": "https://refactor.ai/schema/reframer/role" },
        "priority": { "type": "integer", "minimum": 0, "maximum": 10 }
      }
    },
    "message": {
      "type": "object",
      "required": ["id", "role", "content"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string", "minLength": 1 },
        "role": { "$ref": "https://refactor.ai/schema/reframer/role" },
        "protocol_tags": {
          "type": "array",
          "items": { "type": "string", "pattern": "^<[^>]+>$" }
        },
        "content": {
          "oneOf": [
            { "type": "string" },
            {
              "type": "object",
              "required": ["type", "value"],
              "properties": {
                "type": { "enum": ["text", "json", "binary"] },
                "value": { "type": "string" },
                "encoding": { "enum": ["utf-8", "base64"] }
              }
            }
          ]
        },
        "metadata": {
          "type": "object",
          "additionalProperties": { "type": ["string", "number", "boolean"] }
        }
      }
    },
    "attachment": {
      "type": "object",
      "required": ["id", "media_type", "uri"],
      "properties": {
        "id": { "type": "string", "minLength": 1 },
        "media_type": { "type": "string" },
        "uri": { "type": "string", "format": "uri" },
        "hash": { "type": "string", "pattern": "^[A-Fa-f0-9]{64}$" }
      }
    }
  }
}
```

### 2.2 Role Schema (`role.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://refactor.ai/schema/reframer/role",
  "type": "string",
  "enum": [
    "system",
    "user",
    "assistant",
    "tool",
    "code",
    "data"
  ]
}
```

### 2.3 Constraint Metadata Schema (`constraints.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://refactor.ai/schema/reframer/constraints",
  "type": "object",
  "required": ["routing"],
  "additionalProperties": false,
  "properties": {
    "routing": {
      "type": "object",
      "required": ["tool_budget", "retrieval"],
      "additionalProperties": false,
      "properties": {
        "tool_budget": {
          "type": "object",
          "required": ["total", "per_tool"],
          "properties": {
            "total": { "type": "integer", "minimum": 0, "maximum": 16 },
            "per_tool": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["tool_name", "budget"],
                "properties": {
                  "tool_name": { "type": "string", "minLength": 1 },
                  "budget": { "type": "integer", "minimum": 0, "maximum": 8 }
                }
              }
            }
          }
        },
        "retrieval": {
          "type": "object",
          "required": ["precision_threshold", "sources"],
          "properties": {
            "precision_threshold": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
            "sources": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["source_id", "allow"],
                "properties": {
                  "source_id": { "type": "string", "minLength": 1 },
                  "allow": { "type": "boolean" },
                  "ttl_s": { "type": "integer", "minimum": 0 }
                }
              }
            }
          }
        }
      }
    },
    "safety": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "content_filters": {
          "type": "array",
          "items": { "type": "string" }
        },
        "requires_human_review": { "type": "boolean", "default": false }
      }
    },
    "policies": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "allow_copy": { "type": "boolean", "default": true },
        "allow_schema_mutation": { "type": "boolean", "default": false }
      }
    }
  }
}
```

---

## 3. Validation Strategy

### 3.1 Descriptive Error Reporting

- Wrap JSON Schema validation with custom error translators that map validation failure paths to actionable messages (e.g., `constraints.routing.tool_budget.per_tool[1].budget` → `Tool "code_search" budget exceeds limit (max=8)`).
- Emit machine-readable error codes alongside human-readable messages to power client retries.
- Log rejected payload snippets with PII scrubbing for telemetry dashboards.

### 3.2 Golden Fixtures

- Maintain fixtures under `specification/phase1/fixtures/requests/` including:
  - `happy_path.json`: full multi-channel conversation with tools and retrieval policies.
  - `schema_errors/*.json`: curated invalid payloads annotated with expected error codes.
  - `constraint_defaults.json`: demonstrates default filling when optional policy fields are omitted.
- Integrate fixtures into CI regression by replaying through validation layer and asserting canonicalized outputs.

### 3.3 Unit Test Coverage

- Validation tests cover positive/negative cases per schema component.
- Snapshot tests verify normalized role/mask hints for messages with protocol tags.
- Constraint extraction tests ensure budgets, safety flags, and retrieval policies map to internal structs.

---

## 4. Constraint Extraction Logic

| Constraint Type | Extraction Source | Normalization Rules | Unit Coverage |
| --- | --- | --- | --- |
| Tool Budget | `constraints.routing.tool_budget` | Clamp negative or missing budgets to zero; enforce `total ≥ Σ per_tool.budget`. Emit warning when total exceeds limit (16). | Boundary tests at 0, 8, 16; conflict cases where per-tool sum exceeds total. |
| Retrieval Policies | `constraints.routing.retrieval` | Default `precision_threshold = 0.8` when omitted. Filter `sources` to unique `source_id`. TTL defaults to `86_400` seconds when missing. | Tests verifying deduplication, default TTL injection, and threshold bounds. |
| Safety Flags | `constraints.safety` | Expand `content_filters` into enum set; unsupported filters trigger validation errors. `requires_human_review` default false. | Tests enumerating allowed filters and rejection path for unknown entries. |
| Policy Overrides | `constraints.policies` | Merge with defaults (`allow_copy = true`, `allow_schema_mutation = false`). | Tests covering explicit false overrides and default fallback. |

Pseudocode for normalization:

```python
def normalize_constraints(raw):
    budget_total = clamp(raw.tool_budget.total, 0, 16)
    per_tool = []
    for item in dedupe(raw.tool_budget.per_tool, key="tool_name"):
        per_tool.append({
            "tool_name": item.tool_name,
            "budget": clamp(item.budget or 0, 0, 8)
        })
    if sum(p["budget"] for p in per_tool) > budget_total:
        raise ConstraintError("tool_budget.total", "Sum of per-tool budgets exceeds total")

    retrieval = raw.retrieval or {}
    retrieval["precision_threshold"] = clamp(
        retrieval.get("precision_threshold", 0.8), 0.0, 1.0
    )
    normalized_sources = []
    for source in dedupe(retrieval.get("sources", []), key="source_id"):
        normalized_sources.append({
            "source_id": source.source_id,
            "allow": bool(source.allow),
            "ttl_s": source.ttl_s if source.ttl_s is not None else 86400
        })
    retrieval["sources"] = normalized_sources

    safety = normalize_safety(raw.safety)
    policies = merge_defaults(raw.policies, defaults={
        "allow_copy": True,
        "allow_schema_mutation": False
    })

    return NormalizedConstraints(budget_total, per_tool, retrieval, safety, policies)
```

---

## 5. Protocol Tag Parser

Protocol tags translate inline annotations into role augmentations and mask hints. The parser reads tags of the form `<category:identifier>` and applies table-driven rules.

| Tag Pattern | Role Adjustment | Mask Bits | Additional Effects |
| --- | --- | --- | --- |
| `<tool:NAME>` | Force role `tool`; assign `TOOL_SCOPE` mask; register tool name for budget tracking. | `TOOL_SCOPE` | Adds gating feature `tool_id = NAME`. |
| `<safety:restricted>` | Preserve original role; add `SAFETY_SCOPE` mask bit; mark message for safety review. | `SAFETY_SCOPE` | Emits telemetry counter `safety_restricted_messages`. |
| `<retrieval:context>` | Preserve role; add `RET_SCOPE` mask bit; flag message as retrieval context candidate. | `RET_SCOPE` | Increments retrieval budget usage weight by 1. |
| `<segment:BOUNDARY>` | Preserve role; adds `SEGMENT` mask delimiting segments. | `SEGMENT` | Resets segment position counter. |
| `<role:assistant>` | Override role with explicit enum value; validates against allowed roles. | Depends on tag | Useful for scripted prompts. |

Parser behavior:

- Tags are processed left-to-right; the last role override wins.
- Unknown tags trigger `UNKNOWN_PROTOCOL_TAG` warning but do not block processing.
- Tag effects accumulate, enabling multiple mask bits per message.
- Parser returns both normalized role and list of mask hints for mask compiler ingestion.

Unit tests cover:

- Multiple tags per message with deterministic precedence.
- Conflict detection (e.g., `<tool:a>` followed by `<role:user>` results in validation error due to forbidden override).
- Serialization of parsed hints into downstream `TokenHint` objects.

---

## 6. API Surface

### 6.1 Service Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/v1/reframe` | Validate and normalize a single request; returns normalized payload plus mask hints. |
| `POST` | `/v1/reframe/batch` | Accept array of request payloads; returns per-item success/error envelopes. |
| `GET` | `/v1/schemas/{name}` | Serve JSON schemas (`request`, `role`, `constraints`) for client validation. |
| `GET` | `/v1/health` | Health/Liveness probe exposing schema version and dependency status. |

### 6.2 OpenAPI Summary

```yaml
openapi: 3.1.0
info:
  title: Reframer Service API
  version: 1.0.0
servers:
  - url: https://api.refactor.ai
paths:
  /v1/reframe:
    post:
      operationId: reframeRequest
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: 'https://refactor.ai/schema/reframer/request'
      responses:
        '200':
          description: Normalized response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReframeResponse'
        '400':
          description: Schema validation failed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ValidationError'
components:
  schemas:
    ReframeResponse:
      type: object
      required: [request_id, normalized]
      properties:
        request_id:
          type: string
        normalized:
          type: object
        mask_hints:
          type: array
          items:
            type: object
            properties:
              token_range:
                type: array
                items:
                  type: integer
                  minItems: 2
                  maxItems: 2
              mask_bits:
                type: array
                items:
                  type: string
    ValidationError:
      type: object
      required: [error_code, message, field_path]
      properties:
        error_code:
          type: string
        message:
          type: string
        field_path:
          type: string
        details:
          type: object
```

### 6.3 Contract Tests

- Use contract tests to assert schema served by `/v1/schemas/request` matches repository JSON definition via checksum comparison.
- Batch endpoint tests ensure partial failures return HTTP 207-style multi-status payload with per-item results.
- Health endpoint includes dependency probes (schema registry, feature flag service) with response caching ≤ 1s.

---

## 7. Implementation Notes

- All schemas and OpenAPI spec are generated into artifacts consumed by SDK clients; generation pipeline runs on every merge.
- Validation layer is language-agnostic; reference implementation provided in Rust with Python harness for fixtures.
- Telemetry counters integrate with Phase 0 SLA dashboard skeleton (schema validation failure rate, request throughput).
- Feature flags allow gradual rollout of new protocol tags; unknown tags produce warnings until promoted to errors.

---

## 8. Acceptance Checklist Mapping

| Checklist Item | Evidence |
| --- | --- |
| Finalize JSON schemas for inbound requests, roles, and constraint metadata. | Sections 2.1–2.3 define versioned schemas with validation rules. |
| Implement schema validation with descriptive error reporting and golden fixtures. | Sections 3.1–3.3 detail error translation and fixture strategy. |
| Encode constraint extraction logic with unit coverage. | Section 4 describes normalization rules, pseudocode, and coverage. |
| Build protocol tag parser translating annotations into role + mask hints. | Section 5 specifies tag processing table and tests. |
| Expose reframer API endpoints with contract tests and OpenAPI documentation. | Section 6 documents endpoints, OpenAPI spec, and contract tests. |


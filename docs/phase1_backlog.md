# Phase 1 Backlog Seed

| ID | Title | Description | Owner | Estimate (pts) | Dependencies |
| -- | ----- | ----------- | ----- | -------------- | ------------ |
| P1-1 | Reframer schema validator | Implement JSON schema validation pipeline for requests | Reframer Lead | 5 | Phase 0 telemetry | 
| P1-2 | Role tagging module | Map protocol tags to role embeddings and mask bits | Reframer Lead | 8 | P1-1 |
| P1-3 | Tokenizer vocabulary bootstrap | Create extensible vocabulary with placeholder merges | Tokenization Lead | 13 | Phase 0 repo scaffolding |
| P1-4 | Mask compiler rule ingestion | Parse YAML rules and generate mask bitsets | Distinction Engine Lead | 8 | P1-2 |
| P1-5 | Mask legality property tests | Implement property-based tests for mask conformance | QA Lead | 5 | P1-4 |
| P1-6 | Telemetry for mask entropy | Emit metrics for mask entropy anomalies | Telemetry Lead | 3 | P1-4 |
| P1-7 | Distinction engine integration harness | Connect reframer, tokenizer, mask compiler for end-to-end flow | Integration Lead | 8 | P1-1,P1-3,P1-4 |

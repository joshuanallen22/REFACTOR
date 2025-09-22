# Risk Register

| ID | Risk Description | Category       | Likelihood | Impact | Mitigation Owner     | Mitigation Plan | Status |
| -- | ---------------- | -------------- | ---------- | ------ | -------------------- | --------------- | ------ |
| R1 | Delay in CI infrastructure readiness blocking downstream work | Schedule | Medium | High | Infrastructure Lead | Parallelize CI setup with repo scaffolding; use canned workflows | Open |
| R2 | Telemetry heartbeat not integrated with monitoring stack | Technical | Low | Medium | Telemetry Lead | Implement local exporter + API mock, validate via unit tests | Open |
| R3 | Lack of clarity on retrieval vs. safety responsibilities | Organizational | Medium | Medium | Program Manager | Publish RACI matrix and confirm in steering review | Open |
| R4 | Secrets management misconfiguration leading to credential leaks | Security | Low | High | DevOps Engineer | Adopt template-based configuration with peer review and secret scanning | Open |
| R5 | Scope creep in Phase 1 backlog | Scope | Medium | Medium | Program Manager | Enforce change control and backlog grooming cadence | Open |

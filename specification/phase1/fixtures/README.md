# Reframer Service Fixture Directory

Golden fixtures referenced by the Reframer Service specification live here. They are grouped by artifact type:

- `requests/` — canonical inbound request samples (happy path, constraint defaults, schema violations).
- `responses/` — normalized outputs paired with request fixtures for regression testing.
- `contracts/` — checksum manifests for schemas served by the API endpoints.

Fixture population is tracked in the Phase 1 CI tasks; initial files will be added once the validation harness is implemented.

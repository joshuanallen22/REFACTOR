# REFRACTOR Engineering Foundations

This repository hosts the implementation artifacts for the REFRACTOR program. The Phase 0 deliverables
bootstrap governance, engineering infrastructure, and planning materials so later phases can iterate
quickly.

## Repository layout

- `docs/` – governance, planning, and operational documentation.
- `src/` – Python source packages for telemetry and future system components.
- `tests/` – unit tests executed by the CI pipeline.
- `tools/` – helper scripts and automation entrypoints.
- `.github/workflows/` – CI/CD definitions.
- `specification/` – canonical REFRACTOR requirements and implementation plan (provided).

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quality checks

| Command       | Description                                     |
| ------------- | ----------------------------------------------- |
| `make format` | Format code using Black.                        |
| `make lint`   | Lint code using Ruff.                           |
| `make type`   | Run mypy type checks.                           |
| `make test`   | Execute the pytest unit test suite.             |
| `make ci`     | Run the full CI sequence (format, lint, type, tests). |


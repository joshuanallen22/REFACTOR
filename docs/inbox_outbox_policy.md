# Inbox/Outbox Workflow Policy

## Purpose
Ensure program artifacts transition from planned to completed states with clear traceability.

## Workflow
1. Author creates or updates checklist/task document inside `inbox/`.
2. Work item owner completes deliverables and gathers supporting evidence (links to docs, tests, metrics).
3. Owner requests review from accountable lead; reviewers leave approval in document footer.
4. Upon approval, document is copied to `outbox/` with timestamped filename and changelog entry.
5. `inbox/` copy replaced with pointer to outbox artifact and status updated to ✅.

## Naming Conventions
- `inbox/Phase_<n>_<description>.md` for active work.
- `outbox/<YYYYMMDD>_Phase_<n>_<description>.md` for archived artifacts.

## Tooling
- Git-based workflow ensures history preservation.
- Optional automation script (`tools/archive_checklist.py`) will handle copy + metadata in later phase.

## Communication
- Weekly digest summarizes inbox status and newly archived artifacts.
- Any blockers flagged in daily standup and tracked until resolved.

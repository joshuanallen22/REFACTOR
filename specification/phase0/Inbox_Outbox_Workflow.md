# Inbox/Outbox Workflow Policy

The REFRACTOR program uses the inbox/outbox workflow to track planning artifacts from inception through completion.

## Definitions
- **Inbox:** Active work items, checklists, and drafts that require execution or approval.
- **Outbox:** Completed artifacts with sign-offs and linked evidence. Items are moved here after exit criteria are satisfied.

## Workflow Steps
1. **Authoring:** Teams create new artifacts (charters, checklists, design docs) in the inbox and tag responsible owners.
2. **Review:** Owners solicit feedback via asynchronous comments and scheduled reviews. Review status tracked in weekly ceremonies.
3. **Approval:** Once acceptance criteria met, stakeholders provide written approval (recorded in artifact header).
4. **Archival:** Program management moves the artifact to `outbox/`, adds commit reference to changelog, and updates WBS item status.
5. **Traceability:** Each outbox artifact includes links back to relevant specification sections and backlog tickets.

## Communication Protocol
- Weekly standups highlight inbox items nearing completion or blocked.
- Risk triage meetings review inbox artifacts connected to high-priority risks.
- Outbox updates summarized in biweekly steering committee notes with hyperlinks to supporting evidence.

## Tooling & Ownership
- Source control (this repository) is the system of record; no external documents without mirrored copies.
- Program manager maintains the index of inbox/outbox artifacts and enforces naming conventions.
- Automation hooks (to be implemented in Phase 1) will notify Slack when artifacts transition between states.

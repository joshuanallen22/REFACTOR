# Documentation Workspace Plan

The REFRACTOR program maintains a centralized workspace that links specification material, design
decisions, and operational records.

## Structure
- **Specification Hub:** Direct links to `specification/REFRACTOR_SPEC.md` and the implementation plan.
- **Phase Journals:** Subdirectories `docs/phases/phase_<n>/` for meeting notes, retrospectives, and sign-offs.
- **Decision Log:** Append-only register capturing architectural decisions (ADR format) located at
  `docs/decisions/`.
- **Knowledge Base:** Glossary and onboarding material for new contributors stored under `docs/glossary/`.

## Access & Permissions
- Editable by core engineering, safety, and product stakeholders.
- Read-only mirrors for extended collaborators to maintain alignment without jeopardizing integrity.

## Tooling
- Workspace synchronized with repository via docs-as-code model; changes flow through pull requests.
- Weekly documentation audits ensure artifacts reflect current program state.

## Next Steps
- Populate glossary with terminology from the specification.
- Stand up ADR template before Phase 1 kickoff.
- Automate changelog generation using GitHub Actions after CI passes.

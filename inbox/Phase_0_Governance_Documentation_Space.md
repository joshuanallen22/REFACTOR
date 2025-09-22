# Shared Documentation Space Plan

## 1. Platform & Structure
- **Platform:** Confluence space `REFRACTOR Control Plane` with read/write permissions for core team, read-only for extended stakeholders.
- **Root Sections:**
  1. **Specifications:** Mirrors `specification/` repo folder; embeds canonical artifacts including `REFRACTOR_SPEC.md` and implementation plan.
  2. **Governance:** Hosts charter, RACI, ceremony notes, risk register snapshots, decision logs.
  3. **Engineering Execution:** Sprint notes, phase checklists, dependency tracking, CI/CD runbooks.
  4. **Telemetry & SLAs:** Dashboards, probe definitions, alert thresholds, links to Grafana/Prometheus views.
  5. **Safety & Compliance:** Safety mask policies, incident response procedures, audit trails.

## 2. Artifact Lifecycle
1. Draft in git `inbox/` directory.
2. Publish rendered markdown/PDF in Confluence with version tags (e.g., `v0.1-draft`).
3. Solicit comments via inline annotations; incorporate updates in git source.
4. Upon approval, mark Confluence page as `Approved` and link to outbox artifact commit hash.

## 3. Glossary Integration
- Maintain glossary page seeded from spec Appendix terms; update via weekly sync between Technical Writer and Chief Architect.
- Glossary terms cross-linked within Confluence pages and spec to ensure consistent terminology.

## 4. Access & Permissions
- **Editors:** Program Director, Chief Architect, Module Leads, Safety Lead, Ops Lead.
- **Commenters:** Extended engineering team, Legal Liaison, Data Governance.
- **Viewers:** Executive leadership, partner teams.
- Access reviews performed quarterly and upon staff changes.

## 5. Tooling & Automation
- Use CI job `docs-sync` to publish markdown changes to Confluence via API nightly.
- Slack notifications in `#refactor-docs` summarizing pages updated in last 24h.
- Embed Jira dashboards for backlog metrics; ensure SSO across tools.

## 6. Onboarding & Guidance
- Create onboarding checklist referencing this plan.
- Provide short Loom walkthrough of documentation structure.
- Highlight governance artifact lifecycle in onboarding materials.


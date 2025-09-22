# Shared Documentation Space Plan

## 1. Platform & Structure
- **Platform:** Confluence space `REFRACTOR Control Plane` with read/write permissions for core team, read-only for extended stakeholders, and public read for approved partners.
- **Root Sections:**
  1. **Specifications:** Mirrors `specification/` repo folder; embeds canonical artifacts including `REFRACTOR_SPEC.md` and implementation plan with version tags.
  2. **Governance:** Hosts charter, RACI, ceremony notes, risk register snapshots, decision logs, and approvals archive.
  3. **Engineering Execution:** Sprint notes, phase checklists, dependency tracking, CI/CD runbooks, and retrospectives.
  4. **Telemetry & SLAs:** Dashboards, probe definitions, alert thresholds, Grafana/Prometheus links, and KPI glossary.
  5. **Safety & Compliance:** Safety mask policies, incident response procedures, audit trails, and compliance attestations.
  6. **Customer Readouts:** Launch briefs, SLA commitments, roadmap snapshots for stakeholder consumption.

## 2. Artifact Lifecycle
1. Draft in git `inbox/` directory with metadata (owner, version, review date).
2. Publish rendered markdown/PDF in Confluence with version tags (e.g., `v0.1-draft`).
3. Solicit comments via inline annotations; incorporate updates in git source and note dispositions.
4. Upon approval, mark Confluence page as `Approved`, link to outbox artifact commit hash, and archive superseded versions.
5. Schedule reminder to review each artifact at least quarterly.

## 3. Glossary & Taxonomy Integration
- Maintain glossary page seeded from spec Appendix terms; update via weekly sync between Technical Writer and Chief Architect.
- Cross-link glossary entries into Confluence pages, Jira epics, and spec sections to enforce consistent terminology.
- Track taxonomy changes in decision log with impact notes for downstream tooling and analytics.

## 4. Access & Permissions
- **Editors:** Program Director, Chief Architect, Module Leads, Safety Lead, Ops Lead, Technical Writer.
- **Commenters:** Extended engineering team, Legal Liaison, Data Governance, Finance Partner.
- **Viewers:** Executive leadership, partner teams, approved vendor contacts.
- Access reviews performed quarterly and upon staff changes; revoke within 24h of offboarding.
- Enable page-level restrictions for sensitive safety/compliance artifacts.

## 5. Tooling & Automation
- Use CI job `docs-sync` to publish markdown changes to Confluence via API nightly with diff summaries.
- Slack notifications in `#refactor-docs` summarizing pages updated in last 24h and pending approvals.
- Embed Jira dashboards for backlog metrics; ensure SSO across tools and data retention alignment.
- Maintain backup export weekly to secure storage for disaster recovery.

## 6. Onboarding & Guidance
- Create onboarding checklist referencing this plan with links to key sections and training materials.
- Provide short Loom walkthrough of documentation structure and governance lifecycle.
- Highlight inbox/outbox workflow and approval expectations during onboarding sessions.
- Track completion in onboarding tracker with Program Director sign-off.

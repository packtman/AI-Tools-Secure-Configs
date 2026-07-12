# Admin Controls — Centralized IT Management for AI Tools

This directory provides a **unified reference** for IT administrators managing AI assistant and chat tools at the organizational level. It covers the admin console settings, identity management, data governance, and compliance controls that IT teams configure through web dashboards, APIs, and MDM systems.

## Scope

This guide focuses on **admin-level controls** — settings managed by IT teams through admin consoles, not end-user or developer configurations. These controls govern:

- Who can access AI tools (identity, provisioning, SSO)
- What features users can use (RBAC, feature toggles)
- How data is handled (retention, training opt-out, DLP)
- What integrations are allowed (plugins, extensions, MCP servers)
- How usage is monitored (audit logs, analytics, compliance)

---

## Covered Tools

| Guide | Tool | Admin Interface | Plans with Admin Controls |
|-------|------|-----------------|---------------------------|
| [`claude-desktop.md`](./claude-desktop.md) | Claude (Desktop & Web) | Claude.ai Admin Console + MDM | Team, Enterprise |
| [`cursor.md`](./cursor.md) | Cursor IDE | Cursor Dashboard + MDM | Business (Teams), Enterprise |
| [`chatgpt.md`](./chatgpt.md) | ChatGPT | chatgpt.com/admin | Business, Enterprise |
| [`gemini.md`](./gemini.md) | Gemini (Google Workspace) | Google Admin Console | Business, Enterprise (Standard/Plus) |
| [`github-copilot.md`](./github-copilot.md) | GitHub Copilot | GitHub AI Controls tab | Business, Enterprise |
| [`windsurf.md`](./windsurf.md) | Windsurf (Codeium) | Windsurf Admin Portal | Enterprise |

---

## Admin Controls Comparison Matrix

### Identity & Access Management

| Capability | Claude | Cursor | ChatGPT | Gemini | GitHub Copilot | Windsurf |
|------------|--------|--------|---------|--------|----------------|----------|
| SAML SSO | Team+ | Enterprise | Business+ | All Workspace editions | Enterprise (GHEC) | Enterprise |
| SCIM provisioning | Enterprise | Enterprise | Enterprise | Via Google Cloud Identity | Enterprise (GHEC) | Enterprise |
| Domain verification | Team+ | — | Enterprise | Workspace default | — | — |
| IP allowlisting | Enterprise | — | Enterprise | Via Context-Aware Access | Enterprise (GHEC) | — |
| MFA enforcement | Via IdP | Via IdP | Via IdP | Admin console native | Via IdP / GitHub | Via IdP |
| Role-based access | 3 roles | 3 roles | 4 roles + custom RBAC | OU/Group-based | Custom roles + fine-grained | Super Admin/Group Admin/Admin/User |

### Data Governance

| Capability | Claude | Cursor | ChatGPT | Gemini | GitHub Copilot | Windsurf |
|------------|--------|--------|---------|--------|----------------|----------|
| No training on data | Team+ | All plans | Business+ | All Workspace editions | Business+ | Enterprise |
| Data retention control | Enterprise | — | Enterprise | Admin console | — (180-day audit log) | Enterprise |
| Data residency | Enterprise (US/EU) | — | Enterprise (10 regions) | Workspace data regions | GHEC data residency | Self-hosted option |
| Customer-managed keys | Enterprise | — | Enterprise (EKM) | CMEK via GCP | GHEC (BYOK) | Self-hosted |
| DLP integration | Compliance API | — | Compliance API | Native Workspace DLP | Content exclusion | `.codeiumignore` |
| Conversation export | Enterprise | — | Compliance API | Vault/BigQuery export | Audit log streaming | API export |

### Feature Governance

| Capability | Claude | Cursor | ChatGPT | Gemini | GitHub Copilot | Windsurf |
|------------|--------|--------|---------|--------|----------------|----------|
| Disable specific features | Managed settings | Dashboard + MDM | RBAC per feature | Admin console per service | Per-policy toggle | Admin Portal toggles |
| Extension/plugin control | MDM policy keys | Allowlist (dashboard/MDM) | App governance | Workspace Marketplace | — (IDE native) | MCP whitelist |
| Model access restrictions | Via plan tier | Model allow/blocklist | Per-role usage limits | Edition-based | Policy toggle | Per-team model access |
| File upload controls | Managed settings | — | Per-role toggle | Admin console | Content exclusion | `.codeiumignore` |
| Web browsing control | — | — | Per-role toggle | Admin console | — | Admin toggle |
| Agent/GPT governance | Managed settings | Team Rules + sandbox | GPT/agent publishing + RBAC | Gems governance | Agent policies + MCP registry | MCP whitelist + execution limits |
| Content exclusion | Managed deny lists | Repository blocklist | — | DLP rules | File/directory glob patterns | `.codeiumignore` patterns |

### Monitoring & Compliance

| Capability | Claude | Cursor | ChatGPT | Gemini | GitHub Copilot | Windsurf |
|------------|--------|--------|---------|--------|----------------|----------|
| Audit logs | Enterprise | Enterprise | Enterprise | Cloud Audit Logs | Enterprise (180 days) | Enterprise |
| Usage analytics | Team+ | Team+ | Business+ | Admin console reports | Business+ | Enterprise |
| Compliance certifications | SOC 2 Type II, ISO 27001 | SOC 2 Type II | SOC 2 Type II, ISO 27001 | SOC 2/3, ISO 27001, FedRAMP | SOC 2 Type II, FedRAMP | SOC 2 Type II |
| HIPAA eligible | Enterprise (BAA) | — | Enterprise (BAA) | Enterprise Plus | Enterprise (GHEC BAA) | Self-Hosted |
| Admin API | Compliance API | Admin REST API | — | Google Admin SDK | Enterprise API | Service Keys API |
| Audit log streaming | — | — | — | BigQuery/Chronicle | SIEM streaming (Splunk, Datadog, etc.) | API export |

### Deployment & Enforcement

| Capability | Claude | Cursor | ChatGPT | Gemini | GitHub Copilot | Windsurf |
|------------|--------|--------|---------|--------|----------------|----------|
| MDM (macOS) | plist profiles | plist profiles | — | Chrome/device policy | — | — |
| MDM (Windows) | Registry/Intune | Registry/Intune | — | Chrome/device policy | — | — |
| Server-managed settings | Admin console push | Dashboard push | — | Admin console | Enterprise AI Controls | Admin Portal |
| Update control | `autoUpdaterEnforcementHours` | `UpdateMode` MDM key | Managed by OpenAI | Chrome/OS updates | VS Code/IDE updates | Managed by Codeium |
| Managed browser | — | — | — | Chrome Enterprise | — | — |
| Self-hosted option | — | — | — | — | GHES | ✓ (full self-hosted) |

---

## Implementation Priority

For organizations deploying multiple AI tools, this recommended sequence addresses the highest-risk controls first:

### Phase 1: Identity & Access

1. **SSO enforcement** — Prevent credential sprawl; route all AI tool auth through your IdP.
2. **SCIM provisioning** — Automate onboarding/offboarding to prevent orphaned accounts.
3. **Domain verification** — Ensure only your org's users can join workspaces.
4. **MDM policies** — Lock devices to approved teams/orgs (Cursor `AllowedTeamId`, Claude `forceLoginOrgUUID`).

### Phase 2: Data Governance

1. **Training opt-out verification** — Confirm all tools have data training disabled.
2. **Retention policies** — Set conversation/data retention aligned with your data classification policy.
3. **DLP rules** — Block sensitive data (PII, credentials, proprietary code) from reaching AI services.
4. **Content exclusion** — Configure file/directory exclusions in GitHub Copilot, `.codeiumignore` in Windsurf.
5. **Network egress controls** — Restrict AI sandbox network access (Cursor sandbox allowlist, Claude `sandbox.network.allowedDomains`).

### Phase 3: Feature Governance

1. **Feature audits** — Inventory which AI features are enabled per tool and per team.
2. **RBAC configuration** — Restrict advanced features (agents, code execution, plugins, Sites) to approved groups.
3. **Extension/integration lockdown** — Allowlist only vetted plugins, MCP servers, and extensions across all tools.
4. **Agent governance** — Control agent building, publishing, and execution permissions (ChatGPT workspace agents, GitHub Copilot cloud agent, Claude Code).
5. **Model access control** — Restrict which AI models are available per team/role (Cursor model allowlist, GitHub Copilot model selection policy).

### Phase 4: Monitoring & Compliance

1. **Audit log ingestion** — Route all AI tool audit logs to your SIEM (GitHub streaming, Claude compliance API, Gemini BigQuery export).
2. **Usage dashboards** — Set up analytics to track adoption, cost, and anomalies.
3. **Agent session monitoring** — Review agent activity and session logs (GitHub AI Controls, Cursor analytics).
4. **Compliance documentation** — Document controls for SOC 2, ISO 27001, or other frameworks.

---

## Quick Reference (HTML / PDF)

For a printable, single-document summary of all admin controls with comparison matrices:

| Format | File | Use Case |
|--------|------|----------|
| HTML | [`admin-controls-reference.html`](./admin-controls-reference.html) | Open in browser, searchable, interactive |
| PDF | [`admin-controls-reference.pdf`](./admin-controls-reference.pdf) | Print, share with stakeholders, offline reference |

Both files contain the same content: per-tool admin settings summaries followed by cross-tool comparison matrices covering identity, data governance, feature governance, monitoring, and deployment.

---

## Examples

The [`examples/`](./examples/) directory contains ready-to-use admin configuration templates:

| File | Description |
|------|-------------|
| [`chatgpt-workspace-policy.json`](./examples/chatgpt-workspace-policy.json) | ChatGPT Enterprise workspace default permissions |
| [`gemini-admin-settings.json`](./examples/gemini-admin-settings.json) | Google Workspace Gemini feature access matrix |
| [`cursor-org-policy.json`](./examples/cursor-org-policy.json) | Cursor Enterprise organization-level governance |
| [`claude-admin-policy.json`](./examples/claude-admin-policy.json) | Claude Team/Enterprise admin console policy |
| [`github-copilot-enterprise-policy.json`](./examples/github-copilot-enterprise-policy.json) | GitHub Copilot Enterprise AI Controls policy |
| [`windsurf-admin-policy.json`](./examples/windsurf-admin-policy.json) | Windsurf Enterprise admin portal configuration |
| [`cross-tool-sso-checklist.md`](./examples/cross-tool-sso-checklist.md) | Unified SSO deployment checklist for all six tools |

---

## Relationship to Per-Tool Directories

This directory provides a **cross-tool admin perspective**. The individual tool directories (`claude-desktop/`, `cursor/`, `github-copilot/`, etc.) contain the actual config files, MDM profiles, and tiered examples. Use this directory to:

- Compare admin capabilities across tools
- Plan multi-tool governance strategies
- Find the right admin console settings for each tool
- Coordinate SSO/SCIM across your AI tool portfolio

For drop-in managed configurations, see each tool's dedicated directory.

---

## Last Updated

This reference was last verified against vendor documentation on **July 12, 2026**.

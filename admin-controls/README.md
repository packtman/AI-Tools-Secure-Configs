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

---

## Admin Controls Comparison Matrix

### Identity & Access Management

| Capability | Claude | Cursor | ChatGPT | Gemini |
|------------|--------|--------|---------|--------|
| SAML SSO | Enterprise | Enterprise | Business+ | All Workspace editions |
| SCIM provisioning | Enterprise | Enterprise | Enterprise | Via Google Cloud Identity |
| Domain verification | Team+ | — | Enterprise | Workspace default |
| IP allowlisting | Enterprise | — | Enterprise | Via Context-Aware Access |
| MFA enforcement | Via IdP | Via IdP | Via IdP | Admin console native |
| Role-based access | 3 roles | 3 roles | 4 roles + custom RBAC | OU/Group-based |

### Data Governance

| Capability | Claude | Cursor | ChatGPT | Gemini |
|------------|--------|--------|---------|--------|
| No training on data | Team+ | All plans | Business+ | All Workspace editions |
| Data retention control | Enterprise | — | Enterprise | Admin console |
| Data residency | Enterprise (US/EU) | — | Enterprise (10 regions) | Workspace data regions |
| Customer-managed keys | Enterprise | — | Enterprise (EKM) | CMEK via GCP |
| DLP integration | Compliance API | — | Compliance API | Native Workspace DLP + AI Control Center |
| Conversation export | Compliance API (Enterprise) | — | Compliance API | Vault/BigQuery export |
| Spend controls | Org + per-user caps | Team + per-member + billing groups | Credit pool + per-role caps | Edition-based |

### Feature Governance

| Capability | Claude | Cursor | ChatGPT | Gemini |
|------------|--------|--------|---------|--------|
| Disable specific features | Managed settings | Dashboard + MDM | RBAC per feature | Admin console per service |
| Extension/plugin control | MDM policy keys | Allowlist (dashboard/MDM) | App governance | Workspace Marketplace |
| Model access restrictions | Via plan tier | Model allow/blocklist (provider + model level) | Per-role usage limits | Edition-based |
| File upload controls | Managed settings | — | Per-role toggle | Admin console |
| Web browsing control | — | — | Per-role toggle | Admin console |
| Custom GPT/agent governance | — | Team Rules | GPT publishing + agent RBAC | Gems governance |
| Workspace agents | — | Cloud Agent restrictions | Agent build/share/monitor via RBAC | Agent governance via AI Control Center |
| Sandbox enforcement | `sandbox.enabled` + `failIfUnavailable` | Require sandbox for agents | — | — |
| Sites/app deployment | — | — | Sites (RBAC-controlled) | — |
| Plugin/marketplace control | `strictKnownMarketplaces`, `blockedMarketplaces` | Team Marketplaces | Codex plugins (per-role) | Workspace Marketplace |
| Fail-closed enforcement | `forceRemoteSettingsRefresh` | — | — | — |

### Monitoring & Compliance

| Capability | Claude | Cursor | ChatGPT | Gemini |
|------------|--------|--------|---------|--------|
| Audit logs | Enterprise | Enterprise | Enterprise | Cloud Audit Logs |
| Usage analytics | Team+ | Team+ | Business+ | Admin console reports |
| Compliance certifications | SOC 2 Type II | SOC 2 Type II | SOC 2 Type II | SOC 2/3, ISO 27001, FedRAMP |
| HIPAA eligible | Enterprise (BAA) | — | Enterprise (BAA) | Enterprise Plus |
| Admin API | Compliance API (Enterprise) | Admin API + Analytics API | Compliance API + Analytics API | Google Admin SDK |
| AI code attribution | — | Cursor Blame + AI Code Tracking API | Codex analytics | — |
| AI governance dashboard | — | — | — | AI Control Center |
| Service accounts | — | Enterprise | — | Service accounts (GCP) |
| Billing groups | — | Enterprise | — | — |

### Deployment & Enforcement

| Capability | Claude | Cursor | ChatGPT | Gemini |
|------------|--------|--------|---------|--------|
| MDM (macOS) | plist profiles (Desktop + Code) | plist profiles | — | Chrome/device policy |
| MDM (Windows) | Registry/Intune (Desktop + Code) | Registry/Intune | — | Chrome/device policy |
| Server-managed settings | Admin console push (highest precedence) | Dashboard push | — | Admin console |
| Update control | `autoUpdaterEnforcementHours` | `UpdateMode` MDM key | Managed by OpenAI | Chrome/OS updates |
| Managed browser | — | — | — | Chrome Enterprise |
| Org-pinned login | `forceLoginOrgUUID` | `AllowedTeamId` | SSO enforcement | Workspace login |
| File-based policy | `managed-settings.json` + drop-in directory | — | — | — |
| Multi-team / multi-workspace | Workspace segmentation | Organizations (multi-team) | Global Admin Console | Organizational Units |

---

## Implementation Priority

For organizations deploying multiple AI tools, this recommended sequence addresses the highest-risk controls first:

### Phase 1: Identity & Access (Week 1)

1. **SSO enforcement** — Prevent credential sprawl; route all AI tool auth through your IdP.
2. **SCIM provisioning** — Automate onboarding/offboarding to prevent orphaned accounts.
3. **Domain verification** — Ensure only your org's users can join workspaces.

### Phase 2: Data Governance (Week 2)

1. **Training opt-out verification** — Confirm all tools have data training disabled.
2. **Retention policies** — Set conversation/data retention aligned with your data classification policy.
3. **DLP rules** — Block sensitive data (PII, credentials, proprietary code) from reaching AI services.

### Phase 3: Feature Governance (Week 3)

1. **Feature audits** — Inventory which AI features are enabled per tool and per team.
2. **RBAC configuration** — Restrict advanced features (agents, code execution, plugins) to approved groups.
3. **Extension/integration lockdown** — Allowlist only vetted plugins, MCP servers, and extensions.

### Phase 4: Monitoring & Compliance (Week 4)

1. **Audit log ingestion** — Route all AI tool audit logs to your SIEM.
2. **Usage dashboards** — Set up analytics to track adoption, cost, and anomalies.
3. **Compliance documentation** — Document controls for SOC 2, ISO 27001, or other frameworks.

---

## Quick Reference (HTML)

For a printable, single-document summary of all admin controls with comparison matrices:

| Format | File | Use Case |
|--------|------|----------|
| HTML | [`admin-controls-reference.html`](./admin-controls-reference.html) | Open in browser, searchable, interactive |
| PDF | Use browser Print → Save as PDF | Print, share with stakeholders, offline reference |

The HTML file includes print-optimized CSS (`@media print`) for A4 output. Open in any browser and use Print (Ctrl/Cmd+P) to generate a PDF.

---

## Examples

The [`examples/`](./examples/) directory contains ready-to-use admin configuration templates:

| File | Description |
|------|-------------|
| [`chatgpt-workspace-policy.json`](./examples/chatgpt-workspace-policy.json) | ChatGPT Enterprise workspace default permissions |
| [`gemini-admin-settings.json`](./examples/gemini-admin-settings.json) | Google Workspace Gemini feature access matrix |
| [`cursor-org-policy.json`](./examples/cursor-org-policy.json) | Cursor Enterprise organization-level governance |
| [`claude-admin-policy.json`](./examples/claude-admin-policy.json) | Claude Team/Enterprise admin console policy |
| [`cross-tool-sso-checklist.md`](./examples/cross-tool-sso-checklist.md) | Unified SSO deployment checklist for all four tools |

---

## Relationship to Per-Tool Directories

This directory provides a **cross-tool admin perspective**. The individual tool directories (`claude-desktop/`, `cursor/`, etc.) contain the actual config files, MDM profiles, and tiered examples. Use this directory to:

- Compare admin capabilities across tools
- Plan multi-tool governance strategies
- Find the right admin console settings for each tool
- Coordinate SSO/SCIM across your AI tool portfolio

For drop-in managed configurations, see each tool's dedicated directory.

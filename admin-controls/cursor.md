# Cursor — Admin Controls Reference

## Overview

Cursor provides centralized admin controls through the **Cursor Dashboard** (cursor.com/settings), available to organizations on **Business** (formerly Teams) and **Enterprise** plans. Enterprise customers additionally have access to **Organizations** — a top-level governance container for managing multiple teams from a single dashboard.

Admin controls cover identity management, security enforcement, spend governance, model access, and compliance monitoring. Device-level policies can be enforced via MDM for managed endpoints.

---

## Admin Interface Access

| Interface | URL | Plans |
|-----------|-----|-------|
| Team Dashboard | `cursor.com/settings` | Business, Enterprise |
| Organization Dashboard | `cursor.com/settings` (org-level) | Enterprise only |
| Admin REST API | `cursor.com/docs/account/teams/admin-api` | Business, Enterprise |
| AI Code Tracking API | `cursor.com/docs/account/teams/ai-code-tracking-api` | Enterprise only |

### Roles

| Role | Capabilities |
|------|-------------|
| **Admin** | Full access: billing, SSO, SCIM, invite/remove members, all settings |
| **Unpaid Admin** | Same administrative capabilities without consuming a paid seat |
| **Member** | Use Cursor within admin-defined policies |

---

## 1. Identity & Access Management

### SSO

| Setting | Location | Notes |
|---------|----------|-------|
| SAML SSO | Dashboard → Security & Identity → SSO | Enterprise; supports Okta, Azure AD, Google Workspace |
| Enforce SSO | Dashboard → Security & Identity → SSO | Disables email/password login for team members |
| Allowed Team ID (MDM) | MDM policy `AllowedTeamId` | Lock device login to specific team(s) |

### SCIM 2.0 Provisioning (Enterprise)

| Setting | Location | Notes |
|---------|----------|-------|
| Enable SCIM | Dashboard → Security & Identity → SCIM | Auto-sync users and groups from IdP |
| SCIM endpoint | Generated in dashboard | Provide to IdP for provisioning |
| SCIM bearer token | Generated in dashboard | Authenticates IdP requests |
| Directory group sync | Automatic with SCIM | Groups synced for RBAC and spend limits |

### User Access Controls (Enterprise)

| Control | Effect |
|---------|--------|
| Restrict CLI access | Control which users can access agents via CLI |
| Restrict Cloud Agents | Control which users can create Cloud Agents |
| Restrict analytics | Limit analytics dashboard to admins only |
| Disable BYOK | Prevent users from using their own API keys |
| Global agent run settings | Configure system-level rules for all agent sessions |

---

## 2. Security & Governance

### Privacy & Data

| Setting | Location | Effect |
|---------|----------|--------|
| Privacy Mode (team-wide) | Dashboard → Settings → Privacy | Enforce zero data retention with AI providers |
| Zero data retention | Dashboard → Settings → Privacy | Per-provider: OpenAI, Anthropic, Google Vertex, xAI |
| Repository blocklist | Dashboard → Security | Block specific repos from AI access |

### MCP Server Governance

| Setting | Location | Effect |
|---------|----------|--------|
| MCP allowlist | Dashboard → Security → MCP Servers | Only approved MCP servers permitted |
| MCP denylist | Dashboard → Security → MCP Servers | Block specific MCP server packages |

### Extension Control

| Setting | Location | Effect |
|---------|----------|--------|
| Allowed extensions (dashboard) | Dashboard → Security & Identity | Push extension allowlist to all clients |
| Allowed extensions (MDM) | `AllowedExtensions` MDM key | Device-level override; JSON string of permitted IDs |

### Workspace Trust

| Setting | Location | Effect |
|---------|----------|--------|
| Workspace trust enforcement | MDM `WorkspaceTrustEnabled` | Require explicit trust for new workspaces |

### Sandbox Enforcement (Enterprise)

| Setting | Location | Effect |
|---------|----------|--------|
| Require sandbox | Dashboard → Security | Force sandbox for all agent sessions |
| Network allowlist/denylist | Dashboard → Security | Control outbound network access from sandbox |

---

## 3. Spend & Usage Governance

### Team-Level Spending

| Setting | Location | Effect |
|---------|----------|--------|
| Monthly team spending limit | Dashboard → Usage & Billing | Hard cap on team-wide AI usage |
| Admin-only limit changes | Dashboard → Usage & Billing | Prevent members from modifying limits |
| Usage-based pricing | Dashboard → Usage & Billing | Enable pay-per-use beyond base allocation |

### Per-Member Spending (Enterprise)

| Setting | Location | Effect |
|---------|----------|--------|
| Individual spending limits | Dashboard → Members | Per-user monthly caps |
| Group-based limits | Via SCIM directory sync | Apply limits per IdP group |
| Default per-member cap | Dashboard → Settings | Fallback limit for users without explicit assignment |

### Model Access Control

| Setting | Location | Effect |
|---------|----------|--------|
| Model allowlist | Dashboard → Settings → Models | Restrict which AI models users can access |
| Model blocklist | Dashboard → Settings → Models | Block specific models or providers |
| Provider restrictions | Dashboard → Settings → Models | Limit to approved providers only |

---

## 4. Rules & Configuration Management

### Team Rules

| Setting | Location | Effect |
|---------|----------|--------|
| Server-managed rules | Dashboard → Rules | Push rules to all team members' Cursor clients |
| Server-managed commands | Dashboard → Commands | Push approved commands to all clients |

### Team Marketplaces

| Setting | Location | Effect |
|---------|----------|--------|
| Import marketplace | Dashboard → Plugins | Add custom team marketplaces from GitHub |
| Marketplace limit | — | Business: 1 marketplace; Enterprise: unlimited |

---

## 5. Monitoring & Compliance

### Audit Logs (Enterprise)

| Event Category | Examples |
|----------------|----------|
| Authentication | Login, logout, SSO events |
| Team changes | Member added/removed, role changes |
| Permission updates | Security settings modified |
| API key actions | Key creation, revocation |
| Settings modifications | Any admin setting change |

Audit logs are tamper-proof and available via the dashboard.

### Analytics

| Metric | Plan |
|--------|------|
| Team usage overview | Business+ |
| Per-user usage breakdown | Business+ |
| AI code tracking (per-commit) | Enterprise |
| Conversation analytics | Enterprise |
| Accepted AI changes | Enterprise |

### Admin REST API

Available endpoints for programmatic integration:

| Endpoint Category | Capabilities |
|-------------------|-------------|
| Members | List, invite, remove, update roles |
| Usage | Retrieve usage metrics, spending data |
| Settings | Read/write team configuration |
| Audit | Query audit log entries |

---

## 6. MDM Deployment (Device-Level Enforcement)

### Available MDM Policies

| Policy Key | Type | Effect |
|------------|------|--------|
| `AllowedTeamId` | String | Lock login to specific team(s); comma-separated for multiple |
| `AllowedExtensions` | String (JSON) | Allowlist of permitted extension IDs |
| `WorkspaceTrustEnabled` | Boolean | Enforce workspace trust prompts |
| `UpdateMode` | String | Control updates: `"none"`, `"manual"`, `"start"`, `"default"`, `"silentlyApplyOnQuit"` |
| `NetworkDisableHttp2` | Boolean | Force HTTP/1.1 (for certain proxies) |

### macOS — Jamf / Kandji

**Domain:** `com.todesktop.230313mzl4w4u92`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>AllowedTeamId</key>
  <string>YOUR_TEAM_ID</string>
  <key>WorkspaceTrustEnabled</key>
  <true/>
  <key>UpdateMode</key>
  <string>manual</string>
  <key>AllowedExtensions</key>
  <string>{"esbenp.prettier-vscode": true, "dbaeumer.vscode-eslint": true}</string>
</dict>
</plist>
```

### Windows — Intune / Group Policy

**Path:** `HKLM\SOFTWARE\Policies\Cursor`

| Value | Type | Data |
|-------|------|------|
| `AllowedTeamId` | REG_SZ | Team ID string |
| `WorkspaceTrustEnabled` | REG_DWORD | `1` |
| `UpdateMode` | REG_SZ | `manual` |
| `AllowedExtensions` | REG_SZ | JSON string |

### Linux — Policy File

```bash
~/.cursor/policy.json
```

---

## 7. Organizations (Enterprise)

Cursor Organizations (launched June 2026) provides a company-level governance container:

| Capability | Description |
|------------|-------------|
| Multi-team management | Manage all teams from one dashboard |
| Spend rollup | View consolidated spend and token usage across teams; filter by team, user, service account, or cloud agent |
| Per-team governance | Separate security, budget, model access per team |
| Centralized audit | Organization-wide audit log aggregation |
| Feature settings per team | Enable/disable features independently per team |
| Organization Groups | Cross-team cohorts (e.g., Engineering, Contractors, Pilot Users) for org-wide policy |
| Organization API | Programmatic management of org-level settings |
| Reconciliation model | "Most permissive wins" when reconciling org-group and team-group settings |

### Organization Hierarchy

```
Organization (company-level container)
    ├── Organization Groups (cross-team cohorts for policy)
    ├── Team A (operating unit — department, region, etc.)
    │     ├── Directory Groups (SCIM-synced)
    │     ├── Members (with team-level roles)
    │     └── Team Settings (security, spend, models, features)
    ├── Team B
    │     └── ...
    └── Organization Settings (shared identity, admin, org-wide)
```

### Organization Roles

| Role | Scope | Capabilities |
|------|-------|-------------|
| Org Admin | Organization | Manage org settings, membership, shared identity, view all teams |
| Team Admin | Team | Manage team settings, members, team-level policies |
| Team Owner | Team | Full team access including billing |
| Member | Team | Use Cursor within team-defined policies |

---

## 8. Recommended Admin Configuration

### For regulated environments

- [ ] Enforce SSO with SAML and MFA
- [ ] Enable SCIM for automated user lifecycle
- [ ] Deploy `AllowedTeamId` via MDM to lock device logins
- [ ] Enable Privacy Mode (team-wide) with zero data retention
- [ ] Configure MCP server allowlist — block all unapproved servers
- [ ] Set extension allowlist via dashboard and MDM
- [ ] Require sandbox for all agent sessions
- [ ] Set strict spending limits per user
- [ ] Block BYOK to prevent unauthorized model access
- [ ] Enable audit logs and route to SIEM
- [ ] Restrict Cloud Agent and CLI access to approved users

### For standard enterprise teams

- [ ] Enable SSO (enforce for all)
- [ ] Configure Privacy Mode
- [ ] Set team-level spending limits with admin-only modification
- [ ] Configure model allowlist (approved providers only)
- [ ] Set extension allowlist via dashboard
- [ ] Deploy MCP server allowlist for approved integrations
- [ ] Review analytics monthly
- [ ] Deploy `WorkspaceTrustEnabled: true` via MDM

### For developer-focused teams

- [ ] Enable SSO (optional enforcement)
- [ ] Set reasonable spending limits
- [ ] Use model allowlist to control costs
- [ ] Configure Team Rules for security guidelines
- [ ] Import approved team marketplaces
- [ ] Review usage analytics quarterly

---

## Cross-References

- **Managed config files:** [`../cursor/`](../cursor/) — Drop-in `permissions.json` and `settings.json`
- **MDM guide:** [`../cursor/examples/mdm-policies.md`](../cursor/examples/mdm-policies.md)
- **Security rules:** [`../cursor/rules/security.mdc`](../cursor/rules/security.mdc)
- **Cloud Agent security:** [`../cursor/examples/cloud-agent-security.json`](../cursor/examples/cloud-agent-security.json)

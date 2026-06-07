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

### Plans

| Capability | Teams (Business) | Enterprise |
|------------|------------------|------------|
| SSO (SAML/OIDC) | ✓ | ✓ |
| SCIM Provisioning | — | ✓ |
| Audit Logs | — | ✓ |
| Service Accounts | — | ✓ |
| Billing Groups | — | ✓ |
| Cursor Blame | — | ✓ |
| AI Code Tracking API | — | ✓ |
| Conversation Insights | — | ✓ |
| Organizations (multi-team) | — | ✓ |

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
| Soft spending limits | Dashboard → Usage & Billing | Warn but don't block users at limit |
| Automated alerts | Dashboard → Usage & Billing | Notify users at 50%, 80%, and 100% of limits |
| Admin-only limit changes | Dashboard → Usage & Billing | Prevent members from modifying limits |
| Usage-based pricing | Dashboard → Usage & Billing | Enable pay-per-use beyond base allocation |
| Pooled usage (Enterprise) | Dashboard → Usage & Billing | Shared pool with admin-only controls |

### Per-Member Spending (Enterprise)

| Setting | Location | Effect |
|---------|----------|--------|
| Individual spending limits | Dashboard → Members | Per-user monthly caps |
| Group-based limits | Via SCIM directory sync | Apply limits per IdP group |
| Default per-member cap | Dashboard → Settings | Fallback limit for users without explicit assignment |

### Billing Groups (Enterprise)

| Setting | Location | Effect |
|---------|----------|--------|
| Create billing groups | Dashboard → Members & Groups | Organize members into cost centers |
| Assign via SCIM | Dashboard → Members & Groups | Sync billing groups with IdP groups |
| Assign via API | Admin API | Programmatic group management |
| Assign via CSV | Dashboard → Members & Groups | Bulk upload group assignments |
| Manual assignment | Dashboard → Members & Groups | Select unassigned members to add |
| Per-group spend tracking | Dashboard → Members & Groups | View spend per billing group |
| Move members | Dashboard → Members & Groups | Reassign members between groups |

### Model Access Control

| Setting | Location | Effect |
|---------|----------|--------|
| Model allowlist | Dashboard → Settings → Models | Restrict which AI models users can access |
| Model blocklist | Dashboard → Settings → Models | Block specific models or providers |
| Provider restrictions | Dashboard → Settings → Models | Limit to approved providers only |
| Block new providers by default | Dashboard → Settings → Models | Auto-block newly added providers until admin review |
| Block new model versions by default | Dashboard → Settings → Models | Auto-block new versions until admin approval |
| Speed/context window restrictions | Dashboard → Settings → Models | Block specific model configurations by capability |

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
| Usage breakdown by product surface | Business+ |
| AI code tracking (per-commit) | Enterprise |
| Conversation Insights | Enterprise |
| Accepted AI changes | Enterprise |
| Cursor Blame (AI vs. human attribution) | Enterprise |

### Product Surface Analytics

Admins can filter usage by product surface:

| Surface | Description |
|---------|-------------|
| Clients | IDE-based usage (completions, chat, composer) |
| Cloud Agents | Background agent usage |
| Automations | Automated workflow usage |
| Bugbot | Automated bug detection runs |
| Security Review | Security analysis runs |

### Service Accounts (Enterprise)

| Setting | Location | Effect |
|---------|----------|--------|
| Create service accounts | Dashboard → Service Accounts | Non-human accounts for automation |
| API key management | Dashboard → Service Accounts | Generate/rotate keys per account |
| Usage attribution | Analytics | Service account usage tracked in team analytics |
| Cloud Agent invocation | Via API | Service accounts can invoke cloud agents |
| No seat consumption | — | Included at no extra cost, no seat license required |

### Admin REST API

Available endpoints for programmatic integration:

| Endpoint Category | Capabilities |
|-------------------|-------------|
| Members | List, invite, remove, update roles |
| Usage | Retrieve usage metrics, spending data |
| Settings | Read/write team configuration |
| Audit | Query audit log entries |
| Billing Groups | Create, manage, assign members |
| Service Accounts | Create, manage, rotate keys |

### Analytics API (Enterprise)

| Capability | Description |
|------------|-------------|
| Usage metrics export | Programmatic access to all analytics data |
| Per-user breakdown | Drill down to individual usage patterns |
| Product surface filtering | Filter by clients, Cloud Agents, automations |
| Integration support | Export to external analytics platforms |

### AI Code Tracking API (Enterprise)

| Capability | Description |
|------------|-------------|
| Per-commit attribution | Track AI-assisted vs. human-written code |
| Repository-level metrics | AI adoption rate per repository |
| Cursor Blame | AI-aware git blame in Cursor client |

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
| Spend rollup | View consolidated spend and token usage across teams |
| Per-team governance | Separate security, budget, model access per team |
| Centralized audit | Organization-wide audit log aggregation |
| Feature settings per team | Enable/disable features independently per team |
| Organization-level IDP management | Single SSO/SCIM configuration across all teams |
| Organization-level analytics | Usage analytics with drill-down to each team |
| Multi-team membership | Users can be on multiple teams at once |
| Cross-team user management | Move users between teams via dashboard, API, or CSV |
| Settings inheritance | New users joining a team inherit settings automatically |

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
- [ ] Set strict spending limits per user (hard caps)
- [ ] Block BYOK to prevent unauthorized model access
- [ ] Block new providers and model versions by default
- [ ] Enable audit logs and route to SIEM
- [ ] Restrict Cloud Agent and CLI access to approved users
- [ ] Create billing groups for cost attribution
- [ ] Configure service accounts for CI/CD (no personal accounts for automation)
- [ ] Enable AI Code Tracking for compliance reviews
- [ ] Deploy repository blocklist for sensitive repos

### For standard enterprise teams

- [ ] Enable SSO (enforce for all)
- [ ] Configure Privacy Mode
- [ ] Set team-level spending limits with soft limits and automated alerts
- [ ] Configure model allowlist (approved providers only)
- [ ] Set extension allowlist via dashboard
- [ ] Deploy MCP server allowlist for approved integrations
- [ ] Create billing groups for department-level cost tracking
- [ ] Set up service accounts for automated workflows
- [ ] Review analytics monthly (filter by product surface)
- [ ] Deploy `WorkspaceTrustEnabled: true` via MDM
- [ ] Enable Conversation Insights for development pattern analysis
- [ ] Use Cursor Blame to track AI code attribution

### For developer-focused teams

- [ ] Enable SSO (optional enforcement)
- [ ] Set reasonable spending limits (soft limits recommended)
- [ ] Use model allowlist to control costs
- [ ] Configure Team Rules for security guidelines
- [ ] Import approved team marketplaces
- [ ] Review usage analytics quarterly
- [ ] Set up billing groups if tracking cost per project

---

## Cross-References

- **Managed config files:** [`../cursor/`](../cursor/) — Drop-in `permissions.json` and `settings.json`
- **MDM guide:** [`../cursor/examples/mdm-policies.md`](../cursor/examples/mdm-policies.md)
- **Security rules:** [`../cursor/rules/security.mdc`](../cursor/rules/security.mdc)
- **Cloud Agent security:** [`../cursor/examples/cloud-agent-security.json`](../cursor/examples/cloud-agent-security.json)

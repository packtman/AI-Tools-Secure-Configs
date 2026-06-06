# Claude (Desktop & Web) — Admin Controls Reference

## Overview

Anthropic provides centralized admin controls for Claude through the **Claude.ai Admin Console**, available to organizations on **Claude for Teams** and **Claude for Enterprise** plans. Admins manage identity, feature access, data policies, and managed settings that override all user-level configuration.

Claude Desktop inherits organizational policy from the admin console and can additionally be controlled via MDM (macOS/Windows) for device-level enforcement.

---

## Admin Console Access

| URL | Who can access |
|-----|----------------|
| `claude.ai` → Admin Settings | Primary Owner, Admin roles |

### Roles

| Role | Capabilities |
|------|-------------|
| **Primary Owner** | Full admin access including billing, SSO, org deletion |
| **Admin** | Manage users, policies, audit logs (no billing) |
| **Member** | Use Claude within admin-defined policies |

---

## 1. Identity & Access Management

### SSO (SAML 2.0 / OIDC)

| Setting | Location | Notes |
|---------|----------|-------|
| Enable SSO | Admin Settings → Security → SSO | Supports Okta, Azure AD (Entra ID), Auth0, Google Workspace |
| Enforce SSO | Admin Settings → Security → SSO | When enforced, disables email/password login |
| IdP group mapping | Admin Settings → Security → SSO | Map IdP groups to Claude roles |

### Domain Management

| Setting | Location | Notes |
|---------|----------|-------|
| Domain verification | Admin Settings → Security → Domains | Prove ownership via DNS TXT record |
| Domain capture | Admin Settings → Security → Domains | Auto-claim users with matching email domain |
| External invite restriction | Admin Settings → Security → Domains | Block invites to non-verified domains |

### User Provisioning

| Setting | Location | Notes |
|---------|----------|-------|
| SCIM provisioning | Admin Settings → Security → SCIM | Enterprise only; auto-sync users from IdP |
| Manual invite | Admin Settings → Members | Email-based invite with role assignment |
| Seat management | Admin Settings → Members | Assign/remove seats, view usage |

---

## 2. Feature Governance (Managed Settings)

Managed settings are delivered from the admin console and override all local configuration. They apply uniformly to all users in the organization.

### Admin Console → Claude Code → Managed Settings

These settings control Claude Code and Claude Desktop behavior:

| Setting Key | Type | Effect |
|-------------|------|--------|
| `permissions.allow` | Array | Tools/commands always allowed without prompting |
| `permissions.deny` | Array | Tools/commands permanently blocked |
| `allowedTools` | Array | Restrict available tool categories |
| `disabledTools` | Array | Specific tools to disable |
| `allowedMcpServers` | Array | MCP server allowlist (blocks all others) |
| `deniedMcpServers` | Array | MCP server denylist |
| `allowBypassPermissions` | Boolean | Allow `--dangerously-skip-permissions` flag |
| `allowAutoPermissions` | Boolean | Allow auto-accept mode |
| `channelsEnabled` | Boolean | Allow Claude channels feature |
| `terminalCommandTimeout` | Integer | Max seconds for terminal commands |

### Claude Desktop–Specific Policy Keys

These are deployed via MDM or the admin console for Claude Desktop:

| Key | Type | Effect |
|-----|------|--------|
| `isLocalDevMcpEnabled` | Boolean | Allow users to configure local MCP servers |
| `isDesktopExtensionEnabled` | Boolean | Allow desktop extensions |
| `isDesktopExtensionDirectoryEnabled` | Boolean | Allow access to extension directory |
| `isClaudeCodeForDesktopEnabled` | Boolean | Allow Claude Code access via desktop |
| `secureVmFeaturesEnabled` | Boolean | Allow Cowork (computer use sandbox) |
| `disableAutoUpdates` | Boolean | Disable automatic updates |
| `autoUpdaterEnforcementHours` | Integer | Hours before force-restart for pending update (1–72) |

---

## 3. Data Governance

### Data & Privacy Settings

| Setting | Location | Effect |
|---------|----------|--------|
| Training opt-out | Automatic on Team/Enterprise | Conversations never used for model training |
| Data retention | Admin Settings → Data & Privacy | Configure retention window or indefinite |
| Conversation history | Admin Settings → Data & Privacy | Control whether history is stored server-side |

### Data Residency (Enterprise)

| Region | Availability |
|--------|-------------|
| United States | Default |
| Europe (EU) | Available on Enterprise |

### Compliance

| Certification | Plan |
|---------------|------|
| SOC 2 Type II | Team+ |
| HIPAA (BAA available) | Enterprise |

---

## 4. Monitoring & Audit

### Audit Logs (Enterprise)

| Event Category | Examples |
|----------------|----------|
| Authentication | Login, logout, SSO events, failed attempts |
| Admin actions | Settings changes, role assignments, policy updates |
| User activity | Conversation creation, tool usage, file uploads |
| Security events | Permission changes, API key actions |

### Usage Analytics

| Metric | Available on |
|--------|-------------|
| Active users | Team+ |
| Messages per user | Team+ |
| Model usage breakdown | Team+ |
| Cost per user/team | Enterprise |

---

## 5. MDM Deployment (Device-Level Enforcement)

For organizations requiring device-level policy enforcement beyond the admin console:

### macOS — Managed Preferences

**Domain:** `com.anthropic.claudefordesktop`

Deploy via Jamf, Kandji, Mosyle, or any MDM supporting configuration profiles.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>isLocalDevMcpEnabled</key>
  <false/>
  <key>isDesktopExtensionEnabled</key>
  <false/>
  <key>isClaudeCodeForDesktopEnabled</key>
  <false/>
  <key>secureVmFeaturesEnabled</key>
  <false/>
  <key>disableAutoUpdates</key>
  <false/>
  <key>autoUpdaterEnforcementHours</key>
  <integer>24</integer>
</dict>
</plist>
```

### Windows — Registry / Intune

**Path:** `HKLM\SOFTWARE\Policies\Claude`

| Value | Type | Data |
|-------|------|------|
| `isLocalDevMcpEnabled` | REG_DWORD | `0` |
| `isDesktopExtensionEnabled` | REG_DWORD | `0` |
| `isClaudeCodeForDesktopEnabled` | REG_DWORD | `0` |
| `secureVmFeaturesEnabled` | REG_DWORD | `0` |
| `disableAutoUpdates` | REG_DWORD | `0` |
| `autoUpdaterEnforcementHours` | REG_DWORD | `24` |

---

## 6. Settings Precedence

Claude enforces a strict hierarchy where admin controls always win:

```
Server-managed settings (Admin Console)     ← Highest priority
    ↓
MDM / OS-level policies (plist, registry)
    ↓
File-based managed settings (managed-settings.json)
    ↓
User-level settings (~/.claude/)
    ↓
Project-level settings (.claude/)            ← Lowest priority
```

Within the managed tier, the first source delivering a non-empty configuration wins. Sources do not merge across tiers.

---

## 7. Recommended Admin Configuration

### For regulated environments (finance, healthcare)

- [ ] Enforce SSO with MFA via IdP
- [ ] Enable SCIM for automated provisioning
- [ ] Set `isLocalDevMcpEnabled: false` — block user-added MCP servers
- [ ] Set `isDesktopExtensionEnabled: false` — disable all extensions
- [ ] Set `secureVmFeaturesEnabled: false` — disable computer use sandbox
- [ ] Set `allowBypassPermissions: false` — prevent permission bypass mode
- [ ] Set `allowAutoPermissions: false` — require manual approval for each tool
- [ ] Deploy approved MCP servers via `allowedMcpServers` list only
- [ ] Configure data retention per compliance requirements
- [ ] Route audit logs to SIEM
- [ ] Set `autoUpdaterEnforcementHours: 24` — force updates within 24 hours

### For standard enterprise teams

- [ ] Enable SSO (enforce for all users)
- [ ] Set `isDesktopExtensionEnabled: false` until extensions are vetted
- [ ] Configure `allowedMcpServers` with approved servers
- [ ] Set `allowBypassPermissions: false`
- [ ] Review usage analytics monthly
- [ ] Set `autoUpdaterEnforcementHours: 48`

### For developer-focused organizations

- [ ] Enable SSO (optional enforcement)
- [ ] Allow MCP servers but deploy `deniedMcpServers` for known-risky packages
- [ ] Set `allowBypassPermissions: false` (even for devs)
- [ ] Enable usage analytics for cost management
- [ ] Set `autoUpdaterEnforcementHours: 72`

---

## Cross-References

- **Managed config files:** [`../claude-desktop/`](../claude-desktop/) — Drop-in `claude_desktop_config.json` templates
- **MDM guides:** [`../claude-desktop/examples/mdm-macos-profile.md`](../claude-desktop/examples/mdm-macos-profile.md), [`mdm-windows-gpo.md`](../claude-desktop/examples/mdm-windows-gpo.md)
- **Claude Code managed settings:** [`../claude-code/managed-settings.json`](../claude-code/managed-settings.json)
- **Policy rationale:** [`../claude-desktop/examples/policy-rationale.md`](../claude-desktop/examples/policy-rationale.md)

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
| **Owner** | Manage users, policies, managed settings, audit logs |
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
| `permissions.disableBypassPermissionsMode` | String | Set to `"disable"` to prevent `--dangerously-skip-permissions` |
| `permissions.disableAutoMode` | String | Set to `"disable"` to prevent auto mode activation |
| `allowManagedPermissionRulesOnly` | Boolean | Only managed permission rules apply; user/project rules ignored |
| `allowedMcpServers` | Array | MCP server allowlist (blocks all others) |
| `deniedMcpServers` | Array | MCP server denylist |
| `allowManagedMcpServersOnly` | Boolean | Only managed MCP server lists apply |
| `channelsEnabled` | Boolean | Allow Claude channels feature |
| `forceRemoteSettingsRefresh` | Boolean | Block CLI startup until remote settings fetched; exit if fetch fails (fail-closed) |

### Sandbox Settings (Claude Code)

| Setting Key | Type | Effect |
|-------------|------|--------|
| `sandbox.enabled` | Boolean | Enable OS-level filesystem and network isolation |
| `sandbox.network.allowedDomains` | Array | Domain allowlist for network access within sandbox |
| `sandbox.failIfUnavailable` | Boolean | Exit CLI if sandbox cannot initialize (instead of warning) |
| `sandbox.allowUnsandboxedCommands` | Boolean | Set to `false` to block the `dangerouslyDisableSandbox` escape hatch |
| `sandbox.allowManagedReadPathsOnly` | Boolean | Only managed `allowRead` entries honored; user/project entries ignored |
| `sandbox.allowManagedDomainsOnly` | Boolean | Only managed domain entries honored |

### Hook & Plugin Controls (Claude Code)

| Setting Key | Type | Effect |
|-------------|------|--------|
| `allowManagedHooksOnly` | Boolean | Only managed hooks load; user/project hooks ignored |
| `allowedHttpHookUrls` | Array | Restrict HTTP hook URLs to approved endpoints |
| `strictKnownMarketplaces` | Boolean | Restrict plugin sources to known/approved marketplaces |
| `blockedMarketplaces` | Array | Block specific plugin marketplace sources |
| `allowPluginOnlyCustomization` | Boolean | Block skills, agents, hooks, MCP from user/project sources |

### Policy Helper (Claude Code — MDM/File only)

| Setting Key | Type | Effect |
|-------------|------|--------|
| `policyHelper` | Object | Admin-deployed executable that computes managed settings dynamically |
| `policyHelper.path` | String | Absolute path to helper executable |
| `policyHelper.timeoutMs` | Number | Timeout for helper execution |
| `policyHelper.refreshIntervalMs` | Number | How often to re-run helper (min 60000, 0 to disable) |

> **Note:** `policyHelper` is only honored from MDM or system `managed-settings.json` file. Ignored in user settings, project settings, HKCU registry, and server-managed settings. Requires Claude Code v2.1.136+.

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
| `forceLoginOrgUUID` | String | Pin sign-in to a specific organization (prevents redirect to personal/unmanaged accounts) |

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

## 4. Spend Controls & Seat Management

### Spend Governance

| Setting | Location | Effect |
|---------|----------|--------|
| Organization-level budget | Admin Console → Billing | Hard monthly ceiling for total spend |
| Per-user spending caps | Admin Console → Members | Individual user spending limits |
| Extra usage enablement | Admin Console → Members | Allow extra usage at standard API rates |
| Per-user extra usage cap | Admin Console → Members | Maximum extra usage amount per user |

### Seat Management

| Setting | Location | Effect |
|---------|----------|--------|
| Self-serve seat purchase | Admin Console → Billing | Admins can buy additional seats directly |
| Seat allocation | Admin Console → Members | Assign/remove seats per user |
| Premium seats (Claude Code) | Admin Console → Members | Upgrade users to premium seats with Claude Code |

### Workspace Segmentation (Enterprise)

| Setting | Location | Effect |
|---------|----------|--------|
| Multiple workspaces | Admin Console | Up to 100 workspaces per organization |
| Per-workspace spend limits | Admin Console → Workspace | Cannot exceed org-level limits |
| Per-workspace rate limits | Admin Console → Workspace | RPM, input/output tokens per model |
| Per-workspace data residency | Admin Console → Workspace | Set at creation (immutable) |

---

## 5. Monitoring & Audit

### Compliance API (Enterprise)

| Capability | Description |
|------------|-------------|
| Real-time usage access | Programmatic access to Claude usage data and customer content |
| Activity log export | Export admin action logs and user activity |
| Automated policy enforcement | Build continuous monitoring and flagging systems |
| Selective data deletion | Delete sensitive data per retention requirements |
| Data retention | Activity data retained for 6 years |
| SIEM integration | Route to Splunk, Sentinel, Chronicle, etc. |

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
| Claude Code analytics | Team+ |
| Lines of code accepted | Team+ |
| User adoption metrics | Team+ |

---

## 6. MDM Deployment (Device-Level Enforcement)

For organizations requiring device-level policy enforcement beyond the admin console:

### Claude Desktop — macOS Managed Preferences

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
  <key>forceLoginOrgUUID</key>
  <string>YOUR_ORG_UUID</string>
</dict>
</plist>
```

### Claude Desktop — Windows Registry / Intune

**Path:** `HKLM\SOFTWARE\Policies\Claude`

| Value | Type | Data |
|-------|------|------|
| `isLocalDevMcpEnabled` | REG_DWORD | `0` |
| `isDesktopExtensionEnabled` | REG_DWORD | `0` |
| `isClaudeCodeForDesktopEnabled` | REG_DWORD | `0` |
| `secureVmFeaturesEnabled` | REG_DWORD | `0` |
| `disableAutoUpdates` | REG_DWORD | `0` |
| `autoUpdaterEnforcementHours` | REG_DWORD | `24` |
| `forceLoginOrgUUID` | REG_SZ | `YOUR_ORG_UUID` |

### Claude Code — macOS Managed Preferences

**Domain:** `com.anthropic.claudecode`

Deploy Claude Code policy independently from Claude Desktop:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Settings</key>
  <string>{"permissions":{"disableBypassPermissionsMode":"disable","disableAutoMode":"disable"},"allowManagedPermissionRulesOnly":true,"sandbox":{"enabled":true,"failIfUnavailable":true}}</string>
</dict>
</plist>
```

### Claude Code — Windows Registry / Intune

**Path:** `HKLM\SOFTWARE\Policies\ClaudeCode`

| Value | Type | Data |
|-------|------|------|
| `Settings` | REG_SZ | JSON string containing managed settings |

### Claude Code — File-Based Managed Settings

| Platform | Path |
|----------|------|
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Linux / WSL | `/etc/claude-code/managed-settings.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` |

> **Note:** On Windows, `wslInheritsWindowsSettings: true` (set in HKLM or file-based) makes WSL Claude Code read the Windows policy chain in addition to `/etc/claude-code`.

---

## 7. Settings Precedence

Claude enforces a strict hierarchy where admin controls always win:

```
Server-managed settings (Admin Console)     ← Highest priority
    ↓
MDM / OS-level policies (plist, HKLM registry)
    ↓
File-based managed settings (managed-settings.json + managed-settings.d/*.json)
    ↓
Windows user registry (HKCU — lowest managed tier)
    ↓
Command-line arguments (session overrides)
    ↓
Local project settings (.claude/settings.local.json)
    ↓
Shared project settings (.claude/settings.json)
    ↓
User-level settings (~/.claude/settings.json)   ← Lowest priority
```

Within the managed tier, the first source delivering a non-empty configuration wins. Sources do not merge across tiers. Within the file-based tier, the base file and drop-in fragments (`managed-settings.d/*.json`) merge together.

Array settings (`permissions.allow`, `permissions.deny`, MCP servers) merge entries from all sources — developers can extend managed lists but cannot remove from them.

---

## 8. Recommended Admin Configuration

### For regulated environments (finance, healthcare)

- [ ] Enforce SSO with MFA via IdP
- [ ] Enable SCIM for automated provisioning
- [ ] Set `forceLoginOrgUUID` via MDM — pin sign-in to organization
- [ ] Set `isLocalDevMcpEnabled: false` — block user-added MCP servers
- [ ] Set `isDesktopExtensionEnabled: false` — disable all extensions
- [ ] Set `secureVmFeaturesEnabled: false` — disable computer use sandbox
- [ ] Set `permissions.disableBypassPermissionsMode: "disable"` — prevent permission bypass mode
- [ ] Set `permissions.disableAutoMode: "disable"` — require manual approval for each tool
- [ ] Set `forceRemoteSettingsRefresh: true` — fail-closed enforcement
- [ ] Set `sandbox.enabled: true` with `sandbox.failIfUnavailable: true`
- [ ] Set `allowManagedHooksOnly: true` — block user-defined hooks
- [ ] Set `strictKnownMarketplaces: true` — restrict plugin sources
- [ ] Deploy approved MCP servers via `allowedMcpServers` list only
- [ ] Configure organization and per-user spend caps
- [ ] Configure data retention per compliance requirements
- [ ] Enable Compliance API and route to SIEM
- [ ] Set `autoUpdaterEnforcementHours: 24` — force updates within 24 hours
- [ ] Deploy `policyHelper` for dynamic policy based on device posture (if needed)

### For standard enterprise teams

- [ ] Enable SSO (enforce for all users)
- [ ] Set `forceLoginOrgUUID` via MDM
- [ ] Set `isDesktopExtensionEnabled: false` until extensions are vetted
- [ ] Configure `allowedMcpServers` with approved servers
- [ ] Set `permissions.disableBypassPermissionsMode: "disable"`
- [ ] Set `forceRemoteSettingsRefresh: true`
- [ ] Enable sandbox with network domain allowlist
- [ ] Set organization-level spend caps
- [ ] Review usage analytics monthly
- [ ] Set `autoUpdaterEnforcementHours: 48`
- [ ] Configure Compliance API for quarterly reviews

### For developer-focused organizations

- [ ] Enable SSO (optional enforcement)
- [ ] Allow MCP servers but deploy `deniedMcpServers` for known-risky packages
- [ ] Set `permissions.disableBypassPermissionsMode: "disable"` (even for devs)
- [ ] Enable usage analytics for cost management
- [ ] Set reasonable per-user spend caps
- [ ] Set `autoUpdaterEnforcementHours: 72`

---

## Cross-References

- **Managed config files:** [`../claude-desktop/`](../claude-desktop/) — Drop-in `claude_desktop_config.json` templates
- **MDM guides:** [`../claude-desktop/examples/mdm-macos-profile.md`](../claude-desktop/examples/mdm-macos-profile.md), [`mdm-windows-gpo.md`](../claude-desktop/examples/mdm-windows-gpo.md)
- **Claude Code managed settings:** [`../claude-code/managed-settings.json`](../claude-code/managed-settings.json)
- **Policy rationale:** [`../claude-desktop/examples/policy-rationale.md`](../claude-desktop/examples/policy-rationale.md)

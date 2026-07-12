# Claude Desktop — Enterprise Policy Deployment Guide

## Overview

Claude Desktop supports enterprise-managed policies that override user preferences. These are deployed via Mobile Device Management (MDM) solutions and cannot be changed by end users.

---

## macOS — Managed Preferences

### Domain

```
com.anthropic.claudefordesktop
```

### Deployment via MDM (Jamf, Kandji, Mosyle, etc.)

Create a configuration profile with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `isLocalDevMcpEnabled` | Boolean | `false` to block local MCP servers |
| `isDesktopExtensionEnabled` | Boolean | `false` to disable desktop extensions |
| `isDesktopExtensionDirectoryEnabled` | Boolean | `false` to block access to extension directory |
| `isClaudeCodeForDesktopEnabled` | Boolean | `false` to disable Claude Code access via desktop |
| `secureVmFeaturesEnabled` | Boolean | `false` to disable Cowork (computer use sandbox) |
| `disableAutoUpdates` | Boolean | `true` to disable automatic updates |
| `autoUpdaterEnforcementHours` | Integer | Hours before force-restart for pending update (1–72) |

### Example plist payload

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
  <key>isDesktopExtensionDirectoryEnabled</key>
  <false/>
  <key>isClaudeCodeForDesktopEnabled</key>
  <true/>
  <key>secureVmFeaturesEnabled</key>
  <false/>
  <key>disableAutoUpdates</key>
  <false/>
  <key>autoUpdaterEnforcementHours</key>
  <integer>24</integer>
</dict>
</plist>
```

### Verification

```bash
defaults read com.anthropic.claudefordesktop
```

---

## Windows — Group Policy / Intune

### Registry paths

**Machine-wide (HKLM):**
```
HKLM\SOFTWARE\Policies\Claude
```

**Per-user (HKCU):**
```
HKCU\SOFTWARE\Policies\Claude
```

Machine-wide policies override per-user policies.

### Registry values

| Value name | Type | Data | Effect |
|------------|------|------|--------|
| `isLocalDevMcpEnabled` | REG_DWORD | `0` | Disable local MCP servers |
| `isDesktopExtensionEnabled` | REG_DWORD | `0` | Disable desktop extensions |
| `isDesktopExtensionDirectoryEnabled` | REG_DWORD | `0` | Block access to extension directory |
| `isClaudeCodeForDesktopEnabled` | REG_DWORD | `0` | Disable Claude Code access via desktop |
| `secureVmFeaturesEnabled` | REG_DWORD | `0` | Disable Cowork (computer use sandbox) |
| `disableAutoUpdates` | REG_DWORD | `1` | Disable automatic updates |
| `autoUpdaterEnforcementHours` | REG_DWORD | `24` | Hours before force-restart for pending update |

### Deployment via Intune

1. Create a new Configuration Profile → Custom → OMA-URI.
2. Add OMA-URI entries for each registry value.
3. Assign the profile to the appropriate device group.

---

## Security Recommendations

### For maximum lockdown (regulated environments)

1. Set `isLocalDevMcpEnabled = false` — prevents users from adding arbitrary MCP servers.
2. Set `isDesktopExtensionEnabled = false` — disables all desktop extensions.
3. Set `isDesktopExtensionDirectoryEnabled = false` — blocks extension discovery.
4. Set `secureVmFeaturesEnabled = false` — disables computer use sandbox.
5. Set `autoUpdaterEnforcementHours = 24` — force update within 24 hours.
6. Deploy a pre-approved `claude_desktop_config.json` via MDM with only vetted MCP servers.
7. Set the config file to read-only to prevent user modification.
8. Use server-managed settings from the admin console for highest-priority enforcement.

### For development environments

1. Allow MCP servers (`isLocalDevMcpEnabled = true`) but deploy a curated allowlist.
2. Set `isClaudeCodeForDesktopEnabled = true` — allow Claude Code access.
3. Set `secureVmFeaturesEnabled = false` until Cowork is vetted.
4. Set `autoUpdaterEnforcementHours = 48` — allow reasonable update window.
5. Provide a sanctioned `claude_desktop_config.json` with pre-approved servers.
6. Instruct developers to request security review for additional MCP servers.
7. Monitor tool permission grants through periodic audits.

# Cline — MDM and Enterprise Deployment Guide

This document covers how to deploy and enforce Cline security settings across an organization using MDM (Jamf, Intune, Kandji), group policy, or configuration management tools (Ansible, Chef, Puppet).

## Deployment Approaches

| Method | Best for | Override risk |
|--------|----------|---------------|
| MDM-managed VS Code settings | macOS/Windows fleets with Jamf or Intune | Low — MDM settings override user settings on managed devices |
| VS Code workspace settings | Per-repository enforcement | Medium — developers can override in user settings |
| Environment variables | API key management | Low — set at OS level, not visible in settings files |
| Dotfiles / config management | Developer workstations without MDM | Medium — relies on correct deployment |

---

## 1. VS Code Settings Deployment via MDM

VS Code settings can be enforced via MDM using platform-native configuration profiles.

### macOS (Jamf / Kandji)

Create a custom settings profile or use a script to write to the managed VS Code settings location:

```bash
# Script: deploy-cline-settings.sh
# Deploys Cline security settings to all user accounts on a managed Mac.

SETTINGS_DIR="$HOME/Library/Application Support/Code/User"
SETTINGS_FILE="$SETTINGS_DIR/settings.json"
BACKUP_FILE="$SETTINGS_DIR/settings.json.bak.$(date +%Y%m%d)"

# Back up existing settings
if [ -f "$SETTINGS_FILE" ]; then
    cp "$SETTINGS_FILE" "$BACKUP_FILE"
fi

# Merge Cline security settings using jq
SECURITY_SETTINGS='{
  "cline.alwaysAllowReadOnly": false,
  "cline.alwaysAllowReadOnlyOutsideWorkspace": false,
  "cline.alwaysAllowWrite": false,
  "cline.alwaysAllowWriteOutsideWorkspace": false,
  "cline.alwaysAllowExecute": false,
  "cline.alwaysAllowBrowser": false,
  "cline.alwaysAllowMcp": false,
  "cline.browserToolEnabled": false,
  "cline.telemetrySetting": "disabled"
}'

if command -v jq &>/dev/null; then
    jq -s '.[0] * .[1]' "$SETTINGS_FILE" <(echo "$SECURITY_SETTINGS") > "$SETTINGS_FILE.tmp"
    mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
else
    echo "jq not found — install jq or deploy settings manually"
    exit 1
fi
```

### Windows (Intune / Group Policy)

Deploy settings via PowerShell script in Intune:

```powershell
# Script: Deploy-ClineSettings.ps1
$settingsDir = "$env:APPDATA\Code\User"
$settingsFile = "$settingsDir\settings.json"

$securitySettings = @{
    "cline.alwaysAllowReadOnly" = $false
    "cline.alwaysAllowReadOnlyOutsideWorkspace" = $false
    "cline.alwaysAllowWrite" = $false
    "cline.alwaysAllowWriteOutsideWorkspace" = $false
    "cline.alwaysAllowExecute" = $false
    "cline.alwaysAllowBrowser" = $false
    "cline.alwaysAllowMcp" = $false
    "cline.browserToolEnabled" = $false
    "cline.telemetrySetting" = "disabled"
}

if (Test-Path $settingsFile) {
    $existing = Get-Content $settingsFile | ConvertFrom-Json -AsHashtable
    foreach ($key in $securitySettings.Keys) {
        $existing[$key] = $securitySettings[$key]
    }
    $existing | ConvertTo-Json -Depth 10 | Set-Content $settingsFile
} else {
    New-Item -ItemType Directory -Force -Path $settingsDir
    $securitySettings | ConvertTo-Json -Depth 10 | Set-Content $settingsFile
}
```

---

## 2. Extension Allowlist

To prevent developers from uninstalling Cline's security settings or installing unauthorized AI extensions, use VS Code's extension management:

### Restricting Extensions via Intune

In VS Code's managed settings, you can control extensions:

```json
{
  "extensions.autoUpdate": false,
  "extensions.autoCheckUpdates": false,
  "extensions.ignoreRecommendations": true
}
```

For full extension allowlisting, use VS Code Server policies or enforce via MDM shell scripts that check installed extensions and remove unauthorized ones.

---

## 3. API Key Management

**Never deploy API keys via MDM or in settings files.** Use one of these approaches:

### Environment Variables (Recommended)

Set at the OS level so VS Code inherits them on launch:

```bash
# macOS: add to /etc/launchd.conf or a LaunchAgent plist
# Linux: add to /etc/environment
export ANTHROPIC_API_KEY="$(security find-generic-password -a cline -s anthropic-api-key -w)"

# Windows: Set via System Properties > Environment Variables
```

### Secrets Manager Integration

For enterprise deployments, pull secrets from a vault at session start:

```bash
# Example: pull from HashiCorp Vault at login
export ANTHROPIC_API_KEY=$(vault kv get -field=api_key secret/cline/anthropic)
```

---

## 4. MCP Server Policy

To prevent developers from adding unauthorized MCP servers, manage the Cline MCP settings file via MDM:

### Lock the MCP Settings File

```bash
# macOS: Deploy a read-only MCP settings file
MCP_FILE="$HOME/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
mkdir -p "$(dirname "$MCP_FILE")"
cp /path/to/approved/cline_mcp_settings.json "$MCP_FILE"
chmod 444 "$MCP_FILE"  # Read-only
```

For environments where developers need to add servers, use a review process: developers propose MCP server additions via pull request to the org's Cline config repo, and IT reviews and deploys approved changes.

---

## 5. Monitoring and Audit

### Task History Location

Cline stores task history (including all AI interactions, file reads/writes, and commands) at:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/` |
| Linux | `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/` |
| Windows | `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\tasks\` |

For compliance, collect and retain these logs. Each task directory contains:
- `api_conversation_history.json` — Full LLM conversation (may contain code and prompts)
- `ui_messages.json` — User-visible messages and approvals/denials
- `task_metadata.json` — Timestamp, model used, token counts

### Log Collection Script

```bash
# Collect Cline task logs for SIEM ingestion
TASK_DIR="$HOME/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks"
EXPORT_DIR="/var/log/cline-audit/$(hostname)/$(date +%Y-%m-%d)"
mkdir -p "$EXPORT_DIR"

find "$TASK_DIR" -name "task_metadata.json" -newer /tmp/last-cline-audit-run \
    -exec cp {} "$EXPORT_DIR/" \;

touch /tmp/last-cline-audit-run
```

---

## 6. Deployment Checklist

- [ ] Deploy `settings.json` with all `alwaysAllow*` set to `false` via MDM
- [ ] Configure `allowedCommands` to an explicit, reviewed allowlist
- [ ] Set `browserToolEnabled: false` and `telemetrySetting: "disabled"`
- [ ] Deploy approved `cline_mcp_settings.json` with workspace-scoped filesystem servers only
- [ ] Manage API keys via environment variables or secrets manager — never in settings files
- [ ] Set up log collection from the Cline task history directory
- [ ] Block unapproved VS Code extension updates via MDM
- [ ] Review Cline task logs monthly for anomalies
- [ ] Ensure VS Code workspace trust is enforced (`security.workspace.trust.enabled: true`)

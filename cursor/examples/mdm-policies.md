# Cursor — MDM Enterprise Policy Deployment

## Available MDM Policies

| Policy | Type | Description | Recommended value |
|--------|------|-------------|-------------------|
| `AllowedTeamId` | String | Lock login to a specific Cursor team | Your team ID |
| `AllowedExtensions` | String (JSON) | Allowlist of permitted publishers/extensions (JSON object string). Any entry creates an allowlist; use `"*": true` only when intentionally allowing all with explicit denials. | See below |
| `WorkspaceTrustEnabled` | Boolean | Enforce workspace trust | `true` |
| `UpdateMode` | String | Control updates | `"manual"` |
| `NetworkDisableHttp2` | Boolean | Force HTTP/1.1 | `false` (unless proxy requires it) |

## Not MDM-enforced (use dashboard + config management)

These controls are real and required for a secure rollout, but they are not MDM keys:

| Control | Where to set it | Deployable file |
|---------|-----------------|-----------------|
| Run Mode / Auto-review | Team dashboard → Agents / Security | `permissions-*.json` (`autoRun`) |
| Sandbox network / paths | Team dashboard + local sandbox policy | `sandbox-*.json` |
| MCP allowlist and per-server network | Team dashboard → MCP Configuration | `permissions-*.json` (`mcpAllowlist`) as fallback |
| Browser / file / `.cursor` protections | Team dashboard | See `enterprise-policy-*.json` |
| Privacy Mode / BYOK / repo blocklist | Team dashboard | See `enterprise-policy-*.json` |

Pair MDM identity locks with the Moderate or Strict enterprise-policy checklist before org-wide rollout.

---

## macOS — Jamf Pro / Kandji

### Configuration Profile

Domain: `com.todesktop.230313mzl4w4u92`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>AllowedTeamId</key>
  <string>YOUR_TEAM_ID_HERE</string>

  <key>WorkspaceTrustEnabled</key>
  <true/>

  <key>UpdateMode</key>
  <string>manual</string>

  <key>AllowedExtensions</key>
  <string>{"esbenp.prettier-vscode": true, "dbaeumer.vscode-eslint": true, "ms-python.python": true, "golang.go": true}</string>
</dict>
</plist>
```

---

## Windows — Intune / Group Policy

### Registry path

```
HKLM\SOFTWARE\Policies\Cursor
```

### Registry values

| Value name | Type | Data |
|------------|------|------|
| `AllowedTeamId` | REG_SZ | `YOUR_TEAM_ID_HERE` |
| `WorkspaceTrustEnabled` | REG_DWORD | `1` |
| `UpdateMode` | REG_SZ | `manual` |

### PowerShell deployment script

```powershell
$regPath = "HKLM:\SOFTWARE\Policies\Cursor"

if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}

Set-ItemProperty -Path $regPath -Name "AllowedTeamId" -Value "YOUR_TEAM_ID_HERE" -Type String
Set-ItemProperty -Path $regPath -Name "WorkspaceTrustEnabled" -Value 1 -Type DWord
Set-ItemProperty -Path $regPath -Name "UpdateMode" -Value "manual" -Type String

Write-Output "Cursor enterprise policies applied."
```

---

## Linux — Managed File

Place a JSON policy file at the user-level Cursor policy path:

```bash
mkdir -p ~/.cursor
tee ~/.cursor/policy.json << 'EOF'
{
  "AllowedTeamId": "YOUR_TEAM_ID_HERE",
  "WorkspaceTrustEnabled": true,
  "UpdateMode": "manual",
  "AllowedExtensions": "{\"esbenp.prettier-vscode\": true, \"dbaeumer.vscode-eslint\": true, \"ms-python.python\": true, \"golang.go\": true}"
}
EOF
chmod 644 ~/.cursor/policy.json
```

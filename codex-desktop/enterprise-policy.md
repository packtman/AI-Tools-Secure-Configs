# Codex Desktop App — Enterprise Policy Deployment Guide

## Overview

The OpenAI Codex Desktop App supports enterprise-managed policies through three mechanisms:
1. **Cloud-managed requirements** (ChatGPT Business/Enterprise admin console)
2. **macOS MDM** (managed preferences)
3. **System-level files** (`requirements.toml` and `managed_config.toml`)

These policies enforce constraints that users cannot override, ensuring consistent security posture across the organization.

---

## Cloud-Managed Requirements (Recommended)

### Setup

1. Navigate to [Codex Managed Config](https://chatgpt.com/codex/settings/managed-configs)
2. Create a new managed requirements file using `requirements.toml` format
3. Assign requirements to user groups or set a default fallback policy
4. Changes apply immediately for matching users

### Group Assignment

Admins can configure different policies for different user groups. If a user matches more than one group rule, the first matching rule applies. Codex does not fill unset fields from later matching rules.

### Recommended Policy Tiers

**Standard Developers:**
```toml
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached"]

[features]
browser_use = false
computer_use = false

[in_app_browser]
allow_external_browser_settings_import = false
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]

[features]
browser_use = true
computer_use = false

# This group may use Browser Use. Importing another browser's settings or data stays off.
[in_app_browser]
allow_external_browser_settings_import = false
```

**Regulated Environments:**
```toml
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only"]
allowed_web_search_modes = ["disabled"]

[features]
browser_use = false
in_app_browser = false
computer_use = false
memories = false

[in_app_browser]
allow_external_browser_settings_import = false
```

---

## macOS — Managed Preferences (MDM)

### Preference Domain

```
com.openai.codex
```

### MDM Keys

| Key | Type | Description |
|-----|------|-------------|
| `config_toml_base64` | String | Base64-encoded managed defaults (TOML) |
| `requirements_toml_base64` | String | Base64-encoded requirements (TOML) |

### Deployment Workflow

1. Build the managed payload TOML
2. Encode with `base64` (no wrapping): `base64 -i requirements.toml`
3. Add the encoded string to your MDM profile under `com.openai.codex` domain
4. Push the profile via Jamf, Kandji, Fleet, or Mosyle
5. Ask users to restart Codex to confirm settings apply

### Example: Create MDM Payload

```bash
# Create requirements
cat > /tmp/codex-requirements.toml << 'EOF'
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]

[features]
browser_use = false
computer_use = false

[in_app_browser]
allow_external_browser_settings_import = false
EOF

# Encode for MDM
base64 -i /tmp/codex-requirements.toml
```

### Verification

```bash
defaults read com.openai.codex requirements_toml_base64
# Decode to verify:
defaults read com.openai.codex requirements_toml_base64 | base64 -d
```

---

## Windows — System-Level Files

### Requirements File Location

```
%ProgramData%\OpenAI\Codex\requirements.toml
```

### Managed Config Location

```
%USERPROFILE%\.codex\managed_config.toml
```

### Deployment via Group Policy / Intune

1. Create the `requirements.toml` file with your organization's constraints
2. Deploy to `C:\ProgramData\OpenAI\Codex\requirements.toml` via GPO file distribution or Intune Win32 app
3. Set file permissions to prevent user modification (SYSTEM and Administrators only)

### Example PowerShell Deployment

```powershell
$requirementsPath = "C:\ProgramData\OpenAI\Codex\requirements.toml"
$requirementsDir = Split-Path $requirementsPath

if (-not (Test-Path $requirementsDir)) {
    New-Item -ItemType Directory -Path $requirementsDir -Force
}

@"
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]

[features]
browser_use = false
computer_use = false

[in_app_browser]
allow_external_browser_settings_import = false
"@ | Set-Content -Path $requirementsPath -Encoding UTF8

# Restrict permissions
$acl = Get-Acl $requirementsPath
$acl.SetAccessRuleProtection($true, $false)
$adminRule = New-Object System.Security.AccessControl.FileSystemAccessRule("BUILTIN\Administrators", "FullControl", "Allow")
$systemRule = New-Object System.Security.AccessControl.FileSystemAccessRule("NT AUTHORITY\SYSTEM", "FullControl", "Allow")
$acl.AddAccessRule($adminRule)
$acl.AddAccessRule($systemRule)
Set-Acl -Path $requirementsPath -AclObject $acl
```

---

## Linux — System-Level Files

### Requirements File Location

```
/etc/codex/requirements.toml
```

### Managed Config Location

```
/etc/codex/managed_config.toml
```

### Deployment

```bash
sudo mkdir -p /etc/codex
sudo tee /etc/codex/requirements.toml > /dev/null << 'EOF'
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only", "workspace-write"]

[features]
browser_use = false
computer_use = false

[in_app_browser]
allow_external_browser_settings_import = false
EOF

sudo chmod 644 /etc/codex/requirements.toml
sudo chown root:root /etc/codex/requirements.toml
```

---

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Use cloud-managed requirements to enforce `read-only` sandbox and disable all extended features
2. Set `allowed_web_search_modes = []` to disable web search entirely
3. Pin `browser_use = false`, `features.in_app_browser = false`, `computer_use = false`, and `in_app_browser.allow_external_browser_settings_import = false`
4. Add `deny_read` rules for sensitive paths (e.g., `~/.ssh`, credentials directories)
5. Restrict MCP servers to an empty allowlist or specific approved servers only
6. Add command rules to forbid dangerous operations

### For Development Environments

1. Allow `workspace-write` sandbox mode but block `danger-full-access`
2. Set `approval_policy = "on-request"` as the managed default
3. Allow `cached` web search but block `live` unless needed
4. Define an MCP server allowlist with only approved integrations
5. Use managed hooks to audit command execution
6. Enable telemetry for compliance and audit logging

### Authentication Controls

- Require SSO/MFA via ChatGPT Enterprise workspace settings
- Enable device code authentication only if needed for remote dev environments
- Use RBAC to separate Codex Admin from Codex User permissions

---

## Built-in browser import lock

The built-in browser is the pane a person opens inside the Codex desktop app. It is separate from Browser Use, which is the agent browsing on its own. `in_app_browser.allow_external_browser_settings_import` is a requirements key. `false` blocks importing settings or browsing data from Chrome, Edge, or another browser into that pane. Setting the key to `true` does not block the import. Omitting the key leaves the import available when other product checks allow it.

This key is documented for `requirements.toml` only. There is no `config.toml` override. Do not copy it into `config.toml` or `managed_config.toml`. Do not put it under `[features]`. `features.in_app_browser` is a different key: it turns the pane on or off.

OpenAI's config reference says the CLI and the IDE extension do not provide this pane. They still load the same requirements file.

### Rollout plan

Pilot one managed group that already receives `requirements.toml`. Exit when every pilot host shows `allow_external_browser_settings_import = false` inside `[in_app_browser]` after a Codex restart, and the pilot lead confirms they can still open a page in the built-in browser and sign in there. Expanded pilot: the rest of the Moderate cohort. Exit when a week of helpdesk tickets shows no workflow that requires importing another browser profile. Org-wide: remaining Moderate and Strict devices. Baseline stays unset.

Pre-rollout checklist:

- MDM (Mobile Device Management, the system that pushes settings to laptops) can write `com.openai.codex` / `requirements_toml_base64` on macOS, or the system requirements file on Windows and Linux.
- The ChatGPT admin console path is verified if you use cloud-managed requirements.
- SIEM (Security Information and Event Management, the central log store) already receives the ChatGPT Compliance API export, or you have a file-integrity alert on `requirements.toml`.
- Rollback below is copied into the change ticket before the pilot starts.

What will break: on Moderate and Strict, the built-in browser will not import settings or browsing data from another browser. A developer who relied on that import must open the site in the pane and sign in, or paste the URL into chat. Browser Use history access and Computer Use stay on their own keys.

Developer message to send before rollout:

> On [date], Codex on standard and regulated laptops will stop the built-in browser from importing settings or browsing data from Chrome, Edge, or another browser. That import can copy cookies and saved site data into Codex. If you need a page, open it in the built-in browser and sign in there, or paste the URL into chat. Reply if a named workflow cannot continue without that import. We will review a time-boxed exception for that group. Do not edit the managed requirements file locally. That file wins over `config.toml`.

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `in_app_browser.allow_external_browser_settings_import` | unset | `false` | `false` | Baseline leaves import on the product default so a person can bring bookmarks or a signed-in profile into the pane. Moderate and Strict pin `false` in `requirements.toml`. Turning the pane off with `features.in_app_browser = false` does not block import if a later exception turns the pane back on. |

### Deployment steps

Put the key in the shared requirements file, in its own `[in_app_browser]` table. Codex Desktop, the Codex CLI, and the IDE extension read one requirements file. Deploy it once. Do not create a second CLI-only copy. Do not put this key in `config.toml`, `managed_config.toml`, or `[features]`.

| OS | Requirements path |
|----|-------------------|
| macOS | MDM payload `com.openai.codex` key `requirements_toml_base64`, or `/etc/codex/requirements.toml` |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` |
| Linux | `/etc/codex/requirements.toml` |

MDM:

- Jamf: a custom settings profile for `com.openai.codex` with `requirements_toml_base64` set to the base64 of the requirements file (no line wraps).
- Intune: a Win32 app or device script that writes the Windows path above and locks the ACL to SYSTEM and Administrators.
- Workspace ONE: the same macOS custom settings payload (`com.openai.codex` / `requirements_toml_base64`) and the same Windows file path.

Validation, after restart:

```bash
# macOS MDM
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep allow_external_browser_settings_import

# Linux
grep allow_external_browser_settings_import /etc/codex/requirements.toml
```

```powershell
Select-String -Path "$env:ProgramData\OpenAI\Codex\requirements.toml" -Pattern allow_external_browser_settings_import
```

Moderate and Strict must show `allow_external_browser_settings_import = false` under `[in_app_browser]`. Baseline requirements must omit the key. Confirm the key is not under `[features]`.

Audit: keep shipping the ChatGPT Compliance API export to the SIEM. Alert when `requirements.toml` on a Moderate or Strict host no longer contains `allow_external_browser_settings_import = false`. Codex does not publish a separate "browser import blocked" event name for this key.

### Workflow-preservation notes

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Import settings or browsing data from an external browser into the built-in browser pane | Cookies, saved site data, and history from another browser land inside Codex, including signed-in sessions | Open the site in the built-in browser and sign in there, or paste the URL into chat | Time-box a requirements change that removes this key for a named pilot group. A user edit in `config.toml` does not override requirements. Do not set `true` |

False-positive friction: people who used the import button for bookmarks or a signed-in profile will find that action gone. That stop is expected. Sign in inside the pane for the site they need.

Overlap:

- Codex CLI and the IDE extension do not show the built-in browser pane. They still load the same `requirements.toml`. One file covers the desktop app, the CLI, and the IDE extension. Do not add a second copy under a CLI-only path.
- `features.in_app_browser = false` turns the pane off. It does not block import if a later exception turns the pane on. Strict should keep both keys. Moderate should keep the import lock even when the pane stays available.
- `browser_use.allow_history_access = false` stops agent-driven Browser Use from reading browser history. It does not stop a person from importing browsing data into the built-in pane. Keep this import key as well.
- Claude Code browser pane keys and Copilot local-network keys do not set this Codex key. Configure each tool on its own.

### Rollback

1. Remove `allow_external_browser_settings_import` from the `[in_app_browser]` table in the deployed `requirements.toml`. If that table has no other keys, remove the table. Leave `[features]` in place, including `features.in_app_browser` where Strict already sets it.
2. Push the updated payload: Jamf or Workspace ONE profile, Intune script, or replace `/etc/codex/requirements.toml`.
3. Ask users to restart Codex.

Rollback message:

> We removed the Codex built-in browser import lock. Restart Codex. Importing settings or browsing data from another browser follows the product default again. The pane on/off pin, Browser Use, and the sandbox limits stay as they were.

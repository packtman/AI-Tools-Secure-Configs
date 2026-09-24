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

[browser_use]
allow_history_access = false
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]

[features]
browser_use = true
computer_use = false

# Browser Use may be allowed for this group. History stays off.
[browser_use]
allow_history_access = false
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

[browser_use]
allow_history_access = false
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

[browser_use]
allow_history_access = false
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

[browser_use]
allow_history_access = false
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

[browser_use]
allow_history_access = false
EOF

sudo chmod 644 /etc/codex/requirements.toml
sudo chown root:root /etc/codex/requirements.toml
```

---

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Use cloud-managed requirements to enforce `read-only` sandbox and disable all extended features
2. Set `allowed_web_search_modes = []` to disable web search entirely
3. Pin `browser_use = false`, `in_app_browser = false`, `computer_use = false`, and `browser_use.allow_history_access = false`
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

## Browser history lock

Browser Use is the Codex feature that lets the agent open and operate web pages. `browser_use.allow_history_access` is a separate requirements key that controls whether that feature may read the local browser's visited URLs and search history.

### Rollout plan

Pilot one managed group that already receives `requirements.toml`. Exit when every pilot host shows `allow_history_access = false` after a Codex restart, and the pilot lead confirms that pasted-URL browsing still works for an approved Browser Use exception. Expanded pilot: the rest of the Moderate cohort. Exit when a week of helpdesk tickets shows no workflow that requires history rather than a URL. Org-wide: remaining Moderate and Strict devices. Baseline stays unset.

Pre-rollout checklist:

- MDM (Mobile Device Management, the system that pushes settings to laptops) can write `com.openai.codex` / `requirements_toml_base64` on macOS, or the system requirements file on Windows and Linux.
- The ChatGPT admin console path is verified if you use cloud-managed requirements.
- SIEM (Security Information and Event Management, the central log store) already receives the ChatGPT Compliance API export, or you have a file-integrity alert on `requirements.toml`.
- Rollback below is copied into the change ticket before the pilot starts.

What will break: prompts such as "continue from the pages I visited" or "open my browser history" no longer succeed on Moderate and Strict. Browser Use itself stays off unless you explicitly allow `features.browser_use`. A group that is allowed to use Browser Use still cannot read history.

Developer message to send before rollout:

> On [date], Codex on standard and regulated laptops will stop reading browser history. If a task needs a web page, paste the URL. Browser Use stays off unless security has approved it for your group, and even then history stays off. Reply if a named workflow cannot continue with a pasted URL. We will review a time-boxed exception for that group. Do not edit the managed requirements file locally. That file wins over `config.toml`.

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `browser_use.allow_history_access` | unset | `false` | `false` | Baseline leaves history on the product default so local browser workflows keep working. Moderate and Strict pin `false` in `requirements.toml`. `features.browser_use = false` turns Browser Use off and still leaves history unconstrained if a later exception allows the feature. |

### Deployment steps

Put the key in the shared requirements file. Codex Desktop, the Codex CLI, and the IDE extension read one requirements file. Deploy it once. Do not create a second CLI-only copy.

| OS | Requirements path |
|----|-------------------|
| macOS | MDM payload `com.openai.codex` key `requirements_toml_base64`, or `/etc/codex/requirements.toml` |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` |
| Linux | `/etc/codex/requirements.toml` |

MDM:

- Jamf, Kandji, Fleet, Mosyle: configuration profile for `com.openai.codex`, string `requirements_toml_base64`.
- Intune: Win32 app or PowerShell script that writes the Windows path above. Windows has no Codex registry policy for this key.
- Workspace ONE: same macOS custom settings payload (`com.openai.codex` / `requirements_toml_base64`) and the same Windows file path.

Also set the key in `managed_config.toml` and in the Moderate and Strict `config.toml` templates so a laptop that has not received requirements yet still starts with history off. That copy is a default. Users can change it until requirements are present.

Validation, after restart:

```bash
# macOS MDM
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep allow_history_access

# Linux
grep allow_history_access /etc/codex/requirements.toml
```

```powershell
Select-String -Path "$env:ProgramData\OpenAI\Codex\requirements.toml" -Pattern allow_history_access
```

Moderate and Strict must show `allow_history_access = false`. Baseline requirements must omit the key.

Audit: keep shipping the ChatGPT Compliance API export to the SIEM. Alert when `requirements.toml` on a Moderate or Strict host no longer contains `allow_history_access = false`. Codex does not publish a separate "history read" event name for this key.

### Workflow-preservation notes

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Browser Use reads local browser history | Visited URLs and search terms can include internal hostnames and ticket links | Paste the specific URL, or attach the page content the task needs | Time-box a requirements change for a named pilot group. A user edit in `config.toml` does not override requirements. Do not set `true`. |

False-positive friction: people ask Codex to resume "the tab I already had open." That request fails on Moderate and Strict. The safe path is the URL. This is expected, not a broken install.

Overlap:

- Codex CLI does not browse. It still loads the same `requirements.toml`. One file covers the desktop app, the CLI, and the IDE extension. Do not add a second history key under a CLI-only path.
- Claude Code's Browser pane uses `browserExternalPageTools` and `disableBrowserExternalNavigation`. Copilot's sandbox uses `allowLocalNetwork`. Those keys do not read or lock Codex browser history. Set the Codex key even when the other tools are already locked.
- `features.browser_use = false` and `features.browser_use_external = false` turn browser features off. Keep `allow_history_access = false` as well so an exception that allows Browser Use does not also open history.

### Rollback

1. Remove `allow_history_access` from the `[browser_use]` table in the deployed `requirements.toml`. If that table has no other keys, remove the table.
2. Remove the same key from `managed_config.toml` if you deployed it there.
3. Push the updated payload: Jamf or Workspace ONE profile, Intune script, or replace `/etc/codex/requirements.toml`.
4. Ask users to restart Codex.

Rollback message:

> We removed the Codex browser-history lock. Restart Codex. Browser Use still follows the feature pin, which stays off on standard and regulated laptops. History follows the product default again only where Browser Use is allowed.

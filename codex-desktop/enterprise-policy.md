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
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]

[features]
browser_use = true
computer_use = false
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
```

### Fallback-origin Browser Use full CDP access

Browser Use lets the agent operate a browser. Chrome DevTools Protocol (CDP) is the browser debugging interface: it can read cookies, storage, and network traffic, and it can run script in the page. `browser_use.default_origin_policy` is the fallback for sites with no matching `browser_use.origins` entry. Moderate and Strict requirements pin `full_cdp_access = "deny"` in that table, next to the existing `persistent_approval` and `uploads` keys. Baseline leaves `full_cdp_access` unset.

This is a requirements key only. Keep it out of `config.toml` and `managed_config.toml`. The value is the quoted string `"deny"`, not a boolean and not `features.browser_use_full_cdp_access`. That feature flag turns full CDP off for the whole local runtime, including Browser Developer mode. This origin key blocks full CDP only on unlisted sites. Codex Desktop, the CLI, and the IDE extension read the same `requirements.toml`. The CLI does not browse. Keep this key out of a CLI-only file.

#### Rollout for this key

1. Pilot: 5 to 10 people who are allowed to use Browser Use, for one week. Exit when every blocked CDP request is either accepted or covered by one named-site exception.
2. Expanded pilot: one department, for one week. Exit when exception requests name a site, and nobody asks to set the fallback to `"allow"`.
3. Org-wide: remaining Moderate and Strict groups. Exit when a spot check of endpoints shows `full_cdp_access = "deny"` under `[browser_use.default_origin_policy]`.

Before rollout, confirm the existing requirements path (cloud-managed config, MDM, or system file), confirm the file contains no secrets, and confirm the rollback below is written down. MDM is Mobile Device Management, the software that pushes managed settings to endpoints. `features.browser_use = false` is already set on Moderate and Strict, so most developers will not hit this until an admin enables Browser Use.

Developer message to send first:

> Starting on the rollout date, Codex cannot use full browser debugging (Chrome DevTools Protocol) through Browser Use on websites your admin has not listed. If a task needs that inspection, use your browser's own developer tools, or ask your admin to add that one site. Uploads to unlisted sites stay blocked. This setting does not turn Browser Use off.

#### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `browser_use.default_origin_policy.full_cdp_access` | unset | `"deny"` | `"deny"` | Baseline keeps the vendor default. Moderate and Strict block full CDP on unlisted sites. `"deny"` is already the strongest value, so Strict does not go further. |

#### Deploy and validate

Use the requirements paths already in this guide:

| OS | Path |
|----|------|
| macOS MDM | Preference domain `com.openai.codex`, key `requirements_toml_base64` (Jamf, Intune, or Workspace ONE custom settings) |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` (Intune Win32 or GPO file copy) |
| Linux | `/etc/codex/requirements.toml` |

Workspace ONE does not have a separate Codex payload. Push the same macOS preference domain, or the same system file, that Jamf and Intune use.

```bash
# Linux, or any decoded requirements file
grep -n -A4 '[browser_use.default_origin_policy]' /etc/codex/requirements.toml
# Expected in that table: full_cdp_access = "deny"

# macOS MDM
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep full_cdp_access
# Expected: full_cdp_access = "deny"
```

This key prevents full CDP on fallback origins. It does not emit its own audit event. Keep shipping the ChatGPT Compliance API and existing Codex telemetry to your SIEM (Security Information and Event Management, the central log store). Alert if a Moderate or Strict requirements file is missing `full_cdp_access = "deny"`.

#### Rollback

Delete only the `full_cdp_access` line from the Moderate or Strict requirements file, then redeploy that file through the same MDM or system path. Leave `uploads` and `persistent_approval` in place.

> We removed the Codex fallback-origin full browser-debugging block. Browser Use can request full Chrome DevTools Protocol access on unlisted sites again, subject to normal opt-in and approval. Uploads to unlisted sites stay blocked. Tell us if a workflow is still failing.

#### Workflow preservation

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Full CDP access on a site with no `browser_use.origins` rule | The agent can read cookies, storage, and network traffic, and can run script in a signed-in page | A person uses the browser's own developer tools. Or an admin adds one origin rule with `full_cdp_access = "allow"` for that site, which still requires normal opt-in and approval | Remove `full_cdp_access` for a named group, or add one origin rule. Do not set the fallback to `"allow"`. Do not set `access = "deny"` in the same change: that blocks Browser Use on every fallback site |

False-positive friction shows up when Browser Use is enabled and a developer needs the agent to inspect one known internal site. Handle that with one origin rule, not by clearing the fallback for everyone. Cursor and Claude Code still need their own browser controls. This Codex key does not cover them. It also does not replace `features.browser_use_full_cdp_access`, which turns full CDP off for the whole local runtime.

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
EOF

sudo chmod 644 /etc/codex/requirements.toml
sudo chown root:root /etc/codex/requirements.toml
```

---

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Use cloud-managed requirements to enforce `read-only` sandbox and disable all extended features
2. Set `allowed_web_search_modes = []` to disable web search entirely
3. Pin `browser_use = false`, `in_app_browser = false`, `computer_use = false`
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

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

### Fallback-origin Browser Use downloads

Browser Use lets the agent operate a browser. `browser_use.default_origin_policy` is the fallback for sites with no matching `browser_use.origins` entry. Moderate and Strict requirements pin `downloads = "deny"` in that table, next to the existing `persistent_approval` and `uploads` keys. Baseline leaves `downloads` unset.

This is a requirements key only. Do not copy it into `config.toml` or `managed_config.toml`. The value is the quoted string `"deny"`, not a boolean. Codex Desktop, the CLI, and the IDE extension read the same `requirements.toml`. The CLI does not browse. Do not add a CLI-only copy.

#### Rollout for this key

1. Pilot: 5 to 10 people who are allowed to use Browser Use, for one week. Exit when every blocked download is either accepted or covered by one named-site exception.
2. Expanded pilot: one department, for one week. Exit when exception requests name a site, and nobody asks to set the fallback to `"allow"`.
3. Org-wide: remaining Moderate and Strict groups. Exit when a spot check of endpoints shows `downloads = "deny"` under `[browser_use.default_origin_policy]`.

Before rollout, confirm the existing requirements path (cloud-managed config, MDM, or system file), confirm the file contains no secrets, and confirm the rollback below is written down. `features.browser_use = false` is already set on Moderate and Strict, so most developers will not hit this until an admin enables Browser Use.

Developer message to send first:

> Starting on the rollout date, Codex cannot download files through Browser Use from websites your admin has not listed. If a task needs a file from the web, download it yourself after you review it, or ask your admin to add that one site. Uploads to unlisted sites stay blocked as well.

#### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `browser_use.default_origin_policy.downloads` | unset | `"deny"` | `"deny"` | Baseline keeps the vendor default. Moderate and Strict block downloads from unlisted sites. `"deny"` is already the strongest value, so Strict does not go further. |

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
grep -n -A2 '\[browser_use.default_origin_policy\]' /etc/codex/requirements.toml
# Expected in that table: downloads = "deny"

# macOS MDM
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep downloads
# Expected: downloads = "deny"
```

This key prevents the download. It does not emit its own audit event. Keep shipping the ChatGPT Compliance API and existing Codex telemetry to your SIEM (Security Information and Event Management, the central log store). Alert if a Moderate or Strict requirements file is missing `downloads = "deny"`.

#### Rollback

Delete only the `downloads` line from the Moderate or Strict requirements file, then redeploy that file through the same MDM or system path. Leave `uploads` and `persistent_approval` in place.

> We removed the Codex fallback-origin download block. Browser Use can download from unlisted sites again, subject to normal approvals. Uploads to unlisted sites stay blocked. Tell us if a workflow is still failing.

#### Workflow preservation

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Browser Use download on a site with no `browser_use.origins` rule | The agent can save malware, an unreviewed script, or sensitive files into the workspace | A person downloads the file, reviews it, then places it in the workspace. Or an admin adds one origin rule for that site | Remove `downloads` for a named group, or add one origin rule. Do not set `"allow"`. Do not set `access = "deny"` in the same change: that blocks Browser Use on every fallback site |

False-positive friction shows up when Browser Use is enabled and the agent needs a release file or doc from a known site. Handle that with one origin rule, not by clearing the fallback for everyone. Cursor and Claude Code still need their own browser and shell download rules. This Codex key does not cover them.

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

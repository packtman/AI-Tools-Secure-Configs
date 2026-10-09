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

### Fallback Browser Use site-approval lifetime

Browser Use lets the agent browse websites and take actions on them. A site-access approval is the prompt a person accepts so the agent may use one site. `browser_use.default_origin_policy.access_approval_lifetime` is the fallback for sites that do not match an origin rule. Moderate and Strict requirements pin `access_approval_lifetime = "turn"` in the existing `[browser_use.default_origin_policy]` table, next to `persistent_approval` and `uploads`. Baseline leaves `access_approval_lifetime` unset.

This is a requirements key only. Keep it out of `config.toml` and `managed_config.toml`. The value is the quoted string `"turn"`, not a boolean and not `features.browser_use`. That feature flag turns Browser Use off entirely. `persistent_approval = false` already blocks `Always allow` across sessions. This key shortens the approval that remains inside one thread. The product default is `"thread"`, which keeps the approval until the thread ends. Codex Desktop, the CLI, and the IDE extension read the same `requirements.toml`. Browser Use is a desktop feature. Keep this key out of a CLI-only file. Do not add organization site rules to the template. Do not set `access = "deny"` in this table: that blocks the whole site, not only how long an approval lasts.

#### Rollout for this key

1. Pilot: 5 to 10 people who are allowed to use Browser Use, for one week. Exit when every extra approval prompt is either accepted or covered by one named-site exception.
2. Expanded pilot: one department, for one week. Exit when exception requests name one site, and nobody asks to set the fallback to `"thread"`.
3. Org-wide: remaining Moderate and Strict groups. Exit when a spot check of endpoints shows `access_approval_lifetime = "turn"` under `[browser_use.default_origin_policy]`.

Before rollout, confirm the existing requirements path (cloud-managed config, MDM, or system file), confirm the file contains no secrets, and confirm the rollback below is written down. MDM is Mobile Device Management, the software that pushes managed settings to endpoints. `features.browser_use = false` is already set on Moderate and Strict, so most developers will not hit this until an admin enables Browser Use.

Developer message to send first:

> Starting on the rollout date, a Codex Browser Use approval for a website your admin has not listed lasts only for the current turn. The next turn asks again. If a task needs the approval to last for the rest of the thread on one site, ask your admin to add that one site. This setting does not turn Browser Use off, and it does not change the current rule that Always allow stays off.

#### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `browser_use.default_origin_policy.access_approval_lifetime` | unset (product default `"thread"`) | `"turn"` | `"turn"` | Baseline keeps one site approval for the rest of the thread. Moderate and Strict ask again on the next turn for sites that are not listed. `"turn"` is already the shorter value, so Strict does not go further. |

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
grep -n -A8 '\[browser_use.default_origin_policy\]' /etc/codex/requirements.toml
# Expected in that table: access_approval_lifetime = "turn"

# macOS MDM
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep access_approval_lifetime
# Expected: access_approval_lifetime = "turn"
```

This key shortens how long a site approval lasts. It does not emit its own audit event. Keep shipping the ChatGPT Compliance API and existing Codex telemetry to your SIEM (Security Information and Event Management, the central log store). Alert if a Moderate or Strict requirements file is missing `access_approval_lifetime = "turn"` under `[browser_use.default_origin_policy]`.

#### Rollback

Delete only the `access_approval_lifetime` line from the Moderate or Strict requirements file, then redeploy that file through the same MDM or system path. Leave `persistent_approval` and `uploads` in place.

> We removed the Codex limit that kept unlisted-site approvals to one turn. Those approvals can last for the rest of the thread again. Saved Always allow approvals and uploads stay blocked. Tell us if a workflow is still failing.

#### Workflow preservation

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Reusing a Browser Use site approval on a later turn when the site has no origin rule | The agent can keep using a site the person approved for one action, for the rest of a long thread | A person approves the site again on the next turn. Or an admin adds one origin rule that sets `access_approval_lifetime = "thread"` for that one site | Remove `access_approval_lifetime` for a named group, or add one origin rule. Do not set the fallback to `"thread"`. Do not put a list of every corporate site in the shared template |

False-positive friction shows up only after Browser Use is enabled. A person may think Codex forgot a site they already approved. Handle that with one origin rule, not by clearing the fallback for everyone. Cursor and Claude Code still need their own browser and shell controls. This Codex key does not cover them. It also does not replace `features.browser_use`, which turns Browser Use off, or `persistent_approval`, which blocks Always allow.

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

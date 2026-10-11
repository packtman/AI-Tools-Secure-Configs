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

## Feedback lock (`feedback.enabled`)

Codex lets a user run `/feedback` unless an admin turns it off. The product default is `true`. When the user includes logs, the client can attach a prefix of the session rollout (the local transcript), `codex-logs.log`, a redacted doctor report, and saved auto-review failure records, then send them to OpenAI's Sentry ingest with a thread id and a turn id.

`feedback.enabled` is an exact pin in `requirements.toml`. Users cannot override it. The ChatGPT cloud requirements console honors this key. You can also put it in the system requirements file or the macOS MDM key `requirements_toml_base64`. A copy in `config.toml` or `managed_config.toml` is only a default.

Codex CLI, Codex Desktop, and the IDE extension read one `requirements.toml`. Set the pin once. It does not cover Claude Code feedback surveys, Claude Code feedback drafts, or GitHub Copilot user-feedback collection.

This pin does not turn off Guardian approval. `features.guardian_approval` is a separate key. Leave it unset. Guardian can still record a failed review on the machine. Those records leave the machine only inside a feedback upload that includes logs, so pinning `false` also stops that export.

### Rollout plan

1. Pilot: deploy Moderate `requirements-moderate.toml` to a few workstations. Exit when each pilot user sees a disabled `/feedback` message and a normal shell command still runs.
2. Expanded pilot: add the rest of the standard engineering group. Exit when an exception path exists for a named group that must file a vendor bug, and that path removes only this key.
3. Org-wide: ship the same pin with Strict for regulated groups. Exit when a sample of endpoints shows `enabled = false` under `[feedback]` in the system file, MDM payload, or cloud requirements, and the SIEM has a path for unexpected outbound feedback if the proxy can see it.

Pre-rollout checklist:

- MDM, system-file, or cloud requirements path verified. Any one of those three applies this key.
- Secrets manager is already in place for other Codex pins. This pin does not add a new secret.
- SIEM ingest tested for the endpoint or proxy events you will use.
- Rollback plan documented (remove this one key).

What will break: `/feedback` submissions. Developer message: "Codex /feedback is turned off on managed machines. It can upload a session transcript when logs are included. File product issues through the internal ticket form, and leave out source, secrets, and prompts."

Rollback: delete the `[feedback]` table from the deployed `requirements.toml` (or from the MDM or cloud requirements payload) and restart Codex. Message: "The feedback requirement has been removed. Codex will follow your config.toml value again. The product default allows /feedback until the requirement returns."

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `feedback.enabled` | unset (product default `true`) | `false` | `false` | Moderate and Strict block transcript uploads through `/feedback`. Baseline leaves vendor bug reports available. |

### Deployment

| OS | Requirements path | How this key is enforced |
|----|-------------------|--------------------------|
| macOS | `/etc/codex/requirements.toml` or MDM `com.openai.codex` / `requirements_toml_base64` | System file, cloud requirements, or a Jamf, Intune, or Workspace ONE profile. Encode the TOML with `base64` and put it in `requirements_toml_base64`, not `config_toml_base64`. |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` | Cloud requirements, or an Intune or Group Policy file copy. Windows has no Codex registry policy for this key. |
| Linux | `/etc/codex/requirements.toml` | Cloud requirements, or a root-owned file, mode `644`. |

Workspace ONE and Intune on macOS use the same `com.openai.codex` preference domain as Jamf.

Validation:

- macOS MDM: `defaults read com.openai.codex requirements_toml_base64 | base64 -d` includes `enabled = false` under `[feedback]`.
- Linux: `grep -A1 '^\[feedback\]' /etc/codex/requirements.toml`.
- Windows: `Get-Content "$env:ProgramData\OpenAI\Codex\requirements.toml"`.
- After restart, run `/feedback`. Expected: a disabled message, and no submission. A successful upload means the pin is not active.

Audit: if the corporate proxy can see it, alert on new connections from Codex hosts to `ingest.us.sentry.io` that coincide with a `/feedback` attempt. Ship that proxy event to the SIEM. A successful submission on a Moderate or Strict host means the requirement is missing.

### Workflow preservation

| Blocked | Risk | Safe equivalent |
|---------|------|-----------------|
| `/feedback` with logs | Session rollout prefix, local logs, and auto-review failure records leave the machine | Internal ticket with a short description. Omit source, secrets, and prompts. |
| `/feedback` without logs | Still sends the report, thread id, and client version to OpenAI | Same internal ticket. The pin blocks both forms because the key is one boolean. |
| Setting `feedback.enabled = true` in `config.toml` | Rejected while the requirements pin is active | Remove this one key for a named exception group |

False-positive friction: a developer who hits a Codex crash cannot send the vendor the logs from the machine. Do not turn the org pin back on to collect a one-off report. Collect a redacted note internally, or remove this key for that host group for the time you need the vendor channel.

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

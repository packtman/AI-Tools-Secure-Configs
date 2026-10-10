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

## Credential store lock (`cli_auth_credentials_store`)

Codex can cache a ChatGPT login in `CODEX_HOME/auth.json` when the store is `file`, or when `auto` finds no OS credential store. `keyring` keeps the token in the OS credential store instead. OS credential store means macOS Keychain, Windows Credential Manager, or Linux Secret Service.

This key is an exact pin in `requirements.toml`. Users cannot override it. The ChatGPT cloud requirements console ignores it. Put it in the system requirements file, or in the macOS MDM key `requirements_toml_base64`. A copy in `config.toml` or `managed_config.toml` is only a default.

Codex CLI, Codex Desktop, and the IDE extension read one `requirements.toml`. Set the pin once. It does not cover Claude Code, Cursor, or Copilot tokens.

### Rollout plan

1. Pilot: deploy Moderate `requirements-moderate.toml` to a few workstations that already have a keyring. Exit when each pilot user can log in and `CODEX_HOME/auth.json` is not created or updated.
2. Expanded pilot: add the rest of the standard engineering group, including Linux desktops. Exit when hosts without a keyring are either given one or moved to an exception group that uses `OPENAI_API_KEY`.
3. Org-wide: ship the same pin with Strict for regulated groups. Exit when a sample of endpoints shows the key in the system file or MDM payload, and SIEM has a path for auth-file creation alerts.

Pre-rollout checklist:

- MDM or system-file path verified. Cloud console assignment alone does not apply this key.
- Secrets manager can supply `OPENAI_API_KEY` for CI.
- SIEM ingest tested for file-creation alerts on `auth.json`.
- Rollback plan documented (remove this one key).

What will break: ChatGPT login on hosts with no OS credential store. Developer message: "Codex will store login tokens in the OS credential store. Machines without Keychain, Credential Manager, or Secret Service should use an API key from the secrets manager. Do not set the credential store to file."

Rollback: delete `cli_auth_credentials_store` from the deployed `requirements.toml` (or from the MDM requirements payload) and restart Codex. Leave the managed default in place if you still want keyring as a starting value. Message: "The credential-store requirement has been removed. Codex will follow your config.toml value again. Prefer keyring until the requirement returns."

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `cli_auth_credentials_store` | unset | `"keyring"` | `"keyring"` | Moderate and Strict block plaintext `auth.json`. Baseline does not lock hosts that have no OS credential store. |

### Deployment

| OS | Requirements path | How this key is enforced |
|----|-------------------|--------------------------|
| macOS | `/etc/codex/requirements.toml` or MDM `com.openai.codex` / `requirements_toml_base64` | System file or Jamf, Intune, or Workspace ONE profile. Encode the TOML with `base64` and put it in `requirements_toml_base64`, not `config_toml_base64`. |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` | Intune or Group Policy file copy. Windows has no Codex registry policy for this key. |
| Linux | `/etc/codex/requirements.toml` | Root-owned file, mode `644`. |

Workspace ONE and Intune on macOS use the same `com.openai.codex` preference domain as Jamf.

Validation:

- macOS: `defaults read com.openai.codex requirements_toml_base64 | base64 -d` includes `cli_auth_credentials_store = "keyring"`.
- Linux: `grep cli_auth_credentials_store /etc/codex/requirements.toml`.
- Windows: `Get-Content "$env:ProgramData\OpenAI\Codex\requirements.toml"`.
- After restart, sign in and confirm Codex does not create or update `auth.json` under the Codex home (usually `~/.codex/auth.json`). If that file appears after a fresh login, the pin is not active.

Audit: alert when `auth.json` is created or changed under a Codex home directory. Ship the endpoint file event to the SIEM. A new `auth.json` on a Moderate or Strict host means the requirement is missing or the process is not Codex reading a managed pin.

### Workflow preservation

| Blocked | Risk | Safe equivalent |
|---------|------|-----------------|
| `cli_auth_credentials_store = "file"` | Plaintext login token on disk | Keep `keyring` |
| `cli_auth_credentials_store = "auto"` | Silent fallback to `auth.json` | Keep `keyring`, or install a keyring |
| `cli_auth_credentials_store = "ephemeral"` | Rejected because the pin is exact, not because memory storage is riskier than `file` | CI uses `OPENAI_API_KEY` from the secrets manager and does not save a login |

False-positive friction: Linux servers, containers, and SSH sessions often have no Secret Service. Do not change the org pin to `auto`. Give that group an API key, or remove this one key for that group.

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

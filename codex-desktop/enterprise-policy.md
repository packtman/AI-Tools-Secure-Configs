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
in_app_chat = false
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]

[features]
browser_use = true
computer_use = false
# Browser Use may stay on for this group. ChatGPT conversation screens stay hidden.
in_app_chat = false
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
in_app_chat = false
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
in_app_chat = false
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
in_app_chat = false
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
in_app_chat = false
EOF

sudo chmod 644 /etc/codex/requirements.toml
sudo chown root:root /etc/codex/requirements.toml
```

---

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Use cloud-managed requirements to enforce `read-only` sandbox and disable all extended features
2. Set `allowed_web_search_modes = []` to disable web search entirely
3. Pin `browser_use = false`, `in_app_browser = false`, `computer_use = false`, and `features.in_app_chat = false`
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

## ChatGPT conversation screen lock

ChatGPT and ChatGPT Work conversation screens, and the related cloud automation UI, live in the ChatGPT desktop app. `features.in_app_chat` is a requirements feature key. `false` hides those screens. Setting the key to `true` does not hide them and does not bypass account, workspace-permission, or rollout checks. Omitting the key leaves the screens unconstrained by requirements.

Keep the key in the `[features]` table of `requirements.toml`. A requirements value cannot be overridden from `config.toml`. Do not copy it into `config.toml` or `managed_config.toml` as the lock.

ChatGPT Voice stays available. Existing cloud tasks keep running. Desktop in-app dictation is `features.in_app_dictation`. The experimental CLI `/voice` command is `features.realtime_conversation`. This key does not replace either one.

The CLI and the IDE extension do not show those ChatGPT conversation screens. They still load the same requirements file.

### Rollout plan

Pilot one managed group that already receives `requirements.toml` and uses the ChatGPT desktop app. Exit when every pilot host shows `in_app_chat = false` inside `[features]` after a Codex restart, and the pilot lead confirms they can still type a prompt in the local Codex coding session. Expanded pilot: the rest of the Moderate cohort. Exit when a week of helpdesk tickets shows no workflow that requires the ChatGPT conversation screens, other than a named exception. Org-wide: remaining Moderate and Strict devices. Baseline stays unset.

Pre-rollout checklist:

- MDM (Mobile Device Management, the system that pushes settings to laptops) can write `com.openai.codex` / `requirements_toml_base64` on macOS, or the system requirements file on Windows and Linux.
- The ChatGPT admin console path is verified if you use cloud-managed requirements.
- SIEM (Security Information and Event Management, the central log store) already receives the ChatGPT Compliance API export, or you have a file-integrity alert on `requirements.toml`.
- Rollback below is copied into the change ticket before the pilot starts.

What will break: on Moderate and Strict, the ChatGPT desktop app hides ChatGPT and ChatGPT Work conversation screens and the related cloud automation UI. A developer who used those screens must use the local Codex coding session. ChatGPT Voice stays available. Existing cloud tasks keep running. Desktop dictation and the CLI `/voice` command are separate controls and are not changed by this key.

Developer message to send before rollout:

> On [date], Codex on standard and regulated laptops will hide ChatGPT and ChatGPT Work conversation screens, and the related cloud automation UI, in the ChatGPT desktop app. A conversation there can include source code, secrets, or customer data, and that content leaves the laptop. Use the local Codex coding session instead. ChatGPT Voice stays available. Cloud tasks that are already running keep running. Reply if a named workflow cannot continue without those screens. We will review a time-boxed exception for that group. Do not edit the managed requirements file locally. That file wins over `config.toml`.

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `features.in_app_chat` | unset | `false` | `false` | Baseline leaves ChatGPT and ChatGPT Work conversation screens on the product default. Moderate and Strict pin `false` in `requirements.toml` so those screens, and the related cloud automation UI, stay hidden. Setting `true` does not hide the screens. |

### Deployment steps

Put the key in the shared requirements file, inside the existing `[features]` table. Codex Desktop, the Codex CLI, and the IDE extension read one requirements file. Deploy it once. Do not create a second copy under a CLI-only path.

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
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep in_app_chat

# Linux
grep in_app_chat /etc/codex/requirements.toml
```

```powershell
Select-String -Path "$env:ProgramData\OpenAI\Codex\requirements.toml" -Pattern in_app_chat
```

Moderate and Strict must show `in_app_chat = false` under `[features]`. Baseline requirements must omit the key. Confirm the key is not in `config.toml`.

Audit: keep shipping the ChatGPT Compliance API export to the SIEM. Alert when `requirements.toml` on a Moderate or Strict host no longer contains `in_app_chat = false`. Codex does not publish a separate "conversation screen hidden" event name for this key.

### Workflow-preservation notes

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| ChatGPT and ChatGPT Work conversation screens, and the related cloud automation UI, in the ChatGPT desktop app | A conversation can include source code, secrets, or customer data, and that content leaves the laptop | Use the local Codex coding session | Time-box a requirements change that removes this key for a named group. A user edit in `config.toml` does not override requirements. Do not set `true` |

False-positive friction: people who asked general questions in the ChatGPT conversation screens, or who started cloud automations from that UI, will find those screens gone. That stop is expected. The local Codex coding session still works. Existing cloud tasks keep running. ChatGPT Voice stays available. If those screens are required, remove the key for that group rather than setting `true`.

Overlap:

- The Codex CLI and the IDE extension do not show these ChatGPT conversation screens. They still load the same `requirements.toml`. One file covers the desktop app, the CLI, and the IDE extension. Do not add a second copy under a desktop-only path.
- `features.in_app_dictation = false` disables desktop in-app dictation. `features.realtime_conversation = false` disables the experimental CLI `/voice` command. OpenAI says `in_app_chat` does not block ChatGPT Voice and does not stop existing cloud tasks.
- Claude Code, Cursor, and Copilot chat settings do not set this Codex key. Configure each tool on its own.

### Rollback

1. Remove `in_app_chat` from the `[features]` table in the deployed `requirements.toml`. Leave the other `[features]` keys in place.
2. Push the updated payload: Jamf or Workspace ONE profile, Intune script, or replace `/etc/codex/requirements.toml`.
3. Ask users to restart Codex.

Rollback message:

> We removed the ChatGPT conversation screen lock. Restart Codex. Those screens follow the product default again. Sandbox limits and the other feature pins stay as they were.

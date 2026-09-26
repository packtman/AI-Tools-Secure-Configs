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

[computer_use]
allow_persistent_approval = false
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]

[features]
browser_use = true
computer_use = false

# Computer Use stays off for this group. Saved app approvals stay off if a later exception allows Computer Use.
[computer_use]
allow_persistent_approval = false
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

[computer_use]
allow_persistent_approval = false
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

[computer_use]
allow_persistent_approval = false
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

[computer_use]
allow_persistent_approval = false
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

[computer_use]
allow_persistent_approval = false
EOF

sudo chmod 644 /etc/codex/requirements.toml
sudo chown root:root /etc/codex/requirements.toml
```

---

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Use cloud-managed requirements to enforce `read-only` sandbox and disable all extended features
2. Set `allowed_web_search_modes = []` to disable web search entirely
3. Pin `browser_use = false`, `in_app_browser = false`, `computer_use = false`, and `computer_use.allow_persistent_approval = false`
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

## Saved native-app approval lock

Computer Use is the Codex feature that lets the agent operate native desktop apps. `computer_use.allow_persistent_approval` is a separate requirements key. `false` removes the option to save an app approval across sessions. Approvals for the current session remain available. Setting the key to `true`, or omitting it, does not approve an app.

This key is documented for `requirements.toml`. Do not copy it into `config.toml`. Do not pin org-specific app identities (macOS bundle IDs, Windows packaged-app IDs, or executable publisher rules) in this template. Current OpenAI docs cover Computer Use on macOS and Windows. The CLI does not drive those apps.

### Rollout plan

Pilot one managed group that already receives `requirements.toml`. Exit when every pilot host shows `allow_persistent_approval = false` after a Codex restart, and the pilot lead confirms that a current-session approval still works for an approved Computer Use exception. Expanded pilot: the rest of the Moderate cohort. Exit when a week of helpdesk tickets shows no workflow that requires a saved app approval. Org-wide: remaining Moderate and Strict devices. Baseline stays unset.

Pre-rollout checklist:

- MDM (Mobile Device Management, the system that pushes settings to laptops) can write `com.openai.codex` / `requirements_toml_base64` on macOS, or the system requirements file on Windows and Linux.
- The ChatGPT admin console path is verified if you use cloud-managed requirements.
- SIEM (Security Information and Event Management, the central log store) already receives the ChatGPT Compliance API export, or you have a file-integrity alert on `requirements.toml`.
- Rollback below is copied into the change ticket before the pilot starts.

What will break: on Moderate and Strict, Computer Use will not offer a saved approval that lasts into the next session. A developer who previously saved an app will be asked again each session. Computer Use itself stays off unless that group's requirements set `features.computer_use = true`.

Developer message to send before rollout:

> On [date], Codex on standard and regulated laptops will stop saving native-app approvals across sessions. If a task needs an app, approve that app for the current session. Computer Use stays off unless security has approved it for your group, and even then a saved app approval stays off. Reply if a named workflow cannot continue with a current-session approval. We will review a time-boxed exception for that group. Do not edit the managed requirements file locally. That file wins over `config.toml`.

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `computer_use.allow_persistent_approval` | unset | `false` | `false` | Baseline leaves saved app approvals on the product default. Moderate and Strict pin `false` in `requirements.toml`. `features.computer_use = false` turns Computer Use off and still leaves saved approvals available if a later exception allows the feature. |

### Deployment steps

Put the key in the shared requirements file. Codex Desktop, the Codex CLI, and the IDE extension read one requirements file. Deploy it once. Do not create a second CLI-only copy. Do not put this key in `config.toml` or `managed_config.toml`.

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
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep allow_persistent_approval

# Linux
grep allow_persistent_approval /etc/codex/requirements.toml
```

```powershell
Select-String -Path "$env:ProgramData\OpenAI\Codex\requirements.toml" -Pattern allow_persistent_approval
```

Moderate and Strict must show `allow_persistent_approval = false`. Baseline requirements must omit the key.

Audit: keep shipping the ChatGPT Compliance API export to the SIEM. Alert when `requirements.toml` on a Moderate or Strict host no longer contains `allow_persistent_approval = false`. This key does not add its own log event.

### Workflow-preservation notes

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Computer Use saves an app approval across sessions | One approval can cover later desktop actions in that app without a fresh review | Approve the app for the current session | Time-box a requirements change for a named pilot group. A user edit in `config.toml` does not override requirements. Do not set `true`. |

False-positive friction: people who saved an app approval will be prompted again each session. That prompt is expected. Approve the current session.

Overlap:

- Codex CLI does not drive native desktop apps. It still loads the same `requirements.toml`. One file covers the desktop app, the CLI, and the IDE extension. Do not add a second copy under a CLI-only path.
- Claude Code and Cursor have their own desktop or browser controls. Those keys do not lock Codex app approvals. Set the Codex key even when the other tools are already locked.
- `features.computer_use = false` turns Computer Use off. Keep `allow_persistent_approval = false` as well so an exception that allows Computer Use does not also save app approvals across sessions.
- `browser_use.allow_global_persistent_approval` covers websites, not native apps. Pin both when both policies are in force.
- `computer_use.allow_locked_computer_use` only removes Locked Use enablement controls on a managed Mac. It is not a substitute for this key.
- Do not add bundle IDs, Windows app IDs, or executable publisher rules to this template. App lists are org-specific.

### Rollback

1. Remove `allow_persistent_approval` from the `[computer_use]` table in the deployed `requirements.toml`. If that table has no other keys, remove the table.
2. Push the updated payload: Jamf or Workspace ONE profile, Intune script, or replace `/etc/codex/requirements.toml`.
3. Ask users to restart Codex.

Rollback message:

> We removed the Codex saved app-approval lock. Restart Codex. Computer Use still follows the feature pin, which stays off on standard and regulated laptops. Saved app approvals follow the product default again only where Computer Use is allowed.

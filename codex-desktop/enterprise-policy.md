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
disable_auto_review = true
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]

[features]
browser_use = true
computer_use = false

# Browser Use may be allowed for this group. Automatic review for browser actions stays off.
[browser_use]
disable_auto_review = true
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
disable_auto_review = true
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
disable_auto_review = true
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
disable_auto_review = true
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
disable_auto_review = true
EOF

sudo chmod 644 /etc/codex/requirements.toml
sudo chown root:root /etc/codex/requirements.toml
```

---

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Use cloud-managed requirements to enforce `read-only` sandbox and disable all extended features
2. Set `allowed_web_search_modes = []` to disable web search entirely
3. Pin `browser_use = false`, `in_app_browser = false`, `computer_use = false`, and `browser_use.disable_auto_review = true`
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

## Browser Use automatic review lock

Browser Use is the Codex feature that lets the agent open and operate web pages. Automatic review is Codex's reviewer subagent: it can approve an eligible action without a person clicking. `browser_use.disable_auto_review` is a separate requirements key. `true` skips automatic review for Browser Use and asks the person instead. Setting the key to `false`, or omitting it, leaves automatic review available when other settings allow it. This controls approval handling. It does not turn off model safety monitoring.

This key is documented for `requirements.toml`. Do not copy it into `config.toml`. Do not pin org-specific site lists under `browser_use.origins` in this template.

### Rollout plan

Pilot one managed group that already receives `requirements.toml`. Exit when every pilot host shows `disable_auto_review = true` after a Codex restart, and the pilot lead confirms that a person can still approve a browser action for an approved Browser Use exception. Expanded pilot: the rest of the Moderate cohort. Exit when a week of helpdesk tickets shows no workflow that requires automatic review for browser actions. Org-wide: remaining Moderate and Strict devices. Baseline stays unset.

Pre-rollout checklist:

- MDM (Mobile Device Management, the system that pushes settings to laptops) can write `com.openai.codex` / `requirements_toml_base64` on macOS, or the system requirements file on Windows and Linux.
- The ChatGPT admin console path is verified if you use cloud-managed requirements.
- SIEM (Security Information and Event Management, the central log store) already receives the ChatGPT Compliance API export, or you have a file-integrity alert on `requirements.toml`.
- Rollback below is copied into the change ticket before the pilot starts.

What will break: on Moderate and Strict, Browser Use will not send browser actions to automatic review. A developer whose exception allows Browser Use will be asked to approve the action. Browser Use itself stays off unless that group's requirements set `features.browser_use = true`.

Developer message to send before rollout:

> On [date], Codex on standard and regulated laptops will ask a person before Browser Use acts, instead of letting automatic review approve the action. If a task needs a page, approve that action when Codex asks. Browser Use stays off unless security has approved it for your group, and even then automatic review for browser actions stays off. Reply if a named workflow cannot continue with a person approving the browser action. We will review a time-boxed exception for that group. Do not edit the managed requirements file locally. That file wins over `config.toml`.

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `browser_use.disable_auto_review` | unset | `true` | `true` | Baseline leaves automatic review on the product default so local browser workflows keep working. Moderate and Strict pin `true` in `requirements.toml`. `features.browser_use = false` turns Browser Use off and still leaves automatic review available if a later exception allows the feature. |

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
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep disable_auto_review

# Linux
grep disable_auto_review /etc/codex/requirements.toml
```

```powershell
Select-String -Path "$env:ProgramData\OpenAI\Codex\requirements.toml" -Pattern disable_auto_review
```

Moderate and Strict must show `disable_auto_review = true`. Baseline requirements must omit the key.

Audit: keep shipping the ChatGPT Compliance API export to the SIEM. Alert when `requirements.toml` on a Moderate or Strict host no longer contains `disable_auto_review = true`. Codex does not publish a separate "browser automatic review skipped" event name for this key.

### Workflow-preservation notes

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Browser Use sends an action to automatic review | A reviewer subagent can approve a new site, upload, or download without a person looking at it | The person approves the current browser action | Time-box a requirements change for a named pilot group. A user edit in `config.toml` does not override requirements. Do not set `false`. |

False-positive friction: people who relied on automatic review to approve new sites will see a prompt. That prompt is expected. Approve the current action. The prompt appears only when Browser Use is allowed for that group. While `features.browser_use = false`, there is no browser action to review.

Overlap:

- Codex CLI does not browse. It still loads the same `requirements.toml`. One file covers the desktop app, the CLI, and the IDE extension. Do not add a second copy under a CLI-only path.
- Claude Code's Browser pane uses `browserExternalPageTools` and `disableBrowserExternalNavigation`. Copilot's sandbox uses `allowLocalNetwork`. Those keys do not lock Codex browser automatic review. Set the Codex key even when the other tools are already locked.
- `features.browser_use = false` turns Browser Use off. Keep `disable_auto_review = true` as well so an exception that allows Browser Use does not also send browser actions to automatic review.
- `allowed_approvals_reviewers` and `approvals_reviewer` choose the reviewer for general approval prompts (sandbox escapes, blocked network, MCP approvals). They are not a substitute for this Browser Use key. Pin both when both policies are in force. MCP (Model Context Protocol) is how Codex calls external tool servers.
- `browser_use.allow_history_access` controls history reads. `browser_use.allow_global_persistent_approval` controls Always allow for every site. Neither skips automatic review. If those keys are also deployed, keep them in this same `[browser_use]` table.
- `computer_use.allow_persistent_approval` is a different table. It covers native desktop apps, not websites. Do not use it as a substitute.
- An origin policy `auto_review = "deny"` skips automatic review for one site pattern. Do not add `browser_use.origins` hostnames to this template. Site lists are org-specific. The global key covers every origin without naming hosts.

### Rollback

1. Remove `disable_auto_review` from the `[browser_use]` table in the deployed `requirements.toml`. If that table has no other keys, remove the table.
2. Push the updated payload: Jamf or Workspace ONE profile, Intune script, or replace `/etc/codex/requirements.toml`.
3. Ask users to restart Codex.

Rollback message:

> We removed the Codex browser automatic-review lock. Restart Codex. Browser Use still follows the feature pin, which stays off on standard and regulated laptops. Automatic review for browser actions follows the product default again only where Browser Use is allowed.

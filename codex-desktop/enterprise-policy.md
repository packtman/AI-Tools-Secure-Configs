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

## Rollout plan: legacy Windows sandbox allowlist

MDM (Mobile Device Management) is software that pushes managed settings to endpoints. SIEM (Security Information and Event Management) is centralized log collection and alerting. MXC (Microsoft Execution Containers) is the newer Windows sandbox. It does not need a separate admin setup step. This pin does not disable MXC.

Codex CLI, Codex Desktop, and the IDE extension read one `requirements.toml`. Put the key in that file once. Claude Code and Cursor use their own sandboxes. This key does not configure them.

### Phases

1. **Pilot group.** 10 to 25 Windows endpoints that already receive Codex from MDM, plus 2 macOS or Linux endpoints to confirm the extra table does not change them. Before the pin, IT runs elevated sandbox setup for each Windows pilot user who lacks local admin rights. Exit criteria: Windows pilot sessions stay on `elevated` or `mxc` for 5 business days, no one is stuck on the setup screen without an IT ticket, and macOS or Linux sessions start as before.
2. **Expanded pilot.** One business unit, Windows first. Exit criteria: software inventory shows no `unelevated` selection on pinned machines, and any exception group is named and time-boxed.
3. **Org-wide.** Every managed Windows endpoint, then the same requirements file on macOS and Linux so the fleet stays on one template. Exit criteria: sampled requirements files contain `allowed_sandbox_implementations = ["elevated"]`, and a user `windows.sandbox = "unelevated"` entry does not take effect after restart.

### Pre-rollout checklist

- MDM path verified: Intune or Workspace ONE file copy on Windows, Jamf or Workspace ONE custom settings for `com.openai.codex` on macOS, config management for `/etc/codex/requirements.toml` on Linux.
- Elevated sandbox provisioned for Windows users without local admin: `codex sandbox setup --elevated --user 'DOMAIN\user' --codex-home 'C:\Users\user\.codex'`, run from an elevated deployment process. Replace the identity and path. Do not put real employee names in the repo template.
- No secret is required for this key. Keep using the existing secrets manager for Codex credentials. Do not add tokens to `requirements.toml`.
- SIEM ingest tested for endpoint software inventory or for changes to `requirements.toml`, if the org has a SIEM.
- Rollback plan documented (below) and the developer message sent before the pilot.

### What will break

Windows users who cannot complete elevated setup no longer get the unelevated fallback. Codex stops at setup instead of running with the weaker sandbox. macOS and Linux behavior does not change. MXC remains allowed when the device supports it.

Developer message to send before rollout:

> On Windows, Codex will no longer fall back to the weaker unelevated sandbox. If setup asks for administrator approval, contact IT. Do not set windows.sandbox to unelevated in your config. macOS and Linux are unchanged. MXC, when your PC supports it, is still allowed.

### Rollback

1. Remove `allowed_sandbox_implementations` from the deployed `requirements.toml`. If `[windows]` has no other keys, remove that table too.
2. Redeploy the same way you shipped it: cloud requirements, macOS `requirements_toml_base64`, Windows `%ProgramData%\OpenAI\Codex\requirements.toml`, or Linux `/etc/codex/requirements.toml`.
3. Ask users to restart Codex.

Communication template:

> We rolled back the Windows sandbox allowlist. Codex may offer the unelevated fallback again until we republish the requirements file. Keep using the company-approved Codex install. Reply to this thread if setup still blocks you.

## Config files

| Tier | File | `windows.allowed_sandbox_implementations` |
|------|------|-------------------------------------------|
| Baseline | `codex-desktop/examples/requirements-baseline.toml` | unset |
| Moderate | `codex-desktop/examples/requirements-moderate.toml` | `["elevated"]` |
| Strict | `codex-desktop/examples/requirements-strict.toml` | `["elevated"]` |

`examples/managed-config.toml` sets `windows.sandbox = "elevated"` as a starting value only. A user can still select `unelevated` until the requirements file is deployed.

## Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `windows.allowed_sandbox_implementations` | unset (both legacy modes remain available) | `["elevated"]` | `["elevated"]` | Baseline may not have an admin who can provision elevated setup. Moderate and Strict ship `deny_read`, which unelevated does not honor. |
| `windows.allow_mxc` | unset | unset | unset | Not part of this pin. `false` would block MXC, which is the newer sandbox, not the weak legacy fallback. |
| `windows.sandbox` in managed defaults | n/a (no separate baseline managed file) | `elevated` via the shared enterprise managed defaults | `elevated` via the shared enterprise managed defaults | Starting value only. Requirements are the lock. |

## Deployment steps

Codex has no Windows registry policy for this key. Windows uses the system requirements file. macOS uses the managed preference domain. Linux uses the system file.

| OS | Requirements path | MDM |
|----|-------------------|-----|
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` | Intune Win32 or Workspace ONE file copy. Detection: file exists at that path and contains the key. |
| macOS | `/etc/codex/requirements.toml` or MDM payload | Jamf, Kandji, Fleet, Mosyle, or Workspace ONE custom settings. Domain `com.openai.codex`, key `requirements_toml_base64` (base64, no line wrap). The Windows table is inert on macOS. |
| Linux | `/etc/codex/requirements.toml` | No MDM preference domain. Use configuration management. Root-owned, mode `644`. |

Cloud-managed requirements (ChatGPT Business or Enterprise) are the highest requirements layer for supported local clients. Confirm the key in the cloud payload as well as the device file. Work cloud containers do not use the Windows sandbox. Test a Windows laptop separately.

### Validation

Windows:

```powershell
Select-String -Path "$env:ProgramData\OpenAI\Codex\requirements.toml" -Pattern "allowed_sandbox_implementations"
codex --version
```

In Codex, `/debug-config` should show the elevated legacy mode or MXC, not `unelevated`. A user file `%USERPROFILE%\.codex\config.toml` with `sandbox = "unelevated"` under `[windows]` must not win after restart.

macOS:

```bash
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep allowed_sandbox_implementations
```

Linux:

```bash
grep allowed_sandbox_implementations /etc/codex/requirements.toml
```

### Audit logging

This key does not emit its own SIEM event. Alert on these instead:

- The requirements file hash changes outside a change window.
- A Windows endpoint reports sandbox implementation `unelevated` while the pin is deployed.
- `CODEX_HOME/.sandbox/sandbox.log` shows repeated elevated setup failure (error `1385` is a logon-rights failure). Ship that log through the endpoint agent to the SIEM. Do not upload it through Codex `/feedback`.

## Workflow-preservation notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Selecting `windows.sandbox = "unelevated"` | Weaker network isolation, and `deny_read` does not apply, so credential paths can be read | Finish elevated setup, or use MXC when the device supports it. IT can pre-provision elevated with `codex sandbox setup --elevated`. |
| Empty `allowed_sandbox_implementations = []` | Codex rejects the requirements file and the rest of the policy may not load | Use `["elevated"]`, or omit the key only on Baseline. |
| Setting `windows.allow_mxc = false` to "be stricter" | Turns off the newer sandbox and forces the legacy path | Leave `allow_mxc` unset unless a separate, reviewed change says MXC must be off. |

**False-positive friction:** Company laptops that block local user creation, firewall changes, or sandbox-user logon rights cannot finish elevated setup. Those users see a setup block, not a Codex bug.

**Exception requests:** For a named Windows group, and only while IT fixes that policy, set `allowed_sandbox_implementations = ["elevated", "unelevated"]`. Codex still prefers elevated. Record that `deny_read` does not apply on the unelevated path. Do not set the list to `["unelevated"]` only. Remove the exception when elevated setup works. Do not clear the pin for the whole org.

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

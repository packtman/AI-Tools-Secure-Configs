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
browser_use_external = false
computer_use = false
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]

[features]
browser_use = true
browser_use_external = false
computer_use = false
```

**Regulated Environments:**
```toml
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only"]
allowed_web_search_modes = ["disabled"]

[features]
browser_use = false
browser_use_external = false
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
browser_use_external = false
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
browser_use_external = false
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
browser_use_external = false
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
3. Pin `browser_use = false`, `browser_use_external = false`, `in_app_browser = false`, `computer_use = false`
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

## External Browser Use (`browser_use_external`)

MCP (Model Context Protocol) is a way for an AI tool to call external services. It is separate from this pin. This pin covers Browser Use, which lets Codex operate a web browser.

`features.browser_use` governs Browser Agent inside Codex. `features.browser_use_external` governs external Browser Use: the ChatGPT browser extension and other external browsers, including tabs that are already open and signed in. The vendor default is enabled. If the key is omitted, policy allows the feature. The flag has been stable since 2026-04-30 (Codex commit `719431d`) and is present in stable Codex 0.162.1 (2026-10-09).

Put the key only in `requirements.toml`. Codex rejects a conflicting feature write in `config.toml` or a profile file.

### Rollout Plan

Pilot group: one platform team, about 15 to 30 people, mixed macOS and Windows, for one week.

Exit criteria: Codex still starts, existing requirements (sandbox mode, `computer_use = false`) still apply, and the ChatGPT browser extension no longer drives an external browser. No Sev-1 workflow blocker that lacks a manual workaround.

Expanded pilot: one product org, including Linux developers, for one week.

Exit criteria: exception requests are under 5 percent of the group, SIEM (Security Information and Event Management, centralized log collection) is receiving Codex audit events, and rollback was rehearsed on one device.

Org-wide: remaining Codex users.

Exit criteria: spot checks on each OS show `browser_use_external = false` in the loaded requirements, and open exception grants have an owner and an end date.

Pre-rollout checklist:

- MDM (Mobile Device Management, software that pushes settings to laptops) path verified: Jamf or Workspace ONE for Mac, Intune for Windows, and a root-owned file for Linux.
- Secrets manager already holds Codex credentials. This pin does not add a secret.
- SIEM ingest tested with one pilot host.
- Rollback plan below is documented and the previous requirements file is saved.
- Pilot client is Codex 0.162.1 or another build that includes the 2026-04-30 flag. Confirm the rest of `requirements.toml` still applies after the new key is added.

What will break: developers cannot ask Codex to drive Chrome, Edge, or another external browser through the ChatGPT browser extension, including a tab they already signed into. On Baseline, Codex's own Browser Use remains available. On Moderate and Strict, `browser_use` is already false, so browser work stays manual.

Developer message to send before rollout:

> On [date], Codex will stop controlling external browsers through the ChatGPT browser extension, including tabs you already have open. If your tier still allows Browser Use, use the browser inside Codex. Otherwise open the site yourself and paste what Codex needs. If a logged-in staging site truly requires the extension, file an exception with the site and an end date. Leave `config.toml` unchanged. Codex will reject a local copy of this setting.

Rollback: delete the `browser_use_external` line from `requirements.toml` and redeploy the previous file. Omitting the key returns the vendor default, which allows external Browser Use.

- macOS: replace `requirements_toml_base64` in the `com.openai.codex` profile and push it again from Jamf, Intune, or Workspace ONE. Ask the user to quit and reopen Codex.
- Windows: replace `C:\ProgramData\OpenAI\Codex\requirements.toml` with the previous file. Keep the admin-only ACL.
- Linux: replace `/etc/codex/requirements.toml` with the previous file, still owned by root, mode `644`.
- Cloud-managed requirements: remove the key from the group policy in the ChatGPT admin console. The first matching group rule wins. Codex does not fill the gap from a later rule.

Rollback message:

> We reverted the Codex external-browser lock. Quit Codex and open it again. The ChatGPT browser extension can drive an external browser until we redeploy the pin. Other Codex requirements are unchanged.

### Config Files

Deploy these files as `requirements.toml`. They are the tier files:

| Tier | File |
|------|------|
| Baseline | `codex-desktop/examples/requirements-baseline.toml` |
| Moderate | `codex-desktop/examples/requirements-moderate.toml` |
| Strict | `codex-desktop/examples/requirements-strict.toml` |

Each file sets `browser_use_external = false` under `[features]`.

### Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `features.browser_use_external` | `false` | `false` | `false` | Same value on every tier. The vendor default is enabled, and omitting the key allows the ChatGPT browser extension to use existing signed-in tabs. |
| `features.browser_use` | unset | `false` | `false` | Baseline still allows Codex's own browser. Moderate and Strict turn that surface off. External Browser Use stays off on every tier. |

### Deployment Steps

Codex Desktop, Codex CLI, and the IDE extension share one requirements file. Deploy it once. A second copy in `~/.codex/config.toml` conflicts with the pin.

| OS | Requirements path |
|----|-------------------|
| macOS | MDM preference domain `com.openai.codex`, key `requirements_toml_base64` (base64 of the TOML, no line wrap) |
| Windows | `C:\ProgramData\OpenAI\Codex\requirements.toml` |
| Linux | `/etc/codex/requirements.toml` |

MDM:

- Jamf, Kandji, Fleet, Mosyle, and Workspace ONE on macOS: custom settings payload for `com.openai.codex`. There is no separate Codex configuration profile schema.
- Intune on Windows: Win32 app or PowerShell script that writes the file and keeps it readable by users and writable only by Administrators and SYSTEM. See `examples/mdm-windows-deployment.md`.
- Workspace ONE on Windows: the same file path and ACL. Workspace ONE has no extra Codex registry key.
- ChatGPT Business or Enterprise cloud requirements: paste the tier file at `https://chatgpt.com/codex/settings/managed-configs`. Cloud policy and the device file both apply. A device-file deny still blocks the feature.

Validation, after the user quits and reopens Codex:

```bash
# macOS: decoded managed requirements include the pin
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep browser_use_external

# Linux
grep browser_use_external /etc/codex/requirements.toml

# Version gate: 0.162.1 or any build that includes the 2026-04-30 flag
codex --version
```

```powershell
Select-String -Path "C:\ProgramData\OpenAI\Codex\requirements.toml" -Pattern "browser_use_external"
```

On the endpoint, the ChatGPT browser extension control for driving an external browser is unavailable. If that control still works, the requirements file did not load. Also confirm an older pin such as `computer_use = false` still holds, so the new key did not cause the file to be ignored.

Audit logging: Codex local requirements do not write a separate browser-extension log. Ship ChatGPT Enterprise compliance and analytics events to the SIEM. Alert when a deployed requirements file is missing `browser_use_external = false`, and when a pilot host can still start an external-browser session after restart. Review exception-group membership weekly.

### Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Codex drives Chrome, Edge, or another external browser through the ChatGPT browser extension, including an already signed-in tab | The agent acts with the user's cookies and can read or change authenticated sites | On Baseline, use Browser Use inside Codex and approve the site. On Moderate and Strict, open the site yourself and paste the relevant text. For a repeatable internal site, ask IT to review a Browser Use exception that still leaves `browser_use_external = false`. |

False-positive friction: QA flows that drive a logged-in staging app from the extension will stop. Handle the exception as a separate requirements profile for that group that omits `browser_use_external`, with a named owner and an end date. Do not set the key to `true` in `config.toml`.

Overlap: Claude Code fetch tools and Cursor browser tools are separate products. This pin does not govern them. Configure those tools in their own tier files. Codex CLI does not get a second copy of the key.

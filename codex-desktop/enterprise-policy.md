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

allow_appshots = false
allow_remote_control = false
allow_login_shell = false

[features]
browser_use = false
computer_use = false
fast_mode = false
goals = false
skill_mcp_dependency_install = false
```

**Senior/Trusted Developers:**
```toml
allowed_approval_policies = ["on-request", "never"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
allowed_web_search_modes = ["cached", "live"]
allow_remote_control = false
allow_login_shell = false

[features]
browser_use = true
computer_use = false
skill_mcp_dependency_install = false
```

**Regulated Environments:**
```toml
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only"]
allowed_web_search_modes = ["disabled"]

allow_appshots = false
allow_remote_control = false
allow_login_shell = false

[features]
browser_use = false
in_app_browser = false
computer_use = false
memories = false
fast_mode = false
goals = false
skill_mcp_dependency_install = false
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
allow_appshots = false
allow_remote_control = false
allow_login_shell = false

[features]
browser_use = false
computer_use = false
fast_mode = false
goals = false
skill_mcp_dependency_install = false
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
allow_appshots = false
allow_remote_control = false
allow_login_shell = false

[features]
browser_use = false
computer_use = false
fast_mode = false
goals = false
skill_mcp_dependency_install = false
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
allow_appshots = false
allow_remote_control = false
allow_login_shell = false

[features]
browser_use = false
computer_use = false
fast_mode = false
goals = false
skill_mcp_dependency_install = false
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
4. Pin `fast_mode = false`, `goals = false`, `skill_mcp_dependency_install = false`, `allow_appshots = false`, `allow_remote_control = false`, `allow_login_shell = false` (Codex 0.149.0+)
5. Add `deny_read` rules for sensitive paths (e.g., `~/.ssh`, credentials directories)
6. Restrict MCP servers to an empty allowlist or specific approved servers only
7. Add command rules to forbid dangerous operations

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

## Codex 0.149 Feature Pin Rollout

Use this section when you add the 0.149.0+ pins (`fast_mode`, `goals`, `skill_mcp_dependency_install`, `allow_appshots`, `allow_remote_control`, `allow_login_shell`). Plugin catalog pins (`features.plugins`, `remote_plugin`, `plugin_sharing`, `[marketplaces]`) are a separate change. Do not mix them into this rollout.

### 1. Rollout Plan

**Phased rollout**

| Phase | Who | Exit criteria |
|-------|-----|---------------|
| Pilot | Security plus one app team (10 to 25 people) | `/fast` fails on Moderate/Strict; Goals auto-continue is off; a sample skill cannot npm-install an MCP package; remote-control pairing fails; a login-shell request is rejected |
| Expanded pilot | All engineering laptops, no CI agents | Same checks on macOS, Windows, and Linux; fewer than 3 exception requests per 50 developers per week; SIEM shows no remote-control or Appshots events |
| Org-wide | All managed endpoints | Helpdesk runbook published; rollback tested on one device; FinOps confirms Fast-tier usage is zero for pinned groups |

**Pre-rollout checklist**

- [ ] MDM path verified: Jamf `com.openai.codex:requirements_toml_base64`, Intune file to `%ProgramData%\OpenAI\Codex\requirements.toml`, Linux `/etc/codex/requirements.toml`
- [ ] Secrets manager in place (no API keys in TOML)
- [ ] SIEM ingest tested for ChatGPT Enterprise Compliance API / workspace audit log
- [ ] Rollback plan documented (this section)
- [ ] Fleet is on Codex 0.149.0 or later (`codex --version`). Older builds ignore these keys.

**What will break (Moderate)**

- `/fast` and Fast-tier model picks
- Goal save/resume and automatic continuation
- Skills that try to install extra MCP packages
- Appshots (screenshots of other apps)
- Codex device remote control
- Login-shell tool invocations (profile-sourced PATH and env)

Developer-facing message to send before rollout:

> On DATE we will pin Codex 0.149 controls on managed laptops. Fast mode, Goals auto-continue, Appshots, and Codex remote control will be off. Skills will not auto-install MCP packages. Shell tools will not source ~/.zprofile. If a skill needs a package, file an exception with the package name and business reason. If a tool needs extra PATH, ask IT to add it to shell_environment_policy. Use the standard model catalog, write goals in the ticket, and stay on local sessions. Claude Code Fast mode is a separate control; this change does not pin it.

**Rollback procedure**

1. Remove `fast_mode`, `goals`, `skill_mcp_dependency_install`, `allow_appshots`, `allow_remote_control`, and `allow_login_shell` from `requirements.toml` and `managed_config.toml`.
2. Push the reduced payload through the same MDM or file path. Restart Codex.
3. Communication: "Codex 0.149 feature pins were rolled back. Fast mode, Goals, Appshots, and remote control follow product defaults again. Tell security if a skill still cannot install a package."

### 2. Config Files

- CLI defaults: `codex-cli/examples/config-{strict,moderate,baseline}.toml`
- Desktop defaults: `codex-desktop/examples/config-{strict,moderate,baseline}.toml`
- Enforcement lock: `codex-desktop/examples/requirements-{strict,moderate,baseline}.toml` (shared by CLI and Desktop)

### 3. Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `features.fast_mode` | unset (`true`) | `false` | `false` | Fast mode is spend and processing-path change. Baseline may use it. |
| `features.goals` | unset (`true`) | `false` | `false` | Goals persist state and auto-continue. Baseline may keep them. |
| `features.skill_mcp_dependency_install` | `false` | `false` | `false` | Auto-install is a supply-chain path on every tier. |
| `allow_appshots` | omit | `false` | `false` | Screenshots of other apps can leak secrets. Baseline stays unconstrained. |
| `allow_remote_control` | `false` | `false` | `false` | Remote control is unattended endpoint access on every tier. |
| `allow_login_shell` | `false` | `false` | `false` | Login shells re-import secrets that environment policy stripped. |

### 4. Deployment Steps

| OS | Requirements path | Managed defaults path |
|----|-------------------|-----------------------|
| macOS | MDM `com.openai.codex:requirements_toml_base64` or `/etc/codex/requirements.toml` | MDM `config_toml_base64` or `/etc/codex/managed_config.toml` |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` (Intune / GPO) | `%USERPROFILE%\.codex\managed_config.toml` |
| Linux | `/etc/codex/requirements.toml` (root-owned, mode 644) | `/etc/codex/managed_config.toml` |

Workspace ONE: there is no Codex-specific payload. Deploy the same system files with a file catalog or script.

**Validation**

```bash
codex --version   # expect 0.149.0 or later
codex /fast       # Moderate/Strict: Fast mode stays off
```

On Desktop, open Settings and confirm Fast mode, Goals, Appshots, and remote control are off. Decode the MDM payload:

```bash
defaults read com.openai.codex requirements_toml_base64 | base64 -d
```

**Audit logging:** ChatGPT Enterprise Compliance API and workspace audit log. Alert on remote-control pairing, Appshots enablement, Fast-tier usage, and skill-driven package installs.

Codex has no local MDM enforcement on unmanaged Linux BYOD. Next best control: onboarding script that writes `/etc/codex/requirements.toml`, plus network egress filter to the OpenAI API.

### 5. Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| `/fast` or Fast-tier model | Unreviewed premium processing path and spend | Keep the pinned model. Raise `model_reasoning_effort` if you need more analysis. |
| Goals auto-continue | Unattended shell plus extra retention | Write the goal in the ticket. Start a new thread with `approval_policy = "on-request"`. |
| Skill auto-installs an MCP package | Supply-chain code execution as the user | File an exception. IT installs the reviewed package on the golden image. |
| Appshots | Screenshot of secrets in other windows | Describe the UI in text, or attach a redacted image in the ticket. |
| Codex remote control | Unattended endpoint access | Use existing MDM remote-assist or a jump host. |
| Login-shell tool invocation | Profile-sourced env re-imports secrets | Put required PATH extras in `[shell_environment_policy] set`. |

**False-positive friction:** first-run skills that expect npm/pip on demand. Do not set `skill_mcp_dependency_install = true` on laptops. Handle it as an exception that adds the package to the org image.

**Overlap with other tools:** Claude Code and Cursor also run shell. Pinning Codex Goals does not pin Claude Code plan-mode auto classification or Cursor auto-run. If those tools are in the same org, keep their own unattended-work pins. Codex `allow_remote_control` is not Claude Code `disableRemoteControl`.

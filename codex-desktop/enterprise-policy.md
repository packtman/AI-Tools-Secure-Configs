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
allow_managed_hooks_only = true
allowed_approval_policies = ["on-request"]
allowed_sandbox_modes = ["read-only"]
allowed_web_search_modes = ["disabled"]

[features]
browser_use = false
in_app_browser = false
computer_use = false
memories = false
hooks = true
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

## Security Recommendations

### For Maximum Lockdown (Regulated Environments)

1. Use cloud-managed requirements to enforce `read-only` sandbox and disable all extended features
2. Set `allowed_web_search_modes = []` to disable web search entirely
3. Pin `browser_use = false`, `in_app_browser = false`, `computer_use = false`
4. Add `deny_read` rules for sensitive paths (e.g., `~/.ssh`, credentials directories)
5. Restrict MCP servers to an empty allowlist or specific approved servers only
6. Add command rules to forbid dangerous operations
7. Set `allow_managed_hooks_only = true` so only reviewed administrator hooks can run

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

## Managed Hook Control Update

### 1. Rollout Plan

Before rollout:

- [ ] Verify the cloud, MDM, Group Policy, or system-file path for `requirements.toml`.
- [ ] Inventory user, project, session, and plugin hooks with `/hooks`.
- [ ] Put credentials used by managed hook scripts in the organization secrets manager, not in TOML or scripts.
- [ ] Test Security Information and Event Management (SIEM) ingest from the managed audit hook or endpoint agent.
- [ ] Document the rollback owner and retain the previous managed payload.

| Phase | Scope | Exit criteria |
|-------|-------|---------------|
| Pilot | Security engineering and 5 to 10 volunteer developers | Strict policy is visible in `/hooks`, only managed hooks run, SIEM receives test events, and all blocked hooks have an owner or safe replacement. |
| Expanded pilot | One development group on each supported OS | No unexplained build, test, or editor failures for five working sessions, exception requests are documented, and rollback is tested on one endpoint. |
| Organization-wide | Remaining Strict-tier endpoints in controlled waves | Policy deployment succeeds on at least 95 percent of targeted endpoints, failures are remediated, and support confirms the developer notice was sent. |

What will break: Strict endpoints will no longer run hooks defined by a developer, repository, session, or plugin. Build wrappers, formatting hooks, custom notifications, and local audit scripts may stop firing if they were implemented as Codex hooks.

Developer-facing message:

> Security is enabling managed-only Codex hooks on Strict endpoints. Personal, repository, session, and plugin hooks will stop running. Core Codex commands remain available. Submit a hook review request with the script, owner, event, required permissions, and business reason if the automation is required. Approved hooks will be deployed through endpoint management.

Rollback procedure:

1. Remove `allow_managed_hooks_only = true` from the active `requirements.toml`, or set it to `false`. Keep `[features].hooks = true` so existing hooks can resume.
2. For cloud-managed requirements, publish the previous policy revision. For macOS, regenerate and push `com.openai.codex:requirements_toml_base64`. For Windows, restore `%ProgramData%\OpenAI\Codex\requirements.toml` through Group Policy or Intune. For Linux, restore `/etc/codex/requirements.toml`.
3. Restart Codex, open `/hooks`, and confirm the expected non-managed hooks are visible.
4. Send: "The managed-only Codex hook policy was rolled back while we investigate workflow impact. Previously configured hooks may run again. Continue to review hook source and report unexpected execution."

### 2. Config Files

Use `examples/requirements-strict.toml` for Strict deployments. The control must be top-level in `requirements.toml`:

```toml
allow_managed_hooks_only = true

[features]
hooks = true
```

Do not place `allow_managed_hooks_only` in `config.toml`; Codex does not enforce it there. Moderate and Baseline templates intentionally omit the key so trusted developer hooks continue to work.

### 3. Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for difference |
|---------|----------|----------|--------|-----------------------|
| `[features].hooks` | `true` | `true` | `true` | All tiers keep lifecycle hooks available. Strict limits their source separately. |
| `allow_managed_hooks_only` | Not set | Not set | `true` | Strict blocks unreviewed executable hooks. Other tiers preserve local and repository automation. |

### 4. Deployment Steps

1. Deploy the Strict template through the cloud-managed requirements console, macOS MDM, Windows Group Policy or Intune, or the Linux system file path documented above.
2. If managed hooks are configured, install their scripts separately with endpoint management. Codex validates that managed hook directories are absolute and exist; it does not distribute scripts.
3. Restart Codex. Open `/hooks` and verify that managed entries are marked as managed and cannot be disabled by the user.
4. Trigger one approved test hook and confirm its expected result. Do not treat `codex --version` alone as policy validation.
5. Send managed hook events to the SIEM through the hook's approved logging destination or the endpoint agent. Alert on failed policy hooks, changes to managed hook files, and Strict endpoints that report non-managed hooks.

Workspace ONE can deploy the same macOS custom preference payload or protected Windows and Linux files. Jamf uses the `com.openai.codex` custom schema. Intune uses the protected Windows file deployment described above.

### 5. Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Personal or repository hook execution | An unreviewed script can execute with developer privileges. | Submit the script for review, then deploy it as a managed hook from an absolute, endpoint-managed path. |
| Plugin-provided hooks | A plugin update can change executable behavior without policy review. | Pin and review the plugin, then reproduce the required control as an administrator-managed hook. |
| Session hook overrides | A temporary hook can bypass the reviewed endpoint configuration. | Use a documented one-time command outside the hook system with normal Codex approval and sandbox controls. |

The common false positive is a trusted formatter, test runner, or notification hook being classified as unmanaged. Exception requests should include the script hash, owner, source repository, hook event, required filesystem and network access, review expiration date, and a test plan. Prefer converting approved exceptions to managed hooks instead of disabling the Strict control for an entire team.

Codex Desktop, Codex CLI, and the Codex IDE extension share the configuration system. Apply this requirement once per endpoint or cloud-managed user group, then validate each installed surface. Do not deploy competing requirement files for each surface.

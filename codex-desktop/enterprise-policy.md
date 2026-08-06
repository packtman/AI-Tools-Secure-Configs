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
apps = false
```

---

## Apps (connectors) rollout addendum

Use this section when rolling out Apps defaults without changing the rest of your Codex Desktop posture.

### 1. Rollout Plan

**Phased rollout**

| Phase | Scope | Exit criteria |
|-------|-------|---------------|
| Pilot | 5 to 15 developers on one team | No unexpected connector tool runs; approval prompts understood; SIEM sees connector-related events (or compensating inventory) |
| Expanded pilot | One business unit | Exception process documented; false-positive rate acceptable; rollback tested on two endpoints |
| Org-wide | All Codex Desktop seats | MDM/cloud requirements verified on sample of each OS; support playbook published |

**Pre-rollout checklist**

- [ ] MDM path verified (`com.openai.codex` on macOS, system files on Windows/Linux) or cloud-managed requirements assigned
- [ ] Secrets manager in place (connectors must not become a path to vaulted credentials)
- [ ] SIEM ingest tested (Compliance API / OTLP) or compensating inventory of managed profiles
- [ ] Rollback plan documented (remove `features.apps` pin and `apps._default` from managed payloads)

**What will break (Moderate example)**

- App tools that previously auto-ran now prompt (`default_tools_approval_mode = "prompt"`).
- Tools with `destructive_hint` or `open_world_hint` are denied by default.
- Strict additionally disables Apps entirely (`features.apps = false`).

**Developer message (send before rollout)**

> Starting [DATE], Codex Desktop applies org defaults for connected Apps (connectors). You will be prompted before connector tools run. Destructive and open-world connector tools are blocked unless IT approves a per-app exception. In Strict environments, Apps are disabled. Use approved MCP servers from the allowlist for local tooling. Contact #ai-tools-support for exceptions.

**Rollback**

1. Remove or relax `[apps._default]` from `managed_config.toml` / MDM `config_toml_base64`.
2. Set `features.apps = true` in requirements (or omit the pin) if Apps were disabled.
3. Redeploy MDM/GPO/cloud requirements and ask users to restart Codex.
4. Communication: "Apps connector defaults were reverted as of [TIME]. Restart Codex if prompts still look wrong."

### 2. Config Files

Use the tier files under `examples/` (`config-*.toml`, `requirements-*.toml`, `managed-config.toml`). Prefer Moderate for standard enterprise.

### 3. Tier Delta Table

See `examples/policy-rationale.md` (Tier Delta: Apps defaults).

### 4. Deployment Steps

| OS | Requirements | Managed defaults |
|----|--------------|------------------|
| macOS | MDM `com.openai.codex` / `requirements_toml_base64` or `/etc/codex/requirements.toml` | MDM `config_toml_base64` or `/etc/codex/managed_config.toml` |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` | `%USERPROFILE%\.codex\managed_config.toml` |
| Linux | `/etc/codex/requirements.toml` | `/etc/codex/managed_config.toml` |

**Validation:** Restart Codex, open Settings / startup config summary, confirm `features.apps` and `apps._default` match the tier. On macOS: `defaults read com.openai.codex requirements_toml_base64 | base64 -d`.

**Audit:** Ship ChatGPT Compliance API and OTLP (`[otel]`) to SIEM. Alert on unexpected Apps enablement, `auto_review` usage, or connector tool approvals outside the pilot group.

### 5. Workflow-Preservation Notes

| Blocked / changed | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Strict: Apps disabled | Connector supply-chain and open-world tool risk | Use allowlisted local MCP servers; request a connector pilot |
| Moderate: every app tool prompts | Friction on frequent connector calls | Keep prompting; for a trusted app, add `apps.<id>` with narrower mode after review |
| `destructive_enabled = false` | Destructive connector actions | Run destructive ops manually in an approved console, not via Codex Apps |
| `open_world_enabled = false` | Broad external reach | Use a scoped connector or approved HTTP egress path |
| `auto_review` for app prompts | Automatic approval of connector escalations | Keep `approvals_reviewer = "user"`; exception only with guardian policy |

**False-positive friction:** Teams that rely on one trusted connector may request `apps.<connector_id>.default_tools_approval_mode = "writes"`. Approve only after tool inventory review; do not flip org-wide `_default` to `auto`.

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
3. Pin `browser_use = false`, `in_app_browser = false`, `computer_use = false`, `apps = false`
4. Add `deny_read` rules for sensitive paths (e.g., `~/.ssh`, credentials directories)
5. Restrict MCP servers to an empty allowlist or specific approved servers only
6. Keep `[apps._default] enabled = false` in managed defaults for defense in depth
7. Add command rules to forbid dangerous operations

### For Development Environments

1. Allow `workspace-write` sandbox mode but block `danger-full-access`
2. Set `approval_policy = "on-request"` and `approvals_reviewer = "user"` as managed defaults
3. Allow `cached` web search but block `live` unless needed
4. Define an MCP server allowlist with only approved integrations
5. Set `[apps._default]` with human review and `destructive_enabled = false`
6. Use managed hooks to audit command execution
7. Enable telemetry for compliance and audit logging
### Authentication Controls

- Require SSO/MFA via ChatGPT Enterprise workspace settings
- Enable device code authentication only if needed for remote dev environments
- Use RBAC to separate Codex Admin from Codex User permissions

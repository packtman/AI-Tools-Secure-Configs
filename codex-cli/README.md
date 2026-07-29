# OpenAI Codex CLI  -  Secure Admin Configuration

This directory contains security-hardened configurations for **OpenAI Codex CLI** (the AI coding agent), targeting administrators who need to enforce sandbox restrictions, approval policies, MCP governance, and Codex 0.146+ managed requirement pins.

## What Is Covered

| File | Purpose |
|------|---------|
| `config.toml` | Secure user-level configuration (`~/.codex/config.toml`) |
| `project-config.toml` | Secure project-level configuration (`.codex/config.toml`) |
| `examples/config-strict.toml` | **Strict**  -  Maximum-restriction configuration |
| `examples/config-moderate.toml` | **Moderate**  -  Balanced development configuration |
| `examples/config-baseline.toml` | **Baseline**  -  Essential security only (startups, individual devs) |
| `examples/requirements-strict.toml` | **Strict** admin-enforced requirements (users cannot override) |
| `examples/requirements-moderate.toml` | **Moderate** admin-enforced requirements |
| `examples/requirements-baseline.toml` | **Baseline** admin-enforced requirements |
| `examples/system-config.toml` | System-wide defaults (`/etc/codex/config.toml`) |

## Rollout Plan

### Phased rollout

1. **Pilot group** (security champions + one product team): deploy Moderate `requirements.toml` and `config.toml` on macOS first. Exit when sandbox denials and MCP allowlist misses are understood and documented.
2. **Expanded pilot** (one business unit, include Windows): keep `windows.sandbox_private_desktop = true`, confirm login-shell blocks do not break build toolchains. Exit when exception process SLA is under one business day.
3. **Org-wide**: pin Moderate as default; use Strict only for regulated repos or break-glass review hosts.

### Pre-rollout checklist

- [ ] MDM or package path verified for `/etc/codex/requirements.toml` (Unix) or `%ProgramData%\OpenAI\Codex\requirements.toml` (Windows)
- [ ] Secrets manager in place so developers do not need `.env` reads from the agent
- [ ] SIEM ingest tested for Codex session or hook audit events
- [ ] Rollback package prepared (previous requirements + config files)

### What will break (Moderate)

- Login-shell workflows that depend on `~/.zshrc` or `~/.bashrc` exports
- Skill-driven automatic MCP dependency installs
- Remote plugin catalog browsing and plugin sharing
- Live web search (cached only)
- Unlisted MCP servers

Developer message before rollout: "Codex will no longer load login-shell profiles or auto-install MCP dependencies. Use keyring-backed auth, approved MCP allowlist entries, and non-login shells. Request exceptions through the security ticket queue with business need and expiry date."

### Rollback procedure

1. Replace `/etc/codex/requirements.toml` (or Windows ProgramData path) with the previous file.
2. Replace `/etc/codex/config.toml` if system defaults were changed.
3. On macOS MDM, redeploy the prior `requirements_toml_base64` payload and flush preferences.
4. Communicate: "Codex managed requirements rolled back to \<version\>. Resume normal workflows; report residual denials to IT."

## Configuration Hierarchy (highest → lowest priority)

1. **Admin requirements**  -  cloud-managed, MDM, or system `requirements.toml` (users cannot override)
2. **Command-line arguments**  -  Override config defaults for a single invocation
3. **Project config**  -  `.codex/config.toml` (loaded only for trusted projects)
4. **User config**  -  `~/.codex/config.toml`
5. **System config**  -  `/etc/codex/config.toml` (Unix) or `%ProgramData%\OpenAI\Codex\config.toml` (Windows)

## Overlap with Codex Desktop

CLI and Desktop share `requirements.toml` and `config.toml` paths. Configure once for both. Desktop-only surfaces (in-app browser, Appshots, remote control) are documented under `codex-desktop/`. Open Desktop permission-profile work may land separately; keep these CLI 0.146 pins even if Desktop templates are updated later.

## Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `sandbox_mode` / `allowed_sandbox_modes` | workspace-write allowed | workspace-write allowed | read-only only | Strict is review-only |
| `approval_policy` / `allowed_approval_policies` | never allowed | on-request / untrusted | on-request / untrusted | Baseline allows unattended local use |
| `allow_login_shell` | unset / true default | false | false | Login profiles leak secrets into agent shells |
| `check_for_update_on_startup` | unset / true default | false | false | Enterprise fleets patch via MDM |
| `windows.sandbox_private_desktop` | true | true | true | Safer Windows default on all tiers |
| `features.mcp_2026_07_28` | false | false | false | Under-development MCP protocol |
| `features.skill_mcp_dependency_install` | default on | false | false | Blocks automatic MCP supply-chain installs |
| `features.remote_plugin` | default on | false | false | Unreviewed remote catalogs |
| `features.plugins` | default on | default on | false | Strict removes local plugin runtime |
| `features.apps` | default on | false | false | Connector integrations expand egress |
| `features.network_proxy` | default off | false | false | Keep experimental sandboxed networking off until piloted |
| MCP allowlist | unset | filesystem + git identities | empty (deny all) | Strict needs zero MCP by default |

## Deployment Steps

| OS | User config | System config | Requirements |
|----|-------------|---------------|--------------|
| macOS | `~/.codex/config.toml` | `/etc/codex/config.toml` | MDM `requirements_toml_base64` or `/etc/codex/requirements.toml` |
| Linux | `~/.codex/config.toml` | `/etc/codex/config.toml` | `/etc/codex/requirements.toml` |
| Windows | `%USERPROFILE%\.codex\config.toml` | `%ProgramData%\OpenAI\Codex\config.toml` | `%ProgramData%\OpenAI\Codex\requirements.toml` |

### MDM guidance

- **Jamf / Workspace ONE (macOS):** deliver `com.openai.codex` preference with base64-encoded requirements TOML.
- **Intune (Windows):** Win32 app or proactive remediation that copies `requirements.toml` into `%ProgramData%\OpenAI\Codex\` with SYSTEM-only write ACL.

### Validation

```bash
codex --version
# Confirm rust-v0.146.0 or later for exact managed value enforcement.
test -f /etc/codex/requirements.toml && echo "requirements present"
rg "allow_login_shell|mcp_2026_07_28|skill_mcp_dependency_install" /etc/codex/requirements.toml
```

On Windows, confirm `Get-Content $env:ProgramData\OpenAI\Codex\requirements.toml` shows the expected pins and that `sandbox_private_desktop = true`.

### Audit logging / SIEM

- Prefer managed lifecycle hooks for PreToolUse and PostToolUse audit events (see Desktop/CLI hooks docs).
- Alert on attempts to enable `danger-full-access`, `mcp_2026_07_28`, `skill_mcp_dependency_install`, or empty-requirements drift.

## Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Login shell (`login = true`) | Profile secrets enter agent env | Non-login shell + explicit env vars from secrets manager |
| `curl \| bash` / live package bootstrap via agent | Supply chain | Download, inspect, then run in a local terminal |
| Skill auto-install of MCP deps | Unreviewed MCP code execution | Add identity-matched MCP entries in requirements allowlist |
| Remote plugin catalog | Untrusted extension code | Vendor-reviewed local plugins only (Moderate) or none (Strict) |
| Live web search (Moderate/Strict) | Prompt/code egress | Cached search or approved browser outside Codex |

False-positive friction: `allow_login_shell = false` often breaks custom PATH setups. Exception requests should include the required env vars, compensating control (no secrets in profiles), and an expiry date.

## Key Security Concepts

### Sandbox Modes

| Mode | File access | Network | Use case |
|------|------------|---------|----------|
| `read-only` | Read-only workspace | Disabled | Code review, analysis |
| `workspace-write` | Read/write workspace | Disabled | Local development (default) |
| `danger-full-access` | Full system access | Enabled | NOT recommended for production |

**Security rule:** Never use `danger-full-access` in production or shared environments.

### Approval Policies

| Policy | Behavior |
|--------|----------|
| `untrusted` | Requires approval for every tool use including reads |
| `on-request` | Ask before every write/execute operation; reads are automatic |
| `never` | No approval required (use with extreme caution) |

### Protected Paths

The `.codex/` directory and `.git/` are always protected, even in writable sandbox modes.

### Credential Storage

| Option | Location | Security |
|--------|----------|----------|
| `keyring` | OS credential store | Most secure  -  uses macOS Keychain, Windows Credential Manager, or Linux Secret Service |
| `file` | `~/.codex/auth.json` | Less secure  -  plaintext file |
| `auto` | Keyring with file fallback | Recommended default |

## Deployment Checklist

1. Deploy `requirements.toml` from the chosen tier before relying on user config alone.
2. Deploy `/etc/codex/config.toml` (or Windows ProgramData config) for organization-wide defaults.
3. Keep `danger-full-access` out of `allowed_sandbox_modes`.
4. Set `approval_policy = "on-request"` for Moderate and Strict.
5. Configure `cli_auth_credentials_store = "keyring"` to avoid plaintext credential files.
6. Pin `allow_login_shell = false`, `mcp_2026_07_28 = false`, and `skill_mcp_dependency_install = false` on Moderate/Strict.
7. Audit `.codex/config.toml` in project repositories before marking them as trusted.

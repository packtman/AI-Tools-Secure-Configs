# OpenAI Codex CLI — Secure Admin Configuration

This directory contains security-hardened configurations for **OpenAI Codex CLI** (the AI coding agent), targeting administrators who need to enforce sandbox restrictions, approval policies, and credential management.

## What Is Covered

| File | Purpose |
|------|---------|
| `config.toml` | Secure user-level configuration (`~/.codex/config.toml`) |
| `project-config.toml` | Secure project-level configuration (`.codex/config.toml`) |
| `enterprise-policy.md` | Phased rollout, deployment, rollback, audit, and workflow guidance |
| `examples/config-strict.toml` | **Strict** — Maximum-restriction configuration |
| `examples/config-moderate.toml` | **Moderate** — Balanced development configuration |
| `examples/config-baseline.toml` | **Baseline** — Essential security only (startups, individual devs) |
| `examples/requirements-strict.toml` | **Strict** admin-enforced permission requirements |
| `examples/requirements-moderate.toml` | **Moderate** admin-enforced permission requirements |
| `examples/requirements-baseline.toml` | **Baseline** admin-enforced permission requirements |
| `examples/system-config.toml` | System-wide defaults (`/etc/codex/config.toml`) |
| `examples/settings-rationale.md` | Security rationale and failure modes |

## Configuration Hierarchy

`config.toml` provides defaults. Admin-enforced `requirements.toml` constrains
security-sensitive choices and cannot be bypassed by a project file or CLI
override. Managed permission profiles require Codex 0.138.0 or later.

Requirements are composed from these sources, from lower to higher precedence:

1. **System requirements** — `/etc/codex/requirements.toml` on Unix or `%ProgramData%\OpenAI\Codex\requirements.toml` on Windows
2. **Cloud-managed requirements** — Assigned through Codex managed configuration
3. **Legacy managed config requirements** — Compatibility layer for older deployments
4. **macOS MDM requirements** — `com.openai.codex:requirements_toml_base64`

See [`enterprise-policy.md`](enterprise-policy.md) for exact deployment,
validation, rollback, and SIEM guidance.

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
| `keyring` | OS credential store | Most secure — uses macOS Keychain, Windows Credential Manager, or Linux Secret Service |
| `file` | `~/.codex/auth.json` | Less secure — plaintext file |
| `auto` | Keyring with file fallback | Recommended default |

## Deployment Checklist

1. Upgrade every managed endpoint to Codex 0.138.0 or later.
2. Select one `requirements-<tier>.toml` file and test it with a pilot group.
3. Deploy it as `requirements.toml` through cloud policy, MDM, or the system path.
4. Use `/debug-config` in Codex to confirm `default_permissions` and the permission allowlist.
5. Deploy `config.toml` separately for defaults such as credential storage.
6. Audit `.codex/config.toml` in project repositories before marking them as trusted.

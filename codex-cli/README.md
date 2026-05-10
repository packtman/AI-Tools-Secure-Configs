# OpenAI Codex CLI — Secure Admin Configuration

This directory contains security-hardened configurations for **OpenAI Codex CLI** (the AI coding agent), targeting administrators who need to enforce sandbox restrictions, approval policies, and credential management.

## What Is Covered

| File | Purpose |
|------|---------|
| `config.toml` | Secure user-level configuration (`~/.codex/config.toml`) |
| `project-config.toml` | Secure project-level configuration (`.codex/config.toml`) |
| `examples/config-strict.toml` | **Strict** — Maximum-restriction configuration |
| `examples/config-moderate.toml` | **Moderate** — Balanced development configuration |
| `examples/config-baseline.toml` | **Baseline** — Essential security only (startups, individual devs) |
| `examples/system-config.toml` | System-wide defaults (`/etc/codex/config.toml`) |

## Configuration Hierarchy (highest → lowest priority)

1. **Command-line arguments** — Override everything for a single invocation
2. **Project config** — `.codex/config.toml` (loaded only for trusted projects)
3. **User config** — `~/.codex/config.toml`
4. **System config** — `/etc/codex/config.toml` (Unix only)

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

1. Deploy `/etc/codex/config.toml` on all developer machines for organization-wide defaults.
2. Set `sandbox_mode = "workspace-write"` as the maximum allowed mode.
3. Set `approval_policy = "on-request"` for strict environments.
4. Configure `cli_auth_credentials_store = "keyring"` to avoid plaintext credential files.
5. Disable network access unless explicitly required.
6. Audit `.codex/config.toml` in project repositories before marking them as trusted.

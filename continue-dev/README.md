# Continue.dev — Secure Admin Configuration

This directory contains security-hardened configurations for **Continue.dev** (the open-source AI coding assistant), targeting administrators who need to enforce tool permissions, secrets management, and safe configuration practices.

## What Is Covered

| File | Purpose |
|------|---------|
| `config.yaml` | Secure global configuration template |
| `permissions.yaml` | Tool permission configuration |
| `examples/config-strict.yaml` | **Strict** — Maximum restrictions, indexing disabled (regulated environments) |
| `examples/config-moderate.yaml` | **Moderate** — Balanced security with proxy (enterprise teams) |
| `examples/config-baseline.yaml` | **Baseline** — Essential security only (startups, individual devs) |
| `examples/permissions-strict.yaml` | **Strict** — Read-only tools only, write/bash excluded |
| `examples/permissions-moderate.yaml` | **Moderate** — Read auto-approved, write requires confirmation |
| `examples/permissions-baseline.yaml` | **Baseline** — Most tools auto-approved, bash requires confirmation |
| `examples/config-enterprise.yaml` | Enterprise configuration with proxy (supplemental, see tiered configs) |
| `examples/continuerc-secure.json` | Workspace-level `.continuerc.json` |
| `examples/secrets-management.md` | Secrets management guide |

## Key Security Concepts

### Tool Permission Levels

| Level | Behavior |
|-------|----------|
| `allow` | Tool runs automatically without prompting |
| `ask` | Prompts user for approval before each use |
| `exclude` | Tool is completely hidden from the agent |

Defaults:
- Read-only tools (Read, List, Search, Fetch): `allow`
- Write tools (Edit, Write): `ask`
- Bash: `ask`

### Operational Modes

| Mode | Effect |
|------|--------|
| `--auto` | All tools are allowed (use with caution) |
| `--readonly` | Only read-only tools are available |
| Default | Respects per-tool permission settings |

### Configuration Hierarchy

1. **Workspace** — `.continuerc.json` in project root
2. **Global** — `~/.continue/config.yaml`
3. **Environment** — `.env` files for secrets

### Secrets Management

| Secret type | Visibility | Plans |
|-------------|-----------|-------|
| User secrets | Only the creator | Solo, Teams, Enterprise |
| Org secrets | Proxied, never shared with IDE | Teams, Enterprise |

Secrets are referenced using mustache notation: `${{ secrets.SECRET_NAME }}`

## Deployment Checklist

1. Deploy `~/.continue/config.yaml` with secure defaults on all developer machines.
2. Create `permissions.yaml` with appropriate tool restrictions.
3. Use org secrets (not user secrets) for shared API keys.
4. Deploy `.continuerc.json` to all repositories for project-level overrides.
5. Train developers on permission modes (`--readonly` for code review).
6. Never store API keys in `config.yaml` — use environment variables or org secrets.
7. Audit Continue configuration in repositories before trusting.

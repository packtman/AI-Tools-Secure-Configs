# Windsurf (Codeium) — Secure Admin Configuration

This directory contains security-hardened configurations for **Windsurf** (formerly Codeium), targeting administrators who need to enforce enterprise policies, RBAC, and governance controls.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-admin-policy.md` | Admin security policy checklist |
| `examples/enterprise-policy-strict.json` | **Strict** — No extensions, all features locked down (regulated) |
| `examples/enterprise-policy-moderate.json` | **Moderate** — Approved extensions, workspace trust (enterprise) |
| `examples/enterprise-policy-baseline.json` | **Baseline** — Broad extensions, essential restrictions (startups) |
| `examples/enterprise-policy.json` | Enterprise policy configuration (reference) |
| `examples/mcp-config-secure.json` | Secure MCP server configuration |
| `examples/cascade-hooks.md` | Cascade Hooks for security enforcement |
| `examples/rbac-roles.json` | RBAC role definitions |

## Key Security Concepts

### Enterprise Policies

Windsurf supports centralized policy management via:
- **Windows:** Registry policies at `Software\Policies\Windsurf\{ProductName}`
- **macOS:** Configuration profiles via MDM
- **Linux:** JSON policy files

Policies can control extension allowlists, update modes, and feature access.

### RBAC

Two built-in roles plus custom roles:

| Role | Capabilities |
|------|-------------|
| Admin | Full access — team management, SSO, analytics, service keys |
| User | Standard access — no administrative permissions |
| Custom | Granular permissions across teams, analytics, indexing, SSO |

### Cascade Hooks

Enterprise teams can define hooks that execute at key workflow points:
- **Pre-hooks** — Execute before an action; can block execution
- **Post-hooks** — Execute after an action; for logging and audit

Use cases: security validation, compliance logging, content filtering.

### MCP Configuration

Windsurf uses `~/.codeium/windsurf/mcp_config.json` for global MCP server configuration. Per-workspace overrides can be placed in `.windsurf/mcp_config.json`. Apply the same security principles as Claude Desktop MCP configs.

### Authentication

- SSO via OIDC or SAML 2.0
- SCIM provisioning for automated user lifecycle
- Service keys with scoped permissions for API integrations

## Deployment Checklist

1. Configure SSO (OIDC/SAML) and SCIM provisioning.
2. Deploy enterprise policies via MDM or registry.
3. Restrict extensions to an approved allowlist.
4. Configure RBAC with least-privilege custom roles.
5. Implement Cascade Hooks for security validation and logging.
6. Audit MCP server configurations for security risks.
7. Enable analytics dashboards for usage monitoring.
8. Configure proxy settings for corporate networks.

# Cursor — Secure Admin Configuration

This directory contains security-hardened configurations for **Cursor** (the AI-powered code editor), targeting administrators who need to enforce tool restrictions, workspace trust, and compliance policies across their organization.

## What Is Covered

| File | Purpose |
|------|---------|
| `permissions.json` | Secure `~/.cursor/permissions.json` template |
| `settings.json` | Recommended VS Code / Cursor settings for security |
| `rules/security.mdc` | Cursor Rules file for secure coding instructions |
| `examples/mdm-policies.md` | MDM deployment guide for enterprise policies |
| `examples/permissions-strict.json` | **Strict** — Maximum-restriction permissions |
| `examples/permissions-moderate.json` | **Moderate** — Balanced permissions for development teams |
| `examples/permissions-baseline.json` | **Baseline** — Essential restrictions only (startups, individual devs) |
| `examples/settings-rationale.md` | Comprehensive security reasoning for every setting |
| `examples/cloud-agent-security.json` | Cloud Agent dashboard security reference config |

## Configuration Files

### `permissions.json`

Location: `~/.cursor/permissions.json`

Controls which terminal commands and MCP tools can auto-run without user approval. This file takes precedence over IDE settings, but Team Admin Dashboard controls take highest precedence.

### `settings.json`

Standard VS Code settings applied to Cursor. Can be deployed as:
- User settings (global)
- Workspace settings (`.vscode/settings.json`)
- Managed via MDM

### Cursor Rules

Project rules stored in `.cursor/rules/` provide persistent instructions for Agent mode. Rules can be:
- **Always** — applied to every interaction
- **Auto** — applied when Cursor deems them relevant
- **File-scoped** — applied when matching files are in context
- **Manual** — applied only when explicitly referenced

## MDM-Managed Policies

Enterprise admins can enforce policies through MDM (Jamf, Intune, Kandji):

| Policy key | Type | Description |
|------------|------|-------------|
| `AllowedTeamId` | String | Restricts login to a specific team |
| `AllowedExtensions` | String (JSON) | Allowlist of permitted extensions (JSON object string) |
| `WorkspaceTrustEnabled` | Boolean | Enforce workspace trust mode |
| `UpdateMode` | String | Control update behavior (`manual`, `start`, `default`) |
| `NetworkDisableHttp2` | Boolean | Force HTTP/1.1 for network requests |

## Enterprise Features

| Feature | Description |
|---------|-------------|
| SSO / SAML | Enforce single sign-on for all team members |
| SCIM | Automated user provisioning/deprovisioning |
| Audit logs | Track authentication, settings changes, rule modifications |
| Admin API | Programmatic team and settings management |
| Team Rules | Enforced or optional rules managed from the dashboard |
| Compliance monitoring | Usage and policy adherence tracking |

## Deployment Checklist

1. Deploy `permissions.json` to all developer machines via MDM or config management.
2. Add `.cursor/rules/security.mdc` to all repositories.
3. Configure MDM policies for `AllowedTeamId` and `WorkspaceTrustEnabled`.
4. Set up SSO/SAML and SCIM provisioning in the Cursor dashboard.
5. Create enforced Team Rules in the admin dashboard for org-wide security standards.
6. Enable audit logging and review weekly.
7. Restrict extensions to an approved allowlist via `AllowedExtensions`.

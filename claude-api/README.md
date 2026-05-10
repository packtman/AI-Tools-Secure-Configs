# Claude API — Secure Admin Configuration

This directory contains security-hardened configurations for the **Anthropic Claude API platform** (console.anthropic.com), targeting organization administrators who need to enforce governance, access control, and compliance policies across their teams.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-org-policy.md` | Organization-level security policy checklist |
| `examples/org-policy-strict.json` | **Strict** — Maximum access control, tight limits (regulated industries) |
| `examples/org-policy-moderate.json` | **Moderate** — Balanced access control (enterprise teams) |
| `examples/org-policy-baseline.json` | **Baseline** — Essential security only (startups, individual devs) |
| `examples/workspace-rbac.json` | Workspace RBAC configuration example |
| `examples/rate-limits.json` | Per-workspace rate-limit policy |
| `examples/api-key-policy.md` | API key lifecycle and rotation policy |

## Key Security Concepts

### API Key Types and Scoping

Anthropic issues three key types — each with different blast-radius:

| Key prefix | Scope | When to use |
|------------|-------|-------------|
| `sk-ant-api03-*` | Single workspace, model calls only | Application workloads |
| `sk-ant-admin01-*` | Organization admin API | Automation of user/workspace management |
| `sk-ant-api01-*` | Compliance API (Enterprise only) | Audit, activity feeds, data export |

**Security rule:** Every key should be scoped to exactly one workspace; never share keys across workspaces.

### Workspace Isolation

- Create separate workspaces for production, staging, and development.
- Assign each team its own workspace with explicit member lists.
- Use workspace-level rate limits and spend caps to contain cost overruns.

### Role-Based Access Control

| Role | Capabilities |
|------|-------------|
| Workspace User | Call models via API |
| Workspace Developer | User + manage API keys for that workspace |
| Workspace Admin | Developer + manage workspace members |
| Organization Admin | Full control across all workspaces |
| Organization Billing | View invoices & manage payment |

**Principle of least privilege:** Default new members to *Workspace User*; escalate only when justified.

### Compliance & Audit (Enterprise)

- Enable the Compliance API at the parent organization level.
- Stream activity feeds to your SIEM via the `/v1/compliance/activity` endpoint.
- Treat Compliance Access Keys like production database credentials — store in a secrets manager, never in source control.

## Deployment Checklist

1. Enforce SSO via your identity provider (SAML/OIDC) for all console access.
2. Enable SCIM provisioning to automate user lifecycle.
3. Create workspaces per environment / team.
4. Assign minimal roles to each member.
5. Set rate limits and spend notifications on every workspace.
6. Rotate API keys on a defined schedule (90 days recommended).
7. Enable Compliance API and forward activity logs to your SIEM.
8. Disable unused workspaces promptly.

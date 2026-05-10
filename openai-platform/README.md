# OpenAI Platform — Secure Admin Configuration

This directory contains security-hardened configurations for the **OpenAI API platform** (platform.openai.com), targeting organization owners and security teams who need to enforce access control, audit logging, and data governance.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-org-policy.md` | Organization security policy checklist |
| `examples/org-policy-strict.json` | **Strict** — Maximum access control, IP allowlist, tight limits (regulated) |
| `examples/org-policy-moderate.json` | **Moderate** — Balanced access control, project-based (enterprise) |
| `examples/org-policy-baseline.json` | **Baseline** — Essential security, minimal friction (startups) |
| `examples/org-rbac-policy.json` | RBAC and project structure example |
| `examples/api-key-policy.md` | API key lifecycle and rotation policy |
| `examples/content-filter-policy.json` | Content filtering and safety configuration |
| `examples/network-security.md` | IP allowlisting and mTLS configuration guide |

## Key Security Concepts

### Organization Hierarchy

```
Organization
├── Project A
│   ├── Service Accounts
│   ├── API Keys
│   └── Members (with project-level roles)
├── Project B
│   └── ...
└── Organization-wide settings
    ├── SSO / OIDC
    ├── IP Allowlist
    ├── Audit Logs
    └── Data Controls
```

### Role-Based Access Control

OpenAI supports both preset and custom roles at organization and project levels:

| Level | Role | Capabilities |
|-------|------|-------------|
| Organization | Owner | Full administrative control |
| Organization | Reader | View-only access to org settings |
| Project | Owner | Manage project members, keys, and settings |
| Project | Member | Use API within the project |
| Project | Viewer | View-only access to project resources |

Custom roles can include granular permissions for project management, billing, and admin operations. Note: IP allowlist, mTLS, and OIDC management are restricted to organization Owners.

### API Key Types

| Key type | Scope | Use case |
|----------|-------|----------|
| Admin API key | Organization-wide | User/project management automation |
| Project API key | Single project | Application workloads |
| Service account key | Single project | CI/CD and automated systems |

### Audit Logging

Enable audit logs via **Organization Settings → Data Controls → Data Retention**. Events tracked include:
- API key creation, update, deletion
- User and service account changes
- Login/logout events and failures
- Organization configuration changes

## Deployment Checklist

1. Enable SSO/OIDC and enforce for all members.
2. Create separate projects per team/environment.
3. Assign minimal roles — default to Project Member.
4. Limit Organization Owners to ≤ 3 named individuals.
5. Use service accounts (not personal keys) for automated systems.
6. Enable audit logging and export to SIEM.
7. Configure IP allowlist to restrict API access to corporate IPs.
8. Enable mTLS for production workloads where supported.
9. Set up usage limits and billing alerts per project.
10. Rotate all API keys on a 90-day schedule.

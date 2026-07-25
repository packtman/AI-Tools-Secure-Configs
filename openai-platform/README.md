# OpenAI Platform - Secure Admin Configuration

This directory contains security-hardened configurations for the **OpenAI API platform** (platform.openai.com), targeting organization owners and security teams who need to enforce access control, audit logging, and data governance.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-org-policy.md` | Organization security policy checklist |
| `examples/org-policy-strict.json` | **Strict** - Maximum access control, IP allowlist, tight limits (regulated) |
| `examples/org-policy-moderate.json` | **Moderate** - Balanced access control, project-based (enterprise) |
| `examples/org-policy-baseline.json` | **Baseline** - Essential security, minimal friction (startups) |
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

### Newer Admin Controls (2026 OpenAPI)

| Control | Admin surface | Purpose |
|---------|---------------|---------|
| Hosted tool permissions | `/organization/projects/{id}/hosted_tool_permissions` | Enable or disable MCP, web search, image generation, file search, code interpreter per project |
| Project model permissions | `/organization/projects/{id}/model_permissions` | Allow-list or deny-list model IDs per project |
| API call logging mode | Organization settings (`api_call_logging`) | `disabled`, `enabled_per_call`, `enabled_for_selected_projects`, or `enabled_for_all_projects` |
| Data retention API | `/organization/data_retention` and project variant | Set `retention_type` without storing secrets in config files |
| Container/shell network allowlist | Dashboard org allowlist + request `network_policy` | Cap outbound domains for agentic shell/container tools |
| Fine-tuning checkpoint sharing | `/fine_tuning/checkpoints/{id}/permissions` | Control cross-project sharing of fine-tuned checkpoints |

## Deployment Checklist

1. Enable SSO/OIDC and enforce for all members.
2. Create separate projects per team/environment.
3. Assign minimal roles - default to Project Member.
4. Limit Organization Owners to ≤ 3 named individuals.
5. Use service accounts (not personal keys) for automated systems.
6. Enable audit logging and export to SIEM.
7. Configure IP allowlist to restrict API access to corporate IPs.
8. Set project hosted-tool and model permissions for each environment.
9. Configure the container/shell org network allowlist before enabling sandbox networking.
10. Enable mTLS for production workloads where supported.
11. Set up usage limits and billing alerts per project.
12. Rotate all API keys on a 90-day schedule.

## Tier Delta (selected settings)

| Setting | Baseline | Moderate | Strict | Reason |
|---------|----------|----------|--------|--------|
| `hosted_tool_permissions.mcp.enabled` | true | false | false | MCP bridges untrusted tools; enterprise and regulated tiers disable by default |
| `hosted_tool_permissions.web_search.enabled` | true | false | false | Live retrieval expands prompt-injection and data-egress risk |
| `hosted_tool_permissions.code_interpreter.enabled` | true | true | false | Useful for analysis; Strict removes code execution entirely |
| `container_network_policy.org_allowlist_enforced` | false | true | true | Enterprise and Strict require an admin ceiling on outbound domains |
| `container_network_policy.allowed_domains` | [] | minimal package/VCS hosts | [] | Strict prefers no container networking; Moderate allows narrow build hosts |
| `fine_tuning_checkpoint_sharing.cross_project_sharing_allowed` | true | false | false | Prevents silent model artifact sharing across project boundaries |
| `data_controls.api_call_logging` | enabled_for_all_projects | enabled_for_selected_projects | disabled | Balance audit visibility against prompt or response retention risk |
| `project_model_permissions.mode` | allow_list | allow_list | allow_list | All tiers pin approved models; Strict uses the smallest set |

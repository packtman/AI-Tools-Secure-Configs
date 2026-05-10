# OpenAI Platform — API Key Lifecycle Policy

## Key Types

| Type | Prefix | Scope | Use case |
|------|--------|-------|----------|
| Admin API key | `sk-admin-*` | Organization | User/project management |
| Project API key | `sk-proj-*` | Single project | Application workloads |
| Service account key | `sk-svcacct-*` | Single project | CI/CD, automated systems |

## Creation Rules

1. **Admin keys** — Only Organization Owners may create admin keys. Maximum 2 active admin keys at any time.
2. **Project keys** — Created by Project Admins within their project scope.
3. **Service account keys** — Preferred over personal keys for all automated workloads.
4. Every key must have a descriptive name: `{service}-{env}-{purpose}`.

## Storage

| Approved | NOT acceptable |
|----------|---------------|
| HashiCorp Vault | `.env` files in git |
| AWS Secrets Manager | Slack / email |
| Azure Key Vault | Application source code |
| GCP Secret Manager | CI/CD logs |
| GitHub Actions secrets | Local text files |

## Rotation Schedule

| Key type | Interval | Owner |
|----------|----------|-------|
| Admin API key | 60 days | Organization Owner |
| Project API key | 90 days | Project Admin |
| Service account key | 90 days | Service owner |

## Rotation Procedure

1. Create a new key in the OpenAI dashboard or via Admin API.
2. Update the secrets manager entry.
3. Deploy the new secret to consuming services.
4. Verify the new key works in production.
5. Delete the old key via dashboard or API.
6. Log the rotation in your change management system.

**WARNING:** Admin API keys cannot be recovered once lost. Create a new key and revoke the old one.

## Revocation Triggers

Revoke immediately when:
- A team member with key access departs.
- A key is found in source code, logs, or public repositories.
- A security incident involves the project.
- A key has not been used for 30+ days.
- Anomalous usage patterns are detected.

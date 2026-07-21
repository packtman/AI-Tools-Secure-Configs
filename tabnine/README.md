# Tabnine — Secure Admin Configuration

This directory contains security-hardened configurations for **Tabnine** (Enterprise), targeting administrators who need to enforce sandbox restrictions, command permissions, and workspace boundaries.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-admin-policy.md` | Admin security policy checklist |
| `CLI-ROLLOUT.md` | Phased rollout, tier deltas, deployment, validation, rollback, and workflow-preservation guidance |
| `examples/settings-strict.json` | **Strict** Tabnine CLI admin-enforced system settings |
| `examples/settings-moderate.json` | **Moderate** Tabnine CLI admin-enforced system settings |
| `examples/settings-baseline.json` | **Baseline** Tabnine CLI admin-enforced system settings |
| `examples/settings.comments.md` | Key-by-key rationale for the deployable system settings JSON |
| `examples/command-permissions-strict.json` | **Strict** — Read-only commands only, all writes disabled (regulated) |
| `examples/command-permissions-moderate.json` | **Moderate** — Read/test auto-approved, writes need confirmation (enterprise) |
| `examples/command-permissions-baseline.json` | **Baseline** — Common dev commands auto-approved (startups) |
| `examples/command-permissions.json` | Command permission configuration (reference) |
| `examples/workspace-restrictions.json` | Workspace-scoped tool restrictions |
| `examples/model-configuration.json` | Private LLM endpoint configuration |

## Key Security Concepts

### CLI Sandboxing (v6.1+)

Tabnine agents operate within controlled, isolated sandbox boundaries. This prevents:
- Accidental damage to production systems
- Reduced blast radius from agent actions
- Protection against prompt injection attacks

### Run Command Permissions

Fine-grained, per-command permissions with three levels:

| Level | Behavior |
|-------|----------|
| `auto-approve` | Command runs without confirmation |
| `require-confirmation` | User must approve before execution |
| `disabled` | Command is completely blocked |

Permissions can be configured at:
- Individual command level (`git status`, `npm test`)
- Command category level (`git`, `npm`, `docker`)
- Chained commands are intelligently parsed

### Workspace-Scoped Tool Restrictions

File operations are hard-restricted to the active workspace boundary:
- Blocks access to system paths (`/etc/passwd`, `/etc/shadow`)
- Blocks access to private directories (`~/.ssh`, `~/.aws`)
- Prevents data leakage and exfiltration

### Private LLM Endpoints

Enterprise admins can connect private LLM instances:
- Amazon Bedrock
- Azure OpenAI
- GCP Vertex AI
- OpenAI API
- OpenAI-compatible endpoints

## Deployment Checklist

1. Deploy Tabnine Enterprise with SSO integration.
2. Select one `examples/settings-{tier}.json` file and follow `CLI-ROLLOUT.md`.
3. Deploy it to the admin-enforced system settings path through MDM.
4. Configure command permissions with `require-confirmation` as the enterprise default.
5. Configure MCP Governance in the Admin Console. Do not rely on endpoint JSON alone.
6. Enable workspace-scoped restrictions and verify folder trust.
7. Set up private LLM endpoints if not using Tabnine's hosted models.
8. Configure RBAC roles for admins and installation admins.
9. Enable SMTP for user management notifications.
10. Review and restrict model access to approved models only.
11. Monitor usage through the admin dashboard and an organization-owned telemetry collector.

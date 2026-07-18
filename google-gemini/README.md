# Google Gemini — Secure Admin Configuration

This directory contains security-hardened configurations for **Google Gemini** (Gemini API, Gemini for Google Cloud, and Gemini Code Assist), targeting GCP administrators who need to enforce safety settings, VPC controls, and organizational policies.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-admin-policy.md` | Admin security policy checklist |
| `examples/safety-settings-strict.json` | **Strict** — Maximum content filtering, tight limits (regulated) |
| `examples/safety-settings-moderate.json` | **Moderate** — Balanced filtering, reasonable limits (enterprise) |
| `examples/safety-settings-baseline.json` | **Baseline** — Essential filtering, generous limits (startups) |
| `examples/safety-settings.json` | API safety filter configuration (reference) |
| `examples/admin-settings.json` | Gemini for Cloud admin settings |
| `examples/vpc-service-controls.md` | VPC Service Controls setup guide |
| `examples/org-policy.md` | GCP organization policy constraints |

## Key Security Concepts

### Safety Filters

The Vertex AI Gemini API provides configurable safety filters across five categories:

| Category | Description |
|----------|-------------|
| `HARM_CATEGORY_HARASSMENT` | Negative/harmful comments targeting identity |
| `HARM_CATEGORY_HATE_SPEECH` | Rude, disrespectful, or profane content |
| `HARM_CATEGORY_SEXUALLY_EXPLICIT` | Sexual acts or lewd content |
| `HARM_CATEGORY_DANGEROUS_CONTENT` | Content promoting harmful acts |
| `HARM_CATEGORY_JAILBREAK` | Prompts that attempt to bypass model defenses; Vertex AI only and off by default |

Thresholds: `BLOCK_NONE`, `BLOCK_ONLY_HIGH`, `BLOCK_MEDIUM_AND_ABOVE`, `BLOCK_LOW_AND_ABOVE`

Built-in protections against child safety harms and PII **cannot** be adjusted.

### Safety Filter Tier Delta

| Setting | Baseline | Moderate | Strict | Reason for difference |
|---------|----------|----------|--------|-----------------------|
| Harassment and hate speech | `BLOCK_ONLY_HIGH` | `BLOCK_MEDIUM_AND_ABOVE` | `BLOCK_LOW_AND_ABOVE` | Higher tiers trade more false positives for earlier blocking. |
| Sexually explicit and dangerous content | `BLOCK_MEDIUM_AND_ABOVE` | `BLOCK_MEDIUM_AND_ABOVE` | `BLOCK_LOW_AND_ABOVE` | Baseline still blocks medium-risk explicit and dangerous output. |
| `HARM_CATEGORY_JAILBREAK` | `BLOCK_ONLY_HIGH` | `BLOCK_MEDIUM_AND_ABOVE` | `BLOCK_LOW_AND_ABOVE` | The classifier is off by default, so every tier sets it explicitly. Strict blocks low-confidence bypass attempts. |

Safety settings are request fields, not an MDM policy. Apply every category to each Vertex AI
Gemini request in application code or a shared gateway. A missing category silently falls back to
the model default. For `HARM_CATEGORY_JAILBREAK`, that default is off.

### Gemini for Google Cloud Admin Settings

Configurable per-project settings include:
- Release channel (GA vs. preview)
- Code customization toggle
- Logging for Code Assist
- Prompt/response sharing preferences

### VPC Service Controls

Restrict Gemini traffic to your VPC perimeter:
- Prevent data exfiltration via Gemini APIs
- Control which projects can access Gemini services
- Services to include: Gemini for Google Cloud API, Gemini Code Assist API

### IAM

| Role | Description |
|------|-------------|
| `roles/cloudaicompanion.user` | Use Gemini in Cloud Console |
| `roles/cloudaicompanion.admin` | Manage Gemini settings |
| `roles/aiplatform.user` | Use Vertex AI Gemini API |

## Deployment Checklist

1. Assign IAM roles using least privilege — default to `cloudaicompanion.user`.
2. Configure safety filters at the application level for all API calls.
3. Set up VPC Service Controls perimeter for Gemini APIs.
4. Review and configure admin settings per project.
5. Disable logging/sharing unless explicitly needed and approved.
6. Apply organization policy constraints to restrict Gemini usage by project.
7. Monitor usage via Cloud Audit Logs and Cloud Monitoring.
8. Send a known jailbreak test prompt in the pilot environment and confirm the API returns a
   blocked response at the selected threshold.

The jailbreak classifier can block legitimate red-team and prompt-security testing. Route approved
tests to an isolated project with a time-bounded exception rather than weakening the production
threshold.

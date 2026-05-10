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

The Gemini API provides configurable safety filters across four categories:

| Category | Description |
|----------|-------------|
| `HARM_CATEGORY_HARASSMENT` | Negative/harmful comments targeting identity |
| `HARM_CATEGORY_HATE_SPEECH` | Rude, disrespectful, or profane content |
| `HARM_CATEGORY_SEXUALLY_EXPLICIT` | Sexual acts or lewd content |
| `HARM_CATEGORY_DANGEROUS_CONTENT` | Content promoting harmful acts |

Thresholds: `BLOCK_NONE`, `BLOCK_ONLY_HIGH`, `BLOCK_MEDIUM_AND_ABOVE`, `BLOCK_LOW_AND_ABOVE`

Built-in protections against child safety harms and PII **cannot** be adjusted.

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

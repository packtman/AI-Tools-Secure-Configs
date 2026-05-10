# GitHub Copilot — Content Exclusion Configuration Guide

## Repository-Level Exclusion

1. Navigate to **Repository Settings → Code & automation → Copilot → Content exclusion**.
2. Add path patterns to exclude.

### Recommended exclusion patterns

```
- "**/.env"
- "**/.env.*"
- "**/secrets/**"
- "**/*.pem"
- "**/*.key"
- "**/*.p12"
- "**/*.pfx"
- "**/credentials*"
- "**/*secret*"
- "**/token*"
- "**/.aws/**"
- "**/.ssh/**"
- "**/terraform.tfstate"
- "**/terraform.tfstate.backup"
- "**/terraform.tfvars"
```

## Organization-Level Exclusion

1. Navigate to **Organization Settings → Copilot → Content exclusion**.
2. Specify repository and path patterns.

### Example organization exclusion rules

```yaml
# Block secrets across all repositories
"*":
  - "**/.env"
  - "**/.env.*"
  - "**/secrets/**"
  - "**/*.pem"
  - "**/*.key"
  - "**/credentials*"

# Block infrastructure state files
"*":
  - "**/terraform.tfstate"
  - "**/terraform.tfstate.backup"
  - "**/terraform.tfvars"
  - "**/*.auto.tfvars"

# Block specific sensitive repositories entirely
"acme/payroll-service":
  - "**"

"acme/security-configs":
  - "**"
```

## Enterprise-Level Exclusion

Enterprise owners can set exclusions via:
1. **Enterprise Settings → Copilot → Content exclusion**
2. REST API (API version `2026-03-10`):

```bash
curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/enterprises/ENTERPRISE/copilot/content_exclusions \
  -d '{
    "repositories": [
      {
        "name": "acme/*",
        "paths": ["**/.env", "**/.env.*", "**/secrets/**"]
      }
    ]
  }'
```

## Verification

After configuring exclusions, verify they are working:

1. Open a file matching an excluded pattern in your IDE.
2. Copilot should not provide suggestions for that file.
3. Check the Copilot status indicator — it should show "Content excluded" or similar.
4. Review audit logs for content exclusion events.

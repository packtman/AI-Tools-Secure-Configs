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
# Block secrets and infrastructure state across all repositories
"*":
  - "**/.env"
  - "**/.env.*"
  - "**/secrets/**"
  - "**/*.pem"
  - "**/*.key"
  - "**/credentials*"
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

## API Deployment

The public-preview REST API manages organization rules. The endpoint is singular
`content_exclusion`; GitHub does not publish an enterprise endpoint for this payload.

```bash
curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/orgs/ORG/copilot/content_exclusion \
  -d '{
    "*": ["**/.env", "**/.env.*", "**/secrets/**"],
    "payroll-service": ["**"]
  }'
```

The API does not preserve comments and does not support duplicate keys. Keep the reviewed source
in version control, avoid duplicate repository keys, and send the complete desired rule set.

## Verification

After configuring exclusions, verify they are working:

1. Open a file matching an excluded pattern in your IDE.
2. Copilot should not provide suggestions for that file.
3. Check the Copilot status indicator — it should show "Content excluded" or similar.
4. Review audit logs for content exclusion events.

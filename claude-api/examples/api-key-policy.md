# Claude API — API Key Lifecycle Policy

## Key Creation

1. Keys are created by Workspace Developers or Admins inside a single workspace.
2. Every key **must** have a descriptive name following `{service}-{purpose}` (e.g., `chatbot-prod`, `batch-etl`).
3. Record the key's creation date and owning team in your asset inventory.

## Storage

| Approved stores | NOT acceptable |
|-----------------|---------------|
| HashiCorp Vault | `.env` files committed to git |
| AWS Secrets Manager | Slack messages or emails |
| Azure Key Vault | Sticky notes / wikis |
| GCP Secret Manager | Hard-coded in application source |

## Rotation Schedule

| Key type | Rotation interval | Owner |
|----------|-------------------|-------|
| Standard API key (`sk-ant-api03-*`) | 90 days | Service owner |
| Admin API key (`sk-ant-admin01-*`) | 60 days | Org admin |
| Compliance Access key (`sk-ant-api01-*`) | 90 days | Security team |

## Rotation Procedure

1. Generate a new key in the Anthropic Console.
2. Update the secrets manager entry.
3. Deploy the updated secret to the consuming service.
4. Verify the new key works in production.
5. Revoke the old key in the Console.
6. Log the rotation event in your change management system.

## Revocation Triggers

Revoke immediately when:

- A team member with key access leaves the organization.
- A key is suspected to be leaked (commit scan, log exposure).
- A security incident involves the workspace.
- The key has not been used for 30+ days (consider proactive revocation).

## Monitoring

- Enable Anthropic's Compliance API activity feed and alert on `api_key.created` / `api_key.deleted` events.
- Run weekly automated checks for keys approaching rotation deadline.
- Alert the security team if any key exceeds its rotation window by more than 7 days.

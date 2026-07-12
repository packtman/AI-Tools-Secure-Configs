# Claude API — API Key Lifecycle Policy

## Key Creation

1. Keys are created by Workspace Developers or Admins inside a single workspace.
2. Every key **must** have a descriptive name following `{service}-{purpose}` (e.g., `chatbot-prod`, `batch-etl`).
3. Set an expiration date at creation time. Use 90 days for standard API keys and 60 days for Admin API keys unless a stricter tier applies.
4. Do not choose **Never** for enterprise keys unless a documented exception exists.
5. Record the key's creation date, expiration date, and owning team in your asset inventory.

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

Keys with a lifetime of at least 7 days trigger Anthropic expiration warning emails to the creator. Do not rely on email alone. Keep an internal inventory keyed by `expires_at` and alert the owning team before the expiration window.

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
- A key has `expires_at: null` and no approved exception.

## Monitoring

- Enable Anthropic's Compliance API activity feed and alert on `api_key.created` / `api_key.deleted` events.
- Alert on API keys whose `expires_at` value is `null` in enterprise workspaces.
- Run weekly automated checks for keys approaching rotation deadline.
- Alert the security team if any key exceeds its rotation window by more than 7 days.

## MCP Tunnel Credentials

MCP tunnels expose internal MCP servers through Anthropic-assigned tunnel domains. Treat tunnel connector tokens like API keys:

1. Keep MCP tunnels disabled unless a workspace owner documents the business need.
2. Require WIF (Workload Identity Federation) tokens with the `workspace:manage_tunnels` scope for new tunnel management integrations.
3. Store tunnel tokens only in a secrets manager.
4. Rotate tunnel tokens every 30 days (14 days for Strict environments).
5. Track tunnel CA certificate expiration and rotate certificates before they expire.
6. Archive unused tunnels immediately. Archiving retires the hostname and invalidates the connector token.

# Continue.dev — Secrets Management Guide

## Secret Types

### User Secrets

- Created by individual users in Continue settings.
- Available only to the creator.
- Sent to IDE extensions for direct API calls.
- Available on Solo, Teams, and Enterprise plans.

### Org Secrets

- Created by organization admins.
- Never shared directly with users or IDE extensions.
- LLM requests are proxied through Continue's API to protect the secret.
- Available on Teams and Enterprise plans only.

**Best practice:** Use Org Secrets for all shared API keys to prevent key exposure.

## Referencing Secrets

In `config.yaml` or `.continuerc.json`:

```yaml
apiKey: "${{ secrets.OPENAI_API_KEY }}"
```

In `.env` files (workspace or global):

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

`.env` resolution order:
1. Workspace `.env` (`.continue/.env` in project root)
2. Global `.env` (`~/.continue/.env`)

## Security Rules

1. **Never** put API keys directly in `config.yaml` or `.continuerc.json`.
2. **Never** commit `.env` files to version control.
3. **Always** add `.env` and `.continue/.env` to `.gitignore`.
4. Prefer **Org Secrets** over User Secrets for team-wide keys.
5. Rotate secrets on the same schedule as your API key rotation policy.
6. Use a secrets manager for the source of truth; sync to Continue settings.

## .gitignore entries

```
# Continue.dev secrets
.continue/.env
.continue/sessions/
.continue/index/
```

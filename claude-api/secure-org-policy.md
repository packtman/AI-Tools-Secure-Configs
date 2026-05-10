# Claude API — Organization Security Policy

Use this document as a checklist and reference when hardening your Anthropic organization.

---

## 1. Identity & Access

- [ ] **SSO enforcement** — Require SAML or OIDC login; disable password-only access.
- [ ] **SCIM provisioning** — Connect your IdP to automate onboarding/offboarding.
- [ ] **MFA** — Enforce multi-factor authentication for all console users.
- [ ] **Role assignment** — Default every new member to *Workspace User*; promote only with documented approval.
- [ ] **Admin minimization** — Limit Organization Admin count to ≤ 3 named individuals.

## 2. Workspace Architecture

- [ ] **Environment separation** — Maintain distinct workspaces for production, staging, dev, and sandbox.
- [ ] **Team isolation** — Give each team its own workspace; avoid shared workspaces.
- [ ] **Naming convention** — Use `{team}-{env}` naming (e.g., `ml-team-prod`, `backend-staging`).

## 3. API Key Management

- [ ] **One key per service** — Never share an API key across multiple applications.
- [ ] **Secrets manager** — Store all keys in HashiCorp Vault, AWS Secrets Manager, or equivalent.
- [ ] **No keys in code** — Scan repositories with tools like `trufflehog` or `gitleaks`.
- [ ] **Rotation schedule** — Rotate standard API keys every 90 days; admin keys every 60 days.
- [ ] **Revoke on departure** — Immediately revoke keys when a team member leaves.

## 4. Rate Limits & Spend Controls

- [ ] **Workspace rate limits** — Set requests-per-minute and tokens-per-day caps per workspace.
- [ ] **Spend notifications** — Configure alerts at 50%, 75%, and 90% of budget.
- [ ] **Hard caps** — Set maximum monthly spend per workspace where supported.

## 5. Data & Compliance

- [ ] **Compliance API** — Enable at the parent organization level (Enterprise).
- [ ] **Activity feed export** — Stream to SIEM (Splunk, Datadog, etc.) for audit.
- [ ] **Data retention** — Review Anthropic's data handling policy; opt out of training where available.
- [ ] **Prompt logging** — Decide whether prompts/responses should be retained; configure accordingly.

## 6. Network & Transport

- [ ] **TLS enforcement** — All API calls use HTTPS (default; never override).
- [ ] **IP allowlisting** — If supported, restrict API access to your corporate egress IPs.
- [ ] **Proxy configuration** — Route API traffic through your corporate proxy for inspection.

## 7. Monitoring & Incident Response

- [ ] **Anomaly alerts** — Set up alerts for unusual usage spikes (token volume, error rates).
- [ ] **Audit log review** — Review admin actions weekly.
- [ ] **Incident runbook** — Document steps to revoke keys, disable workspaces, and notify stakeholders.

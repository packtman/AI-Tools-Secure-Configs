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
- [ ] **Inference hooks (Enterprise):** Under Data and privacy, allow Inference hooks only after an AI security server exists. Pilot in shadow mode, then enforce. Store the webhook signing secret in a secrets manager (never in git).
- [ ] **Managed Agents Dreams:** Keep Dreams access off until memory-store classification and an org-level disable control exist.

## 6. Network & Transport

- [ ] **TLS enforcement** — All API calls use HTTPS (default; never override).
- [ ] **IP allowlisting** — If supported, restrict API access to your corporate egress IPs.
- [ ] **Proxy configuration** — Route API traffic through your corporate proxy for inspection.

## 7. Monitoring & Incident Response

- [ ] **Anomaly alerts** — Set up alerts for unusual usage spikes (token volume, error rates).
- [ ] **Audit log review** — Review admin actions weekly.
- [ ] **Inference hooks health:** Alert on endpoint status Tripped, sustained failures per minute, and Activity Feed denials that proceeded without inspection under fail-open.
- [ ] **Incident runbook:** Document steps to revoke keys, disable workspaces, turn Enforce verdicts off (or Allow for your organization off), and notify stakeholders.

---

## 8. Inference Hooks Rollout (Claude Enterprise)

Inference hooks: Anthropic holds each governed prompt for your AI security server's allow or deny verdict before the model runs. One org configuration covers claude.ai, Cowork, and Claude Code.

### Phased rollout

| Phase | Exit criteria |
|-------|---------------|
| Pilot (shadow, 10-25% rollout) | Endpoint Healthy for 7 days; false-positive deny rate reviewed; SIEM sees Activity Feed denials and config changes |
| Expanded (enforce, fail-open, 50-100%) | Exception path documented; circuit-breaker playbook tested; developer message sent |
| Org-wide Strict (enforce, fail-closed, 100%) | No unexplained breaker trips for 14 days; on-call owns AI security server SLOs |

### What will break

- Strict fail-closed blocks prompts when the AI security server times out, returns non-200, or the circuit breaker trips.
- Voice mode and ancillary requests (for example title generation) are not hooked.
- Image-only attachments are not fully inspected (metadata and extracted text only).

### Developer-facing message (send before enforce)

> Starting on DATE, Claude Enterprise prompts may be inspected by our AI security server before Claude answers. Shadow mode does not block you. When we turn on enforcement, a blocked prompt shows a policy message. Request exceptions through TICKET_URL. Do not paste secrets or production credentials into prompts.

### Rollback

1. In `claude.ai` → Organization settings → Data and privacy → Inference hooks, turn **Enforce verdicts** off (pauses inspection within about a minute; config kept).
2. For a harder off switch, turn **Allow for your organization** off under Data and privacy (settings page becomes unavailable until re-enabled; re-enable forces Enforce verdicts off).
3. Communicate: "Inline prompt inspection is paused. Continue normal Claude use. Report residual blocks to SECURITY_ALIAS."

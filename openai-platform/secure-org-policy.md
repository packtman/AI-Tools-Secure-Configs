# OpenAI Platform: Organization Security Policy

## 1. Identity & Access Management

- [ ] **SSO enforcement**: Enable OIDC-based SSO; disable password-only access.
- [ ] **MFA**: Require multi-factor authentication for all organization members.
- [ ] **Minimal owners**: Limit Organization Owners to ≤ 3 named individuals.
- [ ] **Role assignment**: Default new members to Project Member; escalate with approval.
- [ ] **Custom roles**: Create restricted roles for audit-only, billing-only, and read-only access.
- [ ] **Service accounts**: Use service accounts (not personal API keys) for all automated systems.

## 2. Project Architecture

- [ ] **Environment separation**: Maintain distinct projects for production, staging, dev, and sandbox.
- [ ] **Team isolation**: Assign each team its own project(s).
- [ ] **Naming convention**: Use `{team}-{env}` (e.g., `backend-prod`, `ml-staging`).
- [ ] **Budget isolation**: Set separate spending limits per project.

## 3. API Key Management

- [ ] **One key per service**: Never share keys across applications.
- [ ] **Secrets manager**: Store all keys in a secrets vault (HashiCorp Vault, AWS Secrets Manager).
- [ ] **No keys in code**: Scan repos with `trufflehog`, `gitleaks`, or GitHub secret scanning.
- [ ] **Rotation schedule**: Rotate project keys every 90 days, admin keys every 60 days.
- [ ] **Revoke on departure**: Immediately revoke keys when a team member leaves.
- [ ] **Admin key caution**: Admin API keys cannot be recovered if lost.

## 4. Network Security

- [ ] **IP allowlist**: Restrict API access to corporate egress IPs.
- [ ] **Container/shell org network allowlist**: In the OpenAI dashboard, set the maximum outbound domains for Containers and Shell tools; request-level `network_policy` must be a subset.
- [ ] **mTLS**: Enable mutual TLS for production API calls.
- [ ] **Proxy routing**: Route API traffic through your corporate proxy for inspection.
- [ ] **TLS enforcement**: Verify all connections use TLS 1.2+.

## 5. Hosted Tools, Models, and Fine-Tuning

- [ ] **Hosted tool permissions**: Use `/organization/projects/{project_id}/hosted_tool_permissions` to disable MCP, web search, image generation, and code interpreter where not required.
- [ ] **Project model permissions**: Use allow-list mode so projects can call only approved model IDs.
- [ ] **Fine-tuning checkpoint sharing**: Restrict `checkpoint.permission` cross-project sharing to Owners with an approval ticket.

## 6. Data Governance

- [ ] **Audit logging**: Enable and export to SIEM (Splunk, Datadog, etc.).
- [ ] **API call logging mode**: Set org `api_call_logging` to `disabled`, `enabled_per_call`, `enabled_for_selected_projects`, or `enabled_for_all_projects` based on privacy needs.
- [ ] **Data retention**: Configure Organization and project data retention via Admin API (`retention_type`) and dashboard controls.
- [ ] **Training opt-out**: Confirm API data is not used for model training (default for API).
- [ ] **Content filtering**: Apply appropriate safety filters for your use case.
- [ ] **PII handling**: Establish policies for what data can be sent to the API.

## 7. Usage & Cost Controls

- [ ] **Project budgets**: Set monthly spending limits per project.
- [ ] **Rate limits**: Configure per-project rate limits.
- [ ] **Billing alerts**: Set alerts at 50%, 75%, and 90% of budget.
- [ ] **Usage monitoring**: Review API usage dashboards weekly.

## 8. Incident Response

- [ ] **Key compromise runbook**: Document steps to revoke keys, rotate secrets, and notify stakeholders.
- [ ] **Anomaly detection**: Alert on unusual usage patterns (token spikes, new IP addresses).
- [ ] **Audit review**: Review admin actions weekly via audit logs.

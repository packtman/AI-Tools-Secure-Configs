# Windsurf — Admin Security Policy

## 1. Identity & Access

- [ ] **SSO enforcement** — Configure OIDC or SAML 2.0 with your identity provider.
- [ ] **SCIM provisioning** — Enable automated user lifecycle management.
- [ ] **MFA** — Enforce multi-factor authentication via your IdP.
- [ ] **RBAC** — Create custom roles with minimal permissions; avoid assigning Admin to developers.
- [ ] **Service keys** — Use scoped service keys for API integrations; rotate every 90 days.

## 2. Enterprise Policies

- [ ] **Extension allowlist** — Restrict to approved extensions only.
- [ ] **Update mode** — Set to controlled/manual updates for production environments.
- [ ] **Feature toggles** — Disable AI features not approved for your organization.
- [ ] **MDM deployment** — Deploy policies via registry (Windows), configuration profiles (macOS), or JSON files (Linux).

## 3. Code Security

- [ ] **Cascade Hooks** — Implement pre-hooks to validate code before execution.
- [ ] **Content filtering** — Use hooks to scan for secrets and sensitive data.
- [ ] **Indexing controls** — Restrict which repositories can be indexed.
- [ ] **Attribution tracking** — Enable attribution to identify AI-generated code.

## 4. MCP Server Security

- [ ] **Audit all MCP servers** — Review source code and permissions before deployment.
- [ ] **Minimal access** — Restrict MCP servers to specific directories.
- [ ] **No secrets in config** — Use environment variable references instead of inline values.
- [ ] **Approved servers only** — Maintain an allowlist of vetted MCP server packages.

## 5. Network Security

- [ ] **Proxy configuration** — Route Windsurf traffic through your corporate proxy.
- [ ] **TLS enforcement** — Ensure all connections use TLS 1.2+.
- [ ] **Firewall rules** — Allowlist only necessary Codeium/Windsurf endpoints.

## 6. Monitoring & Compliance

- [ ] **Analytics dashboards** — Review usage patterns and team activity.
- [ ] **Audit logging** — Enable and export logs for compliance.
- [ ] **FedRAMP** — Use the FedRAMP-compliant deployment if applicable.
- [ ] **Incident response** — Document runbook for revoking access and service keys.

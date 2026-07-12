# Windsurf — Admin Security Policy

## 1. Identity & Access

- [ ] **SSO enforcement** — Configure SAML 2.0 with your identity provider (Okta, Microsoft Entra ID, Google). Note: only SP-initiated SSO is supported.
- [ ] **SCIM provisioning** — Enable automated user lifecycle management; map IdP groups to Windsurf teams.
- [ ] **MFA** — Enforce multi-factor authentication via your IdP.
- [ ] **RBAC** — Create custom roles with minimal permissions; use Super Admin/Group Admin hierarchy for delegation.
- [ ] **Service keys** — Use scoped service keys for API integrations; rotate every 90 days; assign least-privilege permissions.
- [ ] **User groups** — Split users into groups via SCIM for granular feature and role control.

## 2. Enterprise Policies

- [ ] **Extension allowlist** — Restrict to approved extensions only.
- [ ] **Update mode** — Set to controlled/manual updates for production environments.
- [ ] **Feature toggles** — Disable AI features not approved (web search, deploys, conversation sharing).
- [ ] **Auto-execution control** — Set maximum auto-execution level (disabled / confirm_all / confirm_destructive / full).
- [ ] **Model access** — Restrict available models per team or role.
- [ ] **MDM deployment** — Deploy policies via registry (Windows), configuration profiles (macOS), or JSON files (Linux).

## 3. Agent & Code Security

- [ ] **Cascade auto-execution** — Set maximum steps and require human confirmation for consequential actions.
- [ ] **Cascade Hooks** — Implement pre-hooks to validate code before execution.
- [ ] **Content filtering** — Use hooks to scan for secrets and sensitive data.
- [ ] **Indexing controls** — Restrict which repositories can be indexed.
- [ ] **Attribution filtering** — Enable attribution filtering to identify and flag AI-generated code with license concerns.
- [ ] **`.codeiumignore`** — Deploy ignore patterns to exclude sensitive files from AI context.

## 4. MCP Server Security

- [ ] **Admin-level whitelist** — Configure approved MCP servers in Admin Portal; block all unapproved.
- [ ] **Audit all MCP servers** — Review source code and permissions before adding to whitelist.
- [ ] **Read/write permissions** — Enable read-only operations for analysts; restrict write tools to senior developers.
- [ ] **Approval workflows** — Require human confirmation before executing infrastructure-modifying commands.
- [ ] **No secrets in config** — Use environment variable references instead of inline values.

## 5. Network & Deployment Security

- [ ] **Proxy configuration** — Route Windsurf traffic through your corporate proxy.
- [ ] **TLS enforcement** — Ensure all connections use TLS 1.2+; set `enforceProxyStrictSSL: true`.
- [ ] **Firewall rules** — Allowlist only necessary Codeium/Windsurf endpoints.
- [ ] **Deployment mode** — Choose Cloud, Hybrid, or Self-Hosted based on compliance requirements.
- [ ] **Self-hosted** — For CMMC/HIPAA/FedRAMP: deploy all inference on customer infrastructure.

## 6. Monitoring & Compliance

- [ ] **Analytics dashboards** — Review usage patterns, team activity, and credit consumption.
- [ ] **Audit logging** — Enable and export AI interaction logs for compliance.
- [ ] **SIEM integration** — Route audit logs to your SIEM via service key API.
- [ ] **Compliance certifications** — Verify SOC 2 Type II; use self-hosted for FedRAMP High/HIPAA/CMMC.
- [ ] **Incident response** — Document runbook for revoking access, service keys, and SCIM deprovisioning.

# Windsurf, Admin Security Policy

## 1. Identity & Access

- [ ] **SSO enforcement**, Configure SAML 2.0 with your identity provider (Okta, Microsoft Entra ID, Google). Note: only SP-initiated SSO is supported.
- [ ] **SCIM provisioning**, Enable automated user lifecycle management; map IdP groups to Windsurf teams.
- [ ] **MFA**, Enforce multi-factor authentication via your IdP.
- [ ] **RBAC**, Create custom roles with minimal permissions; use Super Admin/Group Admin hierarchy for delegation.
- [ ] **Service keys**, Use scoped service keys for API integrations; rotate every 90 days; assign least-privilege permissions.
- [ ] **User groups**, Split users into groups via SCIM for granular feature and role control.

## 2. Enterprise Policies (Devin Desktop MDM)

- [ ] **Extension publisher allowlist**, Deploy MDM `AllowedExtensions` as a JSON string of publishers (for example `{"ms-python": true}`), not only extension IDs.
- [ ] **Update mode**, Set to controlled/manual updates for production environments.
- [ ] **Telemetry / feedback**, Set `EnableTelemetry` and `EnableFeedback` false for Moderate and Strict.
- [ ] **Feature toggles**, Disable AI features not approved (web search, deploys, conversation sharing).
- [ ] **Auto-execution control**, Set maximum auto-execution level (disabled / confirm_all / confirm_destructive / full).
- [ ] **Model access**, Restrict available models per team or role.
- [ ] **MDM deployment**, Windows registry `Software\Policies\Windsurf\Windsurf`, macOS `.mobileconfig`, Linux `/etc/windsurf/policies/policy.json`.

## 3. Devin CLI Team Settings (admin portal)

- [ ] **Web search**, Keep disabled for Moderate and Strict (enterprise default is off).
- [ ] **MCP servers**, Disable entirely on Strict; on Moderate enable only with registry enforcement.
- [ ] **MCP registry**, Set org registry URL(s) and turn enforcement on for Moderate and Strict.
- [ ] **Terminal permissions**, Team `deny` / `ask` / `allow` rules with highest precedence over user config.
- [ ] **Sandbox enforcement**, Use `optional` until Windows and Linux (`bwrap`/`socat`) fleet readiness; use `required` only for Strict macOS/Linux cohorts.
- [ ] **Sandbox domain lists**, Authoritative allowlist plus additive denylist for egress control.
- [ ] **Sandbox excluded commands**, Deny wildcard escapes; carve out only approved tools such as `gh`.
- [ ] **Install Devin CLI toggle**, Leave off until onboarding is ready (`showInstallDevinCli: false`).
- [ ] **Devin Local Agent**, Leave disabled until a named pilot completes terminal and MCP review.

## 4. Agent & Code Security

- [ ] **Cascade auto-execution**, Set maximum steps and require human confirmation for consequential actions.
- [ ] **Cascade Hooks**, Implement pre-hooks to validate code before execution.
- [ ] **Content filtering**, Use hooks to scan for secrets and sensitive data.
- [ ] **Indexing controls**, Restrict which repositories can be indexed.
- [ ] **Attribution filtering**, Enable attribution filtering (Enterprise support) to flag public-code matches.
- [ ] **`.codeiumignore` / ignore files**, Deploy ignore patterns to exclude sensitive files from AI context.
- [ ] **Overlap check**, Confirm Cascade editor controls and Devin CLI controls are both set (do not configure only one).

## 5. MCP Server Security

- [ ] **Admin-level whitelist**, Configure approved MCP servers in Admin Portal; block all unapproved.
- [ ] **MCP registry enforcement**, Prefer registry URLs over ad-hoc allowlists when available.
- [ ] **Audit all MCP servers**, Review source code and permissions before adding to whitelist.
- [ ] **Read/write permissions**, Enable read-only operations for analysts; restrict write tools to senior developers.
- [ ] **Approval workflows**, Require human confirmation before executing infrastructure-modifying commands.
- [ ] **No secrets in config**, Use environment variable references instead of inline values.

## 6. Network & Deployment Security

- [ ] **Proxy configuration**, Route Windsurf / Devin Desktop traffic through your corporate proxy.
- [ ] **TLS enforcement**, Ensure all connections use TLS 1.2+; set `enforceProxyStrictSSL: true`.
- [ ] **Firewall rules**, Allowlist only necessary Cognition / Windsurf / Devin endpoints.
- [ ] **Deployment mode**, Choose Cloud, Hybrid, or Self-Hosted based on compliance requirements.
- [ ] **Self-hosted**, For CMMC/HIPAA/FedRAMP: deploy all inference on customer infrastructure.

## 7. Monitoring & Compliance

- [ ] **Analytics dashboards**, Review usage patterns, team activity, and credit consumption.
- [ ] **Audit logging**, Enable and export AI interaction logs for compliance.
- [ ] **SIEM integration**, Route audit logs to your SIEM via service key API.
- [ ] **Compliance certifications**, Verify SOC 2 Type II; use self-hosted for FedRAMP High/HIPAA/CMMC.
- [ ] **Incident response**, Document runbook for revoking access, service keys, and SCIM deprovisioning.
- [ ] **Rollback**, Keep previous MDM profile / `policy.json` and portal screenshots ready; revert `sandboxEnforcement` to `optional` first if Windows pilots fail.

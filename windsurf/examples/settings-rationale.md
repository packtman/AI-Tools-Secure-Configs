# Windsurf — Enterprise Security Settings Rationale

Every setting below explains **what it controls**, **why it matters**, the **recommended value**, and the **risk of misconfiguration**. An admin reading this should understand the reasoning behind each recommendation, not just the value to set.

---

## 1. SSO (OIDC / SAML)

| Aspect | Detail |
|--------|--------|
| **What it does** | Replaces Windsurf-local username/password authentication with your corporate identity provider (Okta, Azure AD, Google Workspace, etc.) via OIDC or SAML 2.0. |
| **Recommended** | **Enforce SSO for all users.** Disable local account creation after SSO enrollment. |

### Why Enforce SSO Over Local Accounts

| Reason | Explanation |
|--------|------------|
| Centralized credential management | Password policies, MFA enforcement, and credential rotation are managed in one place. Local Windsurf accounts bypass all of these. |
| Instant deprovisioning | Disabling a user in your IdP immediately revokes Windsurf access. Local accounts persist until someone remembers to delete them. |
| Conditional access | SSO enables device trust, network location, and risk-based access policies. Local accounts have none of these. |
| Audit trail | SSO login events appear in your IdP's audit log alongside all other application access. Local account logins are only in Windsurf's logs. |
| Compliance | SOC 2, ISO 27001, and FedRAMP all require centralized authentication. Local accounts are audit findings. |

### Misconfiguration Risk

If SSO is configured but not **enforced**, users can create local accounts that bypass MFA, conditional access, and deprovisioning. A departed employee's local Windsurf account remains active indefinitely. Always disable local account creation after SSO is live.

---

## 2. SCIM Provisioning

| Aspect | Detail |
|--------|--------|
| **What it does** | Automates user creation, role assignment, and deprovisioning by synchronizing your IdP's directory with Windsurf via SCIM 2.0. |
| **Recommended** | **Enable SCIM with your IdP.** Map IdP groups to Windsurf roles. |

### Why Automate User Lifecycle

| Scenario | Without SCIM | With SCIM |
|----------|-------------|-----------|
| New hire | Admin manually creates Windsurf account, assigns role, adds to team | User auto-provisioned with correct role when added to IdP group |
| Role change | Admin must remember to update Windsurf role separately | Role updates automatically when IdP group membership changes |
| Termination | Admin must manually deactivate Windsurf account (often forgotten) | Account deactivated within minutes of IdP disable |
| License tracking | Manual headcount reconciliation | Automatic — only active IdP users consume licenses |

### Misconfiguration Risk

Without SCIM, orphaned accounts accumulate. A typical enterprise discovers 15–30% of SaaS accounts belong to former employees during annual access reviews. Each orphaned account is a credential stuffing target and a compliance violation.

---

## 3. RBAC Roles — Least Privilege

| Role | What it grants | Who should have it | Why |
|------|---------------|-------------------|-----|
| **Admin** | Full platform control: SSO config, SCIM, service keys, role management, indexing, billing | 2–3 platform admins | Admin can disable SSO, create unrestricted service keys, or change indexing settings. Limit to break-glass scenarios and designated platform owners. |
| **User** | Standard IDE access, Cascade AI, code completion, file editing | All developers | Sufficient for day-to-day development. Cannot modify platform settings or view other users' analytics. |
| **Custom roles** | Scoped permissions (e.g., analytics read-only, team management) | Security auditors, team leads, compliance officers | Avoids granting full Admin to users who need only a subset of capabilities. |

### When to Create Custom Roles

| Use case | Permissions needed | Why not use Admin |
|----------|-------------------|------------------|
| Security auditor | Read analytics, attribution, audit logs | Auditors need visibility, not control. Admin access would let them modify the settings they're auditing. |
| Team lead | Manage team members, view team analytics | Team leads need people management, not platform configuration. |
| Billing manager | View license usage, manage billing | Billing access should not include SSO configuration or service key management. |

### Misconfiguration Risk

Granting Admin to all team leads (a common shortcut) means any team lead can reconfigure SSO, create unscoped service keys, or disable workspace trust. Custom roles eliminate this by granting exactly the permissions needed.

---

## 4. Enterprise Policies

| Policy | What it controls | Recommended value | Why | Misconfiguration risk |
|--------|-----------------|-------------------|-----|----------------------|
| `AllowedExtensions` | Allowlist of permitted VS Code extensions | Explicit allowlist of vetted extensions | Extensions execute arbitrary code in the IDE process. An unvetted extension can read all open files, intercept keystrokes, or exfiltrate source code to an external server. | An empty allowlist blocks all extensions (breaks workflows). No allowlist (unrestricted) allows any extension including malicious ones. |
| `UpdateMode` | How Windsurf receives updates (`auto`, `manual`, `none`) | `manual` for enterprise; `auto` for developer teams | `manual` lets IT test updates before deployment. `auto` ensures timely security patches but may introduce breaking changes. | `none` freezes the version permanently — missed security patches accumulate. `auto` in regulated environments may deploy untested features. |
| `WorkspaceTrustEnabled` | Whether untrusted workspaces trigger restricted mode | `true` | Prevents malicious repositories from automatically executing tasks, running extensions, or triggering Cascade on open. | If `false`, cloning a repository with a malicious `.windsurf/` configuration automatically executes attacker-controlled hooks and extensions. |
| `TelemetryLevel` | What usage data is sent to Windsurf | `off` for enterprise | Telemetry may include file paths, project names, and usage patterns that reveal organizational structure and technology stack. | If set to `full`, file paths and project metadata are transmitted externally, potentially violating NDAs or data classification policies. |
| `blockExternalExtensions` | Whether extensions from non-marketplace sources are blocked | `true` | Side-loaded extensions bypass marketplace review and malware scanning. | If `false`, users can install `.vsix` files from any source, including phishing emails. |
| `enforceProxyStrictSSL` | Whether TLS certificate validation is enforced for proxy connections | `true` | Prevents MITM attacks on proxy connections. Some corporate proxies use self-signed certificates — add the CA to the trust store instead of disabling validation. | If `false`, any network intermediary can intercept and modify traffic between Windsurf and its APIs. |
| `disableUntrustedWorkspaces` | Whether to block opening untrusted workspace folders entirely | `true` for regulated environments | More restrictive than workspace trust — completely prevents opening unvetted repositories. | If `true` in developer environments, it may block legitimate workflows (e.g., reviewing external PRs). Balance with workspace trust. |

---

## 5. Cascade Hooks — Governance Enforcement

| Hook type | Timing | Can block? | Primary use case |
|-----------|--------|------------|-----------------|
| **Pre-hook** | Before Cascade executes an action | **Yes** | Policy enforcement, secret scanning, path restriction |
| **Post-hook** | After Cascade completes an action | No | Audit logging, notifications, compliance recording |

### Why Hooks Are Essential for Governance

| Reason | Explanation |
|--------|------------|
| Preventive control | Pre-hooks can block actions before they occur — scanning for secrets in generated code, preventing modification of sensitive paths (`.env`, `*.pem`, `.ssh/`), or enforcing naming conventions. |
| Detective control | Post-hooks log every Cascade action with timestamp, user, workspace, and action type. This creates an audit trail for compliance and incident investigation. |
| Separation of duties | Hook scripts are managed by security/platform teams and deployed to a read-only directory. Developers cannot modify or bypass the enforcement logic. |
| Custom policy | Hooks execute arbitrary shell commands, enabling integration with existing security tools (secret scanners, SAST, policy engines). |

### Recommended Hook Set

| Hook | Type | Purpose | Why needed |
|------|------|---------|-----------|
| Secret scanner | Pre-hook | Scan generated code for API keys, tokens, passwords | Cascade may generate code containing placeholder credentials that look real, or copy credentials from context. |
| Path restriction | Pre-hook | Block modification of `.env`, `secrets/`, `*.pem`, `*.key`, `.ssh/`, `.aws/` | Cascade should never modify credential files. Even accidental edits can corrupt authentication. |
| Audit logger | Post-hook | Log all Cascade actions to central log | Provides the audit trail required for SOC 2, ISO 27001, and incident response. |
| SAST trigger | Post-hook | Run static analysis on modified files | Catches security vulnerabilities introduced by AI-generated code before they reach code review. |

### Misconfiguration Risk

Without pre-hooks, Cascade can generate code containing hardcoded secrets and commit it directly. Without post-hooks, there is no audit trail of AI-generated changes, making incident investigation and compliance audits impossible. Hooks that exit non-zero on error (blocking all actions) should be tested extensively before production deployment.

---

## 6. MCP Configuration (`.windsurf/mcp_config.json`)

| Aspect | Detail |
|--------|--------|
| **What it does** | Defines Model Context Protocol servers that Cascade can use as tools (filesystem access, API calls, database queries, etc.). |
| **Recommended** | Only include audited, IT-approved MCP servers. Scope filesystem servers to specific directories. |

### Same Risks as Claude Desktop MCP

| Risk | How it applies to Windsurf |
|------|---------------------------|
| Arbitrary code execution | MCP servers run as local processes with the user's privileges. A malicious server can execute any command. |
| Data exfiltration | A filesystem MCP server scoped to `/` can read any file the user can access, including `~/.ssh`, `~/.aws`, and `~/.gnupg`. |
| Supply chain attack | `npx -y @some-package/mcp-server` downloads and runs code from npm. A typosquatted package name executes malicious code. |
| Workspace-scoped config | `.windsurf/mcp_config.json` in a repository means cloning that repo installs the attacker's MCP servers. |

### Recommended Controls

| Control | Implementation | Why |
|---------|---------------|-----|
| Allowlist MCP servers | Only permit specific, audited server packages | Prevents users from adding arbitrary MCP servers |
| Scope filesystem access | Limit to `./src`, `./tests`, or specific subdirectories | Prevents access to sensitive files outside the project |
| Pin package versions | Use exact versions, not `latest` or `-y` | Prevents supply chain attacks via compromised new versions |
| Review per-project configs | Scan `.windsurf/mcp_config.json` in CI | Catches malicious MCP configurations in pull requests |

### Misconfiguration Risk

An unscoped filesystem MCP server (`"args": ["/"]`) gives Cascade read/write access to the entire filesystem. A developer who copies an MCP config from a blog post may inadvertently install an unaudited server that exfiltrates code to an external endpoint.

---

## 7. Remote Indexing

| Aspect | Detail |
|--------|--------|
| **What it does** | Indexes your codebase remotely to provide better code search and context for Cascade. |
| **Recommended** | Use single-tenant indexing. Understand what data is indexed and where it is stored. |

### Data Handling Implications

| Concern | Detail |
|---------|--------|
| What is indexed | File paths, code content, symbol tables, dependency graphs. This is effectively a full copy of your source code. |
| Where it is stored | Depends on deployment tier. Shared infrastructure (multi-tenant) stores indices alongside other customers. Single-tenant stores in dedicated infrastructure. |
| Retention | Indexed data persists until the workspace is removed. Ensure retention aligns with your data classification policy. |
| Access control | Only users with access to the workspace can query the index. Verify this with your Windsurf account team. |

### Single-Tenant Security

For enterprises with sensitive IP, single-tenant indexing ensures your code index is stored in isolated infrastructure, not shared with other Windsurf customers. This eliminates the risk of cross-tenant data leakage due to infrastructure bugs.

### Misconfiguration Risk

Enabling remote indexing on a repository containing classified or export-controlled code may violate data handling requirements. If the index is multi-tenant and a cross-tenant vulnerability is discovered, all indexed code is at risk.

---

## 8. Proxy Configuration

| Setting | What it controls | Recommended value | Why |
|---------|-----------------|-------------------|-----|
| `http_proxy` | HTTP proxy for non-TLS traffic | Corporate proxy URL | Routes all HTTP traffic through the corporate proxy for inspection and logging. |
| `https_proxy` | HTTPS proxy for TLS traffic | Corporate proxy URL | Routes TLS traffic through the proxy. Required for DLP inspection of AI API calls. |
| `no_proxy` | Hosts that bypass the proxy | `localhost,127.0.0.1,.corp.example.com` | Local and internal traffic should not traverse the proxy (latency, availability). |
| `enforceProxyStrictSSL` | Whether to validate proxy TLS certificates | `true` | See enterprise policies section. |

### Why Proxy Configuration Matters

Corporate proxies provide visibility into Windsurf's network traffic. Without proxy configuration, Windsurf makes direct connections to external APIs, bypassing DLP, URL filtering, and network logging. This creates a blind spot in your network security monitoring.

### Misconfiguration Risk

If `no_proxy` is too broad (e.g., `*`), all traffic bypasses the proxy. If `enforceProxyStrictSSL` is `false`, the proxy connection is vulnerable to MITM. If proxy is not configured at all, Windsurf traffic is invisible to network security tools.

---

## 9. Service Keys

| Aspect | Detail |
|--------|--------|
| **What it does** | API keys for programmatic access to Windsurf enterprise features (SCIM provisioning, API integrations). |
| **Recommended** | Rotate every 90 days. Scope to minimum required permissions. |

| Practice | Recommendation | Why |
|----------|---------------|-----|
| Rotation schedule | Every 90 days (or immediately on suspected compromise) | Limits the window of exposure for leaked keys. Automated rotation via secrets manager is ideal. |
| Scoped permissions | Create separate keys for SCIM, analytics, and administration | A SCIM key should not have admin permissions. Compromise of one key limits blast radius. |
| Storage | Secrets manager (Vault, AWS Secrets Manager, Azure Key Vault) | Never store service keys in code, CI variables without encryption, or shared documents. |
| Monitoring | Alert on unusual API patterns (bulk user creation, rapid role changes) | Detects compromised service key usage. |
| Revocation | Immediate revocation process documented and tested | When a key is suspected compromised, revocation must happen in minutes, not hours. |

### Misconfiguration Risk

A single unscoped, unrotated service key stored in a CI pipeline configuration can grant an attacker full admin access to Windsurf, including the ability to disable SSO, create backdoor accounts, and exfiltrate analytics data.

---

## 10. Analytics and Attribution

| Setting | What it does | Recommended configuration | Why |
|---------|-------------|--------------------------|-----|
| Analytics | Tracks AI usage patterns (completions, Cascade sessions, time saved) | Enable for admins and security auditors only | Usage data reveals adoption patterns and ROI. Restrict access to prevent competitive intelligence leakage. |
| Attribution | Links AI-generated code to specific users and sessions | Enable, restrict to security auditors | Critical for incident response ("which AI session generated the vulnerable code?") and compliance ("can we attribute this code for IP purposes?"). |

### Compliance Tracking

| Requirement | How analytics/attribution helps |
|-------------|-------------------------------|
| SOC 2 CC6.1 | Demonstrates access controls are monitored |
| ISO 27001 A.12.4 | Provides logging and monitoring evidence |
| EU AI Act | Attribution supports transparency requirements for AI-generated content |
| Internal audit | Quantifies AI usage for risk assessment |

### Misconfiguration Risk

If attribution is disabled, there is no way to trace AI-generated code back to the session that created it. This makes incident investigation, IP attribution, and compliance reporting impossible.

---

## 11. FedRAMP Deployment

| Aspect | Detail |
|--------|--------|
| **What it does** | Windsurf offers a FedRAMP-authorized deployment (GovCloud) for U.S. federal agencies and contractors. |
| **When to use** | When handling CUI (Controlled Unclassified Information), working under DFARS/NIST 800-171, or when your ATO requires FedRAMP-authorized tools. |

| Criterion | Standard deployment | GovCloud deployment |
|-----------|-------------------|-------------------|
| Data residency | Multi-region | US-only |
| Compliance | SOC 2 | FedRAMP Moderate (or higher) |
| Personnel | Standard background checks | US persons with government clearance |
| Infrastructure | Shared cloud | GovCloud isolated infrastructure |
| Incident response | Standard SLA | FedRAMP incident response requirements |

### Misconfiguration Risk

Using the standard Windsurf deployment for CUI or ITAR-controlled code violates DFARS 252.204-7012 and can result in contract termination, loss of clearance, and civil penalties. Always confirm the deployment type before onboarding sensitive government projects.

---

## 12. Telemetry Controls

| Setting | What it controls | Recommended value | Why |
|---------|-----------------|-------------------|-----|
| `TelemetryLevel` | Volume and type of usage data sent to Windsurf | `off` for enterprise | Even "anonymous" telemetry can leak organizational structure through file paths, project names, and usage patterns. |

### Privacy Implications

| Data type | Risk if transmitted |
|-----------|-------------------|
| File paths | Reveal project names, technology stack, internal naming conventions |
| Code snippets | May contain proprietary algorithms or business logic |
| Error messages | May contain stack traces with internal URLs, database names, or usernames |
| Usage patterns | Reveal team size, work hours, and productivity metrics |

### Misconfiguration Risk

If telemetry is set to `full` or `crash`, organizational metadata leaves the network. In competitive industries, this metadata has intelligence value. In regulated industries, it may constitute a data export violation.

---

## 13. Feature Toggles

| Aspect | Detail |
|--------|--------|
| **What it does** | Controls whether new Windsurf features are enabled when released. |
| **Recommended** | New features default to **off** for enterprise. Enable after security review. |

### Why New Features Default to Off

| Reason | Explanation |
|--------|------------|
| Security review | New features may introduce new data flows, API integrations, or permissions that have not been evaluated against your security policy. |
| Change management | Enterprise environments require controlled rollouts. Automatic feature enablement bypasses change advisory boards. |
| Testing | New features may interact unexpectedly with your proxy configuration, DLP rules, or MCP setup. |
| Compliance | Features that change data handling (e.g., new indexing capabilities) must be reviewed for regulatory impact before activation. |

### Recommended Process

1. New feature released → remains off by default.
2. Security team reviews feature documentation and data flows.
3. Test in staging/sandbox workspace.
4. Enable for pilot group.
5. Roll out to all users after validation.

### Misconfiguration Risk

If features auto-enable, a new capability that sends code to an external service may activate before the security team is aware. This is especially dangerous for features involving remote indexing, new MCP servers, or third-party integrations.

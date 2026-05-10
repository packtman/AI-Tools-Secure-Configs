# GitHub Copilot — Settings Rationale

> A comprehensive rationale for every security-relevant GitHub Copilot setting.
> For each control: what it does, why it matters, recommended values per environment, and what goes wrong when it is misconfigured.

---

## 1. Organization-Level Feature Policies

Feature policies are configured at **Organization Settings → Copilot → Policies & features**. Each toggle controls whether a capability is available to seated members.

### 1.1 `copilot_in_ide` — Code Completions

| Aspect | Detail |
|--------|--------|
| **What it does** | Enables inline code completions in supported IDEs (VS Code, JetBrains, Visual Studio, Neovim). |
| **Why it matters** | This is the core Copilot feature. Disabling it shuts off all code suggestions while leaving chat and other features intact. |
| **Recommended value** | `enabled` in all environments. If you are paying for Copilot seats, completions are the primary value driver. |
| **Misconfiguration risk** | Disabling by accident silently removes suggestions for every developer in the org. No error is shown — completions simply stop appearing. Developers may waste time debugging IDE extensions. |

### 1.2 `copilot_chat_in_ide` — Chat in IDE

| Aspect | Detail |
|--------|--------|
| **What it does** | Enables the Copilot Chat panel and inline chat (`Ctrl+I`) inside editors. |
| **Why it matters** | Chat allows natural-language interaction with Copilot and can reference open files, terminal output, and workspace context. This is a larger attack surface than completions because users can ask the model to process arbitrary content. |
| **Recommended value** | `enabled` for engineering teams. Consider `disabled` for non-technical seats that only need completions. |
| **Misconfiguration risk** | Disabling unintentionally removes a high-productivity feature. Enabling without content exclusion rules means chat can read and reference files that should be hidden from Copilot (secrets, state files). |

### 1.3 `copilot_cli` — Copilot in the CLI

| Aspect | Detail |
|--------|--------|
| **What it does** | Enables `gh copilot suggest` and `gh copilot explain` commands in the GitHub CLI. |
| **Why it matters** | CLI integration translates natural language into shell commands. This raises risk because the generated commands can modify the system, delete files, or leak environment variables if the user runs them without review. |
| **Recommended value** | `disabled` in production/regulated environments. `enabled` only for developer workstations with clear usage policies. |
| **Misconfiguration risk** | Enabling in CI/CD runners or shared servers lets the model generate and potentially execute destructive commands. An attacker with access to a developer's terminal could use Copilot CLI to generate exfiltration commands that look innocuous. |

### 1.4 `copilot_code_review` — Code Review

| Aspect | Detail |
|--------|--------|
| **What it does** | Enables Copilot to review pull requests and provide AI-generated review comments on diffs. |
| **Why it matters** | AI code review catches classes of bugs and security issues that human reviewers miss under time pressure: SQL injection patterns, hardcoded secrets, missing input validation, insecure deserialization. It acts as a safety net, not a replacement for human review. |
| **Recommended value** | `enabled` in all environments. This is a security-positive feature. |
| **Misconfiguration risk** | Disabling removes a free layer of automated security review. There is no meaningful downside to enabling it — the worst case is a false positive review comment. |

### 1.5 `copilot_pull_request_summaries` — PR Summaries

| Aspect | Detail |
|--------|--------|
| **What it does** | Generates natural-language summaries of pull request changes to aid reviewers. |
| **Why it matters** | Summaries accelerate review by giving reviewers a high-level understanding of what changed. In security-sensitive repos, this helps reviewers identify unexpected scope creep (e.g., a "docs-only" PR that also modifies auth logic). |
| **Recommended value** | `enabled` for most organizations. |
| **Misconfiguration risk** | Low risk either way. Enabling it on repos with content exclusion rules may produce incomplete summaries if the excluded files are central to the change. |

### 1.6 `copilot_web_search` — Web Search

| Aspect | Detail |
|--------|--------|
| **What it does** | Allows Copilot Chat to search the web for answers when its training data is insufficient. Queries are sent to a search provider. |
| **Why it matters** | Web search means conversation context — including code snippets the user shares with Copilot and the questions they ask — may be included in search queries sent to external services. This creates a data leakage vector for proprietary code patterns and internal project names. |
| **Recommended value** | **`disabled`** in all enterprise environments. |
| **Misconfiguration risk** | Enabling allows Copilot to send fragments of private conversations and code to external search APIs. Even if the search provider has a data processing agreement, the telemetry surface area increases substantially. There is no way to audit which queries were sent in real time. |

### 1.7 `copilot_bing_search` — Bing Search

| Aspect | Detail |
|--------|--------|
| **What it does** | Specifically allows Copilot Chat to use Bing as the search backend. This is a subset of the web search capability. |
| **Why it matters** | Same risks as web search (above), plus data flows through Microsoft's Bing infrastructure. For organizations with data processing agreements that don't cover Bing, this creates a compliance gap. |
| **Recommended value** | **`disabled`** in all enterprise environments. |
| **Misconfiguration risk** | Identical to web search. Enabling without a Bing-specific DPA may violate GDPR, CCPA, or contractual obligations to clients. Internal project names, proprietary API patterns, and technology stack details can leak through search queries. |

### Feature Policy Summary Table

| Policy | Dev/Startup | Enterprise | Regulated/Financial |
|--------|:-----------:|:----------:|:-------------------:|
| `copilot_in_ide` | enabled | enabled | enabled |
| `copilot_chat_in_ide` | enabled | enabled | enabled |
| `copilot_cli` | enabled | disabled | disabled |
| `copilot_code_review` | enabled | enabled | enabled |
| `copilot_pull_request_summaries` | enabled | enabled | enabled |
| `copilot_web_search` | enabled | **disabled** | **disabled** |
| `copilot_bing_search` | enabled | **disabled** | **disabled** |

---

## 2. Content Exclusion Patterns

Content exclusion is configured at **Organization Settings → Copilot → Content exclusion** or per-repository. Patterns use `fnmatch` notation (case insensitive).

### Why Content Exclusion Exists

Copilot reads open files and nearby files to generate context for suggestions. Without exclusion rules, Copilot will ingest and potentially reproduce content from files containing secrets, cryptographic material, or regulated data. Content exclusion tells Copilot to **ignore** matching files — no suggestions are generated for them and their content is not sent as context.

### What to Exclude and Why

| Category | Patterns | Rationale |
|----------|----------|-----------|
| **Environment files / secrets** | `**/.env`, `**/.env.*`, `**/secrets/**`, `**/*secret*`, `**/credentials*`, `**/token*` | `.env` files are the most common location for hardcoded API keys, database passwords, and service tokens. If Copilot ingests these, it may reproduce secrets in completions — which then appear in version control, logs, or screen shares. |
| **Cryptographic material** | `**/*.pem`, `**/*.key`, `**/*.p12`, `**/*.pfx`, `**/*.jks`, `**/*.keystore` | Private keys and certificates must never be processed by any external service. A leaked private key compromises TLS, code signing, or SSH access. Even partial exposure through a Copilot suggestion is a critical incident. |
| **Cloud credentials** | `**/.aws/**`, `**/.azure/**`, `**/.config/gcloud/**`, `**/.ssh/**`, `**/.kube/config` | Cloud provider credential files contain access keys, session tokens, and cluster configurations. Copilot ingesting `~/.aws/credentials` could reproduce AWS access keys in a suggestion. |
| **IaC state files** | `**/terraform.tfstate`, `**/terraform.tfstate.backup`, `**/terraform.tfvars`, `**/*.auto.tfvars`, `**/.pulumi/**` | Terraform state files contain the plaintext values of every resource attribute — including database passwords, API keys, and private IPs. `tfvars` files often contain secrets passed as variables. These are the single most dangerous files to expose to any AI tool. |
| **Data files** | `**/*.sql`, `**/*.dump`, `**/*.bak`, `**/fixtures/**`, `**/seeds/**` | Database dumps and seed files may contain PII, financial data, or health records. Even test fixtures often use production-derived data that hasn't been properly anonymized. |
| **Vendor / build directories** | `**/node_modules/**`, `**/vendor/**`, `**/.venv/**`, `**/dist/**` | Excluding these reduces noise (Copilot suggesting vendored code) and avoids ingesting dependencies that may contain embedded credentials or license-problematic code. |

### Scope Hierarchy

| Level | Configured by | Applies to |
|-------|--------------|------------|
| Repository | Repository admins | That repository only |
| Organization | Organization owners | All repos in the org (can target specific repos) |
| Enterprise | Enterprise owners | All orgs under the enterprise |

**Recommendation:** Apply secrets, crypto, and IaC state exclusions at the **organization** or **enterprise** level so that every repository is protected by default. Repository-level exclusions should add project-specific patterns.

### What Goes Wrong Without Exclusions

1. **Secret leakage in suggestions** — Copilot reproduces a database password from `.env` in a new file. The developer doesn't notice and commits it.
2. **Compliance violation** — Copilot ingests PII from a database fixture. The data is sent to GitHub's Copilot backend for processing, violating data residency requirements.
3. **Crypto key exposure** — A private key pattern appears in a Copilot suggestion. Even if not the exact key, it signals to attackers what key format the organization uses.
4. **State file leakage** — Terraform state containing every infrastructure secret is processed by Copilot, creating an unaudited copy of production credentials in a third-party system.

---

## 3. Network Routing

### Subscription-Based Hostnames

GitHub routes Copilot traffic through plan-specific hostnames:

| Plan | Hostname Pattern | Data Processing Agreement |
|------|-----------------|--------------------------|
| Copilot Business | `*.business.githubcopilot.com` | Business ToS — no training on your code |
| Copilot Enterprise | `*.enterprise.githubcopilot.com` | Enterprise ToS — no training, additional IP protections |
| Copilot Individual/Free | `*.individual.githubcopilot.com` | Individual ToS — code may be used for training |

### Why to Block Individual Plan on Corporate Networks

| Risk | Explanation |
|------|-------------|
| **Data governance** | Individual/Free plan users accepted terms that allow GitHub to use code snippets for model improvement. If a developer uses their personal Copilot account on corporate code, that code may be used for training — violating your enterprise agreement expectations. |
| **Shadow AI** | Developers may bypass organizational controls by using personal accounts. Blocking the individual hostname at the firewall ensures only managed Copilot plans can function on the corporate network. |
| **Audit gap** | Individual plan usage does not appear in your organization's audit log. You have no visibility into what code was processed or what suggestions were accepted. |
| **Compliance** | Regulated industries (finance, healthcare, government) require that all code processing tools operate under enterprise data processing agreements. Individual plan traffic falls outside this scope. |

### Firewall Configuration

```
# Allow (outbound HTTPS 443)
*.business.githubcopilot.com
*.enterprise.githubcopilot.com
github.com
api.github.com
copilot-proxy.githubusercontent.com

# Block
*.individual.githubcopilot.com
```

### Minimum Client Versions

Plan-specific routing requires minimum extension versions. Older clients route all traffic through a shared hostname, making plan-based blocking impossible:

| IDE | Minimum Version |
|-----|----------------|
| VS Code | Copilot Chat ≥ 0.17 |
| JetBrains | Copilot ≥ 1.5.6.5692 |
| Visual Studio | ≥ 2022 17.11 |

**Misconfiguration risk:** If you block `*.individual.githubcopilot.com` but developers use older extensions, their traffic routes through the shared hostname. They are effectively on the individual plan without firewall enforcement. Always enforce minimum client versions through MDM or developer onboarding.

---

## 4. Copilot Cloud Agent (Coding Agent) Security

The Copilot coding agent is an autonomous agent that can be assigned GitHub Issues. It creates branches, writes code, runs tests, and opens pull requests — all without direct human involvement during execution.

### 4.1 Why It's Disabled by Default

| Reason | Detail |
|--------|--------|
| **Autonomous code execution** | Unlike completions or chat, the coding agent writes and commits code independently. This requires a higher trust threshold. |
| **Supply chain risk** | Agent-generated code becomes part of your codebase. Without review gates, vulnerable or malicious code could be merged. |
| **Resource consumption** | The agent consumes compute resources (GitHub Actions minutes) and can create many branches and PRs if misconfigured. |
| **Compliance** | Regulated environments need documented approval workflows for code changes. Autonomous agents must be explicitly sanctioned. |

**Recommended value:** Keep disabled until your organization has branch protection rules, required reviewers, and CI/CD security scanning in place. Enable only for specific repositories where the workflow is well-defined.

### 4.2 Built-In Protections

When the coding agent is enabled, GitHub applies automatic security checks to every PR it creates:

| Protection | What It Does | Why It Matters |
|------------|-------------|----------------|
| **CodeQL analysis** | Static analysis runs on every agent-created PR. | Catches common vulnerability patterns (SQL injection, XSS, path traversal) before human review. |
| **Dependency scanning** | Checks any new dependencies the agent introduces. | Prevents the agent from adding packages with known CVEs or suspicious provenance. |
| **Secret scanning** | Scans agent-created commits for credentials and tokens. | The agent operates in an environment with access to Copilot-specific secrets; this prevents accidental inclusion in code. |
| **Code review** | Copilot code review automatically reviews the agent's PR. | Provides an AI-on-AI review layer — catches logical errors and style violations. |

### 4.3 Push Restrictions and Human Review

| Control | Configuration | Rationale |
|---------|--------------|-----------|
| **Agent cannot merge its own PRs** | Built-in restriction | Ensures a human always approves before agent code enters the main branch. This is the single most critical control. |
| **Required reviewers** | Branch protection rules | Set minimum reviewers ≥ 1 (recommend ≥ 2 for main/production branches) so agent PRs always require human sign-off. |
| **Status checks must pass** | Branch protection rules | CI/CD pipeline (tests, linting, SAST) must pass before the PR can be merged. |
| **Dismiss stale reviews** | Branch protection rules | If the agent pushes additional commits after initial review, previous approvals are invalidated. |

### 4.4 Branch Rulesets for Agent-Created PRs

Configure rulesets that specifically target branches created by the coding agent:

| Rule | Setting | Rationale |
|------|---------|-----------|
| **Branch name pattern** | `copilot/*` or `agent/*` | Agent-created branches follow a naming convention. Rulesets targeting this pattern apply controls only to agent work without affecting human branches. |
| **Require pull request** | Yes | Forces all agent work through the PR workflow; direct pushes to protected branches are blocked. |
| **Required approvals** | ≥ 1 | At least one human must review. For security-critical repos, require a CODEOWNERS approval. |
| **Require conversation resolution** | Yes | Review comments must be resolved before merge, ensuring agent-generated code issues are addressed. |
| **Restrict force pushes** | Blocked | Prevents the agent from rewriting history to hide problematic commits. |
| **Restrict deletions** | Blocked | Prevents the agent from deleting branches that might contain evidence of issues. |

### 4.5 Copilot-Specific Secrets and Variables

The coding agent has its own secrets and environment variable system, separate from repository Actions secrets:

| Concept | Detail |
|---------|--------|
| **Copilot secrets** | Configured at **Repository Settings → Copilot → Secrets**. Only the coding agent can read them — they are not exposed to GitHub Actions or other workflows. |
| **Why separate** | Limits blast radius. If a GitHub Actions workflow is compromised, Copilot secrets remain safe. If the coding agent is compromised, Actions secrets remain safe. |
| **What to store** | API keys for services the agent needs during development (e.g., test environment tokens, sandbox API keys). Never store production credentials. |
| **Rotation** | Rotate Copilot secrets on the same schedule as other credentials. The agent has no mechanism to rotate them itself. |

**Misconfiguration risk:** Storing production secrets as Copilot secrets gives the autonomous agent access to production systems. If the agent generates code that logs or exposes these values, they enter version control through the PR. Always use sandbox/test credentials only.

---

## 5. Extensions and MCP Servers

### Copilot Extensions

Extensions expand Copilot's capabilities by connecting it to external services (documentation providers, issue trackers, deployment tools). Each extension is a third-party integration.

| Risk | Detail |
|------|--------|
| **Data exfiltration** | Extensions receive conversation context, which may include code snippets and file contents. A malicious or compromised extension can exfiltrate this data. |
| **Prompt injection** | Extensions can inject content into the Copilot conversation, potentially manipulating the model's behavior to generate insecure code or reveal sensitive information. |
| **Supply chain** | Extensions are maintained by third parties. A legitimate extension can be compromised through a dependency attack or account takeover. |
| **Scope creep** | Extensions may request broad permissions (repository read, issue write) that exceed their stated purpose. |

### Enterprise Governance for Extensions

| Control | How to Implement |
|---------|-----------------|
| **Allowlist only** | Restrict extension installation to an admin-approved list. Disable the marketplace for unapproved extensions. |
| **Review permissions** | Audit each extension's permission scope before approval. Reject extensions that request write access unless justified. |
| **Vendor assessment** | Treat extension vendors like any other third-party SaaS provider: security questionnaire, SOC 2 review, DPA. |
| **Periodic review** | Re-evaluate approved extensions quarterly. Remove any that are no longer actively maintained. |

### MCP (Model Context Protocol) Servers

MCP servers provide Copilot with additional context by serving structured data from external sources.

| Risk | Mitigation |
|------|------------|
| **Arbitrary data injection** | MCP servers can feed any content to the model. Validate that servers only serve intended data. |
| **Network exposure** | MCP servers typically run locally or on internal networks. Ensure they are not exposed to the public internet. |
| **Authentication** | MCP servers should require authentication. An unauthenticated server on the local network can be exploited by any process. |

---

## 6. Seat Management

Configured at **Organization Settings → Copilot → Access**.

### `selected_teams` vs `all_members`

| Setting | Behavior |
|---------|----------|
| `all_members` | Every member of the organization automatically gets a Copilot seat. |
| `selected_teams` | Only members of explicitly listed teams get seats. |

### Why to Use `selected_teams`

| Reason | Explanation |
|--------|-------------|
| **Least privilege** | Not every org member needs Copilot. Contractors, managers, and non-engineering staff don't benefit from code completions but would still have Copilot ingesting context from any repo they access. |
| **Cost control** | Copilot Business is billed per seat. `all_members` includes everyone — including inactive accounts, bots, and non-developers. |
| **Audit clarity** | With `selected_teams`, you know exactly who has Copilot access. Audit questions about "who can use AI on our code" have a clear answer: check the team membership list. |
| **Onboarding control** | New hires must be added to the appropriate team before getting Copilot. This creates an intentional gate where security training can be verified first. |
| **Offboarding** | Removing someone from the team immediately revokes Copilot. With `all_members`, the seat persists until org membership is removed. |

### Additional Seat Settings

| Setting | Recommended Value | Rationale |
|---------|------------------|-----------|
| `auto_assign_new_members` | `false` | Prevents new org members from automatically receiving Copilot. Ensures the onboarding gate is respected. |
| Allowed teams | Explicitly listed | Example: `engineering`, `devops`, `security`. Never use an "all-employees" group. |

**Misconfiguration risk:** Using `all_members` with `auto_assign_new_members: true` means a newly added bot account, contractor, or acquired-company employee immediately gets Copilot on their first login. They may not have completed security training, signed the AI-acceptable-use policy, or had their access scope reviewed.

---

## 7. Custom Instructions (`.github/copilot-instructions.md`)

### What It Does

A `.github/copilot-instructions.md` file at the root of a repository provides persistent instructions that Copilot includes in every interaction within that repository. These instructions shape the model's behavior — what patterns to follow, what to avoid, and what standards to enforce.

### Security-Focused Instruction Patterns

| Pattern | Example Instruction | Why It Matters |
|---------|-------------------|----------------|
| **No hardcoded secrets** | "Never generate code containing hardcoded secrets, API keys, passwords, or tokens." | Prevents the most common AI-assisted security mistake. |
| **Parameterized queries** | "Use parameterized queries for all database operations. Never use string concatenation for SQL." | Eliminates SQL injection from AI-generated code. |
| **Input validation** | "Validate and sanitize all user inputs before processing." | Establishes a baseline expectation that Copilot will include validation. |
| **Least privilege** | "Apply least privilege for IAM roles, file permissions, and access grants." | Prevents Copilot from generating `*:*` IAM policies or `chmod 777`. |
| **No root containers** | "Never generate Dockerfiles that run as root." | Enforces container security best practices. |
| **Secrets manager usage** | "Always use environment variables or a secrets manager for sensitive configuration." | Directs Copilot to the correct pattern instead of inline values. |
| **TLS enforcement** | "Use HTTPS for all network requests. Never disable TLS verification." | Prevents `verify=False` and `rejectUnauthorized: false` patterns. |
| **Error handling** | "Write error handling that does not expose internal details." | Prevents stack traces and internal paths in error responses. |

### Limitations

| Limitation | Impact |
|------------|--------|
| Copilot reads the first ~4,000 characters of the instruction file for code review, and ~1,000 lines for completions. | Keep instructions concise and prioritized — put the most important security rules first. |
| Instructions are advisory, not enforced. | Copilot may still generate code that violates instructions, especially for complex scenarios. Instructions reduce the probability but do not eliminate the risk. Always review AI-generated code. |
| Does not apply to Copilot Chat web interface. | Instructions only take effect in IDEs and code review, not when using Copilot on github.com chat. |

**Misconfiguration risk:** An overly long instruction file gets truncated, and the security rules at the bottom are never seen by Copilot. Always put security instructions in the first 2,000 characters.

---

## 8. Audit Logging

### Key Events to Monitor

GitHub's audit log captures Copilot-related events at the organization level.

| Event | What It Means | Why to Monitor |
|-------|--------------|----------------|
| `copilot.cfb_seat_assignment_created` | A Copilot seat was assigned to a user. | Detect unauthorized seat provisioning. |
| `copilot.cfb_seat_assignment_removed` | A Copilot seat was revoked. | Confirm offboarding completeness. |
| `copilot.content_exclusion_changed` | Content exclusion rules were modified. | Critical — someone may be weakening exclusion rules to expose sensitive files. |
| `copilot.policy_changed` | A feature policy was changed (e.g., web search enabled). | Detect policy drift. Changes to web search or seat management should trigger an alert. |
| `copilot.cfb_seat_cancellation_requested` | An admin canceled a seat. | Track seat lifecycle. |
| `copilot.org_settings_changed` | Organization-level Copilot settings were modified. | Catch any configuration change that weakens security posture. |

### Audit Query Example

```bash
gh api \
  -H "Accept: application/vnd.github+json" \
  "/orgs/ORGNAME/audit-log?phrase=action:copilot" \
  --paginate
```

### What to Alert On

| Condition | Severity | Response |
|-----------|----------|----------|
| `content_exclusion_changed` outside change window | High | Investigate immediately. May indicate an insider weakening controls. |
| `policy_changed` enabling `web_search` or `bing_search` | High | Revert and investigate. Data leakage risk. |
| Seat assigned to a service account or bot | Medium | Verify whether the bot should have Copilot access. |
| Bulk seat assignments (> 50 in one hour) | Medium | May indicate an automation error or unauthorized provisioning script. |
| `org_settings_changed` by a non-admin user | Critical | Indicates privilege escalation. Investigate immediately. |

---

## 9. Proxy and SSL Configuration

### Why Corporate Proxies Matter

Organizations using web proxies or TLS inspection need specific Copilot configuration. Without it, Copilot fails silently — no suggestions appear, and developers assume the feature is broken.

### VS Code Proxy Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| `http.proxy` | `https://proxy.corp.example.com:8443` | Routes Copilot traffic through the corporate proxy for inspection and logging. |
| `http.proxyStrictSSL` | `true` | **Never set to `false`**. Disabling strict SSL allows MITM attacks between the IDE and the proxy. |
| `github.copilot.advanced.debug.overrideProxyUrl` | `https://proxy.corp.example.com:8443` | Some Copilot requests bypass the IDE's proxy settings. This override ensures all Copilot traffic goes through the proxy. |

### Custom CA Certificates

If your proxy performs TLS inspection (MITM for DLP/security monitoring):

```bash
# Required environment variable for VS Code / Cursor
export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca-bundle.crt
```

| Platform | Configuration |
|----------|--------------|
| VS Code / Cursor | `NODE_EXTRA_CA_CERTS` environment variable |
| JetBrains | **Settings → Tools → Server Certificates → Add** |
| Visual Studio | Windows certificate store (auto-detected) |
| Neovim | `NODE_EXTRA_CA_CERTS` or system CA bundle |

### What Goes Wrong

| Misconfiguration | Symptom | Impact |
|-----------------|---------|--------|
| No proxy configured | Copilot requests time out | Developers get no suggestions and blame the tool |
| `proxyStrictSSL: false` | Copilot works but TLS is not verified | MITM attack possible between IDE and proxy |
| Missing CA certificate | `UNABLE_TO_VERIFY_LEAF_SIGNATURE` errors | Copilot non-functional; developers may disable strict SSL as a "fix" |
| Proxy blocks WebSocket | Chat works but completions fail (or vice versa) | Partial functionality causes confusion |

---

## 10. VS Code Settings for Copilot

### Recommended Secure Configuration

```json
{
  "github.copilot.enable": {
    "*": true,
    "plaintext": false,
    "ini": false,
    "properties": false,
    "markdown": true,
    "yaml": true,
    "json": true
  },
  "github.copilot.chat.followUps": "firstOnly",
  "http.proxyStrictSSL": true
}
```

### Setting-by-Setting Rationale

| Setting | Value | Rationale |
|---------|-------|-----------|
| `github.copilot.enable.*` | `true` | Enable completions by default for code files. |
| `github.copilot.chat.followUps` | `"firstOnly"` | Limits auto-generated follow-up suggestions in chat. Reduces the chance of developers blindly following AI-suggested next steps that may be inappropriate. |
| `http.proxyStrictSSL` | `true` | Enforces TLS certificate verification. Never disable. |

---

## 11. `copilot.enable` Per Language

### Why Disable for `plaintext`, `ini`, and `properties`

| Language ID | Why Disable |
|-------------|-------------|
| `plaintext` | Plaintext files frequently contain configuration notes, credentials, internal URLs, IP addresses, and ad-hoc documentation that was never meant for code completion. Copilot processing these files risks ingesting and reproducing sensitive operational data. |
| `ini` | INI files (`.ini`, `.cfg`) are configuration files that commonly contain database connection strings, SMTP passwords, API endpoints, and other sensitive settings. Example: `db_password=hunter2` in a `config.ini` file. |
| `properties` | Java `.properties` files contain application configuration that often includes credentials, JDBC URLs with embedded passwords, and internal service endpoints. |

### Language Enablement Strategy

| Category | Languages | Recommended |
|----------|-----------|-------------|
| **Always enable** | `javascript`, `typescript`, `python`, `go`, `rust`, `java`, `csharp`, `cpp` | These are the primary development languages where Copilot adds the most value. |
| **Enable with caution** | `yaml`, `json`, `dockerfile`, `terraform` | Useful for IaC and config-as-code, but ensure content exclusion rules cover sensitive variants (`.tfvars`, `docker-compose` with secrets). |
| **Disable** | `plaintext`, `ini`, `properties` | Too high a risk of containing credentials and sensitive configuration. |
| **Evaluate per-org** | `markdown`, `sql` | Markdown is generally safe. SQL completions are useful but may reference production schema/data — assess per repository. |

**Misconfiguration risk:** Enabling Copilot for `plaintext` means every `.txt` file in the workspace becomes context for suggestions. If a developer has a `passwords.txt` or `internal-endpoints.txt` open, that content feeds into Copilot's context window.

---

## 12. Summary — Quick Reference

| Setting | Secure Default | Key Risk if Wrong |
|---------|---------------|-------------------|
| Web/Bing search | Disabled | Code snippets sent to external search APIs |
| Code review | Enabled | Lose a free security review layer |
| Content exclusion | Configured for secrets, crypto, IaC | Secrets appear in completions |
| Individual plan blocking | Block at firewall | Shadow AI on personal accounts processes corp code |
| Coding agent | Disabled until controls in place | Autonomous code changes without review gates |
| Extensions | Allowlist only | Third-party data exfiltration |
| Seat management | `selected_teams` | Uncontrolled access, wasted spend |
| Custom instructions | Security rules first | Truncation hides important rules |
| Audit logging | Alert on policy/exclusion changes | Undetected weakening of controls |
| Proxy SSL | `proxyStrictSSL: true` | MITM between IDE and proxy |
| Plaintext/INI completion | Disabled | Config files with secrets ingested |

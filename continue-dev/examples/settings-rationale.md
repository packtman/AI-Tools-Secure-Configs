# Continue.dev — Enterprise Security Settings Rationale

Every setting below explains **what it controls**, **why it matters**, the **recommended value**, and the **risk of misconfiguration**. An admin reading this should understand the reasoning behind each recommendation, not just the value to set.

---

## 1. Tool Permission Levels

Continue.dev's agent mode grants tools (filesystem read/write, terminal execution, web search) with configurable permission levels.

| Permission level | Behavior | When to use |
|-----------------|----------|-------------|
| `allow` | Tool executes without user confirmation | **Read-only tools only**: reading files, viewing diffs, listing directory trees. These cannot modify state. |
| `ask` | User must confirm each tool invocation | **Default for write operations**: file edits, terminal commands, git operations. Human-in-the-loop for all state changes. |
| `exclude` | Tool is completely unavailable to the agent | **Dangerous tools**: tools that access external services, sensitive directories, or perform destructive operations. |

### Why Read-Only Tools Default to `allow`

| Reason | Explanation |
|--------|------------|
| Workflow efficiency | Requiring confirmation for every file read makes the agent unusable. Developers would spend more time approving reads than writing code. |
| Low risk profile | Reading a file cannot modify state. The worst case is information disclosure, which is mitigated by workspace-scoped context providers. |
| Context quality | The agent produces better results when it can freely read relevant files to understand the codebase. Restricting reads degrades output quality. |
| Write tools remain gated | The security-critical boundary is write operations. Keeping reads open while gating writes is the optimal balance. |

### Recommended Permission Matrix

| Tool category | Permission | Rationale |
|--------------|-----------|-----------|
| File read | `allow` | Non-destructive. Agent needs free read access for context. |
| Directory listing | `allow` | Non-destructive. Required for code navigation. |
| Diff viewing | `allow` | Non-destructive. Required for understanding changes. |
| File write/edit | `ask` | State-changing. User must review all modifications. |
| Terminal commands | `ask` | Can execute arbitrary code. User must approve every command. |
| Git operations | `ask` | Repository-modifying. Push/commit require explicit approval. |
| Web search | `ask` | Sends queries to external services. May leak project context. |
| Browser/fetch | `exclude` | Network access to arbitrary URLs. Risk of data exfiltration. |

### Misconfiguration Risk

Setting write tools to `allow` means the agent can modify files without review — a prompt injection can silently introduce backdoors. Setting read tools to `exclude` makes the agent nearly useless (no code context). Setting all tools to `ask` creates confirmation fatigue, leading users to approve blindly.

---

## 2. Operational Modes

| Mode | What it does | When to use |
|------|-------------|-------------|
| **Default** (no flag) | Agent can read and write files, run terminal commands, with permission checks per tool configuration | Standard development. Most flexible, with governance via tool permissions. |
| `--readonly` | Agent can only read files and provide suggestions. Cannot modify any files or run commands. | Code review, learning, exploration. When you want AI assistance without any risk of modification. |
| `--auto` | Agent executes approved actions without confirmation. Overrides `ask` permissions to `allow`. | CI/CD pipelines, automated refactoring (with strict workspace sandboxing). **Never use interactively.** |

### When to Use Each Mode

| Scenario | Recommended mode | Why |
|----------|-----------------|-----|
| Daily development | Default | Balanced productivity and safety. User confirms writes. |
| Security code review | `--readonly` | Reviewer should not accidentally modify the code under review. |
| Onboarding/exploration | `--readonly` | New team members can explore safely without risk of breaking things. |
| Automated refactoring pipeline | `--auto` | CI/CD needs unattended operation. Sandbox the workspace and review changes via PR. |
| Pair programming | Default | Both human and AI contribute. Human confirms AI suggestions. |

### Misconfiguration Risk

Using `--auto` in an interactive IDE session removes all confirmation gates. A prompt injection can modify any file, run any command, and push to git without user awareness. Using `--readonly` for development tasks forces developers to manually apply every suggestion, defeating the purpose of AI assistance.

---

## 3. Secrets Management — User vs Org Secrets

| Secret type | Who creates it | How it's used | Available on |
|------------|---------------|---------------|-------------|
| **User Secrets** | Individual users | Sent to IDE extension. Extension makes direct API calls using the key. | Solo, Teams, Enterprise |
| **Org Secrets** | Organization admins | Never sent to IDE. LLM requests proxied through Continue's server. Key stays server-side. | Teams, Enterprise only |

### Why Org Secrets Are Safer

| Aspect | User Secrets | Org Secrets |
|--------|-------------|-------------|
| Key exposure | Key is present in IDE extension memory and local config. Visible in process dumps, extension logs, or memory inspection. | Key never leaves Continue's server. IDE has no access to the actual key value. |
| Revocation | Each user must update their local config when key rotates. Users who miss the update break their setup. | Admin rotates once. All users seamlessly use the new key via proxy. |
| Auditability | API calls originate from individual user IPs with the shared key. Provider logs show a single key from many IPs. | API calls originate from Continue's proxy. Provider logs show consistent origin. Continue logs show individual user attribution. |
| Deprovisioning | User retains the key after leaving the organization unless the key is rotated. | Deprovisioned user loses proxy access immediately. Key rotation is not required. |
| Cost control | Each user has direct API access. No centralized rate limiting. | Proxy can enforce per-user rate limits, cost quotas, and usage policies. |

### Misconfiguration Risk

Using User Secrets for shared API keys means every developer has the raw API key in their local environment. A single compromised workstation exposes the key. Key rotation requires coordinating with every user individually. Org Secrets eliminate these risks by keeping the key server-side and proxying requests.

---

## 4. Mustache Notation for Secrets

| Aspect | Detail |
|--------|--------|
| **What it does** | The `${{ secrets.SECRET_NAME }}` syntax references secrets by name without embedding the value in configuration files. |
| **Recommended** | **Always use mustache notation.** Never inline API keys. |

### Why Never to Inline API Keys

| Risk of inline keys | Mitigation via mustache notation |
|--------------------|--------------------------------|
| Keys committed to version control | Config files with `${{ secrets.KEY }}` are safe to commit. The placeholder contains no sensitive data. |
| Keys visible in plain text | Secrets are resolved at runtime, not stored in config files. |
| Keys shared via config file copying | Sharing `.continuerc.json` between teams does not expose keys. Each environment resolves secrets independently. |
| Keys in IDE settings sync | If IDE settings sync is enabled, inline keys are uploaded to the sync service. Mustache notation syncs only the placeholder. |
| Key rotation requires file edits | Rotate the secret value once; all configs referencing it automatically use the new value. |

### Example

```yaml
# DANGEROUS — key is embedded in the file
apiKey: "sk-abc123..."

# SAFE — key is resolved at runtime from secrets store
apiKey: "${{ secrets.OPENAI_API_KEY }}"
```

### Misconfiguration Risk

Inlining API keys in `config.yaml` means the key is written to disk in plain text. If the file is committed to git (even accidentally, even in a private repo), the key is in version history permanently. If the workstation is compromised, the key is immediately available. Mustache notation eliminates these risks.

---

## 5. MCP Server Configuration

| Aspect | Detail |
|--------|--------|
| **What it does** | Continue.dev supports Model Context Protocol servers as tools, extending the agent's capabilities with external integrations. |
| **Recommended** | Audit and scope all MCP servers. Use only approved servers. |

### Scoping and Auditing

| Control | Implementation | Why |
|---------|---------------|-----|
| Server allowlist | Only permit specific, IT-approved MCP server packages | Prevents users from adding arbitrary MCP servers that may exfiltrate data. |
| Filesystem scoping | Limit filesystem MCP servers to project directories only | Prevents access to `~/.ssh`, `~/.aws`, and other sensitive locations. |
| Package pinning | Use exact versions, not `latest` | Prevents supply chain attacks via compromised upstream packages. |
| Network auditing | Monitor MCP server network connections | Detect unexpected outbound connections to unauthorized endpoints. |
| Configuration review | Review MCP configs in code review / CI | Catch malicious or overly permissive MCP configurations before they're used. |

### Risk Categories

| MCP server type | Risk level | Recommended approach |
|----------------|-----------|---------------------|
| Filesystem (scoped to `./src`) | Low | Allow with scope restriction |
| Filesystem (scoped to `/` or `~`) | **Critical** | Block. Never allow root or home directory access. |
| Database query | Medium | Allow with read-only connection strings. Audit all queries. |
| HTTP/API client | High | Allow only to approved internal APIs. Block external URLs. |
| Shell execution | **Critical** | Block or require-confirmation for every invocation. |

### Misconfiguration Risk

An unscoped filesystem MCP server gives the agent access to the entire filesystem. A shell-execution MCP server gives the agent arbitrary command execution. A database MCP server with write access allows the agent to modify production data. Each unaudited MCP server is an additional attack surface.

---

## 6. `config.yaml` vs `.continuerc.json` — Configuration Scoping

| File | Scope | Location | Who manages it |
|------|-------|----------|---------------|
| `config.yaml` | User-global | `~/.continue/config.yaml` | Individual developer |
| `.continuerc.json` | Workspace/project | Project root | Team lead or repo owner |

### When to Use Each Scope

| Scenario | Which file | Why |
|----------|-----------|-----|
| Personal model preferences | `config.yaml` | User-specific settings (preferred model, temperature) should not affect the team. |
| Corporate proxy settings | `config.yaml` | Network configuration is per-workstation, not per-project. |
| Project-specific model endpoint | `.continuerc.json` | Different projects may require different models (e.g., project with PII uses private endpoint). |
| Team-wide security prompts | `.continuerc.json` | Custom commands like `security-review` should be consistent across the team. |
| Context providers | `.continuerc.json` | Which context sources are available depends on the project structure. |
| Telemetry settings | `config.yaml` | Telemetry is an organizational decision, not project-specific. |

### Merge Behavior

`.continuerc.json` overrides `config.yaml` for settings present in both files. This means:

- Team leads can enforce project-specific settings even if individual users have different global preferences.
- A project requiring a private model endpoint can override a user's global SaaS endpoint.
- Security-critical settings in `.continuerc.json` take precedence.

### Misconfiguration Risk

Putting API keys in `.continuerc.json` (a file committed to the repo) exposes them in version control. Putting project-specific model endpoints in `config.yaml` means they don't travel with the repo and new team members get misconfigured. Conflicting settings between the two files create unpredictable behavior.

---

## 7. Proxy Settings

| Setting | What it controls | Recommended value | Why |
|---------|-----------------|-------------------|-----|
| `requestOptions.proxy` | HTTP/HTTPS proxy for all LLM API calls | Corporate proxy URL | Routes all AI traffic through the corporate proxy for DLP inspection, logging, and policy enforcement. |
| `requestOptions.verifySsl` | Whether TLS certificates are validated | `true` | Prevents MITM attacks. If your proxy uses a self-signed CA, add the CA to the system trust store instead of disabling verification. |

### Corporate Network Requirements

| Requirement | How proxy settings address it |
|-------------|------------------------------|
| DLP inspection | Proxy can scan LLM requests for PII, credentials, and classified data before they leave the network. |
| URL filtering | Proxy can restrict which LLM endpoints are reachable (block unauthorized APIs). |
| Network logging | All LLM traffic appears in proxy logs, providing a network-level audit trail. |
| Bandwidth management | Proxy can rate-limit LLM traffic to prevent bandwidth saturation. |
| Compliance | Some regulations require all external API traffic to traverse an inspectable path. |

### Misconfiguration Risk

Setting `verifySsl: false` disables TLS certificate validation for all LLM API calls. Any network intermediary can intercept, read, and modify traffic — including source code in prompts and generated code in responses. This is especially dangerous on public Wi-Fi or shared networks. Not configuring a proxy at all means LLM traffic bypasses corporate security controls entirely.

---

## 8. Telemetry (`allowAnonymousTelemetry`)

| Aspect | Detail |
|--------|--------|
| **What it does** | Controls whether Continue.dev collects anonymous usage data (feature usage, error rates, performance metrics). |
| **Recommended** | `false` for enterprise deployments. |

### Why Disable for Enterprise

| Reason | Explanation |
|--------|------------|
| Data classification | Even "anonymous" telemetry may include file paths, error messages with stack traces, or model names that reveal organizational technology choices. |
| Network policy | Telemetry requires outbound connections to Continue.dev servers. Enterprise networks may not permit this, and the connections create noise in security monitoring. |
| Compliance | Data minimization principles (GDPR Article 5(1)(c)) favor collecting only what is strictly necessary. Telemetry data is not necessary for the tool to function. |
| Vendor risk | Telemetry data stored by Continue.dev becomes part of their data breach surface. Disabling eliminates this third-party risk. |
| Predictability | With telemetry off, no data leaves the workstation except explicit LLM API calls through configured endpoints. Network behavior is fully predictable. |

### Misconfiguration Risk

If telemetry is enabled in an environment where outbound connections are monitored, telemetry traffic triggers security alerts and investigation overhead. If telemetry is enabled in a classified environment, it constitutes a data spillage incident regardless of the telemetry content.

---

## 9. Custom Commands (`security-review` Prompt)

| Aspect | Detail |
|--------|--------|
| **What it does** | Custom slash commands that execute predefined prompts. The `security-review` command sends code to the model with a security-focused system prompt. |
| **Recommended** | Create team-standard security commands and distribute via `.continuerc.json`. |

### How to Add Security Tooling

| Command | Purpose | Prompt strategy |
|---------|---------|----------------|
| `/security-review` | Comprehensive vulnerability scan | Check for OWASP Top 10, hardcoded secrets, insecure crypto, auth flaws. Request severity ratings and remediation. |
| `/threat-model` | Identify attack surface | Analyze code for trust boundaries, data flows, and threat vectors. Output STRIDE-based analysis. |
| `/dependency-audit` | Review dependency security | Check for known vulnerabilities, outdated packages, excessive permissions. |
| `/secrets-scan` | Find hardcoded secrets | Scan for API keys, passwords, tokens, connection strings. Flag patterns with high entropy. |

### Example Configuration

```json
{
  "customCommands": [
    {
      "name": "security-review",
      "description": "Review code for security vulnerabilities",
      "prompt": "Review this code for security vulnerabilities. Check for: SQL injection, XSS, CSRF, insecure deserialization, hard-coded secrets, insecure cryptography, path traversal, and authentication/authorization flaws. List each finding with severity (Critical/High/Medium/Low) and remediation."
    }
  ]
}
```

### Why Custom Commands Matter for Security

Custom commands standardize security practices across the team. Without them, each developer writes ad-hoc security prompts of varying quality. With them, every security review uses the same comprehensive checklist, producing consistent and auditable results.

### Misconfiguration Risk

Overly generic prompts produce shallow reviews. Missing custom commands means developers either skip security review or write inconsistent prompts. Commands that include sensitive context (e.g., "our auth uses JWT with secret X") leak secrets into the prompt.

---

## 10. `.env` File Security

| Aspect | Detail |
|--------|--------|
| **What it does** | `.env` files store API keys and configuration values that Continue.dev resolves at runtime. |
| **Recommended** | Always gitignore. Understand resolution order. Never commit. |

### Why to Gitignore

| Risk if committed | Consequence |
|------------------|------------|
| Key exposure | API keys in `.env` are visible to anyone with repo access. In public repos, they're visible to the world. |
| Version history | Even if removed from HEAD, keys persist in git history forever unless the repo is rebased/force-pushed. |
| Fork propagation | Forks inherit the key. Revoking access to the original repo does not revoke access to forks. |
| CI/CD exposure | `.env` files checked into the repo are available in every CI/CD run, expanding the attack surface. |

### Resolution Order

| Priority | Source | Scope |
|----------|--------|-------|
| 1 (highest) | Workspace `.env` (`.continue/.env` in project root) | Project-specific |
| 2 | Global `.env` (`~/.continue/.env`) | User-global |
| 3 | Org Secrets (via Continue Hub) | Organization-wide |
| 4 (lowest) | User Secrets (via Continue settings) | User-specific |

Higher-priority sources override lower-priority ones for the same variable name. This means a workspace `.env` can override an Org Secret — which may be a security concern if developers can set workspace-level overrides for organization-managed keys.

### Required `.gitignore` Entries

```
.continue/.env
.continue/sessions/
.continue/index/
```

### Misconfiguration Risk

Not gitignoring `.continue/.env` risks committing API keys. Not understanding resolution order means a workspace `.env` may silently override an Org Secret, routing traffic through an unintended endpoint. Storing secrets in global `.env` on a shared workstation exposes them to all users of that machine.

---

## 11. Hub-Based Configuration

| Aspect | Detail |
|--------|--------|
| **What it does** | Continue Hub allows organization admins to define and distribute configuration centrally, ensuring all team members use approved settings. |
| **Recommended** | Use Hub for team-wide settings. Reserve local config for personal preferences only. |

### Team Consistency Benefits

| Benefit | How Hub provides it |
|---------|-------------------|
| Uniform model endpoints | All developers use the same approved LLM endpoints. No one accidentally uses an unapproved SaaS model. |
| Consistent security prompts | Custom commands (security-review, threat-model) are identical across the team. |
| Centralized secret management | Org Secrets managed in Hub. No individual key management. |
| Onboarding speed | New developers get the correct configuration automatically. No manual setup. |
| Policy enforcement | Hub settings override local settings, preventing individual users from bypassing organizational policies. |
| Audit trail | Configuration changes in Hub are tracked. Local config changes are not. |

### Hub vs Local Configuration

| Setting type | Where to manage | Why |
|-------------|----------------|-----|
| Model endpoints | Hub | Organizational decision — must be consistent and approved. |
| API keys | Hub (Org Secrets) | Security-critical — must be centrally managed. |
| Custom commands | Hub | Quality assurance — security prompts must be consistent. |
| Telemetry | Hub | Compliance decision — must be uniform. |
| Personal model preferences | Local `config.yaml` | Individual preference — no security impact. |
| Editor-specific settings | Local `config.yaml` | Per-workstation configuration. |

### Misconfiguration Risk

Without Hub, each developer manages their own configuration. This leads to configuration drift (different developers using different models), secret sprawl (each developer manages their own API keys), and inconsistent security practices (different security-review prompts producing different coverage).

---

## 12. Model Selection and API Base Override

| Setting | What it controls | Recommended configuration | Why |
|---------|-----------------|--------------------------|-----|
| `model` | Which LLM model to use | Approved models only (via Hub) | Different models have different data handling policies and costs. |
| `apiBase` | The API endpoint URL | Corporate gateway URL | Routes all LLM traffic through a corporate gateway that enforces rate limits, DLP, logging, and access control. |
| `provider` | The LLM provider (openai, anthropic, etc.) | As required by your gateway | The gateway may present a unified API regardless of the backend model. |

### Why Route Through Corporate Gateways

| Benefit | Explanation |
|---------|------------|
| Centralized logging | All LLM requests and responses are logged at the gateway. Provides a single audit trail regardless of which developer or project initiated the call. |
| DLP enforcement | Gateway can scan prompts for PII, credentials, and classified data before forwarding to the LLM provider. |
| Rate limiting | Gateway enforces per-user and per-team rate limits, preventing cost overruns and ensuring fair usage. |
| Model governance | Gateway controls which models are accessible. Adding or removing models is a server-side change, not a client-side configuration update. |
| Cost tracking | Gateway attributes costs to teams, projects, or cost centers. Direct API calls lack this attribution. |
| Failover | Gateway can route to backup models if the primary is unavailable, without client-side changes. |

### Misconfiguration Risk

If `apiBase` points directly to `api.openai.com` instead of the corporate gateway, all traffic bypasses DLP, logging, rate limiting, and cost tracking. If the model is not on the approved list, developers may use models with data handling policies that violate organizational requirements.

---

## 13. Context Providers — Safety Assessment

Context providers give the agent access to different types of project information. Each has different data implications.

### Safe Context Providers (Low Risk)

| Provider | What it provides | Why it's safe |
|----------|-----------------|--------------|
| `code` | Current file content | Already visible in the editor. No additional exposure. |
| `diff` | Current git diff | Shows only uncommitted changes. Scoped to the workspace. |
| `tree` | Directory structure | File names and paths only. No file content. |
| `highlights` | Syntax-highlighted code regions | Subset of `code`. No additional exposure. |
| `open` | Currently open files | Files the developer has explicitly opened. No additional exposure. |

### Context Providers with Data Implications (Evaluate Carefully)

| Provider | What it provides | Data implication | Recommended action |
|----------|-----------------|-----------------|-------------------|
| `codebase` | Full codebase search via embeddings index | Indexes the entire repository. Embeddings are sent to the configured embeddings provider. | Use only with private embeddings endpoint. Understand what is indexed. |
| `docs` | External documentation | Fetches documentation from URLs. URLs may be logged. | Restrict to approved documentation sources. |
| `web` | Web search results | Sends search queries to external search APIs. Queries may contain project context. | Disable unless needed. Queries may leak project details. |
| `database` | Database query results | Connects to databases and returns query results. May expose production data. | Use only with read-only credentials to non-production databases. |
| `terminal` | Terminal output | Includes command output which may contain secrets, tokens, or sensitive data from previous commands. | Evaluate whether terminal history contains sensitive data. |
| `repo-map` | Repository structure analysis | Sends repository structure to the model. Reveals architecture and technology choices. | Acceptable for most use cases. Review if repo structure is classified. |

### Misconfiguration Risk

Enabling `codebase` with a public embeddings provider (e.g., OpenAI API directly) sends your entire codebase as embeddings to an external service. Enabling `database` with production credentials exposes production data to the LLM. Enabling `web` allows the agent to send search queries that may include code snippets or project names to external search engines. Enabling `terminal` may send previous command output containing secrets or tokens to the model.

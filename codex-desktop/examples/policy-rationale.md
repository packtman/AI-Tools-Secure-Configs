# Codex Desktop App — Policy Rationale

Every setting below explains **what it does**, **why you should care**, and **the recommended value** for different environments.

---

## `sandbox_mode`

**What it does:** Controls what filesystem and network access the Codex agent has during execution.

**Why it matters:** The sandbox is the primary isolation boundary. A misconfigured sandbox can allow the AI agent to read sensitive files, modify system configurations, or exfiltrate data over the network.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated (finance, healthcare) | `read-only` | Agent can only read files — no writes, no network. Eliminates data modification risk. |
| Standard enterprise | `workspace-write` | Allows writing within the project directory only. No network. Balances productivity with safety. |
| Individual developers | `workspace-write` | Same as above. Never use `danger-full-access` unless in a disposable container. |

---

## `approval_policy`

**What it does:** Controls when the agent pauses to ask for human confirmation before executing actions.

**Why it matters:** Without approval prompts, the agent can execute arbitrary commands autonomously. This is the human-in-the-loop control.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `on-request` | Every write/execute requires explicit approval. |
| Standard enterprise | `on-request` | Default for most teams. Reads are automatic; writes need approval. |
| Power users (trusted) | `never` | Only with `workspace-write` sandbox. Accept the risk of autonomous execution within the sandbox. |

---

## `web_search`

**What it does:** Controls whether and how Codex can search the web during tasks.

**Why it matters:** Web content is untrusted input. Live web search exposes the agent to prompt injection attacks from malicious web pages. Cached search uses pre-indexed results, reducing (but not eliminating) this risk.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `disabled` | No external data retrieval. Eliminates web-based injection vector entirely. |
| Standard enterprise | `cached` | Pre-indexed results only. Reduced injection risk. |
| Individual developers | `cached` or `live` | Accept the risk for access to current information. |

---

## `browser_use`

**What it does:** Enables the Browser Use feature, allowing Codex to browse websites and interact with web pages.

**Why it matters:** Browser Use gives the AI agent access to arbitrary web content, creating a large prompt injection surface. Malicious pages can manipulate agent behavior.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | Eliminates browser-based attack surface. |
| Standard enterprise | `false` | Unless specific browser workflows are approved and allowlisted. |
| Individual developers | `true` | With allowlist/blocklist configuration to limit accessible sites. |

---

## `browser_use_full_cdp_access` (Codex 0.150+)

**What it does:** Enables full Chrome DevTools Protocol (CDP) access in the local runtime, including Browser Developer mode. When pinned `false` in `requirements.toml`, the ChatGPT desktop app cannot turn the matching setting on.

**Why it matters:** CDP is a debugger channel. The agent can inspect cookies, local storage, and page internals, not just click visible UI. Omitting the key leaves CDP unconstrained even when `browser_use = false`.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All tiers | `false` in requirements | Teams can still use in-app Browser Use on Baseline without debugger access. |

**What breaks:** Browser Developer mode and the ChatGPT desktop CDP toggle fail closed. Developers describe the page or use the in-app pane without CDP.

## `browser_use_external` (Codex 0.150+)

**What it does:** Allows Computer Use in an external browser (Chrome, Edge, Safari) instead of the in-app pane.

**Why it matters:** External browsers carry the user's full cookie jar, password manager, and logged-in SaaS sessions. The in-app pane is a smaller session.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All tiers | `false` in requirements | Baseline can keep `browser_use = true` for the in-app pane. |

**What breaks:** Computer Use outside the in-app pane fails. File an exception if a workflow must drive the user's real browser, then pair it with `allow_locked_computer_use = false`.

## `computer_use.allow_locked_computer_use` (Codex 0.150+)

**What it does:** Requirements-only. When `false`, Computer Use stops after a managed macOS device locks. This key does not enable Computer Use.

**Why it matters:** If you omit it, requirements do not constrain locked use. A later exception that turns `computer_use` on would then keep clicking after lock screen.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All tiers | `false` | Defense in depth even while Computer Use stays pinned off. |

**What breaks:** Unattended Computer Use after lock screen fails. The user unlocks the Mac to continue.

## `developer_instructions`

**What it does:** Extra text injected into every Codex session. Soft control (prompt), not a sandbox. Valid in `config.toml` and `managed_config.toml` only. Do not put it in `requirements.toml`.

**Why it matters:** Without it, the model has no org-specific guardrails for secrets, piped installers, or SQL concatenation. It does not block tools. Sandbox, approvals, and requirements still do the enforcing.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Secrets, no piped installers, parameterized queries, no CI/infra edits | Highest prompt coverage. |
| Standard enterprise | Secrets, no piped installers, parameterized queries | Skip the CI/infra line so approved platform work can proceed. |
| Individual developers | Secrets and no piped installers | Keep it short. |

**What breaks:** Removing it does not disable tools. The agent follows default behavior.

## `computer_use`

**What it does:** Enables Computer Use, allowing Codex to see the screen, click, and type on the user's desktop (macOS only).

**Why it matters:** Computer Use is the most powerful capability — effectively giving the AI full desktop control. Prompt injection could cause unintended actions across any application.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | Far too powerful for high-risk environments. |
| Standard enterprise | `false` | Unless specific workflows are approved by security. |
| Power users | `true` (with caution) | Only with explicit awareness of prompt injection risks. |

---

## `memories`

**What it does:** Enables Memories, allowing Codex to carry context from past sessions into future work.

**Why it matters:** Memories persist potentially sensitive information across sessions. In shared or regulated environments, this creates data retention and cross-contamination concerns.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | No persistent memory. Each session is isolated. |
| Standard enterprise | `false` | Unless approved by data governance team. |
| Individual developers | `true` | Improves productivity for personal workstations. |

---

## `network_access` (under `[sandbox_workspace_write]`)

**What it does:** Controls whether commands executed in `workspace-write` sandbox mode can access the network.

**Why it matters:** Network access allows data exfiltration. An agent that can write files AND access the network can send code or secrets to external servers.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | `false` | Network should be disabled by default. Enable only for specific approved workflows (e.g., `npm install`). |

---

## `cli_auth_credentials_store`

**What it does:** Controls where Codex stores authentication credentials locally.

**Why it matters:** The `file` option stores credentials in plaintext at `~/.codex/auth.json`. Anyone with read access to the user's home directory can steal the token.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | `keyring` | Uses OS credential store (macOS Keychain, Windows Credential Manager, Linux Secret Service). Encrypted at rest. |

---

## `mcp_servers` (in requirements.toml)

**What it does:** Defines which MCP (Model Context Protocol) servers the agent is allowed to use.

**Why it matters:** MCP servers execute arbitrary operations. A malicious or misconfigured server can exfiltrate data, modify files, or execute commands outside the sandbox.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Empty `[mcp_servers]` | Disables all MCP servers. Zero external tool integrations. |
| Standard enterprise | Explicit allowlist | Only approved, audited servers. Match by command or URL identity. |
| Individual developers | Allowlist recommended | Encourage review of MCP servers before enabling. |

---

## `deny_read` (in requirements.toml)

**What it does:** Prevents the agent from reading specified file paths or patterns, even in writable sandbox modes.

**Why it matters:** Even in `read-only` mode, the agent can read sensitive files (SSH keys, cloud credentials, environment files). Deny-read rules add defense-in-depth.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Comprehensive deny list | Block `.ssh`, `.aws`, `.config/gcloud`, `.env`, `*.pem`, `*.key` |
| Standard enterprise | Credential-focused deny list | Block at minimum `.ssh/id_*`, `.aws/credentials`, `*.pem`, `*.key` |
| Individual developers | Optional | Consider blocking `.ssh` at minimum. |

---

## Summary: Recommended Profiles

### Maximum Lockdown (Regulated)

```toml
sandbox_mode = "read-only"
approval_policy = "on-request"
web_search = "disabled"

[features]
browser_use = false
in_app_browser = false
computer_use = false
memories = false
multi_agent = false
browser_use_full_cdp_access = false
browser_use_external = false

[computer_use]
allow_locked_computer_use = false
```

### Standard Enterprise

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"
web_search = "cached"

[features]
browser_use = false
computer_use = false
memories = false
codex_hooks = true
browser_use_full_cdp_access = false
browser_use_external = false

[computer_use]
allow_locked_computer_use = false
```

### Developer Teams

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"
web_search = "cached"

[features]
browser_use = true
in_app_browser = true
computer_use = false
memories = true
codex_hooks = true
multi_agent = true
browser_use_full_cdp_access = false
browser_use_external = false

[computer_use]
allow_locked_computer_use = false
```

## Tier delta (Codex 0.150 keys)

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `features.browser_use` | unconstrained in requirements (config `true`) | `false` | `false` | Baseline keeps in-app browsing. Moderate and Strict remove the web prompt-injection path. |
| `features.browser_use_full_cdp_access` | `false` | `false` | `false` | CDP is a debugger backdoor. No tier needs it for normal coding. |
| `features.browser_use_external` | `false` | `false` | `false` | External browsers expose the full cookie jar. In-app pane is enough on Baseline. |
| `features.computer_use` | `false` | `false` | `false` | Desktop control stays off on every tier. |
| `computer_use.allow_locked_computer_use` | `false` | `false` | `false` | Omit means unconstrained. Pin off so a later Computer Use exception still stops at lock screen. |
| `developer_instructions` | secrets + no piped installers | + parameterized queries, no new deps | + no CI/infra edits | Prompt only. Stricter text on Strict. Not valid in `requirements.toml`. |

## Workflow-preservation notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Browser Developer mode / full CDP | Debugger access to cookies and storage | Use the in-app browser pane without CDP, or inspect the page in a human-driven browser |
| Computer Use in Chrome, Edge, or Safari | The user's full cookie jar and password manager | Keep Browser Use in the in-app pane, or file an exception that still pins `allow_locked_computer_use = false` |
| Computer Use after the Mac locks | Unattended clicks and typing | Unlock the Mac, then continue the session |
| Piped installers (`curl \| bash`) via prompt only | Supply-chain install | Download, inspect the script, then run it. Sandbox and command rules are the real block. |

False-positive friction: pinning `browser_use_external = false` while `browser_use = true` (Baseline) is expected. Developers still get in-app browsing. If a workflow must drive the user's real browser, treat it as an exception request, not a default.

CLI and Desktop overlap: deploy one `requirements.toml`. Do not pin these keys only in Desktop `config.toml` and assume CLI hosts are covered.

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

## `in_app_browser.allow_external_browser_settings_import` (requirements.toml)

**What it does:** Blocks importing settings or browsing data from Chrome, Edge, or another browser into the Codex built-in browser pane when set to `false`. The built-in browser is the pane a person opens. It is separate from Browser Use, which is the agent browsing on its own. This key lives in the `[in_app_browser]` table of `requirements.toml`. It is separate from `features.in_app_browser`, which turns that pane on or off.

**Why it matters:** An import can copy cookies, saved site data, and history into Codex, including signed-in sessions. Setting this key to `true` does not block the import. Omitting it leaves the import available when other product checks allow it. `features.in_app_browser = false` turns the pane off and does not replace this key: a later exception that turns the pane on would still allow import. A value in `requirements.toml` cannot be overridden by `config.toml`. Do not copy this key into `config.toml`. Do not put it under `[features]`.

**What breaks if removed or set to `true`:** The built-in browser can import another browser's settings or browsing data. Set the TOML boolean `false`. The string `"false"` is not the documented value. Do not set `true`.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated (Strict) | `false` in `requirements.toml` | Import stays off even if a later exception turns the pane on. |
| Standard enterprise (Moderate) | `false` in `requirements.toml` | Same lock. The person signs in inside the pane or pastes the URL. |
| Individual developers (Baseline) | unset | Import follows the product default. |

### Tier delta

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `in_app_browser.allow_external_browser_settings_import` | unset | `false` | `false` | Baseline leaves import on the product default so a person can bring bookmarks or a signed-in profile into the pane. Moderate and Strict pin `false` in `requirements.toml`. Turning the pane off with `features.in_app_browser = false` does not block import if a later exception turns the pane back on. |

---

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

[in_app_browser]
allow_external_browser_settings_import = false
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

[in_app_browser]
allow_external_browser_settings_import = false
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
```

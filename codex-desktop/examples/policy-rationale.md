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

## `browser_use.default_origin_policy.downloads` (in requirements.toml)

Browser Use is the Codex feature that lets the agent open a browser and act on websites. The fallback origin policy applies only to sites that do not match an entry under `browser_use.origins`.

**What it does:** Blocks Browser Use from downloading files on those fallback sites when set to the quoted string `"deny"`.

**Why it is set this way:** Moderate and Strict set `downloads = "deny"`. A download from a site the admin never listed can place malware, an unreviewed installer, or sensitive files into the workspace. `"allow"` does not lock anything: it only lets the normal approval checks continue. Omitting the key leaves downloads unconstrained. Baseline leaves the key unset so low-friction teams keep the vendor default.

**What breaks if misconfigured or removed:** Removing the key, or setting `"allow"`, lets Browser Use download from any fallback site. Setting `access = "deny"` in the same table is a different control: it blocks Browser Use entirely on fallback origins, including page access, uploads, downloads, and browser debugging. `features.browser_use = false` turns the feature off and does not replace this key. If an admin later enables Browser Use for one group, the download lock still applies. A user `config.toml` cannot relax a managed deny. A matching origin rule replaces the fallback for that one site. Do not put organization hostnames in this template.

**Safe equivalent:** A person downloads the reviewed file, or an admin adds one origin rule for that site. An exception removes this key, or adds one origin rule, for a named group. Do not set `"allow"`.

**Overlap:** Codex Desktop, the Codex CLI, and the IDE extension read one `requirements.toml`. The CLI does not browse, so do not copy this key into `codex-cli/`. Cursor and Claude Code keep their own browser and shell download rules. This key does not replace those.

| Tier | Value | Reason for the difference |
|------|-------|---------------------------|
| Baseline | unset | Keeps the vendor default for startups and individual developers. |
| Moderate | `"deny"` | Blocks downloads from sites the admin never listed. |
| Strict | `"deny"` | Same lock. `"deny"` is already the strongest value for this key. |

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

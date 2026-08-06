# Codex Desktop App: Policy Rationale

Every setting below explains **what it does**, **why you should care**, and **the recommended value** for different environments.

---

## `sandbox_mode`

**What it does:** Controls what filesystem and network access the Codex agent has during execution.

**Why it matters:** The sandbox is the primary isolation boundary. A misconfigured sandbox can allow the AI agent to read sensitive files, modify system configurations, or exfiltrate data over the network.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated (finance, healthcare) | `read-only` | Agent can only read files (no writes, no network). Eliminates data modification risk. |
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

## `approvals_reviewer`

**What it does:** Chooses who reviews escalated approval prompts (sandbox escapes, blocked network, MCP prompts, ARC escalations). Values: `user` (human) or `auto_review` (guardian subagent). Legacy alias: `guardian_subagent`.

**Why it matters:** This is separate from `approval_policy` (when to pause). A fleet can pause on request but still route the decision to an automatic reviewer.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `user` | Human must approve escalations. |
| Standard enterprise | `user` | Same; allow auto_review only after guardian policy review. |
| Individual developers | `user` (start) | Opt into `auto_review` only with a written guardian policy. |

---

## `apps._default` (connected apps / connectors)

**What it does:** Sets org-wide defaults for ChatGPT Apps (connectors) unless a per-app `apps.<id>` table overrides them. Key fields: `enabled`, `approvals_reviewer`, `default_tools_approval_mode`, `destructive_enabled`, `open_world_enabled`.

**Why it matters:** Apps expand the tool surface beyond local MCP allowlists. Tools can advertise `destructive_hint` (destructive actions) or `open_world_hint` (broad external reach). Without defaults, users can enable permissive connector behavior.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `enabled=false`, reviewer `user`, mode `prompt`, destructive/open-world `false` | No connectors until an allowlisted pilot exists. |
| Standard enterprise | `enabled=true`, reviewer `user`, mode `prompt`, destructive/open-world `false` | Connectors allowed with human review and no destructive/open-world tools by default. |
| Individual developers | `enabled=true`, mode `writes`, destructive `false`, open-world `true` | More productive defaults; still block destructive_hint tools. |

**Overlap note:** Top-level `approvals_reviewer` covers non-app MCP and sandbox escalations. `apps._default.approvals_reviewer` covers connector tool prompts. Configure both so you do not leave a gap when Apps is enabled.

---

## `features.apps` / `features.enable_mcp_apps`

**What it does:** `features.apps` enables Apps (connector) integrations (stable, on by default). `enable_mcp_apps` controls the MCP-apps path used by some connectors. Pin `features.apps` in `requirements.toml` so users cannot override it.

**Why it matters:** Turning Apps off is the strongest control when your org is not ready for connectors. Managed defaults alone can be changed during a session until restart.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `apps=false` in requirements | Non-overridable disable. |
| Standard enterprise | `apps=true` + strict `apps._default` | Allow connectors under defaults. |
| Individual developers | `apps=true` | Keep upstream productivity. |

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

## `computer_use`

**What it does:** Enables Computer Use, allowing Codex to see the screen, click, and type on the user's desktop (macOS only).

**Why it matters:** Computer Use is the most powerful capability: it effectively gives the AI full desktop control. Prompt injection could cause unintended actions across any application.

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

## Tier Delta: Apps defaults

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `features.apps` (requirements) | `true` | `true` | `false` | Strict blocks connectors entirely; others allow under defaults. |
| `features.enable_mcp_apps` (config) | `true` | `true` | `false` | Align MCP-apps path with Apps availability. |
| `apps._default.enabled` | `true` | `true` | `false` | Defense in depth when Strict re-enables Apps later for a pilot. |
| `apps._default.approvals_reviewer` | `user` | `user` | `user` | All tiers start with human review for app tool prompts. |
| `apps._default.default_tools_approval_mode` | `writes` | `prompt` | `prompt` | Baseline auto-allows non-write tools; enterprise prompts every tool. |
| `apps._default.destructive_enabled` | `false` | `false` | `false` | Destructive-hinted connector tools stay off unless explicitly overridden. |
| `apps._default.open_world_enabled` | `true` | `false` | `false` | Baseline allows open-world tools; enterprise denies by default. |
| Top-level `approvals_reviewer` | `user` | `user` | `user` | Covers non-app escalations; pair with `apps._default`. |

---

## Summary: Recommended Profiles

### Maximum Lockdown (Regulated)

```toml
sandbox_mode = "read-only"
approval_policy = "on-request"
approvals_reviewer = "user"
web_search = "disabled"

[features]
browser_use = false
in_app_browser = false
computer_use = false
memories = false
multi_agent = false
apps = false
enable_mcp_apps = false

[apps._default]
enabled = false
approvals_reviewer = "user"
default_tools_approval_mode = "prompt"
destructive_enabled = false
open_world_enabled = false
```

### Standard Enterprise

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"
approvals_reviewer = "user"
web_search = "cached"

[features]
browser_use = false
computer_use = false
memories = false
codex_hooks = true
apps = true
enable_mcp_apps = true

[apps._default]
enabled = true
approvals_reviewer = "user"
default_tools_approval_mode = "prompt"
destructive_enabled = false
open_world_enabled = false
```

### Developer Teams

```toml
sandbox_mode = "workspace-write"
approval_policy = "on-request"
approvals_reviewer = "user"
web_search = "cached"

[features]
browser_use = true
in_app_browser = true
computer_use = false
memories = true
codex_hooks = true
multi_agent = true
apps = true
enable_mcp_apps = true

[apps._default]
enabled = true
approvals_reviewer = "user"
default_tools_approval_mode = "writes"
destructive_enabled = false
open_world_enabled = true
```

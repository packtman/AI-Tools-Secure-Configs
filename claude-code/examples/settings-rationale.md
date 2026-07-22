# Claude Code — Settings Rationale

Every managed setting explained: **what it does**, **why it matters**, and **the recommended value** for Regulated, Standard Enterprise, and Developer environments.

---

## Permission Rules

### `permissions.deny` — Deny rules

**What it does:** Blocks specific tool invocations. Deny rules are evaluated first and cannot be overridden by any other scope.

**Why it matters:** The deny list is your primary defense against dangerous agent actions. Without it, Claude Code can execute any shell command, read any file, and modify any path the user has access to.

**Key patterns and reasoning:**

| Pattern | Threat it blocks | Severity |
|---------|-----------------|----------|
| `Bash(curl * \| bash)` | Remote code execution via piped downloads | Critical |
| `Bash(sudo *)` | Privilege escalation beyond user scope | Critical |
| `Bash(eval *)` | Arbitrary code execution bypassing shell parsing | Critical |
| `Bash(rm -rf /)` | System destruction | Critical |
| `Bash(nc *)` / `Bash(ncat *)` | Network backdoors and reverse shells | High |
| `Bash(python* -c *)` | Interpreter-based code execution bypass | High |
| `Bash(python* -m http.server*)` | Unauthorized network listeners | High |
| `Bash(chmod 777 *)` | Removes all file permission restrictions | High |
| `Read(./.env)` / `Read(./.env.*)` | Credential theft from environment files | High |
| `Read(~/.ssh/**)` | SSH key theft | Critical |
| `Read(~/.aws/**)` | AWS credential theft | Critical |
| `Read(~/.gnupg/**)` | GPG key theft | High |
| `Read(~/.git-credentials)` | Git credential theft | High |
| `Write(~/.bashrc)` | Shell config poisoning (persistence) | Critical |
| `Write(./.env)` | Credential injection | High |

### `permissions.allow` — Allow rules

**What it does:** Lets specified tools run without prompting the user.

**Why it matters:** Over-broad allow rules remove the human-in-the-loop. Only truly read-only tools should be auto-allowed.

| Tool | Safe to auto-allow? | Reasoning |
|------|---------------------|-----------|
| `Read` | Yes | Read-only; blocked files are handled by deny rules |
| `Grep` | Yes | Search only; no side effects |
| `Glob` | Yes | File listing only; no side effects |
| `LS` | Yes | Directory listing only |
| `Diff` | Yes | Comparison only |
| `Write` | **No** | Creates/overwrites files — must require approval |
| `Edit` | **No** | Modifies files — must require approval |
| `Bash` | **No** | Executes arbitrary commands — must require approval |
| `WebFetch` | **No** | Makes network requests — data exfiltration risk |

### `permissions.disableBypassPermissionsMode`

**What it does:** Prevents users from launching Claude Code with `--dangerously-skip-permissions`.

**Why it matters:** Bypass mode skips ALL permission prompts. A user running in bypass mode has effectively given Claude Code unlimited shell access. In a managed environment, this defeats every other security control.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | `"disable"` | There is no legitimate enterprise use case for bypass mode on shared machines. |

---

## Managed-Only Settings

### `allowManagedPermissionRulesOnly`

**What it does:** When `true`, user and project `allow`, `ask`, and `deny` rules are ignored. Only rules from managed settings apply.

**Why it matters:** Prevents developers from weakening the deny list in their project `.claude/settings.json`.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Cannot allow any permission rule overrides in regulated environments. |
| Standard enterprise | `false` | Let teams add project-specific rules (they can tighten but not loosen managed deny rules). |
| Developer | `false` | Maximum flexibility. |

### `disableAutoMode`

**What it does:** Prevents activation of auto mode, which auto-approves tool calls with background safety checks.

**Why it matters:** Auto mode is a research preview. The background classifier may not catch all dangerous actions. In strict environments, every tool call should require human review.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `"disable"` | Auto-approval is unacceptable for compliance. |
| Standard enterprise | `"disable"` | Until auto mode exits research preview and the classifier is proven reliable. |
| Developer | Not set | Let developers opt in for personal productivity. |

### `disableWorkflows`

**What it does:** Disables dynamic workflows and bundled workflow commands. When enabled, workflow commands are unavailable, the `workflow` keyword does not trigger a workflow run, and `ultracode` is removed from the effort menu. Equivalent environment control: `CLAUDE_CODE_DISABLE_WORKFLOWS=1`.

**Why it matters:** Dynamic workflows are a research preview for long-running, parallel agent work. They can consume more usage and execute broader plans than a normal interactive session, so organizations should pilot them before enabling broadly.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Long-running autonomous workflows need explicit approval, audit coverage, and defined repository scope. |
| Standard enterprise | `true` | Disable until IT has a pilot group, usage monitoring, and an exception process. |
| Developer | `false` | Allow local experimentation after user confirmation prompts. |

### Background task controls

**What they do:** `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=0` keeps long MCP tool calls in the foreground. `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` disables every background task path, including Bash and subagent `run_in_background`, automatic backgrounding, and Ctrl+B.

**Why they matter:** On Claude Code 2.1.212 or later, a main-conversation MCP call moves to the background after two minutes by default. The call can keep changing an external system while Claude starts other work. Tiered controls make that concurrency explicit.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` | No hidden or concurrent task execution. Every Bash, subagent, and MCP operation remains visible until it finishes or is cancelled. |
| Standard enterprise | `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=0` | Prevent implicit MCP concurrency while preserving intentional Ctrl+B backgrounding for long developer tasks. |
| Developer | Neither variable set | Keep the vendor default and maximum workflow flexibility. |

**What breaks if the Strict control is set:** Ctrl+B and every `run_in_background` option become unavailable. Long-running commands and subagents must finish in the foreground.

**What breaks if the Moderate control is removed:** Long MCP calls use the vendor default and automatically leave the foreground after two minutes, so external side effects may overlap with later work.

### `allowManagedHooksOnly`

**What it does:** Blocks all hooks except those in managed settings, SDK hooks, and hooks from force-enabled managed plugins.

**Why it matters:** Hooks execute shell commands at lifecycle events. A malicious hook in a project's `.claude/settings.json` could exfiltrate conversation data, inject instructions, or modify files.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Only IT-deployed hooks should run. |
| Standard enterprise | `false` | Allow project teams to define their own hooks (linting, testing). |
| Developer | `false` | Maximum flexibility. |

### `allowManagedMcpServersOnly`

**What it does:** Only the MCP server allowlist from managed settings is respected. Users can still add servers, but they won't connect.

**Why it matters:** MCP servers can execute arbitrary operations. An unvetted MCP server in a project `.mcp.json` could read source code and exfiltrate it.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Only IT-approved MCP servers. |
| Standard enterprise | `false` | Let teams use project MCP servers with approval dialogs. |
| Developer | `false` | Maximum flexibility. |

### `CLAUDE_CODE_MCP_ALLOWLIST_ENV`

**What it does:** Starts stdio MCP servers with a safe baseline environment plus only variables explicitly configured for that server.

**Why it matters:** By default, a local MCP server inherits the developer's shell environment. That can expose unrelated cloud, package registry, or service credentials to a compromised server.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | `"1"` | Require each MCP server to declare the minimum environment it needs. |

**What breaks if set:** MCP servers that depended on undeclared shell variables can fail to start or authenticate. Add the required names to the server's `env` configuration and resolve secret values through the approved secrets manager.

### `forceRemoteSettingsRefresh`

**What it does:** Blocks CLI startup until server-managed settings are freshly fetched. Exits if fetch fails.

**Why it matters:** Without this, there is a brief window on startup where managed settings are not yet enforced. An attacker who times actions during this window could bypass policies.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Zero-tolerance for unenforced windows. Ensure `api.anthropic.com` is reachable first. |
| Standard enterprise | `false` | Cached settings are sufficient; failing closed could block all work during API outages. |
| Developer | `false` | Availability over strict enforcement. |

---

## Identity & Login

### `forceLoginMethod`

**What it does:** Restricts authentication to `claudeai` (Claude.ai accounts) or `console` (Anthropic Console / API billing).

**Why it matters:** Ensures all users authenticate through your organization's managed identity, not personal accounts.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Enterprise | `"claudeai"` | Forces login through Claude.ai org accounts with SSO. |
| API-billing teams | `"console"` | For teams billed through the API console. |

### `forceLoginOrgUUID`

**What it does:** Requires the authenticated account to belong to a specific organization (by UUID or array of UUIDs).

**Why it matters:** Prevents users from authenticating with personal or other-org accounts that aren't subject to your managed settings.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All enterprise | Set to your org UUID | Prevents policy bypass via alternate accounts. |

### `requiredMinimumVersion`

**What it does:** Blocks Claude Code startup when the installed version is below the managed floor. The recovery commands `claude update`, `claude install`, and `claude doctor` remain available.

**Why it matters:** The older `minimumVersion` key prevents automatic downgrades but never blocks an outdated client from starting. Moderate and Strict require 2.1.212 so every active client understands the automatic MCP backgrounding control.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `"2.1.212"` or a newer security-approved release | Hard floor keeps background task and security behavior consistent. |
| Standard enterprise | `"2.1.212"` or a newer pilot-tested release | Guarantees support for `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`. |
| Developer | Keep `minimumVersion` as an updater floor | Baseline prioritizes startup availability and does not depend on managed MCP backgrounding. |

**What breaks if set too high:** Older clients refuse to start until IT deploys a compliant version. Test the floor on every supported OS and retain an approved installer before rollout.

---

## Sandbox

### `sandbox.enabled`

**What it does:** Enables OS-level filesystem and network isolation for Bash commands.

**Why it matters:** Permissions are evaluated by Claude Code's own logic; the sandbox is enforced by the OS (Seatbelt on macOS, bubblewrap on Linux). Even if Claude is tricked by prompt injection, sandboxed commands physically cannot access restricted paths or network hosts.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | `true` | Defense-in-depth. Sandbox + permissions = two independent security layers. |

### `sandbox.allowUnsandboxedCommands`

**What it does:** Allows Claude Code to retry a failed sandboxed command outside the sandbox (with user approval).

**Why it matters:** This escape hatch weakens the sandbox. If enabled, a cleverly-crafted failure scenario could trick a user into approving an unsandboxed dangerous command.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | No escape hatch. All commands stay sandboxed. |
| Standard enterprise | `false` | Prefer `excludedCommands` for specific known-incompatible tools. |
| Developer | `true` | Convenience for edge cases, with user approval as the gate. |

### `sandbox.network.allowManagedDomainsOnly`

**What it does:** Only domains in the managed-level allowlist are accessible from sandboxed Bash commands. Non-allowed domains are blocked without prompting.

**Why it matters:** Prevents data exfiltration. Without this, Claude could `curl` arbitrary endpoints to send code or credentials.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Strict network control. Only approved registries and APIs. |
| Standard enterprise | `false` | Let users approve new domains via prompts during development. |

---

## Features

### `disableRemoteControl`

**What it does:** Blocks the remote control feature, which allows external tools to send commands to Claude Code.

**Why it matters:** Remote control could be abused to inject prompts or commands from untrusted sources.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | No external control of the agent. |
| Standard enterprise | `true` | Unless specific remote control integrations are approved. |

### `disableSkillShellExecution`

**What it does:** Blocks shell execution in skill files and custom commands from user/project sources.

**Why it matters:** A malicious skill file in a project could execute arbitrary commands when the skill is loaded.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Skills should not execute shell commands. |
| Standard enterprise | `false` | Skills are useful for developer workflows. |

### `autoMemoryEnabled` / `CLAUDE_CODE_DISABLE_AUTO_MEMORY`

**What it does:** Controls whether Claude Code saves learnings to disk for future sessions.

**Why it matters:** Saved memory may contain sensitive context from conversations. In high-security environments, no data should persist beyond the session.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Disabled | No persistent AI memory. Prevents data leakage between sessions. |
| Standard enterprise | Enabled | Productivity benefit outweighs risk. |

### `CLAUDE_CODE_SKIP_PROMPT_HISTORY`

**What it does:** Skips writing session transcripts to disk.

**Why it matters:** Session transcripts contain full conversations — prompts, responses, code, and possibly sensitive data. If the machine is compromised, transcripts are a high-value target.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `1` | No session history on disk. |
| Standard enterprise | Not set | Session history aids debugging and productivity. |

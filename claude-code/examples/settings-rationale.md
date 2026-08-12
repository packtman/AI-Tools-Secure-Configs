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

### `sandbox.bwrapPath` / `sandbox.socatPath`

**What they do:** Managed-only absolute paths to `bwrap` and `socat` on Linux/WSL2. Override `PATH` auto-detection.

**Why they matter:** Locked-down images often restrict `PATH` or install sandbox helpers outside default locations. Without pins, sandboxed Bash fails even when packages are present. Ignored on macOS (Seatbelt).

**What breaks if wrong:** Sandbox cannot start. Strict with `failIfUnavailable: true` blocks work. Moderate with `failIfUnavailable: false` continues without sandbox (weaker isolation).

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `/usr/bin/bwrap` and `/usr/bin/socat` (or your image paths) | Fail-closed sandbox must find binaries reliably. |
| Standard enterprise | Same pins | Reduce sandbox setup tickets on managed Linux/WSL2. |
| Developer | Unset (auto-detect) | Local installs vary; PATH detection is enough. |

---

## Corporate launcher and dynamic policy

### `processWrapper` / `CLAUDE_CODE_PROCESS_WRAPPER`

**What it does:** Prefixes Claude Code self-spawns (background service, agent view sessions, remote control workers, update relaunches) with a corporate launcher command. The env var takes precedence when both are set. Requires Claude Code >= 2.1.210 for the settings key (>= 2.1.208 for the env var). Ignored on Windows. Ignored from project/local settings.

**Why it matters:** PATH wrappers cannot see processes started from the binary path. Without this, mandatory launcher / credential-injection policies miss Claude Code's background processes.

**What breaks if misconfigured:** Claude Code refuses to start the affected process (fail closed). A slow or non-`exec` launcher breaks agent view tracking.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Set absolute launcher path when org mandates process wrapping | Required for endpoint policy parity. |
| Standard enterprise | Optional; set when a launcher already exists | Do not invent a placeholder path in deployable JSON. |
| Developer | Unset | No mandatory launcher. |

### `policyHelper`

**What it does:** Points at an admin-deployed executable that prints a JSON envelope with `managedSettings` (and optional `claudeMd` / `appendSystemPrompt`). Only honored from MDM or system `managed-settings.json`. When configured, helper output is the **only** managed source for that run. Not honored from server-managed settings, user/project settings, or HKCU.

**Why it matters:** Lets policy follow device posture, identity, or a remote service instead of a static file.

**What breaks if misconfigured:** Non-zero exit at startup refuses to start Claude Code. Wrong helper can wipe expected MDM/file policy because it replaces other managed sources. Parent embedder merge is disabled while the helper is active.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Use only with a tested, cached helper and outage plan | Highest blast radius managed control. |
| Standard enterprise | Prefer static managed JSON unless posture routing is required | Simpler operations. |
| Developer | Unset | Not applicable. |

### `wslInheritsWindowsSettings`

**What it does:** Windows managed-settings flag so WSL Claude Code also reads the Windows policy chain (Windows sources win). Only from HKLM or `C:\Program Files\ClaudeCode\managed-settings.json`.

**Why it matters:** One Windows MDM payload covers native Windows and WSL.

**What breaks if false on mixed fleets:** WSL sessions miss Windows-deployed policy.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated / Standard enterprise (Windows+WSL) | `true` | Single payload. |
| Developer / Linux-only / macOS-only | Unset | Not applicable. |

See `examples/corporate-launcher-and-policy-helper.md` for phased rollout, MDM steps, and validation.

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

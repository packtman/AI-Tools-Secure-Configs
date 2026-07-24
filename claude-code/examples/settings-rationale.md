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

### `disableAgentView`

**What it does:** Turns off background agents and agent view (`claude agents`, `--bg`, `/background`, and the on-demand supervisor). Equivalent environment control: `CLAUDE_CODE_DISABLE_AGENT_VIEW=1`.

**Why it matters:** Background agents continue working without continuous operator attention. That expands the window for unintended shell, MCP, or network actions after a prompt-injection or misconfigured permission.

**What breaks:** Developers cannot run background agent sessions or supervise parallel agents from agent view. Use foreground Claude Code sessions instead.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Keep all agent work interactive and visible. |
| Standard enterprise | `true` | Prefer foreground sessions until a monitored background-agent pilot exists. |
| Developer | `false` | Allow local background-agent experimentation. |

### `disableArtifact`

**What it does:** Disables the Artifact tool, which publishes session output as a separately stored, shareable web page on claude.ai. Equivalent environment control: `CLAUDE_CODE_DISABLE_ARTIFACT=1`.

**Why it matters:** Artifact content can include source code and data from connected tools. Disabling it keeps review output inside approved repository and documentation workflows.

**What breaks:** Developers cannot publish interactive artifact pages from Claude Code.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Removes an additional storage and sharing surface. |
| Standard enterprise | `true` | Require publication through approved documentation or review systems. |
| Developer | `false` | Preserve the permission-gated artifact workflow. |

### `awaySummaryEnabled`

**What it does:** Shows a one-line session recap when the user returns after being away. Equivalent environment override: `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` (`0` forces off, `1` forces on).

**Why it matters:** Recaps summarize recent session activity and can surface sensitive code or secrets on a shared screen.

**What breaks:** Setting `false` (or env `0`) removes the return-to-terminal recap. Session history and `/resume` remain available when those features are enabled.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | Avoid unexpected on-screen summaries of sensitive work. |
| Standard enterprise | `false` | Reduce shoulder-surfing and shared-terminal exposure. |
| Developer | `true` | Preserve the productivity recap. |

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

### `disableBundledSkills`

**What it does:** Removes Claude Code's bundled skills and workflows from the model. Custom and plugin skills remain available. Equivalent environment control: `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1`.

**Why it matters:** Strict environments can reduce model-visible orchestration to only organization-reviewed skills.

**What breaks:** Bundled skills such as `/run`, `/verify`, `/debug`, and `/code-review` are unavailable. `/doctor` remains available.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Restrict orchestration to reviewed custom or managed skills. |
| Standard enterprise | `false` | Preserve common development and verification workflows. |
| Developer | `false` | Preserve all bundled productivity features. |

### `fileCheckpointingEnabled`

**What it does:** Controls local file snapshots used by `/rewind` to restore edits. Equivalent environment disable: `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING=1`.

**Why it matters:** Snapshot files persist source content with the session and increase the amount of sensitive code stored on the endpoint.

**What breaks:** Setting `false` removes code restore from `/rewind`. Git remains the supported recovery mechanism.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | Minimize persistent source copies on endpoints. |
| Standard enterprise | `true` (default) | Recovery value outweighs the local storage risk. |
| Developer | `true` (default) | Preserve fast local recovery. |

### `autoMemoryEnabled` / `CLAUDE_CODE_DISABLE_AUTO_MEMORY`

**What it does:** Controls whether Claude Code saves learnings to disk for future sessions.

**Why it matters:** Saved memory may contain sensitive context from conversations. In high-security environments, no data should persist beyond the session.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Disabled | No persistent AI memory. Prevents data leakage between sessions. |
| Standard enterprise | Enabled | Productivity benefit outweighs risk. |

### `CLAUDE_CODE_SKIP_PROMPT_HISTORY`

**What it does:** Skips writing session transcripts to disk.

**Why it matters:** Session transcripts contain full conversations: prompts, responses, code, and possibly sensitive data. If the machine is compromised, transcripts are a high-value target.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `1` | No session history on disk. |
| Standard enterprise | Not set | Session history aids debugging and productivity. |

### `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`

**What it does:** Disables Bash and subagent `run_in_background`, automatic backgrounding, MCP backgrounding, and the Ctrl+B shortcut.

**Why it matters:** Foreground execution keeps autonomous work visible and prevents concurrent tasks from continuing while the developer focuses elsewhere.

**What breaks:** Long commands and subagents occupy the active session until they finish. Developers cannot use Ctrl+B to background them.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `"1"` | Keep all agent work visible and synchronous. |
| Standard enterprise | `"1"` | Preserve operator awareness while broader agent controls mature. |
| Developer | Not set | Preserve background-task productivity. |

### `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`

**What it does:** Skips auto-installation of the Claude Code IDE extension. Equivalent setting: `autoInstallIdeExtension: false`.

**Why it matters:** Unreviewed IDE extension installs can change editor behavior and expand the AI tool surface outside MDM-controlled software catalogs.

**What breaks:** Developers must install the approved IDE extension through the organization's software channel.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `"1"` | Only MDM or software-catalog installs. |
| Standard enterprise | `"1"` | Keep extension rollout managed. |
| Developer | Not set | Allow convenience auto-install. |

### `CLAUDE_CODE_AUTO_CONNECT_IDE`

**What it does:** Overrides automatic IDE connection when Claude Code starts outside an IDE terminal. Equivalent setting: `autoConnectIde`.

**Why it matters:** Auto-connecting to an IDE from an external terminal can attach Claude Code to an unexpected editor session and broaden context sharing.

**What breaks:** Setting `"false"` requires an explicit IDE connection when launching from an external terminal.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `"false"` | Require deliberate IDE attachment. |
| Standard enterprise | Not set | Default auto-connect behavior is acceptable with managed login. |
| Developer | Not set | Preserve convenience. |

### `requiredMinimumVersion`

**What it does:** Blocks startup when the installed Claude Code version is below the managed floor. Update, install, and doctor commands remain available for recovery.

**Why it matters:** `minimumVersion` only prevents future downgrades and does not stop an already-old client from starting. Policies that rely on newer controls need a hard startup floor.

**What breaks:** Setting the floor above the deployed fleet version prevents Claude Code from starting until clients update.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `"2.1.212"` or later validated version | Ensures current agent-view, artifact, and background-task enforcement. |
| Standard enterprise | `"2.1.212"` or later validated version | Ensures the Moderate policy controls are implemented by the client. |
| Developer | Keep `minimumVersion` only | Avoid blocking startup while still preventing accidental downgrade. |

### Terms intentionally not pinned in tier files

These discovery terms are real documentation tokens but are not enterprise security controls for this repo's tiers:

| Term | Why it is not pinned |
|------|----------------------|
| `ANTHROPIC_MODEL` | Model selection preference. Pinning a model can break teams that use Bedrock, Vertex, Foundry, or approved model allowlists. |
| `CLAUDE_MODEL` | Not a valid managed settings or hooks control. Treat as documentation noise if it appears in discovery. |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Subagent model routing preference, not a threat control. Leave unset unless an org model governance standard requires it. |

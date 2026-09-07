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
### `fastMode`

**What it does:** Turns Claude Code Fast mode on or off. Fast mode is a research preview that uses Claude Opus (Opus 5 or Opus 4.8) at higher per-token cost for lower latency. It is not a different model. Running `/fast` writes `fastMode: true` to `~/.claude/settings.json` and, by default, that preference persists across sessions.

**Why it matters:** Fast mode is extra spend. On Pro, Max, Team, and Enterprise it draws from usage credits, even when included plan usage remains. On Console it bills at Fast mode rates. Team and Enterprise keep it off until an Owner enables it at Admin Settings > Claude Code. Device managed settings close the gap for users who already opted in, and for Console orgs that provisioned API access. Equivalent env kill switch: `CLAUDE_CODE_DISABLE_FAST_MODE=1` (the settings key cannot turn Fast mode back on while that env is set).

**This is not Codex Fast mode.** Codex uses `features.fast_mode` in `config.toml` / `requirements.toml`. Pin both if the org runs both tools.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` plus `CLAUDE_CODE_DISABLE_FAST_MODE=1` | Research-preview spend path, and `--settings` must not re-enable it. |
| Standard enterprise | `false` plus `CLAUDE_CODE_DISABLE_FAST_MODE=1` | Keep standard-speed Opus until billing and an exception process exist. |
| Developer | Unset | Vendor default is off. Users may run `/fast` after Owner enablement or provisioned Console access. |

Do not set `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK` or `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`. Those skip the org-disabled availability check that Fast mode runs against `api.anthropic.com`.

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
### `disableClaudeAiConnectors`

**What it does:** Stops Claude Code from fetching MCP connectors attached to the signed-in claude.ai account, so those connectors never connect. MCP is Model Context Protocol, a way for AI tools to call external services.

**Why it matters:** The vendor default is `false`. Without this pin, Drive, Slack, GitHub, and custom claude.ai connectors load into Claude Code even when `managed-mcp.json` is not deployed. `allowManagedMcpServersOnly` does not cover this path. A `true` in any file applies; a project-level `false` cannot override a managed `true`. Distinct from `allowAllClaudeAiMcps` (leave unset: default `false` keeps `managed-mcp.json` exclusive). Requires Claude Code v2.1.182 or later. Session env `ENABLE_CLAUDEAI_MCP_SERVERS=false` is a one-session kill.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Personal claude.ai connectors are an unvetted MCP path. |
| Standard enterprise | `true` | Keep MCP on org-approved servers until connectors are allowlisted. |
| Developer | Unset | Allow personal connectors after the normal MCP approval prompt. |

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

### `availableModels`

**What it does:** Restricts which models users can select for the main session, subagents, skills, the advisor, and background agents. Entries match a family (`sonnet`), a version prefix, or a full model ID. A managed list replaces user and project entries as of Claude Code v2.1.175.

**Why it matters:** `ANTHROPIC_MODEL`, `CLAUDE_MODEL`, `--model`, and `/model` are session overrides. They are not org policy. Without a managed allowlist, any entitled model can run, including high-capability families you did not approve for cost, data handling, or capability reasons. An empty array (`[]`) blocks named picks but still leaves the account Default usable.

**What goes wrong:** If the list has no guaranteed-available entry, Default-model enforcement is skipped. Device-local files do not reach Claude Code on the web; use server-managed settings for cloud sessions. On Bedrock, Vertex, Foundry, or a custom `ANTHROPIC_BASE_URL`, list the provider IDs your gateway actually serves.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `["sonnet", "haiku"]` | Keep common coding models. Exclude `opus` and `fable` until those families have an explicit exception. |
| Standard enterprise | `["sonnet", "haiku", "opus"]` | Allow Opus for harder coding tasks. Still exclude `fable` until advisor and usage-credit review is done. |
| Developer | Unset | Startups can use any entitled model. Pin the list when you need an org allowlist. |

### `enforceAvailableModels`

**What it does:** When `true` in managed settings and `availableModels` is a non-empty array, the Default picker option cannot resolve to a model outside the list. Requires Claude Code v2.1.175 or later.

**Why it matters:** `availableModels` alone leaves Default on the account or org default. That is the loophole: a developer never types `--model` and still lands on an unapproved family.

**What goes wrong:** `availableModels: []` never engages this setting. Pair it with `minimumVersion: "2.1.175"` (or `requiredMinimumVersion` if you need a hard startup floor).

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Close the Default loophole. |
| Standard enterprise | `true` | Same control; keep Opus in the allowlist so Default can remap to an approved family. |
| Developer | Unset | No allowlist to enforce. |

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

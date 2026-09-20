# Claude Code Moderate Settings: Comment Reference

Use this file with the deployable `managed-settings-moderate.json`. Each key explains what it does, why Moderate sets it this way, and what breaks if it is wrong.

## `disableAgentView`

**Value:** `true`

**What:** Turns off background agents and agent view (`claude agents`, `--bg`, `/background`, and the on-demand supervisor).

**Why (Moderate tier):** Background agents continue without continuous operator attention and expand the window for unintended shell, MCP, or network actions.

**What breaks if set to true:** Developers must use foreground Claude Code sessions. Request a monitored pilot exception for background agents.

**Strict difference:** Also `true`.

**Baseline difference:** `false`, allowing local background-agent experimentation.

---

## `disableArtifact`

**Value:** `true`

**What:** Disables the Artifact tool, which publishes session output as a separately stored web page on claude.ai.

**Why (Moderate tier):** Prevents source code and session-derived data from leaving the repository review workflow through an artifact link.

**What breaks if set to true:** Developers cannot publish interactive artifact pages from Claude Code. Use the organization's approved documentation or review platform instead.

**Strict difference:** Also `true`.

**Baseline difference:** `false`, preserving permission-gated artifact publishing.

---

## `awaySummaryEnabled`

**Value:** `false`

**What:** Disables the one-line session recap shown when a user returns to the terminal.

**Why (Moderate tier):** Recaps can expose sensitive code or secrets on shared screens.

**What breaks if set to false:** No automatic away-summary line. Session history and resume features remain governed by their own settings.

**Strict difference:** Also `false`, reinforced with `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0`.

**Baseline difference:** `true`, preserving the productivity recap.

---

## `disableWorkflows`

**Value:** `true`

**What:** Disables dynamic workflows and bundled workflow commands.

**Why (Moderate tier):** Long-running multi-agent workflows need a monitored pilot first.

**What breaks if set to true:** Workflow commands and ultracode are unavailable.

---

## `requiredMinimumVersion`
## `fastMode`

**Value:** `false`

**What:** Turns Claude Code Fast mode off. Fast mode is a research preview that uses Claude Opus (Opus 5 or Opus 4.8) at higher per-token cost for lower latency. `/fast` writes `fastMode: true` to `~/.claude/settings.json` and, by default, that preference persists across sessions.

**Why (Moderate tier):** Fast mode is extra spend on usage credits (subscription plans) or API tokens (Console), and it is disabled by default for Team and Enterprise until an Owner enables it in Admin Settings. Moderate keeps standard-speed work available and blocks this path until billing, usage-credit, and an exception process exist. Pair with `CLAUDE_CODE_DISABLE_FAST_MODE=1` so `--settings '{"fastMode": true}'` cannot turn it back on for one session.

**What breaks if set to false:** `/fast` stays off, the lightning icon does not appear, and sessions stay on standard-speed Opus (or the current model). Interactive debugging that wanted lower latency uses standard Opus or a lower effort level instead.

**Strict difference:** Also `false`, with the same env kill switch.

**Baseline difference:** Unset. Vendor default is off. Users may run `/fast` after the Owner console toggle (Team/Enterprise) or provisioned Console access.

**Overlap:** Codex `features.fast_mode` is a different product. If the org deploys both Claude Code and Codex, pin both. Do not set `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK` or `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`; those skip the org-disabled availability check.

---

## `disableClaudeAiConnectors`

**Value:** `true`

**What:** Stops Claude Code from fetching or connecting MCP connectors attached to the signed-in claude.ai account.

**Why (Moderate):** The vendor default is `false`, so Drive, Slack, and custom claude.ai connectors load into Claude Code even when you have not deployed `managed-mcp.json`. `allowManagedMcpServersOnly` only locks the `allowedMcpServers` list; it does not stop this fetch. A managed `true` is one-way: a project `.claude/settings.json` cannot set `false` to turn connectors back on. Distinct from `allowAllClaudeAiMcps`, which is relevant only after `managed-mcp.json` is deployed (leave that key unset; the default `false` keeps exclusive control). Requires Claude Code v2.1.182 or later. Session env `ENABLE_CLAUDEAI_MCP_SERVERS=false` is a one-session kill, not a substitute for the managed key.

**What breaks if removed:** Personal claude.ai connectors load and can read or send repository data outside the org MCP allowlist.

**Strict difference:** Also `true`. Strict still needs this pin because `allowManagedMcpServersOnly` does not cover claude.ai connectors unless `managed-mcp.json` is also deployed.

**Baseline difference:** Unset, so startups can use personal claude.ai connectors after the normal MCP approval prompt.

---

## `enableAllProjectMcpServers`

**Value:** `false`

**What:** Stops Claude Code from auto-approving every MCP server defined in a project `.mcp.json` file. MCP is Model Context Protocol, a way for AI tools to call external services.

**Why (Moderate):** The vendor default is unset, which asks once per server. Any-file scope means a repo `.claude/settings.json`, `~/.claude/settings.json`, `--settings`, or the approval dialog ("approve all", which writes this key to `.claude/settings.local.json`) can set `true` and skip review. Managed `false` is the lock in a trusted folder. Distinct from `allowManagedMcpServersOnly` (that key only locks the `allowedMcpServers` list; Moderate keeps it `false` so project MCP still works after a prompt). Distinct from `disableClaudeAiConnectors` (claude.ai account connectors, not `.mcp.json`). Distinct from `enabledMcpjsonServers` (named allowlist, org-specific) and `disabledMcpjsonServers` (named denylist, org-specific). No env-var substitute. JSON boolean `false` only. The string `"false"` is ignored.

**What breaks if removed:** A project can auto-connect every `.mcp.json` server, including filesystem or shell servers, without a prompt.

**Strict difference:** Also `false`. Strict still needs this pin because `allowManagedMcpServersOnly` does not replace the project `.mcp.json` approval path. If managed `allowedMcpServers` is unset, every matching server is still allowed and auto-approval would skip the prompt.

**Baseline difference:** Unset, so startups can click "approve all" for local experimentation.

---

## `forceLoginMethod` / `forceLoginOrgUUID`

**Value:** `"2.1.212"`

**What:** Blocks Claude Code startup on older clients while leaving update, install, and doctor commands available for recovery.

**Why:** The Moderate policy relies on current agent-view, artifact, and background-task enforcement. The older `minimumVersion` key prevents downgrade but does not block startup.

**What breaks if too high:** Developers cannot start Claude Code until IT deploys an approved version at or above the configured floor. Validate the pilot fleet before raising the floor.

**What breaks if removed:** Older clients can start without the expected background task behavior or current security fixes.

---

## `sandbox` settings

### `sandbox.enabled: true`
OS-level isolation for Bash commands. Defense-in-depth: the sandbox is enforced by the OS (Seatbelt on macOS, bubblewrap on Linux), not by Claude Code itself.

### `sandbox.autoAllowBashIfSandboxed: true`
Auto-approve sandboxed Bash commands. Reduces prompt fatigue while the sandbox limits blast radius.

### `sandbox.allowUnsandboxedCommands: false`
Prevents the "try without sandbox" escape hatch. A crafted failure could trick users into approving unsandboxed commands.

### `sandbox.failIfUnavailable: false`
In Moderate tier, allow work to continue if the sandbox is unavailable (e.g., missing bubblewrap on a new machine). In Strict tier, this is `true` (fail-closed).

---

## `minimumVersion`

**What:** Floor that prevents auto-update and `claude update` from installing a version below this one.

**Why (Moderate tier):** `enforceAvailableModels` requires Claude Code v2.1.175 or later. Older builds apply `availableModels` but still let Default resolve to an unapproved model.

**What breaks if set too high:** Users on an older approved build cannot start until they update through the org-approved channel.

---

## `availableModels`

**What:** Allowlist of model families (or version prefixes / full IDs) users may select for the main session, subagents, skills, the advisor, and background agents.

**Why (Moderate tier):** `ANTHROPIC_MODEL`, `CLAUDE_MODEL`, `--model`, and `/model` are session overrides, not org policy. A managed list replaces user and project entries as of v2.1.175. Moderate keeps `sonnet`, `haiku`, and `opus` so standard coding work still has a high-capability option. Do not ship `[]`: that blocks named models but leaves the account Default usable even with `enforceAvailableModels`.

**What breaks if misconfigured:** An excluded family is substituted or rejected at startup (`--model`, `ANTHROPIC_MODEL`, resumed transcripts, `advisorModel`). Keep at least one guaranteed-available entry. Cloud sessions on Anthropic-managed VMs ignore device files: deliver this list through server-managed settings.

---

## `enforceAvailableModels`

**What:** Extends `availableModels` to the Default picker option so Default cannot resolve to a model outside the list.

**Why (Moderate tier):** Without this, a developer picks Default and lands on the account or org default, which may be a model you intended to restrict. Requires v2.1.175+ and a non-empty `availableModels` list.

**What breaks if removed:** The Default loophole returns. **What breaks if true with `availableModels: []`:** Enforcement is skipped.

---

## `env` settings

### `CLAUDE_CODE_ENABLE_TELEMETRY: "0"`
Disables telemetry. Data minimization principle.

### `CLAUDE_CODE_DISABLE_AUTO_MEMORY: "1"`
Prevents Claude Code from saving learnings to disk. Reduces risk of sensitive context persisting across sessions.

### `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS: "1"`
Keeps Bash commands, subagents, and MCP calls in the foreground so the operator can see when they are active.

### `CLAUDE_CODE_ENABLE_AWAY_SUMMARY: "0"`
Forces session recaps off even if a user re-enables them in `/config`.

### `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL: "1"`
Blocks auto-installation of the Claude Code IDE extension so installs go through the approved software channel.

### `CLAUDE_CODE_MCP_ALLOWLIST_ENV: "1"`

**What:** Starts stdio MCP servers with Claude Code's safe baseline environment plus only the variables explicitly declared in that server's configuration.

**Why (Moderate tier):** A local MCP process does not need every credential exported in the developer's shell. Restricting inheritance reduces the damage from a compromised or overprivileged server.

**What breaks if removed:** Every stdio MCP server can inherit unrelated shell tokens and credentials.

**What breaks if misconfigured:** A server that relied on an inherited variable may fail to start or authenticate. Add only its required variables to the server's `env` configuration, using your secrets manager rather than literal credentials.

**Tier difference:** Baseline, Moderate, and Strict all set this to `"1"` because ambient credential exposure is not required for normal MCP operation.

### `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS: "0"`

**What:** Keeps every MCP tool call in the foreground instead of automatically moving calls longer than two minutes to background tasks. This control applies to Claude Code 2.1.212 and later.

**Why (Moderate tier):** MCP tools can modify external systems. Keeping a long call visible prevents Claude from starting unrelated work while the external operation is still running. Developers can still press Ctrl+B to background a call intentionally.

**What breaks if removed:** Long MCP calls use the vendor default and move to the background after two minutes. The call continues while Claude works on something else, which can create unexpected concurrent side effects.

**Strict difference:** Strict sets `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS: "1"` instead, removing explicit and automatic backgrounding for Bash, subagent, and MCP work.

**Baseline difference:** Baseline leaves both variables unset and uses the vendor default, including automatic backgrounding for MCP calls longer than two minutes on Claude Code 2.1.212 or later.
### `CLAUDE_CODE_DISABLE_FAST_MODE: "1"`
Session kill switch for Fast mode. Read at startup. The `fastMode` settings key cannot turn Fast mode back on while this is set. Do not set `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK` or `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS`.

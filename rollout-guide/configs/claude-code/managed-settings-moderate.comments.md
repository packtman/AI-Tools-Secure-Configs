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

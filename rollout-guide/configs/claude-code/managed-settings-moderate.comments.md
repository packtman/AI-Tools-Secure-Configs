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

**What breaks if set above the deployed version:** Claude Code exits until the endpoint is updated. Validate the pilot fleet before raising the floor.

---

## `env` settings

### `CLAUDE_CODE_ENABLE_TELEMETRY: "0"`
Disables telemetry. Data minimization principle.

### `CLAUDE_CODE_DISABLE_AUTO_MEMORY: "1"`
Prevents Claude Code from saving learnings to disk.

### `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS: "1"`
Keeps Bash commands, subagents, and MCP calls in the foreground so the operator can see when they are active.

### `CLAUDE_CODE_ENABLE_AWAY_SUMMARY: "0"`
Forces session recaps off even if a user re-enables them in `/config`.

### `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL: "1"`
Blocks auto-installation of the Claude Code IDE extension so installs go through the approved software channel.

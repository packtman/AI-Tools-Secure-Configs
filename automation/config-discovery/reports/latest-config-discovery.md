# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | content-changed | 200 | https://code.claude.com/docs/en/settings.md |
| Claude Code | Hooks documentation | content-changed | 200 | https://code.claude.com/docs/en/hooks.md |
| Claude Code | Dynamic workflows documentation | content-changed | 200 | https://code.claude.com/docs/en/workflows.md |
| Claude Code | Claude Code changelog | new-source-baseline | 200 | https://code.claude.com/docs/en/changelog.md |

## Review Details

### Claude Code: Managed settings documentation

- Change type: `content-changed`
- Source URL: https://code.claude.com/docs/en/settings.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... ------------------------------------------------------------------------------------------------
------------ | :------------------------------------------ | | **Managed** | Server-managed
settings, plist / registry, or system-level `managed-settings.json` | All organization members for
server-managed delivery; all users on the machine for plist, HKLM registry, and file deli ...

> ... re (themes, editor settings) * Tools and plugins you use across all projects * API keys and
authentication (stored securely) **Project scope** is best for: * Team-shared settings (permissions,
hooks, MCP servers) * Plugins the whole team should have * Standardizing tooling across
collaborators **Local scope** is best for: * Personal overrides for a specific project * T ...

> ... ude/settings.json` instead. Before v2.1.142, project settings could set `auto`. The
`--permission-mode` CLI flag overrides this setting for a single session | `"acceptEdits"` | |
`disableBypassPermissionsMode` | Set to `"disable"` to prevent `bypassPermissions` mode from being
activated. This disables the `--dangerously-skip-permissions` command-line flag. Typically placed in
[managed ...

> ... d entry is stripped and the valid subset is enforced. A wholly invalid value is dropped with a
warning, since denying every server would block servers the policy never named. | |
`sandbox.credentials` | {/* min-version: 2.1.191 */}An individual invalid entry in `files` or
`envVars` is stripped with a warning and the valid subset is enforced. A wholly invalid `crede ...

> ... ettings) * Tools and plugins you use across all projects * API keys and authentication (stored
securely) **Project scope** is best for: * Team-shared settings (permissions, hooks, MCP servers) *
Plugins the whole team should have * Standardizing tooling across collaborators **Local scope** is
best for: * Personal overrides for a specific project * Testing confi ...

Potential config terms not found in local tool files:

`ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_ARTIFACT`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, `DISABLE_AUTO_COMPACT`, `DISABLE_DOCTOR_COMMAND`, `FORCE_COLOR`, `advisorModel`, `agentPushNotifEnabled`, `allowAllClaudeAiMcps`, `allowAllUnixSockets`, `allowAppleEvents`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

Maintenance review (2026-07-15): implemented the newly documented `sandbox.credentials`, `requiredMinimumVersion`, `disableSideloadFlags`, and `autoMode.classifyAllShell` controls in the tiered Claude Code configs. The remaining identifiers above are user-interface preferences, runtime overrides, or controls already proposed in PR #55. `availableModels` and `enforceAvailableModels` require an organization-approved model list, so this repository does not invent a universal allowlist.

### Claude Code: Hooks documentation

- Change type: `content-changed`
- Source URL: https://code.claude.com/docs/en/hooks.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... o three cadences: * once per session: `SessionStart` and `SessionEnd` * once per turn:
`UserPromptSubmit`, `Stop`, and `StopFailure` * on every tool call inside the agentic loop:
`PreToolUse` and `PostToolUse` The table below summarizes when each event fires. The [Hook
events](#hook-events) section documents the full input schema and decision control options for each
...

> ... * once per session: `SessionStart` and `SessionEnd` * once per turn: `UserPromptSubmit`, `Stop`,
and `StopFailure` * on every tool call inside the agentic loop: `PreToolUse` and `PostToolUse` The
table below summarizes when each event fires. The [Hook events](#hook-events) section documents the
full input schema and decision control options for each one. | Event | Whe ...

> ... idle | | `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into
context. Fires at session start and when files are lazily loaded during a session | | `ConfigChange`
| When a configuration file changes during a session | | `CwdChanged` | When the working directory
changes, for example when Claude executes a `cd` command. Useful for reactive e ...

> ... session_start" } ``` #### InstructionsLoaded decision control InstructionsLoaded hooks have no
decision control. They can't block or modify instruction loading. Use this event for audit logging,
compliance tracking, or observability. ### UserPromptSubmit Runs when the user submits a prompt,
before Claude processes it. This allows you to add additional context bas ...

> ... t`, the script would hit `exit 0` instead. Exit code 0 with no output means the hook has no
decision to report, so the tool call continues through the normal [permission
flow](/en/permissions). The hook can deny the call, but staying silent doesn't approve it. Claude
Code reads the JSON decision, blocks the tool call, and shows Claude the reason. The
[Configuration](#c ...

Potential config terms not found in local tool files:

`ANTHROPIC_MODEL`, `CLAUDE_MODEL`, `ExitPlanMode`, `PermissionDenied`, `PermissionRequest`, `allowedPrompts`, `allowed_domains`, `block-rm.sh`, `blocked_domains`, `bypass_permissions_disabled`, `continueOnBlock`, `defaultMode`, `enabledPlugins`, `hookSpecificOutput.permissionDecision`, `hookSpecificOutput.permissionDecisionReason`, `localSettings`, `mcp__brave-search`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed: this source change expands hook event and decision-schema documentation. Existing managed hook controls and audit guidance remain applicable, and the extracted identifiers are hook payload fields or examples rather than new organization policy keys.

### Claude Code: Dynamic workflows documentation

- Change type: `content-changed`
- Source URL: https://code.claude.com/docs/en/workflows.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... plete documentation index at: https://code.claude.com/docs/llms.txt > Use this file to discover
all available pages before exploring further. # Orchestrate subagents at scale with dynamic
workflows > Dynamic workflows orchestrate many subagents from a script Claude writes and you can
rerun. Use them for codebase audits, large migrations, and cross-checked research. {/* plan- ...

> ... sdk/overview). The same disable settings apply on every surface. To turn workflows off for
yourself: * Toggle Dynamic workflows off in `/config`. Persists across sessions. * Set
`"disableWorkflows": true` in `~/.claude/settings.json`. Persists across sessions. * Set
`CLAUDE_CODE_DISABLE_WORKFLOWS=1`. Read at startup, so it applies wherever you set it. To turn
workflows off ...

> ... or yourself: * Toggle Dynamic workflows off in `/config`. Persists across sessions. * Set
`"disableWorkflows": true` in `~/.claude/settings.json`. Persists across sessions. * Set
`CLAUDE_CODE_DISABLE_WORKFLOWS=1`. Read at startup, so it applies wherever you set it. To turn
workflows off for your whole organization, set `"disableWorkflows": true` in [managed
settings](/en/server-managed- ...

> ... Claude write a workflow for your task in two ways: * [Ask for a workflow](#ask-for-a-workflow-
in-your-prompt) in your prompt, either in your own words or by including the keyword `ultracode`,
and Claude writes one for the task. * [Let Claude decide with ultracode](#let-claude-decide-with-
ultracode): set `/effort ultracode` and Claude plans a workflow for every substa ...

> ... * Set `CLAUDE_CODE_DISABLE_WORKFLOWS=1`. Read at startup, so it applies wherever you set it. To
turn workflows off for your whole organization, set `"disableWorkflows": true` in [managed
settings](/en/server-managed-settings), or use the toggle on the [Claude Code admin
settings](https://claude.ai/admin-settings/claude-code) page. When workflows are disabled, the
bundled w ...

Potential config terms found upstream are already present in local tool files.

No additional config update needed: `disableWorkflows` is already tiered and documented. `CLAUDE_CODE_SUBAGENT_MODEL` is now identified as a runtime model override, not a security boundary.

### Claude Code: Claude Code changelog

- Change type: `new-source-baseline`
- Source URL: https://code.claude.com/docs/en/changelog.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... eAutoMode` in settings * Fixed the terminal freezing and keystrokes lagging while streaming
responses containing very long lists, tables, paragraphs, or code blocks * Fixed remote managed
settings from a non-interactive run (`claude -p`, the SDK) being permanently recorded as consented
without ever showing the security consent dialog * Fixed spurious prompt-injection warnin ...

> ... agents view from a session leaving overlapping ghost frames with
`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` * Fixed late-appearing `.claude/*` symlinks not being
reconciled into the sandbox deny-write list * Hardened the Agent tool against indirect prompt
injection via content a subagent read * Improved the Bash/PowerShell tool message when a command
hits its timeout ...

> ... ed `SessionStart`, `Setup`, and `SubagentStart` hooks silently hiding stderr when exiting with
code 2 - the error is now shown in the transcript * Fixed `claude --dangerously-skip-permissions
daemon ` being treated as a chat prompt instead of running the subcommand * Fixed `SendMessage`
silently misrouting when a re-spawned agent reuses a previous agent's name - the to ...

> ... ait * Fixed Claude assuming a `cd` took effect after its command was moved to the background;
the tool result now states the working directory is unchanged * Fixed plugin-provided MCP servers
being torn down when MCP servers are re-synced mid-session * Fixed plan approvals without edits
being labeled "(edited by user)" and overwriting the plan file with a stale ...

> ... bles, paragraphs, or code blocks * Fixed remote managed settings from a non-interactive run
(`claude -p`, the SDK) being permanently recorded as consented without ever showing the security
consent dialog * Fixed spurious prompt-injection warnings triggered by benign system-generated
conversation updates * Fixed the auto-updater overwriting a custom launcher script o ...

Potential config terms not found in local tool files:

`ANTHROPIC_CUSTOM_MODEL_OPTION`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_MODEL`, `ANTHROPIC_SMALL_FAST_MODEL`, `CLAUDE_CODE_ALWAYS_ENABLE_EFFORT`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_1M_CONTEXT`, `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`, `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_CRON`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, `CLAUDE_CODE_DISABLE_MOUSE`, `CLAUDE_CODE_DISABLE_MOUSE_CLICKS`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK`, `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`, `CLAUDE_CODE_ENABLE_AUTO_MODE`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL`, `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

Maintenance review (2026-07-15): the security-relevant changelog additions are covered by this update. Most extracted environment variables are developer preferences or diagnostics. Organization model restrictions should use managed `availableModels` plus `enforceAvailableModels` with a reviewed model list, not environment variables.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | content-changed | 200 | https://code.claude.com/docs/en/settings.md |
| Claude Code | Hooks documentation | content-changed | 200 | https://code.claude.com/docs/en/hooks.md |
| Claude Code | Dynamic workflows documentation | content-changed | 200 | https://code.claude.com/docs/en/workflows.md |
| Claude Desktop | Claude Desktop enterprise configuration | new-source-baseline | 200 | https://support.claude.com/en/articles/12622667-enterprise-configuration-for-claude-desktop |

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

`ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, `DISABLE_AUTO_COMPACT`, `DISABLE_DOCTOR_COMMAND`, `FORCE_COLOR`, `advisorModel`, `agentPushNotifEnabled`, `allowAllClaudeAiMcps`, `allowAllUnixSockets`, `allowAppleEvents`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

Review outcome: resolved

Added tiered managed controls for Agent View, Artifact publishing, bundled skills, claude.ai connectors, sideload flags, and file checkpoint retention. Raised the Moderate and Strict minimum to 2.1.193 so sideload enforcement is active. The remaining candidates are model, IDE, interface, or default-secure sandbox preferences. `disableClaudeAiConnectors` supersedes `allowAllClaudeAiMcps` for this repo's deny-by-default enterprise posture. The default `false` values for unrestricted Unix sockets and Apple Events remain secure without duplicating them in the minimal policy.

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

`ANTHROPIC_MODEL`, `CLAUDE_MODEL`, `ExitPlanMode`, `PermissionDenied`, `PermissionRequest`, `allowedPrompts`, `allowed_domains`, `availableModels`, `block-rm.sh`, `blocked_domains`, `bypass_permissions_disabled`, `continueOnBlock`, `defaultMode`, `enabledPlugins`, `hookSpecificOutput.permissionDecision`, `hookSpecificOutput.permissionDecisionReason`, `localSettings`, `mcp__brave-search`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

Review outcome: resolved

No additional config update is needed. These candidates are hook event names, decision payload fields, example script names, and example domains. Existing managed hook controls, permission rules, and audit guidance already govern them. Adding event-schema names to managed settings would be invalid.

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

Potential config terms not found in local tool files:

`CLAUDE_CODE_SUBAGENT_MODEL`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

Review outcome: resolved

No additional config update is needed. `CLAUDE_CODE_SUBAGENT_MODEL` is a runtime model-selection preference, not an organization security control. Moderate and Strict already set `disableWorkflows: true`, and the new `disableBundledSkills` and `disableAgentView` controls cover the related enterprise rollout surfaces.

### Claude Desktop: Claude Desktop enterprise configuration

- Change type: `new-source-baseline`
- Source URL: https://support.claude.com/en/articles/12622667-enterprise-configuration-for-claude-desktop
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> Enterprise configuration for Claude Desktop | Claude Help Center Skip to main content API Docs
Release Notes How to Get Support English Franais Deutsch Bahasa Indonesia Italiano   Portugus P
Espaol  ...

> ... rty -Path "HKLM:\SOFTWARE\Policies\Claude" -Name "isDesktopExtensionDirectoryEnabled" -Value 1
-Type DWord Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Claude" -Name "isLocalDevMcpEnabled"
-Value 1 -Type DWord Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Claude" -Name
"isClaudeCodeForDesktopEnabled" -Value 1 -Type DWord ``` Enterprise policy options Key T ...

> ... -ItemProperty -Path "HKLM:\SOFTWARE\Policies\Claude" -Name "isDesktopExtensionDirectoryEnabled"
-Value 1 -Type DWord Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Claude" -Name
"isLocalDevMcpEnabled" -Value 1 -Type DWord Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Claude"
-Name "isClaudeCodeForDesktopEnabled" -Value 1 -Type DWord ``` Enterprise policy options Key Type
Def ...

> Enterprise configuration for Claude Desktop | Claude Help Center Skip to main content API Docs
Release Notes How to Get Support English Franais Deutsch Bahasa Indonesia Italiano   Portugus P ...

Review outcome: resolved

No config update is needed. This new canonical source confirms the existing Claude Desktop MDM keys, registry path, managed-preferences domain, and update controls. The previous watcher pointed at Claude Code MCP documentation and produced invalid Desktop candidates, so it was replaced with this enterprise policy source.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

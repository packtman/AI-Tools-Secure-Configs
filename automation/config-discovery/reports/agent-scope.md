# Agent scope for this run

### Claude Code `CLAUDE_CODE_DISABLE_CRON`

- Source: Scheduled tasks documentation (`https://code.claude.com/docs/en/scheduled-tasks.md`) and environment variables (`https://code.claude.com/docs/en/env-vars.md`)
- Pin: `"1"` on Moderate and Strict managed `env`. Baseline unset.
- Why: vendor default leaves the session scheduler on. `/loop` and `CronCreate` keep using the session's shell, file, and MCP permissions between turns, including after the session is backgrounded. There is no `settings.json` key. `disableWorkflows`, `disableAgentView`, and `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` do not cover this path. Strict `disableBundledSkills` hides `/loop` but does not stop `CronCreate`. Does not stop Desktop scheduled tasks, cloud Routines, Cursor Automations, Copilot cloud agent, or GitHub Actions.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- `CLAUDE_CODE_AUTO_CONNECT_IDE` / `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`: Global-config IDE preferences, not managed settings.
- `CLAUDE_CODE_DISABLE_AGENT_VIEW` / `CLAUDE_CODE_DISABLE_ARTIFACT` / `CLAUDE_CODE_DISABLE_FAST_MODE` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW`: session overrides for keys already covered in open PRs.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: operational timing. Workflows stay off via `disableWorkflows`.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: per-server identity env vars, not allowlists.
- Background-task MCP env vars and `WaitForMcpServers`: operational.
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`: gateway compatibility pin, not a tier default (PR #67).
- `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`: session kill; `availableModels` already constrains advisor picks. Pin only if `/advisor` must be off entirely.
- `disabledMcpServers`: not the vendor key (`deniedMcpServers` / `disabledMcpjsonServers` already exist).
- Codex 0.154.0 is now stable. Experimental worktrees, TUI prefs, and GPT-6-Astra catalog entries are not admin locks. Deferred so this PR stays on the unique Claude Code cron pin.

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), `syncClaudeAiSkills` (open #90), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred), `sandbox.allowAppleEvents` (vendor default already `false`; lock later if user override becomes a measured gap).

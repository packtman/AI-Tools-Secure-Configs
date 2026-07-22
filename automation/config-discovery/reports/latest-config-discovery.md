# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Environment variables documentation | candidate-filter-changed | 200 | https://code.claude.com/docs/en/env-vars.md |

## Review Details

### Claude Code: Environment variables documentation

- Change type: `candidate-filter-changed`
- Source URL: https://code.claude.com/docs/en/env-vars.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... --bare` mode or [`autoMemoryEnabled: false`](/docs/en/settings#available-settings) would
otherwise disable it. When disabled, Claude does not create or load auto memory files | |
`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Set to `1` to disable all background task functionality,
including the `run_in_background` parameter on Bash and subagent tools, auto-backgrounding, and the
Ctrl+B shortcut | | ...

> ... _ALLOWLIST_ENV` | Set to `1` to spawn stdio MCP servers with only a safe baseline environment
plus the server's configured `env`, instead of inheriting your shell environment | |
`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` | {/* min-version: 2.1.212 */}Elapsed time in milliseconds
before a still-running MCP tool call [moves to a background task](/docs/en/mcp#automatic-
backgrounding-of-long-tool-cal ...

> ... ion reaches the model's context limit. The override can only lower the threshold, so values
above the default have no effect. Applies to both main conversations and subagents | |
`CLAUDE_AUTO_BACKGROUND_TASKS` | Set to `1` to force-enable automatic backgrounding of long-running
agent tasks. When enabled, subagents are moved to the background after running for approximately two
minutes. ...

> ... ocs/en/scheduled-tasks). The `/loop` skill and cron tools become unavailable and any already-
scheduled tasks stop firing, including tasks that are already running mid-session | |
`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Set to `1` to strip Anthropic-specific `anthropic-beta`
request headers and beta tool-schema fields (such as `defer_loading` and `eager_input_streaming`)
from API requests. Use ...

> ... sitive whole number with no upper bound. Anything else is ignored and the default applies, so
the cap can be raised but not turned off. Requires Claude Code v2.1.212 or later | |
`CLAUDE_CODE_MCP_ALLOWLIST_ENV` | Set to `1` to spawn stdio MCP servers with only a safe baseline
environment plus the server's configured `env`, instead of inheriting your shell environment | |
`CLAUDE_CODE_MC ...

Potential config terms found upstream are already present in local tool files.

Review resolution:

- Added `CLAUDE_CODE_MCP_ALLOWLIST_ENV=1` to every tier so stdio MCP servers receive only a safe baseline plus explicitly configured variables.
- Added `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=0` to Moderate and `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` to Strict.
- Left `CLAUDE_AUTO_BACKGROUND_TASKS` unset because force-enabling automatic work in non-interactive sessions is not an enterprise-safe default.
- Documented `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` as a conditional gateway compatibility switch, not a general tier control.
- Replaced the soft enterprise `minimumVersion` updater floor with `requiredMinimumVersion=2.1.212`, which blocks older clients that cannot enforce the new MCP behavior.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

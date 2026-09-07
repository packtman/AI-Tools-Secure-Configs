# Agent scope for this run

### Claude Code `disableClaudeAiConnectors`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and MCP documentation (`https://code.claude.com/docs/en/mcp.md`)
- Pin: `true` on Moderate and Strict. Baseline unset.
- Why: vendor default `false` fetches claude.ai account MCP connectors even when `managed-mcp.json` is not deployed. `allowManagedMcpServersOnly` does not cover this path. Leave `allowAllClaudeAiMcps` unset. Session env `ENABLE_CLAUDEAI_MCP_SERVERS=false` is a one-session kill, not a substitute. Requires Claude Code v2.1.182+.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- `CLAUDE_CODE_AUTO_CONNECT_IDE` / `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`: Global-config IDE preferences, not managed settings.
- `CLAUDE_CODE_DISABLE_AGENT_VIEW` / `CLAUDE_CODE_DISABLE_ARTIFACT` / `CLAUDE_CODE_DISABLE_FAST_MODE` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW`: session overrides for keys already covered in open PRs.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: operational timing. Workflows stay off via `disableWorkflows`.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: per-server identity env vars, not allowlists.
- Background-task MCP env vars and `WaitForMcpServers`: operational.
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`: gateway compatibility pin, not a tier default (PR #67).
- `disabledMcpServers`: not the vendor key (`deniedMcpServers` / `disabledMcpjsonServers` already exist).
- Codex 0.152.0 is now stable. `tools.update_plan.enabled` defaulted off in that release; deferred so this PR stays on the unique Claude Code connector pin. Do not pin 0.152 alpha leftovers.

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred).

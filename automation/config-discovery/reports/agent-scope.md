# Agent scope for this run

### Claude Code Desktop Browser pane

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and Desktop documentation (`https://code.claude.com/docs/en/desktop`)
- Pin: Moderate `browserExternalPageTools: "disabled"`. Strict `disableBrowserExternalNavigation: true`. Baseline unset.
- Why: vendor default is unset, so Claude can fetch attacker-controlled pages or send session data from the Desktop Browser pane. Moderate keeps human browsing and blocks agent-driven page tools. Strict also blocks people, including Claude in Chrome allowlisted sites. Managed only. The terminal CLI ignores both keys. Localhost previews keep working. No env-var substitute. Only JSON boolean `true` turns `disableBrowserExternalNavigation` on (the string `"true"` is ignored). Distinct from `WebFetch`, Cursor browser tools, Copilot web search, and Claude Desktop MDM.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels`.
- Remaining `CLAUDE_CODE_*` / `DISABLE_*` names: session UX, telemetry, or one-session kills for keys already pinned.
- `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`: session thinking UX toggle, not a browsing lock.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: per-server identity env vars, not allowlists.
- `disabledMcpServers`: not the vendor key (`deniedMcpServers` / `disabledMcpjsonServers` already exist).

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred), `disableMobileSimulatorTools` (next unique Desktop follow-up), `sshHostAllowlist` (org-specific host patterns), `cleanupPeriodDays` (open #105), `permissions.blockReadsOutsideWorkingDirectories` (open #104).

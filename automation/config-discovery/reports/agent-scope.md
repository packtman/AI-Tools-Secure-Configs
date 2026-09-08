# Agent scope for this run

### Claude Code `disableMobileSimulatorTools`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and Desktop documentation (`https://code.claude.com/docs/en/desktop`)
- Pin: `true` on Moderate and Strict. Baseline unset.
- Why: vendor default is unset, so Claude can tap, screenshot, and capture devices in the Desktop iOS Simulator pane, including staging app data and auth tokens. Managed only. People keep manual use of the pane. The terminal CLI ignores this key. Only the JSON boolean `true` takes effect (the string `"true"` is ignored). Distinct from computer use, from Desktop Browser pane keys (open PR #108), and from Claude Desktop MDM. No env-var substitute.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION`: session model picks, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- `CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`: notification UX toggle, not a hook lock.
- Remaining `CLAUDE_CODE_DISABLE_*` env vars: session UX or one-session kills already covered in open PRs.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: runtime labels, not allowlists.
- `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`: session thinking UX toggle.
- Codex `tui.disable_paste_burst` / `features.context_management.experimental_mode`: TUI or experimental prefs, not admin locks.
- `mcp-tunnels-2026-05-19`: covered by open PR #70.

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred), Desktop Browser pane keys (open #108), `sshHostAllowlist` (org-specific host patterns), `cleanupPeriodDays` (open #105), `permissions.blockReadsOutsideWorkingDirectories` (open #104).

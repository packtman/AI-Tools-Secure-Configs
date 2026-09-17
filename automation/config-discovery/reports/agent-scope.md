# Agent scope for this run

### Claude Code `sandbox.enableWeakerNestedSandbox`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and Sandboxing documentation (`https://code.claude.com/docs/en/sandboxing`)
- Pin: `false` on Moderate and Strict. Baseline unset.
- Why: vendor default is already `false`, but Any-file scope means user, project, or CLI `--settings` can set `true`. That bind-mounts the container's existing `/proc` and exposes process information that a fresh mount would hide. Vendor docs call this a considerable weakening of Linux sandbox isolation. Managed `false` is the lock. No env-var substitute. JSON boolean `false` only. Linux and WSL2 only.
- Safe equivalent: enable unprivileged user namespaces, run on the host, or use a container that can mount `/proc`. Do not set `true`.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels`.
- `sandbox.enableWeakerNetworkIsolation`: open PR #117 (macOS trustd sibling).
- `sandbox.allowAppleEvents`: open PR #116.
- `CLAUDE_CODE_AUTO_CONNECT_IDE` / `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`: Global-config IDE preferences, not this pin.
- `CLAUDE_CODE_DISABLE_AGENT_VIEW` / `CLAUDE_CODE_DISABLE_ARTIFACT` / `CLAUDE_CODE_DISABLE_FAST_MODE` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW`: session overrides for keys already covered in open PRs.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: operational timing. Workflows stay off via `disableWorkflows`.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: per-server identity env vars, not allowlists.
- Background-task MCP env vars and `WaitForMcpServers`: operational.
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`: gateway compatibility pin, not a tier default (PR #67).
- `disabledMcpServers`: not the vendor key (`deniedMcpServers` / `disabledMcpjsonServers` already exist).

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred), Copilot `failIfUnavailable` / `allowLocalNetwork` / `keychainAccess` (open #113-#115), Copilot `addCurrentWorkingDirectory: false` (needs org-specific path grants), Codex Appshots / remote control (open #112), Codex `browser_use.allow_history_access` (deferred so this PR stays unique), Gemini `security.disableAlwaysAllow` / `admin.mcp.config` (wait for #64+#76).

# Agent scope for this run

### Claude Code `sandbox.network.allowAllUnixSockets`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and Sandboxing documentation (`https://code.claude.com/docs/en/sandboxing`)
- Pin: `false` on Moderate and Strict. Baseline unset.
- Why: vendor default is already `false`, but Any-file scope means user, project, or CLI `--settings` can set `true`. On Linux and WSL2 this is the only permit path (seccomp cannot inspect socket paths). On WSL2, `true` also reopens the interop socket that launches `cmd.exe` and `powershell.exe`. Docker, SSH-agent, D-Bus, and X11 sockets can bypass the sandbox. Managed `false` is the lock. No env-var substitute. JSON boolean `false` only.
- Safe equivalent: run the named tool in a normal terminal, or add that command to `sandbox.excludedCommands`. Do not set `true`. Do not pin an org-specific `allowUnixSockets` path list in this template.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels`.
- `sandbox.network.allowLocalBinding`: open PR #119 (macOS localhost TCP bind sibling).
- `sandbox.enableWeakerNestedSandbox`: open PR #118 (Linux/WSL2 `/proc` sibling).
- `sandbox.enableWeakerNetworkIsolation`: open PR #117 (macOS trustd sibling).
- `sandbox.allowAppleEvents`: open PR #116.
- `sandbox.network.allowUnixSockets`: macOS path list only. Org-specific. Arrays merge across scopes, so an empty managed list is not a lock. Not pinned in this template.
- `CLAUDE_CODE_AUTO_CONNECT_IDE` / `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`: Global-config IDE preferences, not this pin.
- `CLAUDE_CODE_DISABLE_AGENT_VIEW` / `CLAUDE_CODE_DISABLE_ARTIFACT` / `CLAUDE_CODE_DISABLE_FAST_MODE` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW`: session overrides for keys already covered in open PRs.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: operational timing. Workflows stay off via `disableWorkflows`.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: per-server identity env vars, not allowlists.
- Background-task MCP env vars and `WaitForMcpServers`: operational.
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`: gateway compatibility pin, not a tier default (PR #67).
- `disabledMcpServers`: not the vendor key (`deniedMcpServers` / `disabledMcpjsonServers` already exist).

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred), Copilot `failIfUnavailable` / `allowLocalNetwork` / `keychainAccess` (open #113-#115), Copilot `addCurrentWorkingDirectory: false` (needs org-specific path grants), Codex Appshots / remote control (open #112), Codex `browser_use.allow_history_access` (deferred so this PR stays unique), Gemini `security.disableAlwaysAllow` / `admin.mcp.config` (wait for #64+#76).

# Agent scope for this run

### Claude Code `sandbox.allowAppleEvents`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and Sandboxing documentation (`https://code.claude.com/docs/en/sandboxing`)
- Pin: `false` on Moderate and Strict. Baseline unset.
- Why: vendor default is already `false`, but user or CLI settings can set `true` and remove code-execution isolation. Sandboxed commands can then launch other applications unsandboxed with no prompt and send AppleScript to running apps such as Terminal (TCC still applies). Project settings cannot enable this key. Managed `false` is the lock. There is no env-var substitute. JSON boolean `false` only. macOS only; Windows and Linux ignore the key.
- Distinct from `allowUnsandboxedCommands` (escape hatch for all commands) and from Copilot CLI `sandbox.userPolicy.seatbelt.keychainAccess` (open PR #113). Cursor sandbox policy does not cover Claude Code Apple Events.
- Safe equivalent: add a named command to `excludedCommands` so it runs outside the sandbox with a prompt. Do not set `allowAppleEvents: true`.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- `CLAUDE_CODE_AUTO_CONNECT_IDE` / `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`: Global-config IDE preferences, not managed settings.
- `CLAUDE_CODE_DISABLE_AGENT_VIEW` / `CLAUDE_CODE_DISABLE_ARTIFACT` / `CLAUDE_CODE_DISABLE_FAST_MODE` / `CLAUDE_CODE_AUTO_COMPACT_WINDOW`: session overrides for keys already covered in open PRs.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: operational timing. Workflows stay off via `disableWorkflows`.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: per-server identity env vars, not allowlists.
- Background-task MCP env vars and `WaitForMcpServers`: operational.
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`: gateway compatibility pin, not a tier default (PR #67).
- `disabledMcpServers`: not the vendor key (`deniedMcpServers` / `disabledMcpjsonServers` already exist).
- Copilot `failIfUnavailable` / `allowLocalNetwork` / `keychainAccess` (open #113-#115).
- Codex Appshots / remote control (open #112).
- Codex `browser_use.allow_history_access` deferred so this PR stays on the unique Claude Code Apple Events pin.

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), `enableWeakerNetworkIsolation` / `enableWeakerNestedSandbox` (vendor default already `false`; pin later if user override is a measured gap), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred), Copilot `addCurrentWorkingDirectory: false` (needs org-specific path grants).

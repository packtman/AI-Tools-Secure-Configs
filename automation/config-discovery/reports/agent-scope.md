# Agent scope for this run

### Claude Code `enableAllProjectMcpServers`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and MCP documentation (`https://code.claude.com/docs/en/mcp.md`)
- Pin: `false` on Moderate and Strict. Baseline unset.
- Why: vendor default is unset (ask per server), but Any-file scope means a repo `.claude/settings.json`, user settings, `--settings`, or the approval dialog ("approve all") can set `true` and skip review. Managed `false` is the lock in a trusted folder. Distinct from `allowManagedMcpServersOnly` (locks `allowedMcpServers` only). Distinct from `disableClaudeAiConnectors` (claude.ai account connectors). Distinct from `enabledMcpjsonServers` / `disabledMcpjsonServers` (org-specific name lists). No env-var substitute. JSON boolean `false` only.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- `allowUnixSockets`: org-specific macOS path list. Arrays merge across scopes, so an empty template is not a lock.
- `allowMachLookup`: org-specific XPC / Mach service list. Same merge rule. Do not pin `[]`.
- `sandbox.filesystem.disabled`: User or managed. Current Moderate/Strict templates already configure `sandbox.filesystem`, which restricts this key to managed settings. Deferred so this PR stays unique.
- `sandbox.credentials.allowPlaintextInject`: User or managed default `false`. Deferred so this PR stays unique.
- Copilot `addCurrentWorkingDirectory: false`: needs org-specific path grants.
- Copilot `failIfUnavailable` / `allowLocalNetwork` / `keychainAccess` (open #113-#115).
- Codex Appshots / remote control (open #112).
- Codex `browser_use.allow_history_access` (wait for #96+#112).
- Gemini `security.disableAlwaysAllow` / `admin.mcp.config` (wait for #64+#76).
- `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88).

Did not add: `allowAllUnixSockets` (open #120), `allowLocalBinding` (open #119), `enableWeakerNestedSandbox` (open #118), `enableWeakerNetworkIsolation` (open #117), `allowAppleEvents` (open #116).

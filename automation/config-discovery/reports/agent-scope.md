# Agent scope for this run

### GitHub Copilot `sandbox.userPolicy.network.allowLocalNetwork`

- Source: Enterprise managed settings reference (`https://docs.github.com/en/copilot/reference/enterprise-managed-settings-reference`)
- Pin: `false` on Moderate and Strict. Baseline unset.
- Why: for Copilot CLI sandbox capability settings, managed `false` prohibits the capability. Omitting the key leaves the user's setting, so loopback and LAN stay reachable from the sandbox. Distinct from `gitAuth` / `ghAuth` (those only block Copilot-injected GitHub tokens), from Claude Code `sandbox.network`, from Codex network requirements, and from Cursor MCP network modes. Do not pin `allowOutbound: false` in this template (that blocks npm and git remotes).

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- Remaining `CLAUDE_CODE_DISABLE_*` env vars: session UX, already-covered keys, or one-session kills.
- `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL`: per-server identity env vars, not allowlists.
- `sandbox.addCurrentWorkingDirectory: false`: would block workspace writes without org-specific path grants.
- `sandbox.userPolicy.network.allowOutbound: false`: blocks npm, git remotes, and package registries.
- `sandbox.userPolicy.seatbelt.keychainAccess`: open PR #113 pins this separately.

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), Gemini `security.disableAlwaysAllow` / `admin.mcp.config` (wait for #64+#76), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred).

# Agent scope for this run

### Claude Code `sandbox.filesystem.disabled`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`) and sandboxing docs (`https://code.claude.com/docs/en/sandboxing`)
- Pin: `false` on Moderate and Strict (including the default managed drop-in and `sandbox-config.json`). Baseline unset.
- Why: vendor default is already `false`, but User settings and `--settings` can set `true` unless managed settings configure `sandbox.filesystem`. A `true` value skips filesystem isolation, so `denyRead` and `credentials.files` deny entries are not enforced, while network isolation stays on. Pinning `false` is the value lock and the who lock. Requires Claude Code v2.1.216+. JSON boolean `false` only. Do not set `true`.
- Complementary: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` independently ignores `disabled` from every source. It is not a substitute for the managed JSON lock.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- `enableAllProjectMcpServers`: open PR #121.
- `allowAllUnixSockets`: open PR #120.
- `allowLocalBinding`: open PR #119.
- `enableWeakerNestedSandbox`: open PR #118.
- `enableWeakerNetworkIsolation`: open PR #117.
- `allowAppleEvents`: open PR #116.
- `allowUnixSockets` / `allowMachLookup`: org-specific arrays; empty is not a lock.
- `sandbox.credentials.allowPlaintextInject`: deferred so this PR stays unique.
- `disableSideloadFlags`: open PR #61.
- `pluginSuggestionMarketplaces`: wait for #88.
- Copilot `failIfUnavailable` / `allowLocalNetwork` / `keychainAccess`: open PRs #113-#115.
- Copilot `addCurrentWorkingDirectory: false`: needs org-specific path grants.
- Codex Appshots / remote control: open PR #112.
- Codex `browser_use.allow_history_access`: deferred so this PR stays unique.
- Gemini `security.disableAlwaysAllow` / `admin.mcp.config`: wait for #64+#76.

Did not add: `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `allowedHttpHookUrls` / `requiredMaximumVersion` (still deferred).

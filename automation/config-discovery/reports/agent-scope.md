# Agent scope for this run

### GitHub Copilot `sandbox.failIfUnavailable`

- Source: Enterprise managed settings reference (`https://docs.github.com/en/copilot/reference/enterprise-managed-settings-reference`)
- Pin: `true` on Moderate and Strict. Baseline unset.
- Why: force-on setting. Managed `true`, with `sandbox.enabled: true`, blocks model and tool execution when Copilot cannot validate, compile, or enforce the sandbox backend. `enabled: true` alone can still fall through to unsandboxed commands if Seatbelt, the Linux backend, or policy compile fails. Managed `false` or omit leaves the user's setting. This property does not enable sandboxing by itself.
- Distinct from Claude Code `sandbox.failIfUnavailable` (different client). Distinct from Copilot `gitAuth` / `ghAuth` / `allowDevToolAccess`. Distinct from open PRs #113 (`userPolicy.seatbelt.keychainAccess`) and #114 (`userPolicy.network.allowLocalNetwork`). Those keys do not fail-close a missing backend.

## No config update needed (scoped missing terms)

- Copilot `sandbox.userPolicy.network.allowOutbound: false`: blocks npm, git remotes, and package registries. Do not pin in this template.
- Copilot `sandbox.addCurrentWorkingDirectory: false`: needs org-specific path grants.
- Copilot `userPolicy.seatbelt.keychainAccess`: open PR #113.
- Copilot `userPolicy.network.allowLocalNetwork`: open PR #114.
- Claude Code `disableSideloadFlags`: open #61.
- Claude Code `pluginSuggestionMarketplaces`: wait for #88.
- Gemini `security.disableAlwaysAllow` / `admin.mcp.config`: wait for #64+#76.
- Tabnine system settings: open #65.

Did not add: `allowOutbound`, `addCurrentWorkingDirectory`, Keychain, local-network, `disableSideloadFlags`, `pluginSuggestionMarketplaces`.

# Agent scope for this run

### GitHub Copilot `sandbox.userPolicy.seatbelt.keychainAccess`

- Source: Enterprise managed settings reference (`https://docs.github.com/en/copilot/reference/enterprise-managed-settings-reference`)
- Pin: `false` on Moderate and Strict. Baseline unset.
- Why: vendor docs treat capability settings as "managed false prohibits the capability; omit leaves the user's setting." The macOS Keychain holds cloud tokens, certificates, and Wi-Fi secrets. `gitAuth` / `ghAuth` only block Copilot-injected GitHub tokens. Windows and Linux ignore this Seatbelt key.
- Distinct from Claude Code `sandbox.credentials`, Codex `[permissions.filesystem]`, and open Copilot PR #86 (MCP/plugins).

## No config update needed (scoped missing terms)

- `desktopSessionCleanupPeriodDays`: when managed settings set `cleanupPeriodDays` (open #105), Claude Code ignores this Desktop-only key.
- `skipDangerousModePermissionPrompt`: `false` equals unset. `disableBypassPermissionsMode` already blocks bypass mode.
- `sandbox.enableWeakerNetworkIsolation` / `enableWeakerNestedSandbox`: vendor default `false`. Defer unless project-file override becomes a measured gap.
- `sandbox.allowAppleEvents`: vendor default `false`. Deferred.
- Gemini `security.disableAlwaysAllow` / `admin.mcp.config`: wait to reconcile after #64 and #76 merge.
- `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88).
- Codex Appshots / device remote control (open #112).
- `addCurrentWorkingDirectory`: pinning `false` would block workspace writes unless org-specific path grants exist. Not a repo template.

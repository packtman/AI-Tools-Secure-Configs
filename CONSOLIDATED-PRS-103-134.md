# Consolidated security controls: PRs #103-#134

This branch consolidates the effective security-policy changes from the open draft PRs created in the last month.

## Included source PRs

- Claude Code: #103, #104, #105, #108, #109, #110, #111, #116, #117, #118, #119, #120, #121, #122, #123
- Codex: #112, #124, #125, #126, #127, #128, #129, #130, #131, #132, #133, #134
- GitHub Copilot: #113, #114, #115

PRs #106 and #107 are excluded because they are already merged into main.

## Consolidation approach

The source PRs repeatedly modify the same generated documentation, discovery reports, snapshots, and rollout prose. Replaying those stale snapshots would create conflicts and regress newer main-branch state.

This consolidation keeps the net admin/security controls in the deployable policy examples and rollout configs, while de-duplicating overlapping generated artifacts.

### Claude Code controls

- switchModelsOnFlag = false
- permissions.blockReadsOutsideWorkingDirectories = true
- cleanupPeriodDays = 30 (Moderate), 7 (Strict)
- browserExternalPageTools = "disabled" (Moderate)
- disableBrowserExternalNavigation = true (Strict)
- disableMobileSimulatorTools = true
- wslInheritsWindowsSettings = true
- CLAUDE_CODE_DISABLE_CRON = 1
- sandbox.allowAppleEvents = false
- sandbox.enableWeakerNetworkIsolation = false
- sandbox.enableWeakerNestedSandbox = false
- sandbox.network.allowLocalBinding = false
- sandbox.network.allowAllUnixSockets = false
- enableAllProjectMcpServers = false
- sandbox.filesystem.disabled = false
- sandbox.credentials.allowPlaintextInject = false

### GitHub Copilot controls

- sandbox.failIfUnavailable = true
- sandbox.userPolicy.seatbelt.keychainAccess = false
- sandbox.userPolicy.network.allowLocalNetwork = false

### Codex controls

- allow_appshots = false
- allow_remote_control = false
- browser_use.allow_history_access = false
- browser_use.allow_global_persistent_approval = false
- browser_use.disable_auto_review = true
- computer_use.allow_persistent_approval = false
- features.in_app_local_automation = false
- in_app_browser.allow_external_browser_settings_import = false
- features.in_app_dictation = false
- features.realtime_conversation = false
- features.in_app_chat = false
- browser_use.default_origin_policy.persistent_approval = false
- browser_use.default_origin_policy.uploads = "deny"

## Review note

This PR is intended to replace the open draft PRs listed above after review and merge.

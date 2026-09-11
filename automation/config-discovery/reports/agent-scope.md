# Agent scope for this run

### Codex Desktop `allow_appshots` and `allow_remote_control`

- Source: Managed configuration (`https://developers.openai.com/codex/enterprise/managed-configuration`) and config reference (`allow_appshots`, `allow_remote_control`)
- Pin: `false` on Moderate and Strict. Baseline unset.
- Why: omitted keys are unconstrained. Appshots captures the frontmost Mac window (image plus available text) into ChatGPT. Device remote control lets another client drive this device's Codex session. These keys belong in `requirements.toml` only, not `config.toml`. Distinct from Computer Use, Browser Use, Claude Code `disableRemoteControl`, and Copilot `remoteControl.mode`. Does not disable SSH. Deploy one shared `requirements.toml` for Desktop, CLI, and the IDE extension.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists.
- Remaining `CLAUDE_CODE_DISABLE_*` env vars: session UX, already-covered keys, or one-session kills.
- `maxEffortLevel` / `fastModePerSessionOptIn`: cost and Fast-mode UX. `disableWorkflows` already removes ultracode on Moderate and Strict. `fastMode: false` already covers Fast mode.
- `allow_browser_and_computer_use`: duplicative of existing `[features] browser_use` / `computer_use` pins.
- Codex 0.155.0 is still alpha. Do not pin alpha leftovers.

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), WSL inheritance (open #110), Desktop Browser pane (open #108), Desktop iOS Simulator (open #109), session scheduled tasks (open #111), `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion` (still deferred), `sandbox.allowAppleEvents` (vendor default already `false`; lock later if user override becomes a measured gap).

# Agent scope for this run

### Claude Code `wslInheritsWindowsSettings`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`)
- Pin: `true` on Moderate and Strict in the Windows managed file or HKLM. Baseline unset.
- Why: vendor default `false` means WSL reads only `/etc/claude-code` and ignores Windows MDM. That leaves a Windows-MDM fleet looking compliant while WSL runs without the same deny rules, MCP lock, or login pin. Managed only. Honored only in HKLM or `C:\Program Files\ClaudeCode\` (Windows admin). Server-managed settings ignore this key. No effect on native Windows, macOS, or native Linux. No env-var substitute. JSON boolean `true` only. Distinct from `parentSettingsBehavior` (open PR #83) and `policyHelper` (open PR #85).

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- Remaining `CLAUDE_CODE_DISABLE_*` env vars: session UX or one-session kills already covered by dedicated keys in open PRs, or gateway compatibility (`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, PR #67).
- `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`: session kill for the experimental advisor. `availableModels` already constrains advisor picks. Defer a managed `env` pin unless an org must disable `/advisor` entirely.
- `desktopSessionCleanupPeriodDays`: ignored when managed settings set `cleanupPeriodDays` (open PR #105).
- `sshHostAllowlist`: org-specific host patterns; an empty array disables SSH. Not a repo template.
- Codex TUI prefs (`tui.auto_recap`, `tui.disable_paste_burst`, `features.context_management.experimental_mode`): not admin locks.

Did not add: `disableSideloadFlags` (open #61), `pluginSuggestionMarketplaces` (wait for #88), Desktop Browser pane (open #108), Desktop iOS Simulator tools (open #109), `managedSourcesBehavior` (`first-wins` is already the vendor default), `httpHookAllowedEnvVars` / `allowedHttpHookUrls` (arrays merge across files), `requiredMaximumVersion` / `requiredMinimumVersion` (org-specific version bounds).

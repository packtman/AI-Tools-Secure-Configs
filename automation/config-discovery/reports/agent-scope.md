# Agent scope for this run

Completed 2026-10-14: pin Codex `features.browser_use_external = false` on Baseline, Moderate, and Strict `requirements.toml`.

- Source: `https://developers.openai.com/codex/config-reference` and `https://developers.openai.com/codex/enterprise/managed-configuration`, fetched 2026-10-14.
- Vendor default is enabled. Omitting the key allows external Browser Use (ChatGPT browser extension, including already signed-in tabs). `features.browser_use = false` does not cover that path.
- Requirements pin only. Do not copy it into `config.toml` or `managed_config.toml`.
- Stable since 2026-04-30 (commit `719431d`). Present in Codex 0.162.1.
- Watcher: added `browser_use_external` to the existing Codex Desktop `codex-rs/config.md` `watch_for`. Did not replace that URL (open #96). Registry stays 14 tools / 31 sources.

## Do not re-add

- `disableClaudeAiConnectors`: already on main.
- Cursor `readBoundary` (open #144), Codex `allowed_sandbox_implementations` (#143), `feedback.enabled` (#142), `cli_auth_credentials_store` (#141), origin-policy keys through #140, `computer_use.default_app_access` (#138).
- `features.browser_use_full_cdp_access` (open #137). `features.fast_mode`, `features.goals`, `features.skill_mcp_dependency_install`, `allow_login_shell` (open #92).
- `features.plugins`, `features.remote_plugin`, `features.plugin_sharing`, marketplace allowlists (open #87).
- `allow_managed_hooks_only` (open #60, Strict).
- Do not set `default_origin_policy.access = "deny"`. Do not pin `windows.allow_mxc = false`, `allow_browser_and_computer_use`, `allowed_login_methods`, `features.guardian_approval = false`, or an empty `application.network` domain map.

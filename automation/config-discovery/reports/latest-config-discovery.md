# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Codex Desktop | OpenAI Codex config schema | new-source-baseline | 200 | https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json |
| Codex Desktop | OpenAI Codex advanced configuration | new-source-baseline | 200 | https://developers.openai.com/codex/config-advanced.md |
| Codex Desktop | OpenAI Codex managed configuration | new-source-baseline | 200 | https://developers.openai.com/codex/enterprise/managed-configuration.md |

## Review Details

### Codex Desktop: OpenAI Codex config schema

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> ... n": "Collection of common configuration options that a user can define as a unit in
`config.toml`.", "properties": { "analytics": { "$ref": "#/definitions/AnalyticsConfigToml" },
"approval_policy": { "$ref": "#/definitions/AskForApproval" }, "approvals_reviewer": { "$ref":
"#/definitions/ApprovalsReviewer" }, "chatgpt_base_url": { "type": "string" },
"experimental_compact_ ...

> ... osity" }, "oss_provider": { "type": "string" }, "personality": { "$ref":
"#/definitions/Personality" }, "plan_mode_reasoning_effort": { "$ref":
"#/definitions/ReasoningEffort" }, "sandbox_mode": { "$ref": "#/definitions/SandboxMode" },
"service_tier": { "description": "Optional explicit service tier request id for new turns (for
example `default`, `priority`, or `flex`; ...

> ... num": [ "none", "friendly", "pragmatic" ], "type": "string" }, "PluginConfig": {
"additionalProperties": false, "properties": { "enabled": { "default": true, "type": "boolean" },
"mcp_servers": { "additionalProperties": { "$ref": "#/definitions/PluginMcpServerConfig" },
"description": "Per-MCP-server policy overlays for MCP servers contributed by this plugin.", "type":
...

> ... asoning effort for spawned subagents when the spawn call does not select one." }, "enabled": {
"description": "Whether multi-agent tools are enabled. Defaults to true. An enabled
`features.multi_agent_v2` setting takes precedence.", "type": "boolean" }, "interrupt_message": {
"description": "Whether to record a model-visible message when an agent turn is interrupted ...

> ... pproving or denying the request. The legacy value `guardian_subagent` is accepted for
compatibility.", "enum": [ "user", "auto_review", "guardian_subagent" ], "type": "string" },
"AppsConfigToml": { "additionalProperties": { "$ref": "#/definitions/AppConfig" }, "description":
"App/connector settings loaded from `config.toml`.", "properties": { "_default": { "all ...

Potential config terms not found in local tool files:

`McpServerConfig`, `ModelProviderInfo`, `auto_review`, `enabled_tools`, `mcp__`, `mcp_oauth_callback_port`, `memory_mode`, `model-with-reasoning`, `model_auto_compact_token_limit`, `model_providers`, `request_permissions`, `with_additional_permissions`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Codex Desktop: OpenAI Codex advanced configuration

- Change type: `new-source-baseline`
- Source URL: https://developers.openai.com/codex/config-advanced.md
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> # Advanced Configuration > For the complete documentation index, see
[llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are
available by appending `.md` to the ...

> ... y key. Examples: ```shell # Dedicated flag codex --model gpt-5.6-terra # Generic key/value
override (value is TOML, not JSON) codex --config model='"gpt-5.6-terra"' codex --config
sandbox_workspace_write.network_access=true codex --config
'shell_environment_policy.include_only=["PATH","HOME"]' ``` Notes: - Keys can use dot notation to
set nested values (for example ...

> ... vel config keys in the profile file; don't nest them under `[profiles.profile-name]`. ```toml #
~/.codex/deep-review.config.toml model = "gpt-5.5" model_reasoning_effort = "xhigh" approval_policy
= "on-request" model_catalog_json = "/Users/me/.codex/model-catalogs/deep-review.json" ``` ```shell
codex --profile deep-review codex exec --profile deep-review "review thi ...

> ... estrictions still apply. Add request headers when needed: ```toml [model_providers.example]
http_headers = { "X-Example-Header" = "example-value" } env_http_headers = { "X-Example-Features" =
"EXAMPLE_FEATURES" } ``` Use command-backed authentication when a provider needs Codex to fetch
bearer tokens from an external credential helper: ```toml [model_providers.proxy ...

> ... rkspace_write.network_access=true codex --config
'shell_environment_policy.include_only=["PATH","HOME"]' ``` Notes: - Keys can use dot notation to
set nested values (for example, `mcp_servers.context7.enabled=false`). - `--config` values are
parsed as TOML. When in doubt, quote the value so your shell doesn't split it on spaces. - If the
value can't be parsed a ...

Potential config terms not found in local tool files:

`apps_mcp_product_sku`, `auth_mode`, `feature_enabled`, `guardian_policy_config`, `mcp.call`, `mcp.call.duration_ms`, `mcp.tools.cache_write.duration_ms`, `mcp.tools.fetch_uncached.duration_ms`, `mcp.tools.list.duration_ms`, `model_catalog_json`, `model_instructions_file`, `model_provider`, `model_providers`, `model_verbosity`, `model_warning`, `read_allowed`, `remote_models.fetch_update.duration_ms`, `remote_models.load_cache.duration_ms`, `request_permissions`, `thread.skills.enabled_total`, `tmp_mem_enabled`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Codex Desktop: OpenAI Codex managed configuration

- Change type: `new-source-baseline`
- Source URL: https://developers.openai.com/codex/enterprise/managed-configuration.md
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> # Managed configuration > For the complete documentation index, see
[llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are
available by appending `.md` ...

> ... `.md` to the page URL. Managed configuration controls supported local runtime behavior for
covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension. Supported
requirements can differ by client and version. Managed configuration doesn't grant ChatGPT workspace
access, assign seats, or replace workspace role-based access control (RBAC). Use [Roles and ...

> ... managed requirements delivered in the cloud config bundle. 3. Legacy `managed_config.toml`
fields that the local client reinterprets as requirements. 4. macOS managed preferences (MDM)
delivered through `com.openai.codex:requirements_toml_base64`. Higher-precedence layers override
ordinary scalar and list values from lower layers. Tables merge by key, while req ...

> # Managed configuration > For the complete documentation index, see
[llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are
available by appending `.md` to the ...

> ... BAC). Use [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-
workspace-permissions) for workspace feature access and this page for local runtime policy.
Enterprise admins can control supported local client behavior in two ways: - **Requirements**:
admin-enforced constraints that users can't override. - **Managed defaults**: start ...

Potential config terms not found in local tool files:

`allowAppshots`, `allow_appshots`, `allow_remote_control`, `allowed_approvals_reviewers`, `allowed_domains`, `allowed_permission_profiles`, `default_permissions`, `guardian_policy_config`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

## Maintenance agent notes (2026-08-10)

### Claude Code: Managed settings documentation

Applied config update in this PR:
- Pinned `parentSettingsBehavior: "first-wins"` on Moderate and Strict so IDE/Agent SDK parent managed settings are dropped when admin MDM or file-based managed settings are present.
- Enabled `sandbox.network.strictAllowlist: true` on Strict only (requires Claude Code v2.1.219+), paired with existing `allowManagedDomainsOnly: true`.
- Raised Moderate `minimumVersion` to `2.1.133` and Strict to `2.1.219`.
- Baseline leaves both keys unset.

Skipped discovery noise for this run:
- `ANTHROPIC_MODEL` / `CLAUDE_MODEL` / `CLAUDE_CODE_SUBAGENT_MODEL`: model selection prefs, not admin security pins for this repo.
- IDE/agent env terms (`CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, artifact/checkpoint/bundled-skill disables): deferred to avoid duplicating open PRs #66/#68.

### Codex Desktop: config schema / advanced / managed-configuration

No additional config update in this PR beyond repairing discovery watchers (replaced moved `codex-rs/config.md` stub with schema + advanced + managed-configuration docs).

Missing-term candidates map to controls already covered or deferred by open PRs:
- `auto_review` / `guardian_policy_config` / `allowed_approvals_reviewers` → open #78
- Apps / connector defaults → open #79
- `in_app_updates` and related Desktop requirements → open #77
- Broader CLI 0.146 requirements (`plugins`, `remote_plugin`, `plugin_sharing`) → open #72
- Remaining unique 0.147 follow-ups (`recommended_plugins`, `plugin_hooks`, `--approve-for-me`) deferred to a later run after #72 merges

### Continue.dev / Claude Desktop / OpenAI Platform

No config update needed in this run:
- Continue `mcpServers` empty-pin work is already in open #75.
- Claude Desktop `CLAUDE_CODE_MCP_SERVER_*` names are runtime env noise for MCP process identity, not admin managed settings.
- OpenAI Platform OpenAPI schema terms remain deferred noise pending a focused Platform PR.


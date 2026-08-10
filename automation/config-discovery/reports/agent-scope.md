# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools to process (3 of 3 with missing terms)

### Codex Desktop

- Source: OpenAI Codex config schema
- Missing terms: `McpServerConfig`, `ModelProviderInfo`, `auto_review`, `enabled_tools`, `mcp__`, `mcp_oauth_callback_port`, `memory_mode`, `model-with-reasoning`, `model_auto_compact_token_limit`, `model_providers`, `request_permissions`, `with_additional_permissions`

### Codex Desktop

- Source: OpenAI Codex advanced configuration
- Missing terms: `apps_mcp_product_sku`, `auth_mode`, `feature_enabled`, `guardian_policy_config`, `mcp.call`, `mcp.call.duration_ms`, `mcp.tools.cache_write.duration_ms`, `mcp.tools.fetch_uncached.duration_ms`, `mcp.tools.list.duration_ms`, `model_catalog_json`, `model_instructions_file`, `model_provider`, `model_providers`, `model_verbosity`, `model_warning`
- (6 more terms in the full report)

### Codex Desktop

- Source: OpenAI Codex managed configuration
- Missing terms: `allowAppshots`, `allow_appshots`, `allow_remote_control`, `allowed_approvals_reviewers`, `allowed_domains`, `allowed_permission_profiles`, `default_permissions`, `guardian_policy_config`

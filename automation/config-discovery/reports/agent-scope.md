# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools to process (4 of 7 with missing terms)

### Claude Code

- Source: Managed settings documentation
- Missing terms: `ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_ARTIFACT`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`

### Claude Code

- Source: Hooks documentation
- Missing terms: `ANTHROPIC_MODEL`, `CLAUDE_MODEL`

### Claude Code

- Source: Dynamic workflows documentation
- Missing terms: `CLAUDE_CODE_SUBAGENT_MODEL`

### Codex Desktop

- Source: OpenAI Codex config schema
- Missing terms: `McpServerConfig`, `ModelProviderInfo`, `enabled_tools`, `mcp__`, `mcp_oauth_callback_port`, `memory_mode`, `model-with-reasoning`, `model_auto_compact_token_limit`, `model_providers`, `request_permissions`, `with_additional_permissions`

## Deferred (3 tools)

These tools also have missing terms but are deferred to a follow-up run:

- Codex Desktop (OpenAI Codex advanced configuration)
- Claude Desktop (Claude Desktop MCP documentation)
- OpenAI Platform (OpenAI OpenAPI schema)

# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools to process (4 of 4 with missing terms)

### Claude Code

- Sources:
  - Managed settings documentation: `ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_ARTIFACT`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`
  - Hooks documentation: `ANTHROPIC_MODEL`, `CLAUDE_MODEL`
- Combined missing terms: `ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_ARTIFACT`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, `CLAUDE_MODEL`

### Continue.dev

- Sources:
  - Configuration reference: `mcpServers`
- Combined missing terms: `mcpServers`

### Claude Desktop

- Sources:
  - Claude Desktop MCP documentation: `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`
- Combined missing terms: `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`

### Claude API

- Sources:
  - Anthropic admin API documentation: `fast-mode-2026-02-01`, `mcp-tunnels-2026-05-19`, `model_group`
  - Anthropic API release notes: `LanguageModel`, `LanguageModelSession`, `fast-mode-2026-02-01`, `mcp_oauth`, `model_context_window_exceeded`
- Combined missing terms: `fast-mode-2026-02-01`, `mcp-tunnels-2026-05-19`, `model_group`, `LanguageModel`, `LanguageModelSession`, `mcp_oauth`, `model_context_window_exceeded`

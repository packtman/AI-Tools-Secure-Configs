# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools to process (4 of 6 with missing terms)

### Claude Code

- Source: Managed settings documentation
  - Missing terms: `--fallback-model`, `--permission-mode`, `--settings`, `--teammate-mode`, `ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, `allowLocalBinding`, `allowUnixSockets`
- Source: Hooks documentation
  - Missing terms: `--allow-dangerously-skip-permissions`, `--permission-mode`, `ANTHROPIC_MODEL`, `CLAUDE_MODEL`, `PermissionDenied`, `PermissionRequest`, `localSettings`, `mcp_server_name`, `my-mcp-server`, `permission_mode`, `permission_prompt`, `permission_suggestions`

### Codex CLI

- Source: OpenAI Codex releases
  - Missing terms: `codex-windows-sandbox-setup`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe.tar.gz`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe.zip`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe.zst`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe.tar.gz`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe.zip`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe.zst`

### Continue.dev

- Source: Configuration reference
  - Missing terms: `mcpServers`

### Google Gemini

- Source: Vertex AI Gemini safety settings
  - Missing terms: `BLOCKED_REASON_UNSPECIFIED`, `blockReason`, `safetySettings`

## Deferred (2 tools)

These tools also have missing terms but are deferred to a follow-up run:

- Claude Desktop (Claude Desktop MCP documentation)
- OpenAI Platform (OpenAI OpenAPI schema)

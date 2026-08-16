# Agent scope for this run

Processed Codex CLI and Codex Desktop for Codex 0.147 Agent Plugins, marketplace allowlists, and `--approve-for-me`.

Other tools with missing-term noise (`ANTHROPIC_MODEL`, Continue `mcpServers`, Claude Desktop MCP env vars, OpenAI Platform schema terms) were deferred: they are not new admin controls, or they are already covered by open draft PRs.

## Tools processed

### Codex CLI

- Source: OpenAI Codex releases rust-v0.147.0 (2026-08-07) and managed configuration docs
- Added: `requirements-{strict,moderate,baseline}.toml`, plugin feature pins, `[marketplaces]`, `allowed_approvals_reviewers`

### Codex Desktop

- Source: same managed configuration docs (CLI and Desktop share `requirements.toml`)
- Added: the same 0.147 pins on existing requirements and config templates

## Deferred

- Claude Code env vars and hook terms: developer/runtime, not new managed-settings keys for this run; covered by open PRs #66/#68/#80-#85
- Continue.dev `mcpServers`: already handled in open PR #75
- Claude Desktop `CLAUDE_CODE_MCP_SERVER_*`: Claude Code MCP env, not Desktop MDM keys; covered by #70
- OpenAI Platform OpenAPI schema terms: API event names, not org-policy keys; covered by #69
- GitHub Copilot managed-settings MCP/plugins: open PR #86
- Gemini CLI console templates: reconcile #64 and #76 after merge

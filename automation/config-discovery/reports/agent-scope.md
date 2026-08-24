# Agent scope for this run

This run applied a unique Codex 0.149.0+ config update instead of duplicating open Claude Code PRs.

Process notes:

1. Claude Code missing terms (`ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_MODEL`, `CLAUDE_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`) are session overrides. Org allowlisting is open PR #89. No pin.
2. `CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS` disables audit Notification hooks in Desktop/VS Code hosts. Leave unset.
3. `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS` is a timing knob. No pin.
4. Claude Desktop `CLAUDE_CODE_*` terms are Claude Code env vars, not Desktop config keys. No pin.
5. Continue `mcpServers` is open PR #75. No pin.
6. Unique work: pin Codex `fast_mode`, `goals`, `skill_mcp_dependency_install`, `allow_appshots`, `allow_remote_control`, and `allow_login_shell`. Repair the Desktop config-reference watcher.

## Applied this run

### Codex CLI and Codex Desktop

- Source: OpenAI Codex config reference (`https://developers.openai.com/codex/config-reference`)
- Pins: `features.fast_mode`, `features.goals`, `features.skill_mcp_dependency_install`, `allow_appshots`, `allow_remote_control`, `allow_login_shell`
- Did not pin: `features.plugins`, `remote_plugin`, `plugin_sharing`, `[marketplaces]` (open PR #87)

## Deferred

- OpenAI Platform OpenAPI schema event names
- Claude Code `pluginSuggestionMarketplaces` (pair with marketplace PR #88 after merge)
- `disableSideloadFlags` (open PR #61)

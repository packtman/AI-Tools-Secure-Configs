# Agent scope for this run

Unique pin applied: Claude Code `switchModelsOnFlag: false` on Moderate and Strict.

Missing-term review (no additional pins this run):

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `ANTHROPIC_CUSTOM_MODEL_OPTION` / `CLAUDE_MODEL`: session picks, not allowlists
- Remaining `CLAUDE_CODE_DISABLE_*` env vars: one-session kills for keys already in open PRs, or local prefs
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: timing pref, not a security control

Deferred to a later run: Codex CLI paste-burst keys, Claude Desktop MCP session env vars, OpenAI Platform API event schema names.

# Agent scope for this run

Processed on 2026-07-25 for branch `cusor/automated-ai-config-rollout-710d`.

## Completed in this run

### Codex Desktop

- Added Codex 0.138.0+ permission-profile requirements, remote-control/Appshots controls, managed-hooks-only, and Strict experimental network allowlist.
- Updated managed defaults, rationale, enterprise policy, README, and discovery watchers.

### OpenAI Platform

- Added hosted tool permissions, model permissions, API call logging modes, container/shell network allowlist, checkpoint sharing, and retention fields across all tiers.
- Documented Admin API and dashboard deployment plus tier deltas.

### Continue.dev

- Added explicit empty `mcpServers: []` to tier and enterprise example configs.

## Deferred

### Claude Code

- Missing agent/IDE/artifact/away-summary terms are already handled in open PR #68. Avoid duplicate edits on this branch.

### Claude Desktop

- Missing terms are Claude Code MCP helper env vars from a shared docs URL. No Claude Desktop config keys to add.

### Claude API

- Release-note terms such as `fast-mode-2026-02-01` and `mcp_oauth` deferred to a later scoped run.

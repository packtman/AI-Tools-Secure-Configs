# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools processed this run

### Codex Desktop

- Source: OpenAI Codex config schema / config advanced docs
- Action: Pinned `features.in_app_updates` (requirements-only, stable, default on upstream) in Baseline/Moderate/Strict requirements; updated rollout, MDM, rationale, and CLI overlap notes; replaced moved `codex-rs/config.md` watcher with schema + advanced docs (14 tools / 30 sources).

## Intentionally skipped (duplicate open PRs or non-admin noise)

- Claude Code IDE/model env vars (`ANTHROPIC_MODEL`, `CLAUDE_CODE_*` UX flags): not admin managed-settings pins (see #66/#68).
- Codex CLI release terms `McpConnectionSet`, `McpRuntime`, `forceRefetch`: runtime reconnect helpers, not requirements keys (see #72).
- OpenAI Platform `project.model_permissions` / `data_retention` / hosted tools: covered by open PR #69.
- Claude Desktop / Claude API tunnels and custom roles: covered by open PR #70.
- Gemini Management Console: covered by open PR #76.

## Deferred follow-ups

- Codex Desktop `auto_review` / `approvals_reviewer` and remaining permission-profile schema terms after #69 merges.
- Reconcile local Gemini settings (#64) with Management Console templates (#76) if both land.
- Claude Managed Agents Dreams research-preview governance when org-level disable controls ship.

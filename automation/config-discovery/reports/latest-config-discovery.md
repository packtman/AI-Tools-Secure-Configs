# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Cursor | MCP documentation | fingerprint-method-changed | 200 | https://docs.cursor.com/en/tools/mcp |

## Review Details

### Cursor: MCP documentation

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.cursor.com/en/tools/mcp
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

Keyword snippets:

> Cursor Docs - Agent, Rules, MCP, Skills & CLI Skip to main content Cursor Logo Docs API Learn Help
Search docs... K Sign in Download Command Palette Search for a command to run... Get Started Welcome
Quickstart ...

> ... Palette Search for a command to run... Get Started Welcome Quickstart Models & Pricing Changelog
Agent Overview Agents Window Agent Review Planning Prompting Debugging Design Mode Tools Security
Grok Bot Overview Get Started Use Cases Work with Grok Bot Settings Teams and Enterprise Customize
Overview Plugins Rules Skills Subagents Hooks MCP Cloud Agents Overview ...

> ... ugins Rules Skills Subagents Hooks MCP Cloud Agents Overview Setup Builds Capabilities Best
Practices Choose Where Cloud Agents Run Automations Bugbot Security Agents PR Routing & Approval
Mobile Security Self-Hosted Machines Settings API Origin Overview CLI Create a repository Clone,
Push & Pull Mirror GitHub Pull requests Browse & Search Settings Codebase settings ...

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

## Config update applied this run

Pinned unique Claude Code control `switchModelsOnFlag: false` on Moderate and Strict (Baseline unset). Vendor default is `true`: a safety classifier flag auto-continues on a fallback model. Any-file scope. No environment-variable substitute. Do not pin `CLAUDE_CODE_DISABLE_REFUSAL_FALLBACK`. Distinct from `availableModels` (open #89) and from `disableAutoMode`. Covers Claude Code only. Requires v2.1.170+.

Added watcher `code.claude.com/docs/en/settings-reference.md`. Registry: 14 tools / 30 sources. Consecutive live scan after Cursor MCP recovered from a transient SSL error: `no upstream source changes detected`.

## No config update needed

Scanner missing terms reviewed and not pinned in this unique PR:

- `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_MODEL`, `ANTHROPIC_CUSTOM_MODEL_OPTION`, `CLAUDE_MODEL`: session or picker values, not org allowlists. Model allowlists stay in open #89 (`availableModels` / `enforceAvailableModels`).
- Remaining `CLAUDE_CODE_DISABLE_*` and `CLAUDE_CODE_*` env vars in the settings-reference missing list: one-session kills or local UI prefs for keys already in open PRs (#80 autocompact, #93 Fast mode, #98 Artifact) or not admin-tier defaults.
- `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, `CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`: local IDE or notify prefs, not managed threat controls.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: timing pref, not a security control. Workflows stay disabled via `disableWorkflows` on Moderate/Strict.
- Cursor MCP HTML: no new admin control in the recovered 200 snapshot. Dashboard MCP allowlists stay in open #73.
- Deferred: Codex CLI paste-burst / experimental context keys (UX), Claude Desktop MCP session env vars, OpenAI Platform API event schema names.

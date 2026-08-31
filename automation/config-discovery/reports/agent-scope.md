# Agent scope for this run

Processed one unique Claude Code admin control that is not in open PRs #61 through #98.

## Applied

### Claude Code `feedbackDrafts`

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`)
- Pin: `"off"` on Moderate and Strict. Baseline unset.
- Why: vendor default `"notify"` lets Claude queue SendFeedback drafts that may include session content. User or managed only. Distinct from telemetry and from the session-quality survey.

## No config update needed (scoped missing terms)

- `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_MODEL` / `CLAUDE_MODEL`: model-selection env vars, not org allowlists. Do not pin as a substitute for `availableModels` (open PR #89).
- `CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`: session notify switch, not a durable managed lock.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: operational timing. Moderate and Strict already pin `disableWorkflows: true`.
- Other `CLAUDE_CODE_*` names in the settings-reference missing-term list: session overrides, UX toggles, or Global-config IDE preferences. Dedicated keys already exist in open PRs where they are admin controls.

## Deferred

- Claude Desktop MCP env vars
- OpenAI Platform OpenAPI schema terms
- `disableSideloadFlags` (open #61)
- `pluginSuggestionMarketplaces` (wait for #88)
- `managedSourcesBehavior` / `httpHookAllowedEnvVars` / `requiredMaximumVersion`

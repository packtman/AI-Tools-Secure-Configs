# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation if you want the end result to be a PR with real config updates, not only a discovery report.

GitHub Actions acts as the sensor. Cursor Cloud acts as the config-maintenance agent.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run.
- Optional PR trigger: run when a PR from `automation/config-maintenance` is opened or updated, especially when the workflow notes that `ANTHROPIC_API_KEY` was unavailable.
- Repository: this repo.
- Branch: `automation/config-maintenance` when that branch exists, otherwise the default branch.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for an open config maintenance PR or branch named automation/config-maintenance.
2. Read automation/config-discovery/reports/agent-scope.md first and process only the scoped tools.
3. Read automation/config-discovery/reports/latest-config-discovery.md for details on those tools.
4. For each changed upstream source in scope, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
5. Pay special attention to "Potential config terms not found in local tool files."
6. If a real control changed or was added, update the affected tool's tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
7. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
8. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
9. Do not create a report-only PR. The PR should contain actual config changes when a relevant control changed.
10. If no config change is needed, update the report with a short "No config update needed" explanation for each changed source.
11. Validate edited JSON, YAML, TOML, and shell files using AGENTS.md.
12. Commit and push the branch.

Use automation/config-discovery/agent-prompt.md as the detailed policy for how to write config updates.
```

## Expected Result

For a vendor change such as Claude Code adding dynamic workflows, the agent should:

- Add the new managed setting to the Claude Code tier files.
- Set secure values by tier, for example Baseline allows local experimentation, Moderate and Strict disable the research-preview workflow mode.
- Update JSONC, deployable JSON, rationale docs, tier delta tables, and workflow-preservation notes.
- Push a PR that reviewers can merge as an actual config update.

## Why This May Require Cursor Automation

The discovery scanner is intentionally dependency-free. The GitHub workflow can run the maintenance agent when `ANTHROPIC_API_KEY` is configured, but it opens a discovery-only PR when that secret is unavailable. Cursor Automation is the fallback path that turns the same discovery report into reviewed tiered config changes.

# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation if you want the end result to be a PR with real config updates, not only a discovery report.

GitHub Actions acts as the sensor. Cursor Cloud acts as the config-maintenance agent.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run.
- Repository: this repo.
- Branch: default branch for scheduled runs. If a discovery handoff PR already exists, run against that PR branch.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for open config maintenance PRs with branches matching `automation/config-maintenance-*`.
2. Read automation/config-discovery/reports/latest-config-discovery.md.
3. Read automation/config-discovery/reports/agent-scope.md and process only the scoped tools.
4. For each changed upstream source, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
5. Pay special attention to "Potential config terms not found in local tool files."
6. If a real control changed or was added, update the affected tool's tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
7. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
8. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
9. Do not leave a report-only PR when a relevant control changed. The PR should contain actual config changes.
10. If no config change is needed, update the report with a short "No config update needed" explanation for each scoped source.
11. Validate edited JSON, YAML, TOML, and shell files with `python3 scripts/validate_config_files.py --changed`.
12. Commit and push the branch.

Use automation/config-discovery/agent-prompt.md as the detailed policy for how to write config updates.
```

## When GitHub Actions Opens a Handoff PR

The GitHub workflow opens a handoff PR when `ANTHROPIC_API_KEY` is missing or unavailable. That PR is still useful: it contains the changed upstream source fingerprints, the reviewer report, and the scoped work list. Run this Cursor Automation against the handoff PR branch to convert it into a config-update PR.

## Expected Result

For a vendor change such as Claude Code adding dynamic workflows, the agent should:

- Add the new managed setting to the Claude Code tier files.
- Set secure values by tier, for example Baseline allows local experimentation, Moderate and Strict disable the research-preview workflow mode.
- Update JSONC, deployable JSON, rationale docs, tier delta tables, and workflow-preservation notes.
- Push a PR that reviewers can merge as an actual config update.

## Why This May Require Cursor Automation

The scanner step can detect source changes and identify candidate config terms, but it cannot safely decide the tier policy for a brand-new vendor control. When the GitHub-hosted maintenance agent is unavailable, Cursor Automation provides the AI review step that turns a discovery handoff PR into a config-update PR.

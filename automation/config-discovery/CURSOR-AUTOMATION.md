# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation when the GitHub workflow opens a discovery handoff PR or when you want Cursor to perform the final config-maintenance review.

GitHub Actions acts as the sensor. If `ANTHROPIC_API_KEY` is configured, the workflow also runs the Claude Code maintenance agent. If that secret is missing or the agent cannot finish, Cursor Cloud acts as the config-maintenance agent.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run, or trigger on discovery handoff PRs.
- Repository: this repo.
- Branch: the open `automation/config-maintenance-*` PR branch when one exists, otherwise the default branch.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for an open config maintenance PR or branch named `automation/config-maintenance-*`.
2. Read automation/config-discovery/reports/latest-config-discovery.md.
3. Read automation/config-discovery/reports/agent-scope.md and process only the scoped tools.
4. For each scoped changed upstream source, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
5. Pay special attention to "Potential config terms not found in local tool files."
6. If a real control changed or was added, update the affected tool's strict, moderate, and baseline tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
7. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
8. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
9. Do not create a report-only PR when a relevant control changed.
10. If no config change is needed, update the report with a short "No config update needed" explanation for each changed source.
11. Validate edited JSON, YAML, TOML, and shell files using `python3 scripts/validate_config_files.py --changed`.
12. Commit and push the branch.

Use automation/config-discovery/agent-prompt.md as the detailed policy for how to write config updates.
```

## Expected Result

For a vendor change such as Claude Code adding dynamic workflows, the agent should:

- Add the new managed setting to the Claude Code tier files.
- Set secure values by tier, for example Baseline allows local experimentation, Moderate and Strict disable the research-preview workflow mode.
- Update JSONC, deployable JSON, rationale docs, tier delta tables, and workflow-preservation notes.
- Push a PR that reviewers can merge as an actual config update.

## Why Cursor Automation Is Useful

The scheduled workflow can detect source changes and, when configured with `ANTHROPIC_API_KEY`, run the inline maintenance agent. Cursor Automation remains useful as a fallback for discovery handoff PRs, for agent failures such as turn limits, and for security review of brand-new vendor controls.

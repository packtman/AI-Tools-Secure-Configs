# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation if you want the end result to be a PR with real config updates, not only a discovery report.

GitHub Actions acts as the sensor. Cursor Cloud acts as the config-maintenance agent when the workflow cannot run the model step itself, for example because `ANTHROPIC_API_KEY` is unavailable.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run.
- Repository: this repo.
- Branch: a discovery handoff branch named `automation/config-maintenance-<run_id>`, or the default branch if no handoff PR exists.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for an open config maintenance PR or branch named `automation/config-maintenance-*`.
2. Read automation/config-discovery/reports/latest-config-discovery.md.
3. For each changed upstream source, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
4. Pay special attention to "Potential config terms not found in local tool files."
5. If a real control changed or was added, update the affected tool's tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
6. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
7. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
8. Do not create a report-only PR. The PR should contain actual config changes when a relevant control changed.
9. If no config change is needed, update the report with a short "No config update needed" explanation for each changed source.
10. Validate edited JSON, YAML, TOML, and shell files using AGENTS.md or `python3 scripts/validate_config_files.py --changed`.
11. Commit and push the branch.

Use automation/config-discovery/agent-prompt.md as the detailed policy for how to write config updates.
```

## Expected Result

For a vendor change such as Claude Code adding dynamic workflows, the agent should:

- Add the new managed setting to the Claude Code tier files.
- Set secure values by tier, for example Baseline allows local experimentation, Moderate and Strict disable the research-preview workflow mode.
- Update JSONC, deployable JSON, rationale docs, tier delta tables, and workflow-preservation notes.
- Push a PR that reviewers can merge as an actual config update.

## Why This Requires Cursor Automation

The discovery scanner is intentionally dependency-free and can detect source changes, identify candidate config terms, and open a handoff PR. It cannot safely decide the tier policy for a brand-new vendor control on its own. That security decision needs the GitHub-hosted model step, Cursor Automation, or a human reviewer.

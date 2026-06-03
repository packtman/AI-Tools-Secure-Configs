# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation if you want the end result to be a PR with real config updates, not only a discovery report.

GitHub Actions acts as the sensor. If repository secret `ANTHROPIC_API_KEY` is configured, the workflow can also run the built-in config-maintenance agent. Cursor Cloud is still useful as a fallback when that secret is unavailable, or as the preferred agent if you want maintenance decisions to run in Cursor.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run.
- Repository: this repo.
- Branch: default branch, unless your automation service creates a working branch automatically.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for an open config maintenance PR or branch named automation/config-maintenance.
2. Continue from that branch if it exists, do not start from the default branch and overwrite the intake PR.
3. Read automation/config-discovery/reports/agent-scope.md first.
4. Read automation/config-discovery/reports/latest-config-discovery.md for source details on the scoped tools.
5. For each changed upstream source in scope, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
6. Pay special attention to "Potential config terms not found in local tool files."
7. If a real control changed or was added, update the affected tool's tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
8. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
9. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
10. Do not create a report-only PR. The PR should contain actual config changes when a relevant control changed.
11. If no config change is needed, update the report with a short "No config update needed" explanation for each changed source.
12. Validate edited JSON, YAML, TOML, and shell files with `python3 automation/config-discovery/validate_repo_configs.py`.
13. Commit and push the branch.

Use automation/config-discovery/agent-prompt.md as the detailed policy for how to write config updates.
```

## Expected Result

For a vendor change such as Claude Code adding dynamic workflows, the agent should:

- Add the new managed setting to the Claude Code tier files.
- Set secure values by tier, for example Baseline allows local experimentation, Moderate and Strict disable the research-preview workflow mode.
- Update JSONC, deployable JSON, rationale docs, tier delta tables, and workflow-preservation notes.
- Push a PR that reviewers can merge as an actual config update.

## Why Cursor Automation Is Still Useful

The scanner itself is dependency-free and only detects source changes plus candidate config terms. It cannot safely decide the tier policy for a brand-new vendor control. That security decision needs the built-in Claude Code action, a Cursor Cloud automation, or a human reviewer.

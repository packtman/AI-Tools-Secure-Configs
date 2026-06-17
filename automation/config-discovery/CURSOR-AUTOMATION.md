# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation if you want Cursor to be the config-maintenance agent that turns discovery signals into PRs with real config updates.

GitHub Actions can run the default Claude Code maintenance agent from `.github/workflows/config-discovery.yml`. Cursor Cloud is the recommended alternate agent when you want the same review loop to run in Cursor, or when you do not want to store an Anthropic API key in GitHub Actions.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run.
- Repository: this repo.
- Branch: `automation/config-maintenance` when it exists, otherwise the default branch.
- Expected PR branch: `automation/config-maintenance` or Cursor's generated automation branch.
- If the discovery workflow has not produced a fresh report, run the discovery scanner first and commit the report before reviewing configs.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for an open config maintenance PR or branch named automation/config-maintenance.
2. Read automation/config-discovery/reports/agent-scope.md first. Process only the tools listed there.
3. Read automation/config-discovery/reports/latest-config-discovery.md for the scoped tools.
4. For each changed upstream source, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
5. Pay special attention to "Potential config terms not found in local tool files."
6. If a real control changed or was added, update the affected tool's tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
7. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
8. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
9. Do not create a report-only PR when a relevant control changed. The PR should contain the actual config and documentation updates.
10. If no config change is needed, update the report with a short "No config update needed" explanation for each scoped source.
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

## Why This Requires Cursor Automation

The GitHub workflow is intentionally dependency-free and does not call a model API. It can detect source changes and identify candidate config terms, but it cannot safely decide the tier policy for a brand-new vendor control. That security decision needs an AI maintenance agent or a human reviewer.

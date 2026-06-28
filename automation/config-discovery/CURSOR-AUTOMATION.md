# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation when the GitHub workflow opens a discovery handoff PR, or when you prefer Cursor to perform the final config-maintenance review.

GitHub Actions acts as the sensor. If repository secret `ANTHROPIC_API_KEY` is configured, the workflow also runs the Claude Code action as the config-maintenance agent. If that secret is missing or a reviewer wants a second pass, Cursor Cloud can act as the config-maintenance agent using this prompt.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run.
- Repository: this repo.
- Branch: the open `automation/config-maintenance-<run_id>` PR branch, or the default branch if your automation service creates a working branch automatically.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for an open config maintenance PR or branch named `automation/config-maintenance-<run_id>`.
2. Read automation/config-discovery/reports/latest-config-discovery.md.
3. Read automation/config-discovery/reports/agent-scope.md and process only the tools listed there.
4. For each scoped changed upstream source, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
5. Pay special attention to "Potential config terms not found in local tool files."
6. If a real control changed or was added, update the affected tool's tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
7. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
8. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
9. Do not create a report-only PR when a relevant control changed. The final PR should contain actual config changes for real controls.
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

## Why Cursor Automation Is Still Useful

The deterministic scanner can detect source changes and identify candidate config terms, but it cannot safely decide the tier policy for a brand-new vendor control. That security decision needs an AI maintenance agent or a human reviewer. Cursor Automation is the fallback when the GitHub workflow cannot run the Claude Code action, and it is also useful for a second-pass review of complex vendor changes.

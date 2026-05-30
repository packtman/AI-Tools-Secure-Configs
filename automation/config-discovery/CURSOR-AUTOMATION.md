# Cursor Automation Setup

Use this prompt for an optional Cursor Cloud scheduled automation if you want a second agent to review discovery PRs, or if GitHub Actions does not have the `ANTHROPIC_API_KEY` secret needed to run the built-in config-maintenance agent.

GitHub Actions acts as the sensor and, when configured with the model API key, also runs the config-maintenance agent. Cursor Cloud can act as a fallback or additional review agent on the same PR branch.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run, or manually after a discovery PR appears.
- Repository: this repo.
- Branch: default branch, unless your automation service creates a working branch automatically.

## Prompt

```text
You are maintaining AI-Secure-Configs.

Goal: keep hardened AI tool configs current across Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, and Claude API.

Process:

1. Check for an open config maintenance PR or branch named automation/config-maintenance.
2. Read automation/config-discovery/reports/latest-config-discovery.md.
3. For each changed upstream source, open the upstream source and identify real admin, managed-settings, permission, privacy, sandbox, network, MCP, audit, retention, identity, or content-exclusion controls.
4. Pay special attention to "Potential config terms not found in local tool files."
5. If a real control changed or was added, update the affected tool's tier files, rationale docs, README, rollout guide, deployment paths, validation steps, and workflow-preservation notes.
6. Keep deployable JSON valid. If comments are needed, update JSONC and companion .comments.md files.
7. Do not add secrets, tokens, org IDs, team IDs, tenant IDs, or production hostnames.
8. Do not create a report-only PR. The PR should contain actual config changes when a relevant control changed.
9. If no config change is needed, update the report with a short "No config update needed" explanation for each changed source.
10. Validate edited JSON, YAML, TOML, and shell files using AGENTS.md.
11. Commit and push the branch.

Use automation/config-discovery/agent-prompt.md as the detailed policy for how to write config updates.
```

## Expected Result

For a vendor change such as Claude Code adding dynamic workflows, the agent should:

- Add the new managed setting to the Claude Code tier files.
- Set secure values by tier, for example Baseline allows local experimentation, Moderate and Strict disable the research-preview workflow mode.
- Update JSONC, deployable JSON, rationale docs, tier delta tables, and workflow-preservation notes.
- Push a PR that reviewers can merge as an actual config update.

## When to Use Cursor Automation

Use Cursor automation when:

- GitHub Actions cannot access `ANTHROPIC_API_KEY`.
- You want a separate agent review before merging generated config changes.
- A discovery PR contains only snapshots and a report, and a human wants an agent to complete the rollout-engineering review.

The source-change signal alone is not enough to merge. A human or AI maintenance agent must decide whether the upstream change is a real admin control, then update tiered configs, rationale, rollout impact, deployment paths, validation steps, and workflow-preservation notes.

# Cursor Automation Setup

Use this prompt for a Cursor Cloud scheduled automation if you want Cursor to create the final PR with real config updates.

GitHub Actions can run the integrated maintenance agent itself, but Cursor Cloud is a good fit when you want Cursor to own the agent run, credentials, commits, and PR branch. In that mode, GitHub Actions acts as the sensor and Cursor Cloud acts as the config-maintenance agent.

## Recommended Trigger

- Schedule: daily, after `.github/workflows/config-discovery.yml` has run.
- Repository: this repo.
- Branch: `automation/config-maintenance` when the GitHub workflow produced a discovery PR, otherwise the default branch.

## GitHub Workflow Pairing

If Cursor Cloud will be the only maintenance agent, run the GitHub workflow with `run_maintenance_agent: false`. That produces a report-only PR for Cursor to review. If the integrated GitHub agent is enabled, do not also schedule Cursor against the same branch unless you intentionally want a second review pass.

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

## Why This Requires Cursor Automation

The discovery scanner is dependency-free and can identify candidate config terms, but it cannot safely decide the tier policy for a brand-new vendor control. That security decision needs an AI maintenance agent or a human reviewer. Use this Cursor automation when you do not want the integrated GitHub workflow to run the maintenance agent.

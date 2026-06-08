# Config Discovery Automation

This directory contains the scheduled automation that watches upstream AI tool sources and opens a pull request when a source changes in a way that may affect the hardened configs in this repo.

The goal is not to dump every vendor setting into the repo. The goal is to create an end-to-end maintenance loop: source change detection, config coverage analysis, agent review, focused config edits, validation, and a PR that contains the actual hardened config update.

## Files

| File | Purpose |
|------|---------|
| `tool-sources.json` | Curated watch list of official docs, changelogs, and repositories for each supported tool. |
| `discover_configs.py` | Dependency-free scanner that fingerprints sources, extracts likely config terms, and writes a PR report when a source changes. |
| `agent-prompt.md` | Instructions for the config-maintenance agent that turns discovery reports into config and documentation updates. |
| `CURSOR-AUTOMATION.md` | Copy/paste setup prompt for a Cursor Cloud scheduled automation that produces final config-update PRs. |
| `state/source-snapshots.json` | Persisted source fingerprints. This changes only when a watched source changes or a new source is added. |
| `reports/latest-config-discovery.md` | Latest generated discovery report for reviewers. |
| `reports/agent-scope.md` | Focused work list for the maintenance agent (max N tools per run). |
| `build_agent_scope.py` | Builds `agent-scope.md` from missing-term sections in the report. |
| `.github/workflows/config-discovery.yml` | Scheduled workflow that runs the scanner and opens or updates a PR. |

## Operating Modes

Use one of these modes:

| Mode | What runs | Secret required | Result |
|------|-----------|-----------------|--------|
| Integrated GitHub workflow | GitHub Actions runs discovery, then `anthropics/claude-code-action` reviews scoped tools. | `ANTHROPIC_API_KEY` | One open PR from `automation/config-maintenance` with source snapshots, report updates, and config edits when needed. |
| Cursor Cloud scheduled automation | GitHub Actions runs discovery, Cursor Cloud runs the prompt in `CURSOR-AUTOMATION.md`. | Cursor automation credentials, no repository model key required by this workflow | A Cursor-created branch or PR with the same config-maintenance policy. |
| Discovery only | GitHub Actions runs discovery with `run_maintenance_agent: false`. | None | A report-only PR for human or separate agent review. |

The integrated workflow is the simplest path when this repository is allowed to store an Anthropic API key as a GitHub secret. Use Cursor Cloud mode when you want Cursor to own the agent run or when model credentials are managed outside GitHub Actions.

## How the Loop Works

1. The workflow runs on the daily schedule or by manual dispatch.
2. The scanner fetches each URL in `tool-sources.json`.
3. It compares the normalized response fingerprint, HTTP status, and fetch error state with `state/source-snapshots.json`.
4. If nothing changed, the workflow exits without a commit.
5. If one or more sources changed, the scanner updates the state and writes `reports/latest-config-discovery.md`.
6. The workflow commits those files to `automation/config-maintenance` and opens or updates a discovery branch.
7. If the integrated agent is enabled, the workflow runs the scoped maintenance agent in the same workflow. If Cursor Cloud mode is enabled instead, the Cursor automation should run `agent-prompt.md` on that branch.
8. The agent reads the report, checks the upstream source, updates affected tiered configs and rollout docs, validates the files, commits the real config changes, and pushes the final PR branch.

GitHub Actions alone can detect and stage the source-change signal. It cannot safely decide the security posture for a brand-new vendor setting without an AI review step. Use either the integrated agent step or the Cursor Cloud automation prompt in this directory for the final config-update PR behavior.

## Enable the Integrated GitHub Workflow

1. In GitHub, enable Actions for this repository.
2. Set workflow permissions to **Read and write permissions** and allow Actions to create pull requests.
3. Add repository secret `ANTHROPIC_API_KEY`.
4. Confirm `.github/workflows/config-discovery.yml` is on the default branch.
5. Run **Config Discovery** from the Actions tab with:
   - `force_agent_review: true`, to test the agent even when no source changed.
   - `max_tools: 1`, to keep the first test PR small.
   - `run_maintenance_agent: true`, to produce config edits when a real control changed.
6. Review the PR from branch `automation/config-maintenance`.

The workflow preserves the existing `automation/config-maintenance` branch when a PR is already open. New scheduled runs add commits to that branch instead of replacing reviewer-visible work.

## Manual Dispatch Controls

| Input | Default | Use when |
|-------|---------|----------|
| `force_agent_review` | `false` | You want the agent to re-check the current report even if source fingerprints did not change. |
| `run_maintenance_agent` | `true` | Set to `false` for a report-only PR that a human or separate Cursor automation will review. |
| `max_tools` | `4` | Lower this when the report contains many changed tools and you want smaller PRs. |

Scheduled runs use `run_maintenance_agent: true` and `max_tools: 4`.

## Adding a Source

Add an entry to `tool-sources.json` under the relevant tool:

```json
{
  "name": "Vendor policy documentation",
  "kind": "docs",
  "url": "https://vendor.example/docs/admin-policy",
  "watch_for": [
    "policy",
    "managed settings",
    "permissions"
  ]
}
```

Use official vendor sources when possible. Prefer stable markdown, raw files, API endpoints, or pages that are specific to configuration, admin policy, managed settings, MCP, permissions, sandboxing, network controls, privacy, audit logs, or content exclusion. Avoid generic marketing pages when a reference page exists, because page chrome changes can create noisy PRs.

## Local Validation

```bash
python3 automation/config-discovery/discover_configs.py \
  --sources automation/config-discovery/tool-sources.json \
  --state automation/config-discovery/state/source-snapshots.json \
  --report automation/config-discovery/reports/latest-config-discovery.md \
  --check
```

Run an offline smoke check without network access or file writes:

```bash
python3 automation/config-discovery/discover_configs.py \
  --sources automation/config-discovery/tool-sources.json \
  --state /tmp/source-snapshots.json \
  --report /tmp/latest-config-discovery.md \
  --offline
```

## Review Standard for Generated PRs

Treat the initial discovery commit as an intake signal. The final PR should include actual config updates when the upstream change is relevant. Before changing a config:

- Read the upstream source that changed.
- Confirm the vendor setting is real and relevant to one of this repo's supported tiers.
- Update only the affected tool files.
- Keep deployable JSON valid. If rationale comments are needed, use JSONC plus stripped JSON or a `.comments.md` companion.
- Include rollout impact, deployment steps, audit logging, rollback, and workflow-preservation notes when behavior changes.
- Do not add secrets, tokens, API keys, or organization-specific identifiers.

## GitHub Permissions

The workflow needs:

- `contents: write`, to commit updated snapshots and reports.
- `pull-requests: write`, to open or update the discovery PR.

No external package registry tokens or vendor API keys are required for discovery. The maintenance agent step requires repository secret `ANTHROPIC_API_KEY`.

## Agent step failures (`error_max_turns`)

If the Claude Code action log shows `error_max_turns` with `num_turns` above the configured limit, the maintenance task was too large for one run. The workflow now:

- Builds `reports/agent-scope.md` with at most four tools that have missing local terms.
- Uses `--max-turns 60` and instructs the agent to mirror strict, moderate, and baseline per scoped tool.
- Commits partial file changes if the agent edited files before hitting the limit.
- Fails the job only when the agent errors and leaves no diff.

Re-run with `workflow_dispatch` and `force_agent_review: true` to process deferred tools on a later run.

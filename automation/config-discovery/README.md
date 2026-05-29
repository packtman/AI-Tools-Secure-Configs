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
| `.github/workflows/config-discovery.yml` | Scheduled workflow that runs the scanner and opens or updates a PR. |

## How the Loop Works

1. The workflow runs on the daily schedule or by manual dispatch.
2. The scanner fetches each URL in `tool-sources.json`.
3. It compares the response hash, HTTP status, and fetch error state with `state/source-snapshots.json`.
4. If nothing changed, the workflow exits without a commit.
5. If one or more sources changed, the scanner updates the state and writes `reports/latest-config-discovery.md`.
6. The workflow commits those files to `automation/config-maintenance` and opens or updates a discovery branch.
7. A Cursor Cloud automation should run `agent-prompt.md` on that branch. That agent reads the report, checks the upstream source, updates affected tiered configs and rollout docs, validates the files, commits the real config changes, and pushes the final PR branch.

GitHub Actions alone can detect and stage the source-change signal. It cannot safely decide the security posture for a brand-new vendor setting without an AI review step. Use the Cursor Cloud automation prompt in this directory for the final config-update PR behavior.

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

Use official vendor sources when possible. Prefer pages that are specific to configuration, admin policy, managed settings, MCP, permissions, sandboxing, network controls, privacy, audit logs, or content exclusion.

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

No external package registry tokens or vendor API keys are required.

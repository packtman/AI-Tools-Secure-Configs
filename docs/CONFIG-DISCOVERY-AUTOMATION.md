# Config Discovery Automation

This repository includes a scheduled automation that watches official vendor documentation and release feeds for AI tool configuration changes. When a watched source changes, the automation opens a pull request with:

- Updated source fingerprints in `config-discovery/source-state.json`
- A triage report in `config-discovery/reports/`
- Local files likely affected by the upstream change
- Review checklists for turning the discovery into hardened config updates

The automation is designed for rollout engineering. It finds candidate changes, then asks for a security review before any hardened tier files are changed.

## Why the scanner does not auto-edit configs

Vendor docs often describe settings before they are enforceable by MDM, before they have clear failure behavior, or before they are appropriate for every tier. Automatically copying those settings can break developer workflows or create an audit gap.

The generated PR should be used as the first step in a review loop:

1. Read the upstream source in context.
2. Decide whether the change affects Baseline, Moderate, Strict, or only documentation.
3. Update the smallest relevant set of files.
4. Keep deployable JSON valid, with JSONC or `.comments.md` for explanations.
5. Add rollout, deployment, delta table, and workflow-preservation updates when behavior changes.

## Schedule and workflow

The workflow is defined in `.github/workflows/config-discovery.yml`.

- Runs daily at 13:00 UTC
- Can be started manually with `workflow_dispatch`
- Uses Python standard library only
- Uses the repository `GITHUB_TOKEN` to raise GitHub API rate limits
- Creates or updates a pull request from `automation/config-discovery`

## Source manifest

Watched sources live in `config-discovery/sources.json`.

Each tool entry includes:

- `id`: stable tool identifier
- `name`: human-readable tool name
- `local_paths`: repository files the report should point reviewers to
- `watch_terms`: terms used to extract useful snippets from upstream text
- `sources`: official documentation pages, raw docs, or release APIs to fingerprint

Add a new source when a vendor introduces a new admin, policy, security, or release page that may affect local configs.

## Fingerprint state

The scanner stores successful source fingerprints in `config-discovery/source-state.json`. A changed SHA256 hash means the normalized upstream source text changed.

Fetch failures do not update the state file by default. This avoids noisy PRs when a vendor page is temporarily unavailable.

## Generated reports

Reports are written to `config-discovery/reports/YYYY-MM-DD-config-source-changes.md`.

Each report includes:

- Changed source table
- Previous and current fingerprints
- Watch terms that matched the source
- Local files likely to inspect
- Upstream snippets around relevant security and configuration terms
- A review checklist

## Local commands

Run a dry check:

```bash
python3 scripts/discover_config_updates.py
```

Update fingerprints and write a report when changes are found:

```bash
python3 scripts/discover_config_updates.py --update-state
```

Fail if any source cannot be fetched:

```bash
python3 scripts/discover_config_updates.py --update-state --fail-on-fetch-error
```

## Reviewer expectations

When a discovery PR appears, reviewers should convert it into one of these outcomes:

1. **No local change needed:** close with a note explaining why the upstream change does not affect hardened configs.
2. **Documentation-only update:** update README, rationale, deployment, or rollout notes.
3. **Config update:** change only the affected tier files, comments, rationale docs, and delta tables.
4. **New tool or new control surface:** add the smallest defendable config set and mark any custom settings clearly.

For config updates, keep the repository standard output order for rollout material:

1. Rollout Plan
2. Config Files
3. Tier Delta Table
4. Deployment Steps
5. Workflow-Preservation Notes

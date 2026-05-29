# Config discovery (local helper)

This directory supports **manual** maintenance: you (or a Cursor agent) check upstream vendor sources and open PRs when hardened configs need updates. There is no required GitHub Actions workflow.

See **`MANUAL-MAINTENANCE.md`** for the recommended chat prompt and process.

## Files

| File | Purpose |
|------|---------|
| `tool-sources.json` | Curated watch list of official docs, changelogs, and repositories (29 sources, 14 tools). |
| `discover_configs.py` | Optional local scanner: fingerprints sources and writes a change report. |
| `agent-prompt.md` | Policy for how an agent should author tier updates and rollout docs. |
| `MANUAL-MAINTENANCE.md` | Copy/paste prompt for Cursor and expected outcomes. |
| `state/source-snapshots.json` | Persisted fingerprints (optional; updated when you run the scanner). |
| `reports/latest-config-discovery.md` | Latest scanner output (optional). |

## Run the scanner locally

```bash
python3 automation/config-discovery/discover_configs.py \
  --sources automation/config-discovery/tool-sources.json \
  --state automation/config-discovery/state/source-snapshots.json \
  --report automation/config-discovery/reports/latest-config-discovery.md
```

Validate the registry only:

```bash
python3 automation/config-discovery/discover_configs.py \
  --sources automation/config-discovery/tool-sources.json \
  --state automation/config-discovery/state/source-snapshots.json \
  --report /tmp/report.md \
  --check
```

## Adding a source

Add an entry under the relevant tool in `tool-sources.json`. Prefer stable URLs (raw markdown, changelogs, schema files) over marketing pages.

## Review standard

Before merging a config PR:

- Confirm each change maps to a real admin or security control.
- Update only affected tool tiers and rollout material.
- Keep deployable JSON valid; use JSONC and `.comments.md` for rationale.
- Do not commit secrets, tokens, or org-specific identifiers.

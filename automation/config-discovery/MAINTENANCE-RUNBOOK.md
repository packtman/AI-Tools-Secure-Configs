# Automated Config Maintenance Runbook

This runbook describes the scheduled agent that keeps this repository current with upstream AI tool configuration changes.

## Success Criteria

The automation is working when:

1. It checks only official vendor docs, changelogs, release feeds, and repositories listed in `tool-sources.json`.
2. It opens or updates a pull request only when a watched source changes or a manual force review is requested.
3. The pull request contains one of these outcomes:
   - Focused config and documentation updates for real admin or security controls.
   - A short "No config update needed" note in the discovery report for changed sources that do not affect this repo.
4. Edited JSON, YAML, TOML, and shell files validate with the commands in `AGENTS.md`.
5. The pull request contains no secrets, API keys, tenant IDs, team IDs, production hostnames, or organization-specific values.

## Daily Loop

1. GitHub Actions runs `.github/workflows/config-discovery.yml`.
2. `discover_configs.py` fetches every source in `tool-sources.json`.
3. The scanner normalizes fetched content, removes common volatile fields, and compares fingerprints against `state/source-snapshots.json`.
4. If nothing changed, the workflow exits without a PR.
5. If something changed, the workflow writes:
   - `reports/latest-config-discovery.md`, the full review signal.
   - `reports/agent-scope.md`, the bounded work list for the maintenance agent.
6. The maintenance agent reads `agent-prompt.md`, processes only scoped tools, edits the tiered config files and docs when needed, validates, commits, and pushes.
7. The workflow opens or updates the `automation/config-maintenance` pull request.

## Required Repository Setup

| Item | Required value | Why it is needed |
|------|----------------|------------------|
| GitHub Actions permissions | `contents: write`, `pull-requests: write` | Allows the workflow to commit discovery reports and open PRs. |
| Agent secret | `ANTHROPIC_API_KEY` when using the included Claude Code action | Allows the workflow agent step to review vendor changes. |
| Branch protection | Require human review before merge | The agent proposes security policy changes, but humans approve them. |
| Scheduled trigger | Daily or less frequent | Keeps configs current without creating noisy repeated checks. |

If you use Cursor Cloud instead of the included GitHub agent step, create a scheduled Cursor Automation with the prompt in `CURSOR-AUTOMATION.md`. Keep the same success criteria and review requirements.

## Scope Control

The scanner can detect many changed sources in a single run. To keep PRs reviewable:

- `build_agent_scope.py` limits the agent to a small number of tools per run.
- The agent must not review tools omitted from `reports/agent-scope.md`.
- Deferred tools remain listed in the scope report and can be handled by a later scheduled or manual run.
- A source move, redirect, or documentation restructure should update `tool-sources.json` so future runs watch the canonical page.

## Adding or Repairing a Watched Source

1. Prefer official vendor pages that are specific to admin policy, managed settings, permissions, sandboxing, MCP, network controls, privacy, audit logs, retention, identity, or content exclusion.
2. Avoid generic landing pages and marketing pages when a stable reference page exists.
3. Add the source under the matching tool in `tool-sources.json`.
4. Include `watch_for` terms that are likely to appear near real config controls.
5. Run:

```bash
python3 automation/config-discovery/discover_configs.py \
  --sources automation/config-discovery/tool-sources.json \
  --state automation/config-discovery/state/source-snapshots.json \
  --report automation/config-discovery/reports/latest-config-discovery.md \
  --check
```

## Reviewer Checklist for Generated PRs

Reviewers should confirm:

- The changed upstream source is real and official.
- Added settings are documented by the vendor, or marked `CUSTOM:` with a clear threat-model rationale.
- Tier values are intentional: Baseline preserves common workflows, Moderate balances enterprise safety, Strict minimizes autonomy.
- Each non-trivial setting explains what it does, why the tier uses it, and what breaks if misconfigured.
- Deployable JSON remains valid. Rationale for JSON settings lives in JSONC or companion `.comments.md` files.
- Rollout guidance covers pilot phases, rollback, validation, audit logging, and workflow-preservation notes when behavior changes.
- The PR does not contain secrets or organization-specific identifiers.

## Failure Handling

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Workflow exits with no PR | No upstream fingerprints changed | No action needed. |
| Agent hits a turn limit | Too many tools scoped in one run | Lower `--max-tools` in the workflow or re-run after merging the first PR. |
| Source fetch fails | Vendor page moved, blocked, or changed format | Replace the URL with the canonical vendor page and re-run the registry check. |
| PR contains only a discovery report | Agent found no relevant control or could not finish | Require "No config update needed" notes, or re-run with a narrower scope. |
| Validation fails | Edited config syntax is invalid | Fix the edited file and rerun the relevant validator from `AGENTS.md`. |

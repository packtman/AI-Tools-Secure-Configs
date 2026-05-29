# Config Discovery Cost Controls

This automation is designed to keep daily runs cheap while still alerting you when upstream vendor docs change.

## Default behavior

| Trigger | Discovery (free) | Config agent (API cost) |
|---------|------------------|---------------------------|
| Daily schedule (`cron`) | Yes | No |
| Manual workflow dispatch | Yes | Only if you enable **run_config_agent** and content changed |

Scheduled runs fingerprint upstream sources and open or update a PR with the report. They do not call the model unless you opt in (see below).

## Agent run caps (per invocation)

These defaults are set in `.github/workflows/config-discovery.yml` and can be overridden with repository **Variables** (Settings → Secrets and variables → Actions → Variables):

| Variable | Default | Purpose |
|----------|---------|---------|
| `CONFIG_AGENT_MAX_BUDGET_USD` | `0.75` | Hard stop via Claude Code `--max-budget-usd` |
| `CONFIG_AGENT_MAX_TURNS` | `12` | Hard stop via `--max-turns` |
| `CONFIG_AGENT_MAX_SOURCES` | `1` | Sources queued per run (extras deferred to a later run) |
| `CONFIG_AGENT_ON_SCHEDULE` | `false` | Set to `true` only if you want the daily cron to call the agent |

## Typical spend

- **Discovery-only run:** $0 (HTTP fetches only).
- **Agent run (defaults):** Often under $0.75 per invocation; previously uncapped Opus runs with 30+ turns and WebFetch could exceed $2.

The agent is instructed not to use WebFetch; it should rely on snippets already captured in the discovery report.

## Recommended operating model

1. Let the schedule run discovery-only (default).
2. When a PR shows real `content-changed` sources, review the report yourself or run the workflow manually with **run_config_agent** enabled.
3. If multiple tools changed the same day, handle one source per agent run (`CONFIG_AGENT_MAX_SOURCES=1`). Deferred sources are listed in the report.
4. For larger batches, use Cursor Cloud (`CURSOR-AUTOMATION.md`) with your own budget instead of raising GitHub Actions caps.

## Enabling agent on schedule (not recommended unless budgeted)

Set repository variable `CONFIG_AGENT_ON_SCHEDULE` to `true`. Keep `CONFIG_AGENT_MAX_BUDGET_USD` low and review monthly API usage in the Anthropic console.

# Config Discovery Cost Controls

This automation watches **29 upstream sources** across 14 tools. Costs split into discovery (free) and the config agent (Anthropic API, Sonnet by default).

## Default behavior

| Trigger | Discovery | Config agent |
|---------|-----------|----------------|
| Daily schedule (`cron`) | Yes ($0) | No |
| Manual dispatch | Yes ($0) | Only if **run_config_agent** is enabled and content-level changes exist |

Scheduled runs do not call the model unless you set `CONFIG_AGENT_ON_SCHEDULE=true`.

## Agent queue: all sources

`CONFIG_AGENT_MAX_SOURCES=0` (default) queues **every** agent-worthy source in one run. There is no per-run deferral when the cap is 0.

Agent-worthy means `content-changed`, `new-source-baseline`, or fetch/HTTP status changes. Metadata-only `fingerprint-method-changed` does **not** invoke the agent.

## Dynamic spend caps (per agent run)

Limits scale with `agent_queue_count` in `reports/discovery-summary.json`:

| Queued sources | Budget cap (USD) | Turn cap |
|----------------|------------------|----------|
| 1 | $2.50 | 15 |
| 3 | $3.00 | 14 |
| 5 | $3.75 | 18 |
| 10 | $6.00 | 28 |
| 15 | $8.25 | 38 |
| 29 (all watched, if all changed same day) | $15.00 (ceiling) | 66 |

Formula: `budget = min(ceiling, max(2.50, 0.45 × queued + 1.50))`, `turns = min(80, max(15, 2 × queued + 8))`.

Override ceiling with repository variable `CONFIG_AGENT_BUDGET_CEILING_USD` (default `15.00`).

Set `CONFIG_AGENT_STATIC_LIMITS=true` to use fixed `CONFIG_AGENT_MAX_BUDGET_USD` and `CONFIG_AGENT_MAX_TURNS` instead.

## Estimated API cost (Sonnet, no WebFetch)

These are planning numbers, not guarantees. Actual cost appears in the workflow log (`total_cost_usd`) when the agent finishes.

| Scenario | Queued sources | Typical spend | Notes |
|----------|----------------|---------------|--------|
| Quiet day | 0 | $0 | Discovery only |
| Single doc update | 1 | $0.15 – $0.60 | Often "no config update needed" |
| Few tools changed | 3 | $0.50 – $1.50 | Light tier edits |
| Busy vendor day | 5 – 10 | $1.50 – $5.00 | Several small diffs |
| Full queue (rare) | 29 | $4.00 – $12.00 | Capped at $15 budget; may hit turn limit first |

**Per source (rule of thumb):**

- Report-only "no update needed": about **$0.05 – $0.15**
- Small config + rationale edit: about **$0.20 – $0.50**

**Monthly planning (example):**

| Pattern | Agent runs / month | Est. API spend |
|---------|-------------------|----------------|
| Discovery daily, agent 4× when docs change | 4 | $2 – $8 |
| Agent weekly on manual trigger | 4 | $2 – $6 |
| Agent on every schedule (not recommended) | 30 | $15 – $90+ |

Discovery-only scheduled runs: **$0** API (GitHub Actions minutes only).

## Comparison to your failed run

| | Failed run (May 2026) | Current defaults |
|--|----------------------|------------------|
| Model | Opus | Sonnet |
| Sources | 28 (fingerprint noise) | Only content-level |
| WebFetch | Yes | No |
| Budget cap | None (~$2.52 at 31 turns) | Yes (up to $15) |

## Repository variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CONFIG_AGENT_MAX_SOURCES` | `0` | `0` = queue all agent-worthy sources |
| `CONFIG_AGENT_BUDGET_CEILING_USD` | `15.00` | Max `--max-budget-usd` per run |
| `CONFIG_AGENT_MAX_BUDGET_USD` | `12.00` | Used only if `CONFIG_AGENT_STATIC_LIMITS=true` |
| `CONFIG_AGENT_MAX_TURNS` | `80` | Used only if static limits enabled |
| `CONFIG_AGENT_STATIC_LIMITS` | `false` | Disable dynamic sizing |
| `CONFIG_AGENT_ON_SCHEDULE` | `false` | Call agent on daily cron |

## Operating model

1. Let the schedule run discovery-only (free).
2. When the PR lists content-level changes, run the workflow with **run_config_agent** to process **all** queued sources in one pass.
3. Check Anthropic usage dashboard after the first full run to calibrate these estimates for your repo.

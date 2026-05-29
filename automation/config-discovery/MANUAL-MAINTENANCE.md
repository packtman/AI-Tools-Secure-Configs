# Manual config maintenance (recommended)

The simplest way to keep this repo current is to ask a Cursor agent (or another assistant) to check upstream vendor docs and open a PR. No GitHub Actions, API secrets, or scheduled automation required.

## When to ask

- After a vendor announces new admin, managed-settings, MCP, sandbox, or policy controls
- Monthly or quarterly, if you want a proactive sweep
- When you add a new tool directory and want parity with official docs

## What to paste in chat

```text
Check AI-Secure-Configs for upstream config changes and open a PR if needed.

1. Read automation/config-discovery/tool-sources.json and automation/config-discovery/agent-prompt.md.
2. Optionally run the local discovery scanner (commands in automation/config-discovery/README.md) or fetch the official docs/changelogs yourself.
3. For each supported tool, compare upstream admin/security controls with our Strict / Moderate / Baseline tier files.
4. If a real control was added or changed, update tier JSON/JSONC, rationale, README, and rollout-guide sections. Keep deployable JSON valid.
5. Do not add secrets, tokens, org IDs, tenant IDs, team IDs, or production hostnames.
6. Validate edited JSON, YAML, TOML, and shell files per AGENTS.md.
7. Open a focused PR with a clear summary of what changed and why.

Supported tools: Claude Code, Cursor, GitHub Copilot, Codex CLI, Codex Desktop, Continue.dev, Windsurf, Tabnine, Amazon Q Developer, Gemini CLI, Google Gemini, Claude Desktop, OpenAI Platform, Claude API.
```

## Optional: local discovery first

The scanner fingerprints URLs in `tool-sources.json` and writes a report. Use it to narrow what the agent should read:

```bash
python3 automation/config-discovery/discover_configs.py \
  --sources automation/config-discovery/tool-sources.json \
  --state automation/config-discovery/state/source-snapshots.json \
  --report automation/config-discovery/reports/latest-config-discovery.md
```

Commit snapshot/report updates only if you want them in git; they are not required for a config PR.

## Cost

- **Local scanner:** free (HTTP only).
- **Cursor / Claude review:** depends on your plan; typically far simpler than wiring Anthropic API keys into GitHub Actions.

## What a good PR includes

- Actual tier config changes when a vendor control matters for security posture
- Rationale and rollout notes when behavior changes
- A short note per source when no repo change is needed (avoid empty mystery PRs)

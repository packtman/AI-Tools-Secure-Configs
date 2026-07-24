# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config update is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## No scoped tools

No unresolved 'Potential config terms not found' sections remain after this maintenance run.

Claude Code managed controls were updated for agent view, Artifacts, away summaries, background tasks, IDE install, and the 2.1.212 hard version floor. Discovery watchers were stabilized and candidate filtering was added. See resolution notes in `latest-config-discovery.md`.

# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. Mark each reviewed source with `Review outcome: resolved` and explain what changed or why no config update was needed.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## No scoped tools

No 'Potential config terms not found' sections were found.
No additional config review is required for this report.

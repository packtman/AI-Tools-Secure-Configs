# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools to process (1 of 1 with missing terms)

### OpenAI Platform

- Source: OpenAI OpenAPI schema
  - Missing terms: `allowed_tools`, `checkpoint.permission`, `enabled_for_all_projects`, `enabled_for_selected_projects`, `enabled_per_call`, `label_model`, `mcp`, `mcp_approval_request`, `mcp_approval_response`, `mcp_call`, `mcp_list_tools`, `mcp_list_tools.completed`, `mcp_list_tools.failed`, `mcp_list_tools.in_progress`, `reinforcement`
  - (6 more terms in the full report)

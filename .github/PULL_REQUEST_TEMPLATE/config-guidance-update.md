# Config guidance update

Use this template for pull requests created from config discovery findings.

## Source changes reviewed

- [ ] I read `config-discovery/reports/latest.md`
- [ ] I opened each changed official source linked in the report
- [ ] I identified which tools, tiers, and deployment docs are affected

## Config impact

- [ ] No tiered config changes are needed, source change is informational only
- [ ] Tiered config files were updated where needed
- [ ] JSON files remain valid after comments are stripped, or have a matching `.comments.md`
- [ ] TOML and YAML comments explain non-trivial settings
- [ ] No secrets, tokens, or API keys were added
- [ ] No em dashes were added in prose or comments

## Rollout impact

- [ ] Rollout plan, deployment paths, or validation commands were updated if vendor guidance changed
- [ ] Workflow-preservation notes were updated for any new blocked or changed behavior
- [ ] Tier delta table was updated if a setting changed across Baseline, Moderate, or Strict
- [ ] Tool overlap was considered, especially shell execution, MCP, network egress, and content exclusion

## Validation

- [ ] Changed JSON files validated with `python3 -m json.tool <file>`
- [ ] Changed YAML files validated with `yamllint -d relaxed <file>`
- [ ] Changed TOML files validated with `python3 -c "import toml; toml.load('<file>')"`
- [ ] Changed shell scripts validated with `bash -n <file>`
- [ ] Discovery scanner ran locally, `python3 scripts/discover_config_updates.py --dry-run`

## Reviewer notes

Explain the security or workflow reason for this change:

- 

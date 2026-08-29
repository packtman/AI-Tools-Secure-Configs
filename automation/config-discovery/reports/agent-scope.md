# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools processed (2026-08-29)

### Claude Code

- Source: Settings reference (`https://code.claude.com/docs/en/settings-reference.md`)
- Unique control pinned: `autoContinueAtUsageLimit: false` on Moderate and Strict (Baseline unset). Vendor default is `true`. Requires v2.1.234+.
- Watcher added: `https://code.claude.com/docs/en/settings-reference.md`

## Deferred

Open PRs #61-#96 already cover earlier unique keys. Next unique follow-ups after those merge: pair `disableSideloadFlags` after #61; `pluginSuggestionMarketplaces` after #88; `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` only if an org wants it as a gateway compatibility pin (not a default); `managedSourcesBehavior` / `requiredMaximumVersion` / `httpHookAllowedEnvVars` in later runs; do not pin Codex 0.152 alpha.

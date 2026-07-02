# Agent scope for this run

Process only the tools listed below. For each tool:

1. Read the cited missing terms and the upstream URL from the full discovery report.
2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.
3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.
4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.
5. Validate edited JSON, YAML, and TOML before finishing.

Do not attempt to review unchanged tools or sources with no missing local terms in this run.

## Tools to process (1 of 1 tools with missing terms)

### Gemini CLI

- Source: Gemini CLI settings reference
  - Missing terms: `advanced.autoConfigureMemory`, `agents.browser.blockFileUploads`, `context.fileFiltering.enableFuzzySearch`, `context.fileFiltering.enableRecursiveFileSearch`, `experimental.autoMemory`, `experimental.gemmaModelRouter.autoStartServer`, `experimental.gemmaModelRouter.enabled`, `experimental.modelSteering`, `experimental.voice.activationMode`, `experimental.voice.whisperModel`, `experimental.voiceMode`, `general.defaultApprovalMode`, `general.enableAutoUpdate`, `general.enableNotifications`, `general.plan.enabled`
  - (9 more terms in the full report)

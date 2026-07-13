# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Gemini CLI | Gemini CLI settings reference | new-source-baseline | 200 | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/settings.md |

## Review Details

### Gemini CLI: Gemini CLI settings reference

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/settings.md
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> ... mand opens a dialog to view and edit all your Gemini CLI settings, including your UI experience,
keybindings, and accessibility features. Your Gemini CLI settings are stored in a `settings.json`
file. In addition to using the `/settings` command, you can also edit them in one of the following
locations: - **User settings**: `~/.gemini/settings.json` - **Workspace setting ...

> ... e the context summary (GEMINI.md, MCP servers) above the input. | `false` | | Hide CWD |
`ui.footer.hideCWD` | Hide the current working directory in the footer. | `false` | | Hide Sandbox
Status | `ui.footer.hideSandboxStatus` | Hide the sandbox status indicator in the footer. | `false`
| | Hide Model Info | `ui.footer.hideModelInfo` | Hide the model name and conte ...

> ... ormat. | `true` | | Hide Banner | `ui.hideBanner` | Hide the application banner | `false` | |
Hide Context Summary | `ui.hideContextSummary` | Hide the context summary (GEMINI.md, MCP servers)
above the input. | `false` | | Hide CWD | `ui.footer.hideCWD` | Hide the current working directory
in the footer. | `false` | | Hide Sandbox Status | `ui.footer.hideSandb ...

> ... e LLM-based error correction for edit tools. When enabled, tools will fail immediately if exact
string matches are not found, instead of attempting to self-correct. | `true` | ### Security | UI
Label | Setting | Description | Default | | ------------------------------------- |
----------------------------------------------- | ---------------------------------------- ...

Potential config terms not found in local tool files:

`advanced.autoConfigureMemory`, `agents.browser.blockFileUploads`, `context.fileFiltering.enableFuzzySearch`, `context.fileFiltering.enableRecursiveFileSearch`, `experimental.autoMemory`, `experimental.gemmaModelRouter.autoStartServer`, `experimental.gemmaModelRouter.enabled`, `experimental.modelSteering`, `experimental.voice.activationMode`, `experimental.voice.whisperModel`, `experimental.voiceMode`, `general.defaultApprovalMode`, `general.enableAutoUpdate`, `general.enableNotifications`, `general.plan.enabled`, `general.plan.modelRouting`, `general.sessionRetention.enabled`, `general.sessionRetention.maxAge`, `general.vimMode`, `hooksConfig.enabled`, `ide.enabled`, `model.compressionThreshold`, `model.disableLoopDetection`, `model.name`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

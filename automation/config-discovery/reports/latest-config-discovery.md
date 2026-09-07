# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | candidate-filter-changed | 200 | https://code.claude.com/docs/en/settings.md |
| Claude Code | Environment variables documentation | candidate-filter-changed | 200 | https://code.claude.com/docs/en/env-vars.md |
| GitHub Copilot | Organization policy documentation | content-changed | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies.md |
| GitHub Copilot | Content exclusion documentation | content-changed | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot.md |

## Review Details

### Claude Code: Managed settings documentation

- Change type: `candidate-filter-changed`
- Source URL: https://code.claude.com/docs/en/settings.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... ------------------------------------------------------------------------------------------------
------------ | :------------------------------------------ | | **Managed** | Server-managed
settings, plist / registry, or system-level `managed-settings.json` | All organization members for
server-managed delivery; all users on the machine for plist, HKLM registry, and file deli ...

> ... re (themes, editor settings) * Tools and plugins you use across all projects * API keys and
authentication (stored securely) **Project scope** is best for: * Team-shared settings (permissions,
hooks, MCP servers) * Plugins the whole team should have * Standardizing tooling across
collaborators **Local scope** is best for: * Personal overrides for a specific project * T ...

> ... ude/settings.json` instead. Before v2.1.142, project settings could set `auto`. The
`--permission-mode` CLI flag overrides this setting for a single session | `"acceptEdits"` | |
`disableBypassPermissionsMode` | Set to `"disable"` to prevent `bypassPermissions` mode from being
activated. This disables the `--dangerously-skip-permissions` command-line flag. Typically placed in
[managed ...

> ... to all scopes including managed servers. Denylist takes precedence over allowlist. See [Managed
MCP configuration](/docs/en/managed-mcp) | `[{ "serverName": "filesystem" }]` | | `disableAgentView`
| Set to `true` to turn off [background agents and agent view](/docs/en/agent-view): `claude
agents`, `--bg`, `/background`, and the on-demand supervisor. Typically set in [manag ...

> ... etting `CLAUDE_CODE_DISABLE_AGENT_VIEW` to `1` | `true` | | `disableAllHooks` | Disable all
[hooks](/docs/en/hooks) and any custom [status line](/docs/en/statusline) | `true` | |
`disableArtifact` | Set to `true` to disable the [Artifact](/docs/en/artifacts) tool, which
publishes session output as a private web page on claude.ai. Equivalent to setting
`CLAUDE_CODE_DISABLE_ ...

Potential config terms found upstream are already present in local tool files.

### Claude Code: Environment variables documentation

- Change type: `candidate-filter-changed`
- Source URL: https://code.claude.com/docs/en/env-vars.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... navailable, any configured `advisorModel` is ignored, and the `--advisor` flag is accepted but
has no effect, so existing scripts that pass it continue to work without errors | |
`CLAUDE_CODE_DISABLE_AGENT_VIEW` | Set to `1` to turn off [background agents and agent
view](/docs/en/agent-view): `claude agents`, `--bg`, `/background`, and the on-demand supervisor.
Equivalent to the [`disabl ...

> ... ) setting. You can also switch with `/tui default`. Does not apply to background sessions opened
from [agent view](/docs/en/agent-view), which always use fullscreen rendering | |
`CLAUDE_CODE_DISABLE_ARTIFACT` | Set to `1` to disable the [Artifact](/docs/en/artifacts) tool,
which publishes session output as a private web page on claude.ai. Equivalent to the
[`disableArtifact`](/docs/en ...

> ... --bare` mode or [`autoMemoryEnabled: false`](/docs/en/settings#available-settings) would
otherwise disable it. When disabled, Claude does not create or load auto memory files | |
`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Set to `1` to disable all background task functionality,
including the `run_in_background` parameter on Bash and subagent tools, auto-backgrounding, and the
Ctrl+B shortcut | | ...

> ... IDE_HOST_OVERRIDE` | Override the host address used to connect to the IDE extension. By default
Claude Code auto-detects the correct address, including WSL-to-Windows routing | |
`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL` | Set to `1` to skip auto-installation of IDE extensions.
Equivalent to setting [`autoInstallIdeExtension`](/docs/en/settings#global-config-settings) to
`false` | | `CLAUDE_CODE_ ...

> ... s. In v2.1.158 through v2.1.206, setting this to `1` was required to make [auto
mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) available on those providers | |
`CLAUDE_CODE_ENABLE_AWAY_SUMMARY` | Override [session recap](/docs/en/interactive-mode#session-
recap) availability. Set to `0` to force recaps off regardless of the `/config` toggle. Set to `1`
to force recaps on ...

Potential config terms found upstream are already present in local tool files.

### GitHub Copilot: Organization policy documentation

- Change type: `content-changed`
- Source URL: https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies.md
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> ... minister/manage-for-organization/manage-policies shortTitle: Manage policies contentType: how-
tos category: - Manage Copilot for a team --- {% data reusables.organizations.copilot-policy-ent-
overrides-org %} ## Enabling {% data variables.product.prodname_copilot_short %} features and models
in your organization {% data reusables.profile.access_org %} {% data reusa ...

> --- title: Managing policies and features for GitHub Copilot in your organization intro: 'Control
the availability of {% data variables.product.prodname_copilot %} features and models for users
granted a license by your organization.' permissions: Organization ...

> ... es and models in your organization {% data reusables.profile.access_org %} {% data
reusables.profile.org_settings %} 1. {% data reusables.user-settings.code-planning-automation %}
click **{% octicon "copilot" aria-hidden="true" aria-label="copilot" %} {% data
variables.product.prodname_copilot_short %}**. * Click **Policies** to edit the policies that
control p ...

> ... e_copilot_short %}, which may incur additional costs. 1. For each policy you want to configure,
click the dropdown menu and select an enforcement option. {% data reusables.copilot.mcp-servers-
policy-note %} ## Enabling or disabling third-party coding agents in your repositories > [!NOTE] > *
{% data reusables.copilot.plans.permission-paid-plans-no-purchase-link ...

### GitHub Copilot: Content exclusion documentation

- Change type: `content-changed`
- Source URL: https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot.md
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> ... {% data variables.product.prodname_copilot_short %} from accessing certain content.'
permissions: 'Repository administrators, organization owners, and enterprise owners can manage
content exclusion settings. People with the "Maintain" role for a repository can view, but not edit,
content exclusion settings for that repository.' product: '{% data reusables.gated-features.copi ...

> ... lot-cli/about-copilot-cli), [AUTOTITLE](/copilot/concepts/agents/cloud-agent/about-cloud-agent),
and [AUTOTITLE](/copilot/how-tos/chat-with-copilot/chat-in-ide). {% data
reusables.repositories.navigate-to-repo %} {% data reusables.repositories.sidebar-settings %} 1. {%
data reusables.user-settings.code-planning-automation %} click **{% octicon "copilot" aria-
hidden="tru ...

> ... es located anywhere (within a Git repository or elsewhere), enter `"*":` followed by the path to
the file, or files, you want to exclude. If you want to specify multiple file path patterns, list
each pattern on a separate line. To exclude files in a Git repository from {% data
variables.product.prodname_copilot_short %}, enter a reference to the repository on one li ...

> ... it these settings. 1. In the box following "Paths to exclude in this repository," enter the
paths to files from which {% data variables.product.prodname_copilot_short %} should be excluded.
Use the format: `- "/PATH/TO/DIRECTORY/OR/FILE"`, with each path on a separate line. You can add
comments by starting a line with `#`. > [!TIP] {% data reusables.copilot.content- ...

> ... ub-copilot-in-your-organization/managing-github-copilot-features-in-your-organization/testing-
changes-to-content-exclusions-in-your-ide - /copilot/managing-copilot/configuring-and-auditing-
content-exclusion/excluding-content-from-github-copilot - /copilot/how-tos/content-
exclusion/excluding-content-from-github-copilot - /copilot/how-tos/content-exclusion/exclude- ...

## Resolution Notes (2026-07-24)

### Claude Code

Config update applied in this PR:

- Added managed `disableAgentView`, `disableArtifact`, `awaySummaryEnabled`, Strict `disableBundledSkills`, and Strict `fileCheckpointingEnabled: false`.
- Replaced soft `minimumVersion` with `requiredMinimumVersion: 2.1.212` for Moderate and Strict.
- Added Moderate/Strict env controls for background tasks, away summary, IDE extension auto-install, and Strict auto IDE connect.
- Updated rationale, env reference, rollout JSON/JSONC/comments, tier deltas, developer communication, and workflow-preservation notes.
- Focused Claude Code discovery candidates with `candidate_allowlist` and switched watchers to stable `code.claude.com` markdown.

No further Claude Code config update needed for the remaining discovery noise terms:

- `ANTHROPIC_MODEL` / model-option env vars: model selection preferences, not threat controls.
- `CLAUDE_MODEL`: not a valid managed settings or hooks control.
- `CLAUDE_CODE_SUBAGENT_MODEL`: subagent model routing preference only.

### GitHub Copilot

No config update needed. The watcher change moves Organization policy and Content exclusion sources from volatile HTML docs pages to stable raw GitHub Docs markdown. Existing Copilot org-policy and content-exclusion templates remain aligned with the current policy and exclusion guidance.

### Codex CLI

No config update needed for `McpRuntime`. It appears in release chatter as an internal runtime name, not a documented admin setting in the Codex configuration reference.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

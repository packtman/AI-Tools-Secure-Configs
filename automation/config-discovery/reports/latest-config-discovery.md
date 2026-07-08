# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| GitHub Copilot | Organization policy documentation | content-changed | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/administer-copilot/manage-for-organization/manage-policies.md |
| GitHub Copilot | Content exclusion documentation | content-changed | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot.md |

## Review Details

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

> ... atures and models in your organization {% data reusables.profile.access_org %} {% data
reusables.profile.org_settings %} 1. In the sidebar, under "Code, planning, and automation", click
**{% octicon "copilot" aria-hidden="true" aria-label="copilot" %} {% data
variables.product.prodname_copilot_short %}**. * Click **Policies** to edit the policies that
control p ...

No config update needed (2026-07-08): this source was moved from redirect-heavy HTML to the stable GitHub Docs markdown file. The existing GitHub Copilot tier policies and rationale already cover feature policies, Copilot CLI, coding agent review gates, extensions, MCP governance, model availability review, and web/Bing search restrictions.

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

> ... /agents/about-copilot-cli), [AUTOTITLE](/copilot/concepts/agents/cloud-agent/about-cloud-agent),
and [AUTOTITLE](/copilot/how-tos/chat-with-copilot/chat-in-ide). {% data
reusables.repositories.navigate-to-repo %} {% data reusables.repositories.sidebar-settings %} 1. In
the "Code & automation" section of the sidebar, click **{% octicon "copilot" aria-hidden="true"
aria-l ...

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

No config update needed (2026-07-08): this source was moved from redirect-heavy HTML to the stable GitHub Docs markdown file. The existing content-exclusion examples and rationale already cover organization-level patterns, sensitive file classes, audit log review, validation steps, and workflow-preserving testing guidance.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

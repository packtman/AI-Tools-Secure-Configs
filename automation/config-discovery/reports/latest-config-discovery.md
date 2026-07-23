# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Codex CLI | OpenAI Codex repository | content-changed | 200 | https://developers.openai.com/codex/config-reference |
| Codex Desktop | OpenAI Codex repository | content-changed | 200 | https://developers.openai.com/codex/enterprise/admin-setup |
| Codex Desktop | OpenAI Codex config reference | content-changed | 200 | https://developers.openai.com/codex/enterprise/managed-configuration |

## Review Details

### Codex CLI: OpenAI Codex repository

- Change type: `content-changed`
- Source URL: https://developers.openai.com/codex/config-reference
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> Configuration Reference | ChatGPT Learn ChatGPT Home API Codex Docs Guides, concepts, and product
docs for Codex Use cases Example workflows and tasks teams can take on with ChatGPT or C ...

> ... Audio and speech Overview Voice agents Specialized models Deep research Embeddings Moderation
Overview Agents SDK Quickstart Agent definitions Models and providers Running agents Sandbox agents
Orchestration Guardrails Results and state Integrations and observability Evaluate agent workflows
ChatKit Overview Customize Widgets Actions Advanced integrations Overview ...

> ... egrations GitHub Slack Linear Reference CLI customization Developer commands Developer settings
Plugin submission errors Overview Permissions Profiles Sandboxing Auto-review Agent approvals &
security Internet access Codex Security Overview Cloud FAQ Codex Security plugin Quickstart Run a
security scan Run a deep scan Review code changes Triage a backlog Fix finding ...

> ... les Extend ChatGPT and Codex Record & Replay MCP Windows Desktop app Windows sandbox WSL
*+*]:mt-3"> Copy Page Configuration Reference Complete reference for Codex config.toml and
requirements.toml Copy Page Use this page as a searchable reference for Codex configuration files.
For conceptual guidance and examples, start with Config basics and Advanced Config . config.t ...

> ... atGPT Work admin FAQ Identity and authentication Authentication overview Access tokens Workspace
access, policy, and models Groups and provisioning Roles and workspace permissions Managed
configuration HIPAA configuration Workspace model availability Plugin and connector controls Plugin
controls Skill controls Usage, governance, and compliance Governance Workspace ...

No config update needed: this change establishes the focused Codex configuration reference as the
new watcher baseline. Existing Codex CLI tier files already cover the referenced approval, sandbox,
requirements, and managed-hook controls.

### Codex Desktop: OpenAI Codex repository

- Change type: `content-changed`
- Source URL: https://developers.openai.com/codex/enterprise/admin-setup
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> ... Enterprise rollout across workspace and developer surfaces Copy Page Use this guide to plan a
ChatGPT Enterprise rollout across these administration boundaries: Workspace access. Local runtime
policy for covered capabilities in the ChatGPT desktop app, Codex CLI, and IDE extension. Codex
cloud. Platform API access. Plugins and connector access. Permissions in connected ...

> ... llout: Workspace access: Membership, seats, roles, and supported workspace features. Local
runtime policy: Approvals, permission profiles, filesystem and network access, and other
requirements for supported local clients. Codex cloud: Hosted environments, repository connections,
and cloud runtime policy. Connected systems: Provider-side application installation, account ...

> ... mproving the threat model Safety Cyber Safety Overview Getting started Admin rollout guide
ChatGPT Work admin FAQ Identity and authentication Authentication overview Access tokens Workspace
access, policy, and models Groups and provisioning Roles and workspace permissions Managed
configuration HIPAA configuration Workspace model availability Plugin and connector controls Pl ...

> ... nd workspace permissions Managed configuration HIPAA configuration Workspace model availability
Plugin and connector controls Plugin controls Skill controls Usage, governance, and compliance
Governance Workspace analytics Analytics API Compliance API and audit events Deployment and model
providers Windows app deployment Remote connections Amazon Bedrock Explore use ca ...

> Admin rollout guide | ChatGPT Learn ChatGPT Home API Codex Docs Guides, concepts, and product docs
for Codex Use cases Example workflows and tasks teams can take on with ChatGPT or Codex Docs U ...

No config update needed: this change replaces the generic GitHub repository page with OpenAI's
admin rollout guide. The current Codex Desktop rollout documentation already separates workspace
access, local runtime requirements, managed configuration, and compliance monitoring.

### Codex Desktop: OpenAI Codex config reference

- Change type: `content-changed`
- Source URL: https://developers.openai.com/codex/enterprise/managed-configuration
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> Managed configuration | ChatGPT Learn ChatGPT Home API Codex Docs Guides, concepts, and product docs
for Codex Use cases Example workflows and tasks teams can take on with ChatGPT or Codex Docs ...

> ... Audio and speech Overview Voice agents Specialized models Deep research Embeddings Moderation
Overview Agents SDK Quickstart Agent definitions Models and providers Running agents Sandbox agents
Orchestration Guardrails Results and state Integrations and observability Evaluate agent workflows
ChatKit Overview Customize Widgets Actions Advanced integrations Overview ...

> ... egrations GitHub Slack Linear Reference CLI customization Developer commands Developer settings
Plugin submission errors Overview Permissions Profiles Sandboxing Auto-review Agent approvals &
security Internet access Codex Security Overview Cloud FAQ Codex Security plugin Quickstart Run a
security scan Run a deep scan Review code changes Triage a backlog Fix finding ...

> ... Compliance API and audit events Deployment and model providers Windows app deployment Remote
connections Amazon Bedrock *+*]:mt-3"> Copy Page Managed configuration Enforce runtime requirements
across supported local clients and distribute managed defaults Copy Page Managed configuration
controls supported local runtime behavior for covered capabilities in the ChatGPT de ...

> ... en for users who turned hooks off locally, pin [features].hooks = true alongside [hooks] . To
skip user, project, session, and plugin hooks while still allowing managed hooks, set
allow_managed_hooks_only = true . allow_managed_hooks_only = true [ features ] hooks = true [ hooks
] managed_dir = "/enterprise/hooks" windows_managed_dir = 'C:\enterprise\hooks' [[ hooks . Pr ...

No config update needed: this change establishes OpenAI's managed-configuration page as the watcher
baseline. The strict, moderate, and baseline Codex Desktop requirements files already include
`allow_managed_hooks_only` with tier-appropriate values.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

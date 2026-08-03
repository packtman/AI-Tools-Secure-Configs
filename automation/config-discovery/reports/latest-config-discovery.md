# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Maintenance applied (2026-08-03)

Gemini CLI Management Console controls covered in this branch:

- Added tiered `management-console-*.json` targets for Strict Mode (`admin.secureModeEnabled`), Extensions, MCP enable/allowlist/`requiredConfig`, and Unmanaged Capabilities / Agent Skills (`admin.skills.enabled`).
- Documented that remote `admin.*` must not be copied into local `settings.json`.
- Replaced the noisy Gemini GitHub homepage watcher with settings schema, enterprise-controls, and Agent Skills docs.
- Schema rescan: potential admin terms for Gemini CLI are present in local management-console templates.

Deferred duplicates (already open elsewhere): Continue (#75), Amazon Q (#74), Cursor (#73), Codex CLI/Copilot (#72), Windsurf (#71), Claude Desktop/API (#70), Codex Desktop/OpenAI Platform (#69), Claude Code (#66/#68), Tabnine (#65), Gemini CLI local settings refresh (#64).

No config update needed for Claude Code missing terms such as `ANTHROPIC_MODEL` / `CLAUDE_MODEL` / IDE UX env vars: developer preference or model routing, not org admin security knobs. Codex release names `McpConnectionSet` / `McpRuntime` / `forceRefetch` are not admin settings.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/settings |
| Claude Code | Hooks documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Claude Code | Dynamic workflows documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/workflows |
| GitHub Copilot | Organization policy documentation | content-changed | 200 | https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization |
| GitHub Copilot | Content exclusion documentation | content-changed | 200 | https://docs.github.com/en/copilot/managing-copilot/configuring-and-auditing-content-exclusion |
| Codex CLI | OpenAI Codex repository | content-changed | 200 | https://github.com/openai/codex |
| Codex CLI | OpenAI Codex releases | content-changed | 200 | https://api.github.com/repos/openai/codex/releases?per_page=10 |
| Codex Desktop | OpenAI Codex repository | content-changed | 200 | https://github.com/openai/codex |
| Codex Desktop | OpenAI Codex config reference | content-changed | 200 | https://raw.githubusercontent.com/openai/codex/main/codex-rs/config.md |
| Continue.dev | Configuration reference | content-changed | 200 | https://docs.continue.dev/reference |
| Continue.dev | Continue repository | content-changed | 200 | https://github.com/continuedev/continue |
| Windsurf | Windsurf documentation | content-changed | 200 | https://docs.windsurf.com/ |
| Windsurf | Windsurf changelog | content-changed | 200 | https://windsurf.com/changelog |
| Tabnine | Tabnine admin documentation | content-changed | 200 | https://docs.tabnine.com/ |
| Tabnine | Tabnine enterprise documentation | content-changed | 200 | https://www.tabnine.com/enterprise |
| Amazon Q Developer | Amazon Q Developer IAM reference | content-changed | 200 | https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonqdeveloper.html |
| Gemini CLI | Gemini CLI settings schema | new-source-baseline | 200 | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json |
| Gemini CLI | Gemini CLI enterprise admin controls | new-source-baseline | 200 | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/admin/enterprise-controls.md |
| Gemini CLI | Gemini CLI Agent Skills documentation | new-source-baseline | 200 | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/skills.md |
| Gemini CLI | Gemini CLI documentation | content-changed | 200 | https://cloud.google.com/gemini/docs/codeassist/gemini-cli |
| Google Gemini | Vertex AI Gemini safety settings | content-changed | 200 | https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters |
| Google Gemini | Google Cloud organization policies | content-changed | 200 | https://cloud.google.com/resource-manager/docs/organization-policy/overview |
| Claude Desktop | Claude Desktop MCP documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Claude Desktop | Claude Desktop support documentation | content-changed | 200 | https://support.anthropic.com/en/ |
| OpenAI Platform | OpenAI OpenAPI repository | content-changed | 200 | https://github.com/openai/openai-openapi |
| OpenAI Platform | OpenAI OpenAPI schema | content-changed | 200 | https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml |
| Claude API | Anthropic admin API documentation | content-changed | 200 | https://platform.claude.com/docs/en/api/admin.md |
| Claude API | Anthropic API release notes | content-changed | 200 | https://platform.claude.com/docs/en/release-notes/api.md |

## Review Details

### Claude Code: Managed settings documentation

- Change type: `content-changed`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/settings
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... d shortcuts On this page Configuration scopes Available scopes When to use each scope How scopes
interact What uses scopes Settings files When edits take effect Invalid entries in managed settings
Available settings Global config settings Worktree settings Permission settings Permission rule
syntax Sandbox settings Sandbox path prefixes Attribution settings File suggestion ...

> ... in content Claude Code Docs home page English Search...  K Ask Assistant Claude Developer
Platform Claude Code on the Web Claude Code on the Web Search... Navigation Settings and permissions
Claude Code settings Getting started Build with Claude Code Administration Configuration Reference
Agent SDK What's New Resources Settings and permissions Settings Permissions San ...

> ... it in ~/.claude/settings.json instead. Before v2.1.142, project settings could set auto . The
--permission-mode CLI flag overrides this setting for a single session "acceptEdits"
disableBypassPermissionsMode Set to "disable" to prevent bypassPermissions mode from being
activated. This disables the --dangerously-skip-permissions command-line flag. Typically placed in
managed settings t ...

> ... ons Claude Code settings Getting started Build with Claude Code Administration Configuration
Reference Agent SDK What's New Resources Settings and permissions Settings Permissions Sandbox
environments Bash sandbox Environments Cloud environments Model and responses Model configuration
Speed up responses with fast mode Escalate hard decisions with the advisor tool O ...

> ... , editor settings) Tools and plugins you use across all projects API keys and authentication
(stored securely) Project scope is best for: Team-shared settings (permissions, hooks, MCP servers)
Plugins the whole team should have Standardizing tooling across collaborators Local scope is best
for: Personal overrides for a specific project Testing configurations be ...

Potential config terms not found in local tool files:

`ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_ARTIFACT`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Code: Hooks documentation

- Change type: `content-changed`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/hooks
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... nput UserPromptSubmit decision control UserPromptExpansion UserPromptExpansion input
UserPromptExpansion decision control MessageDisplay MessageDisplay input MessageDisplay output
PreToolUse PreToolUse input PreToolUse decision control Defer a tool call for later
PermissionRequest PermissionRequest input PermissionRequest decision control Permission update
entries Pos ...

> ... Use PreToolUse input PreToolUse decision control Defer a tool call for later PermissionRequest
PermissionRequest input PermissionRequest decision control Permission update entries PostToolUse
PostToolUse input PostToolUse decision control PostToolUseFailure PostToolUseFailure input
PostToolUseFailure decision control PostToolBatch PostToolBatch input PostToolBatch deci ...

> ... askCompleted input TaskCompleted decision control Stop Stop input Stop decision control
StopFailure StopFailure input TeammateIdle TeammateIdle input TeammateIdle decision control
ConfigChange ConfigChange input ConfigChange decision control CwdChanged CwdChanged input CwdChanged
output DirectoryAdded DirectoryAdded input FileChanged FileChanged input FileChanged output ...

> ... on" : "session_start" }  InstructionsLoaded decision control InstructionsLoaded hooks have no
decision control. They can't block or modify instruction loading. Use this event for audit logging,
compliance tracking, or observability.  UserPromptSubmit Runs when the user submits a prompt, before
Claude processes it. This allows you to add additional context based ...

> ... tup , resume , clear , compact , fork Setup which CLI flag triggered setup init , maintenance
SessionEnd why the session ended clear , resume , logout , prompt_input_exit ,
bypass_permissions_disabled , other Notification notification type permission_prompt , idle_prompt ,
auth_success , elicitation_dialog , elicitation_complete , elicitation_response , agent_needs_inp
...

Potential config terms not found in local tool files:

`ANTHROPIC_MODEL`, `CLAUDE_MODEL`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Code: Dynamic workflows documentation

- Change type: `content-changed`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/workflows
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> Orchestrate subagents at scale with dynamic workflows - Claude Code Docs Documentation Index Fetch
the complete documentation index at: /docs/llms.txt Use this file to discover all available pages
before exploring further. Skip to ma ...

> ... and the Agent SDK . The same disable settings apply on every surface. To turn workflows off for
yourself: Toggle Dynamic workflows off in /config . Persists across sessions. Set
"disableWorkflows": true in ~/.claude/settings.json . Persists across sessions. Set
CLAUDE_CODE_DISABLE_WORKFLOWS=1 . Read at startup, so it applies wherever you set it. To turn
workflows off for y ...

> ... flows off for yourself: Toggle Dynamic workflows off in /config . Persists across sessions. Set
"disableWorkflows": true in ~/.claude/settings.json . Persists across sessions. Set
CLAUDE_CODE_DISABLE_WORKFLOWS=1 . Read at startup, so it applies wherever you set it. To turn
workflows off for your whole organization, set "disableWorkflows": true in managed settings , or use
the toggle on ...

> ... kflow Bundled workflows Watch the run Have Claude write a workflow Ask for a workflow in your
prompt Dismiss or turn off the keyword Where the keyword works Let Claude decide with ultracode
Approve the plan before it runs Save the workflow for reuse Distribute a workflow in a plugin Pass
input to a saved workflow Example workflow prompts Audit many files for the same ...

> ... sions. Set CLAUDE_CODE_DISABLE_WORKFLOWS=1 . Read at startup, so it applies wherever you set it.
To turn workflows off for your whole organization, set "disableWorkflows": true in managed settings
, or use the toggle on the Claude Code admin settings page. When workflows are disabled, the bundled
workflow commands are unavailable, the ultracode keyword no longer triggers a ...

Potential config terms not found in local tool files:

`CLAUDE_CODE_SUBAGENT_MODEL`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### GitHub Copilot: Organization policy documentation

- Change type: `content-changed`
- Source URL: https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> ... LI command reference CLI plugin reference CLI programmatic reference ACP server CLI
configuration directory Custom agents configuration Custom instructions support Hooks reference
Policy conflicts Supported surfaces for policies Managed settings reference Copilot allowlist
reference MCP allowlist enforcement Metrics data Copilot billing Models and pricing Billing ...

> Managing GitHub Copilot in your organization - GitHub Docs Skip to main content GitHub Docs Version:
Free, Pro, & Team Search or ask Copilot Search or ask Copilot Select language: current language is
English Search or ask Co ...

> ... MCP servers Spaces Create Copilot Spaces Collaborate with others Copilot for GitHub tasks Use
Copilot to create or update issues Create a PR summary Use the GitHub MCP Server from Copilot Chat
Use Copilot agents Get started Kick off a task Research, plan, iterate Manage agent sessions Copilot
code review Review Copilot output Set up Set up for self Install Copilot exten ...

> ... Cloud and local sandboxes Spark Copilot usage metrics All articles Copilot usage metrics
Prompting Prompt engineering Response customization Context MCP Spaces Repository indexing Content
exclusion Tools AI tools About Copilot integrations Models Default availability Bring your own key
Utility models Auto model selection FedRAMP models Base and LTS models Usage limits Billin ...

> ... d agent About cloud agent Agent management Custom agents About automations Rationale,
confidence, and approvals Access management MCP and cloud agent Risks and mitigations Copilot CLI
About Copilot CLI Comparing CLI features Copilot CLI in Actions Cancel and roll back Context
management About remote control Custom agents Autonomous task completion Parallel task ...

### GitHub Copilot: Content exclusion documentation

- Change type: `content-changed`
- Source URL: https://docs.github.com/en/copilot/managing-copilot/configuring-and-auditing-content-exclusion
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> Configure and audit content exclusion - GitHub Docs Skip to main content GitHub Docs Version: Free,
Pro, & Team Search or ask Copilot Search or ask Copilot Select language: current language is English
Search or ask Co ...

> ... pilot Learn how to prevent Copilot from accessing certain content. Reviewing changes to content
exclusions for GitHub Copilot You can monitor changes to content exclusions in your repositories and
organizations. Help and support Did you find what you needed? Yes No Privacy policy Help us make
these docs great! All GitHub docs are open source. See something that's wrong ...

> ... ons Analyze feedback Generate code Implement a feature Refactor code Improve code readability
Fix lint errors Refactor for optimization Refactor for sustainability Refactor design patterns
Refactor data access layers Decouple business logic Handle cross-cutting Simplify inheritance
hierarchies Fix database deadlocks Translate code Document code File issues without b ...

> ... lot requests (legacy) Billing overview (legacy) Monitor premium requests (legacy) Model
multipliers for annual plans (legacy) Agentic audit log events Agent session filters Review excluded
files Copilot usage metrics Copilot usage metrics data Interpret usage metrics Reconciling Copilot
usage metrics Copilot LoC metrics Team-level metrics Example schema Tutorials Al ...

> Configure and audit content exclusion - GitHub Docs Skip to main content GitHub Docs Version: Free,
Pro, & Team Search or ask Copilot Search or ask Copilot Select language: current language is Englis
...

### Codex CLI: OpenAI Codex repository

- Change type: `content-changed`
- Source URL: https://github.com/openai/codex
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... vigation Menu Toggle navigation Sign in Appearance settings Platform AI CODE CREATION GitHub
Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry
Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev
environments Issues Plan and track work Code Review Manage code changes ...

### Codex CLI: OpenAI Codex releases

- Change type: `content-changed`
- Source URL: https://api.github.com/repos/openai/codex/releases?per_page=10
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... n, WebSockets, redirects, and LM Studio connections. (#34479, #34509, #34655, #34678, #35023,
#35056, #35239)\n- Keep MCP connections and Apps tools current when authentication or configuration
changes, reconnecting closed servers without restarting healthy connections. (#34952, #34957,
#35028, #35144, #35146, #35151)\n- Preserve submitted messages, final responses, fail ...

> ... ed mention results. (#35000, #35021, #34775, #34778, #35365, #35375)\n- Fix Windows navigation
keys, reliably terminate sandboxed process trees, and preserve proxy settings during security
reviews. (#34625, #34624, #35036)\n- Retain more available skills under tight context budgets and
warn when skill catalogs must be truncated. (#34732, #34738, #34997)\n\n## Docume ...

> ... type": "application/octet-stream",         "digest":
"sha256:8e55bac532c56e75ed21fd1bcafb641b6dfec02127ea4ae9cf8e7e708e59b60f",         "label": "",
"name": "codex-windows-sandbox-setup",         "size": 1421,         "state": "uploaded"       },
{         "content_type": "application/x-msdos-program",         "digest":
"sha256:b7dd86881d468ac74160652 ...

> ... ix @copyberry\n- #34581 Add routing-card lexical skill selection @copyberry\n- #34588 Bind MCP
calls to captured catalog revisions @copyberry\n- #34590 Add keyed shell environment policy filters
@copyberry\n- #34597 Enforce exact values from managed config requirements @copyberry\n- #34598 Skip
missing paths in filesystem sandbox entries @copyberry\n- #34601 Sanit ...

Potential config terms not found in local tool files:

`McpConnectionSet`, `McpRuntime`, `forceRefetch`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Codex Desktop: OpenAI Codex repository

- Change type: `content-changed`
- Source URL: https://github.com/openai/codex
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> ... Codex CLI is a coding agent from OpenAI that runs locally on your computer. If you want Codex in
your code editor (VS Code, Cursor, Windsurf), install in your IDE. If you want the desktop app
experience, run codex app or visit the Codex App page . If you are looking for the cloud-based agent
from OpenAI, Codex Web , go to chatgpt.com/codex . Quickstart Installing a ...

### Codex Desktop: OpenAI Codex config reference

- Change type: `content-changed`
- Source URL: https://raw.githubusercontent.com/openai/codex/main/codex-rs/config.md
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> # Configuration docs moved This file has moved. Please see the latest configuration documentation
here: - Full config docs: [docs/config.md](https://github.com/openai/codex/blob/main/docs/ ...

### Continue.dev: Configuration reference

- Change type: `content-changed`
- Source URL: https://docs.continue.dev/reference
- Status: `200`
- Related repo paths: continue-dev/

Keyword snippets:

> config.yaml Reference | Continue Docs Search...  K Docs Blog IDE Extensions CLI Getting Started
Install Quick Start Customization Overview Features Agent Chat Autocomplete Edit Customiz ...

> ... e Docs Search...  K Docs Blog IDE Extensions CLI Getting Started Install Quick Start
Customization Overview Features Agent Chat Autocomplete Edit Customize Customization Overview Models
MCP servers Rules Prompts Model Providers Model Roles Deep Dives Reference config.yaml Reference
Migrating Config to YAML Continue Documentation MCP Server config.json Reference ( ...

> ... Rules Prompts Model Providers Model Roles Deep Dives Reference config.yaml Reference Migrating
Config to YAML Continue Documentation MCP Server config.json Reference (Deprecated) Context
Providers (Deprecated) @Codebase (Deprecated) @Docs (Deprecated) Guides How to Understand
Configuration Configuring Models, Rules, and Tools Codebase and Documentation Awareness U ...

> ... Search...  K Docs Blog IDE Extensions CLI Getting Started Install Quick Start Customization
Overview Features Agent Chat Autocomplete Edit Customize Customization Overview Models MCP servers
Rules Prompts Model Providers Model Roles Deep Dives Reference config.yaml Reference Migrating
Config to YAML Continue Documentation MCP Server config.json Reference (Depr ...

Potential config terms found upstream are already present in local tool files.

### Continue.dev: Continue repository

- Change type: `content-changed`
- Source URL: https://github.com/continuedev/continue
- Status: `200`
- Related repo paths: continue-dev/

Keyword snippets:

> ... ESTING.md TESTING.md docs-search-dark-mode-fix.png docs-search-dark-mode-fix.png package-
lock.json package-lock.json package.json package.json tsconfig.json tsconfig.json worktree-
config.yaml worktree-config.yaml View all files Repository files navigation README Code of conduct
Contributing Apache-2.0 license Security More items Continue Pioneering open-source coding a ...

> ... ce coding agent continue.dev Topics agent ai cli developer-tools open-source Resources Readme
Apache-2.0 license Code of conduct Code of conduct Contributing Contributing Security policy
Security policy Activity Custom properties Stars 35.3k stars Watchers 165 watching Forks 5.2k forks
Report repository Releases Used by Contributors Languages Footer  2026 GitHub, ...

> ... ut the Continue Docs . Final 2.0.0 Release We polished Continue and did a final 2.0.0 release of
the VS Code extension, CLI, and JetBrains plugin. This included removing anonymous telemetry,
pulling out authentication, squashing bugs, and more. VS Code CLI JetBrains Note: We recommend using
the Continue CLI instead of the JetBrains plugin. Contributors Thank you to t ...

### Windsurf: Windsurf documentation

- Change type: `content-changed`
- Source URL: https://docs.windsurf.com/
- Status: `200`
- Related repo paths: windsurf/

Keyword snippets:

> ... . Skip to main content Devin Docs home page English Search...  K Ask Assistant Support Devin
Devin Search... Navigation Getting Started Welcome to Devin Desktop Cloud CLI Desktop Enterprise Use
Cases API Federal Devin Desktop Editor Getting Started Set Up Install Devin Desktop FAQ Recommended
Extensions Models Adaptive Quick Review Tab Command Code Lenses Terminal Br ...

> ... ommended Extensions Models Adaptive Quick Review Tab Command Code Lenses Terminal Browser
Previews AI Commit Messages DeepWiki Codemaps Vibe and Replace Advanced Devin Local Agent Cascade
Context Awareness Troubleshooting Agent Command Center Agent Command Center Spaces Devin Agent
Client Protocol (preview) Building a custom ACP agent Releases Changelog Changelog ( ...

> ... Local Our next-generation agent harness, shared with Devin CLI. Runs on your machine as the
primary local agent. Usage Credits and usage. Terminal An upgraded Terminal experience. MCP MCP
servers extend the agent's capabilities. Memories Memories and rules help customize behavior.
Context Awareness Instantly understands your codebase. Advanced Advanced configur ...

> ... ins Changelog Get Started Features Cascade (JetBrains) Context Awareness Best Practices
Troubleshooting Accounts Usage Quota Analytics Teams & Enterprise Security FedRAMP Security Admin
Guide Reporting On this page Set Up Onboarding 1. Select your preferred theme 2. Log In / Sign Up 3.
Start Building with Devin! Things to Try Forgot to Import VS Code Configuratio ...

### Windsurf: Windsurf changelog

- Change type: `content-changed`
- Source URL: https://windsurf.com/changelog
- Status: `200`
- Related repo paths: windsurf/

Keyword snippets:

> ... r, scroll, and type faster and stay responsive while streaming. A brief remote-connection drop
no longer flashes a "disconnected" banner. You can now configure a session's network policy and
grant or deny network access requests inline from the chat, without switching to the web app. Devin
Local Devin Local customizations and the sidebar skills count now span all ...

> ... ins Changelog Get Started Features Cascade (JetBrains) Context Awareness Best Practices
Troubleshooting Accounts Usage Quota Analytics Teams & Enterprise Security FedRAMP Security Admin
Guide Reporting On this page v3.6.27 v3.6.22 v3.6.21 v3.5.17 v3.4.27 v3.4.22 v3.3.18 v3.2.28 v3.2.23
v3.2.19 v3.2.16 v3.1.7 v3.0.28 v3.0.21 v3.0.12 v2.3.15 v2.3.9 v2.2.17 v2.1.32 ...

> ... eases (Next) Windsurf Plugins Changelog Get Started Features Cascade (JetBrains) Context
Awareness Best Practices Troubleshooting Accounts Usage Quota Analytics Teams & Enterprise Security
FedRAMP Security Admin Guide Reporting On this page v3.6.27 v3.6.22 v3.6.21 v3.5.17 v3.4.27 v3.4.22
v3.3.18 v3.2.28 v3.2.23 v3.2.19 v3.2.16 v3.1.7 v3.0.28 v3.0.21 v3.0.12 v2.3.15 ...

> ... ent space and from a Devin Local session's sidebar context menu, and the Cascade panel's ...
menu now only offers the customization surfaces that apply to the agent you have open. MCP servers
reporting "Needs auth" now show an Authenticate button in the Devin Local MCP list, marketplace
card, and detail page, which clears the stored OAuth credentials and reruns ...

> ... connection failures under TLS-intercepting proxies. Devin Local Edits produced in autonomous
mode now produce reviewable diffs. ACU usage is now shown in the /usage command. Skill permissions:
frontmatter now applies to auto-approvals. Enterprise login policies are now enforced in the CLI.
Added a sandbox.excluded allow/ask/deny config (user and team settings) to run s ...

### Tabnine: Tabnine admin documentation

- Change type: `content-changed`
- Source URL: https://docs.tabnine.com/
- Status: `200`
- Related repo paths: tabnine/

Keyword snippets:

> ... ine Subscription Plans Support & Feedback Getting started Install Quickstart Guide Context
Engine Tabnine Agent Tabnine Chat Tabnine CLI Code Completions Tabnine's Prompting Guide
Administering Tabnine Private Installation Release Notes Powered by GitBook On this page For the
complete documentation index, see llms.txt . This page is also available as Markdown . C ...

> Overview | Tabnine Docs  Ctrl k Tabnine website Contact Sales More Welcome Overview Architecture
Security Privacy Protection Personalization AI Models Integrations System & Hardware Requirements
Supported Languages Supported IDEs Tabnine Subscription Plans Support & Feedback Getting started I
...

### Tabnine: Tabnine enterprise documentation

- Change type: `content-changed`
- Source URL: https://www.tabnine.com/enterprise
- Status: `200`
- Related repo paths: tabnine/

No configured watch keywords were found in the fetched content.

### Amazon Q Developer: Amazon Q Developer IAM reference

- Change type: `content-changed`
- Source URL: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonqdeveloper.html
- Status: `200`
- Related repo paths: amazon-q-developer/

No configured watch keywords were found in the fetched content.

### Gemini CLI: Gemini CLI settings schema

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> ... ription": "Settings configured remotely by enterprise admins.\n\n- Category: `Admin`\n- Requires
restart: `no`\n- Default: `{}`", "default": {}, "type": "object", "properties": {
"secureModeEnabled": { "title": "Secure Mode Enabled", "description": "If true, disallows YOLO mode
and \"Always allow\" options from being used.", "markdownDescription": "If true, disallows YOLO mo
...

> ... (allowlist).\n\n- Category: `Admin`\n- Requires restart: `no`\n- Default: `{}`", "default": {},
"type": "object", "additionalProperties": { "$ref": "#/$defs/MCPServerConfig" } }, "requiredConfig":
{ "title": "Required MCP Config", "description": "Admin-required MCP servers that are always
injected.", "markdownDescription": "Admin-required MCP servers that are always injec ...

> ... ng. Isolates individual tools instead of the entire CLI process.\n\n- Category: `Security`\n-
Requires restart: `yes`\n- Default: `false`", "default": false, "type": "boolean" },
"disableYoloMode": { "title": "Disable YOLO Mode", "description": "Disable YOLO mode, even if
enabled by a flag.", "markdownDescription": "Disable YOLO mode, even if enabled by a flag.\n\n-
Catego ...

> ... ownDescription": "Hide the current working directory in the footer.\n\n- Category: `UI`\n-
Requires restart: `no`\n- Default: `false`", "default": false, "type": "boolean" },
"hideSandboxStatus": { "title": "Hide Sandbox Status", "description": "Hide the sandbox status
indicator in the footer.", "markdownDescription": "Hide the sandbox status indicator in the foote
...

> ... sed by editors for validation and autocompletion.", "type": "string", "default":
"https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json" },
"mcpServers": { "title": "MCP Servers", "description": "Configuration for MCP servers.",
"markdownDescription": "Configuration for MCP servers.\n\n- Category: `Advanced`\n- Requires re ...

Potential config terms found upstream are already present in local tool files.

### Gemini CLI: Gemini CLI enterprise admin controls

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/admin/enterprise-controls.md
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> ... by users with sufficient privileges. In contrast, admin controls are immutable at the local
level, making them the preferred method for enforcing policy. ## Available Controls ### Strict Mode
**Enabled/Disabled** | Default: enabled If enabled, users will not be able to enter yolo mode. ###
Extensions **Enabled/Disabled** | Default: disabled If disabled, users will not ...

> ... the preferred method for enforcing policy. ## Available Controls ### Strict Mode
**Enabled/Disabled** | Default: enabled If enabled, users will not be able to enter yolo mode. ###
Extensions **Enabled/Disabled** | Default: disabled If disabled, users will not be able to use or
install extensions. See [Extensions](../extensions/index.md) for more details. ### MCP #### ...

> ... xtensions **Enabled/Disabled** | Default: disabled If disabled, users will not be able to use or
install extensions. See [Extensions](../extensions/index.md) for more details. ### MCP ####
Enabled/Disabled **Enabled/Disabled** | Default: disabled If disabled, users will not be able to use
MCP servers. See [MCP Server Integration](../tools/mcp-server.md) for mor ...

> ... ing from the local configuration, it will not be initialized. This ensures users maintain final
control over which permitted servers are actually active in their environment. #### Required MCP
Servers (preview) **Default**: empty Allows administrators to define MCP servers that are **always
injected** into the user's environment. Unlike the allowlist (which filters user-configu ...

> ... http`). Local execution fields (`command`, `args`, `env`, `cwd`) are not supported. - Required
servers can coexist with allowlisted servers - both features work independently. ### Unmanaged
Capabilities **Enabled/Disabled** | Default: disabled If disabled, users will not be able to use
certain features. Currently, this control disables Agent Skills. See [Agent Skills](../cli/skil ...

### Gemini CLI: Gemini CLI Agent Skills documentation

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/skills.md
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> # Agent Skills Agent Skills let you extend Gemini CLI with specialized expertise, procedural
workflows, and task-specific resources. Based on the [Agent Skills](https://agentskills.io) open
stan ...

> ... s and injects the name and description of all enabled skills into the system prompt. 2.
**Activation**: When Gemini identifies a task matching a skill's description, it calls the
`activate_skill` tool. 3. **Consent**: You will see a confirmation prompt in the UI detailing the
skill's name, purpose, and the directory path it will gain access to. 4. **Injection**: Upon your
...

> ... l to include built-in skills. gemini skills list --all # Install a skill from a Git repository
or local directory. # Use --consent to skip the security confirmation prompt. gemini skills install
https://github.com/user/repo.git --consent # Uninstall a skill. gemini skills uninstall my-skill
--scope workspace ``` #### Command options The skill management commands support s ...

> ... description of all enabled skills into the system prompt. 2. **Activation**: When Gemini
identifies a task matching a skill's description, it calls the `activate_skill` tool. 3.
**Consent**: You will see a confirmation prompt in the UI detailing the skill's name, purpose, and
the directory path it will gain access to. 4. **Injection**: Upon your approval: - The `SK ...

> ... self-contained directory that packages instructions and assets into a discoverable capability.
Unlike general context files ([GEMINI.md](./gemini-md.md)), which provide persistent workspace-wide
background, Skills represent **on-demand expertise**. This lets Gemini CLI maintain a vast library
of specialized capabilities-such as security auditing, cloud deployments, o ...

### Gemini CLI: Gemini CLI documentation

- Change type: `content-changed`
- Source URL: https://cloud.google.com/gemini/docs/codeassist/gemini-cli
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> ... ase notes Gemini for Google Cloud release notes Gemini Code Assist release notes Get started Set
up Gemini Code Assist Write better prompts Configure Gemini for Google Cloud admin settings overview
Turn off Gemini for Google Cloud products Gemini Code Assist Configure Gemini Code Assist Configure
Gemini Code Assist release channels Keyboard shortcuts Exclude files f ...

> ... pute Data analytics and pipelines Databases Distributed, hybrid, and multicloud Industry
solutions Migration Networking Observability and monitoring Security Storage Cross-product tools
close Access and resources management Costs and usage management Infrastructure as code SDK,
languages, frameworks, and tools / Console English Deutsch Espaol Espaol - Amrica L ...

### Google Gemini: Vertex AI Gemini safety settings

- Change type: `content-changed`
- Source URL: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters
- Status: `200`
- Related repo paths: google-gemini/

Keyword snippets:

> ... orm section of the Google Cloud console, go to the Agent Studio page. Go to Agent Studio Under
Create a new prompt , click any of the buttons to open the prompt design page. Click Safety settings
. The Safety settings dialog window opens. For each harm category, configure the selected threshold
value. Click Save . Example output for a blocked response The following is an e ...

> ... he response's Candidate.content field. It does not provide any feedback to the model.
Configurable content filters Content filters assess content against a list of harms. For each harm
category, the content filters assign one score based on the probability of the content being harmful
and another score based on the severity of harmful content. The configurable content fi ...

> ... ent based on your preferences. To see an example of getting started with Responsible AI with
Gemini API, run the "Responsible AI with Agent Platform Gemini API: Safety ratings and thresholds"
notebook in one of the following environments: Open in Colab | Open in Colab Enterprise | Open in
Agent Platform Workbench | View on GitHub Google's generative AI models are des ...

> ... ts Capabilities Safety Overview Responsible AI System instructions for safety Configure content
filters Gemini for safety filtering and content moderation Abuse monitoring Process blocked
responses Content Credentials AI Content Detection API Text and code generation Text generation
System instructions Function calling Structured output Content generation parameter ...

> Safety and content filters | Gemini Enterprise Agent Platform | Google Cloud Documentation Skip to
main content Technology areas close AI and ML Application development Application hosting Compute
Data anal ...

### Google Gemini: Google Cloud organization policies

- Change type: `content-changed`
- Source URL: https://cloud.google.com/resource-manager/docs/organization-policy/overview
- Status: `200`
- Related repo paths: google-gemini/

Keyword snippets:

> Organization Policy overview | Google Cloud Documentation Skip to main content Technology areas
close AI and ML Application development Application hosting Compute Data analytics and pipelines
Databa ...

> ... nce Resources Cross-product tools More Console Discover Product overview Hierarchy evaluation
Get started Enforce an organization policy Create resource restrictions Create custom constraints
Create organization policies Test custom constraints with Gemini Cloud Assist Test organization
policies Apply organization policies Scope organization policies with tags Manage b ...

> ... licies Scope organization policies with tags Manage baseline constraints Configure service
restrictions Restrict IAM service account usage Restrict service usage Restrict resource locations
Disable Cloud Logging for the Cloud Healthcare API Restrict identities Domain-restricted sharing
Restrict identities with domain-restricted sharing Monitor Audit logging for Organ ...

> ... rict resource locations Disable Cloud Logging for the Cloud Healthcare API Restrict identities
Domain-restricted sharing Restrict identities with domain-restricted sharing Monitor Audit logging
for Organization Policy Troubleshoot Troubleshoot organization policies AI and ML Application
development Application hosting Compute Data analytics and pipelines Database ...

### Claude Desktop: Claude Desktop MCP documentation

- Change type: `content-changed`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/mcp
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... h credentials Override OAuth metadata discovery Restrict OAuth scopes Use dynamic headers for
custom authentication Add MCP servers from JSON configuration Import MCP servers from Claude Desktop
Use MCP servers from claude.ai Organization controls on connector tools Disable claude.ai connectors
Use Claude Code as an MCP server MCP output limits and warnings Raise the limi ...

> Connect Claude Code to tools via MCP - Claude Code Docs Documentation Index Fetch the complete
documentation index at: /docs/llms.txt Use this file to discover all available pages before
exploring further. Skip to ma ...

> ... bleshooting Troubleshoot installation and login Troubleshoot performance and stability Debug
configuration Error reference On this page What you can do with MCP Find and build MCP servers
Installing MCP servers Option 1: Add a remote HTTP server Option 2: Add a remote SSE server Option
3: Add a local stdio server Option 4: Add a remote WebSocket server Managing yo ...

> ... eveloper Platform Claude Code on the Web Claude Code on the Web Search... Navigation MCP Connect
Claude Code to tools via MCP Getting started Build with Claude Code Administration Configuration
Reference Agent SDK What's New Resources Agents and parallel work Overview Create custom subagents
Agent view Run agent teams Dynamic workflows Isolate sessions with worktrees MCP ...

Potential config terms not found in local tool files:

`CLAUDE_AUTO_BACKGROUND_TASKS`, `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`, `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Desktop: Claude Desktop support documentation

- Change type: `content-changed`
- Source URL: https://support.anthropic.com/en/
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... 78 articles Pro and Max plans 15 articles Team and Enterprise plans 62 articles Identity
management (SSO, JIT, SCIM) 15 articles Claude Cowork 10 articles Claude Code 20 articles Claude
Desktop 9 articles Claude Mobile apps 15 articles Claude API and Console 40 articles Connectors 22
articles Claude in Chrome 5 articles Claude for Education 4 articles Claude for Nonprofi ...

> ... Italiano   Portugus P  Espaol  English Search for answers or browse by topic Search for
articles... Claude 78 articles Pro and Max plans 15 articles Team and Enterprise plans 62 articles
Identity management (SSO, JIT, SCIM) 15 articles Claude Cowork 10 articles Claude Code 20 articles
Claude Desktop 9 articles Claude Mobile apps 15 articles Claud ...

### OpenAI Platform: OpenAI OpenAPI repository

- Change type: `content-changed`
- Source URL: https://github.com/openai/openai-openapi
- Status: `200`
- Related repo paths: openai-platform/

Keyword snippets:

> ... ple when possible. The OpenAI team will make a best-effort attempt to triage and resolve spec
issues. For immediate help with the OpenAI API, contact OpenAI Support . License This project is
licensed under the MIT License . About OpenAPI specification for the OpenAI API
platform.openai.com/docs/api-reference/introduction Topics openai openai-api Resources Readme MI ...

### OpenAI Platform: OpenAI OpenAPI schema

- Change type: `content-changed`
- Source URL: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
- Status: `200`
- Related repo paths: openai-platform/

Keyword snippets:

> ... ng/checkpoints/{fine_tuned_model_checkpoint}/permissions: get: operationId:
listFineTuningCheckpointPermissions tags: - Fine-tuning summary: > **NOTE:** This endpoint requires
an [admin API key](../admin-api-keys). Organization owners can use this endpoint to view all
permissions for a fine-tuned model checkpoint. parameters: - in: path name: fine_tuned_model_che ...

> ... iption: Given text and/or image inputs, classifies if those inputs are potentially harmful. -
name: Audit Logs description: List user actions and configuration changes within this organization.
paths: /assistants: get: operationId: listAssistants tags: - Assistants summary: Returns a list of
assistants. deprecated: true parameters: - name: limit in: query description: > ...

> ... and describe the various models available in the API. - name: Moderations description: Given
text and/or image inputs, classifies if those inputs are potentially harmful. - name: Audit Logs
description: List user actions and configuration changes within this organization. paths:
/assistants: get: operationId: listAssistants tags: - Assistants summary: Returns a ...

> ... used in multi-turn conversations when using the Responses API statelessly (like when the `store`
parameter is set to `false`, or when an organization is enrolled in the zero data retention
program). responses: "200": description: OK content: application/json: schema: $ref:
"#/components/schemas/ConversationItemList" x-oaiMeta: name: List items group: conversations p ...

> ... type": "skill_reference", "skill_id": "skill_4db6f1a2c9e73508b41f9da06e2c7b5f" }, { "type":
"skill_reference", "skill_id": "openai-spreadsheets", "version": "latest" } ], "network_policy": {
"type": "allowlist", "allowed_domains": ["api.buildkite.com"] } }' response: | { "id":
"cntr_682e30645a488191b6363a0cbefc0f0a025ec61b66250591", "object": "container", "created ...

Potential config terms not found in local tool files:

`allowed_tools`, `checkpoint.permission`, `enabled_for_all_projects`, `enabled_for_selected_projects`, `enabled_per_call`, `label_model`, `mcp`, `mcp_approval_request`, `mcp_approval_response`, `mcp_call`, `mcp_list_tools`, `mcp_list_tools.completed`, `mcp_list_tools.failed`, `mcp_list_tools.in_progress`, `moderation_result`, `moderation_results`, `organization.data_retention`, `project.data_retention`, `project.model_permissions`, `project.model_permissions.deleted`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude API: Anthropic admin API documentation

- Change type: `content-changed`
- Source URL: https://platform.claude.com/docs/en/api/admin.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... ion applies to. - `"all_connectors"` - `type: "rbac_role_permission"` Object type. For RBAC Role
Permissions, this is always `"rbac_role_permission"`. - `"rbac_role_permission"` # Workspaces ##
Create Workspace **post** `/v1/organizations/workspaces` Create Workspace ### Header Parameters -
`"anthropic-beta": optional array of string` Optional header to specify the b ...

> ... there is no seat-tier parameter. When no seat is free the request fails with a 400 error rather
than purchasing a seat. ### Body Parameters - `email: string` Email of the User. - `role: "billing"
or "claude_code_user" or "developer" or 2 more` Role for the invited User. The accepted values
depend on the organization type. Console and API organizations accept `us ...

> # Admin # Organizations ## Get Current Organization **get** `/v1/organizations/me` Retrieve
information about the organization associated with the authenticated API key. ### Returns -
`Organization object { id, name, type }` - `id: string` ID of the Organization. - `name: string`
Name of the Organization. - `type: "organization"` Object type. For ...

> ... Workspace Members, this is always `"workspace_member_deleted"`. - `"workspace_member_deleted"` -
`user_id: string` ID of the User. - `workspace_id: string` ID of the Workspace. # Rate Limits ##
List Workspace Rate Limits **get** `/v1/organizations/workspaces/{workspace_id}/rate_limits` List
rate-limit overrides configured for a workspace. Returns only the groups and ...

> # Admin # Organizations ## Get Current Organization **get** `/v1/organizations/me` Retrieve
information about the organization associated with the authenticated API key. ### Returns - `Or ...

Potential config terms not found in local tool files:

`always_allow`, `fast-mode-2026-02-01`, `mcp-tunnels-2026-05-19`, `model_group`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude API: Anthropic API release notes

- Change type: `content-changed`
- Source URL: https://platform.claude.com/docs/en/release-notes/api.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... [Claude Opus 4.8](/docs/en/about-claude/models/migration-guide). Read more in [Fast
mode](/docs/en/build-with-claude/fast-mode#supported-models). ### June 26, 2026 * We've raised [rate
limits](/docs/en/api/rate-limits) across the Claude API. Claude Sonnet and Claude Haiku rate limits
now match Claude Opus at every usage tier, and usage tiers have been consolidated int ...

> ... t API moved from `/v1/organizations/tunnels` on the Admin API to `/v1/tunnels` on the Claude
API. The new surface uses the `anthropic-beta: mcp-tunnels-2026-06-22` header and the
`workspace:manage_tunnels` WIF scope. The previous surface remains available during a migration
window. See the [Tunnels API reference](/docs/en/api/beta/tunnels). ### June 18, 2026 * The Py ...

> ... custom roles. Group and custom-role requests require the `anthropic-beta: ce-user-
management-2026-07-13` beta header; member and invite requests take no beta header. An Admin API key
with the `read:org_audit` scope can also call every user-management `GET` endpoint. See [User
management](/docs/en/manage-claude/user-management). ### July 10, 2026 * [Dreams](/do ...

> ... d custom-role requests require the `anthropic-beta: ce-user-management-2026-07-13` beta header;
member and invite requests take no beta header. An Admin API key with the `read:org_audit` scope can
also call every user-management `GET` endpoint. See [User management](/docs/en/manage-claude/user-
management). ### July 10, 2026 * [Dreams](/docs/en/managed-agents/drea ...

> ... ks-libraries/cli/quickstart). ### April 7, 2026 * We announced [Claude Mythos
Preview](https://anthropic.com/glasswing) is available as a gated research preview for defensive
cybersecurity work as part of [Project Glasswing](https://anthropic.com/glasswing). Access is
invitation-only. * The [Messages API](/docs/en/api/messages) is now available on Amazon Bedrock as
...

Potential config terms not found in local tool files:

`LanguageModel`, `LanguageModelSession`, `fast-mode-2026-02-01`, `mcp_oauth`, `model_context_window_exceeded`, `policy_violation_investigation`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

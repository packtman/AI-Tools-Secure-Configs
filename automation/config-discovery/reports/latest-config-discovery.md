# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | fingerprint-method-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/settings |
| Claude Code | Hooks documentation | fingerprint-method-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Claude Code | Dynamic workflows documentation | fingerprint-method-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/workflows |
| Cursor | Team administration documentation | fingerprint-method-changed | 200 | https://docs.cursor.com/en/account/teams/admin-dashboard |
| Cursor | MCP documentation | fingerprint-method-changed | 200 | https://docs.cursor.com/en/tools/mcp |
| GitHub Copilot | Organization policy documentation | fingerprint-method-changed | 200 | https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization |
| GitHub Copilot | Content exclusion documentation | fingerprint-method-changed | 200 | https://docs.github.com/en/copilot/managing-copilot/configuring-and-auditing-content-exclusion |
| Codex CLI | OpenAI Codex repository | fingerprint-method-changed | 200 | https://github.com/openai/codex |
| Codex CLI | OpenAI Codex releases | fingerprint-method-changed | 200 | https://api.github.com/repos/openai/codex/releases?per_page=10 |
| Codex Desktop | OpenAI Codex repository | fingerprint-method-changed | 200 | https://github.com/openai/codex |
| Codex Desktop | OpenAI Codex config reference | fingerprint-method-changed | 200 | https://raw.githubusercontent.com/openai/codex/main/codex-rs/config.md |
| Continue.dev | Configuration reference | fingerprint-method-changed | 200 | https://docs.continue.dev/reference |
| Continue.dev | Continue repository | fingerprint-method-changed | 200 | https://github.com/continuedev/continue |
| Windsurf | Windsurf documentation | fingerprint-method-changed | 200 | https://docs.windsurf.com/ |
| Windsurf | Windsurf changelog | fingerprint-method-changed | 200 | https://windsurf.com/changelog |
| Tabnine | Tabnine admin documentation | fingerprint-method-changed | 200 | https://docs.tabnine.com/ |
| Tabnine | Tabnine enterprise documentation | fingerprint-method-changed | 200 | https://www.tabnine.com/enterprise |
| Amazon Q Developer | Amazon Q Developer administration guide | fingerprint-method-changed | 200 | https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-admin.html |
| Amazon Q Developer | Amazon Q Developer IAM reference | fingerprint-method-changed | 200 | https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonqdeveloper.html |
| Gemini CLI | Gemini CLI repository | fingerprint-method-changed | 200 | https://github.com/google-gemini/gemini-cli |
| Gemini CLI | Gemini CLI documentation | fingerprint-method-changed | 200 | https://cloud.google.com/gemini/docs/codeassist/gemini-cli |
| Google Gemini | Vertex AI Gemini safety settings | fingerprint-method-changed | 200 | https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters |
| Google Gemini | Google Cloud organization policies | fingerprint-method-changed | 200 | https://cloud.google.com/resource-manager/docs/organization-policy/overview |
| Claude Desktop | Claude Desktop MCP documentation | fingerprint-method-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Claude Desktop | Claude Desktop support documentation | fingerprint-method-changed | 200 | https://support.anthropic.com/en/ |
| OpenAI Platform | OpenAI OpenAPI repository | fingerprint-method-changed | 200 | https://github.com/openai/openai-openapi |
| OpenAI Platform | OpenAI OpenAPI schema | fingerprint-method-changed | 200 | https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml |
| Claude API | Anthropic admin API documentation | fingerprint-method-changed | 200 | https://platform.claude.com/docs/en/api/admin.md |
| Claude API | Anthropic API release notes | fingerprint-method-changed | 200 | https://platform.claude.com/docs/en/release-notes/api.md |

## Review Details

### Claude Code: Managed settings documentation

- Change type: `fingerprint-method-changed`
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

> ... so a repository cannot grant itself auto mode. Set it in ~/.claude/settings.json instead. The
--permission-mode CLI flag overrides this setting for a single session "acceptEdits"
disableBypassPermissionsMode Set to "disable" to prevent bypassPermissions mode from being
activated. This disables the --dangerously-skip-permissions command-line flag. Typically placed in
managed settings t ...

> ... ons Claude Code settings Getting started Build with Claude Code Administration Configuration
Reference Agent SDK What's New Resources Settings and permissions Settings Permissions Sandbox
environments Bash sandbox Model and responses Model configuration Speed up responses with fast mode
Escalate hard decisions with the advisor tool Output styles Interface Terminal ...

> ... , editor settings) Tools and plugins you use across all projects API keys and authentication
(stored securely) Project scope is best for: Team-shared settings (permissions, hooks, MCP servers)
Plugins the whole team should have Standardizing tooling across collaborators Local scope is best
for: Personal overrides for a specific project Testing configurations be ...

Potential config terms not found in local tool files:

`--fallback-model`, `--permission-mode`, `--settings`, `--teammate-mode`, `ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, `allowLocalBinding`, `allowUnixSockets`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Code: Hooks documentation

- Change type: `fingerprint-method-changed`
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
output FileChanged FileChanged input FileChanged output WorktreeCreate WorktreeCreate input ...

> ... n" : "session_start" }  InstructionsLoaded decision control InstructionsLoaded hooks have no
decision control. They cannot block or modify instruction loading. Use this event for audit logging,
compliance tracking, or observability.  UserPromptSubmit Runs when the user submits a prompt, before
Claude processes it. This allows you to add additional context based ...

> ... ed startup , resume , clear , compact Setup which CLI flag triggered setup init , maintenance
SessionEnd why the session ended clear , resume , logout , prompt_input_exit ,
bypass_permissions_disabled , other Notification notification type permission_prompt , idle_prompt ,
auth_success , elicitation_dialog , elicitation_complete , elicitation_response SubagentStart age
...

Potential config terms not found in local tool files:

`--allow-dangerously-skip-permissions`, `--permission-mode`, `ANTHROPIC_MODEL`, `CLAUDE_MODEL`, `PermissionDenied`, `PermissionRequest`, `localSettings`, `mcp_server_name`, `my-mcp-server`, `permission_mode`, `permission_prompt`, `permission_suggestions`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Code: Dynamic workflows documentation

- Change type: `fingerprint-method-changed`
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

> ... ce On this page When to use a workflow Run a bundled workflow Bundled workflows Watch the run
Have Claude write a workflow Ask for a workflow in your prompt Let Claude decide with ultracode
Approve the plan before it runs Save the workflow for reuse Pass input to a saved workflow How a
workflow runs Behavior and limits Manage runs Resume after a pause Cost Turn workf ...

> ... sions. Set CLAUDE_CODE_DISABLE_WORKFLOWS=1 . Read at startup, so it applies wherever you set it.
To turn workflows off for your whole organization, set "disableWorkflows": true in managed settings
, or use the toggle on the Claude Code admin settings page. When workflows are disabled, the bundled
workflow commands are unavailable, the ultracode keyword no longer triggers a ...

Potential config terms found upstream are already present in local tool files.

### Cursor: Team administration documentation

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.cursor.com/en/account/teams/admin-dashboard
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

No configured watch keywords were found in the fetched content.

### Cursor: MCP documentation

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.cursor.com/en/tools/mcp
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

Keyword snippets:

> Cursor Docs - Agent, Rules, MCP, Skills & CLI

### GitHub Copilot: Organization policy documentation

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> ... LI command reference CLI plugin reference CLI programmatic reference ACP server CLI
configuration directory Custom agents configuration Custom instructions support Hooks reference
Policy conflicts Supported surfaces for policies Copilot allowlist reference MCP allowlist
enforcement Metrics data Copilot billing Models and pricing Billing cycle Seat assignment Licen ...

> Managing GitHub Copilot in your organization - GitHub Docs Skip to main content GitHub Docs Version:
Free, Pro, & Team Search or ask Copilot Search or ask Copilot Select language: current language is
English Search or ask Co ...

> ... MCP servers Spaces Create Copilot Spaces Collaborate with others Copilot for GitHub tasks Use
Copilot to create or update issues Create a PR summary Use the GitHub MCP Server from Copilot Chat
Use Copilot agents Get started Kick off a task Research, plan, iterate Manage agent sessions Copilot
code review Review Copilot output Set up Set up for self Install Copilot exten ...

> ... Cloud and local sandboxes Spark Copilot usage metrics All articles Copilot usage metrics
Prompting Prompt engineering Response customization Context MCP Spaces Repository indexing Content
exclusion Tools AI tools About Copilot integrations Models Utility models Auto model selection
FedRAMP models Base and LTS models Usage limits Billing Billing for individuals Billing for or ...

> ... ons Code referencing Chat Agents Cloud agent About cloud agent Agent management Custom agents
About automations Access management MCP and cloud agent Risks and mitigations Copilot CLI About
Copilot CLI Comparing CLI features Cancel and roll back About remote control Custom agents About CLI
plugins Autonomous task completion Parallel task execution Researching w ...

### GitHub Copilot: Content exclusion documentation

- Change type: `fingerprint-method-changed`
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

- Change type: `fingerprint-method-changed`
- Source URL: https://github.com/openai/codex
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... vigation Menu Toggle navigation Sign in Appearance settings Platform AI CODE CREATION GitHub
Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry
New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant
dev environments Issues Plan and track work Code Review Manage code chan ...

### Codex CLI: OpenAI Codex releases

- Change type: `fingerprint-method-changed`
- Source URL: https://api.github.com/repos/openai/codex/releases?per_page=10
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... delete`, `/delete`, and app-server `thread/delete`, with confirmation safeguards and subagent
cleanup. (#25018, #27476)\n- Added `/import` for selectively importing setup, project configuration,
and recent chats from Claude Code. (#27070, #27071, #27703)\n- Typing `@` now opens the unified
mentions menu for files, plugins, and skills by default. (#27499)\n- Added managed ...

> ... type": "application/octet-stream",         "digest":
"sha256:f328de200721ab9a0fb1ecb91949b6b58a8485b72b5fbf647b7e43f563a81ef7",         "label": "",
"name": "codex-windows-sandbox-setup",         "size": 1421,         "state": "uploaded"       },
{         "content_type": "application/x-msdos-program",         "digest":
"sha256:fc634a39d177dc42090a6ef ...

> ... 700 Remove fs/join and fs/parent from exec-server protocol @anp-oai\n- #26426 Warn when
hooks.json has unsupported top-level fields @abhinav-oai\n- #27318 [codex] Move persistence policy
application into ThreadStore @wiltzius-openai\n- #27498 Route image extension reads through turn
environments v2 @won-openai\n- #27623 Add spans to turn lifecycle gaps @mchen-oai\ ...

Potential config terms not found in local tool files:

`codex-windows-sandbox-setup`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe.tar.gz`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe.zip`, `codex-windows-sandbox-setup-aarch64-pc-windows-msvc.exe.zst`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe.tar.gz`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe.zip`, `codex-windows-sandbox-setup-x86_64-pc-windows-msvc.exe.zst`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Codex Desktop: OpenAI Codex repository

- Change type: `fingerprint-method-changed`
- Source URL: https://github.com/openai/codex
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> ... Codex CLI is a coding agent from OpenAI that runs locally on your computer. If you want Codex in
your code editor (VS Code, Cursor, Windsurf), install in your IDE. If you want the desktop app
experience, run codex app or visit the Codex App page . If you are looking for the cloud-based agent
from OpenAI, Codex Web , go to chatgpt.com/codex . Quickstart Installing a ...

### Codex Desktop: OpenAI Codex config reference

- Change type: `fingerprint-method-changed`
- Source URL: https://raw.githubusercontent.com/openai/codex/main/codex-rs/config.md
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> # Configuration docs moved This file has moved. Please see the latest configuration documentation
here: - Full config docs: [docs/config.md](../docs/config.md) - MCP servers section: [docs ...

### Continue.dev: Configuration reference

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.continue.dev/reference
- Status: `200`
- Related repo paths: continue-dev/

Keyword snippets:

> config.yaml Reference | Continue - Docs Search...  K IDE Extensions CLI Getting Started Install
Quick Start Customization Overview Features Agent Chat Autocomplete Edit Customize Custom ...

> ... Continue - Docs Search...  K IDE Extensions CLI Getting Started Install Quick Start
Customization Overview Features Agent Chat Autocomplete Edit Customize Customization Overview Models
MCP servers Rules Prompts Model Providers Model Roles Deep Dives Reference config.yaml Reference
Migrating Config to YAML Continue Documentation MCP Server config.json Reference ( ...

> ... Rules Prompts Model Providers Model Roles Deep Dives Reference config.yaml Reference Migrating
Config to YAML Continue Documentation MCP Server config.json Reference (Deprecated) Context
Providers (Deprecated) @Codebase (Deprecated) @Docs (Deprecated) Guides How to Understand
Configuration Configuring Models, Rules, and Tools Codebase and Documentation Awareness U ...

> ... ue - Docs Search...  K IDE Extensions CLI Getting Started Install Quick Start Customization
Overview Features Agent Chat Autocomplete Edit Customize Customization Overview Models MCP servers
Rules Prompts Model Providers Model Roles Deep Dives Reference config.yaml Reference Migrating
Config to YAML Continue Documentation MCP Server config.json Reference (Depr ...

Potential config terms not found in local tool files:

`mcpServers`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Continue.dev: Continue repository

- Change type: `fingerprint-method-changed`
- Source URL: https://github.com/continuedev/continue
- Status: `200`
- Related repo paths: continue-dev/

Keyword snippets:

> ... ESTING.md TESTING.md docs-search-dark-mode-fix.png docs-search-dark-mode-fix.png package-
lock.json package-lock.json package.json package.json tsconfig.json tsconfig.json worktree-
config.yaml worktree-config.yaml View all files Repository files navigation README Code of conduct
Contributing Apache-2.0 license Security Continue Pioneering open-source coding agent What i ...

> ... g agent continue.dev Topics agent cli open-source ai developer-tools Resources Readme License
Apache-2.0 license Code of conduct Code of conduct Contributing Contributing Security policy
Security policy Uh oh! There was an error while loading. Please reload this page . Activity Custom
properties Stars 33.8k stars Watchers 159 watching Forks 4.7k forks Report repos ...

> ... ut the Continue Docs . Final 2.0.0 Release We polished Continue and did a final 2.0.0 release of
the VS Code extension, CLI, and JetBrains plugin. This included removing anonymous telemetry,
pulling out authentication, squashing bugs, and more. VS Code CLI JetBrains Note: We recommend using
the Continue CLI instead of the JetBrains plugin. Contributors Thank you to t ...

### Windsurf: Windsurf documentation

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.windsurf.com/
- Status: `200`
- Related repo paths: windsurf/

Keyword snippets:

> ... . Skip to main content Devin Docs home page English Search...  K Ask Assistant Support Devin
Devin Search... Navigation Getting Started Welcome to Devin Desktop Cloud CLI Desktop Enterprise Use
Cases API Devin Desktop Editor Getting Started Set Up Devin Desktop FAQ Recommended Extensions
Models Adaptive Quick Review Tab Command Code Lenses Terminal Browser Previews A ...

> ... in Desktop FAQ Recommended Extensions Models Adaptive Quick Review Tab Command Code Lenses
Terminal Browser Previews AI Commit Messages DeepWiki Codemaps Vibe and Replace Advanced Cascade
Accounts Context Awareness Troubleshooting Security Agent Command Center Agent Command Center Spaces
Devin Devin Local Agent Agent Client Protocol (preview) Building a custom ACP ...

> ... Local Our next-generation agent harness, shared with Devin CLI. Runs on your machine as the
primary local agent. Usage Credits and usage. Terminal An upgraded Terminal experience. MCP MCP
servers extend the agent's capabilities. Memories Memories and rules help customize behavior.
Context Awareness Instantly understands your codebase. Advanced Advanced configur ...

### Windsurf: Windsurf changelog

- Change type: `fingerprint-method-changed`
- Source URL: https://windsurf.com/changelog
- Status: `200`
- Related repo paths: windsurf/

Keyword snippets:

> ... ascade Download 1.13.12  v1.13.9 January 16, 2026  Bug Fixes and Improvements Improvements to
GPT-5.2-Codex harness Admins can now manage Windsurf restrictions via Windows Group Policy Download
1.13.9  v1.13.8 January 14, 2026  GPT-5.2-Codex Adds support for GPT-5.2-Codex with four reasoning
efforts (low, medium, high, and xhigh). GPT-5.2-Codex is OpenAI's lat ...

> ... rolling out gradually. If you don't see it yet, try logging out of the website and IDE then
logging back in. Devin Cloud is disabled by default for enterprise accounts. Enterprise admins
should enable Devin access in their organization settings if they have already purchased Cognition
Platform.  Agent Command Center New Kanban-style view showing all local and cl ...

> ... tant Support Devin Devin Search... Navigation Releases Changelog Cloud CLI Desktop Enterprise
Use Cases API Devin Desktop Editor Cascade Accounts Context Awareness Troubleshooting Security Agent
Command Center Agent Command Center Spaces Devin Devin Local Agent Agent Client Protocol (preview)
Building a custom ACP agent Releases Changelog Changelog (Next) Releases R ...

> ... enhancements and continued Devin Desktop polish. Devin Local Added a devin plugin system for
extending Devin Local - in preview and opt-in for enterprises. Subagents can now call MCP tools
directly. Teams can enforce terminal allow/deny lists through CLI permission scopes. Agent and
Editor modes Enabled the Cmd+. mode-toggle shortcut from the empty editor welc ...

> ... le scroll-to-next-hunk settings (default off) Preserved colors and styling in Cascade terminal
output Multiple fixes to the Model Context Protocol implementation Supports lowering permissions for
Cascade's Web Fetch tool Fix race condition in the dedicated terminal implementation Support force
killing commands in the dedicated terminal Improved markdown completion Fix ...

### Tabnine: Tabnine admin documentation

- Change type: `fingerprint-method-changed`
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

- Change type: `fingerprint-method-changed`
- Source URL: https://www.tabnine.com/enterprise
- Status: `200`
- Related repo paths: tabnine/

No configured watch keywords were found in the fetched content.

### Amazon Q Developer: Amazon Q Developer administration guide

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-admin.html
- Status: `200`
- Related repo paths: amazon-q-developer/

No configured watch keywords were found in the fetched content.

### Amazon Q Developer: Amazon Q Developer IAM reference

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonqdeveloper.html
- Status: `200`
- Related repo paths: amazon-q-developer/

Keyword snippets:

> Actions, resources, and condition keys for Amazon Q Developer - Service Authorization Reference View
a markdown version of this page Actions, resources, and condition keys for Amazon Q De ...

> Actions, resources, and condition keys for Amazon Q Developer - Service Authorization Reference View
a markdown version of this page Actions, resources, and condition keys for Amazon Q Developer -
Service Authorization ...

> ... ctions, resources, and condition keys for Amazon Q Developer - Service Authorization Reference
Documentation Identity and Access Management Service Authorization Reference Actions Resource types
Condition keys Actions, resources, and condition keys for Amazon Q Developer Amazon Q Developer
(service prefix: qdeveloper ) provides the following service-specific resources, ac ...

> ... ion keys for Amazon Q Developer Actions defined by Amazon Q Developer You can specify the
following actions in the Action element of an IAM policy statement. Use policies to grant
permissions to perform an operation in AWS. When you use an action in a policy, you usually allow or
deny access to the API operation or CLI command with the same name. However, in some cases ...

> ... pes defined by Amazon Q Developer Condition keys for Amazon Q Developer Actions defined by
Amazon Q Developer You can specify the following actions in the Action element of an IAM policy
statement. Use policies to grant permissions to perform an operation in AWS. When you use an action
in a policy, you usually allow or deny access to the API operation or CLI comma ...

### Gemini CLI: Gemini CLI repository

- Change type: `fingerprint-method-changed`
- Source URL: https://github.com/google-gemini/gemini-cli
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> ... uide - Common issues and solutions. FAQ - Frequently asked questions. Use /bug command to report
issues directly from the CLI. Using MCP Servers Configure MCP servers in ~/.gemini/settings.json to
extend Gemini CLI with custom tools: > @github List my open pull requests > @slack Send a summary of
today's commits to #dev channel > @database Run a query to find inactive us ...

> ... ols. Custom Extensions - Build and share your own commands. Advanced Topics Headless Mode
(Scripting) - Use Gemini CLI in automated workflows. IDE Integration - VS Code companion. Sandboxing
& Security - Safe execution environments. Trusted Folders - Control execution policies by folder.
Enterprise Guide - Deploy and manage in a corporate environment. Telemetry & M ...

> ... vigation Menu Toggle navigation Sign in Appearance settings Platform AI CODE CREATION GitHub
Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry
New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant
dev environments Issues Plan and track work Code Review Manage code chan ...

> ... nion. Sandboxing & Security - Safe execution environments. Trusted Folders - Control execution
policies by folder. Enterprise Guide - Deploy and manage in a corporate environment. Telemetry &
Monitoring - Usage tracking. Tools reference - Built-in tools overview. Local development - Local
development tooling. Troubleshooting & Support Troubleshooting Guide - Common i ...

> ... tegrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev
environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub
Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret
protection Stop leaks before they start EXPLORE Why GitHub Documentation B ...

### Gemini CLI: Gemini CLI documentation

- Change type: `fingerprint-method-changed`
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

- Change type: `fingerprint-method-changed`
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
Vertex AI Workbench | View on GitHub Google's generative AI models, like Gemini ...

> ... ts Capabilities Safety Overview Responsible AI System instructions for safety Configure content
filters Gemini for safety filtering and content moderation Abuse monitoring Process blocked
responses Content Credentials AI Content Detection API Text and code generation Text generation
System instructions Function calling Structured output Content generation parameter ...

> Safety and content filters | Gemini Enterprise Agent Platform | Google Cloud Documentation Skip to
main content Technology areas close AI and ML Application development Application hosting Compute
Data anal ...

Potential config terms not found in local tool files:

`BLOCKED_REASON_UNSPECIFIED`, `blockReason`, `safetySettings`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Google Gemini: Google Cloud organization policies

- Change type: `fingerprint-method-changed`
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

- Change type: `fingerprint-method-changed`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/mcp
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... h credentials Override OAuth metadata discovery Restrict OAuth scopes Use dynamic headers for
custom authentication Add MCP servers from JSON configuration Import MCP servers from Claude Desktop
Use MCP servers from Claude.ai Use Claude Code as an MCP server MCP output limits and warnings Raise
the limit for a specific tool Respond to MCP elicitation requests Use MCP reso ...

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

`--channels`, `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Desktop: Claude Desktop support documentation

- Change type: `fingerprint-method-changed`
- Source URL: https://support.anthropic.com/en/
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... les Pro and Max plans 15 articles Team and Enterprise plans 63 articles Claude API and Console
40 articles Identity management (SSO, JIT, SCIM) 15 articles Claude Code 19 articles Claude Desktop
9 articles Claude Mobile apps 20 articles Connectors 20 articles Claude in Chrome 5 articles Claude
for Education 4 articles Claude for Nonprofits 6 articles Privacy and legal 22 ...

> ... Italiano   Portugus P  Espaol  English Search for answers or browse by topic Search for
articles... Claude 84 articles Pro and Max plans 15 articles Team and Enterprise plans 63 articles
Claude API and Console 40 articles Identity management (SSO, JIT, SCIM) 15 articles Claude Code 19
articles Claude Desktop 9 articles Claude Mobile apps 20 artic ...

### OpenAI Platform: OpenAI OpenAPI repository

- Change type: `fingerprint-method-changed`
- Source URL: https://github.com/openai/openai-openapi
- Status: `200`
- Related repo paths: openai-platform/

No configured watch keywords were found in the fetched content.

### OpenAI Platform: OpenAI OpenAPI schema

- Change type: `fingerprint-method-changed`
- Source URL: https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml
- Status: `200`
- Related repo paths: openai-platform/

Keyword snippets:

> ... ng/checkpoints/{fine_tuned_model_checkpoint}/permissions: get: operationId:
listFineTuningCheckpointPermissions tags: - Fine-tuning summary: > **NOTE:** This endpoint requires
an [admin API key](../admin-api-keys). Organization owners can use this endpoint to view all
permissions for a fine-tuned model checkpoint. parameters: - in: path name: fine_tuned_model_che ...

> ... ion: >- Given text and/or image inputs, classifies if those inputs are potentially harmful. -
name: Audit Logs description: List user actions and configuration changes within this organization.
paths: /assistants: get: operationId: listAssistants tags: - Assistants summary: Returns a list of
assistants. deprecated: true parameters: - name: limit in: query description: > ...

> ... d describe the various models available in the API. - name: Moderations description: >- Given
text and/or image inputs, classifies if those inputs are potentially harmful. - name: Audit Logs
description: List user actions and configuration changes within this organization. paths:
/assistants: get: operationId: listAssistants tags: - Assistants summary: Returns a ...

> ... used in multi-turn conversations when using the Responses API statelessly (like when the `store`
parameter is set to `false`, or when an organization is enrolled in the zero data retention
program). responses: '200': description: OK content: application/json: schema: $ref:
'#/components/schemas/ConversationItemList' x-oaiMeta: name: List items group: conversations p ...

> ... type": "skill_reference", "skill_id": "skill_4db6f1a2c9e73508b41f9da06e2c7b5f" }, { "type":
"skill_reference", "skill_id": "openai-spreadsheets", "version": "latest" } ], "network_policy": {
"type": "allowlist", "allowed_domains": ["api.buildkite.com"] } }' node.js: >- import OpenAI from
'openai'; const client = new OpenAI({ apiKey: process.env['OPENAI_API_KEY'], ...

Potential config terms not found in local tool files:

`VAR_chat_model_id`, `VAR_completion_model_id`, `allowed_domains`, `allowed_tools`, `api.model.request`, `channels`, `checkpoint.permission`, `custom-model-name`, `enabled_for_all_projects`, `enabled_for_selected_projects`, `enabled_per_call`, `event_CEKKrf1KTGvemCPyiJTJ2`, `fine_tuned_model`, `fine_tuned_model_checkpoint`, `label_model`, `mcp`, `mcp_682d437d90a88191bf88cd03aae0c3e503937d5f622d7a90`, `mcp_approval_request`, `mcp_approval_response`, `mcp_call`, `mcp_call_001`, `mcp_list_tools`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude API: Anthropic admin API documentation

- Change type: `fingerprint-method-changed`
- Source URL: https://platform.claude.com/docs/en/api/admin.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... erDeleteResponse object { id, type }` - `id: string` ID of the User. - `type: "user_deleted"`
Deleted object type. For Users, this is always `"user_deleted"`. - `"user_deleted"` # Workspaces ##
Create Workspace **post** `/v1/organizations/workspaces` Create Workspace ### Header Parameters -
`"anthropic-beta": optional array of string` Optional header to specify the b ...

> ... ways `"organization"`. - `"organization"` # Invites ## Create Invite **post**
`/v1/organizations/invites` Create Invite ### Body Parameters - `email: string` Email of the User. -
`role: "user" or "developer" or "billing" or "claude_code_user"` Role for the invited User. Cannot
be "admin". - `"user"` - `"developer"` - `"billing"` - `"claude_code_user"` ### Return ...

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

`allowed_inference_geos`, `fast-mode-2026-02-01`, `jwks_polling_disabled_at`, `mcp-atlassian`, `mcp-tunnels-2026-05-19`, `model_breakdown`, `model_group`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude API: Anthropic API release notes

- Change type: `fingerprint-method-changed`
- Source URL: https://platform.claude.com/docs/en/release-notes/api.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... s 4.7. Set `speed: "fast"` with `model: "claude-opus-4-7"` and the `fast-mode-2026-02-01` beta
header for significantly faster output token generation at premium pricing. Pricing, rate limits,
and access are the same as for Opus 4.6 fast mode; interested customers should join the
[waitlist](https://claude.com/fast-mode). ### May 11, 2026 - We've launched **Claude Plat ...

> ... 've released the [Rate Limits API](/docs/en/manage-claude/rate-limits-api), allowing
administrators to programmatically query the rate limits configured for their organization and
workspaces. ### April 23, 2026 - Memory for Claude Managed Agents is now in public beta under the
standard `managed-agents-2026-04-01` header. See [Using agent memory](/docs/en/managed-agen ...

> ... de any `tools` when including `tool_use` and `tool_result` blocks. - We've launched an OpenAI-
compatible API endpoint, allowing you to test Claude models by changing just your API key, base URL,
and model name in existing OpenAI integrations. This compatibility layer supports core chat
completions functionality. Learn more in [OpenAI SDK compatibility](/docs/en ...

> ... ks-libraries/cli/quickstart). ### April 7, 2026 - We announced [Claude Mythos
Preview](https://anthropic.com/glasswing) is available as a gated research preview for defensive
cybersecurity work as part of [Project Glasswing](https://anthropic.com/glasswing). Access is
invitation-only. - The [Messages API](/docs/en/api/messages) is now available on Amazon Bedrock as
...

Potential config terms not found in local tool files:

`disabled`, `fast-mode-2026-02-01`, `mcp_oauth`, `model_context_window_exceeded`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

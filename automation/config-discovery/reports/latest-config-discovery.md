# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/settings |
| Claude Code | Hooks documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Claude Code | Dynamic workflows documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/workflows |
| Claude Code | Settings reference | new-source-baseline | 200 | https://code.claude.com/docs/en/settings-reference.md |
| Cursor | Team administration documentation | content-changed | 200 | https://docs.cursor.com/en/account/teams/admin-dashboard |
| Cursor | MCP documentation | content-changed | 200 | https://docs.cursor.com/en/tools/mcp |
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
| Gemini CLI | Gemini CLI repository | content-changed | 200 | https://github.com/google-gemini/gemini-cli |
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

> ... t apply A value you set is ignored A managed change hasn't reached you A committed key doesn't
reach teammates Permission rules combine differently than you expected Exceptions to managed
settings precedence Settings in cloud sessions What's next Settings Claude Code settings Copy page
Copy page Change Claude Code settings, pick the scope a key belongs in, verify the change ...

> ... s Getting started Build with Claude Code Administration Configuration Reference Agent SDK What's
New Resources Settings Settings overview Settings reference Example settings files Permissions and
sandboxing Permissions Permission modes Bash sandbox Sandbox environments Environments Cloud
environments Self-hosted environments Model and responses Model configuration Spee ...

> ... d Build with Claude Code Administration Configuration Reference Agent SDK What's New Resources
Settings Settings overview Settings reference Example settings files Permissions and sandboxing
Permissions Permission modes Bash sandbox Sandbox environments Environments Cloud environments Self-
hosted environments Model and responses Model configuration Speed up respons ...

> ... sion history, and plugins there instead. Claude Code also keeps a fifth file, ~/.claude.json ,
that it writes for itself; you don't need to edit it. It holds your sign-in session, MCP server
configurations, per-project state such as trust decisions, and the global config keys that /config
writes for you.  Share settings with your team Commit .claude/settings.j ...

Potential config terms not found in local tool files:

`ANTHROPIC_DEFAULT_MODEL`, `ANTHROPIC_MODEL`

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
PostToolUse input PostToolUse decision control Annotate a result for the auto mode classifier
PostToolUseFailure PostToolUseFailure input PostToolUseFailure decision control PostT ...

> ... askCompleted input TaskCompleted decision control Stop Stop input Stop decision control
StopFailure StopFailure input TeammateIdle TeammateIdle input TeammateIdle decision control
ConfigChange ConfigChange input ConfigChange decision control CwdChanged CwdChanged input CwdChanged
output DirectoryAdded DirectoryAdded input FileChanged FileChanged input FileChanged output ...

> ... s have no decision control. They can't block or modify instruction loading. Claude Code discards
their JSON output fields , such as systemMessage and continue . Use this event for audit logging,
compliance tracking, or observability.  UserPromptSubmit Runs when the user submits a prompt, before
Claude processes it. This allows you to add additional context based ...

> ... the transcript cwd Current working directory when the hook is invoked permission_mode Current
permission mode : "default" , "plan" , "acceptEdits" , "auto" , "dontAsk" , or "bypassPermissions" .
The mode labeled Manual arrives as "default" , never as "manual" , so scripts that match "default"
keep working. Not all events receive this field. Check the JSON example in ea ...

Potential config terms not found in local tool files:

`ANTHROPIC_MODEL`, `CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`, `CLAUDE_MODEL`

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

`CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Code: Settings reference

- Change type: `new-source-baseline`
- Source URL: https://code.claude.com/docs/en/settings-reference.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... ltracode) | Have Claude plan a [workflow](/docs/en/workflows#let-claude-decide-with-ultracode)
for each substantive task without being asked | Model and responses | Any file | |
[`useAutoModeDuringPlan`](#useautomodeduringplan) | Let the [auto mode](/docs/en/permission-
modes#eliminate-prompts-with-auto-mode) classifier review shell commands in [plan
mode](/docs/en/permission-mod ...

> ... tifact`](#disableartifact) | Turn the [Artifact tool](/docs/en/artifacts) off for everyone; use
`enableArtifact` for yourself | Remote, desktop, and notifications | Any file | |
[`disableAutoMode`](#disableautomode) | Remove [auto mode](/docs/en/permission-modes#eliminate-
prompts-with-auto-mode) from the permission mode cycle | Permission settings | Any file | |
[`disableB ...

> ... sonly) | Make the managed [MCP](/docs/en/mcp) allowlist the only one that applies | MCP |
Managed | | [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly) | Make [managed
settings](/docs/en/managed-settings) the only source of [permission
rules](/docs/en/permissions#managed-settings) | Permission settings | Managed | |
[`alwaysThinkingEnabled`](#alwaysthink ...

> ... naged | | [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly) | Make [managed
settings](/docs/en/managed-settings) the only source of [permission
rules](/docs/en/permissions#managed-settings) | Permission settings | Managed | |
[`alwaysThinkingEnabled`](#alwaysthinkingenabled) | Turn [extended thinking](/docs/en/model-
config#extended-thinking) off for ...

> ... ssPermissions mode](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) |
Permission settings | Any file | | [`plansDirectory`](#plansdirectory) | Choose where [plan
mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) writes plan files | Memory
and context | Any file | | [`pluginConfigs`](#pluginconfigs) | Store the answers you ...

Potential config terms not found in local tool files:

`ANTHROPIC_DEFAULT_MODEL`, `ANTHROPIC_MODEL`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`, `CLAUDE_CODE_DISABLE_ARTIFACT`, `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`, `CLAUDE_CODE_DISABLE_FAST_MODE`, `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`, `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`, `DISABLE_AUTO_COMPACT`, `DISABLE_DOCTOR_COMMAND`, `DISABLE_ERROR_REPORTING`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Cursor: Team administration documentation

- Change type: `content-changed`
- Source URL: https://docs.cursor.com/en/account/teams/admin-dashboard
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

Keyword snippets:

> ... ngs API Origin Overview CLI Create a repository Clone, Push & Pull Mirror GitHub Pull requests
Browse & Search Settings Codebase settings Integrations Integrations Slack Microsoft Teams Jira
Linear Notion GitHub GitLab Azure DevOps Bitbucket JetBrains Xcode Deeplinks SDK TypeScript Python
Bridge Changelog CLI Overview Installation Capabilities Changelog Shell Mo ...

### Cursor: MCP documentation

- Change type: `content-changed`
- Source URL: https://docs.cursor.com/en/tools/mcp
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

Keyword snippets:

> Cursor Docs - Agent, Rules, MCP, Skills & CLI Skip to main content Cursor Logo Docs API Learn Help
Search docs... K Sign in Download Command Palette Search for a command to run... Get Started Welcome
Quickstart ...

> ... Palette Search for a command to run... Get Started Welcome Quickstart Models & Pricing Changelog
Agent Overview Agents Window Agent Review Planning Prompting Debugging Design Mode Tools Security
Customize Overview Plugins Rules Skills Subagents Hooks MCP Cloud Agents Overview Setup Builds
Capabilities Best Practices Automations Bugbot Security Agents PR Routing & ...

> ... Security Customize Overview Plugins Rules Skills Subagents Hooks MCP Cloud Agents Overview Setup
Builds Capabilities Best Practices Automations Bugbot Security Agents PR Routing & Approval Mobile
Security Settings API Origin Overview CLI Create a repository Clone, Push & Pull Mirror GitHub Pull
requests Browse & Search Settings Codebase settings Integrations Integra ...

### GitHub Copilot: Organization policy documentation

- Change type: `content-changed`
- Source URL: https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> ... LoC metrics Team-level metrics Example schema Enterprise administrators Agent session filters
Agentic audit log events Enterprise managed settings MCP private registry enforcement Policy
conflicts Tutorials All tutorials GitHub Copilot Cookbook All prompts Communicate effectively Create
templates Summarize repository activity Synthesize research Create diagrams Ge ...

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

> ... legacy) What changed with billing (legacy) Copilot requests (legacy) Billing overview (legacy)
Monitor premium requests (legacy) Model multipliers for annual plans (legacy) Review excluded files
Copilot usage metrics Copilot usage metrics data Interpret usage metrics Reconciling Copilot usage
metrics Copilot LoC metrics Team-level metrics Example schema Enterprise a ...

> Configure and audit content exclusion - GitHub Docs Skip to main content GitHub Docs Version: Free,
Pro, & Team Search or ask Copilot Search or ask Copilot Select language: current language is Englis
...

### Codex CLI: OpenAI Codex repository

- Change type: `content-changed`
- Source URL: https://github.com/openai/codex
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... Skip to content Navigation Menu Sign in Appearance settings Platform AI CODE CREATION GitHub
Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry
Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev
environments Issues Plan and track work Code Review Manage code changes ...

### Codex CLI: OpenAI Codex releases

- Change type: `content-changed`
- Source URL: https://api.github.com/repos/openai/codex/releases?per_page=10
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... e telemetry shutdown worker during initialization @copyberry\n- #39051 Use installed callable
apps for TUI mentions @copyberry\n- #39055 Add network policy metadata to environment configuration
@copyberry\n- #39056 Verify the pinned zsh manifest in release builds @copyberry\n- #39057 Rate-
limit TUI frames from their actual emission time @copyberry\n- #39058 Tag Codex App ...

> ... ry\n- #39064 Restrict queued-message editing to its dedicated binding @copyberry\n- #39065 Limit
terminal hyperlink layout to the visible viewport @copyberry\n- #39067 Add desktop security
enforcement diagnostics @copyberry\n- #39068 Remove skill model delegation support @copyberry\n-
#39072 Persist generated images through turn executors @copyberry\n- #39073 Propag ...

> ... type": "application/octet-stream",         "digest":
"sha256:3d86b58561a6b5b40bb7a0ede89f2acc260d8fdb5ef5066a447c5a480f4de7b3",         "label": "",
"name": "codex-windows-sandbox-setup",         "size": 1421,         "state": "uploaded"       },
{         "content_type": "application/x-msdos-program",         "digest":
"sha256:e969c2d27545c763c309565 ...

> ... handshakes @copyberry\n- #38893 Restore thread timestamp maxima independently @copyberry\n-
#38894 Add working-directory commands to the TUI @copyberry\n- #38899 Move requirements policy
ownership to execpolicy @copyberry\n- #38902 Honor per-environment shell variable policies
@copyberry\n- #38907 Edit queued messages with Vim history-up @copyberry\n- #38913 Stop ...

> ... 39609 Limit Bazel integration test threads on macOS @copyberry\n- #39611 Harden MCP OAuth
fallback credential writes @copyberry\n- #39614 Prevent `apply_patch` from widening write
permissions @copyberry\n- #39615 Bind MCP OAuth refresh tokens to their issuer @copyberry\n- #39616
Validate linked worktrees before inheriting project trust @copyberry\n- #39618 Apply compos ...

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
Security policy Activity Custom properties Stars 35.6k stars Watchers 163 watching Forks 5.3k forks
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

> ... the fork in a new tab, keeping the original conversation open. "Grant access" on a network
access request is disabled with an explanation when an admin owns the session's network policy.
Download 3.7.16  v3.6.27 August 1, 2026 Fixed Devin Desktop for Windows loads root and intermediate
certificates from the Windows certificate store again, so sign-in and other H ...

> ... ins Changelog Get Started Features Cascade (JetBrains) Context Awareness Best Practices
Troubleshooting Accounts Usage Quota Analytics Teams & Enterprise Security FedRAMP Security Admin
Guide Reporting On this page v3.8.20 v3.7.25 v3.7.16 v3.6.27 v3.6.22 v3.6.21 v3.5.17 v3.4.27 v3.4.22
v3.3.18 v3.2.28 v3.2.23 v3.2.19 v3.2.16 v3.1.7 v3.0.28 v3.0.21 v3.0.12 v2.3.15 ...

> ... eases (Next) Windsurf Plugins Changelog Get Started Features Cascade (JetBrains) Context
Awareness Best Practices Troubleshooting Accounts Usage Quota Analytics Teams & Enterprise Security
FedRAMP Security Admin Guide Reporting On this page v3.8.20 v3.7.25 v3.7.16 v3.6.27 v3.6.22 v3.6.21
v3.5.17 v3.4.27 v3.4.22 v3.3.18 v3.2.28 v3.2.23 v3.2.19 v3.2.16 v3.1.7 v3.0.28 ...

> ... copied in before the session starts. New settings control whether integrated terminal activity
and local user-edit activity are shared with ACP agents (both remain on by default). mcp_config.json
no longer shows spurious "Property is not allowed" warnings. Up/down arrows in the chat input once
again navigate through previous prompts. Fixed the migration wizard ...

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

### Gemini CLI: Gemini CLI repository

- Change type: `content-changed`
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

> ... Skip to content Navigation Menu Sign in Appearance settings Platform AI CODE CREATION GitHub
Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry
Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev
environments Issues Plan and track work Code Review Manage code changes ...

> ... nion. Sandboxing & Security - Safe execution environments. Trusted Folders - Control execution
policies by folder. Enterprise Guide - Deploy and manage in a corporate environment. Telemetry &
Monitoring - Usage tracking. Tools reference - Built-in tools overview. Local development - Local
development tooling. Troubleshooting & Support Troubleshooting Guide - Common i ...

> ... LOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track
work Code Review Manage code changes Code Quality Enforce quality at merge APPLICATION SECURITY
GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build
Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation B ...

### Gemini CLI: Gemini CLI documentation

- Change type: `content-changed`
- Source URL: https://cloud.google.com/gemini/docs/codeassist/gemini-cli
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> ... rn off Gemini for Google Cloud products Get started Set up Gemini Code Assist Write better
prompts Gemini Code Assist Configure Gemini Code Assist Gemini Code Assist administrator settings
Configure Gemini Code Assist release channels Keyboard shortcuts Exclude files from Gemini Code
Assist use Configure local codebase awareness Configure Gemini Code Assist logging ...

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
System instructions Structured output Content generation parameters Image generatio ...

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

> ... authentication Where the helper runs Which variables a helper can read Trust a folder before its
headersHelper runs Add MCP servers from JSON configuration Import MCP servers from Claude Desktop
Use MCP servers from claude.ai Organization controls on connector tools Disable claude.ai connectors
Use Claude Code as an MCP server MCP output limits and warnings Raise the limi ...

> Connect Claude Code to tools via MCP - Claude Code Docs Documentation Index Fetch the complete
documentation index at: /docs/llms.txt Use this file to discover all available pages before
exploring further. Skip to ma ...

> ... bleshooting Troubleshoot installation and login Troubleshoot performance and stability Debug
configuration Error reference On this page What you can do with MCP Find and build MCP servers
Installing MCP servers Option 1: Add a remote HTTP server Option 2: Add a remote SSE server Option
3: Add a local stdio server Option 4: Add a remote WebSocket server Add a serve ...

> ... eveloper Platform Claude Code on the Web Claude Code on the Web Search... Navigation MCP Connect
Claude Code to tools via MCP Getting started Build with Claude Code Administration Configuration
Reference Agent SDK What's New Resources Agents and parallel work Overview Create custom subagents
Agent view Run agent teams Cross-session messaging Dynamic workflows Isolate ses ...

Potential config terms not found in local tool files:

`CLAUDE_AUTO_BACKGROUND_TASKS`, `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`, `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Desktop: Claude Desktop support documentation

- Change type: `content-changed`
- Source URL: https://support.anthropic.com/en/
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... ter prompts Claude Code cheatsheet Claude Code user FAQ Claude Code power user tips Claude Code:
Common developer use cases Claude Code communications kit Claude Code champion kit Claude Desktop
General Install Claude Desktop Deploy Claude Desktop for Windows Deploy Claude Desktop for macOS
Enterprise configuration for Claude Desktop Use quick entry with Claude Desktop on ...

> ... nt? Managing your active sessions Understanding your billing address and tax calculation Notice
regarding consumption tax (JCT) for Japanese customers Configuring session security settings How to
get support for Claude for Government Public Sector FAQs Claude 4 Invite Contest Conversation
management Delete or rename a conversation Share and unshare chats Use incogni ...

> ... Pro plan? How do I sign up for the Pro plan? How to change your Pro plan from monthly to annual
billing Max plan What is the Max plan? How do I sign up for the Max plan? Team and Enterprise plans
Plan overviews What is the Enterprise plan? What is the Team plan? Get started Get started with the
Team plan Move your personal Claude account to a Team or Enterprise organ ...

> ... our Team plan from monthly to annual billing Add or update your Team plan's tax or VAT ID Cancel
your organization's Team plan subscription How am I billed for my Enterprise plan? Admin management
Roles and permissions Purchase and manage seats on Team plans Purchase and manage seats on
Enterprise plans Manage members on Team and Enterprise plans Claude Enterpris ...

> ...  K Claude Release notes Get started with Claude Get started with Claude What are some things I
can use Claude for? Where can I access Claude? How up-to-date is Claude's training data? What
interfaces can I use to access Claude? Choose a Claude plan Verify your phone number How to gift a
Claude subscription How to redeem a Claude gift subscription Account manag ...

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
"#/components/schemas/ConversationItemList" "429": $ref: "#/components/responses/TooManyReques ...

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

> ... s/en/api/admin --- # Admin # Organizations ## Get Current Organization **get**
`/v1/organizations/me` Retrieve information about the organization associated with the authenticated
API key. ### Returns - `Organization object { id, name, type }` - `id: string` ID of the
Organization. - `name: string` Name of the Organization. - `type: "organization"` Object type. For
...

> ... Workspace Members, this is always `"workspace_member_deleted"`. - `"workspace_member_deleted"` -
`user_id: string` ID of the User. - `workspace_id: string` ID of the Workspace. # Rate Limits ##
List Workspace Rate Limits **get** `/v1/organizations/workspaces/{workspace_id}/rate_limits` List
rate-limit overrides configured for a workspace. Returns only the groups and ...

> --- title: Admin url: https://platform.claude.com/docs/en/api/admin --- # Admin # Organizations ##
Get Current Organization **get** `/v1/organizations/me` Retrieve information about the organizati
...

Potential config terms not found in local tool files:

`always_allow`, `fast-mode-2026-02-01`, `mcp-tunnels-2026-05-19`, `model_group`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude API: Anthropic API release notes

- Change type: `content-changed`
- Source URL: https://platform.claude.com/docs/en/release-notes/api.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... about-claude/models/migration-guide). Read more in [Fast
mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode#supported-models). ### June
26, 2026 * We've raised [rate limits](https://platform.claude.com/docs/en/api/rate-limits) across
the Claude API. Claude Sonnet and Claude Haiku rate limits now match Claude Opus at every usage
tier, and usage tiers ...

> ... ce_user_data` scope. See [Sessions on users'
machines](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-
sessions). * We've added the `anthropic-workspace-id` response header to the Claude API. It carries
the `wrkspc_`-prefixed ID of the workspace that the request's API key or access token resolved to,
including your organization's ...

> ... {session_id}` retrieves one session's metadata, and `GET
/v1/compliance/apps/sessions/local/{session_id}/messages` returns its transcript, all with your
existing Compliance Access Key and the `read:compliance_user_data` scope. See [Sessions on users'
machines](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-
sessions). * We'v ...

> ... d custom-role requests require the `anthropic-beta: ce-user-management-2026-07-13` beta header;
member and invite requests take no beta header. An Admin API key with the `read:org_audit` scope can
also call every user-management `GET` endpoint. See [User
management](https://platform.claude.com/docs/en/manage-claude/user-management). ### July 10, 2026 *
[Dreams](h ...

> ... t and available to the agent for that session. ### August 5, 2026 * **Inference hooks** are now
in beta for Claude Enterprise organizations. Point Claude at your organization's AI security server,
and each governed prompt across claude.ai, Cowork, and Claude Code is held for the server's allow or
deny verdict before inference proceeds. Requests are signed, failure h ...

Potential config terms not found in local tool files:

`LanguageModel`, `LanguageModelSession`, `allowed_domains`, `blocked_domains`, `fast-mode-2026-02-01`, `mcp_oauth`, `model_context_window_exceeded`, `permission_policy`, `policy_violation_investigation`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

## This run (2026-08-23)

Config update applied: Claude Code `useAutoModeDuringPlan: false` on Moderate and Strict. Baseline remains unset (vendor default `true`). Watcher added: `https://code.claude.com/docs/en/settings-reference.md`.

### No config update needed (scoped scanner terms)

- `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_MODEL`, `CLAUDE_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL`: session and default-model overrides, not an org allowlist. Model allowlists are `availableModels` plus `enforceAvailableModels` (open PR #89). Do not pin model IDs in managed `env`.
- `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `DISABLE_AUTO_COMPACT`: autocompact window is covered by open PR #80.
- `CLAUDE_CODE_AUTO_CONNECT_IDE`, `CLAUDE_CODE_DISABLE_AGENT_VIEW`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`, `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`: IDE and agent-view env flags, covered by open PR #68. Not plan-mode approval controls.
- `CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`: notification preference, not an admin lock.
- `CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`: workflow timing, not a security gate. Workflows stay off via `disableWorkflows` on Moderate and Strict.
- Remaining `CLAUDE_CODE_DISABLE_*` / `DISABLE_*` scanner hits from the settings reference: developer UX or traffic flags, not new managed permission controls for this run.

Deferred (not unique this run): Continue `mcpServers` (open #75), Claude Desktop `CLAUDE_CODE_MCP_SERVER_*` (not Desktop keys), OpenAI Platform MCP schema terms, Codex 0.148-plus (still alpha; latest observed `rust-v0.150.0-alpha.7`), `disableSideloadFlags` (open #61), Gemini #64+#76 after merge, Managed Agents Dreams org kill switch.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

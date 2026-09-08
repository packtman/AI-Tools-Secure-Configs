# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/settings |
| Claude Code | Hooks documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Claude Code | Settings reference | content-changed | 200 | https://code.claude.com/docs/en/settings-reference.md |
| Claude Code | MCP documentation | content-changed | 200 | https://code.claude.com/docs/en/mcp.md |
| Claude Code | Desktop documentation | new-source-baseline | 200 | https://code.claude.com/docs/en/desktop |
| Cursor | Team administration documentation | content-changed | 200 | https://docs.cursor.com/en/account/teams/admin-dashboard |
| Cursor | MCP documentation | content-changed | 200 | https://docs.cursor.com/en/tools/mcp |
| GitHub Copilot | Organization policy documentation | content-changed | 200 | https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization |
| GitHub Copilot | Content exclusion documentation | content-changed | 200 | https://docs.github.com/en/copilot/managing-copilot/configuring-and-auditing-content-exclusion |
| Codex CLI | OpenAI Codex repository | content-changed | 200 | https://github.com/openai/codex |
| Codex CLI | OpenAI Codex releases | content-changed | 200 | https://api.github.com/repos/openai/codex/releases?per_page=10 |
| Codex Desktop | OpenAI Codex repository | content-changed | 200 | https://github.com/openai/codex |
| Continue.dev | Continue repository | content-changed | 200 | https://github.com/continuedev/continue |
| Tabnine | Tabnine admin documentation | content-changed | 200 | https://docs.tabnine.com/ |
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

> ... laude Code is lost in new sessions A managed change hasn't reached you A committed key doesn't
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

`ANTHROPIC_DEFAULT_MODEL`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed: `ANTHROPIC_DEFAULT_MODEL` is a session model pick, not an org allowlist. Do not pin it as a substitute for `availableModels` (open PR #89).

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

`CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed: `CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS` is a notification UX toggle, not a permission or hook lock.

### Claude Code: Settings reference

- Change type: `content-changed`
- Source URL: https://code.claude.com/docs/en/settings-reference.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... (#disablebundledskills) | Turn off the [skills](/docs/en/skills#bundled-skills) and
[workflows](/docs/en/workflows) included with Claude Code | Plugins and skills | Any file | |
[`disableClaudeAiConnectors`](#disableclaudeaiconnectors) | Turn off [claude.ai
connectors](/docs/en/mcp#disable-claude-ai-connectors) so Claude Code doesn't fetch them | MCP | Any
file | | [`disableCommandP ...

> ... ) | Let Claude send a [push notification to your phone](/docs/en/remote-control#mobile-push-
notifications) when it decides to | Remote, desktop, and notifications | Any file | |
[`allowAllClaudeAiMcps`](#allowallclaudeaimcps) | Load the [claude.ai connectors](/docs/en/mcp)
Claude Code fetches itself alongside a deployed [`managed-mcp.json`](/docs/en/managed-mcp#exclusive-
contro ...

> ... tions | Managed | | [`disabledMcpjsonServers`](#disabledmcpjsonservers) | Reject specific
servers from a project's [`.mcp.json`](/docs/en/mcp#project-scope) | MCP | Any file | |
[`disableMobileSimulatorTools`](#disablemobilesimulatortools) | Block Claude's tools in the
[desktop](/docs/en/desktop) iOS Simulator pane | Tools | Managed | |
[`disableRemoteControl`](#disableremotecontrol) ...

> ... sonly) | Make the managed [MCP](/docs/en/mcp) allowlist the only one that applies | MCP |
Managed | | [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly) | Make [managed
settings](/docs/en/managed-settings) the only settings source of [permission
rules](/docs/en/permissions#managed-settings) | Permission settings | Managed | |
[`alwaysThinkingEnabled`](#al ...

> ... [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly) | Make [managed
settings](/docs/en/managed-settings) the only settings source of [permission
rules](/docs/en/permissions#managed-settings) | Permission settings | Managed | |
[`alwaysThinkingEnabled`](#alwaysthinkingenabled) | Turn [extended thinking](/docs/en/model-
config#extended-thinking) off for ...

Potential config terms not found in local tool files:

`ANTHROPIC_CUSTOM_MODEL_OPTION`, `ANTHROPIC_DEFAULT_MODEL`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_CODE_DISABLE_ADVISOR_TOOL`, `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`, `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`, `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING`, `DISABLE_AUTO_COMPACT`, `DISABLE_DOCTOR_COMMAND`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

Config update applied from this source: pin `disableMobileSimulatorTools: true` on Moderate and Strict (Baseline unset). Vendor default is unset, so Claude can tap, screenshot, and capture devices in the Desktop iOS Simulator pane. Managed only. The terminal CLI ignores this key. People keep manual use of the pane. Only the JSON boolean `true` takes effect (the string `"true"` is ignored). Distinct from computer use and from Desktop Browser pane keys (open PR #108). No env-var substitute.

No config update needed for the other missing terms: `ANTHROPIC_*` names are session model picks, not org allowlists. Remaining `CLAUDE_CODE_*` / `DISABLE_*` names are session UX, one-session kills, or keys already covered in open PRs.

### Claude Code: MCP documentation

- Change type: `content-changed`
- Source URL: https://code.claude.com/docs/en/mcp.md
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... cal and SSH sessions | The desktop app delivers them in-process | `blocked` entries in your
organization's [connector tool controls](#organization-controls-on-connector-tools) |
[`disableClaudeAiConnectors`](#disable-claude-ai-connectors), `ENABLE_CLAUDEAI_MCP_SERVERS`, and
[`allowAllClaudeAiMcps`](/docs/en/settings-reference#allowallclaudeaimcps) act only on the first
row, the conn ...

> ... ization's [connector tool controls](#organization-controls-on-connector-tools) |
[`disableClaudeAiConnectors`](#disable-claude-ai-connectors), `ENABLE_CLAUDEAI_MCP_SERVERS`, and
[`allowAllClaudeAiMcps`](/docs/en/settings-reference#allowallclaudeaimcps) act only on the first
row, the connectors Claude Code fetches itself. The other two rows differ from it in these ways: *
**Clou ...

> ... tings-reference#allowallclaudeaimcps) act only on the first row, the connectors Claude Code
fetches itself. The other two rows differ from it in these ways: * **Cloud sessions**:
`allowedMcpServers` and `deniedMcpServers` entries that reach the session, for example through
[server-managed settings](/docs/en/server-managed-settings), filter the delivered connectors too.
The s ...

> ... Claude Code v2.1.246 or later; before v2.1.246, a strict session still waited on approval for
them, which left background sessions waiting at startup. See [Exclusive control with managed-
mcp.json](/docs/en/managed-mcp#exclusive-control-with-managed-mcp-json) for what the flag does under
a managed MCP file. [Project server approvals and workspace trust](#project-server-appr ...

> ... s) that pushes messages into your session, so Claude reacts to Telegram messages, Discord chats,
or webhook events while you're away. ## Find and build MCP servers Browse reviewed connectors in the
[Anthropic Directory](https://claude.ai/directory). Directory connectors use the same MCP
infrastructure as Claude Code, so you can add any remote server listed there with ...

Potential config terms not found in local tool files:

`CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`, `ENABLE_TOOL_SEARCH`, `MCP_PROTOCOL_NEGOTIATION`, `MCP_SDK_GENERATION`, `WaitForMcpServers`, `allowed-tools`, `disabledMcpServers`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed: `CLAUDE_CODE_MCP_SERVER_NAME` / `CLAUDE_CODE_MCP_SERVER_URL` are per-server identity env vars, not allowlists. Background-task env vars and `WaitForMcpServers` are operational. `disabledMcpServers` is not the vendor key (`deniedMcpServers` / `disabledMcpjsonServers` already exist).

### Claude Code: Desktop documentation

- Change type: `new-source-baseline`
- Source URL: https://code.claude.com/docs/en/desktop
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... Claude from using tools to read or act on external pages in the Browser pane . Users can still
navigate to external sites themselves, and local dev server previews are unaffected.
disableMobileSimulatorTools set to true to block Claude's tools for controlling and capturing
devices in the iOS Simulator pane . The pane stays usable for the user's own taps; only Claude's
access is remove ...

> ... eTools managed setting . With tools disabled, users can still navigate to external sites;
Claude's tools can't read or act on them. To turn off external browsing entirely, set the
disableBrowserExternalNavigation managed setting to true . This blocks all external navigation in
the Browser, including sites on your organization's allowlist; localhost dev servers and file
previews keep workin ...

> ... organization already configured those lists for the extension, the Browser respects them
automatically. Administrators can also turn off Claude's tools on external pages with the
browserExternalPageTools managed setting . With tools disabled, users can still navigate to external
sites; Claude's tools can't read or act on them. To turn off external browsing entirely, set the
disabl ...

> ... naged devices Cloud sessions SSH sessions Pre-configure SSH connections for your team Restrict
which SSH hosts users can connect to Enterprise configuration Admin console controls Managed
settings Device management policies Network access requirements Authentication and SSO Data handling
Deployment Coming from the CLI? CLI flag equivalents Shared configuration MCP servers f ...

> ... ry Best practices Platforms and integrations Overview Remote Control Claude Code on the web
Claude Code on desktop Get started Reference Linux (beta) Windows (WSL) Scheduled tasks iOS
simulator (beta) Mobile Chrome extension Computer use (preview) Visual Studio Code JetBrains IDEs
Code review & CI/CD Claude Code in Slack Claude Tag On this page Start a session Work with ...

Potential config terms not found in local tool files:

`CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

Config update applied from this source: added this Desktop docs watcher and pinned `disableMobileSimulatorTools: true` on Moderate and Strict (Baseline unset). People keep manual use of the iOS Simulator pane. The terminal CLI ignores this key. JSON boolean `true` only.

No config update needed for `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`: session thinking UX toggle, not a simulator lock. Deferred unique follow-ups from this page: Desktop Browser pane keys (open PR #108) and `sshHostAllowlist` (org-specific SSH host patterns; empty array disables SSH).

### Cursor: Team administration documentation

- Change type: `content-changed`
- Source URL: https://docs.cursor.com/en/account/teams/admin-dashboard
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

Keyword snippets:

> ... ing Changelog Agent Overview Agents Window Agent Review Planning Prompting Debugging Design Mode
Tools Security Grok Bot Overview Get Started Use Cases Work with Grok Bot Settings Teams and
Enterprise Customize Overview Plugins Rules Skills Subagents Hooks MCP Cloud Agents Overview Setup
Builds Capabilities Best Practices Choose Where Cloud Agents Run Automation ...

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
Grok Bot Overview Get Started Use Cases Work with Grok Bot Settings Teams and Enterprise Customize
Overview Plugins Rules Skills Subagents Hooks MCP Cloud Agents Overview ...

> ... ugins Rules Skills Subagents Hooks MCP Cloud Agents Overview Setup Builds Capabilities Best
Practices Choose Where Cloud Agents Run Automations Bugbot Security Agents PR Routing & Approval
Mobile Security Self-Hosted Machines Settings API Origin Overview CLI Create a repository Clone,
Push & Pull Mirror GitHub Pull requests Browse & Search Settings Codebase settings ...

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

> ... kills Cloud and local sandboxes Copilot usage metrics All articles Copilot usage metrics
Prompting Prompt engineering Response customization Context MCP Spaces Repository indexing Content
exclusion Tools AI tools About Copilot integrations Models Bring your own key Utility models Auto
model selection Base and LTS models Usage limits Billing Billing for individuals Organizati ...

> ... xpand sidebar Scroll breadcrumbs left Home GitHub Copilot How-tos Administer Copilot Manage for
organization Scroll breadcrumbs right GitHub Copilot Get started Quickstart Copilot CLI quickstart
Copilot app quickstart What is GitHub Copilot? Plans Features Best practices Enterprise AI
governance Concepts Completions Code suggestions Code referencing Chat Agents ...

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

> ... g directory, and thread forks work with symlinked session roots.
([#42039](https://github.com/openai/codex/pull/42039),
[#42135](https://github.com/openai/codex/pull/42135))\n\n## Configuration and API Updates\n\n- App-
server thread metadata includes nullable `model` and `reasoningEffort` fields. Structured
asynchronous questions are supported through `request_user_input ...

> ... type": "application/octet-stream",         "digest":
"sha256:65724412517a59f7cd3d6018c08053e9f6eef62a42913e192010554c05bb9db9",         "label": "",
"name": "codex-windows-sandbox-setup",         "size": 1421,         "state": "uploaded"       },
{         "content_type": "application/x-msdos-program",         "digest":
"sha256:18bedfdf2f125a731586cdd ...

> ... tps://github.com/openai/codex/pull/41929) Open the agents overview directly in the reconnect
test\n- [#41933](https://github.com/openai/codex/pull/41933) Report configured sandbox policy
consistently\n- [#41934](https://github.com/openai/codex/pull/41934) Omit undersized WAV output from
Code Mode\n- [#41936](https://github.com/openai/codex/pull/41936) Attach faile ...

Potential config terms not found in local tool files:

`disable_paste_burst`, `features.context_management.experimental_mode`, `tui.disable_paste_burst`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed: Codex `tui.auto_recap`, `tui.disable_paste_burst`, and `features.context_management.experimental_mode` are TUI or experimental prefs, not admin locks. Codex 0.152.0 `tools.update_plan.enabled` defaulted off; 0.153.4 is stable.

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
Security policy Activity Custom properties Stars 35.8k stars Watchers 171 watching Forks 5.4k forks
Report repository Releases Used by Contributors Languages Footer  2026 GitHub, ...

> ... ut the Continue Docs . Final 2.0.0 Release We polished Continue and did a final 2.0.0 release of
the VS Code extension, CLI, and JetBrains plugin. This included removing anonymous telemetry,
pulling out authentication, squashing bugs, and more. VS Code CLI JetBrains Note: We recommend using
the Continue CLI instead of the JetBrains plugin. Contributors Thank you to t ...

### Tabnine: Tabnine admin documentation

- Change type: `content-changed`
- Source URL: https://docs.tabnine.com/
- Status: `200`
- Related repo paths: tabnine/

Keyword snippets:

> ... rt & Feedback Getting started Install Quickstart Guide Context Engine Tabnine Agent Tabnine Chat
Tabnine CLI Code Completions Tabnine's Prompting Guide Tabnine Plugin for OpenCode Administering
Tabnine Private Installation Release Notes Powered by GitBook On this page For the complete
documentation index, see llms.txt . This page is also available as Markdown . C ...

> Overview | Tabnine Docs  Ctrl k Tabnine website Contact Sales More Welcome Overview Architecture
Security Privacy Protection Personalization AI Models Integrations System & Hardware Requirements
Supported Languages Supported IDEs Tabnine Subscription Plans Support & Feedback Getting started I
...

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

> ... d Products Agent Platform Apigee API Management BigQuery Compute Engine Cloud CDN Cloud Run
Cloud Storage Cloud SQL Gemini Enterprise Google Kubernetes Engine Looker Cross-product Tools Access
and resources management Costs and usage management Infrastructure as code SDK, languages,
frameworks, and tools Technology Areas AI and ML Application development Applicat ...

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
main content Documentation close Get Started Get Started with Google Cloud Product List Cloud
Customer Care ...

### Google Gemini: Google Cloud organization policies

- Change type: `content-changed`
- Source URL: https://cloud.google.com/resource-manager/docs/organization-policy/overview
- Status: `200`
- Related repo paths: google-gemini/

Keyword snippets:

> Organization Policy overview | Google Cloud Documentation Skip to main content Documentation close
Get Started Get Started with Google Cloud Product List Cloud Customer Care Featured Products Agent P
...

> ... re Overview Guides Reference Resources Console Discover Product overview Hierarchy evaluation
Get started Enforce an organization policy Create resource restrictions Create custom constraints
Create organization policies Test custom constraints with Gemini Cloud Assist Test organization
policies Apply organization policies Scope organization policies with tags Manage b ...

> ... licies Scope organization policies with tags Manage baseline constraints Configure service
restrictions Restrict IAM service account usage Restrict service usage Restrict resource locations
Disable Cloud Logging for the Cloud Healthcare API Restrict identities Domain-restricted sharing
Restrict identities with domain-restricted sharing Monitor Audit logging for Organ ...

> ... rict resource locations Disable Cloud Logging for the Cloud Healthcare API Restrict identities
Domain-restricted sharing Restrict identities with domain-restricted sharing Monitor Audit logging
for Organization Policy Troubleshoot Troubleshoot organization policies Get Started Get Started with
Google Cloud Product List Cloud Customer Care Featured Products Agent ...

### Claude Desktop: Claude Desktop MCP documentation

- Change type: `content-changed`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/mcp
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... authentication Where the helper runs Which variables a helper can read Trust a folder before its
headersHelper runs Add MCP servers from JSON configuration Import MCP servers from Claude Desktop
Use MCP servers from claude.ai How connectors reach Claude Code Organization controls on connector
tools Disable claude.ai connectors Use Claude Code as an MCP server MCP output l ...

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

> ... fetches them from claude.ai The settings in this section and managed MCP configuration Cloud
sessions The remote host passes them in Your claude.ai organization settings, plus the allowlist and
denylist settings that reach the session and any managed-mcp.json on the host that runs it The
desktop app 's local and SSH sessions The desktop app delivers them in-process b ...

Potential config terms not found in local tool files:

`CLAUDE_AUTO_BACKGROUND_TASKS`, `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`, `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed for Claude Desktop: these `CLAUDE_CODE_*` names are Claude Code session env vars scraped from the shared MCP docs URL. Desktop iOS Simulator lock in Claude Code is `disableMobileSimulatorTools` (this PR). Desktop MDM connector policy is a separate control (open PR #70).

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
Plan overviews What is the Enterprise plan? What is the Team plan? Claude Team plan for scientists
Get started Get started with the Team plan Move your personal Claude accou ...

> ... illing Add or update your Team plan's tax or VAT ID Cancel your organization's Team plan
subscription How am I billed for my Enterprise plan? Understanding your Team plan invoices Admin
management Roles and permissions Purchase and manage seats on Team plans Purchase and manage seats
on Enterprise plans Manage members on Team and Enterprise plans Claude Enterpris ...

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

No config update needed: these OpenAPI schema names are API request/response fields or audit event types, not OpenAI Platform org-policy admin locks already covered in `openai-platform/examples/`.

### Claude API: Anthropic admin API documentation

- Change type: `content-changed`
- Source URL: https://platform.claude.com/docs/en/api/admin.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... d-7a8b-49c0-9d1e-2f3a4b5c6d7e", "type": "organization" }, "type": "rbac_role_permission" } ],
"has_more": true, "next_page": "eyJjdXJzb3IiOiAicmJhY19yb2xlXzAxIn0" } ``` ## Admin  Workspaces ###
Create Workspace **POST** `/v1/organizations/workspaces` Create Workspace #### Headers -
`"anthropic-beta": optional array of string` Optional header to specify the beta vers ...

> ... t-tier parameter. When no seat is free the request fails with a 400 error rather than purchasing
a seat. #### Body parameters - `email: string` Email of the User. format: email - `role: "billing"
or "claude_code_user" or "developer" or 2 more` Role for the invited User. The accepted values
depend on the organization type. Console and API organizations accept `us ...

> # Admin ## Admin  Organizations ### Get Current Organization **GET** `/v1/organizations/me` Retrieve
information about the organization associated with the authenticated API key. #### Returns -
`Organization object` - `id: string` ID of the Organization. format: uuid - `name: string` Name of
the Organization. - `type: "organization"` Object type. For Orga ...

> ... nse (200) ```json { "type": "workspace_member_deleted", "user_id":
"user_01WCz1FkmYMm4gnmykNKUu3Q", "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ" } ``` ## Admin
Workspaces  Rate Limits ### List Workspace Rate Limits **GET**
`/v1/organizations/workspaces/{workspace_id}/rate_limits` List rate-limit overrides configured for a
workspace. Returns only the groups and ...

> # Admin ## Admin  Organizations ### Get Current Organization **GET** `/v1/organizations/me` Retrieve
information about the organization associated with the authenticated API key. #### Re ...

Potential config terms not found in local tool files:

`allowed_inference_geos`, `always_allow`, `fast-mode-2026-02-01`, `mcp-tunnels-2026-05-19`, `model_group`, `slack_channel_id`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed: `mcp-tunnels-2026-05-19` is covered by open PR #70. `fast-mode-2026-02-01` is an API beta header, not a Claude Code Fast mode lock. `allowed_inference_geos`, `always_allow`, `model_group`, and `slack_channel_id` are Admin API fields, not new tier defaults.

### Claude API: Anthropic API release notes

- Change type: `content-changed`
- Source URL: https://platform.claude.com/docs/en/release-notes/api.md
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... Python, TypeScript, C#, Go, Java, PHP, and Ruby SDKs under `client.beta.organization`. They
cover organization info, members, invites, workspaces and workspace members, API keys, rate limits,
service accounts, workload identity federation issuers and rules, and customer-managed encryption
keys. Usage and cost reports and the Claude Enterprise user-management and anal ...

> ... emoved from an organization. This lets organization admins more easily track usage for each
account, and ensure key usage is legitimate. These API keys can be scoped to a specific workspace or
[work on admin endpoints and across any workspace](https://platform.claude.com/docs/en/manage-
claude/authentication#select-a-workspace) the account has access to. Workspace API ...

> ... 5-04-14) and [Migrate from `skills-2025-10-02`](https://platform.claude.com/docs/en/build-with-
claude/skills-guide#migrate-from-skills-2025-10-02). - You can now create **personal keys** and
**service account keys** in the Claude Console. They act as you or as a [service
account](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation#ser ...

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

`LanguageModel`, `LanguageModelSession`, `allowed_domains`, `blocked_domains`, `fast-mode-2026-02-01`, `mcp_oauth`, `model_context_window_exceeded`, `permission_policy`, `policy_violation_investigation`, `thinking.block_binding.prefix_mismatch_behavior`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

No config update needed: these release-note names are API types, beta headers, or event fields. `thinking.block_binding.prefix_mismatch_behavior` is an API thinking-block field, not a managed settings key. Inference hooks remain console settings (open PR #84). Dreams stays off until an org-level disable ships.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

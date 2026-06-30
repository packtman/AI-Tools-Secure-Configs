# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/settings |
| Claude Code | Hooks documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Claude Code | Dynamic workflows documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/workflows |
| GitHub Copilot | MCP server access policy documentation | new-source-baseline | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-server-access.md |
| GitHub Copilot | MCP allowlist enforcement documentation | new-source-baseline | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/reference/mcp-allowlist-enforcement.md |
| GitHub Copilot | Content exclusion documentation | content-changed | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/configure-content-exclusion/exclude-content-from-copilot.md |
| GitHub Copilot | Content exclusion audit documentation | new-source-baseline | 200 | https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/configure-content-exclusion/review-changes.md |
| Codex CLI | OpenAI Codex config reference | new-source-baseline | 200 | https://raw.githubusercontent.com/openai/codex/main/docs/config.md |
| Codex CLI | OpenAI Codex releases | content-changed | 200 | https://api.github.com/repos/openai/codex/releases?per_page=10 |
| Codex Desktop | OpenAI Codex repository | content-changed | 200 | https://github.com/openai/codex |
| Codex Desktop | OpenAI Codex config reference | content-changed | 200 | https://raw.githubusercontent.com/openai/codex/main/docs/config.md |
| Continue.dev | Configuration reference | content-changed | 200 | https://docs.continue.dev/reference |
| Continue.dev | Continue repository | content-changed | 200 | https://github.com/continuedev/continue |
| Windsurf | Windsurf documentation | content-changed | 200 | https://docs.windsurf.com/ |
| Windsurf | Windsurf changelog | content-changed | 200 | https://windsurf.com/changelog |
| Tabnine | Tabnine admin documentation | content-changed | 200 | https://docs.tabnine.com/ |
| Gemini CLI | Gemini CLI repository | content-changed | 200 | https://github.com/google-gemini/gemini-cli |
| Gemini CLI | Gemini CLI documentation | content-changed | 200 | https://cloud.google.com/gemini/docs/codeassist/gemini-cli |
| Google Gemini | Vertex AI Gemini safety settings | content-changed | 200 | https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters |
| Google Gemini | Google Cloud organization policies | content-changed | 200 | https://cloud.google.com/resource-manager/docs/organization-policy/overview |
| Claude Desktop | Claude Desktop MCP documentation | content-changed | 200 | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Claude Desktop | Claude Desktop support documentation | content-changed | 200 | https://support.anthropic.com/en/ |
| OpenAI Platform | OpenAI OpenAPI repository | content-changed | 200 | https://github.com/openai/openai-openapi |
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

> ... ce On this page When to use a workflow Run a bundled workflow Bundled workflows Watch the run
Have Claude write a workflow Ask for a workflow in your prompt Let Claude decide with ultracode
Approve the plan before it runs Save the workflow for reuse Pass input to a saved workflow How a
workflow runs Behavior and limits Manage runs Resume after a pause Cost Turn workf ...

> ... sions. Set CLAUDE_CODE_DISABLE_WORKFLOWS=1 . Read at startup, so it applies wherever you set it.
To turn workflows off for your whole organization, set "disableWorkflows": true in managed settings
, or use the toggle on the Claude Code admin settings page. When workflows are disabled, the bundled
workflow commands are unavailable, the ultracode keyword no longer triggers a ...

Potential config terms found upstream are already present in local tool files.

### GitHub Copilot: MCP server access policy documentation

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-server-access.md
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> --- title: Configure MCP server access for your organization or enterprise intro: You can configure
an MCP registry URL and access control policy to determine which MCP servers developers can discover
and use in supported IDEs and {% data variables.copilot.copilot_cli_short %}. permissions:
Enterprise owners and organizatio ...

> --- title: Configure MCP server access for your organization or enterprise intro: You can configure
an MCP registry URL and access control policy to determine which MCP servers developers can discover
and use in supported IDEs and {% data v ...

> --- title: Configure MCP server access for your organization or enterprise intro: You can configure
an MCP registry URL and access control policy to determine which MCP servers developers can discover
and use in supported IDEs and {% data variables.copilot.copilot_cli_short %}. permissions: Enterpr
...

> ... nabled everywhere**. 1. In the **MCP Registry URL** section, enter the URL of your registry,
then click **Save**. {% data reusables.copilot.mcp.azure-api-center-url %} 1. In the **Restrict MCP
access to registry servers** section, select the dropdown menu, then click one of the following
options: * **Allow all**: No restrictions. All MCP servers can be used. * **Registry only* ...

> ... ict MCP access to registry servers** section, select the dropdown menu, then click one of the
following options: * **Allow all**: No restrictions. All MCP servers can be used. * **Registry
only**: Only servers from the registry may run. Your chosen policy will immediately apply to
developers in your enterprise. ## Configuring the MCP allowlist policy for an organization ...

### GitHub Copilot: MCP allowlist enforcement documentation

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/github/docs/main/content/copilot/reference/mcp-allowlist-enforcement.md
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> --- title: MCP allowlist enforcement intro: 'Understand the logic and limitations of MCP allowlist
enforcement.' versions: feature: copilot contentType: reference category: - Learn about Copilot ---
## Cu ...

> ... t.prodname_copilot_short %}** until strict enforcement is available. ## Enforcement for local
servers MCP allowlist enforcement applies to both remote and local MCP servers. When "Registry only"
is configured, local servers must be included in your registry with the correct server ID, which
must exactly match the installed server ID. A server's canonical ID is often defi ...

> ... reference category: - Learn about Copilot --- ## Current enforcement limitations MCP allowlist
enforcement currently has the following limitations: * Enforcement is based only on server name/ID
matching, which can be bypassed by editing configuration files * Strict enforcement that prevents
installation of non-registry servers is not yet available For the highest leve ...

> ... e bypassed by editing configuration files * Strict enforcement that prevents installation of
non-registry servers is not yet available For the highest level of security, you can **disable MCP
servers in {% data variables.product.prodname_copilot_short %}** until strict enforcement is
available. ## Enforcement for local servers MCP allowlist enforcement applies to both remote a ...

> ... cluded in your registry with the correct server ID, which must exactly match the installed
server ID. A server's canonical ID is often defined in its documentation or manifest. ## Policy
resolution for users with multiple seats MCP allowlist enforcement is always tied to the
organization or enterprise that assigns the {% data variables.product.prodname_copilot %} seat. If a
...

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

### GitHub Copilot: Content exclusion audit documentation

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/github/docs/main/content/copilot/how-tos/configure-content-exclusion/review-changes.md
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> --- title: Reviewing changes to content exclusions for GitHub Copilot shortTitle: Review changes
intro: You can monitor changes to content exclusions in your repositories and organizations.
permissions: Organization owners produc ...

> ... eenshot of the last edited information. The time of change link is highlighted with a dark
orange outline.](/assets/images/help/copilot/content-exclusions-last-edited-by.png) The "Audit log"
page for the organization is displayed, showing the most recently logged occurrences of the
`copilot.content_exclusion_changed` action in the repository. {% data reusables.copilo ...

> ... e.](/assets/images/help/copilot/content-exclusions-last-edited-by.png) The "Audit log" page for
the organization is displayed, showing the most recently logged occurrences of the
`copilot.content_exclusion_changed` action in the repository. {% data reusables.copilot.more-
details-content-exclusion-logs %} ## Reviewing changes in your organization {% data
reusables.profile.access_org %} {% da ...

> --- title: Reviewing changes to content exclusions for GitHub Copilot shortTitle: Review changes
intro: You can monitor changes to content exclusions in your repositories and organizations.
permissions: Organization owners product: '{% data reusables.gated-features.copilot-business-and-
enterprise %}' versions: feature: copilot redirect_from: - /copilot/managing-cop ...

> ... can monitor changes to content exclusions in your repositories and organizations. permissions:
Organization owners product: '{% data reusables.gated-features.copilot-business-and-enterprise %}'
versions: feature: copilot redirect_from: - /copilot/managing-copilot/managing-github-copilot-in-
your-organization/reviewing-activity-related-to-github-copilot-in-your-organiz ...

### Codex CLI: OpenAI Codex config reference

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/openai/codex/main/docs/config.md
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> # Configuration For basic configuration instructions, see [this
documentation](https://developers.openai.com/codex/config-basic). For advanced configuration
instructions, see [this documen ...

### Codex CLI: OpenAI Codex releases

- Change type: `content-changed`
- Source URL: https://api.github.com/repos/openai/codex/releases?per_page=10
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... type": "application/octet-stream",         "digest":
"sha256:a4e9414dfeb97d3f145bd7fd4a85db0a981a10282edb2a533e8b7d6e4cbcfa36",         "label": "",
"name": "codex-windows-sandbox-setup",         "size": 1389,         "state": "uploaded"       },
{         "content_type": "application/x-msdos-program",         "digest":
"sha256:cbf5538d880ebd255ede54a ...

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
- Source URL: https://raw.githubusercontent.com/openai/codex/main/docs/config.md
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> # Configuration For basic configuration instructions, see [this
documentation](https://developers.openai.com/codex/config-basic). For advanced configuration
instructions, see [this documen ...

### Continue.dev: Configuration reference

- Change type: `content-changed`
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

- Change type: `content-changed`
- Source URL: https://github.com/continuedev/continue
- Status: `200`
- Related repo paths: continue-dev/

Keyword snippets:

> ... ESTING.md TESTING.md docs-search-dark-mode-fix.png docs-search-dark-mode-fix.png package-
lock.json package-lock.json package.json package.json tsconfig.json tsconfig.json worktree-
config.yaml worktree-config.yaml View all files Repository files navigation README Code of conduct
Contributing Apache-2.0 license Security More items Continue Pioneering open-source coding a ...

> ... g agent continue.dev Topics agent cli open-source ai developer-tools Resources Readme License
Apache-2.0 license Code of conduct Code of conduct Contributing Contributing Security policy
Security policy Uh oh! There was an error while loading. Please reload this page . Activity Custom
properties Stars 34.6k stars Watchers 165 watching Forks 4.9k forks Report repos ...

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
Cases API Devin Desktop Editor Getting Started Set Up Devin Desktop FAQ Recommended Extensions
Models Adaptive Quick Review Tab Command Code Lenses Terminal Browser Previews A ...

> ... in Desktop FAQ Recommended Extensions Models Adaptive Quick Review Tab Command Code Lenses
Terminal Browser Previews AI Commit Messages DeepWiki Codemaps Vibe and Replace Advanced Cascade
Context Awareness Troubleshooting Agent Command Center Agent Command Center Spaces Devin Devin Local
Agent Agent Client Protocol (preview) Building a custom ACP agent Releases Cha ...

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

> ... ascade Download 1.13.12  v1.13.9 January 16, 2026  Bug Fixes and Improvements Improvements to
GPT-5.2-Codex harness Admins can now manage Windsurf restrictions via Windows Group Policy Download
1.13.9  v1.13.8 January 14, 2026  GPT-5.2-Codex Adds support for GPT-5.2-Codex with four reasoning
efforts (low, medium, high, and xhigh). GPT-5.2-Codex is OpenAI's lat ...

> ... ins Changelog Get Started Features Cascade (JetBrains) Context Awareness Best Practices
Troubleshooting Accounts Usage Quota Analytics Teams & Enterprise Security FedRAMP Security Admin
Guide Reporting On this page v3.3.18 v3.2.28 v3.2.23 v3.2.19 v3.2.16 v3.1.7 v3.0.28 v3.0.21 v3.0.12
v2.3.15 v2.3.9 v2.2.17 v2.1.32 v2.1.29 v2.0.67 v2.0.63 v2.0.61 v2.0.50 v2.0.44 ...

> ... eases (Next) Windsurf Plugins Changelog Get Started Features Cascade (JetBrains) Context
Awareness Best Practices Troubleshooting Accounts Usage Quota Analytics Teams & Enterprise Security
FedRAMP Security Admin Guide Reporting On this page v3.3.18 v3.2.28 v3.2.23 v3.2.19 v3.2.16 v3.1.7
v3.0.28 v3.0.21 v3.0.12 v2.3.15 v2.3.9 v2.2.17 v2.1.32 v2.1.29 v2.0.67 v2.0.63 v ...

> ... ows system-wide installs. CLI and Devin Local On Windows, bash now resolves to Git Bash instead
of the WSL launcher stub. Subagents can now be configured with a default model. The MCP registry
cache is now warmed during startup, so MCP servers are ready sooner. Injected context is no longer
included in auto-generated session titles. Fixed agent messages over-me ...

> ... le scroll-to-next-hunk settings (default off) Preserved colors and styling in Cascade terminal
output Multiple fixes to the Model Context Protocol implementation Supports lowering permissions for
Cascade's Web Fetch tool Fix race condition in the dedicated terminal implementation Support force
killing commands in the dedicated terminal Improved markdown completion Fix ...

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
Agent Platform Workbench | View on GitHub Google's generative AI models, like G ...

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
Use MCP servers from claude.ai Disable claude.ai connectors Use Claude Code as an MCP server MCP
output limits and warnings Raise the limit for a specific tool Respond to MCP elic ...

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

`CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Claude Desktop: Claude Desktop support documentation

- Change type: `content-changed`
- Source URL: https://support.anthropic.com/en/
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... e 76 articles Pro and Max plans 15 articles Team and Enterprise plans 60 articles Identity
management (SSO, JIT, SCIM) 15 articles Claude Cowork 9 articles Claude Code 19 articles Claude
Desktop 9 articles Claude Mobile apps 20 articles Claude API and Console 40 articles Connectors 21
articles Claude in Chrome 5 articles Claude for Education 4 articles Claude for Nonprofi ...

> ... Italiano   Portugus P  Espaol  English Search for answers or browse by topic Search for
articles... Claude 76 articles Pro and Max plans 15 articles Team and Enterprise plans 60 articles
Identity management (SSO, JIT, SCIM) 15 articles Claude Cowork 9 articles Claude Code 19 articles
Claude Desktop 9 articles Claude Mobile apps 20 articles Claude ...

### OpenAI Platform: OpenAI OpenAPI repository

- Change type: `content-changed`
- Source URL: https://github.com/openai/openai-openapi
- Status: `200`
- Related repo paths: openai-platform/

No configured watch keywords were found in the fetched content.

### Claude API: Anthropic admin API documentation

- Change type: `content-changed`
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

`fast-mode-2026-02-01`, `model_group`

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

> ... 've released the [Rate Limits API](/docs/en/manage-claude/rate-limits-api), allowing
administrators to programmatically query the rate limits configured for their organization and
workspaces. ### April 23, 2026 * Memory for Claude Managed Agents is now in public beta under the
standard `managed-agents-2026-04-01` header. See [Using agent memory](/docs/en/managed-agen ...

> ... -lived OIDC tokens from your own identity provider (AWS IAM, Google Cloud, GitHub Actions,
Kubernetes, Microsoft Entra ID, Okta, SPIFFE, and more) instead of long-lived static API keys.
Configure issuers and federation rules in the Claude Console, and the SDK handles token exchange and
refresh automatically. See [Authentication](/docs/en/manage-claude/authentic ...

> ... ks-libraries/cli/quickstart). ### April 7, 2026 * We announced [Claude Mythos
Preview](https://anthropic.com/glasswing) is available as a gated research preview for defensive
cybersecurity work as part of [Project Glasswing](https://anthropic.com/glasswing). Access is
invitation-only. * The [Messages API](/docs/en/api/messages) is now available on Amazon Bedrock as
...

Potential config terms not found in local tool files:

`LanguageModel`, `LanguageModelSession`, `fast-mode-2026-02-01`, `mcp_oauth`, `model_context_window_exceeded`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

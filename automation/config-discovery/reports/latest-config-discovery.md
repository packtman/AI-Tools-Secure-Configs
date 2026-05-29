# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Claude Code | Managed settings documentation | new-source-baseline | 200 | https://docs.anthropic.com/en/docs/claude-code/settings |
| Claude Code | Hooks documentation | new-source-baseline | 200 | https://docs.anthropic.com/en/docs/claude-code/hooks |
| Cursor | Team administration documentation | new-source-baseline | 200 | https://docs.cursor.com/en/account/teams/admin-dashboard |
| Cursor | MCP documentation | new-source-baseline | 200 | https://docs.cursor.com/en/tools/mcp |
| GitHub Copilot | Organization policy documentation | new-source-baseline | 200 | https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization |
| GitHub Copilot | Content exclusion documentation | new-source-baseline | 200 | https://docs.github.com/en/copilot/managing-copilot/configuring-and-auditing-content-exclusion |
| Codex CLI | OpenAI Codex repository | new-source-baseline | 200 | https://github.com/openai/codex |
| Codex CLI | OpenAI Codex releases | new-source-baseline | 200 | https://github.com/openai/codex/releases |
| Codex Desktop | OpenAI Codex repository | new-source-baseline | 200 | https://github.com/openai/codex |
| Codex Desktop | OpenAI Codex config reference | new-source-baseline | 200 | https://raw.githubusercontent.com/openai/codex/main/codex-rs/config.md |
| Continue.dev | Configuration reference | new-source-baseline | 200 | https://docs.continue.dev/reference |
| Continue.dev | Continue repository | new-source-baseline | 200 | https://github.com/continuedev/continue |
| Windsurf | Windsurf documentation | new-source-baseline | 200 | https://docs.windsurf.com/ |
| Windsurf | Windsurf changelog | new-source-baseline | 200 | https://windsurf.com/changelog |
| Tabnine | Tabnine admin documentation | new-source-baseline | 200 | https://docs.tabnine.com/ |
| Tabnine | Tabnine enterprise documentation | new-source-baseline | 200 | https://www.tabnine.com/enterprise |
| Amazon Q Developer | Amazon Q Developer administration guide | new-source-baseline | 200 | https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-admin.html |
| Amazon Q Developer | Amazon Q Developer IAM reference | new-source-baseline | 200 | https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonqdeveloper.html |
| Gemini CLI | Gemini CLI repository | new-source-baseline | 200 | https://github.com/google-gemini/gemini-cli |
| Gemini CLI | Gemini CLI documentation | new-source-baseline | 200 | https://cloud.google.com/gemini/docs/codeassist/gemini-cli |
| Google Gemini | Vertex AI Gemini safety settings | new-source-baseline | 200 | https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters |
| Google Gemini | Google Cloud organization policies | new-source-baseline | 200 | https://cloud.google.com/resource-manager/docs/organization-policy/overview |
| Claude Desktop | Claude Desktop MCP documentation | new-source-baseline | 200 | https://docs.anthropic.com/en/docs/claude-code/mcp |
| Claude Desktop | Claude Desktop support documentation | new-source-baseline | 200 | https://support.anthropic.com/en/ |
| OpenAI Platform | OpenAI OpenAPI repository | new-source-baseline | 200 | https://github.com/openai/openai-openapi |
| OpenAI Platform | OpenAI OpenAPI schema | new-source-baseline | 200 | https://raw.githubusercontent.com/openai/openai-openapi/master/openapi.yaml |
| Claude API | Anthropic admin API documentation | new-source-baseline | 200 | https://docs.anthropic.com/en/api/admin-api |
| Claude API | Anthropic API release notes | new-source-baseline | 200 | https://docs.anthropic.com/en/release-notes/api |

## Review Details

### Claude Code: Managed settings documentation

- Change type: `new-source-baseline`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/settings
- Status: `200`
- Related repo paths: claude-code/, rollout-guide/configs/claude-code/

Keyword snippets:

> ... ttings Worktree settings Permission settings Permission rule syntax Sandbox settings Sandbox
path prefixes Attribution settings File suggestion settings Hook configuration Compute managed
settings with a policy helper Settings precedence Verify active settings Key points about the
configuration system System prompt Excluding sensitive files Subagent configuration Plugin con ...

> ... in content Claude Code Docs home page English Search... ⌘ K Ask Assistant Claude Developer
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
Output styles Interface Terminal configuration Fullscreen rendering Voice dicta ...

> ... , editor settings) Tools and plugins you use across all projects API keys and authentication
(stored securely) Project scope is best for: Team-shared settings (permissions, hooks, MCP servers)
Plugins the whole team should have Standardizing tooling across collaborators Local scope is best
for: Personal overrides for a specific project Testing configurations be ...

### Claude Code: Hooks documentation

- Change type: `new-source-baseline`
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

> ... n" : "session_start" } ​ InstructionsLoaded decision control InstructionsLoaded hooks have no
decision control. They cannot block or modify instruction loading. Use this event for audit logging,
compliance tracking, or observability. ​ UserPromptSubmit Runs when the user submits a prompt,
before Claude processes it. This allows you to add additional context based ...

> ... ed startup , resume , clear , compact Setup which CLI flag triggered setup init , maintenance
SessionEnd why the session ended clear , resume , logout , prompt_input_exit ,
bypass_permissions_disabled , other Notification notification type permission_prompt , idle_prompt ,
auth_success , elicitation_dialog , elicitation_complete , elicitation_response SubagentStart age
...

### Cursor: Team administration documentation

- Change type: `new-source-baseline`
- Source URL: https://docs.cursor.com/en/account/teams/admin-dashboard
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

No configured watch keywords were found in the fetched content.

### Cursor: MCP documentation

- Change type: `new-source-baseline`
- Source URL: https://docs.cursor.com/en/tools/mcp
- Status: `200`
- Related repo paths: cursor/, rollout-guide/configs/cursor/

Keyword snippets:

> Cursor Docs — Agent, Rules, MCP, Skills & CLI

### GitHub Copilot: Organization policy documentation

- Change type: `new-source-baseline`
- Source URL: https://docs.github.com/en/copilot/managing-copilot/managing-github-copilot-in-your-organization
- Status: `200`
- Related repo paths: github-copilot/, rollout-guide/configs/github-copilot/

Keyword snippets:

> ... LI command reference CLI plugin reference CLI programmatic reference ACP server CLI
configuration directory Custom agents configuration Custom instructions support Hooks reference
Policy conflicts Copilot allowlist reference MCP allowlist enforcement Metrics data Copilot billing
Models and pricing Model multipliers for annual plans Billing cycle Seat assignment Li ...

> Managing GitHub Copilot in your organization - GitHub Docs Skip to main content GitHub Docs Version:
Free, Pro, & Team Search or ask Copilot Search or ask Copilot Select language: current language is
English Search or ask Co ...

> ... stom agents Spaces Create Copilot Spaces Collaborate with others Copilot for GitHub tasks Use
Copilot to create or update issues Create a PR summary Use the GitHub MCP Server from Copilot Chat
Use Copilot agents Get started Kick off a task Research, plan, iterate Manage agent sessions Copilot
code review Review Copilot output Set up Set up for self Install Copilot exten ...

> ... lls Enterprise management Spark Copilot usage metrics All articles Copilot usage metrics
Prompting Prompt engineering Response customization Context MCP Spaces Repository indexing Content
exclusion Tools AI tools About Copilot integrations Models Utility models Auto model selection
FedRAMP models Base and LTS models Usage limits Billing Usage-based billing for individuals Us ...

> ... ions Code suggestions Code referencing Chat Agents Cloud agent About cloud agent Agent
management Custom agents Access management MCP and cloud agent Risks and mitigations Copilot CLI
About Copilot CLI Comparing CLI features Cancel and roll back About remote control Custom agents
About CLI plugins Enterprise plugin standards Autonomous task completion Parallel ...

### GitHub Copilot: Content exclusion documentation

- Change type: `new-source-baseline`
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

> ... lot billing Models and pricing Model multipliers for annual plans Billing cycle Seat assignment
License changes Azure billing Agentic audit log events Agent session filters Review excluded files
Copilot usage metrics Copilot usage metrics data Interpret usage metrics Reconciling Copilot usage
metrics Copilot LoC metrics Team-level metrics Example schema Tutorials Al ...

> Configure and audit content exclusion - GitHub Docs Skip to main content GitHub Docs Version: Free,
Pro, & Team Search or ask Copilot Search or ask Copilot Select language: current language is Englis
...

### Codex CLI: OpenAI Codex repository

- Change type: `new-source-baseline`
- Source URL: https://github.com/openai/codex
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... igation Menu Toggle navigation Sign in Appearance settings Platform AI CODE CREATION GitHub
Copilot Write better code with AI GitHub Spark Build and deploy intelligent apps GitHub Models
Manage and compare prompts MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions
Automate any workflow Codespaces Instant dev environments Issues Plan and track w ...

> ... n in Appearance settings Platform AI CODE CREATION GitHub Copilot Write better code with AI
GitHub Spark Build and deploy intelligent apps GitHub Models Manage and compare prompts MCP Registry
New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant
dev environments Issues Plan and track work Code Review Manage code chan ...

### Codex CLI: OpenAI Codex releases

- Change type: `new-source-baseline`
- Source URL: https://github.com/openai/codex/releases
- Status: `200`
- Related repo paths: codex-cli/

Keyword snippets:

> ... tegrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev
environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub
Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret
protection Stop leaks before they start EXPLORE Why GitHub Documentation B ...

> ... 21559 ) Packaged Codex builds can discover and use the bundled patched zsh helper across
supported macOS and Linux targets. ( #23756 , #24171 ) The Python SDK now exposes friendly Sandbox
presets for thread and turn APIs. ( #24772 ) Bug Fixes Markdown tables and multiline lists render
more readably in the TUI, with better column sizing and app-style table formattin ...

> ... os malloc diagnostics @fcoury-oai #24474 Log rollout writer OS errors @etraut-openai #24076
chore: stop consuming legacy config profiles @jif-oai #24131 centralize Responses retry policy
@rhan-oai #23858 [wip] goal shift @jif-oai #24555 chore: drop orphaned codex memories MCP crate
@jif-oai #24558 chore: move memory prompt builder into extension @jif-oai #24562 Ad ...

> ... over a remote transport. ( #24420 ) Vim mode gained text-object editing, improved word/line-end
behavior, and a configurable interrupt-turn binding. ( #24382 , #24380 , #24766 ) /permissions now
understands named permission profiles and displays configured custom profiles. ( #21559 ) Packaged
Codex builds can discover and use the bundled patched zsh helper across supp ...

### Codex Desktop: OpenAI Codex repository

- Change type: `new-source-baseline`
- Source URL: https://github.com/openai/codex
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> ... Codex CLI is a coding agent from OpenAI that runs locally on your computer. If you want Codex in
your code editor (VS Code, Cursor, Windsurf), install in your IDE. If you want the desktop app
experience, run codex app or visit the Codex App page . If you are looking for the cloud-based agent
from OpenAI, Codex Web , go to chatgpt.com/codex . Quickstart Installing a ...

### Codex Desktop: OpenAI Codex config reference

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/openai/codex/main/codex-rs/config.md
- Status: `200`
- Related repo paths: codex-desktop/

Keyword snippets:

> # Configuration docs moved This file has moved. Please see the latest configuration documentation
here: - Full config docs: [docs/config.md](../docs/config.md) - MCP servers section: [docs ...

### Continue.dev: Configuration reference

- Change type: `new-source-baseline`
- Source URL: https://docs.continue.dev/reference
- Status: `200`
- Related repo paths: continue-dev/

Keyword snippets:

> config.yaml Reference | Continue Docs Search... ⌘ K Docs Blog Sign in Checks CLI IDE Extensions
Getting Started Install Quick Start Customization Overview Features Agent Chat Autocomplet ...

> ... . ⌘ K Docs Blog Sign in Checks CLI IDE Extensions Getting Started Install Quick Start
Customization Overview Features Agent Chat Autocomplete Edit Customize Customization Overview Models
MCP servers Rules Prompts Model Providers Model Roles Deep Dives Telemetry Reference config.yaml
Reference Migrating Config to YAML Continue Documentation MCP Server config.json R ...

> ... mpts Model Providers Model Roles Deep Dives Telemetry Reference config.yaml Reference Migrating
Config to YAML Continue Documentation MCP Server config.json Reference (Deprecated) Context
Providers (Deprecated) @Codebase (Deprecated) @Docs (Deprecated) Guides How to Understand Hub vs
Local Configuration Configuring Models, Rules, and Tools Codebase and Documentatio ...

> ... ocs Blog Sign in Checks CLI IDE Extensions Getting Started Install Quick Start Customization
Overview Features Agent Chat Autocomplete Edit Customize Customization Overview Models MCP servers
Rules Prompts Model Providers Model Roles Deep Dives Telemetry Reference config.yaml Reference
Migrating Config to YAML Continue Documentation MCP Server config.json Refer ...

### Continue.dev: Continue repository

- Change type: `new-source-baseline`
- Source URL: https://github.com/continuedev/continue
- Status: `200`
- Related repo paths: continue-dev/

Keyword snippets:

> ... G.md CONTRIBUTING.md LICENSE LICENSE README.md README.md SECURITY.md SECURITY.md package-
lock.json package-lock.json package.json package.json tsconfig.json tsconfig.json worktree-
config.yaml worktree-config.yaml View all files Repository files navigation README Code of conduct
Contributing Apache-2.0 license Security Continue Source-controlled AI checks, enforceable i ...

> ... en-source ai developer-tools jetbrains-plugin vs-code-extenstion llm Resources Readme License
Apache-2.0 license Code of conduct Code of conduct Contributing Contributing Security policy
Security policy Uh oh! There was an error while loading. Please reload this page . Activity Custom
properties Stars 33.4k stars Watchers 158 watching Forks 4.6k forks Report repos ...

> ... Here is an example that performs a security review: --- name : Security Review description :
Review PR for basic security vulnerabilities --- Review this PR and check that : - No secrets or API
keys are hardcoded - All new API endpoints have input validation - Error responses use the standard
error format Install CLI AI checks are powered by the open-source Contin ...

### Windsurf: Windsurf documentation

- Change type: `new-source-baseline`
- Source URL: https://docs.windsurf.com/
- Status: `200`
- Related repo paths: windsurf/

Keyword snippets:

> ... Mode Modes App Deploys Web and Docs Search Memories & Rules Skills AGENTS.md Workflows Worktrees
Model Context Protocol (MCP) Cascade Hooks Accounts Usage Quota Analytics Teams & Enterprise Context
Awareness Overview Fast Context Windsurf Ignore Troubleshooting Common Issues Proxy Configuration
SSL Inspection Linux inotify Limits WSL Issues Gathering Logs Security Fe ...

> ... mmand Code Lenses Terminal Browser Previews AI Commit Messages DeepWiki Codemaps Vibe and
Replace Advanced Agent Command Center Agent Command Center Spaces Devin Devin Local Agent Cascade
Overview Arena Mode Modes App Deploys Web and Docs Search Memories & Rules Skills AGENTS.md
Workflows Worktrees Model Context Protocol (MCP) Cascade Hooks Accounts Usage Quota Ana ...

> ... nter Spaces Devin Devin Local Agent Cascade Overview Arena Mode Modes App Deploys Web and Docs
Search Memories & Rules Skills AGENTS.md Workflows Worktrees Model Context Protocol (MCP) Cascade
Hooks Accounts Usage Quota Analytics Teams & Enterprise Context Awareness Overview Fast Context
Windsurf Ignore Troubleshooting Common Issues Proxy Configuration SSL Insp ...

> ... ess Overview Fast Context Windsurf Ignore Troubleshooting Common Issues Proxy Configuration SSL
Inspection Linux inotify Limits WSL Issues Gathering Logs Security FedRAMP Security Admin Guide
Reporting On this page Set Up Onboarding 1. Select setup flow 2. Choose editor theme 3. Sign up /
Log in Having Trouble? 4. Let’s Surf! Update Windsurf Things to Try Forgot ...

### Windsurf: Windsurf changelog

- Change type: `new-source-baseline`
- Source URL: https://windsurf.com/changelog
- Status: `200`
- Related repo paths: windsurf/

Keyword snippets:

> ... cade 1.13.9 January 16, 2026 1.13.9 January 16, 2026 Bug Fixes and Improvements Improvements to
GPT-5.2-Codex harness Admins can now manage Windsurf restrictions via Windows Group Policy 1.13.8
January 14, 2026 1.13.8 January 14, 2026 GPT-5.2-Codex Adds support for GPT-5.2-Codex with four
reasoning efforts (low, medium, high, and xhigh). GPT-5.2-Codex is OpenAI's ...

> ... rolling out gradually. If you don't see it yet, try logging out of the website and IDE then
logging back in. Devin Cloud is disabled by default for enterprise accounts. Enterprise admins
should enable Devin access in their organization settings if they have already purchased Cognition
Platform. Agent Command Center New Kanban-style view showing all local and clou ...

> ... indsurf Editor Pricing Windsurf for Enterprise Capabilities Cascade Tab JetBrains Plugin Company
About Us Blog Careers Support Contact Partnerships Terms of Service Privacy Policy Security Windsurf
for Government Resources Docs Changelog Releases Brand Referrals University Windsurf vs Cursor
Windsurf vs Copilot 2025 Gartner Magic Quadrant Arena Leaderboard Connect U ...

> ... agent to 2026.5.26. See the changelog for the full list of changes. Devin Local is now aware of
the files you have open in the editor as part of its context. When prompted for an MCP tool
permission in Devin Local, two additional server-level options are now offered: approve all tools on
the server for the current session, or permanently. Repaired hooks for De ...

> ... le scroll-to-next-hunk settings (default off) Preserved colors and styling in Cascade terminal
output Multiple fixes to the Model Context Protocol implementation Supports lowering permissions for
Cascade's Web Fetch tool Fix race condition in the dedicated terminal implementation Support force
killing commands in the dedicated terminal Improved markdown completion Fix ...

### Tabnine: Tabnine admin documentation

- Change type: `new-source-baseline`
- Source URL: https://docs.tabnine.com/
- Status: `200`
- Related repo paths: tabnine/

Keyword snippets:

> ... & Feedback Getting started Install Quickstart Guide Context Engine Tabnine Agent Tabnine Chat
Tabnine Testing Tabnine CLI Code Completions Inline Actions Tabnine's Prompting Guide Administering
Tabnine Private Installation Release Notes Powered by GitBook On this page Copy On this page Welcome
Overview What is Tabnine? Tabnine is the AI code assistant that accele ...

> Overview | Tabnine Docs ⌘ Ctrl k Tabnine website Contact Sales More Welcome Overview Architecture
Security Privacy Protection Personalization AI Models Integrations System & Hardware Requirements
Supported Languages Supported IDEs Tabnine Subscription Plans Support & Feedback Getting started I
...

### Tabnine: Tabnine enterprise documentation

- Change type: `new-source-baseline`
- Source URL: https://www.tabnine.com/enterprise
- Status: `200`
- Related repo paths: tabnine/

No configured watch keywords were found in the fetched content.

### Amazon Q Developer: Amazon Q Developer administration guide

- Change type: `new-source-baseline`
- Source URL: https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-admin.html
- Status: `200`
- Related repo paths: amazon-q-developer/

No configured watch keywords were found in the fetched content.

### Amazon Q Developer: Amazon Q Developer IAM reference

- Change type: `new-source-baseline`
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

- Change type: `new-source-baseline`
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

> ... n in Appearance settings Platform AI CODE CREATION GitHub Copilot Write better code with AI
GitHub Spark Build and deploy intelligent apps GitHub Models Manage and compare prompts MCP Registry
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

- Change type: `new-source-baseline`
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
languages, frameworks, and tools / Console English Deutsch Español Español – América L ...

### Google Gemini: Vertex AI Gemini safety settings

- Change type: `new-source-baseline`
- Source URL: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters
- Status: `200`
- Related repo paths: google-gemini/

Keyword snippets:

> ... nt Remove objects from an image using inpaint Expand the content of an image using outpaint
Replace the background of an image Configure Imagen parameters Configure Responsible AI safety
settings Use prompt rewriter Set text prompt language Configure aspect ratio Set output resolution
Omit content using a negative prompt Generate deterministic images Generate images for re ...

> ... ribes each of the safety and content filter types and outlines key safety concepts. For
configurable content filters, it shows you how to configure the blocking thresholds of each harm
category to control how often prompts and responses are blocked. There are also examples provided to
demonstrate how to program a configurable content filter. Safety and content filters ac ...

> ... ased on your preferences. To see an example of getting started with Responsible AI with Vertex
AI Gemini API, run the "Responsible AI with Vertex AI Gemini API: Safety ratings and thresholds"
notebook in one of the following environments: Open in Colab | Open in Colab Enterprise | Open in
Vertex AI Workbench | View on GitHub Google's generative AI models, like Gemini ...

> ... ts Capabilities Safety Overview Responsible AI System instructions for safety Configure content
filters Gemini for safety filtering and content moderation Abuse monitoring Process blocked
responses Content Credentials Text and code generation Text generation System instructions Function
calling Structured output Content generation parameters Code execution Medical ...

> Safety and content filters | Generative AI on Vertex AI | Google Cloud Documentation Skip to main
content Technology areas close AI and ML Application development Application hosting Compute Data
analytics ...

### Google Gemini: Google Cloud organization policies

- Change type: `new-source-baseline`
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

- Change type: `new-source-baseline`
- Source URL: https://docs.anthropic.com/en/docs/claude-code/mcp
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... h credentials Override OAuth metadata discovery Restrict OAuth scopes Use dynamic headers for
custom authentication Add MCP servers from JSON configuration Import MCP servers from Claude Desktop
Use MCP servers from Claude.ai Use Claude Code as an MCP server MCP output limits and warnings Raise
the limit for a specific tool Respond to MCP elicitation requests Use MCP reso ...

> Connect Claude Code to tools via MCP - Claude Code Docs Skip to main content Claude Code Docs home
page English Search... ⌘ K Ask Assistant Claude Developer Platform Claude Code on the Web Claude
Code on the Web Sear ...

> ... bleshooting Troubleshoot installation and login Troubleshoot performance and stability Debug
configuration Error reference On this page What you can do with MCP Find and build MCP servers
Installing MCP servers Option 1: Add a remote HTTP server Option 2: Add a remote SSE server Option
3: Add a local stdio server Managing your servers Dynamic tool updates Automati ...

> ... orm Claude Code on the Web Claude Code on the Web Search... Navigation Tools and plugins Connect
Claude Code to tools via MCP Getting started Build with Claude Code Administration Configuration
Reference Agent SDK What's New Resources Agents and parallel work Overview Create custom subagents
Agent view Run agent teams Dynamic workflows Isolate sessions with worktrees Too ...

### Claude Desktop: Claude Desktop support documentation

- Change type: `new-source-baseline`
- Source URL: https://support.anthropic.com/en/
- Status: `200`
- Related repo paths: claude-desktop/

Keyword snippets:

> ... les Pro and Max plans 15 articles Team and Enterprise plans 55 articles Claude API and Console
40 articles Identity management (SSO, JIT, SCIM) 15 articles Claude Code 19 articles Claude Desktop
9 articles Claude Mobile apps 20 articles Connectors 20 articles Claude in Chrome 5 articles Claude
for Education 4 articles Claude for Nonprofits 6 articles Privacy and legal 20 ...

> ... Italiano 日本語 한국어 Português Pусский 简体中文 Español 繁體中文 English Search for answers or browse by
topic Search for articles... Claude 84 articles Pro and Max plans 15 articles Team and Enterprise
plans 55 articles Claude API and Console 40 articles Identity management (SSO, JIT, SCIM) 15
articles Claude Code 19 articles Claude Desktop 9 articles Claude Mobile apps 20 artic ...

### OpenAI Platform: OpenAI OpenAPI repository

- Change type: `new-source-baseline`
- Source URL: https://github.com/openai/openai-openapi
- Status: `200`
- Related repo paths: openai-platform/

No configured watch keywords were found in the fetched content.

### OpenAI Platform: OpenAI OpenAPI schema

- Change type: `new-source-baseline`
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

### Claude API: Anthropic admin API documentation

- Change type: `new-source-baseline`
- Source URL: https://docs.anthropic.com/en/api/admin-api
- Status: `200`
- Related repo paths: claude-api/

No configured watch keywords were found in the fetched content.

### Claude API: Anthropic API release notes

- Change type: `new-source-baseline`
- Source URL: https://docs.anthropic.com/en/release-notes/api
- Status: `200`
- Related repo paths: claude-api/

Keyword snippets:

> ... de Opus 4.7. Set speed: "fast" with model: "claude-opus-4-7" and the fast-mode-2026-02-01 beta
header for significantly faster output token generation at premium pricing. Pricing, rate limits,
and access are the same as for Opus 4.6 fast mode; interested customers should join the waitlist .
May 11, 2026 We've launched Claude Platform on AWS , bringing the Claude API t ...

> ... o beta header required. April 24, 2026 We've released the Rate Limits API , allowing
administrators to programmatically query the rate limits configured for their organization and
workspaces. April 23, 2026 Memory for Claude Managed Agents is now in public beta under the standard
managed-agents-2026-04-01 header. See Using agent memory for the full integration guide. ...

> ... to provide any tools when including tool_use and tool_result blocks. We've launched an OpenAI-
compatible API endpoint, allowing you to test Claude models by changing just your API key, base URL,
and model name in existing OpenAI integrations. This compatibility layer supports core chat
completions functionality. Learn more in OpenAI SDK compatibility . February ...

> ... mer stories Engineering at Anthropic Events Powered by Claude Service partners Startups program
Company Anthropic Careers Economic Futures Research News Responsible Scaling Policy Security and
compliance Transparency Learn Blog Courses Use cases Connectors Customer stories Engineering at
Anthropic Events Powered by Claude Service partners Startups program Help and s ...

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

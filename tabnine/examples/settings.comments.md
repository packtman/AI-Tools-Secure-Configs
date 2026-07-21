# Tabnine CLI system settings comments

The three `settings-*.json` files are valid JSON for Tabnine CLI system settings. This companion documents each non-trivial key without making the deployable files invalid.

## General settings

| Key | What it does | Why it is set | What breaks if changed or removed |
|-----|--------------|---------------|-----------------------------------|
| `general.defaultApprovalMode` | Selects read-only planning, confirmation for every action, or automatic file edits. | Strict uses `plan`, Moderate uses `default`, and Baseline uses `auto_edit` to match each tier's human-review requirement. | A more permissive value lets the agent change files with less review. A more restrictive value blocks normal editing workflows. |
| `general.debugKeystrokeLogging` | Writes terminal keystrokes to debug output. | It is disabled in every tier to prevent prompts, paths, or pasted secrets from entering console logs. | Enabling it can expose sensitive terminal input to logs and screen recordings. |
| `general.devtools` | Opens the developer tools inspector at startup. | It is disabled in every tier because normal users do not need a debugging surface that can expose session state. | Enabling it increases local data exposure. Removing it restores the vendor default, which is currently disabled but can drift. |

## Tool settings

| Key | What it does | Why it is set | What breaks if changed or removed |
|-----|--------------|---------------|-----------------------------------|
| `tools.enableRemoteCodeSearch` | Allows Tabnine Remote Code Search to retrieve organization code context. | Strict and Moderate disable it until repository scope and data handling are approved. Baseline keeps it enabled for normal search workflows. | Disabling it removes remote repository context. Enabling it without repository governance can expose code outside the active workspace. |
| `tools.sandbox` | Runs tool execution in Tabnine's supported sandbox. | Every tier enables it to reduce filesystem, process, and network blast radius. | Removing it can run tools with the user's full host permissions. Enabling it without Docker, Podman, or the supported OS sandbox can prevent commands from starting. |
| `tools.shell.enableInteractiveShell` | Allows interactive shell sessions. | Strict disables it because long-lived interactive processes are harder to approve and audit. | Disabling it breaks REPLs, interactive installers, debuggers, and commands that prompt for input. |

## Security settings

| Key | What it does | Why it is set | What breaks if changed or removed |
|-----|--------------|---------------|-----------------------------------|
| `security.disableYoloMode` | Blocks the `--yolo` and `--approval-mode=yolo` bypasses. | It is enabled in every tier because unrestricted automatic approval defeats tool policy. | Removing it lets users bypass confirmation from CLI flags. |
| `security.disableAlwaysAllow` | Removes persistent "Always allow" choices from approval dialogs. | Strict and Moderate enable it so a one-time approval cannot silently become permanent. Baseline leaves the choice visible for lower-friction local work. | Enabling it increases repeat prompts. Disabling it allows users to create durable approvals that may outlive the original task. |
| `security.enablePermanentToolApproval` | Shows the option to approve a tool for future sessions. | It is disabled in every tier because durable tool grants are difficult to review and expire. | Enabling it reduces prompts but can preserve unsafe permissions indefinitely. |
| `security.autoAddToPolicyByDefault` | Preselects permanent approval for low-risk tools. | It is disabled in every tier to require an intentional policy change. | Enabling it can turn a routine approval into a persistent rule by mistake. |
| `security.blockGitExtensions` | Blocks extensions installed directly from Git. | It is enabled in every tier to prevent unreviewed repository code from becoming a Tabnine extension. | Removing it restores Git extension installation and increases supply-chain risk. |
| `security.allowedExtensions` | Defines extension patterns allowed despite the Git extension block. | Strict uses an empty list so no exception is implied. Moderate and Baseline omit it so admins can add reviewed exceptions without replacing a strict deny list. | Adding a broad regular expression can bypass the Git extension block. An empty list can block required enterprise extensions. |
| `security.folderTrust.enabled` | Requires workspace trust checks before workspace settings and skills load. | It is enabled in every tier so an untrusted repository cannot activate local instructions or tools. | Disabling it allows repository-controlled configuration to load immediately. Misclassifying a trusted repository blocks workspace skills and settings. |
| `security.enableConseca` | Enables Tabnine's context-aware security checker. | Strict and Moderate enable it for an additional decision layer. Baseline leaves it off to reduce false-positive friction. | Enabling it can delay or block legitimate tool calls. Disabling it removes contextual detection of risky actions. |
| `security.environmentVariableRedaction.enabled` | Redacts environment variable values that appear secret-like. | It is enabled in every tier to reduce credential exposure in context and telemetry. | Disabling it can send secrets to the model or logs. Over-redaction can hide variables needed to diagnose a command. |
| `security.environmentVariableRedaction.allowed` | Lists variables that must never be redacted. | It is empty in every tier because no secret-bearing variable needs a blanket exception. | Adding a secret variable exposes its value. Leaving a required non-secret variable redacted can reduce diagnostic context. |
| `security.environmentVariableRedaction.blocked` | Lists variables that must always be redacted. | Common AI and cloud credential variables are explicitly blocked as defense in depth. | Removing an entry relies only on automatic detection. Adding broad non-secret variables can break debugging context. |

## Context, telemetry, MCP, hooks, and skills

| Key | What it does | Why it is set | What breaks if changed or removed |
|-----|--------------|---------------|-----------------------------------|
| `context.fileFiltering.respectGitIgnore` | Excludes Git-ignored files from context search. | It is enabled in every tier because ignored files often include generated output or local secrets. | Disabling it may expose ignored credentials and increases context noise. Some ignored fixtures may need an explicit exception. |
| `context.fileFiltering.respectGeminiIgnore` | Applies `.tabnineignore` rules despite the vendor key's historical name. | It is enabled in every tier to give administrators a Tabnine-specific exclusion layer. | Disabling it makes `.tabnineignore` ineffective and can expose intentionally excluded files. |
| `telemetry.enabled` | Exports local OpenTelemetry data. | It is disabled in the templates until an organization-owned collector and retention policy are configured. | Enabling it without replacing the default collector can fail or route data incorrectly. Leaving it disabled removes local CLI telemetry from the SIEM. |
| `telemetry.logPrompts` | Includes prompts and messages in telemetry attributes. | It is disabled in every tier because prompts can contain source code, secrets, or personal data. | Enabling it improves troubleshooting but creates a sensitive log data set. |
| `mcp.allowed` | Limits locally configured MCP servers by name. | Strict uses an empty allowlist and also requires Admin Console `Block all`. Other tiers use the Admin Console allowlist because local server names are organization-specific. | An empty list blocks MCP workflows. A broad list permits tools that can read data or perform remote actions. |
| `hooksConfig.enabled` | Enables lifecycle hooks from settings and extensions. | Strict disables hooks because there is no local managed-only hook mode. Moderate and Baseline allow hooks after pilot review. | Disabling it breaks compliance and workflow hooks. Enabling it lets repository or extension hooks execute commands. |
| `skills.enabled` | Enables Agent Skills discovered from built-in, extension, user, and trusted workspace locations. | Strict disables skills because workspace skills can contain executable scripts. Moderate and Baseline allow reviewed skills. | Disabling it removes reusable workflows. Enabling it without trust review can load malicious instructions or scripts. |

## Source references

- [Tabnine CLI settings](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/settings)
- [Tabnine CLI settings reference](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/settings/settings-reference.md)
- [Tabnine MCP governance](https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/mcp-governance.md)
- [Tabnine Agent Skills](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/agent-skills.md)

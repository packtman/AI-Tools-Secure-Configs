# Config Discovery Report

This report was generated because one or more watched upstream sources changed.
Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.

## Summary

| Tool | Source | Change | Status | URL |
|------|--------|--------|--------|-----|
| Gemini CLI | Gemini CLI settings schema | new-source-baseline | 200 | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json |
| Gemini CLI | Gemini CLI enterprise controls | new-source-baseline | 200 | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/admin/enterprise-controls.md |
| Gemini CLI | Gemini CLI policy engine | new-source-baseline | 200 | https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/policy-engine.md |
| Google Gemini | Vertex AI Gemini safety reference | new-source-baseline | 200 | https://raw.githubusercontent.com/GoogleCloudPlatform/vertex-ai-samples/main/skills/genai-sdk/references/safety.md |
| Google Gemini | Google Cloud organization policies | content-changed | 200 | https://cloud.google.com/resource-manager/docs/organization-policy/overview |

## Review Details

### Gemini CLI: Gemini CLI settings schema

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/schemas/settings.schema.json
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> ... ng. Isolates individual tools instead of the entire CLI process.\n\n- Category: `Security`\n-
Requires restart: `yes`\n- Default: `false`", "default": false, "type": "boolean" },
"disableYoloMode": { "title": "Disable YOLO Mode", "description": "Disable YOLO mode, even if
enabled by a flag.", "markdownDescription": "Disable YOLO mode, even if enabled by a flag.\n\n-
Catego ...

> ... hether Folder trust is enabled.\n\n- Category: `Security`\n- Requires restart: `yes`\n- Default:
`true`", "default": true, "type": "boolean" } }, "additionalProperties": false },
"environmentVariableRedaction": { "title": "Environment Variable Redaction", "description":
"Settings for environment variable redaction.", "markdownDescription": "Settings for environment
variable redaction.\ ...

> ... ownDescription": "Hide the current working directory in the footer.\n\n- Category: `UI`\n-
Requires restart: `no`\n- Default: `false`", "default": false, "type": "boolean" },
"hideSandboxStatus": { "title": "Hide Sandbox Status", "description": "Hide the sandbox status
indicator in the footer.", "markdownDescription": "Hide the sandbox status indicator in the foote
...

> ... kills.\n\n- Category: `Advanced`\n- Requires restart: `yes`\n- Default: `[]`", "default": [],
"type": "array", "items": { "type": "string" } } }, "additionalProperties": false }, "hooksConfig":
{ "title": "HooksConfig", "description": "Hook configurations for intercepting and customizing agent
behavior.", "markdownDescription": "Hook configurations for intercepting and ...

> ... quires restart: `yes`\n- Default: `false`", "default": false, "type": "boolean" }, "autoMemory":
{ "title": "Auto Memory", "description": "Automatically extract memory patches and skills from past
sessions in the background. Every change is written as a unified diff `.patch` file under ` /.inbox/
/` and held for review in /memory inbox; nothing is applied until yo ...

Potential config terms found upstream are already present in local tool files.

### Gemini CLI: Gemini CLI enterprise controls

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/admin/enterprise-controls.md
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> # Enterprise Admin Controls Gemini CLI empowers enterprise administrators to manage and enforce
security policies and configuration settings across their entire organization. Secure defaults are
ena ...

> ... le/manage-gemini-cli). **Enterprise Admin Controls are enforced globally and cannot be
overridden by users locally**, ensuring a consistent security posture. ## Admin Controls vs. System
Settings While [System-wide settings](../cli/settings.md) act as convenient configuration overrides,
they can still be modified by users with sufficient privileges. In contrast, admin cont ...

> ... tp`). Local execution fields (`command`, `args`, `env`, `cwd`) are not supported. - Required
servers can coexist with allowlisted servers - both features work independently. ### Unmanaged
Capabilities **Enabled/Disabled** | Default: disabled If disabled, users will not be able to use
certain features. Currently, this control disables Agent Skills. See [Agent Skills ...

> ... rides, they can still be modified by users with sufficient privileges. In contrast, admin
controls are immutable at the local level, making them the preferred method for enforcing policy. ##
Available Controls ### Strict Mode **Enabled/Disabled** | Default: enabled If enabled, users will
not be able to enter yolo mode. ### Extensions **Enabled/Disabled** | Default ...

> # Enterprise Admin Controls Gemini CLI empowers enterprise administrators to manage and enforce
security policies and configuration settings across their entire organization. Secure defaults are
enabled automatically for all enterprise users, but can be customized via the [Management ...

### Gemini CLI: Gemini CLI policy engine

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/policy-engine.md
- Status: `200`
- Related repo paths: gemini-cli/

Keyword snippets:

> # Policy engine Gemini CLI includes a powerful policy engine that provides fine-grained control over
tool execution. It allows users and administrators to define rules that determine wheth ...

> # Policy engine Gemini CLI includes a powerful policy engine that provides fine-grained control over
tool execution. It allows users and administrators to define rules that determine whether a tool
call should be allowed, denied, or require user confirmation. ## Quick start To create your first
policy: 1 ...

> ... any filename ending in `.toml`; all such files in this directory will be loaded and combined:
```toml [[rule]] toolName = "run_shell_command" commandPrefix = "rm -rf" decision = "deny" priority
= 100 ``` 3. **Run a command** that triggers the policy (for example, ask Gemini CLI to `rm -rf /`).
The tool will now be blocked automatically. ## Core concepts The pol ...

> # Policy engine Gemini CLI includes a powerful policy engine that provides fine-grained control over
tool execution. It allows users and administrators to define rules that determine whether a tool
call should be allowed, denied, or require user confirmation. ## Quick start To create ...

> ... ilename ending in `.toml`; all such files in this directory will be loaded and combined: ```toml
[[rule]] toolName = "run_shell_command" commandPrefix = "rm -rf" decision = "deny" priority = 100
``` 3. **Run a command** that triggers the policy (for example, ask Gemini CLI to `rm -rf /`). The
tool will now be blocked automatically. ## Core concepts The policy engine ...

Potential config terms not found in local tool files:

`adminPolicyPaths`, `autoEdit`, `mcpName`, `mcp_`, `mcp_server_search`, `mcp_server_tool`

Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.

### Google Gemini: Vertex AI Gemini safety reference

- Change type: `new-source-baseline`
- Source URL: https://raw.githubusercontent.com/GoogleCloudPlatform/vertex-ai-samples/main/skills/genai-sdk/references/safety.md
- Status: `200`
- Related repo paths: google-gemini/

Keyword snippets:

> ... ngs that I might say to the universe after stubbing my toe in the dark.",
config=types.GenerateContentConfig( system_instruction="Be as mean as possible.", safety_settings=[
types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), types.SafetySetting(
category=types.HarmCategory.HARM_CATE ...

> ... iverse after stubbing my toe in the dark.", config=types.GenerateContentConfig(
system_instruction="Be as mean as possible.", safety_settings=[ types.SafetySetting(
category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), types.SafetySetting(
category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=ty ...

> ... ateContentConfig( system_instruction="Be as mean as possible.", safety_settings=[
types.SafetySetting( category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), types.SafetySetting(
category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), types.SafetySetting( ...

> ... ystem_instruction="Be as mean as possible.", safety_settings=[ types.SafetySetting(
category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), types.SafetySetting(
category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE, ), types.SafetySetting( category=types.HarmC
...

### Google Gemini: Google Cloud organization policies

- Change type: `content-changed`
- Source URL: https://cloud.google.com/resource-manager/docs/organization-policy/overview
- Status: `200`
- Related repo paths: google-gemini/

No configured watch keywords were found in the fetched content.

## Required Follow-Up

1. Read the changed upstream source.
2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.
3. If a config change is needed, update only the affected tool and tier files.
4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.
5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.
6. Validate edited JSON, YAML, TOML, or shell files before merging.

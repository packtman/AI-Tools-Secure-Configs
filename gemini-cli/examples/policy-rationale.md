# Gemini CLI — Policy Rationale

Every setting below explains **what it does**, **why you should care**, and **the recommended value** for different environments.

---

## `tools.sandbox`

**What it does:** Controls whether tool execution (shell commands, file operations) runs inside a container sandbox.

**Why it matters:** Without sandbox isolation, the AI agent executes commands directly on the host system with the user's full permissions. A prompt injection attack or hallucinated command could delete files, install malware, or exfiltrate data.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated (finance, healthcare) | `"docker"` | All execution in isolated containers. Prevents host system access. |
| Standard enterprise | `"docker"` | Same. Docker should be available on all developer machines. |
| Individual developers | `"docker"` or `true` | Sandbox is always recommended. Use `false` only if Docker is unavailable. |

---

## `tools.core` (Allowlist)

**What it does:** Explicitly lists the only tools the AI agent can use. Any tool not on this list is unavailable.

**Why it matters:** This is the most powerful security control. By default, Gemini CLI exposes all built-in tools. An allowlist ensures the agent can only use approved operations.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Read-only tools only | `ReadFileTool`, `GlobTool`, `GrepTool`, `ListDirectoryTool`. No write or shell. |
| Standard enterprise | Read/write + safe shell | Add `WriteFileTool`, `EditFileTool`, `ShellTool(git)`, `ShellTool(npm test)`. |
| Individual developers | Broad allowlist or omit | Pair broad access with `admin-policy-baseline.toml` for catastrophic command denies. |

---

## Admin policy TOML

**What it does:** Applies administrator-owned `allow`, `deny`, or `ask_user` decisions to tool calls. Admin policy rules override user policy rules.

**Why it matters:** The legacy `tools.exclude` setting is deprecated. Admin policy rules provide explicit precedence, approval behavior, shell-prefix matching, and MCP matching.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `admin-policy-strict.toml` | Deny shell, file-changing, and MCP tools at the admin tier. |
| Standard enterprise | `admin-policy-moderate.toml` | Deny destructive commands and require approval for shell, file changes, and MCP. |
| Individual developers | `admin-policy-baseline.toml` | Deny only catastrophic shell prefixes and preserve broad workflows. |

**What breaks if removed or misconfigured:** Deprecated blocklists may stop working in a future release. A writable or incorrectly owned admin policy directory is ignored, so user policy rules can take effect instead.

---

## `mcp.allowed` (MCP Allowlist)

**What it does:** Restricts which MCP (Model Context Protocol) servers can run. Only servers whose names appear in this list are enabled.

**Why it matters:** MCP servers are arbitrary programs that the AI can invoke. An unauthorized MCP server could execute any code, access any data, or communicate with external services.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `[]` (empty array) | No MCP servers permitted. Zero external integrations. |
| Standard enterprise | Explicit list of approved servers | Only IT-audited and approved servers. Define them in `mcpServers` too. |
| Individual developers | Omit (all allowed) or light allowlist | Personal choice, but encourage review of server code. |

---

## `mcpServers.<name>.includeTools`

**What it does:** Restricts which specific tools from an MCP server are exposed to the AI model.

**Why it matters:** Even an approved MCP server might expose dangerous tools (e.g., `delete-all`, `drop-database`). Restricting to specific tools follows least-privilege.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | Always use | Only expose the specific tools needed. Never trust a server blindly. |

---

## `mcpServers.<name>.trust`

**What it does:** If `true`, bypasses the confirmation dialog for all tool calls to this server.

**Why it matters:** Auto-approving tool calls removes the human-in-the-loop for that server. A compromised or buggy server could execute harmful operations without any user review.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Never `true` | All tool calls must be reviewed. |
| Standard enterprise | `false` or omit | Require confirmation for all MCP calls. |
| Individual developers | Use sparingly | Only for well-understood, read-only tools. |

---

## `security.auth.enforcedType`

**What it does:** Forces all users to authenticate with a specific method. Users cannot choose an alternative.

**Why it matters:** Ensures corporate identity is used for all Gemini CLI sessions, enabling audit trails and access control.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Enterprise (any) | `"oauth-personal"` | Google login ties sessions to corporate identity. Enables audit. |
| CI/CD pipelines | `"vertex-ai"` | Use Vertex AI with Application Default Credentials or `GOOGLE_APPLICATION_CREDENTIALS`. |
| Individual developers | Omit (user choice) | No enforcement needed. |

---

## `security.folderTrust.enabled`

**What it does:** Requires users to explicitly trust a project folder before Gemini CLI loads project-level settings and context files.

**Why it matters:** A malicious repository could include `.gemini/settings.json` or `GEMINI.md` with harmful instructions or tool configurations. Folder trust prevents automatic loading.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | `true` | Always require explicit trust. Prevents supply-chain attacks via repository configs. |

---

## `security.disableYoloMode`

**What it does:** Prevents users from entering YOLO mode, which runs tools without confirmation prompts.

**Why it matters:** Disabling approval prompts lets a prompt injection or mistaken instruction execute tools without a human checkpoint. Google highly recommends this setting for enterprise deployments.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All managed tiers | `true` | Keep a human approval boundary even in developer-focused environments. |

**What breaks if removed or misconfigured:** Users can select YOLO mode and bypass normal confirmation prompts.

---

## `security.disableAlwaysAllow`

**What it does:** Prevents users from saving permanent tool approvals.

**Why it matters:** A permanent approval can silently carry an old trust decision into a new repository or session.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated and standard enterprise | `true` | Require a fresh decision for each sensitive operation. |
| Individual developers | `false` | Preserve opt-in permanent approvals where endpoint policy permits them. |

**What breaks if misconfigured:** Setting it to `true` removes the "always allow" workflow and increases approval prompts. Setting it to `false` allows durable user exceptions.

---

## `security.environmentVariableRedaction`

**What it does:** Removes environment variables with secret-like names from hook processes. The `allowed` list restores only variables an approved hook requires.

**Why it matters:** Hooks run with the user's privileges and can otherwise inherit API keys, tokens, and credentials. Redaction is disabled by default upstream.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All managed tiers | `enabled: true`, minimal `allowed` list | Prevent accidental secret exposure to project or extension hooks. |

**What breaks if misconfigured:** Hooks that legitimately require a redacted variable fail until IT adds that exact variable name to `allowed`. Disabling redaction exposes the full inherited environment.

---

## `hooksConfig.enabled`

**What it does:** Enables or disables Gemini CLI hooks.

**Why it matters:** Hooks execute arbitrary commands as the signed-in user. Project and extension hooks expand the code-execution surface.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | Remove hook execution unless IT has a separately approved deployment. |
| Standard enterprise | `true` | Preserve linting and validation hooks with environment redaction enabled. |
| Individual developers | `true` | Preserve workflows, with folder trust and redaction as safeguards. |

**What breaks if misconfigured:** Disabling hooks stops project automation, validation, and audit hooks. Enabling unreviewed hooks can expose secrets or execute hostile code.

---

## `telemetry.enabled` and `telemetry.logPrompts`

**What it does:** Controls whether usage telemetry is collected, and whether user prompt content is included in telemetry data.

**Why it matters:** Telemetry provides visibility for audit and compliance. However, logging prompts captures potentially sensitive code and business logic.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `enabled: true`, `logPrompts: false` | Need audit trail but cannot capture sensitive code in logs. |
| Standard enterprise | `enabled: true`, `logPrompts: false` | Same — audit without data exposure. |
| Individual developers | `enabled: false` | Minimal data collection for personal use. |

---

## `privacy.usageStatisticsEnabled`

**What it does:** Controls whether general usage statistics are sent to Google.

**Why it matters:** Usage statistics may include metadata about how the tool is used. Enterprise environments typically disable external telemetry.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Enterprise (any) | `false` | Do not send usage data to external parties. |
| Individual developers | User choice | Personal preference. |

---

## `general.enableAutoUpdate`

**What it does:** Controls whether Gemini CLI automatically downloads and installs updates. This replaces deprecated `general.disableAutoUpdate` with the opposite boolean meaning.

**Why it matters:** Auto-updates ensure security patches but bypass IT testing and approval processes.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | IT must test and approve each version. |
| Standard enterprise | `true` | Auto-updates ensure timely security patches. |
| Individual developers | `true` | Stay current with latest features. |

---

## `model.maxSessionTurns`

**What it does:** Limits the maximum number of turns (user/model/tool interactions) in a single session.

**Why it matters:** Unbounded sessions increase the risk of context confusion and unintended escalation. A limit forces periodic human review.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `20` | Short sessions force frequent human oversight. |
| Standard enterprise | `50` | Reasonable limit for productive sessions. |
| Individual developers | `-1` (unlimited) | No artificial limit. |

---

## Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for difference |
|---------|----------|----------|--------|-----------------------|
| `general.enableAutoUpdate` | `true` | `true` | `false` | Strict requires tested, centrally deployed versions. Other tiers prioritize rapid security updates. |
| `tools.core` | Omitted | Read/write and scoped shell allowlist | Read-only allowlist | Higher tiers reduce the operations exposed to the model. |
| Admin policy TOML | Deny catastrophic shell prefixes | Deny destructive prefixes, ask for shell, writes, and MCP | Deny shell, writes, and MCP | Approval and tool restrictions increase with risk. |
| `mcp.allowed` | Omitted | `["corp-tools"]` | `[]` | Strict disables external tools, Moderate permits only a vetted server, Baseline allows local choice. |
| `security.disableYoloMode` | `true` | `true` | `true` | Every managed tier retains confirmation prompts. |
| `security.disableAlwaysAllow` | `false` | `true` | `true` | Baseline permits durable user approvals; higher tiers require fresh review. |
| `security.environmentVariableRedaction.enabled` | `true` | `true` | `true` | Hook environments should not inherit likely secrets in any tier. |
| `hooksConfig.enabled` | `true` | `true` | `false` | Strict removes arbitrary hook execution; other tiers preserve automation. |
| `security.auth.enforcedType` | Omitted | `"oauth-personal"` | `"oauth-personal"` | Enterprise tiers require managed identity. |
| `telemetry.enabled` | `false` | `true` | `true` | Enterprise tiers need metadata audit visibility. |
| `telemetry.logPrompts` | `false` | `false` | `false` | Prompt contents can contain source code and secrets. |
| `model.maxSessionTurns` | `-1` | `50` | `20` | Higher tiers force more frequent human checkpoints. |

---

## Summary: Recommended Profiles

### Maximum Lockdown (Regulated)

```json
{
  "tools": { "sandbox": "docker", "core": ["ReadFileTool", "GlobTool", "GrepTool", "ListDirectoryTool"] },
  "mcp": { "allowed": [] },
  "security": { "disableYoloMode": true, "disableAlwaysAllow": true, "environmentVariableRedaction": { "enabled": true, "allowed": [] }, "auth": { "enforcedType": "oauth-personal" } },
  "hooksConfig": { "enabled": false },
  "telemetry": { "enabled": true, "logPrompts": false },
  "privacy": { "usageStatisticsEnabled": false },
  "general": { "enableAutoUpdate": false }
}
```

### Standard Enterprise

```json
{
  "tools": { "sandbox": "docker", "core": ["ReadFileTool", "WriteFileTool", "EditFileTool", "GlobTool", "GrepTool", "ListDirectoryTool", "ShellTool(git)", "ShellTool(npm test)"] },
  "mcp": { "allowed": ["corp-tools"] },
  "security": { "disableYoloMode": true, "disableAlwaysAllow": true, "environmentVariableRedaction": { "enabled": true, "allowed": [] }, "auth": { "enforcedType": "oauth-personal" } },
  "hooksConfig": { "enabled": true },
  "telemetry": { "enabled": true, "logPrompts": false },
  "privacy": { "usageStatisticsEnabled": false }
}
```

### Developer Teams

```json
{
  "tools": { "sandbox": "docker" },
  "mcp": {},
  "security": { "disableYoloMode": true, "disableAlwaysAllow": false, "environmentVariableRedaction": { "enabled": true, "allowed": [] }, "folderTrust": { "enabled": true } },
  "hooksConfig": { "enabled": true },
  "telemetry": { "enabled": false, "logPrompts": false },
  "privacy": { "usageStatisticsEnabled": false }
}
```

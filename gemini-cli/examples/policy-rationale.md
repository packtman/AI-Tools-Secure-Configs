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
| Individual developers | Broad allowlist or omit | Can use `tools.exclude` blocklist instead for lighter restrictions. |

---

## `tools.exclude` (Blocklist)

**What it does:** Blocks specific tools by name. All other tools remain available.

**Why it matters:** Less secure than allowlisting because it only blocks known-bad patterns. Users may find creative workarounds. Use only when `tools.core` is too restrictive for your needs.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | Don't use — use `tools.core` instead | Blocklists are insufficient for high-security environments. |
| Standard enterprise | Don't use — use `tools.core` instead | Allowlists provide better coverage. |
| Individual developers | Block dangerous patterns | `ShellTool(rm -rf /)`, `ShellTool(sudo rm)`, etc. |

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
| CI/CD pipelines | `"service-account"` | Service accounts for automated workflows. |
| Individual developers | Omit (user choice) | No enforcement needed. |

---

## `security.folderTrust.enabled`

**What it does:** Requires users to explicitly trust a project folder before Gemini CLI loads project-level settings and context files.

**Why it matters:** A malicious repository could include `.gemini/settings.json` or `GEMINI.md` with harmful instructions or tool configurations. Folder trust prevents automatic loading.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All environments | `true` | Always require explicit trust. Prevents supply-chain attacks via repository configs. |

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

## `general.disableAutoUpdate`

**What it does:** Prevents Gemini CLI from automatically downloading and installing updates.

**Why it matters:** Auto-updates ensure security patches but bypass IT testing and approval processes.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | IT must test and approve each version. |
| Standard enterprise | `false` | Auto-updates ensure timely security patches. |
| Individual developers | `false` | Stay current with latest features. |

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

## Summary: Recommended Profiles

### Maximum Lockdown (Regulated)

```json
{
  "tools": { "sandbox": "docker", "core": ["ReadFileTool", "GlobTool", "GrepTool", "ListDirectoryTool"] },
  "mcp": { "allowed": [] },
  "security": { "auth": { "enforcedType": "oauth-personal" } },
  "telemetry": { "enabled": true, "logPrompts": false },
  "privacy": { "usageStatisticsEnabled": false },
  "general": { "disableAutoUpdate": true }
}
```

### Standard Enterprise

```json
{
  "tools": { "sandbox": "docker", "core": ["ReadFileTool", "WriteFileTool", "EditFileTool", "GlobTool", "GrepTool", "ListDirectoryTool", "ShellTool(git)", "ShellTool(npm test)"] },
  "mcp": { "allowed": ["corp-tools"] },
  "security": { "auth": { "enforcedType": "oauth-personal" } },
  "telemetry": { "enabled": true, "logPrompts": false },
  "privacy": { "usageStatisticsEnabled": false }
}
```

### Developer Teams

```json
{
  "tools": { "sandbox": "docker", "exclude": ["ShellTool(rm -rf /)"] },
  "mcp": {},
  "security": { "folderTrust": { "enabled": true } },
  "telemetry": { "enabled": false, "logPrompts": false },
  "privacy": { "usageStatisticsEnabled": false }
}
```

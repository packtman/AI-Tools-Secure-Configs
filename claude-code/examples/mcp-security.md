# Claude Code — MCP Server Security Guide

## Risk Model

Each MCP server entry grants Claude Code the ability to execute arbitrary operations via the specified tool or endpoint. This represents a significant attack surface.

**Threats:**
- **Data exfiltration** — A malicious MCP server can read files and send data to external endpoints.
- **Privilege escalation** — A poorly-scoped MCP server can access resources beyond its intended scope.
- **Supply chain attacks** — An MCP server package from npm/PyPI may contain malicious code.
- **Prompt injection** — MCP server responses can inject instructions that manipulate Claude's behavior.
- **Credential theft** — API keys in `env` blocks are passed to the server process in plaintext.

---

## Managed MCP Controls

### Allowlist / Denylist

In `managed-settings.json`:

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "internal-api" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" },
    { "serverName": "shell" }
  ]
}
```

- `allowedMcpServers` — When set, only these servers can be configured (undefined = no restrictions, empty array = block all).
- `deniedMcpServers` — Explicitly blocked servers. Denylist takes precedence over allowlist.
- `allowManagedMcpServersOnly` — When `true`, only the managed allowlist is respected.

### Managed MCP file

Deploy `managed-mcp.json` alongside `managed-settings.json` at the system path:

| OS | Path |
|----|------|
| macOS | `/Library/Application Support/ClaudeCode/managed-mcp.json` |
| Linux / WSL | `/etc/claude-code/managed-mcp.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-mcp.json` |

This file uses the same format as `.mcp.json` and defines organization-wide MCP servers.

---

## MCP Permission Rules

Control MCP tool usage via permission rules:

```json
{
  "permissions": {
    "allow": ["mcp__github__search_repositories"],
    "ask": ["mcp__github__create_issue"],
    "deny": [
      "mcp__filesystem__*",
      "mcp__shell__*"
    ]
  }
}
```

Pattern syntax:
- `mcp__servername` — Matches the server name exactly (no tools).
- `mcp__servername__*` — Matches all tools from that server.
- `mcp__servername__toolname` — Matches a specific tool.
- `mcp__*` — Matches all MCP tools from any server.

---

## Security Best Practices

### Before deploying an MCP server

1. **Audit the source code** — Review the server's repository for security issues.
2. **Check permissions** — Understand what filesystem, network, and API access the server needs.
3. **Pin versions** — Use specific versions, not `latest`, for reproducibility and security.
4. **Sandbox** — Enable Claude Code's sandbox to restrict what MCP servers can do.

### Credential management

1. **Never hard-code secrets** in `.mcp.json` — Use `${ENV_VAR}` syntax.
2. **Use `headersHelper`** for dynamic authentication instead of static tokens.
3. **Rotate tokens** used by MCP servers on the same schedule as other API keys.
4. **Restrict OAuth scopes** with `oauth.scopes` to the minimum required.

### Network security

1. **Prefer HTTP transport** over stdio for remote servers (supports TLS).
2. **Use VPC endpoints** for internal MCP servers.
3. **Restrict with sandbox network allowlist** — Only allow MCP servers to reach necessary domains.

### Monitoring

1. **Use PostToolUse hooks** to log all MCP tool invocations.
2. **Use PreToolUse hooks** to validate MCP tool inputs before execution.
3. **Review `/mcp` status** regularly to verify connected servers.

---

## Project-Scoped MCP Security

Project-scoped MCP servers (`.mcp.json` committed to a repository) require trust approval before use. To manage this:

```json
{
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": ["github", "memory"],
  "disabledMcpjsonServers": ["filesystem", "shell"]
}
```

- `enableAllProjectMcpServers: false` — Require explicit approval for each project MCP server.
- `enabledMcpjsonServers` — Pre-approve specific servers by name.
- `disabledMcpjsonServers` — Block specific servers by name.

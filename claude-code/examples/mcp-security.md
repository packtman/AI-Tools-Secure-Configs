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

### Claude.ai account connectors

Claude Code can fetch MCP connectors attached to the signed-in claude.ai account (Drive, Slack, custom connectors). That path is separate from `allowedMcpServers` and from `managed-mcp.json`.

Pin `disableClaudeAiConnectors: true` in managed settings on Moderate and Strict. The vendor default is `false`, so those connectors load unless you pin this key or deploy `managed-mcp.json` (which takes exclusive control unless you also set `allowAllClaudeAiMcps: true`).

- Scope: any settings file. A `true` in managed settings cannot be turned off by a project `false`.
- Requires Claude Code v2.1.182 or later.
- Session env `ENABLE_CLAUDEAI_MCP_SERVERS=false` is a one-session kill, not a substitute.
- Leave `allowAllClaudeAiMcps` unset. The default `false` keeps `managed-mcp.json` exclusive. Set `true` only if IT has allowlisted specific claude.ai connectors.
- This pin covers Claude Code only. Claude Desktop MDM connector policy is a separate control.

```json
{
  "disableClaudeAiConnectors": true
}
```

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

Claude Code can make a **per-tool decision** independently of whether the MCP server is permitted to connect:

| Decision | Example action | Result |
|----------|----------------|--------|
| **Allow** | GitHub `search_repositories`, `get_file_contents` | Executes without an approval prompt |
| **Ask** | GitHub `create_issue`, `create_pull_request` | Prompts the user to approve the call |
| **Deny** | GitHub `delete_file`, `push_files`; all filesystem/shell MCP tools | Blocks the call |

A copyable **Claude Code** example is in [`mcp-tool-permissions.json`](./mcp-tool-permissions.json). Merge its `permissions` object into the appropriate `settings.json` or enterprise `managed-settings.json` (do **not** replace the entire managed settings file):

```json
{
  "permissions": {
    "allow": [
      "mcp__github__search_repositories",
      "mcp__github__get_file_contents"
    ],
    "ask": [
      "mcp__github__create_issue",
      "mcp__github__create_pull_request"
    ],
    "deny": [
      "mcp__github__delete_file",
      "mcp__github__push_files",
      "mcp__filesystem__*",
      "mcp__shell__*"
    ]
  }
}
```

### Tiered managed configuration examples

These permissions are **included directly in each Claude Code managed-settings tier**. Choose a tier before deployment; do not blindly paste the standalone snippet into every tier.

| Tier | Allow without prompt | Ask for approval | Deny |
|------|----------------------|------------------|------|
| [Strict](./managed-settings-strict.json) | No MCP tools | No MCP tools | `mcp__*` (all MCP tools) |
| [Moderate](./managed-settings-moderate.json) | `github.search_repositories` | `github.get_file_contents`, `github.create_issue`, `github.create_pull_request` | `github.delete_file`, `github.push_files`; all `filesystem` and `shell` MCP tools |
| [Baseline](./managed-settings-baseline.json) | `github.search_repositories`, `github.get_file_contents` | `github.create_issue`, `github.create_pull_request` | Same destructive GitHub and filesystem/shell MCP calls |

- Strict intentionally preserves the previous **deny-all MCP** posture; adding more specific allow or ask rules would not work because deny has precedence.
- Moderate and Baseline set `permissions.defaultMode: "default"` so unmatched calls follow interactive default-mode permission handling. These are **illustrative per-tool rules, not a comprehensive deny-by-default allowlist**. Review unlisted MCP tools and their effective permissions before rollout.
- The example MCP server name is `github`; replace it with your configured server's actual name and tool IDs. The tier files do not install or approve an MCP server by themselves.
- If you need a stricter posture with approved exceptions, build a fully scoped server/tool exposure policy or enforce through an MCP gateway, rather than using a blanket `mcp__*` deny alongside narrower allows.

### Important precedence and deployment details

- **Deny > Ask > Allow**, regardless of specificity. A broad `ask: ["mcp__*"]` takes precedence over a narrower `allow: ["mcp__github__search_repositories"]`. The tiered configs below intentionally avoid the broad `ask` rule except for the Strict deny-everything policy. Check other managed rules and organization-level policies for conflicts.
- The inverse also holds: `deny: ["mcp__github__*"]` cannot be paired with a narrower `allow` exception. This sample is **not a deny-by-default allowlist**: unlisted tools follow the client's remaining permission rules and mode. For stronger enforcement, combine explicit denied tools, server governance, scoped credentials, and an MCP gateway or pre-tool policy enforcement.
- `allowedMcpServers` and `deniedMcpServers` control **server availability**, not per-call approval. A permitted server can expose multiple tools with very different risks.
- Use the **actual** tool names exposed by the installed server; examples assume a GitHub MCP server named `github`. Names and offered operations can differ by server version and toolset. `mcp__servername__*` matches all tools from that server, while `mcp__servername__toolname` matches an individual tool. No MCP server is installed by this JSON snippet.
- The tool's ability to search/read data does not make it inherently low-risk. Limit identities, repositories, and scopes at the service; use server-side controls for parameter-sensitive policies.
- Tool-level decisions are enforced by **Claude Code**, not by the MCP specification, and are not portable JSON to Cursor, Gemini CLI, or Codex.

### Verify before rollout

1. Configure an approved GitHub MCP server and confirm its exposed tool names with `/mcp`.
2. Load the proposed settings, then inspect **`/permissions`** to identify the effective rule and source.
3. Test an allowed read/search, a write that prompts, and a denied destructive call **in a disposable test repository**.
4. Confirm a managed `ask` catch-all is not unintentionally shadowing `allow`, and verify the behavior of **unlisted** MCP calls.
5. Log calls, scope MCP credentials, and test that denied actions cannot be performed through a different allowed tool.

Vendor reference: [Claude Code permission rules](https://code.claude.com/docs/en/permissions).

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

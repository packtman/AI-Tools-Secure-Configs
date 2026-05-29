# Claude Desktop — MCP OAuth and Server Restrictions

Reference for enterprise admins aligning Claude Desktop with Anthropic MCP documentation (2026).

## Managed deployment controls

Deploy via MDM (macOS managed preferences or Windows registry), not in `claude_desktop_config.json`:

| Control | Strict | Moderate | Baseline |
|---------|--------|----------|----------|
| `isLocalDevMcpEnabled` | `false` | `false` | `true` |
| `isDesktopExtensionEnabled` | `false` | `false` | `true` |
| `isClaudeCodeForDesktopEnabled` | `false` | `false` | `true` |

## MCP server configuration

- Use an empty `mcpServers` object in Strict tier configs.
- Moderate tier: allowlist only IT-vetted servers in `config-moderate.json`.
- Restrict OAuth scope discovery: do not import servers from Claude.ai without security review.
- Block dynamic header injection for custom auth unless the server is on the corporate allowlist.

## Environment variables (operator reference)

These are set by the Claude Desktop installer or IT packaging, not committed to repo configs:

| Variable | Purpose | Enterprise guidance |
|----------|---------|---------------------|
| `CLAUDE_CODE_MCP_SERVER_NAME` | Names the active MCP server for diagnostics | Set only in support bundles, not user-editable profiles |
| `CLAUDE_CODE_MCP_SERVER_URL` | Remote MCP endpoint for HTTP/SSE servers | Use internal gateway URLs; block public internet endpoints in Strict |

## Workflow preservation

| Blocked capability | Risk | Safe alternative |
|--------------------|------|------------------|
| Local dev MCP | Unvetted stdio servers with full user permissions | Use corporate HTTP MCP gateway with OAuth and audit logging |
| Import from Claude.ai | Brings consumer-configured servers into enterprise desktop | IT publishes approved `mcpServers` via MDM-managed config |

## Validation

1. Confirm `mcpServers` is empty or allowlisted on a pilot Mac/Windows endpoint.
2. Attempt to add a new MCP server: Strict should block or require admin unlock.
3. Verify OAuth flows use corporate IdP where Anthropic supports SSO for Desktop.

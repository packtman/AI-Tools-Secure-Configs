# Cline — Secure Admin Configuration

This directory contains security-hardened configurations for **Cline** (the open-source AI coding agent for VS Code), targeting administrators who need to enforce tool restrictions, auto-approval controls, MCP governance, and compliance policies across their organization.

## What Is Covered

| File | Purpose |
|------|---------|
| `settings.json` | VS Code `settings.json` template for Cline extension settings |
| `examples/settings-strict.json` | **Strict** — Maximum restrictions; all actions require approval |
| `examples/settings-moderate.json` | **Moderate** — Balanced for development teams; read-only auto-approved |
| `examples/settings-baseline.json` | **Baseline** — Essential restrictions only; startups and individual devs |
| `examples/mcp-config-secure.json` | Secure MCP server configuration with filesystem scoping |
| `examples/settings-rationale.md` | Comprehensive security reasoning for every setting |
| `examples/mdm-policies.md` | MDM/GPO deployment guide for enterprise rollout |

## What Is Cline

Cline is a VS Code extension that gives the editor a full AI agent capable of reading, writing, and executing code. It communicates with LLM providers (Anthropic, OpenAI, Google, etc.) and can:

- Read and write files anywhere in the workspace (or beyond, if unrestricted)
- Execute terminal commands
- Launch browser automation (via `@browserbase` or built-in browser tool)
- Connect to MCP servers to invoke external tools and APIs
- Auto-approve any of these actions if misconfigured

This makes Cline both powerful and high-risk without proper configuration.

## Configuration Files

### VS Code `settings.json`

Cline is configured via standard VS Code settings under the `cline.*` prefix. Settings can be deployed at three scopes:

| Scope | Location | Override order |
|-------|----------|----------------|
| User (global) | `~/.vscode/settings.json` (or `Code/User/settings.json`) | Lowest precedence |
| Workspace | `.vscode/settings.json` in project root | Overrides user settings |
| MDM-managed | Via Intune/Jamf/Kandji device management | Highest precedence (cannot be overridden) |

### MCP Configuration

Cline stores its MCP server configuration at:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| Linux | `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| Windows | `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json` |

## Critical Security Settings

The four `alwaysAllow*` settings are the most important security controls in Cline:

| Setting | Risk when `true` | Recommendation |
|---------|-----------------|----------------|
| `cline.alwaysAllowReadOnly` | AI reads any file without approval | `false` for regulated; `true` for developer |
| `cline.alwaysAllowWrite` | AI writes/overwrites files silently | `false` always |
| `cline.alwaysAllowExecute` | AI runs any terminal command silently | `false` always |
| `cline.alwaysAllowBrowser` | AI browses any URL without approval | `false` always |
| `cline.alwaysAllowMcp` | AI calls any MCP tool without approval | `false` always |

**Never set `alwaysAllowWrite`, `alwaysAllowExecute`, or `alwaysAllowMcp` to `true` in a production or shared environment.**

## Deployment Checklist

1. Deploy `settings.json` via MDM or VS Code policy to all developer machines.
2. Set `cline.allowedCommands` to an explicit allowlist — never leave empty with `alwaysAllowExecute: true`.
3. Scope all MCP filesystem servers to specific workspace paths only.
4. Ensure API keys are sourced from environment variables or secrets managers — never from `cline.apiKey` in a shared settings file.
5. Disable `cline.alwaysAllowWrite`, `cline.alwaysAllowExecute`, and `cline.alwaysAllowMcp` via MDM so users cannot override.
6. Review Cline task history files for sensitive data regularly (stored in the extension's globalStorage directory).
7. Configure network proxy settings if routing AI traffic through a corporate gateway.

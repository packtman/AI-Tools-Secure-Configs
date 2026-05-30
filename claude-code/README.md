# Claude Code — Secure Admin Configuration

This directory contains comprehensive, security-hardened configurations for **Claude Code** (Anthropic's AI coding agent), targeting organization administrators who need to enforce safe tool usage, permission boundaries, sandbox isolation, MCP governance, hooks-based audit logging, and compliance policies.

## What Is Covered

### Core Configuration Files

| File | Purpose |
|------|---------|
| `managed-settings.json` | Enterprise managed settings — deploy via MDM, admin console, or filesystem |
| `settings.json` | Recommended project-level settings (commit to `.claude/settings.json`) |
| `CLAUDE.md` | Secure project instructions template (commit to repo root or `.claude/`) |

### Example Configurations

| File | Purpose |
|------|---------|
| `examples/managed-settings-strict.json` | **Strict** — Maximum-restriction lockdown (regulated environments) |
| `examples/managed-settings-moderate.json` | **Moderate** — Balanced enterprise policy (standard dev teams) |
| `examples/managed-settings-baseline.json` | **Baseline** — Essential security only (startups, individual devs) |
| `examples/managed-settings-drop-in.md` | Multi-file drop-in directory guide |
| `examples/hooks-security.json` | Security-focused hooks (audit, secret scanning, destructive command blocking) |
| `examples/hook-scripts/*.sh` | Ready-to-use hook shell scripts |
| `examples/sandbox-config.json` | OS-level sandbox (filesystem + network isolation) |
| `examples/managed-mcp.json` | Managed MCP server configuration |
| `examples/mcp-security.md` | MCP server security guide (risk model, allowlists, best practices) |
| `examples/server-managed-settings-guide.md` | Claude.ai Admin Console deployment guide |
| `examples/environment-variables-reference.md` | Security-relevant env vars reference |
| `examples/permissions-cheatsheet.md` | Complete permission rules quick reference |

---

## Settings Hierarchy (highest → lowest priority)

1. **Managed** — `managed-settings.json`, MDM policies, or server-managed (cannot be overridden)
2. **Command line** — Temporary session overrides (`--model`, `--allowedTools`)
3. **Local** — `.claude/settings.local.json` (git-ignored, personal)
4. **Project** — `.claude/settings.json` (committed, team-shared)
5. **User** — `~/.claude/settings.json` (personal defaults)

If a tool is denied at any level, no other level can allow it.

---

## Managed Settings Deployment

### File-based (MDM or manual)

| OS | File path |
|----|-----------|
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Linux / WSL | `/etc/claude-code/managed-settings.json` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` |

Supports a `managed-settings.d/` drop-in directory alongside the base file for modular policy deployment.

### MDM / OS-level policies

| Platform | Mechanism |
|----------|-----------|
| macOS | Managed preferences domain `com.anthropic.claudecode` (deploy via Jamf, Kandji, etc.) |
| Windows (machine) | Registry `HKLM\SOFTWARE\Policies\ClaudeCode` → `Settings` value (REG_SZ containing JSON) |
| Windows (user) | Registry `HKCU\SOFTWARE\Policies\ClaudeCode` (lowest policy priority) |

### Server-managed (Admin Console)

- Configure in **Claude.ai → Admin Settings → Claude Code → Managed settings**.
- Requires Claude for Teams or Enterprise, Claude Code ≥ 2.1.38.
- No MDM infrastructure needed.
- See `examples/server-managed-settings-guide.md` for details.

---

## Permission Rules

### Evaluation order

```
deny  →  ask  →  allow
```

The first matching rule wins. Deny rules always take precedence.

### Rule types

| Rule | Effect |
|------|--------|
| `deny` | Blocks the tool entirely |
| `ask` | Prompts user for approval each time |
| `allow` | Runs without confirmation |

### Key syntax

| Pattern | Matches |
|---------|---------|
| `Bash(curl * \| bash)` | Piped execution |
| `Bash(sudo *)` | Privilege escalation |
| `Read(./.env)` | Reading .env files |
| `Read(~/.ssh/**)` | Reading SSH keys |
| `Read(//etc/shadow)` | Absolute path to system files |
| `Write(~/.bashrc)` | Writing to shell config |
| `mcp__servername__*` | All tools from an MCP server |
| `Agent(Explore)` | Explore subagent |

See `examples/permissions-cheatsheet.md` for the complete reference.

---

## Sandbox (OS-Level Isolation)

Claude Code's sandbox provides OS-level filesystem and network isolation for Bash commands:

- **macOS:** Uses Seatbelt framework
- **Linux / WSL2:** Uses bubblewrap

### Key sandbox settings

| Setting | Description |
|---------|-------------|
| `sandbox.enabled` | Enable/disable sandbox |
| `sandbox.autoAllowBashIfSandboxed` | Auto-approve sandboxed Bash (no per-command prompts) |
| `sandbox.allowUnsandboxedCommands` | Allow escape hatch to run outside sandbox |
| `sandbox.failIfUnavailable` | Fail hard if sandbox cannot start |
| `sandbox.filesystem.allowWrite` | Paths writable by sandboxed processes |
| `sandbox.filesystem.denyRead` | Paths blocked from reading |
| `sandbox.network.allowedDomains` | Domains accessible from sandbox |
| `sandbox.network.deniedDomains` | Domains always blocked |
| `sandbox.network.allowManagedDomainsOnly` | Only managed-level domain allowlist applies |

See `examples/sandbox-config.json` for a complete example.

---

## Hooks (Lifecycle Automation)

Hooks execute at specific points in Claude Code's lifecycle. Security-relevant hooks:

| Event | Use case |
|-------|----------|
| `PreToolUse` | Block dangerous commands, validate MCP inputs |
| `PostToolUse` | Scan for leaked secrets, audit log commands |
| `Stop` | Session-end audit summary |
| `ConfigChange` | Log configuration modifications |

Hook types: `command` (shell), `http` (webhook), `mcp_tool`, `prompt` (LLM), `agent`.

See `examples/hooks-security.json` and `examples/hook-scripts/` for ready-to-use examples.

### Managed hooks control

| Setting | Effect |
|---------|--------|
| `allowManagedHooksOnly` | Block all user/project/plugin hooks |
| `allowedHttpHookUrls` | Allowlist for HTTP hook target URLs |
| `httpHookAllowedEnvVars` | Allowlist for env vars in HTTP hook headers |
| `disableAllHooks` | Kill switch for all hooks |

---

## MCP Server Governance

| Setting | Effect |
|---------|--------|
| `allowedMcpServers` | Allowlist of permitted MCP servers |
| `deniedMcpServers` | Blocklist of prohibited MCP servers |
| `allowManagedMcpServersOnly` | Only managed allowlist applies |
| `enableAllProjectMcpServers` | Auto-approve project `.mcp.json` servers |
| `enabledMcpjsonServers` | Pre-approve specific project servers |
| `disabledMcpjsonServers` | Block specific project servers |

Deploy `managed-mcp.json` alongside `managed-settings.json` for organization-wide MCP servers.

See `examples/mcp-security.md` for the complete security guide.

---

## Managed-Only Settings (Cannot Be Overridden)

| Setting | Effect |
|---------|--------|
| `allowManagedPermissionRulesOnly` | Block user/project permission rules |
| `allowManagedHooksOnly` | Block user/project hooks |
| `allowManagedMcpServersOnly` | Only managed MCP allowlist |
| `forceRemoteSettingsRefresh` | Fail-closed startup |
| `channelsEnabled` | Enable/disable channels |
| `blockedMarketplaces` | Block plugin marketplace sources |
| `strictKnownMarketplaces` | Restrict marketplace sources |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Only managed read paths |
| `sandbox.network.allowManagedDomainsOnly` | Only managed domains |

---

## Deployment Checklist

### Phase 1: Identity & Access
- [ ] Set `forceLoginMethod: "claudeai"` to restrict to org accounts.
- [ ] Set `forceLoginOrgUUID` to lock to your organization.
- [ ] Set `minimumVersion` to enforce a floor version.
- [ ] Set `autoUpdatesChannel: "stable"` for controlled updates.

### Phase 2: Permissions
- [ ] Deploy `managed-settings.json` with deny rules for dangerous patterns.
- [ ] Set `disableBypassPermissionsMode: "disable"`.
- [ ] Set `disableAutoMode: "disable"` (if not using auto mode).
- [ ] Consider `allowManagedPermissionRulesOnly: true` for maximum control.

### Phase 3: Sandbox
- [ ] Enable sandbox with `sandbox.enabled: true`.
- [ ] Configure `filesystem.denyRead` for sensitive paths.
- [ ] Configure `filesystem.denyWrite` to restrict writes.
- [ ] Configure `network.allowedDomains` for legitimate package registries.
- [ ] Set `allowUnsandboxedCommands: false`.

### Phase 4: MCP Governance
- [ ] Define `allowedMcpServers` and `deniedMcpServers`.
- [ ] Deploy `managed-mcp.json` for org-wide MCP servers.
- [ ] Consider `allowManagedMcpServersOnly: true` for strict environments.

### Phase 5: Hooks & Monitoring
- [ ] Deploy audit logging hooks (PostToolUse).
- [ ] Deploy secret-scanning hooks (PostToolUse for Write|Edit).
- [ ] Deploy destructive command blocking hooks (PreToolUse for Bash).
- [ ] Set `allowedHttpHookUrls` to restrict hook destinations.
- [ ] Consider `allowManagedHooksOnly: true` for strict environments.

### Phase 6: Project-Level
- [ ] Commit `.claude/settings.json` to all repositories.
- [ ] Commit `CLAUDE.md` or `.claude/CLAUDE.md` to all repositories.
- [ ] Review and update deny rules quarterly.

# Claude Desktop — Secure Admin Configuration

This directory contains comprehensive, security-hardened configurations for **Claude Desktop** (Anthropic's desktop application), targeting administrators who need to control MCP server access, tool permissions, extension policies, and enterprise-wide deployment.

## What Is Covered

### Core Configuration Files

| File | Purpose |
|------|---------|
| `claude_desktop_config.json` | Secure MCP configuration template |
| `enterprise-policy.md` | Enterprise policy deployment guide |

### Example Configurations

| File | Purpose |
|------|---------|
| `examples/config-strict.json` | **Strict** — Zero MCP, all features disabled (regulated environments) |
| `examples/config-moderate.json` | **Moderate** — Scoped MCP servers, extensions disabled (enterprise teams) |
| `examples/config-baseline.json` | **Baseline** — MCP enabled, essential restrictions (startups, individual devs) |
| `examples/config-minimal.json` | Zero MCP servers — maximum lockdown (legacy, see strict) |
| `examples/config-restricted-mcp.json` | Tightly scoped MCP servers (legacy, see moderate) |
| `examples/mdm-macos-profile.md` | macOS MDM deployment guide (Jamf, Kandji) |
| `examples/mdm-windows-gpo.md` | Windows GPO / Intune deployment guide |
| `examples/policy-rationale.md` | Reasoning behind every enterprise policy key |

## Configuration File Locations

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

Changes require a full restart — no hot-reload.

---

## Enterprise Policy Keys (Complete Reference)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `isLocalDevMcpEnabled` | Boolean | `true` | Allow users to configure local MCP servers |
| `isDesktopExtensionEnabled` | Boolean | `true` | Allow desktop extensions |
| `isDesktopExtensionDirectoryEnabled` | Boolean | `true` | Allow access to extension directory |
| `isClaudeCodeForDesktopEnabled` | Boolean | `true` | Allow Claude Code access in desktop |
| `secureVmFeaturesEnabled` | Boolean | `true` | Allow Cowork (computer use sandbox) access |
| `disableAutoUpdates` | Boolean | `false` | Disable automatic updates |
| `autoUpdaterEnforcementHours` | Integer | `72` | Hours before force-restart for pending update (1-72) |

### Policy Deployment

| Platform | Mechanism |
|----------|-----------|
| macOS | Managed preferences domain `com.anthropic.claudefordesktop` via MDM |
| Windows (machine) | Registry `HKLM\SOFTWARE\Policies\Claude` |
| Windows (user) | Registry `HKCU\SOFTWARE\Policies\Claude` (lower priority) |

Machine-level policies override in-app settings. Enterprise policy controls override user-level allowlist settings.

---

## MCP Security Model

Each MCP server entry in `claude_desktop_config.json` grants Claude the ability to execute arbitrary operations. This is functionally equivalent to giving the AI a shell.

**Threats:**
- A misconfigured server can read/write any file the user can access.
- Malicious packages can exfiltrate data.
- API keys in `env` blocks are passed in cleartext to the server process.
- Untrusted MCP server responses can inject instructions (prompt injection).

**Mitigations:**
- Restrict MCP servers to the minimum needed.
- Scope filesystem servers to single directories.
- Use environment variables from a secrets manager, not inline values.
- Review MCP server source code before deployment.
- Deploy enterprise policies to block local MCP if not needed.

---

## Deployment Checklist

### Phase 1: Enterprise Policies
- [ ] Deploy MDM profile to disable unnecessary features.
- [ ] Set `isLocalDevMcpEnabled: false` if MCP is not needed.
- [ ] Set `isDesktopExtensionEnabled: false` if extensions are not needed.
- [ ] Configure update enforcement with `autoUpdaterEnforcementHours`.

### Phase 2: MCP Governance
- [ ] Audit all MCP servers — review source and permissions.
- [ ] Restrict MCP servers to approved packages only.
- [ ] Scope filesystem servers to single project directories.
- [ ] Never store API keys directly in config — use env var references.

### Phase 3: Monitoring
- [ ] Monitor Claude Desktop tool permission grants.
- [ ] Review and revoke overly broad tool permissions.
- [ ] Audit installed extensions periodically.

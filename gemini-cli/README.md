# Google Gemini CLI — Secure Admin Configuration

This directory contains comprehensive, security-hardened configurations for **Google Gemini CLI** (Google's AI coding agent for the desktop), targeting administrators who need to enforce tool restrictions, sandbox policies, MCP server governance, and enterprise-wide deployment via system settings files.

## What Is Covered

### Core Configuration Files

| File | Purpose |
|------|---------|
| `settings.json` | Secure user-level settings template (`~/.gemini/settings.json`) |
| `enterprise-policy.md` | Enterprise deployment guide (system settings, auth enforcement) |

### Example Configurations

| File | Purpose |
|------|---------|
| `examples/settings-strict.json` | **Strict** — Maximum lockdown (regulated environments) |
| `examples/settings-moderate.json` | **Moderate** — Balanced security for enterprise teams |
| `examples/settings-baseline.json` | **Baseline** — Essential security (startups, individual devs) |
| `examples/system-settings-enterprise.json` | System-level override file for enterprise deployment |
| `examples/system-defaults-enterprise.json` | System-level defaults file |
| `examples/deployment-guide.md` | Multi-platform deployment guide |
| `examples/policy-rationale.md` | Reasoning behind every policy setting |

## Configuration File Locations

| OS | User Settings | System Defaults | System Overrides |
|----|---------------|-----------------|------------------|
| macOS | `~/.gemini/settings.json` | `/Library/Application Support/GeminiCli/system-defaults.json` | `/Library/Application Support/GeminiCli/settings.json` |
| Windows | `~/.gemini/settings.json` | `C:\ProgramData\gemini-cli\system-defaults.json` | `C:\ProgramData\gemini-cli\settings.json` |
| Linux | `~/.gemini/settings.json` | `/etc/gemini-cli/system-defaults.json` | `/etc/gemini-cli/settings.json` |

Project-level overrides: `.gemini/settings.json` in the project root.

---

## Configuration Precedence

Settings are applied in this order (highest number overrides lower):

1. **System defaults** (`system-defaults.json`) — base layer, lowest priority
2. **User settings** (`~/.gemini/settings.json`) — per-user preferences
3. **Project settings** (`.gemini/settings.json`) — project-specific
4. **System overrides** (`settings.json` in system path) — **highest priority, admin-enforced**

For single-value settings, the system overrides file has the **final say**. For arrays and objects (like `mcpServers`, `includeDirectories`), values are merged across all levels.

---

## Key Security Concepts

### Tool Access Control

Gemini CLI provides two mechanisms for controlling which tools the AI can use:

| Setting | Type | Description |
|---------|------|-------------|
| `tools.core` | Allowlist | Only these tools are available (most secure) |
| `tools.exclude` | Blocklist | These tools are blocked (less secure) |
| `tools.allowed` | Auto-approve list | These tools bypass confirmation dialog |
| `tools.sandbox` | Isolation | Execute tools in Docker/Podman sandbox |

**Security recommendation:** Use `tools.core` (allowlist) over `tools.exclude` (blocklist).

### MCP Server Governance

| Setting | Description |
|---------|-------------|
| `mcp.allowed` | Allowlist of permitted MCP server names |
| `mcp.excluded` | Blocklist of denied MCP server names |
| `mcpServers.<name>.includeTools` | Allow only specific tools from a server |
| `mcpServers.<name>.excludeTools` | Block specific tools from a server |
| `mcpServers.<name>.trust` | Auto-approve all calls (use with caution) |

If `mcp.allowed` is set in the system overrides file, users cannot add their own MCP servers.

### Sandbox Modes

| Mode | Description |
|------|-------------|
| `true` / `"docker"` | Docker-based sandbox (recommended) |
| `"podman"` | Podman-based sandbox |
| Custom command | Custom sandbox execution |
| `false` | No sandbox (**not recommended**) |

macOS also supports Seatbelt (`sandbox-exec`) profiles via `SEATBELT_PROFILE`:

| Profile | Description |
|---------|-------------|
| `permissive-open` | Restricts writes to project folder (default) |
| `strict` | Declines operations by default |
| Custom | User-defined `.sb` profile in `.gemini/` |

### Authentication Enforcement

| Setting | Description |
|---------|-------------|
| `security.auth.enforcedType` | Required auth method for all users |
| `security.auth.selectedType` | Currently selected auth type |
| `security.auth.useExternal` | Whether to use external auth flow |
| `security.folderTrust.enabled` | Whether folder trust is enabled |

### Telemetry Control

| Setting | Description |
|---------|-------------|
| `telemetry.enabled` | Enable/disable telemetry collection |
| `telemetry.target` | Destination: `local` or `gcp` |
| `telemetry.otlpEndpoint` | OTLP collector endpoint |
| `telemetry.logPrompts` | Log user prompt content (**set to false**) |

---

## Security Differences: Gemini CLI vs. Gemini API

The existing `google-gemini/` directory covers Gemini API safety settings and GCP-level controls. This directory focuses on the **local desktop tool**:

- Shell command execution and file modification
- MCP server integrations
- Sandbox/isolation policies
- Tool access restrictions
- Local authentication and credential management
- Enterprise system-level overrides

---

## Deployment Checklist

### Phase 1: System Overrides
- [ ] Deploy system `settings.json` to enforce tool restrictions and MCP allowlists
- [ ] Set `tools.core` to allowlist only approved tools
- [ ] Set `tools.sandbox = "docker"` to enforce sandboxed execution
- [ ] Define `mcp.allowed` to restrict MCP servers to approved list
- [ ] Set `security.auth.enforcedType` to require corporate authentication

### Phase 2: Privacy & Telemetry
- [ ] Set `telemetry.logPrompts = false` to avoid capturing sensitive prompts
- [ ] Set `privacy.usageStatisticsEnabled = false` unless explicitly approved
- [ ] Configure telemetry to point at your OTLP collector if audit logging is needed
- [ ] Disable auto-updates if IT needs to test versions: `general.disableAutoUpdate = true`

### Phase 3: Project-Level Controls
- [ ] Deploy `.gemini/settings.json` to repositories with project-specific restrictions
- [ ] Configure `.geminiignore` files to prevent the AI from reading sensitive paths
- [ ] Set context file (`GEMINI.md`) guidelines for coding standards
- [ ] Review and approve custom sandbox profiles in `.gemini/` directories

### Phase 4: Monitoring
- [ ] Monitor telemetry data for anomalous tool usage patterns
- [ ] Audit MCP server configurations across user settings
- [ ] Review `tools.allowed` lists to prevent over-permissive auto-approvals
- [ ] Validate sandbox enforcement is not bypassed

# OpenAI Codex Desktop App — Secure Admin Configuration

This directory contains comprehensive, security-hardened configurations for the **OpenAI Codex Desktop App** (OpenAI's desktop application for AI-assisted coding), targeting administrators who need to enforce sandbox restrictions, approval policies, MCP server governance, and enterprise-wide deployment via managed configuration.

## What Is Covered

### Core Configuration Files

| File | Purpose |
|------|---------|
| `config.toml` | Secure desktop app configuration template |
| `enterprise-policy.md` | Enterprise policy deployment guide (MDM, system files) |

### Example Configurations

| File | Purpose |
|------|---------|
| `examples/config-strict.toml` | **Strict** — Maximum lockdown (regulated environments) |
| `examples/config-moderate.toml` | **Moderate** — Balanced security for enterprise teams |
| `examples/config-baseline.toml` | **Baseline** — Essential security (startups, individual devs) |
| `examples/requirements-strict.toml` | **Strict** admin-enforced requirements |
| `examples/requirements-moderate.toml` | **Moderate** admin-enforced requirements |
| `examples/requirements-baseline.toml` | **Baseline** admin-enforced requirements |
| `examples/managed-config.toml` | Managed defaults for enterprise deployment |
| `examples/mdm-macos-profile.md` | macOS MDM deployment guide |
| `examples/mdm-windows-deployment.md` | Windows deployment guide |
| `examples/policy-rationale.md` | Reasoning behind every policy setting |

## Configuration File Locations

| OS | User Config | System Config | Managed Config |
|----|-------------|---------------|----------------|
| macOS | `~/.codex/config.toml` | `/etc/codex/config.toml` | MDM `com.openai.codex` |
| Windows | `%USERPROFILE%\.codex\config.toml` | `%ProgramData%\OpenAI\Codex\config.toml` | `%USERPROFILE%\.codex\managed_config.toml` |
| Linux | `~/.codex/config.toml` | `/etc/codex/config.toml` | `/etc/codex/managed_config.toml` |

Project-level overrides: `.codex/config.toml` in the repository root (loaded only for trusted projects).

---

## Enterprise Configuration Architecture

The Codex Desktop App uses a layered configuration system with two enforcement mechanisms:

### 1. Requirements (`requirements.toml`) — Admin-Enforced Constraints

Requirements are constraints that **users cannot override**. They control security-sensitive settings:

- Allowed approval policies
- Allowed sandbox modes
- Web search mode restrictions
- MCP server allowlists
- Feature flag pins
- Command rules (prompt/forbidden)
- Filesystem deny-read rules

**Precedence (earlier wins per field):**
1. Cloud-managed requirements (ChatGPT Business/Enterprise)
2. macOS MDM via `com.openai.codex:requirements_toml_base64`
3. System `requirements.toml` (`/etc/codex/requirements.toml` on Unix, `%ProgramData%\OpenAI\Codex\requirements.toml` on Windows)

### 2. Managed Defaults (`managed_config.toml`) — Starting Values

Managed defaults set values when Codex launches. Users can change them during a session, but defaults reapply on restart.

**Precedence (top overrides bottom):**
1. Managed preferences (macOS MDM; highest)
2. `managed_config.toml` (system/managed file)
3. `config.toml` (user's base configuration)

---

## Key Security Concepts

### Sandbox Modes

| Mode | File Access | Network | Use Case |
|------|------------|---------|----------|
| `read-only` | Read-only workspace | Disabled | Code review, analysis |
| `workspace-write` | Read/write workspace | Disabled by default | Local development |
| `danger-full-access` | Full system access | Enabled | **NOT recommended** |

### Approval Policies

| Policy | Behavior |
|--------|----------|
| `untrusted` | Requires approval for every tool use including reads |
| `on-request` | Ask before every write/execute; reads are automatic |
| `never` | No approval required (**use with extreme caution**) |

### MCP Server Governance

MCP connects Codex to external tools. In `requirements.toml`, you can define an MCP server allowlist:

```toml
[mcp_servers.docs]
identity = { command = "codex-mcp" }

[mcp_servers.remote]
identity = { url = "https://example.com/mcp" }
```

If `mcp_servers` is present but empty, Codex disables all MCP servers.

### Feature Flags (Enterprise-Pinnable)

| Feature | Description |
|---------|-------------|
| `browser_use` | Browser Use and Browser Agent |
| `in_app_browser` | In-app browser pane |
| `browser_use_full_cdp_access` | Full Chrome DevTools Protocol (CDP) access and Browser Developer mode (Codex 0.150+) |
| `browser_use_external` | Computer Use in an external browser (Codex 0.150+) |
| `computer_use` | Computer Use (macOS only) |
| `codex_hooks` | Lifecycle hooks |
| `multi_agent` | Subagent collaboration |
| `memories` | Cross-session memory |

Requirements-only Computer Use lock (not a `[features]` key):

| Key | Description |
|-----|-------------|
| `computer_use.allow_locked_computer_use` | When `false`, Computer Use stops after a managed macOS device locks. Omit means unconstrained. Does not enable Computer Use. |

### Protected Paths

The `.codex/` directory and `.git/` are always protected, even in writable sandbox modes.

---

## Security Differences: Codex Desktop vs. Codex CLI

The Codex Desktop App, CLI, and IDE extension share the same configuration system (`config.toml`) and managed configuration layers. The desktop app additionally provides:

- **Browser Use** — AI can browse websites (allowlist/blocklist controlled)
- **Computer Use** — AI can interact with desktop apps (macOS only; not available in EEA/UK/Switzerland)
- **Codex Pets** — Visual overlays (low security risk)
- **Context-aware suggestions** — Follow-up recommendations

These features introduce additional attack surface that administrators should evaluate.

**Overlap with Codex CLI:** Desktop and CLI share `config.toml`, `requirements.toml`, and `managed_config.toml`. Deploy one `requirements.toml` for both surfaces. If you pin CDP, external Browser Use, or locked Computer Use only in Desktop config, a CLI host that later installs the app will not be locked until the same requirements file is on disk. Do not configure the same keys twice with different values.

---

## Deployment Checklist

### Phase 1: Requirements Enforcement
- [ ] Deploy `requirements.toml` via cloud-managed config, MDM, or system file
- [ ] Set `allowed_sandbox_modes` to exclude `danger-full-access`
- [ ] Set `allowed_approval_policies` to exclude `never` (if needed)
- [ ] Restrict MCP servers to an approved allowlist
- [ ] Pin `browser_use = false` and `computer_use = false` unless explicitly needed
- [ ] Pin `browser_use_full_cdp_access = false` and `browser_use_external = false` (Codex 0.150+)
- [ ] Pin `[computer_use] allow_locked_computer_use = false` even when Computer Use is already off
- [ ] Add `deny_read` rules for sensitive paths

### Phase 2: Managed Defaults
- [ ] Deploy `managed_config.toml` with conservative starting values
- [ ] Set `approval_policy = "on-request"` as the default
- [ ] Set `sandbox_mode = "workspace-write"` as the default
- [ ] Disable `network_access` unless required
- [ ] Configure telemetry to point at your OTLP collector

### Phase 3: Monitoring & Governance
- [ ] Enable audit logging via ChatGPT Compliance API
- [ ] Configure Analytics API for adoption tracking
- [ ] Set up RBAC via ChatGPT Enterprise workspace settings
- [ ] Periodically audit drift between local configs and managed policies
- [ ] Review MCP server access and tool permission grants

### Validation (Codex 0.150+)

Confirm the client is new enough, then confirm the pins are on disk (or in MDM):

```bash
codex --version
# Expect 0.150.0 or later. Do not pin 0.151 alpha.

# Linux / macOS system file
grep -n "allow_locked_computer_use\|browser_use_full_cdp_access\|browser_use_external" /etc/codex/requirements.toml

# macOS MDM
defaults read com.openai.codex requirements_toml_base64 | base64 -d | grep -E "allow_locked_computer_use|browser_use_full_cdp_access|browser_use_external"
```

On Windows, open `%ProgramData%\OpenAI\Codex\requirements.toml` and confirm the same three keys. If a user can still enable Browser Developer mode, the requirements file is missing, unsigned, or the client is older than 0.150.0.

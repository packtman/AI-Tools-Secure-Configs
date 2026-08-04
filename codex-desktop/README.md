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

Requirements file paths (admin-enforced):

| OS | Requirements path |
|----|-------------------|
| macOS / Linux | `/etc/codex/requirements.toml` (or MDM / cloud-managed requirements) |
| Windows | `%ProgramData%\OpenAI\Codex\requirements.toml` |

---

## Rollout Plan (`features.in_app_updates`)

### Phased rollout

1. **Pilot group** (security + platform eng): Deploy Moderate `requirements.toml` with `in_app_updates = false` to 10 to 25 endpoints that already receive Codex via MDM. Exit criteria: no in-app Update prompts for 5 business days; MDM package install path verified; no support tickets for missing critical fixes that MDM could not deliver.
2. **Expanded pilot** (one business unit): Same pin plus SIEM or inventory check that installed versions match the approved build. Exit criteria: version drift under 5%; exception process documented.
3. **Org-wide**: Push Moderate or Strict pin to all Desktop seats. Exit criteria: 95%+ of endpoints report pinned requirements; rollback package staged.

### Pre-rollout checklist

- [ ] MDM path verified (Jamf / Intune / Workspace ONE can install a pinned Codex build)
- [ ] Secrets manager in place for any ChatGPT/Codex admin credentials (not stored in this repo)
- [ ] SIEM or endpoint inventory ingest tested for Codex app version
- [ ] Rollback plan documented (previous `requirements.toml` and prior MDM package)

### What will break

- Moderate/Strict: the desktop Update button / in-app updater stops offering upgrades.
- Developer message before rollout: "Codex Desktop updates now come only from IT software distribution. If you need a newer build, request it through the service desk. Do not sideload installer links from chat."

### Rollback

1. Replace deployed `requirements.toml` (or MDM `requirements_toml_base64`) with the prior revision that omitted or set `in_app_updates = true`.
2. Redeploy the previous MDM package if you also rolled back the binary.
3. Communicate: "In-app updates are temporarily re-enabled while we fix distribution. Resume normal Update prompts after restart."

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
| `in_app_updates` | Desktop in-app binary updates (requirements-only; default on) |
| `computer_use` | Computer Use (macOS only) |
| `codex_hooks` | Lifecycle hooks |
| `multi_agent` | Subagent collaboration |
| `memories` | Cross-session memory |

### Tier delta: `features.in_app_updates`

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `features.in_app_updates` | `true` | `false` | `false` | Baseline allows vendor self-update; Moderate/Strict require MDM or approved software distribution |

Validation after deploy: restart Codex, then confirm the active requirements include `in_app_updates` (cloud managed-config UI, decoded MDM `requirements_toml_base64`, or `/etc/codex/requirements.toml`). The Update affordance in the desktop title bar should be unavailable when pinned `false`.

### Protected Paths

The `.codex/` directory and `.git/` are always protected, even in writable sandbox modes.

---

## Security Differences: Codex Desktop vs. Codex CLI

The Codex Desktop App, CLI, and IDE extension share the same configuration system (`config.toml`) and managed configuration layers. The desktop app additionally provides:

- **Browser Use** — AI can browse websites (allowlist/blocklist controlled)
- **Computer Use** — AI can interact with desktop apps (macOS only; not available in EEA/UK/Switzerland)
- **In-app updates**: Desktop self-update channel gated by `features.in_app_updates` in requirements
- **Codex Pets** — Visual overlays (low security risk)
- **Context-aware suggestions** — Follow-up recommendations

These features introduce additional attack surface that administrators should evaluate.

**Overlap with Codex CLI:** Desktop uses `features.in_app_updates` (requirements-only). CLI uses `check_for_update_on_startup` for TUI update checks. Pinning only one leaves the other client free to prompt for updates. When both are rolled out, set Desktop `in_app_updates = false` and CLI `check_for_update_on_startup = false` under Moderate/Strict.

---

## Deployment Checklist

### Phase 1: Requirements Enforcement
- [ ] Deploy `requirements.toml` via cloud-managed config, MDM, or system file
- [ ] Set `allowed_sandbox_modes` to exclude `danger-full-access`
- [ ] Set `allowed_approval_policies` to exclude `never` (if needed)
- [ ] Restrict MCP servers to an approved allowlist
- [ ] Pin `browser_use = false` and `computer_use = false` unless explicitly needed
- [ ] Pin `in_app_updates = false` for Moderate/Strict (keep MDM patch channel ready first)
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

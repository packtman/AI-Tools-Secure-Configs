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

### Approvals reviewer (`approvals_reviewer`)

Who reviews escalated approval prompts (sandbox escapes, blocked network, MCP prompts, ARC escalations). This does not change the sandbox boundary.

| Value | Behavior |
|-------|----------|
| `user` | Human reviews the prompt (default) |
| `auto_review` | A carefully prompted subagent gathers context and approves or denies |
| `guardian_subagent` | Legacy alias accepted for compatibility with `auto_review` |

Admin enforcement uses `allowed_approvals_reviewers` in `requirements.toml`. Managed Markdown for the automatic reviewer uses `guardian_policy_config` (takes precedence over local `[auto_review].policy`).

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
| `computer_use` | Computer Use (macOS only) |
| `codex_hooks` | Lifecycle hooks |
| `multi_agent` | Subagent collaboration |
| `memories` | Cross-session memory |

### Protected Paths

The `.codex/` directory and `.git/` are always protected, even in writable sandbox modes.

---

## Rollout Plan (`allowed_approvals_reviewers`)

MDM means Mobile Device Management (software that pushes managed settings to endpoints). SIEM means Security Information and Event Management (centralized log collection and alerting). MCP means Model Context Protocol (a way for AI tools to call external services).

### Phased rollout

1. **Pilot group** (security + platform eng): Deploy Moderate `requirements.toml` with `allowed_approvals_reviewers = ["user"]` to 10 to 25 endpoints. Exit criteria: no `auto_review` selections succeed for 5 business days; escalated prompts still reach a human; no support tickets that require auto_review to unblock.
2. **Expanded pilot** (one product org): Keep `["user"]` for Moderate/Strict groups; optionally leave a Baseline pilot cohort with `["user", "auto_review"]` plus `guardian_policy_config`. Exit criteria: ticket volume stable; SIEM or audit sampling shows human review on Strict/Moderate escalations; Baseline auto_review denials for secret/network paths behave as expected.
3. **Org-wide**: Assign requirements by ChatGPT workspace group or MDM scope. Exit criteria: inventory shows every managed Desktop install on the assigned tier; rollback package tested once.

### Pre-rollout checklist

- [ ] MDM or cloud managed-config path verified (Jamf / Intune / Workspace ONE or ChatGPT managed configs)
- [ ] Secrets manager in place for any developer credentials Codex must not read
- [ ] SIEM ingest tested for Codex or ChatGPT compliance/audit events you already collect
- [ ] Rollback `requirements.toml` revision staged and communication template ready

### What will break

| Tier | Impact | Developer message |
|------|--------|-------------------|
| Moderate / Strict | `approvals_reviewer = "auto_review"` is denied; escalations wait on a human | "Codex will ask you (not an automatic reviewer) before sandbox escapes, blocked network, MCP approvals, and similar escalations. Stay at your desk for prompts, or use pair review." |
| Baseline | Auto review is allowed but starts as `user`; managed guardian policy may deny more than a local policy | "You may enable automatic review for productivity. Org policy still denies secret reads, outbound network, and destructive commands. If a prompt is denied, ask a human teammate or open an exception request." |

### Rollback procedure

1. Replace deployed `requirements.toml` (or MDM `requirements_toml_base64`) with the prior revision that omitted `allowed_approvals_reviewers` (or included `auto_review`).
2. Push via the same MDM or cloud managed-config channel; ask users to restart Codex.
3. Communication template: "We temporarily restored optional automatic approval review while we investigate friction. Human review remains available. Reply to this thread with blocked workflows."

### Tier delta: `allowed_approvals_reviewers`

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `allowed_approvals_reviewers` | `["user", "auto_review"]` | `["user"]` | `["user"]` | Baseline allows optional automatic review; Moderate/Strict keep human-in-the-loop for escalations |
| `guardian_policy_config` | Conservative deny-secrets/network policy | (omit) | (omit) | Only needed when `auto_review` is allowed; managed policy overrides local `[auto_review].policy` |
| `approvals_reviewer` (managed/config default) | `user` | `user` | `user` | All tiers start with human review; Baseline users may switch if allowlisted |

Validation after deploy: restart Codex, then confirm active requirements include `allowed_approvals_reviewers` (cloud managed-config UI, decoded MDM `requirements_toml_base64`, or `/etc/codex/requirements.toml`). Attempting `approvals_reviewer = "auto_review"` under Moderate/Strict should fall back and notify the user.

**Overlap with approval_policy:** `approval_policy` decides when Codex pauses. `approvals_reviewer` decides who answers the pause. Pin both. Do not assume denying `never` alone blocks automatic review of escalations.

**Overlap with Codex CLI:** Desktop and CLI share `approvals_reviewer` / requirements keys when the client version supports them. Deploy the same `allowed_approvals_reviewers` pin to both surfaces under Moderate/Strict so CLI users cannot enable `auto_review` while Desktop cannot.

---

## Security Differences: Codex Desktop vs. Codex CLI

The Codex Desktop App, CLI, and IDE extension share the same configuration system (`config.toml`) and managed configuration layers. The desktop app additionally provides:

- **Browser Use** — AI can browse websites (allowlist/blocklist controlled)
- **Computer Use** — AI can interact with desktop apps (macOS only; not available in EEA/UK/Switzerland)
- **Codex Pets** — Visual overlays (low security risk)
- **Context-aware suggestions** — Follow-up recommendations

These features introduce additional attack surface that administrators should evaluate.

---

## Deployment Checklist

### Phase 1: Requirements Enforcement
- [ ] Deploy `requirements.toml` via cloud-managed config, MDM, or system file
- [ ] Set `allowed_sandbox_modes` to exclude `danger-full-access`
- [ ] Set `allowed_approval_policies` to exclude `never` (if needed)
- [ ] Pin `allowed_approvals_reviewers = ["user"]` for Moderate/Strict
- [ ] For Baseline only, allow `auto_review` and set `guardian_policy_config`
- [ ] Restrict MCP servers to an approved allowlist
- [ ] Pin `browser_use = false` and `computer_use = false` unless explicitly needed
- [ ] Add `deny_read` rules for sensitive paths

### Phase 2: Managed Defaults
- [ ] Deploy `managed_config.toml` with conservative starting values
- [ ] Set `approval_policy = "on-request"` as the default
- [ ] Set `approvals_reviewer = "user"` as the default
- [ ] Set `sandbox_mode = "workspace-write"` as the default
- [ ] Disable `network_access` unless required
- [ ] Configure telemetry to point at your OTLP collector

### Phase 3: Monitoring & Governance
- [ ] Enable audit logging via ChatGPT Compliance API
- [ ] Configure Analytics API for adoption tracking
- [ ] Set up RBAC via ChatGPT Enterprise workspace settings
- [ ] Periodically audit drift between local configs and managed policies
- [ ] Review MCP server access and tool permission grants

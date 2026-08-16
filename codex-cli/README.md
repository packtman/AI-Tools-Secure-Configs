# OpenAI Codex CLI — Secure Admin Configuration

This directory contains security-hardened configurations for **OpenAI Codex CLI** (the AI coding agent), targeting administrators who need to enforce sandbox restrictions, approval policies, and credential management.

## What Is Covered

| File | Purpose |
|------|---------|
| `config.toml` | Secure user-level configuration (`~/.codex/config.toml`) |
| `project-config.toml` | Secure project-level configuration (`.codex/config.toml`) |
| `examples/config-strict.toml` | **Strict** — Maximum-restriction configuration |
| `examples/config-moderate.toml` | **Moderate** — Balanced development configuration |
| `examples/config-baseline.toml` | **Baseline** — Essential security only (startups, individual devs) |
| `examples/requirements-strict.toml` | **Strict** admin-enforced requirements (Codex 0.147 plugins and `--approve-for-me`) |
| `examples/requirements-moderate.toml` | **Moderate** admin-enforced requirements (org marketplace allowlist) |
| `examples/requirements-baseline.toml` | **Baseline** admin-enforced requirements (plugin sharing off) |
| `examples/system-config.toml` | System-wide defaults (`/etc/codex/config.toml`) |

## Configuration Hierarchy (highest → lowest priority)

1. **Command-line arguments** — Override everything for a single invocation
2. **Project config** — `.codex/config.toml` (loaded only for trusted projects)
3. **User config** — `~/.codex/config.toml`
4. **System config** — `/etc/codex/config.toml` (Unix only)

## Key Security Concepts

### Sandbox Modes

| Mode | File access | Network | Use case |
|------|------------|---------|----------|
| `read-only` | Read-only workspace | Disabled | Code review, analysis |
| `workspace-write` | Read/write workspace | Disabled | Local development (default) |
| `danger-full-access` | Full system access | Enabled | NOT recommended for production |

**Security rule:** Never use `danger-full-access` in production or shared environments.

### Approval Policies

| Policy | Behavior |
|--------|----------|
| `untrusted` | Requires approval for every tool use including reads |
| `on-request` | Ask before every write/execute operation; reads are automatic |
| `never` | No approval required (use with extreme caution) |

### Protected Paths

The `.codex/` directory and `.git/` are always protected, even in writable sandbox modes.

### Credential Storage

| Option | Location | Security |
|--------|----------|----------|
| `keyring` | OS credential store | Most secure — uses macOS Keychain, Windows Credential Manager, or Linux Secret Service |
| `file` | `~/.codex/auth.json` | Less secure — plaintext file |
| `auto` | Keyring with file fallback | Recommended default |

## Deployment Checklist

1. Deploy `/etc/codex/config.toml` on all developer machines for organization-wide defaults.
2. Set `sandbox_mode = "workspace-write"` as the maximum allowed mode.
3. Set `approval_policy = "on-request"` for strict environments.
4. Configure `cli_auth_credentials_store = "keyring"` to avoid plaintext credential files.
5. Disable network access unless explicitly required.
6. Audit `.codex/config.toml` in project repositories before marking them as trusted.
7. For Codex 0.147+: deploy `requirements.toml` so `--approve-for-me` and plugin marketplaces cannot bypass laptop policy.

---

## Codex 0.147 Agent Plugins and `--approve-for-me`

Codex 0.147 (2026-08-07) added portable Agent Plugins (search across local, personal, workspace, and remote catalogs) and `--approve-for-me`, a CLI flag that sets `approvals_reviewer = "auto_review"` for one session without editing `config.toml`. `--full-auto` was removed; use `--sandbox workspace-write` instead. Unfamiliar local projects now require explicit trust before project `.codex/` layers load.

**MDM** means Mobile Device Management: software that pushes managed settings to endpoints. **SIEM** means Security Information and Event Management: centralized log collection and alerting. **MCP** means Model Context Protocol: a way for AI tools to call external services through MCP servers. **Agent Plugins** are installable bundles of skills, connectors, and sometimes MCP servers. **Auto-review** is a reviewer swap: a second model decides approval escalations. It does not widen the sandbox.

Codex CLI, Codex Desktop, and the IDE extension share `requirements.toml`. Deploy one requirements file. Do not copy the same pins into a second tool-specific file. Plugin marketplace restrictions apply to ChatGPT/Codex Desktop and Codex CLI. They do not control the IDE extension, ChatGPT on the web, or mobile.

### 1. Rollout Plan

**Pre-rollout checklist**

- [ ] Fleet is on Codex 0.147.0 or later (`codex --version`). Older clients ignore `[marketplaces]` and `--approve-for-me`.
- [ ] MDM path verified: macOS `com.openai.codex:requirements_toml_base64`, Windows `%ProgramData%\OpenAI\Codex\requirements.toml`, Linux `/etc/codex/requirements.toml`, or ChatGPT cloud-managed requirements.
- [ ] Secrets manager in place. Do not put tokens in `requirements.toml` or marketplace URLs that embed credentials.
- [ ] SIEM ingest tested for Codex session logs / ChatGPT Compliance API events.
- [ ] Rollback plan documented (this section).
- [ ] Inventory existing user marketplaces. `[marketplaces]` does not unload already-configured sources at runtime.

**Phased rollout**

| Phase | Who | Exit criteria |
|-------|-----|---------------|
| Pilot | Security + one app team (10 to 25 people) | `codex plugin marketplace add` from an unapproved git host fails; `--approve-for-me` falls back on Moderate/Strict; `/plugins` still works for the org catalog on Moderate |
| Expanded pilot | One business unit | Exception queue under an agreed weekly cap; no SIEM alerts for unmatched marketplace installs succeeding |
| Org-wide | Remaining Codex CLI/Desktop users | Same validation commands green on a sample of endpoints; rollback unused for 14 days |

**What will break (Moderate)**

- `codex --approve-for-me "..."` no longer auto-reviews; developers must approve in the TUI or use a Baseline exception profile.
- `codex plugin marketplace add https://github.com/random/repo.git` fails unless it matches `allowed_sources`.
- `/plugins search` does not query remote catalogs (`features.remote_plugin = false`).
- Developers cannot publish a laptop-built plugin into the workspace catalog (`plugin_sharing = false`).
- Codex 0.147 also prompts for explicit project trust. Untrusted repos skip project `.codex/` config, hooks, and rules.

Developer-facing message to send before rollout:

> On DATE we will enforce Codex plugin marketplace allowlists and keep human approval on (no `--approve-for-me` on laptops). Install plugins only from OUR-ORG/codex-plugins. If a plugin is missing, file an exception with the catalog URL and business reason. For CI, keep using `--sandbox workspace-write` (not the removed `--full-auto`). Unfamiliar repos will ask you to trust the project before `.codex/` settings load.

**Rollback**

1. Revert `/etc/codex/requirements.toml` (or MDM `requirements_toml_base64`, or cloud-managed assignment) to the previous file.
2. Remove `allowed_approvals_reviewers`, `[marketplaces]`, and `features.plugins` / `remote_plugin` / `plugin_sharing` pins.
3. Ask users to restart Codex CLI/Desktop.
4. Communication: "Codex plugin and auto-review pins were rolled back. You can use `--approve-for-me` and add marketplaces again. Tell security if a plugin install is still blocked."

### 2. Config Files

Use `examples/requirements-{strict,moderate,baseline}.toml` plus matching `examples/config-*.toml`. Replace `YOUR-ORG` before production.

### 3. Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `features.plugins` | unset (available) | unset (available) | `false` | Strict removes plugin-bundled tools/hooks/MCP. Moderate uses an org catalog instead of a total off switch. |
| `features.remote_plugin` | unset | `false` | `false` | Remote catalog federation is the 0.147 supply-chain expansion. Baseline may experiment. |
| `features.plugin_sharing` | `false` | `false` | `false` | All tiers block laptop-to-workspace plugin publish. |
| `marketplaces.restrict_to_allowed_sources` | unset | `true` | `true` | Moderate/Strict require an allowlist. Strict ships no extra sources (OpenAI-managed catalogs only, and plugins are off). |
| `marketplaces.allowed_sources` | unset | org git placeholder | none | Moderate names one reviewed catalog. Strict relies on plugins=false. |
| `allowed_approvals_reviewers` | unset (allows `auto_review`) | `["user"]` | `["user"]` | Blocks `--approve-for-me` on laptops. Baseline keeps it for CI. |
| `approvals_reviewer` (defaults) | unset | `user` | `user` | Starting value. Requirements are the enforcement layer. |

### 4. Deployment Steps

| OS | User config | System config | Requirements (enforced) | Managed defaults |
|----|-------------|---------------|-------------------------|------------------|
| macOS | `~/.codex/config.toml` | `/etc/codex/config.toml` | `/etc/codex/requirements.toml` or MDM `com.openai.codex:requirements_toml_base64` | MDM `config_toml_base64` or `/etc/codex/managed_config.toml` |
| Linux | `~/.codex/config.toml` | `/etc/codex/config.toml` | `/etc/codex/requirements.toml` | `/etc/codex/managed_config.toml` |
| Windows | `%USERPROFILE%\.codex\config.toml` | `%ProgramData%\OpenAI\Codex\config.toml` | `%ProgramData%\OpenAI\Codex\requirements.toml` | `%USERPROFILE%\.codex\managed_config.toml` |

Jamf / Intune / Workspace ONE: push the same `com.openai.codex` payload as Desktop (base64 TOML). Linux has no native Codex MDM; use a root-owned `/etc/codex/requirements.toml` (mode 644, not a symlink) via your config management tool.

**Validation**

```bash
codex --version   # expect 0.147.0 or later
codex plugin marketplace list --json
# Moderate: adding an unmatched git host should fail
codex plugin marketplace add https://github.com/unapproved/plugins.git ; echo exit:$?
# Moderate/Strict: auto-review should not stick
codex --approve-for-me "print hello" 2>&1 | head
```

On Desktop, open Plugins Directory and confirm only the org catalog (Moderate) or no plugins (Strict). Confirm the startup config summary shows managed requirements.

**Audit logging**

- ChatGPT Enterprise: Compliance API / workspace audit log. Alert on marketplace add, plugin install, and approval-policy changes.
- Local: session transcripts under `~/.codex/sessions` (do not ingest prompt bodies into SIEM unless policy allows). Alert if `--approve-for-me` or `approvals_reviewer=auto_review` appears on Moderate/Strict endpoints.
- Requirements load failure fails closed for cloud-managed bundles (no silent start without policy). Alert on clients that start without a requirements cache after assignment.

### 5. Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| `codex --approve-for-me` | Auto-review removes the human pause. Sandbox still applies, but risky commands can proceed without a person. | Keep `approvals_reviewer = "user"`. For CI, use `--sandbox workspace-write` (not `--full-auto`) on a Baseline runner or an exception profile. |
| `codex plugin marketplace add <unapproved git>` | Unreviewed plugins can bundle MCP, hooks, and skills. | Add the catalog to `marketplaces.allowed_sources`, pin `ref`, then `codex plugin marketplace add` that URL. |
| Remote `/plugins search` | Federated remote catalogs expand supply chain. | Search the org git marketplace only. |
| Workspace plugin sharing | A laptop-built plugin becomes org-wide code execution. | Publish through the reviewed git catalog. |
| Trusting a cloned repo blindly | Malicious `.codex/config.toml` could try to weaken local defaults. | Inspect `.codex/` first. Project config still cannot override requirements. |
| Plugin-bundled MCP | Same exfil risk as other MCP. | Put MCP in the managed `mcp_servers` allowlist (Strict: empty table). Plugin MCP uses `plugins.<plugin>.mcp_servers.<server>` identity matching. |

**False-positive friction:** Moderate developers will hit marketplace add failures for personal catalogs. Handle exceptions by adding a named `allowed_sources` rule (git URL + `ref`, or `host_pattern` for an internal Git host), not by setting `restrict_to_allowed_sources = false`.

**Overlap:** Claude Code and Cursor also run shell and MCP. Codex marketplace pins do not cover those tools. Copilot `allowedMcpServers` is a different file. Do not treat one allowlist as covering the others.

**Gap:** Plugin marketplace requirements do not apply to the Codex IDE extension, ChatGPT on the web, or mobile. Use workspace RBAC and network egress filters for those surfaces.

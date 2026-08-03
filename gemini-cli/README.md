# Google Gemini CLI: Secure Admin Configuration

Hardened templates for Google Gemini CLI for IT and security teams rolling out agent tooling without breaking developer workflows.

This update focuses on **Management Console** remote admin controls (`admin.secureModeEnabled`, `admin.mcp.*`, `admin.skills.enabled`). Endpoint `settings.json` templates remain available for hosts that lack Gemini Code Assist enterprise remote admin.

## What Is Covered

| File | Purpose |
|------|---------|
| `settings.json` | User/system settings template (`~/.gemini/settings.json`) |
| `enterprise-policy.md` | System settings paths, MDM notes, Management Console mapping |
| `examples/management-console-strict.json` | Strict Management Console targets |
| `examples/management-console-moderate.json` | Moderate Management Console targets + required MCP example |
| `examples/management-console-baseline.json` | Baseline Management Console targets |
| `examples/management-console.comments.md` | Rationale for every console / `admin.*` control |
| `examples/settings-*.json` | Endpoint settings tiers |
| `examples/system-settings-enterprise.json` | System overrides example |
| `examples/system-defaults-enterprise.json` | System defaults example |
| `examples/deployment-guide.md` | Multi-platform endpoint deployment |
| `examples/policy-rationale.md` | Endpoint settings rationale |

---

## 1. Rollout Plan

### Phased rollout

| Phase | Scope | Exit criteria |
|-------|-------|---------------|
| Pilot | 5-15 developers on one team with Gemini Code Assist enterprise | Console Strict Mode verified; no YOLO; MCP/skills match tier; no P0 tickets for 1 week |
| Expanded pilot | One business unit / OS mix | SIEM sees auth and policy-relevant events; exception process works; endpoint system settings (if used) match console intent |
| Org-wide | All licensed users | Rollback runbook tested; owner named for console changes; quarterly control review scheduled |

### Pre-rollout checklist

- [ ] Confirm Gemini Code Assist enterprise entitlements and Management Console access (https://goo.gle/manage-gemini-cli)
- [ ] Decide tier: Strict, Moderate, or Baseline
- [ ] Secrets manager ready for any MCP OAuth (never store secrets in these templates)
- [ ] SIEM ingest path identified for Gemini CLI / Google Cloud audit signals you already collect
- [ ] Rollback owner and communication template approved
- [ ] If some users lack remote admin: plan endpoint system overrides as the next-best control

### What will break (by tier)

| Tier | Likely breakage | Developer message |
|------|-----------------|-------------------|
| Strict | No YOLO / Always allow; no MCP; no Agent Skills; no extensions | "Gemini CLI runs in org Strict Mode. YOLO, MCP, Skills, and extensions are off. Use reviewed local tools only, or request an exception." |
| Moderate | No YOLO; no Skills/extensions; MCP only via allowlist + required remote servers; local stdio MCP blocked by admin merge rules | "MCP is limited to approved remote servers. Skills and extensions stay off until reviewed. YOLO remains disabled." |
| Baseline | No YOLO; extensions off; Skills allowed with consent prompts | "Strict Mode stays on. You may use reviewed Agent Skills. Prefer org skill catalogs over random git installs." |

### Rollback procedure

1. Management Console: restore previous Strict Mode / Extensions / MCP / Unmanaged Capabilities values (or disable custom MCP allowlist and required servers).
2. If endpoint system overrides were also deployed, revert `/etc/gemini-cli/settings.json` (Linux), `/Library/Application Support/GeminiCli/settings.json` (macOS), or `C:\ProgramData\gemini-cli\settings.json` (Windows) to the prior artifact.
3. Ask users to restart Gemini CLI so remote admin and local files reload.
4. Communication template: "We rolled back Gemini CLI admin policy to [previous tier/date]. Restart the CLI. Open a ticket if sessions still show the new restrictions."

---

## 2. Config Files (Management Console)

Use exact filenames under `examples/`:

- `management-console-baseline.json`
- `management-console-moderate.json`
- `management-console-strict.json`

These files are **policy targets**, not drop-in local settings. The `runtimeAdminEquivalent.admin` object documents what the CLI applies after the management service maps console fields.

Necessary controls only:

| Control | Threat or function |
|---------|--------------------|
| Strict Mode | Blocks YOLO / Always allow auto-approval |
| Extensions off | Blocks unreviewed extension tool surface |
| MCP master switch | Stops or allows external tool bridges |
| MCP allowlist / requiredConfig | Limits or forces remote MCP (Moderate) |
| Unmanaged Capabilities / Skills | Stops or allows Agent Skills packages |

---

## 3. Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for difference |
|---------|----------|----------|--------|------------------------|
| Strict Mode / `admin.secureModeEnabled` | enabled / true | enabled / true | enabled / true | All tiers block YOLO and Always allow |
| Extensions / `admin.extensions.enabled` | disabled / false | disabled / false | disabled / false | Extensions expand tools outside MCP governance |
| MCP enabled / `admin.mcp.enabled` | true | true | false | Strict removes MCP; others keep constrained MCP |
| MCP allowlist / `admin.mcp.config` | `{}` (local MCP still usable) | explicit remote allowlist | `{}` (unused) | Moderate enforces audited remotes |
| Required MCP / `admin.mcp.requiredConfig` | `{}` | remote compliance example | `{}` | Only Moderate injects mandatory remote MCP |
| Unmanaged Capabilities / `admin.skills.enabled` | enabled / true | disabled / false | disabled / false | Baseline allows Skills; higher tiers wait for review |

---

## 4. Deployment Steps

### Management Console (preferred when available)

1. Open https://goo.gle/manage-gemini-cli with an enterprise admin account.
2. Set Strict Mode, Extensions, MCP, Required MCP Servers (preview), and Unmanaged Capabilities to match the chosen tier file.
3. For Moderate required/allowlisted servers: remote `http` or `sse` only. Set trust off unless a written exception exists. Keep OAuth client secrets in a secrets manager, not git.
4. Validate on a pilot machine: restart Gemini CLI, confirm YOLO is blocked, confirm `/mcp` and Skills behavior match the tier.

### Endpoint system settings (next-best control)

Gemini CLI has **no Jamf/Intune managed-settings schema** equivalent to Cursor/Claude Desktop MDM keys. Use:

| OS | System overrides path |
|----|----------------------|
| Linux | `/etc/gemini-cli/settings.json` |
| macOS | `/Library/Application Support/GeminiCli/settings.json` |
| Windows | `C:\ProgramData\gemini-cli\settings.json` |

Push those files with your config management or MDM file/payload mechanism. They can still be changed by users with local admin rights. Prefer Management Console when entitled.

### Validation

- Confirm Strict Mode: attempt YOLO / Always allow and expect denial under remote admin.
- MCP Strict: `/mcp` or MCP tools unavailable.
- MCP Moderate: only allowlisted names connect; required server appears without local config; local `command`-based servers are cleared/ignored per admin merge rules.
- Skills Strict/Moderate: Agent Skills unavailable; Baseline: `/skills list` works, activation still prompts for consent.
- Endpoint overlay: `gemini` starts and reads system overrides (check deployed file hash/mtime).

### Audit logging / SIEM

- Enable Gemini CLI telemetry to your approved collector when using endpoint templates (`telemetry.enabled`, never log prompts in regulated tiers).
- Alert on: sudden enabling of YOLO if remote admin drops; new MCP endpoints; Skills installs from untrusted git hosts; admin console policy edits.
- Ship Google Cloud / Workspace admin audit events for console changes to SIEM if available.

---

## 5. Workflow-Preservation Notes

| Blocked | Risk | Safe equivalent |
|---------|------|-----------------|
| YOLO / Always allow | Unreviewed destructive commands | Keep step-by-step approvals; use narrow `tools.core` allowlists on endpoints |
| Arbitrary MCP (Strict) | Data exfil via tool bridges | Call approved internal APIs from reviewed scripts outside the agent |
| Local stdio MCP under admin allowlist | User swaps binary via `command` | Host only remote HTTP/SSE MCP behind corp auth |
| Agent Skills (Strict/Moderate) | Untrusted skill packs + directory access | Publish reviewed skills later; until then use GEMINI.md runbooks |
| Extensions | Opaque extra tools | Request exception with threat review; prefer MCP allowlist |

### False-positive friction

- Moderate required MCP with `trust: false` increases approval prompts: expected. Do not flip trust on without review.
- Baseline empty MCP allowlist is permissive: teams that need host enforcement without enterprise console should also deploy system `mcp.allowed`.
- Overlap: Claude Code, Cursor, Codex, and Gemini CLI can all run shell and MCP. Align allowlists across tools so you do not double-block a safe workflow in one tool while leaving the same risk open in another.

### Exception requests

Require: business justification, tool/MCP/skill name, data classification, time-bound owner, and Moderate-or-better compensating control (allowlist entry, required remote server with tool filters, or temporary Baseline Skills enablement for a named group only).

---

## Configuration File Locations (endpoint)

| OS | User Settings | System Defaults | System Overrides |
|----|---------------|-----------------|------------------|
| macOS | `~/.gemini/settings.json` | `/Library/Application Support/GeminiCli/system-defaults.json` | `/Library/Application Support/GeminiCli/settings.json` |
| Windows | `~/.gemini/settings.json` | `C:\ProgramData\gemini-cli\system-defaults.json` | `C:\ProgramData\gemini-cli\settings.json` |
| Linux | `~/.gemini/settings.json` | `/etc/gemini-cli/system-defaults.json` | `/etc/gemini-cli/settings.json` |

Project overrides: `.gemini/settings.json`.

## Precedence

1. System defaults  
2. User settings  
3. Project settings  
4. System overrides (highest for local files)  
5. Remote Management Console admin controls (immutable locally when present)

## Related Guides

- [Enterprise Policy](./enterprise-policy.md)
- [Deployment Guide](./examples/deployment-guide.md)
- [Management Console rationale](./examples/management-console.comments.md)
- [Endpoint policy rationale](./examples/policy-rationale.md)
- [Official enterprise admin controls](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/admin/enterprise-controls.md)

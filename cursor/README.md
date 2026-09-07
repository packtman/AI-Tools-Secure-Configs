# Cursor: Secure Admin Configuration

This directory contains security-hardened configurations for **Cursor** (the AI-powered code editor), targeting administrators who need to enforce tool restrictions, workspace trust, sandboxing, and compliance policies across their organization.

## What Is Covered

| File | Purpose |
|------|---------|
| `permissions.json` | Secure `~/.cursor/permissions.json` template (Allowlist + Auto-review) |
| `settings.json` | Recommended VS Code / Cursor settings for security |
| `rules/security.mdc` | Cursor Rules file for secure coding instructions |
| `examples/mdm-policies.md` | MDM deployment guide for enterprise policies |
| `examples/permissions-strict.json` | **Strict**: Maximum-restriction permissions |
| `examples/permissions-moderate.json` | **Moderate**: Balanced permissions for development teams |
| `examples/permissions-baseline.json` | **Baseline**: Essential restrictions only (startups, individual devs) |
| `examples/sandbox-strict.json` | **Strict**: Deny-by-default sandbox network and no temp writes |
| `examples/sandbox-moderate.json` | **Moderate**: Deny-by-default sandbox with package registries |
| `examples/sandbox-baseline.json` | **Baseline**: Sandbox on with starter allowlist |
| `examples/enterprise-policy-strict.json` | **Strict**: Dashboard/MDM policy checklist |
| `examples/enterprise-policy-moderate.json` | **Moderate**: Dashboard/MDM policy checklist |
| `examples/enterprise-policy-baseline.json` | **Baseline**: Dashboard/MDM policy checklist |
| `examples/settings-rationale.md` | Comprehensive security reasoning for every setting |
| `examples/cloud-agent-security.json` | Cloud Agent dashboard security reference config |

## Configuration Files

### `permissions.json`

Location: `~/.cursor/permissions.json` (optional project copy at `<repo>/.cursor/permissions.json`)

Controls:

- **Allowlist mode**: `terminalAllowlist` and `mcpAllowlist` (`server:tool` syntax)
- **Auto-review mode** (Cursor 3.6+): `autoRun.allow_instructions` and `autoRun.block_instructions` (plain English)

Team Admin Dashboard Auto-review and MCP policies take highest precedence and replace local files when set.

### `sandbox.json`

Location: `~/.cursor/sandbox.json` or `<repo>/.cursor/sandbox.json`

Controls where sandboxed shell commands can read/write and which network destinations they can reach. Team-admin policy and Cursor hardcoded protections always win over local files.

### Cursor Rules

Project rules stored in `.cursor/rules/` provide persistent instructions for Agent mode. Rules can be:

- **Always**: applied to every interaction
- **Auto**: applied when Cursor deems them relevant
- **File-scoped**: applied when matching files are in context
- **Manual**: applied only when explicitly referenced

Rules are steering, not a hard security boundary. Pair them with Run Mode, sandboxing, and hooks.

## MDM-Managed Policies

Enterprise admins can enforce policies through MDM (Jamf, Intune, Kandji):

| Policy key | Type | Description |
|------------|------|-------------|
| `AllowedTeamId` | String | Restricts login to a specific team |
| `AllowedExtensions` | String (JSON) | Allowlist of permitted extensions (JSON object string) |
| `WorkspaceTrustEnabled` | Boolean | Enforce workspace trust mode |
| `UpdateMode` | String | Control update behavior (`manual`, `start`, `default`) |
| `NetworkDisableHttp2` | Boolean | Force HTTP/1.1 for network requests |

`permissions.json` and `sandbox.json` are not MDM keys. Deploy them with config management, and enforce Run Mode / MCP / Privacy Mode from the team dashboard.

## Enterprise Features

| Feature | Description |
|---------|-------------|
| SSO / SAML | Enforce single sign-on for all team members |
| SCIM | Automated user provisioning/deprovisioning |
| Run Mode policy | Org default Auto-review or Allowlist; disable Run Everything |
| Agent sandbox | Org-wide sandbox for local agent shell commands |
| Browser / file protections | Require approval for Browser, file deletion, external files, and `.cursor` changes |
| MCP allowlist | Approve servers, tools, and per-server network modes |
| BYOK disable | Block personal provider API keys |
| Repository blocklist | Block sensitive repos from Cursor |
| Protected Git Scopes | Lock Git orgs/namespaces to your Cursor org for Cloud Agents and Bugbot |
| Audit logs | Track authentication, settings changes, rule modifications |
| Admin API | Programmatic team and settings management |
| Team Rules | Enforced or optional rules managed from the dashboard |

## Rollout Plan (Cursor)

### Phased rollout

1. **Pilot (5-15 developers)**: Deploy Moderate `permissions.json` + `sandbox.json`, set dashboard Run Mode to Auto-review with Run Everything disabled, enforce Privacy Mode and AllowedTeamId.
   - Exit criteria: less than 10% exception requests per week; no secret-exfiltration SIEM alerts; developers can complete lint/test workflows.
2. **Expanded pilot (one org unit)**: Add MCP allowlist, Browser Protection, `.cursor` Directory Protection, repository blocklist for regulated repos.
   - Exit criteria: MCP exception process documented; sandbox Linux kernel/AppArmor issues resolved; SIEM ingest confirmed.
3. **Org-wide**: Enforce Strict or Moderate by risk tier. Disable BYOK where ZDR depends on Cursor routing.
   - Exit criteria: MDM coverage report green; rollback drill completed; developer FAQ published.

### Pre-rollout checklist

- [ ] MDM path verified for `AllowedTeamId`, `WorkspaceTrustEnabled`, `AllowedExtensions`
- [ ] Secrets manager path documented (no secrets in rules or MCP configs)
- [ ] SIEM ingest tested for Cursor audit logs and hook failure events
- [ ] Rollback plan documented (dashboard toggles + file removal)
- [ ] Overlap review with Claude Code / Copilot shell and MCP controls completed

### What will break (Moderate)

- Piped downloads (`curl … \| bash`) need approval
- `.env` / credential file reads need approval
- AWS and Kubernetes mutating commands need approval
- MCP tools do not auto-run
- Browser tool calls need approval when Browser Protection is on
- Sandboxed commands cannot reach arbitrary hosts

Developer message template: "Cursor will auto-run only approved local lint/test commands. Cloud mutations, secret file reads, MCP tools, and Browser actions will ask for approval. Download packages yourself, inspect them, then run installs when prompted."

### Rollback

1. Team dashboard: restore previous Run Mode, MCP, Privacy, and Cloud Agent settings.
2. Remove or replace `~/.cursor/permissions.json` and `~/.cursor/sandbox.json`.
3. MDM: clear or restore previous `AllowedTeamId` / `AllowedExtensions` payloads if those caused login or extension blocks.
4. Communicate: "Cursor agent approvals temporarily restored to the prior policy while we investigate."

## Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| Run Mode default | Auto-review | Auto-review | Allowlist | Strict prefers deterministic allowlists over classifier judgment |
| Run Everything | Disabled | Disabled | Disabled | Unattended full autonomy is never acceptable for org devices |
| `terminalAllowlist` breadth | Broad (install/build) | Lint/test/build | Read-only git/fs | Tighter lists reduce unattended side effects |
| `autoRun.block_instructions` | Secrets + pipe-to-shell + prod destroy | Adds AWS/K8s/sudo/git push/MCP writes | Adds Browser, package installs, docker push, terraform | Higher tiers force more human gates |
| `mcpAllowlist` | `[]` | `[]` | `[]` | No MCP auto-run in file templates; use dashboard for exceptions |
| Sandbox `networkPolicy.default` | deny | deny | deny | Deny-by-default; allowlist grows only with justified registries |
| `disableTmpWrite` | false | false | true | Strict reduces temp-dir staging for payloads |
| `enableSharedBuildCache` | true | true | false | Strict avoids shared cache side channels across modes |
| Browser Protection | on | on | on | Browser tool can reach arbitrary origins |
| `.cursor` Directory Protection | off | on | on | Prevents agents from rewriting local rules/settings |
| BYOK disabled | no | yes | yes | Personal keys bypass Cursor ZDR agreements |
| Cloud Agent computer use | disabled | disabled | disabled | GUI/browser automation is high blast radius |
| Community marketplace import | off | off | off | Reduces unvetted plugin/MCP supply chain risk |

## Deployment Steps

### File paths

| OS | permissions.json | sandbox.json |
|----|------------------|--------------|
| macOS / Linux | `~/.cursor/permissions.json` | `~/.cursor/sandbox.json` |
| Windows | `%USERPROFILE%\.cursor\permissions.json` | `%USERPROFILE%\.cursor\sandbox.json` |
| Per-repo (optional) | `<repo>/.cursor/permissions.json` | `<repo>/.cursor/sandbox.json` |

### MDM

See `examples/mdm-policies.md` for Jamf / Intune / Linux policy payloads (`AllowedTeamId`, `AllowedExtensions`, `WorkspaceTrustEnabled`, `UpdateMode`).

### Validation

1. Cursor Settings → Agents → Approvals & Execution shows org-allowed modes only (no Run Everything).
2. Trigger a blocked instruction (for example an AWS CLI call) and confirm an approval prompt.
3. In a sandboxed command, confirm outbound calls to non-allowlisted hosts fail.
4. Confirm personal account login fails when `AllowedTeamId` MDM is set.
5. Confirm MCP servers outside the dashboard allowlist cannot start.

### Audit logging / SIEM

- Stream Enterprise audit logs (auth, member, admin setting changes) to SIEM.
- Use hooks with `failClosed` for command/file events that Cursor audit logs do not cover.
- Alert on: Privacy Mode disabled attempts, MCP allowlist changes, Run Everything enablement, BYOK enablement, repeated approval bypass patterns from hooks.

## Workflow-Preservation Notes

| Blocked / prompted operation | Risk | Safe equivalent |
|------------------------------|------|-----------------|
| `curl https://… \| bash` | Remote code execution | Download, inspect, then run a pinned installer |
| Reading `.env` / PEM / SSH keys | Secret exfiltration to the model or logs | Use secrets manager injection in CI, not agent context |
| AWS / kubectl mutate | Production change without change control | Run through approved CLI/CD pipeline after human review |
| MCP auto-run | Third-party tool can read/write external systems | Add only reviewed servers to dashboard allowlist; keep file `mcpAllowlist` empty |
| Browser tool | Navigation to unapproved origins | Use Browser Controls allowlist or keep Browser Protection on |
| `Run Everything` | No approval prompts | Keep Auto-review or Allowlist; use hooks for hard denies |

### False-positive friction

- Auto-review may over-block unusual but safe local scripts: add a narrow `allow_instructions` sentence or an Allowlist entry after security review.
- Linux sandbox needs kernel 6.2+ Landlock or AppArmor package in remote/CLI environments: document the install package before Strict rollout.
- Empty MCP allowlist causes prompt fatigue if MCP is core to the workflow: approve specific `server:tool` entries in the dashboard, not `*:*`.

### Overlap with other tools

Claude Code and Cursor both execute local shell commands and can host MCP servers. Apply shell/MCP policy in both places, or explicitly choose one agent runtime per team to avoid a gap where only one tool is locked down.

## Deployment Checklist

1. Deploy `permissions.json` and `sandbox.json` to developer machines via config management.
2. Set team dashboard Run Mode to Auto-review (or Allowlist for Strict) and disable Run Everything.
3. Enable Browser, File-Deletion, External-File, and `.cursor` Directory Protection.
4. Enforce Privacy Mode; disable BYOK if you rely on Cursor ZDR.
5. Configure MCP allowlist and per-server network mode in the dashboard.
6. Add `.cursor/rules/security.mdc` to repositories and enforced Team Rules as needed.
7. Configure MDM policies for `AllowedTeamId` and `WorkspaceTrustEnabled`.
8. Set up SSO/SAML and SCIM provisioning.
9. Enable audit logging and SIEM streaming; review weekly.
10. Restrict extensions via `AllowedExtensions` and set an install cooldown.

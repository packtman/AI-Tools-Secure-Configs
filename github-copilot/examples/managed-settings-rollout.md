# GitHub Copilot managed settings rollout (Moderate)

**Tool:** GitHub Copilot (Business or Enterprise)
**Tier:** Moderate (Enterprise), with Strict and Baseline deltas in the table below
**Environment:** Standard enterprise, mixed OS (macOS, Windows, Linux), MDM available (Jamf + Intune), SIEM available
**Upstream change this rollout covers:** MCP allowlists in `copilot/managed-settings.json` (GA 2026-08-06) and Agent Plugins 1.0 governance via `enabledPlugins` / `strictKnownMarketplaces` (GA 2026-08-12)

This guide is for IT admins who have not used Copilot as a daily driver. Pair it with `org-policy-moderate.json` (GitHub.com AI Controls) and `copilot-instructions.md` (repo instructions). Managed settings are a separate, stronger control plane than the AI Controls MCP registry toggle.

---

## Glossary

| Term | Definition |
|------|-----------|
| **MDM** | Mobile Device Management: software that pushes policies to endpoints (Jamf on macOS, Intune on Windows). |
| **SIEM** | Security Information and Event Management: centralized log collection and alerting. |
| **MCP** | Model Context Protocol: a way for Copilot to call external tools through MCP servers. |
| **Managed settings** | JSON that GitHub Copilot clients load from a `.github-private` repo, MDM, or a device file. Users cannot loosen most keys. |
| **Agent Plugin** | A package that can include a skill and an MCP server. Agent Plugins 1.0 is an open standard (2026-08-12) used by Copilot, VS Code, and other agents. |
| **Bypass / YOLO** | Copilot CLI and VS Code mode that auto-approves tools, paths, and URLs. Equivalent risk to Claude Code `--dangerously-skip-permissions`. |
| **`.github-private`** | A private GitHub repository that stores enterprise AI standards, including `copilot/managed-settings.json`. |

---

## 1. Rollout Plan

### 1.1 Phased rollout

#### Phase 1: Pilot group (5-10 developers, 2 weeks)

**Who:** Two or three teams that already have Copilot seats. Include one VS Code user, one Copilot CLI user (if you will allow CLI exceptions), and one Copilot app user. MCP allowlists are enforced on those three clients. They are not enforced on Copilot cloud agent.

**What to deploy:**
- `managed-settings-moderate.json` as `copilot/managed-settings.json` in the source organization's `.github-private` repository
- Replace `YOUR-ORG` and `YOUR-ORG/YOUR-PLUGIN-MARKETPLACE`
- Keep the AI Controls **MCP servers in Copilot** policy enabled
- Set **Restrict MCP access to registry servers** to **Allow all** so this file is the single MCP allowlist
- Keep `org-policy-moderate.json` feature policies (CLI disabled, web search disabled, content exclusion)

**Exit criteria:**
- [ ] Pilot clients show the policy after restart or re-sign-in (within about one hour for server-managed)
- [ ] A non-allowlisted MCP server is blocked on VS Code and the Copilot app
- [ ] Built-in GitHub MCP still works
- [ ] Bypass / YOLO cannot be enabled
- [ ] Zero credential or disk-exfil incidents
- [ ] Rollback tested on one endpoint
- [ ] At least 60% of the pilot group rate the change as manageable

#### Phase 2: Expanded pilot (25-50 developers, 2 weeks)

**Who:** All engineering teams with Copilot seats. Exclude CI runners and shared servers.

**What to deploy:**
- Same managed settings, plus MDM or file-based delivery for Linux and for Copilot CLI sessions that must work if the server fetch fails
- Publish the real org plugin marketplace repo, or temporarily empty `strictKnownMarketplaces` only if Phase 1 showed plugin discovery was blocking a required workflow (track as an exception)
- Confirm cloud agent remains limited in org policy (allowlists do not apply there)

**Exit criteria:**
- [ ] Phase 1 criteria still hold
- [ ] Exception process used at least once (add a `serverUrl` or `serverCommand`)
- [ ] Linux file-based path owned by root and not world-writable
- [ ] VS Code, Copilot app, and (if enabled) Copilot CLI all observed the allowlist
- [ ] SIEM shows Copilot audit events for policy and content-exclusion changes

#### Phase 3: Org-wide

**Who:** Every Copilot-seated user.

**What to deploy:**
- Server-managed file on the default branch of `.github-private`
- MDM string keys for macOS and Windows device groups that must be governed before sign-in
- File-based settings on Linux
- Quarterly review of `allowedMcpServers` and the plugin marketplace repo

### 1.2 Pre-rollout checklist

| # | Item | Owner | Status |
|---|------|-------|--------|
| 1 | Source organization and `.github-private` repository exist (or MDM/file-based chosen instead) | GitHub admin | [ ] |
| 2 | `YOUR-ORG/YOUR-PLUGIN-MARKETPLACE` repo created, or marketplace keys removed until it exists | Platform | [ ] |
| 3 | AI Controls MCP toggle enabled; registry restriction set to Allow all | GitHub admin | [ ] |
| 4 | Cloud agent disabled or limited in org policy (allowlists are not enforced there) | Security | [ ] |
| 5 | Secrets manager in place. No tokens in managed-settings.json | Security | [ ] |
| 6 | SIEM ingest tested for `copilot.*` audit events | Security | [ ] |
| 7 | MDM path verified: Jamf `com.github.copilot`, Intune `HKLM\SOFTWARE\Policies\GitHubCopilot` | Endpoint | [ ] |
| 8 | Linux file path `/etc/github-copilot/managed-settings.json` documented for non-MDM fleets | Endpoint | [ ] |
| 9 | Rollback plan reviewed (this document, section 1.4) | IT | [ ] |
| 10 | Developer message sent at least 3 business days before Phase 1 | Engineering manager | [ ] |

### 1.3 What will break

| Workflow | Why it breaks on Moderate | Developer-facing message |
|----------|---------------------------|--------------------------|
| Adding a public MCP server from a blog post | Not on `allowedMcpServers` | Use the built-in GitHub MCP, or file an exception with the exact `serverUrl` or `serverCommand`. Do not rename a server to bypass policy. Names are not a security control. |
| Installing a plugin from Awesome Copilot | `strictKnownMarketplaces` pins the org catalog | Request the plugin be added to `YOUR-ORG/YOUR-PLUGIN-MARKETPLACE`, or request a team override if the enterprise marked the key overridable. |
| Copilot CLI `--yolo` / VS Code global auto-approve | `disableBypassPermissionsMode` is `disable` | Approve tools one at a time. If a workflow is blocked, file an exception. Do not look for a bypass flag. |
| Copilot cloud agent MCP | Allowlists are not enforced on cloud agent | Cloud agent stays limited in org policy. Do not assume this file covers it. |
| Package restore inside Copilot CLI sandbox (if CLI is later enabled) | Sandbox is forced on | Restore packages on the host terminal, or request a path grant. |

**Message to send before rollout:**

> Starting [DATE], GitHub Copilot will load enterprise managed settings. Two changes matter for daily work. First, Copilot will only connect to approved MCP servers (the built-in GitHub MCP is already approved). Second, plugins can only be installed from our org marketplace. Copilot will also refuse YOLO / allow-all. If a server or plugin you need is missing, file an exception with the exact URL or command. Do not put tokens in config files.

### 1.4 Rollback procedure

**Files and keys to revert:**

| Channel | What to revert |
|---------|----------------|
| Server-managed | Revert `copilot/managed-settings.json` on the default branch of `.github-private`. Optionally delete `copilot/team-mappings.json` and `copilot/teams/*.json`. |
| File-based | Remove `/Library/Application Support/GitHubCopilot/managed-settings.json` (macOS), `%ProgramFiles%\GitHubCopilot\managed-settings.json` (Windows), `/etc/github-copilot/managed-settings.json` (Linux). |
| MDM | Remove string values under `com.github.copilot` (macOS) and `HKLM\SOFTWARE\Policies\GitHubCopilot` (Windows). |
| AI Controls | Leave the MCP toggle as it was. Do not re-enable registry-only restriction unless you are abandoning managed-settings allowlists. |

Ask users to restart VS Code, Copilot CLI, and the Copilot app. Server-managed rollback can take up to an hour unless they sign in again.

**Communication template:**

> We rolled back Copilot managed settings at [TIME]. Restart your editor. MCP and plugin installs should match the previous baseline. If a server is still blocked, sign out of GitHub Copilot and sign back in, then contact #it-ai-tools.

---

## 2. Config Files

Deployable JSON (no comments):

- [`managed-settings-strict.json`](managed-settings-strict.json)
- [`managed-settings-moderate.json`](managed-settings-moderate.json)
- [`managed-settings-baseline.json`](managed-settings-baseline.json)

JSONC with inline rationale:

- [`managed-settings-strict.jsonc`](managed-settings-strict.jsonc)
- [`managed-settings-moderate.jsonc`](managed-settings-moderate.jsonc)
- [`managed-settings-baseline.jsonc`](managed-settings-baseline.jsonc)

Key mapping: [`managed-settings.comments.md`](managed-settings.comments.md)

Replace `YOUR-ORG` and `YOUR-ORG/YOUR-PLUGIN-MARKETPLACE` before deploy. Never commit tokens.

---

## 3. Tier Delta Table

| Setting | Baseline | Moderate | Strict | Reason for the difference |
|---------|----------|----------|--------|---------------------------|
| `permissions.disableBypassPermissionsMode` | `"disable"` | `"disable"` | `"disable"` | Bypass skips every tool prompt. Keep it off in every tier. |
| `enabledPlugins` | omitted | `{}` | `{}` | Do not auto-install plugins until an admin names them. |
| `extraKnownMarketplaces` | omitted | org GitHub repo | omitted | Moderate adds one approved catalog. Strict adds none. |
| `strictKnownMarketplaces` | omitted | same org repo | `[]` | Empty array locks all plugin installs. Baseline keeps the vendor default marketplace. |
| `allowedMcpServers` | omitted | GitHub Copilot MCP URL | `[]` | Empty array allows built-in servers only. Omit the key to allow all except deny. |
| `deniedMcpServers` | filesystem MCP at `/` | filesystem MCP at `/` | filesystem MCP at `/` | Same concrete disk-exfil block in every tier. |
| `sandbox.enabled` | omitted | `true` | `true` | CLI sandbox floor for enterprise. Baseline leaves it optional. |
| `sandbox.allowBypass` | omitted | `false` | `false` | Model cannot request unsandboxed commands. |
| `sandbox.gitAuth` / `ghAuth` / `allowDevToolAccess` | omitted | omitted | `false` | Strict blocks token injection and registry caches. |
| `remoteControl.mode` | omitted | `requireSSO` | `disabled` | Strict blocks device-side remote control. Moderate requires SSO. |
| Org policy MCP availability (companion) | often enabled | enabled | disabled | AI Controls kill switch is separate. Strict can disable MCP entirely. |

---

## 4. Deployment Steps

### 4.1 File paths

| OS | File-based `managed-settings.json` | Native MDM |
|----|--------------------------------------|------------|
| macOS | `/Library/Application Support/GitHubCopilot/managed-settings.json` | Forced preferences, domain `com.github.copilot`, values are strings |
| Windows | `%ProgramFiles%\GitHubCopilot\managed-settings.json` | `REG_SZ` values under `HKLM\SOFTWARE\Policies\GitHubCopilot` |
| Linux | `/etc/github-copilot/managed-settings.json` | Not supported. Use the file path. Copilot CLI requires a regular file owned by root, not a symlink, not group- or world-writable. |

Server-managed path (all OS, after sign-in): source org `.github-private` repo, file `copilot/managed-settings.json` on the default branch.

Precedence: MDM, then server-managed, then file-based, then user settings. Copilot CLI `sandbox` is the exception: managed sandbox values combine in the most restrictive direction.

### 4.2 MDM payload guidance

Native MDM does not drop a JSON file. It sets one string per key. Nested keys use dots. Booleans, arrays, and objects are JSON text inside the string.

| MDM key | Moderate string value |
|---------|------------------------|
| `permissions.disableBypassPermissionsMode` | `disable` |
| `sandbox.enabled` | `true` |
| `sandbox.allowBypass` | `false` |
| `allowedMcpServers` | `[{"serverUrl":"https://api.githubcopilot.com/*"}]` |
| `deniedMcpServers` | `[{"serverCommand":["npx","-y","@modelcontextprotocol/server-filesystem","/"]}]` |
| `strictKnownMarketplaces` | `[{"source":"github","repo":"YOUR-ORG/YOUR-PLUGIN-MARKETPLACE"}]` |
| `remoteControl.mode` | `requireSSO` |

**Jamf (macOS):** Custom Settings payload, preference domain `com.github.copilot`, keys as strings.

**Intune (Windows):** Administrative template or OMA-URI / Win32 registry payload writing `REG_SZ` under `HKLM\SOFTWARE\Policies\GitHubCopilot`.

**Workspace ONE:** Profile with the same domain (macOS) or registry path (Windows).

Clients refresh about hourly. In VS Code, run `Developer: Sync Account Policy` during testing.

### 4.3 Validation

```bash
# Server-managed: confirm the file is on the default branch
gh api repos/YOUR-ORG/.github-private/contents/copilot/managed-settings.json \
  --jq .sha

# After restart or re-sign-in:
# VS Code: Command Palette -> Developer: Sync Account Policy
# Then try to add an MCP server that is not on the allowlist.
# Expected: client blocks it. Built-in GitHub MCP still runs.

# Copilot CLI: confirm YOLO is suppressed
copilot --yolo
# Expected: startup ignores bypass flags when disableBypassPermissionsMode is disable.

# Linux file-based permissions
ls -l /etc/github-copilot/managed-settings.json
# Expected: regular file, owner root, not group/world writable, not a symlink
```

Minimum clients for MCP allowlists: GitHub Copilot app, Copilot CLI v1.0.11+, VS Code v1.109.3+. JetBrains, Eclipse, and Xcode are public preview. Copilot cloud agent is unsupported for this key.

### 4.4 Audit logging

**Where logs go:** GitHub organization or enterprise audit log.

**Ship to SIEM:** stream the audit log to S3, Azure Event Hubs, GCS, Splunk, or Datadog, or poll:

```bash
gh api \
  -H "Accept: application/vnd.github+json" \
  "/orgs/YOUR_ORG/audit-log?phrase=action:copilot&per_page=100" \
  --paginate
```

**Alert on:**
- `copilot.policy_changed` (AI Controls toggles)
- `copilot.content_exclusion_changed`
- Changes to `.github-private` `copilot/managed-settings.json` (protect the default branch, require review)
- Copilot cloud agent session start while MCP allowlists are in force (coverage gap)

---

## 5. Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent |
|-------------------|------|-----------------|
| Public MCP server not on the allowlist | Unreviewed tools and data exfil | File an exception with `serverUrl` (remote) or exact `serverCommand` (local). Download, inspect, then request add. |
| `serverName` allow entry | Users can rename servers | Never use `serverName` for enforcement. |
| Awesome Copilot / random marketplace plugin | Plugin can ship an MCP server | Add the plugin to the org marketplace after review, then set `enabledPlugins` to `true` if it must be default. |
| `--yolo` / Allow all | Unattended shell, path, and URL access | Approve each tool. For repetitive low-risk tools, request a narrower allow, not bypass. |
| Copilot CLI unsandboxed command | Host compromise | Run the command in a local terminal you control, or request a sandbox path grant. |
| Root filesystem MCP | Disk exfil | Use a project-scoped filesystem MCP path, then add that exact `serverCommand` to the allowlist. |
| Cloud agent MCP | Allowlist not enforced | Keep cloud agent disabled or limited. Do not use cloud agent as an MCP bypass. |

### False-positive friction

| Setting | Common friction | How to handle exceptions |
|---------|-----------------|--------------------------|
| `allowedMcpServers` with only the GitHub URL | Playwright, internal APIs, and stdio servers stop | Add one matcher per server. Prefer `serverUrl` or `serverCommand`. Expire exceptions in 90 days. |
| `strictKnownMarketplaces` placeholder repo | Plugin UI shows nothing | Publish the marketplace before Phase 2, or omit both marketplace keys until it exists. |
| `sandbox.allowDevToolAccess: false` (Strict) | npm/pip restore fails in CLI | Grant specific cache paths. Do not set the flag back to `true` for the whole org. |
| Malformed JSON | Client treats allowlist as empty and blocks all non-built-in MCP | Validate JSON in CI before merge. Failed policy fails closed. |

### Tool overlap

Claude Code, Cursor, and Copilot can each run MCP servers and a shell.

| Concern | Guidance |
|---------|----------|
| Double MCP config | An allowlisted Copilot MCP server is not automatically allowed in Claude Code or Cursor. Copy the same server identity into Claude Code `allowedMcpServers` / managed MCP and keep Cursor `mcpAllowlist` empty (prompt every tool). |
| Double shell | Copilot CLI sandbox does not bind Cursor terminal allowlists or Claude Code Bash rules. Configure each tool. Do not weaken one because another looks covered. |
| Cloud agent gap | Only Copilot cloud agent skips this MCP allowlist. Keep it limited in org policy. Claude Code remote control and Cursor cloud agents are separate kill switches. |

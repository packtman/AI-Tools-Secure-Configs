# AI Coding Tools: Enterprise Rollout Engineering Guide

**Tools:** Claude Code + Cursor + GitHub Copilot
**Tier:** Moderate (Enterprise)
**Environment:** Standard enterprise, mixed OS (macOS/Windows/Linux), MDM available (Jamf + Intune), SIEM available
**Constraints:** Must allow `pnpm`, must block `.env` reads, no MCP auto-approval

---

## Glossary (First-Time Definitions)

| Term | Definition |
|------|-----------|
| **MDM** | Mobile Device Management: software that pushes configuration profiles and policies to managed endpoints (Jamf for macOS, Intune for Windows). |
| **SIEM** | Security Information and Event Management: centralized log analysis platform (Splunk, Sentinel, Elastic) that aggregates security events and triggers alerts. |
| **MCP** | Model Context Protocol: a standard that lets AI tools connect to external data sources (databases, APIs, file servers) through "MCP servers." |
| **Managed settings** | Configuration files deployed by IT that override user preferences. Users cannot weaken these settings. |
| **Sandbox** | OS-level isolation that restricts what an AI tool's shell commands can access on the filesystem and network, even if the tool itself is tricked. |
| **Content exclusion** | Rules telling an AI tool to ignore specific files (secrets, keys, credentials) so they are never sent to the AI model. |
| **Workspace trust** | A feature in Cursor/VS Code that treats newly opened folders as untrusted until the user explicitly approves them, preventing malicious repo files from auto-executing. |
| **Bypass mode** | A Claude Code flag (`--dangerously-skip-permissions`) that skips all permission prompts, giving the AI agent unrestricted access. |
| **Deep link** | A URL scheme (like `cursor://` or `vscode://`) that can trigger IDE actions when clicked, potentially from untrusted sources. |

---

## 1. ROLLOUT PLAN

### 1.1 Phased Rollout

#### Phase 1: Pilot Group (5-10 developers, 2 weeks)

**Who:** Select developers from 2-3 teams who represent different stacks (frontend/backend/infra). Include at least one developer who is skeptical of AI tools and one power user.

**What to deploy:**
- Claude Code managed-settings-moderate.json to pilot endpoints
- Cursor permissions-moderate.json + settings.json to pilot endpoints
- GitHub Copilot org policy (Moderate) scoped to a pilot team

**Exit criteria to proceed:**
- [ ] Zero security incidents (no credential exposure, no unauthorized network access)
- [ ] Fewer than 3 workflow-blocking issues per developer per week (track via a shared channel)
- [ ] All SIEM ingest pipelines confirmed working (Claude Code audit hooks, GitHub Copilot audit log, Cursor telemetry)
- [ ] Rollback tested: at least one endpoint reverted and confirmed functional
- [ ] Developer satisfaction survey: at least 60% rate the config as "manageable" or better

#### Phase 2: Expanded Pilot (25-50 developers, 2 weeks)

**Who:** Expand to all engineering teams, but exclude CI/CD systems and shared servers.

**What to deploy:**
- Same configs as Phase 1
- Add audit hook scripts to all repos (PostToolUse secret scanning, PreToolUse destructive-command blocking)
- Deploy `.github/copilot-instructions.md` to all active repositories

**Exit criteria to proceed:**
- [ ] All Phase 1 criteria still met at larger scale
- [ ] Exception request process tested: at least 2 exception requests filed and resolved
- [ ] No increase in developer support tickets beyond 20% above baseline
- [ ] SIEM dashboards reviewed by security team and confirmed actionable
- [ ] All OS variants (macOS, Windows, Linux) confirmed working

#### Phase 3: Org-Wide (all developers)

**Who:** All developers, all endpoints.

**What to deploy:**
- Full config deployment via MDM (Jamf for macOS, Intune for Windows, onboarding script for Linux)
- Firewall rules for GitHub Copilot (block `*.individual.githubcopilot.com`)
- Content exclusion at GitHub organization level

**Ongoing:**
- Quarterly review of deny rules and content exclusion patterns
- Monthly SIEM alert tuning
- Annual tier reassessment (should we move to Strict or relax to Baseline?)

---

### 1.2 Pre-Rollout Checklist

| # | Item | Owner | Status |
|---|------|-------|--------|
| 1 | MDM path verified: Jamf can push to `/Library/Application Support/ClaudeCode/` on macOS | IT Ops | [ ] |
| 2 | MDM path verified: Intune can write to `HKLM\SOFTWARE\Policies\ClaudeCode` and `HKLM\SOFTWARE\Policies\Cursor` on Windows | IT Ops | [ ] |
| 3 | Secrets manager in place: no API keys in config files, all reference `${ENV_VAR}` or secrets manager paths | Security | [ ] |
| 4 | SIEM ingest tested: Claude Code audit hook logs arrive in SIEM within 5 minutes | Security | [ ] |
| 5 | SIEM ingest tested: GitHub Copilot audit log events appear via API polling or webhook | Security | [ ] |
| 6 | Rollback plan documented and tested on at least one endpoint per OS | IT Ops | [ ] |
| 7 | Developer communication drafted: "what changes, what breaks, how to get help" (see Section 1.3) | Engineering Manager | [ ] |
| 8 | Exception request process defined: form/channel, SLA, approval chain | Security | [ ] |
| 9 | Claude.ai org UUID obtained and verified (`forceLoginOrgUUID`) | IT Ops | [ ] |
| 10 | Cursor team ID obtained and verified (`AllowedTeamId`) | IT Ops | [ ] |
| 11 | GitHub Copilot Enterprise/Business seats provisioned for pilot teams | IT Ops | [ ] |
| 12 | Firewall rules drafted for Copilot hostname blocking (not yet applied) | Network | [ ] |
| 13 | Linux onboarding script tested on Ubuntu, Fedora, and any other distros in use | IT Ops | [ ] |
| 14 | Minimum tool versions enforced: Claude Code >= 2.1.38, Copilot Chat >= 0.17 | IT Ops | [ ] |

---

### 1.3 "What Will Break" Section

The following developer workflows will be affected by the Moderate tier. Send this message to developers BEFORE rollout.

---

**DEVELOPER COMMUNICATION TEMPLATE:**

Subject: AI Coding Tools Security Configuration -- What Changes on [DATE]

Hi team,

Starting [DATE], we are rolling out security configurations for Claude Code, Cursor, and GitHub Copilot. These settings protect our code and credentials while keeping your core workflows intact.

**What changes:**

1. **Claude Code**: Write, edit, and shell commands now require your approval before running. You will see a prompt asking "Allow this action?" Read-only operations (searching, reading files, listing directories) still run automatically.

2. **Cursor**: Only safe, read-only terminal commands auto-run (like `git status`, `npm test`, `npm run lint`). Other commands will ask for your approval. Build commands like `npm run build` and `go test` are included in the allowlist.

3. **GitHub Copilot**: Web/Bing search is disabled in Copilot Chat. Content exclusion rules now prevent Copilot from reading `.env` files, secrets directories, and cryptographic keys. Completions are disabled for `.ini` and `.properties` files.

**What will feel different:**
- You will be prompted more often when Claude Code wants to run shell commands or edit files. This is intentional.
- `curl | bash` install patterns are blocked. Download scripts first, review them, then run them.
- `.env` files are hidden from AI tools. Use environment variables via your secrets manager instead.
- Copilot CLI (`gh copilot suggest`) is disabled.

**What is NOT affected:**
- All standard build/test/lint commands work normally
- Git operations work normally
- Package managers (`npm`, `pnpm`, `pip`, `cargo`, `go`) work normally
- Reading source code, searching, and navigating all work normally

**Need help?** Post in #ai-tools-support. If a specific command is blocked and you believe it should be allowed, file an exception request at [LINK].

---

### 1.4 Rollback Procedure

#### Claude Code Rollback

| OS | Action |
|----|--------|
| macOS | Remove `/Library/Application Support/ClaudeCode/managed-settings.json` and any files in `managed-settings.d/` |
| Linux | Remove `/etc/claude-code/managed-settings.json` and any files in `managed-settings.d/` |
| Windows | Delete registry key `HKLM\SOFTWARE\Policies\ClaudeCode` or remove `C:\Program Files\ClaudeCode\managed-settings.json` |

Restart Claude Code after removal. Settings revert to user/project defaults immediately.

If using server-managed settings (Admin Console): navigate to Claude.ai Admin Settings, remove or reset the managed settings JSON. Changes propagate on next CLI startup.

#### Cursor Rollback

| OS | Action |
|----|--------|
| macOS | Remove Jamf configuration profile for domain `com.todesktop.230313mzl4w4u92` |
| Windows | Delete registry key `HKLM\SOFTWARE\Policies\Cursor` |
| Linux | Remove `~/.cursor/policy.json` |

For settings.json changes: revert the `.vscode/settings.json` or user-level settings file to the previous version (keep a backup before deployment).

For permissions.json: remove `~/.cursor/permissions.json` to revert to defaults.

#### GitHub Copilot Rollback

| Control | Revert Action |
|---------|---------------|
| Feature policies | Organization Settings -> Copilot -> Policies: re-enable disabled features |
| Content exclusion | Organization Settings -> Copilot -> Content exclusion: remove added patterns |
| Firewall rules | Remove the block on `*.individual.githubcopilot.com` from firewall/proxy |
| Seat management | Switch from `selected_teams` back to `all_members` if needed |

#### Communication Template for Rollback

Subject: AI Tools Config Rolled Back -- Action Required

Hi team,

We have reverted the AI coding tool security configurations as of [DATE/TIME]. Your tools should now behave as they did before [ROLLOUT_DATE]. If you are still experiencing issues, restart your IDE and Claude Code CLI. Contact #ai-tools-support if problems persist.

We will communicate next steps and a revised rollout timeline within [X] business days.

---

## 2. CONFIG FILES

### Important Notes
- All JSON config files below use JSONC format (`// comments`) for documentation
- Deploy the file with comments stripped, OR use a deployment script that strips `//` comments
- A parallel `.comments.md` file accompanies each JSON config for audit purposes
- No secrets, tokens, or API keys appear in any file. Placeholders reference env vars or secrets manager paths.
- The abbreviation "em dash" is avoided throughout; commas, colons, and parentheses are used instead.

---

### 2.1 Claude Code: `managed-settings-moderate.json`

See file: [`rollout-guide/configs/claude-code/managed-settings-moderate.jsonc`](configs/claude-code/managed-settings-moderate.jsonc)

### 2.2 Claude Code: `managed-settings-moderate.comments.md`

See file: [`rollout-guide/configs/claude-code/managed-settings-moderate.comments.md`](configs/claude-code/managed-settings-moderate.comments.md)

### 2.3 Cursor: `permissions-moderate.json`

See file: [`rollout-guide/configs/cursor/permissions-moderate.jsonc`](configs/cursor/permissions-moderate.jsonc)

### 2.4 Cursor: `settings.json`

See file: [`rollout-guide/configs/cursor/settings.jsonc`](configs/cursor/settings.jsonc)

### 2.5 GitHub Copilot: `org-policy-moderate.json`

See file: [`rollout-guide/configs/github-copilot/org-policy-moderate.jsonc`](configs/github-copilot/org-policy-moderate.jsonc)

### 2.6 GitHub Copilot: `.github/copilot-instructions.md`

See file: [`rollout-guide/configs/github-copilot/copilot-instructions.md`](configs/github-copilot/copilot-instructions.md)

---

## 3. TIER DELTA TABLE

### 3.1 Claude Code

| Setting | Baseline | Moderate | Strict | Reason for Difference |
|---------|----------|----------|--------|----------------------|
| `permissions.allow` | Read, Grep, Glob, LS, Diff, Write, Edit, MultiEdit, WebFetch | Read, Grep, Glob, LS, Diff | Read, Grep, Glob, LS | Strict removes Diff from auto-allow; Moderate removes write/exec tools from auto-allow |
| `permissions.ask` | Bash, mcp__* | Write, Edit, MultiEdit, Bash, WebFetch, mcp__* | Diff, Write, Edit, MultiEdit, Bash, WebFetch | Strict has no MCP in ask (all denied); Moderate requires approval for writes |
| `permissions.deny` (shell patterns) | curl\|bash, rm -rf, sudo, eval, nc, python -m http.server | Same + chmod 777, exec, nohup, python -c, node -e | Same + ALL curl, ALL wget, ALL rm, ALL chmod, ALL chown, setsid, ruby -e, perl -e, php -r | Strict blocks entire command families, not just dangerous arguments |
| `permissions.deny` (read patterns) | .env, *.pem, *.key, ~/.ssh, ~/.aws, ~/.gnupg, /etc/shadow | Same + credentials*, ~/.config/gcloud, ~/.azure, ~/.kube, ~/.docker, ~/.npmrc, ~/.netrc, ~/.git-credentials, /etc/passwd | Same + *.jks, *.keystore, *secret*, *token*, ~/.pypirc, /etc/sudoers, /etc/ssl/private | Each tier adds more credential file patterns |
| `disableBypassPermissionsMode` | Not set | `"disable"` | `"disable"` | Moderate and Strict both block the dangerous skip-permissions flag |
| `allowManagedPermissionRulesOnly` | `false` | `false` | `true` | Strict prevents any user/project override of permission rules |
| `disableAutoMode` | `"allow"` | `"disable"` | `"disable"` | Moderate disables auto mode (research preview, unreliable safety classifier) |
| `allowManagedHooksOnly` | `false` | `false` | `true` | Strict locks hooks to IT-deployed only |
| `allowManagedMcpServersOnly` | `false` | `false` | `true` | Strict locks MCP to IT-approved servers only |
| `forceRemoteSettingsRefresh` | Not set | Not set | `true` | Strict fails-closed if managed settings cannot be fetched |
| `disableRemoteControl` | `false` | `true` | `true` | Both Moderate and Strict block external prompt injection via remote control |
| `sandbox.enabled` | Not set | `true` | `true` | OS-level isolation in both enterprise tiers |
| `sandbox.autoAllowBashIfSandboxed` | Not set | `true` | `false` | Moderate auto-approves sandboxed commands for productivity; Strict still requires approval |
| `sandbox.failIfUnavailable` | Not set | `false` | `true` | Strict refuses to run if sandbox cannot start |
| `sandbox.network.allowManagedDomainsOnly` | Not set | `false` (users approve new domains) | `true` | Strict locks network egress to managed allowlist |
| `autoMemoryEnabled` | Not set | Not set | `false` (disabled) | Strict prevents persistent AI memory across sessions |
| `forceLoginMethod` | Not set | `"claudeai"` | `"claudeai"` | Enterprise tiers force org-managed login |
| `forceLoginOrgUUID` | Not set | Set to org UUID | Set to org UUID | Prevents personal account usage |

### 3.2 Cursor

| Setting | Baseline | Moderate | Strict | Reason for Difference |
|---------|----------|----------|--------|----------------------|
| `terminalAllowlist` length | ~48 commands (build, install, dev server included) | ~35 commands (read-only + test/lint/build) | ~15 commands (read-only + git status/diff/log only) | Each tier removes more auto-approved commands |
| `npm install` / `pip install` / `docker` in allowlist | Yes | No | No | Moderate requires approval for package installs (supply chain risk) |
| `npm run dev` / `npm run build` in allowlist | Yes | `npm run build` yes, `npm run dev` no | No | Strict requires approval for all non-trivial commands |
| `mcpAllowlist` | Empty (all MCP prompts) | Empty (all MCP prompts) | Empty (all MCP prompts) | Cursor MCP approval is always prompted; allowlist would auto-approve |
| `workspace.trust.enabled` | `true` | `true` (MDM enforced) | `true` (MDM enforced) | All tiers enable; Moderate/Strict enforce via MDM so users cannot disable |
| `workspace.trust.startupPrompt` | `"once"` | `"always"` | `"always"` | Enterprise tiers force trust decision every session |
| `extensions.autoUpdate` | Not set | `false` | `false` | Prevents unreviewed extension updates |
| `AllowedTeamId` (MDM) | Not set | Set to team ID | Set to team ID | Locks login to managed team |

### 3.3 GitHub Copilot

| Setting | Baseline | Moderate | Strict | Reason for Difference |
|---------|----------|----------|--------|----------------------|
| `seat_management.assignment` | `all_members` | `selected_teams` | `selected_teams` | Enterprise tiers restrict to approved teams |
| `auto_assign_new_members` | `true` | `false` | `false` | Enterprise tiers require explicit provisioning |
| `copilot_cli` | `enabled` | `disabled` | `disabled` | CLI generates shell commands; risk on shared systems |
| `copilot_chat_on_github` | `enabled` | `enabled` | `disabled` | Strict limits AI interaction surfaces |
| `copilot_code_review` | `enabled` | `enabled` | `disabled` | Strict disables to reduce data exposure surface |
| `copilot_pull_request_summaries` | `enabled` | `enabled` | `disabled` | Strict limits AI processing of code diffs |
| `copilot_web_search` | `disabled` | `disabled` | `disabled` | All tiers block (data leakage to search APIs) |
| `copilot_bing_search` | `disabled` | `disabled` | `disabled` | All tiers block (data leakage to Bing) |
| Content exclusion patterns | 5 patterns (.env, secrets, .pem, .key) | 8 patterns (+ credentials, terraform state/vars) | 20 patterns (+ .p12, .pfx, .jks, token, secret, Dockerfiles, .aws, .ssh, .kube, helm values) | Each tier adds more sensitive file patterns |
| `excluded_repositories` | None | 3 sensitive repos | 5+ sensitive repos | Strict excludes more repos from AI processing |
| `block_individual_traffic` | `true` | `true` | `true` | All tiers block shadow AI via personal accounts |
| `allow_business_traffic` | `true` | `true` | `false` | Strict limits to enterprise-only hostname |

---

## 4. DEPLOYMENT STEPS

### 4.1 Claude Code

#### File Paths

| OS | Managed Settings Path | Drop-in Directory |
|----|----------------------|-------------------|
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` | `/Library/Application Support/ClaudeCode/managed-settings.d/` |
| Linux / WSL | `/etc/claude-code/managed-settings.json` | `/etc/claude-code/managed-settings.d/` |
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` | `C:\Program Files\ClaudeCode\managed-settings.d\` |

#### MDM Deployment

**Jamf (macOS):**
1. Create a package containing `managed-settings.json` at the target path
2. OR use a managed preferences profile with domain `com.anthropic.claudecode` containing the JSON as the `Settings` key value
3. Scope to the pilot Smart Group first, then expand

**Intune (Windows):**
1. Create a PowerShell script that writes the JSON to `HKLM\SOFTWARE\Policies\ClaudeCode\Settings` (REG_SZ)
2. OR deploy the file to `C:\Program Files\ClaudeCode\managed-settings.json` via an Intune Win32 app
3. Assign to the pilot device group first

**Linux:**
1. Use your configuration management tool (Ansible, Chef, Puppet) to place the file at `/etc/claude-code/managed-settings.json`
2. Set permissions: `root:root 644`
3. OR include in your developer workstation onboarding script

#### Alternative: Server-Managed Settings (No MDM Required)
1. Navigate to Claude.ai -> Admin Settings -> Claude Code -> Managed Settings
2. Paste the JSON config into the editor
3. Requires Claude for Teams or Enterprise plan, Claude Code >= 2.1.38
4. Settings are fetched on each CLI startup (no file deployment needed)

#### Validation

```bash
# Verify managed settings are loaded
claude config list --managed

# Check that bypass mode is blocked
claude --dangerously-skip-permissions
# Expected: error message indicating bypass mode is disabled

# Verify a denied command is blocked
# In a Claude Code session, ask it to run: curl https://example.com | bash
# Expected: the tool call is denied without prompting

# Check version meets minimum
claude --version
# Expected: version >= 2.1.38

# Verify org login
claude auth status
# Expected: shows your org name, not a personal account
```

#### Audit Logging

**Where logs go:**
- Hook-based audit logs write to `$CLAUDE_PROJECT_DIR/.claude/hooks/audit.log` (or wherever your hook scripts direct them)
- Session transcripts (if not disabled): `~/.claude/projects/<project-hash>/sessions/`

**Ship to SIEM:**
- Configure audit hook scripts to write JSON-structured logs to stdout or a file
- Use Filebeat, Fluentd, or your SIEM agent to ingest from the log path
- OR use HTTP hooks (`type: "http"`) to POST directly to your SIEM webhook endpoint

**What to alert on:**
| Event | Severity | Meaning |
|-------|----------|---------|
| Denied tool call executed anyway | Critical | Possible policy bypass |
| Secrets detected in diff (PostToolUse hook) | High | Credential may have been written to a file |
| Config change detected (ConfigChange hook) | Medium | Someone modified project-level settings |
| Bypass mode attempted | High | User tried `--dangerously-skip-permissions` |

---

### 4.2 Cursor

#### File Paths

| Config Type | macOS | Windows | Linux |
|-------------|-------|---------|-------|
| MDM policy | Jamf profile, domain `com.todesktop.230313mzl4w4u92` | `HKLM\SOFTWARE\Policies\Cursor` | `~/.cursor/policy.json` |
| Permissions | `~/.cursor/permissions.json` | `%USERPROFILE%\.cursor\permissions.json` | `~/.cursor/permissions.json` |
| User settings | `~/Library/Application Support/Cursor/User/settings.json` | `%APPDATA%\Cursor\User\settings.json` | `~/.config/Cursor/User/settings.json` |
| Workspace settings | `<project>/.vscode/settings.json` | `<project>\.vscode\settings.json` | `<project>/.vscode/settings.json` |
| Cursor rules | `<project>/.cursor/rules/security.mdc` | Same | Same |

#### MDM Deployment

**Jamf (macOS):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>AllowedTeamId</key>
  <string>REPLACE_WITH_YOUR_TEAM_ID</string>
  <key>WorkspaceTrustEnabled</key>
  <true/>
  <key>UpdateMode</key>
  <string>manual</string>
</dict>
</plist>
```
Deploy as a configuration profile with domain `com.todesktop.230313mzl4w4u92`.

**Intune (Windows):**
```powershell
$regPath = "HKLM:\SOFTWARE\Policies\Cursor"
if (-not (Test-Path $regPath)) {
    New-Item -Path $regPath -Force | Out-Null
}
Set-ItemProperty -Path $regPath -Name "AllowedTeamId" -Value "REPLACE_WITH_YOUR_TEAM_ID" -Type String
Set-ItemProperty -Path $regPath -Name "WorkspaceTrustEnabled" -Value 1 -Type DWord
Set-ItemProperty -Path $regPath -Name "UpdateMode" -Value "manual" -Type String
```

**Linux (onboarding script):**
```bash
mkdir -p ~/.cursor
cat > ~/.cursor/policy.json << 'POLICY_EOF'
{
  "AllowedTeamId": "REPLACE_WITH_YOUR_TEAM_ID",
  "WorkspaceTrustEnabled": true,
  "UpdateMode": "manual"
}
POLICY_EOF
chmod 644 ~/.cursor/policy.json
```

#### Deploying permissions.json

Cursor does not support MDM-managed permissions. Deploy via:
1. Onboarding script that writes to `~/.cursor/permissions.json`
2. Configuration management (Ansible/Chef/Puppet)
3. Dotfiles repo that developers clone during setup

**Limitation:** Cursor's `permissions.json` is user-writable. A developer can modify it. For compensating controls, enforce workspace trust via MDM (that IS enforceable) and use network egress filtering as a second layer.

#### Deploying settings.json

Two options:
1. **Workspace-level** (recommended): commit `.vscode/settings.json` to each repository. This travels with the code and applies to everyone.
2. **User-level**: deploy to the user settings path via onboarding script. This is a default that repos can override.

#### Deploying Cursor Rules

Commit `.cursor/rules/security.mdc` to each repository. This provides security instructions to Cursor's AI agent.

#### Validation

```bash
# Verify workspace trust is enforced
# Open Cursor, then open a new folder
# Expected: trust prompt appears asking if you trust the folder

# Verify terminal allowlist
# In Cursor Agent mode, ask it to run: rm -rf node_modules
# Expected: Cursor asks for approval (not in allowlist)

# Verify allowed commands run without prompt
# Ask Cursor to run: git status
# Expected: runs immediately without approval prompt

# Check MDM policy is applied (macOS)
defaults read com.todesktop.230313mzl4w4u92 AllowedTeamId
# Expected: your team ID

# Check MDM policy is applied (Windows)
reg query "HKLM\SOFTWARE\Policies\Cursor" /v AllowedTeamId
# Expected: your team ID
```

#### Audit Logging

Cursor does not have built-in audit logging comparable to Claude Code hooks. Compensating controls:
- **Workspace trust events**: monitor via MDM compliance checks
- **Extension installs**: monitor via MDM inventory (Jamf can report installed extensions)
- **Network activity**: use proxy/firewall logs to track Cursor's API calls
- **Git activity**: standard git audit (push logs, branch protection audit log)

---

### 4.3 GitHub Copilot

#### Configuration Paths

GitHub Copilot is configured at three levels, all through the GitHub web interface or API:

| Level | Where to Configure |
|-------|--------------------|
| Enterprise | Enterprise Settings -> Copilot -> Policies |
| Organization | Organization Settings -> Copilot -> Policies & features |
| Repository | Repository Settings -> Code & automation -> Copilot |

There are no local files to deploy for org policy. IDE-level settings go in VS Code/Cursor settings.json (see Section 4.2).

#### MDM Guidance

GitHub Copilot org policies are configured server-side (GitHub.com). MDM is not needed for the org policy itself. However, MDM is useful for:
1. Deploying IDE settings that configure the Copilot extension (proxy, SSL, language enablement)
2. Enforcing minimum Copilot extension versions
3. Blocking the Copilot Individual extension if your org uses Copilot Business/Enterprise

#### Deployment Steps

1. **Enable Copilot Enterprise/Business** at Organization Settings -> Copilot
2. **Set seat management** to `selected_teams`, add your engineering teams
3. **Disable features** per the Moderate policy:
   - Copilot CLI: disabled
   - Web search: disabled
   - Bing search: disabled
   - Docset management: disabled
4. **Configure content exclusion** at Organization Settings -> Copilot -> Content exclusion:
   - Add all patterns from `org-policy-moderate.json` content_exclusions.global_patterns
   - Add sensitive repositories to excluded_repositories
5. **Deploy `.github/copilot-instructions.md`** to all repositories (via script or PR)
6. **Configure firewall rules**:
   ```
   # Allow (HTTPS 443)
   *.enterprise.githubcopilot.com
   *.business.githubcopilot.com
   github.com
   api.github.com
   copilot-proxy.githubusercontent.com

   # Block
   *.individual.githubcopilot.com
   ```
7. **Deploy VS Code/Cursor Copilot settings** via `.vscode/settings.json` in repos

#### Validation

```bash
# Verify org policy via API
gh api /orgs/YOUR_ORG/copilot/billing
# Expected: shows seat count, plan type

# Verify content exclusion
# Open a .env file in VS Code/Cursor with Copilot enabled
# Expected: no completions appear, status bar shows "Content excluded"

# Verify feature policies
gh api /orgs/YOUR_ORG/copilot
# Expected: shows feature toggles matching your policy

# Verify firewall blocking
# On a corporate machine, try to use a personal Copilot account
# Expected: connection fails (*.individual.githubcopilot.com blocked)

# Verify minimum extension version
# In VS Code: Extensions panel -> GitHub Copilot -> check version
# Expected: Copilot Chat >= 0.17
```

#### Audit Logging

**Where logs go:** GitHub audit log (Organization Settings -> Logs -> Audit log)

**Ship to SIEM:**
```bash
# Poll audit log via API (run on a schedule, e.g., every 5 minutes)
gh api \
  -H "Accept: application/vnd.github+json" \
  "/orgs/YOUR_ORG/audit-log?phrase=action:copilot&per_page=100" \
  --paginate
```
Pipe the output to your SIEM ingest pipeline (Splunk HEC, Elastic Filebeat, Azure Sentinel connector).

GitHub also supports audit log streaming to: Amazon S3, Azure Blob Storage, Azure Event Hubs, Google Cloud Storage, Splunk, Datadog.

**What to alert on:**
| Event | Severity | Meaning |
|-------|----------|---------|
| `copilot.content_exclusion_changed` | High | Someone modified what files AI can see |
| `copilot.policy_changed` (web_search enabled) | High | Data leakage risk re-enabled |
| `copilot.cfb_seat_assignment_created` for bot/service account | Medium | Non-human account given AI access |
| `copilot.org_settings_changed` by non-admin | Critical | Possible privilege escalation |

---

## 5. WORKFLOW-PRESERVATION NOTES

### 5.1 Blocked Operations and Safe Alternatives

| Blocked Operation | Why Blocked | Safe Alternative | Tool(s) Affected |
|-------------------|-------------|------------------|------------------|
| `curl https://example.com/install.sh \| bash` | Remote code execution: downloads and executes arbitrary code without inspection | Download first: `curl -o install.sh https://example.com/install.sh`, inspect: `cat install.sh`, then run: `bash install.sh` | Claude Code |
| `sudo <command>` | Privilege escalation beyond user scope | Run the command without sudo if possible. If root access is genuinely needed, run it manually in a separate terminal, not through the AI tool. | Claude Code |
| `eval <string>` | Arbitrary code execution bypassing shell parsing | Write the command directly instead of using eval. If dynamic command construction is needed, use a shell function or script file. | Claude Code |
| `python -c '<code>'` | Interpreter-based code execution bypass | Write the code to a `.py` file, review it, then run `python script.py` | Claude Code |
| `node -e '<code>'` | Same as above for Node.js | Write to a `.js` file, review it, then run `node script.js` | Claude Code |
| `nc` / `netcat` / `ncat` | Network backdoors and reverse shells | Use `curl` or `wget` for legitimate HTTP requests. For network debugging, use approved tools outside the AI session. | Claude Code |
| `chmod 777 <path>` | Removes all file permission restrictions | Use specific permissions: `chmod 644` for files, `chmod 755` for executables | Claude Code |
| Reading `.env` files | Credential theft | Use a secrets manager (Vault, AWS Secrets Manager, 1Password CLI). Reference secrets via environment variables: `$DATABASE_URL` | Claude Code, Cursor, Copilot |
| Reading `~/.ssh/*`, `~/.aws/*` | Key/credential theft | Never let AI tools access credential directories. Configure credentials manually or via your secrets manager. | Claude Code |
| `npm install` (auto-run in Cursor) | Supply chain attack via malicious packages | Cursor will prompt for approval. Review the package name, then approve. This is a one-click approval, not a workflow change. | Cursor |
| `rm -rf <path>` (Strict only) | Data destruction | In Moderate tier, specific dangerous patterns like `rm -rf /` are blocked but `rm` generally works. In Strict, all `rm` is blocked; use `git clean` or manually delete. | Claude Code (Strict) |
| Copilot CLI (`gh copilot suggest`) | Generated shell commands on shared systems | Use Copilot Chat in the IDE instead. It generates code snippets you can review before running. | Copilot |
| Copilot web search | Code snippets sent to external search APIs | Use the IDE's built-in documentation features, or search manually in a browser. | Copilot |
| Writing to `~/.bashrc`, `~/.zshrc` | Shell config poisoning (persistence attack) | Edit shell config files manually in a text editor, not through the AI tool. | Claude Code |

### 5.2 Common False-Positive Friction Points

These settings commonly cause developer frustration that is NOT a security issue. Here is how to handle exception requests for each:

| Setting | False-Positive Scenario | How to Handle |
|---------|------------------------|---------------|
| `Bash(python* -c *)` deny | Developer wants Claude Code to run a quick one-liner like `python -c "import sys; print(sys.version)"` | This is blocked because `-c` can execute arbitrary code. The workaround (write to file, run file) is safe. If the team's workflow heavily relies on Python one-liners, consider adding specific safe patterns to the project-level allow list: `Bash(python* -c "import sys*)` |
| `Read(.env)` deny | Developer needs Claude Code to help debug an environment variable issue | The AI tool should never see real credentials. Instead, create a `.env.example` file with placeholder values and let the AI read that. |
| `npm install` not in Cursor allowlist | Developer is annoyed by the approval prompt for every install | This is intentional (supply chain protection). If the team installs packages dozens of times daily, consider adding `npm install` back to the allowlist with a compensating control (lockfile review in CI). File an exception request. |
| `docker build` / `docker compose up` blocked | Developer uses containers frequently | In Moderate tier, these require approval but are not denied. The developer clicks "approve" once. If this is too much friction, add to the Cursor allowlist via exception request. |
| `WebFetch` requires approval (Claude Code) | Developer wants Claude to read documentation URLs | Approval is a single click. If a team needs frequent web access, consider moving WebFetch to the allow list at the project level, with the understanding that it enables data exfiltration if the AI is compromised. |
| Content exclusion on `*.yaml` (Copilot, Strict only) | Copilot stops suggesting in Kubernetes/Helm YAML files | In Moderate tier, YAML completions are enabled. Only `helm/values*.yaml` is excluded in Strict. If you are on Strict and need YAML completions, file an exception to narrow the exclusion to only secret-containing YAML files. |
| Workspace trust prompt every session | Developer opens the same project daily and finds the prompt annoying | This is by design. The prompt takes 1 second. If truly problematic, switch to `"once"` for that team. Never disable workspace trust entirely. |

### 5.3 Exception Request Process

1. Developer submits request via [FORM/CHANNEL] including:
   - Tool name and specific setting to modify
   - Business justification (what workflow is blocked)
   - Proposed change (exact setting value)
   - Risk acceptance: developer acknowledges the security trade-off

2. Security team reviews within 2 business days

3. If approved:
   - For Claude Code: add to project-level `.claude/settings.json` (if `allowManagedPermissionRulesOnly` is false) OR add to managed-settings.d/ drop-in
   - For Cursor: add to permissions.json or .vscode/settings.json
   - For Copilot: modify content exclusion or feature policy at org level

4. Document the exception in your security register with an expiration date (recommend 90 days, then re-review)

### 5.4 Tool Overlap: Claude Code + Cursor Both Run Shell

Both Claude Code and Cursor can execute shell commands in the terminal. This creates potential for double-configuration or gaps:

| Concern | Guidance |
|---------|----------|
| **Double prompting** | If a developer uses Claude Code inside Cursor's terminal, both tools may prompt for the same command. This is redundant but not harmful. The developer sees one prompt from each tool. |
| **Gap: Cursor allowlist vs. Claude Code deny** | A command in Cursor's `terminalAllowlist` (like `npm test`) will auto-run in Cursor, but Claude Code has its own permission system. When Claude Code runs `npm test`, it follows Claude Code's rules (it is in `ask`, so it prompts). These are separate enforcement layers. |
| **Recommendation** | Configure both tools independently. Cursor's allowlist controls what auto-runs in the IDE terminal. Claude Code's permissions control what the Claude agent can do. They are complementary, not redundant. Do not weaken one because the other provides coverage. |
| **MCP servers** | Both tools support MCP servers. If you define MCP servers in both `.mcp.json` (for Claude Code) and Cursor's MCP settings, the same server may be accessible from both tools. Use `allowManagedMcpServersOnly` in Claude Code and an empty `mcpAllowlist` in Cursor to ensure consistent MCP governance. |

# Claude Code Managed Settings (Moderate Tier): Key-by-Key Rationale

This file accompanies the deployable `managed-settings-moderate.json`. Since production JSON cannot contain comments, this document maps each key to its rationale. Keep this alongside the deployed JSON for audit and review purposes.

---

## `permissions.allow`

**Keys:** `Read`, `Grep`, `Glob`, `LS`, `Diff`

**What:** Auto-approve these read-only tools without prompting the user.

**Why (Moderate tier):** These tools cannot modify files, execute commands, or exfiltrate data. Auto-approving them keeps the developer workflow fast. Deny rules still apply (e.g., `Read(./.env)` is still blocked even though `Read` is in the allow list).

**What breaks if removed:** Every file read, search, or directory listing prompts the user. Claude Code becomes unusably slow for basic tasks.

---

## `permissions.ask`

**Keys:** `Write`, `Edit`, `MultiEdit`, `Bash`, `WebFetch`, `mcp__*`

**What:** Require user approval before running these tools.

**Why (Moderate tier):** These tools can modify files, execute commands, or make network requests. The user reviews each action before it runs. In Baseline tier, `Write`, `Edit`, `MultiEdit`, and `WebFetch` are in `allow`. In Strict tier, the same tools are in `ask` but MCP is fully denied.

**What breaks if removed:** These tools would need to be in `allow` (dangerous, no human review) or `deny` (blocks all useful work).

---

## `permissions.deny` (shell patterns)

### `Bash(curl * | bash)`, `Bash(curl * | sh)`, `Bash(wget * | bash)`, `Bash(wget * | sh)`
**Threat:** Remote code execution via piped downloads. Downloads and executes arbitrary code without inspection.

### `Bash(rm -rf /)`, `Bash(rm -rf /*)`, `Bash(rm -rf ~)`, `Bash(rm -rf ~/*)`
**Threat:** System or home directory destruction.

### `Bash(chmod 777 *)`, `Bash(chmod -R 777 *)`
**Threat:** Removes all file permission restrictions, making files world-readable/writable.

### `Bash(sudo *)`, `Bash(su *)`
**Threat:** Privilege escalation beyond user scope.

### `Bash(eval *)`, `Bash(exec *)`
**Threat:** Arbitrary code execution that bypasses shell parsing and pattern matching.

### `Bash(nc *)`, `Bash(ncat *)`, `Bash(netcat *)`
**Threat:** Network backdoors and reverse shells.

### `Bash(python* -c *)`, `Bash(node -e *)`
**Threat:** Interpreter-based code execution that bypasses Bash pattern matching.

### `Bash(python* -m http.server*)`
**Threat:** Unauthorized network listeners that could serve files to attackers.

### `Bash(nohup *)`
**Threat:** Background process persistence. A process that survives after the session ends.

---

## `permissions.deny` (file read patterns)

### `.env` and credentials files
**Patterns:** `Read(./.env)`, `Read(./.env.*)`, `Read(./secrets/**)`, `Read(./**/*.pem)`, `Read(./**/*.key)`, `Read(./**/*.p12)`, `Read(./**/*.pfx)`, `Read(./**/credentials*)`

**Threat:** Credential theft. These files commonly contain API keys, database passwords, TLS private keys, and service tokens.

### Home directory credential stores
**Patterns:** `Read(~/.ssh/**)`, `Read(~/.aws/**)`, `Read(~/.config/gcloud/**)`, `Read(~/.azure/**)`, `Read(~/.kube/config)`, `Read(~/.docker/config.json)`, `Read(~/.npmrc)`, `Read(~/.gnupg/**)`, `Read(~/.netrc)`, `Read(~/.git-credentials)`

**Threat:** SSH key theft, cloud credential theft, package registry token theft, GPG key theft. These directories contain credentials for infrastructure access.

### System files
**Patterns:** `Read(//etc/shadow)`, `Read(//etc/passwd)`

**Threat:** System account enumeration and password hash theft.

---

## `permissions.deny` (file write patterns)

### Credential stores
**Patterns:** `Write(~/.ssh/**)`, `Write(~/.aws/**)`, `Write(~/.config/gcloud/**)`, `Write(~/.azure/**)`, `Write(~/.kube/**)`, `Write(~/.docker/**)`, `Write(~/.gnupg/**)`

**Threat:** Credential injection or modification. Writing to these directories could plant attacker-controlled keys.

### Shell configuration
**Patterns:** `Write(~/.bashrc)`, `Write(~/.zshrc)`, `Write(~/.profile)`

**Threat:** Shell config poisoning. Modifying these files provides persistence: malicious commands run every time the user opens a terminal.

### Secrets files
**Patterns:** `Write(./.env)`, `Write(./.env.*)`, `Write(./secrets/**)`, `Write(./**/*.pem)`, `Write(./**/*.key)`

**Threat:** Credential injection or overwriting existing credentials.

---

## `disableBypassPermissionsMode`

**Value:** `"disable"`

**What:** Prevents `--dangerously-skip-permissions` flag.

**Why:** Bypass mode skips ALL permission prompts. A user in bypass mode has given Claude Code unlimited shell access. This defeats every deny rule above.

**What breaks if removed:** Users can bypass all security controls with a single CLI flag.

---

## `allowManagedPermissionRulesOnly`

**Value:** `false`

**What:** Allows user/project settings to add permission rules alongside managed rules.

**Why (Moderate):** Teams can tighten rules at the project level (add more deny patterns) or add project-specific allow rules (e.g., allow specific build commands). They cannot override managed deny rules.

**Strict difference:** Set to `true`, blocking all user/project permission rules.

---

## `disableAutoMode`

**Value:** `"disable"`

**What:** Prevents activation of "auto mode" (auto-approves tool calls with background safety classifier).

**Why:** Auto mode is a research preview. The classifier may miss dangerous actions. Enterprise environments should require human review for every tool call.

---

## `disableRemoteControl`

**Value:** `true`

**What:** Blocks external tools from sending commands to Claude Code sessions.

**Why:** Remote control could inject prompts from untrusted sources, bypassing the user's review.

---

## `disableDeepLinkRegistration`

**Value:** `"disable"`

**What:** Prevents protocol handler registration for `claude-code://` deep links.

**Why:** Untrusted websites could use deep links to trigger Claude Code actions.

---

## `disableWorkflows`

**Value:** `true`

**What:** Disables dynamic workflows and bundled workflow commands. Equivalent environment control: `CLAUDE_CODE_DISABLE_WORKFLOWS=1`.

**Why (Moderate tier):** Dynamic workflows are a research preview for long-running, parallel agent work. Moderate tier keeps normal Claude Code use available but blocks this higher-autonomy mode until admins have a pilot, usage monitoring, and exception process.

**What breaks if set to true:** Developers cannot use workflow commands, the `workflow` keyword will not trigger runs, and `ultracode` is removed from the effort menu.

**Strict difference:** Also `true`, because Strict blocks research-preview autonomous workflows by default.

**Baseline difference:** `false`, allowing teams to use dynamic workflows after local confirmation prompts.

---

## `forceLoginMethod` / `forceLoginOrgUUID`

**Values:** `"claudeai"` / `"REPLACE_WITH_YOUR_ORG_UUID"`

**What:** Forces authentication through your org's Claude.ai account with SSO.

**Why:** Ensures all usage is under your org's managed identity, billing, and data processing agreement. Prevents personal accounts that bypass managed settings.

**What breaks if wrong:** If `forceLoginOrgUUID` has the wrong UUID, all users are locked out of Claude Code.

---

## `requiredMinimumVersion`

**Value:** `"2.1.212"`

**What:** Refuses to start Claude Code when the installed version is older than the policy floor. Recovery commands such as `claude update`, `claude install`, and `claude doctor` remain available.

**Why (Moderate tier):** Version 2.1.212 introduces automatic MCP backgrounding and `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`. The hard floor ensures the Moderate foreground policy is understood by every active client. The older `minimumVersion` key only prevents updater downgrades and does not block an outdated client from starting.

**What breaks if too high:** Developers cannot start Claude Code until IT deploys an approved version at or above the configured floor. Pilot the version before raising this value.

**What breaks if removed:** Older clients can start without the expected background task behavior or current security fixes.

---

## `sandbox` settings

### `sandbox.enabled: true`
OS-level isolation for Bash commands. Defense-in-depth: the sandbox is enforced by the OS (Seatbelt on macOS, bubblewrap on Linux), not by Claude Code itself.

### `sandbox.autoAllowBashIfSandboxed: true`
Auto-approve sandboxed Bash commands. Reduces prompt fatigue while the sandbox limits blast radius.

### `sandbox.allowUnsandboxedCommands: false`
Prevents the "try without sandbox" escape hatch. A crafted failure could trick users into approving unsandboxed commands.

### `sandbox.failIfUnavailable: false`
In Moderate tier, allow work to continue if the sandbox is unavailable (e.g., missing bubblewrap on a new machine). In Strict tier, this is `true` (fail-closed).

---

## `env` settings

### `CLAUDE_CODE_ENABLE_TELEMETRY: "0"`
Disables telemetry. Data minimization principle.

### `CLAUDE_CODE_DISABLE_AUTO_MEMORY: "1"`
Prevents Claude Code from saving learnings to disk. Reduces risk of sensitive context persisting across sessions.

### `CLAUDE_CODE_MCP_ALLOWLIST_ENV: "1"`

**What:** Starts stdio MCP servers with Claude Code's safe baseline environment plus only the variables explicitly declared in that server's configuration.

**Why (Moderate tier):** A local MCP process does not need every credential exported in the developer's shell. Restricting inheritance reduces the damage from a compromised or overprivileged server.

**What breaks if removed:** Every stdio MCP server can inherit unrelated shell tokens and credentials.

**What breaks if misconfigured:** A server that relied on an inherited variable may fail to start or authenticate. Add only its required variables to the server's `env` configuration, using your secrets manager rather than literal credentials.

**Tier difference:** Baseline, Moderate, and Strict all set this to `"1"` because ambient credential exposure is not required for normal MCP operation.

### `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS: "0"`

**What:** Keeps every MCP tool call in the foreground instead of automatically moving calls longer than two minutes to background tasks. This control applies to Claude Code 2.1.212 and later.

**Why (Moderate tier):** MCP tools can modify external systems. Keeping a long call visible prevents Claude from starting unrelated work while the external operation is still running. Developers can still press Ctrl+B to background a call intentionally.

**What breaks if removed:** Long MCP calls use the vendor default and move to the background after two minutes. The call continues while Claude works on something else, which can create unexpected concurrent side effects.

**What breaks if misconfigured:** A nonzero value is a delay in milliseconds. A very low value backgrounds routine calls almost immediately, while an invalid value can fall back to vendor behavior.

**Strict difference:** Strict sets `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS: "1"` instead, removing explicit and automatic backgrounding for Bash, subagent, and MCP work.

**Baseline difference:** Baseline leaves both variables unset and uses the vendor default, including automatic backgrounding for MCP calls longer than two minutes on Claude Code 2.1.212 or later.

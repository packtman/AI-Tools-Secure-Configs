# Claude Code — Permission Rules Cheatsheet

## Rule Evaluation Order

```
deny  →  ask  →  allow
```

The first matching rule wins. Deny rules are always checked before ask and allow.

---

## Tool Names

| Tool | Description | Default |
|------|------------|---------|
| `Read` | Read file contents | No approval required |
| `Write` | Create or overwrite files | Approval required |
| `Edit` | Edit existing files | Approval required |
| `MultiEdit` | Edit multiple locations in one file | Approval required |
| `Bash` | Execute shell commands | Approval required |
| `Grep` | Search file contents | No approval required |
| `Glob` | Find files by pattern | No approval required |
| `LS` | List directory contents | No approval required |
| `Diff` | Show file differences | No approval required |
| `WebFetch` | Fetch content from URLs | Approval required |
| `mcp__*` | MCP server tools | Approval required |
| `Agent(*)` | Subagent invocations | Depends on agent |

---

## Pattern Syntax

```
Tool                    — matches ALL invocations of the tool
Tool(specifier)         — matches specific argument
Tool(prefix *)          — wildcard with word boundary (space before *)
Tool(prefix*)           — wildcard without boundary
Tool(./path/**)         — recursive wildcard
Tool(//absolute/path)   — absolute filesystem path
Tool(~/home/path)       — home-relative path
```

### Read / Edit path anchors

| Pattern | Matches |
|---------|---------|
| `Read(./.env)` or `Read(.env)` | `.env` at or under current directory |
| `Read(/src/**)` | Files under `src/` relative to project root |
| `Read(~/Documents/*.pdf)` | PDFs in home ~/Documents |
| `Read(//etc/shadow)` | Absolute path `/etc/shadow` |
| `Read(**/.env)` | Any `.env` at any depth (same as `Read(.env)`) |
| `Read(//**/.env)` | Any `.env` anywhere on the filesystem |

### Bash patterns

| Pattern | Matches |
|---------|---------|
| `Bash(npm run build)` | Exact command |
| `Bash(npm run test *)` | Commands starting with `npm run test` (word boundary) |
| `Bash(npm *)` | Any `npm` command |
| `Bash(* --version)` | Any command ending with `--version` |
| `Bash(git * main)` | Git commands targeting main branch |

**Compound commands:** `Bash(safe-cmd *)` does NOT match `safe-cmd && other-cmd`. Each subcommand is matched independently. Shell operators `&&`, `||`, `;`, `|` split compound commands.

---

## Common Deny Patterns

### Dangerous shell operations

```json
"Bash(curl * | bash)",
"Bash(curl * | sh)",
"Bash(wget * | bash)",
"Bash(wget * | sh)",
"Bash(rm -rf /)",
"Bash(rm -rf /*)",
"Bash(rm -rf ~)",
"Bash(chmod 777 *)",
"Bash(chmod -R 777 *)",
"Bash(sudo *)",
"Bash(su *)",
"Bash(eval *)",
"Bash(exec *)",
"Bash(nc *)",
"Bash(ncat *)",
"Bash(netcat *)",
"Bash(nohup *)",
"Bash(setsid *)"
```

### Code execution via interpreters

```json
"Bash(python* -c *)",
"Bash(python* -m http.server*)",
"Bash(node -e *)",
"Bash(ruby -e *)",
"Bash(perl -e *)",
"Bash(php -r *)"
```

### Reading secrets and credentials

```json
"Read(./.env)",
"Read(./.env.*)",
"Read(./secrets/**)",
"Read(./**/*.pem)",
"Read(./**/*.key)",
"Read(./**/*.p12)",
"Read(./**/*.pfx)",
"Read(./**/*.jks)",
"Read(./**/credentials*)",
"Read(./**/token*)",
"Read(~/.ssh/**)",
"Read(~/.aws/**)",
"Read(~/.config/gcloud/**)",
"Read(~/.azure/**)",
"Read(~/.kube/config)",
"Read(~/.docker/config.json)",
"Read(~/.npmrc)",
"Read(~/.pypirc)",
"Read(~/.gnupg/**)",
"Read(~/.netrc)",
"Read(~/.git-credentials)",
"Read(//etc/shadow)",
"Read(//etc/passwd)",
"Read(//etc/sudoers)"
```

### Writing to sensitive locations

```json
"Write(~/.ssh/**)",
"Write(~/.aws/**)",
"Write(~/.config/gcloud/**)",
"Write(~/.azure/**)",
"Write(~/.kube/**)",
"Write(~/.docker/**)",
"Write(~/.gnupg/**)",
"Write(~/.bashrc)",
"Write(~/.zshrc)",
"Write(~/.profile)",
"Write(./.env)",
"Write(./.env.*)",
"Write(./secrets/**)",
"Write(./**/*.pem)",
"Write(./**/*.key)"
```

### MCP tool restrictions

```json
"mcp__filesystem__*",
"mcp__shell__*",
"mcp__*__write*",
"mcp__*__delete*",
"mcp__*__execute*"
```

### Subagent restrictions

```json
"Agent(Explore)",
"Agent(Plan)"
```

---

## Managed-Only Settings

These keys are **only** read from managed settings and have no effect in user/project settings:

| Key | Effect |
|-----|--------|
| `allowedChannelPlugins` | Allowlist of channel plugins |
| `allowManagedHooksOnly` | Block user/project/plugin hooks |
| `allowManagedMcpServersOnly` | Only managed MCP allowlist applies |
| `allowManagedPermissionRulesOnly` | Block user/project permission rules |
| `blockedMarketplaces` | Blocklist of plugin marketplace sources |
| `channelsEnabled` | Enable/disable channels |
| `forceRemoteSettingsRefresh` | Block startup until settings fetched |
| `pluginTrustMessage` | Custom plugin trust warning text |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Only managed `allowRead` applies |
| `sandbox.network.allowManagedDomainsOnly` | Only managed domain allowlist applies |
| `strictKnownMarketplaces` | Restrict plugin marketplace sources |
| `wslInheritsWindowsSettings` | WSL reads Windows managed settings |

## Works from Any Scope (but most useful in managed)

| Key | Effect |
|-----|--------|
| `disableBypassPermissionsMode` | Prevents `--dangerously-skip-permissions` |
| `disableAutoMode` | Prevents auto mode activation |
| `disableRemoteControl` | Blocks remote control feature |
| `disableSkillShellExecution` | Blocks shell execution in skills |
| `disableDeepLinkRegistration` | Prevents protocol handler registration |
| `disableAllHooks` | Disables all hooks (managed hooks require managed-level setting) |

---

## Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Prompts on first use of each tool |
| `acceptEdits` | Auto-accepts file edits and filesystem commands in workspace |
| `plan` | Read-only: reads files and runs read-only shell commands only |
| `auto` | Auto-approves with background safety checks (research preview) |
| `dontAsk` | Auto-denies unless pre-approved via rules |
| `bypassPermissions` | Skips all prompts (ONLY for isolated containers/VMs) |

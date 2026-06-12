# Cline Security Settings — Complete Rationale Guide

This document provides the definitive security reasoning behind every setting in the AI-Secure-Configs Cline configuration. For each setting, it explains what it does, why it matters, the recommended value across three environment tiers, and the consequences of misconfiguration.

## Environment Tiers

| Tier | Description | Risk tolerance |
|------|-------------|----------------|
| **Regulated** | Healthcare, finance, government, defense — subject to HIPAA, SOC 2, FedRAMP, PCI-DSS | Zero tolerance; all controls enforced |
| **Standard Enterprise** | Corporate engineering teams with IP protection requirements | Low tolerance; most controls enforced |
| **Developer** | Startups, open-source contributors, individual developers | Moderate tolerance; security-aware defaults |

---

## 1. Auto-Approval Controls (`alwaysAllow*`)

These six settings are the most security-critical in Cline. They control whether the AI agent can act without human review. Enabling any of them shifts control from the developer to the model.

### 1.1 `cline.alwaysAllowReadOnly`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Cline automatically approves all read-only file operations (reading files, listing directories) without showing an approval dialog. |
| **Why it matters** | Even "read-only" access can expose secrets. A model that can silently enumerate and read files can discover `.env`, `~/.ssh/id_rsa`, `~/.aws/credentials`, private key files, and other sensitive content without any visible action. The approval dialog is the developer's opportunity to see what the AI is doing. |
| **Misconfiguration risk** | With `true`, the AI can silently read any file the developer has access to — including files outside the current project if `alwaysAllowReadOnlyOutsideWorkspace` is also `true`. Sensitive credentials, proprietary code, and personal data can be read and incorporated into AI context without notification. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Every file read must be explicitly approved and auditable |
| Standard Enterprise | `true` (workspace only) | Acceptable for read-only operations within workspace; set `alwaysAllowReadOnlyOutsideWorkspace: false` |
| Developer | `true` | Acceptable for personal workstations; still set `Outside Workspace` to `false` |

### 1.2 `cline.alwaysAllowReadOnlyOutsideWorkspace`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, extends auto-approved read-only access to files outside the current VS Code workspace (e.g., `/etc/passwd`, `~/.ssh/`, `~/Documents/`). |
| **Why it matters** | This is the most dangerous read-only setting. Most credential files, SSH keys, and cloud provider configs live outside the project workspace. Enabling this gives the AI silent access to the entire filesystem within the user's permissions. |
| **Misconfiguration risk** | Combined with `alwaysAllowReadOnly: true`, an AI agent can silently read SSH keys, AWS credentials, database passwords, browser-stored secrets, and any other file accessible to the user account. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Non-negotiable; enforce via MDM |
| Standard Enterprise | `false` | No legitimate use case justifies silent access outside workspace |
| Developer | `false` | Recommended; only override if you understand the implications |

### 1.3 `cline.alwaysAllowWrite`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Cline automatically approves all file write operations (creating, modifying, deleting files) without showing an approval dialog. |
| **Why it matters** | Writes are irreversible without version control. A model that can silently overwrite files can corrupt source code, modify configuration, delete data, or plant malicious content — all without the developer reviewing what was written. |
| **Misconfiguration risk** | With `true`, the AI can silently overwrite any writable file. In a repository, this means unreviewed code changes. On a system, this means modified configs, scripts, and data. Combined with `alwaysAllowExecute`, this becomes arbitrary code execution. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Non-negotiable |
| Standard Enterprise | `false` | Non-negotiable; the diff review step is a critical security gate |
| Developer | `false` | Strongly recommended; even personal workstations benefit from reviewing writes |

### 1.4 `cline.alwaysAllowWriteOutsideWorkspace`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, extends auto-approved writes to files outside the current VS Code workspace. |
| **Why it matters** | This would allow the AI to silently modify shell configuration (`~/.bashrc`, `~/.zshrc`), SSH configs (`~/.ssh/config`), git config (`~/.gitconfig`), and system files — creating persistent backdoors or altering developer behavior. |
| **Misconfiguration risk** | Enables persistent modification of developer environment. An AI writing to `~/.bashrc` can add aliases or PATH entries that execute malicious code on every terminal session. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| All | `false` | Non-negotiable across all environments |

### 1.5 `cline.alwaysAllowExecute`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Cline automatically executes terminal commands without showing an approval dialog. |
| **Why it matters** | This is the most dangerous setting in Cline. Silent command execution means the AI can run any command the user can run — install packages, modify system state, exfiltrate data via curl, or establish network connections — all without developer knowledge. |
| **Misconfiguration risk** | With `true`, Cline is effectively a remote code execution interface controlled by the AI model. Any prompt injection in a file the model reads could trigger arbitrary command execution. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| All | `false` | Non-negotiable across all environments. Use `allowedCommands` for safe commands instead. |

### 1.6 `cline.alwaysAllowBrowser`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, the AI can autonomously browse URLs using the built-in browser tool without approval. |
| **Why it matters** | The browser tool can access internal network addresses (SSRF), exfiltrate data by navigating to attacker-controlled pages, submit forms, and interact with authenticated web apps using the developer's session cookies. |
| **Misconfiguration risk** | Enables server-side request forgery against internal services. An AI browsing internal URLs (e.g., `http://169.254.169.254/latest/meta-data/` for AWS metadata) can leak cloud credentials. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| All | `false` | Non-negotiable. `browserToolEnabled: false` is the additional defense-in-depth control. |

### 1.7 `cline.alwaysAllowMcp`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, all MCP tool calls execute without approval dialogs. |
| **Why it matters** | MCP servers can access external APIs, databases, filesystems, and execute arbitrary code depending on which servers are configured. Blanket auto-approval removes the human check on every tool call. |
| **Misconfiguration risk** | A single compromised MCP server combined with `alwaysAllowMcp: true` gives an attacker (via prompt injection) silent access to every capability exposed by that server. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Non-negotiable |
| Standard Enterprise | `false` | Use `alwaysAllowMcpTools` to allowlist specific safe, read-only MCP tools if needed |
| Developer | `false` | Use `alwaysAllowMcpTools` for specific tools; never blanket-approve |

---

## 2. Terminal Command Allowlist (`cline.allowedCommands`)

### 2.1 `cline.allowedCommands`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Defines a list of terminal commands that can be auto-executed when `alwaysAllowExecute` is `false`. Commands not in this list still require manual approval. |
| **Why it matters** | An explicit allowlist ensures the AI can only run commands the organization has vetted. This is the recommended pattern: keep `alwaysAllowExecute: false` and use `allowedCommands` for safe, read-only or low-risk commands. |
| **Misconfiguration risk** | Adding overly broad patterns (e.g., `npm run *`) defeats the allowlist. Each entry should be a full, specific command. Never add `bash`, `sh`, `python`, `node`, or interpreters to the allowlist — they can run arbitrary code. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `[]` (empty) | All commands require explicit approval |
| Standard Enterprise | Read-only git/test commands | See `settings-moderate.json` for the recommended list |
| Developer | Expanded test/build commands | See `settings-baseline.json` for the recommended list |

**Commands that must never be in the allowlist:**

| Command | Reason |
|---------|--------|
| `bash`, `sh`, `zsh` | Shell interpreter — executes arbitrary commands |
| `python`, `node`, `ruby`, `perl` | Script interpreters — executes arbitrary code |
| `curl`, `wget` | Network access — can download and pipe malicious payloads |
| `sudo` | Privilege escalation |
| `rm`, `rm -rf` | Destructive file deletion |
| `chmod`, `chown` | Permission escalation |
| `ssh`, `scp`, `rsync` | Remote access and data exfiltration |
| `docker run`, `kubectl exec` | Container escape / arbitrary execution |
| `eval`, `exec` | Dynamic code evaluation |
| `crontab` | Persistence mechanism |
| `nc`, `ncat`, `netcat` | Network backdoors |

---

## 3. Browser Tool (`cline.browserToolEnabled`)

| Attribute | Detail |
|-----------|--------|
| **What it does** | Enables or disables the built-in browser automation tool entirely. When `false`, the AI cannot use browser capabilities regardless of approval settings. |
| **Why it matters** | Defense-in-depth against browser-based attacks. Even if `alwaysAllowBrowser` is `false`, a compromised model could attempt to use the browser if it is enabled. Disabling it entirely removes the attack surface. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | Non-negotiable |
| Standard Enterprise | `false` | Disable unless there is a documented use case for browser automation |
| Developer | `false` | Disable by default; enable only for specific browser automation tasks |

---

## 4. Telemetry (`cline.telemetrySetting`)

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls whether usage telemetry is sent to Cline's servers. Values: `"enabled"`, `"disabled"`. |
| **Why it matters** | Telemetry may include session metadata, task descriptions, file names, and error context. In regulated environments, data residency and third-party data sharing requirements prohibit sending any project metadata outside the organization. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `"disabled"` | Non-negotiable under GDPR, HIPAA, FedRAMP |
| Standard Enterprise | `"disabled"` | Default to off; review vendor DPA before enabling |
| Developer | `"disabled"` | Privacy-preserving default |

---

## 5. Checkpoints (`cline.enableCheckpoints`)

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, Cline creates git-based checkpoints (shadow commits) before making changes, allowing easy rollback. |
| **Why it matters** | Checkpoints are the primary recovery mechanism when an AI write goes wrong. Disabling them means file changes are immediately permanent and may be difficult to reverse. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| All | `true` | Always enable; there is no security downside to checkpoints |

---

## 6. API Provider and Model Selection

| Attribute | Detail |
|-----------|--------|
| **What it does** | Configures which LLM provider and model Cline uses for all agent interactions. |
| **Why it matters** | In enterprise settings, the provider must be under contract (DPA, BAA for HIPAA), traffic must route through approved channels, and the model must meet capability/compliance requirements. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | Organization-specific (e.g., Azure OpenAI for FedRAMP, Anthropic Enterprise for HIPAA) | Ensure BAA/DPA is in place with the provider |
| Standard Enterprise | `anthropic` / `claude-sonnet-4-6` or org-approved provider | Route via corporate proxy if required |
| Developer | Personal preference | Still prefer HTTPS; avoid logging sensitive API keys in settings files |

**Never set `cline.apiKey` in a shared settings file or commit it to source control.** Use VS Code's built-in secrets storage (the keychain integration) or set the API key as an environment variable (`ANTHROPIC_API_KEY`) at the OS level.

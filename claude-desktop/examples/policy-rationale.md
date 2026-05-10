# Claude Desktop — Enterprise Policy Rationale

Every setting below explains **what it does**, **why you should care**, and **the recommended value** for different environments.

---

## `isLocalDevMcpEnabled`

**What it does:** Controls whether users can add local MCP (Model Context Protocol) servers in their `claude_desktop_config.json`.

**Why it matters:** MCP servers execute arbitrary commands on the user's machine. A malicious or misconfigured MCP server can read files, exfiltrate data, modify code, or install malware — all with the user's privileges.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated (finance, healthcare) | `false` | Eliminates the entire MCP attack surface. Users cannot add any local tool integrations. |
| Standard enterprise | `false` with pre-deployed config | Block user-added servers but deploy an IT-approved `claude_desktop_config.json` with vetted servers. |
| Developer teams | `true` | Developers need MCP for productivity. Mitigate by auditing configs and training on safe usage. |

---

## `isDesktopExtensionEnabled`

**What it does:** Controls whether Claude Desktop extensions can be installed and used.

**Why it matters:** Extensions run code in the desktop app's context and may access conversation data, files, or network resources. An unvetted extension could exfiltrate prompts/responses or inject malicious instructions.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | Eliminates extension attack surface entirely. |
| Standard enterprise | `false` | Unless specific extensions are required and vetted. |
| Developer teams | `true` | With user education on evaluating extensions. |

---

## `isDesktopExtensionDirectoryEnabled`

**What it does:** Controls whether users can browse and install extensions from the extension directory.

**Why it matters:** The directory makes it easy to discover and install unvetted extensions. Disabling it while keeping `isDesktopExtensionEnabled: true` means only manually-installed (IT-approved) extensions work.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | No extensions at all. |
| Standard enterprise | `false` | Block discovery; allow only pre-approved extensions deployed by IT. |
| Developer teams | `true` | With training on safe extension evaluation. |

---

## `isClaudeCodeForDesktopEnabled`

**What it does:** Controls whether Claude Code (the AI coding agent) can be accessed through Claude Desktop.

**Why it matters:** Claude Code has deep filesystem and shell access. If users don't need coding agent capabilities, disabling this reduces the attack surface significantly.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Non-developer users | `false` | Business users have no need for coding tools. Prevents accidental exposure. |
| Developer teams | `true` | Core functionality. Pair with Claude Code managed-settings.json for governance. |

---

## `secureVmFeaturesEnabled`

**What it does:** Controls whether the Cowork (computer use) feature is available. This allows Claude to interact with applications on the user's machine via a sandboxed VM.

**Why it matters:** Computer use means Claude can see the screen, click buttons, and type. While sandboxed, this is a powerful capability that could be misused via prompt injection to perform unintended actions.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `false` | Computer use is too powerful for high-risk environments. |
| Standard enterprise | `false` | Unless specific computer use workflows are approved. |
| Developer / power user | `true` | With user awareness of prompt injection risks. |

---

## `disableAutoUpdates`

**What it does:** Prevents Claude Desktop from automatically downloading and installing updates.

**Why it matters:** Auto-updates are a double-edged sword. They ensure security patches are applied quickly, but in enterprise environments, IT may need to test updates before deployment.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | IT must test and approve each version before deployment. |
| Standard enterprise | `false` | Auto-updates ensure timely security patches. Pair with `autoUpdaterEnforcementHours`. |
| Developer teams | `false` | Stay current with latest features and fixes. |

---

## `autoUpdaterEnforcementHours`

**What it does:** When an update is downloaded and ready, this controls how many hours before Claude Desktop forces a restart to apply it.

**Why it matters:** Users who defer updates indefinitely remain vulnerable to known security issues. This setting balances user autonomy with timely patching.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `24` | Force updates within 24 hours to minimize exposure window. |
| Standard enterprise | `48` | Gives users reasonable time to save work. |
| Flexible | `72` (default) | Maximum deferral. Acceptable if you have other patching controls. |

---

## Summary: Recommended Profiles

### Maximum Lockdown (Regulated)

```json
{
  "isLocalDevMcpEnabled": false,
  "isDesktopExtensionEnabled": false,
  "isDesktopExtensionDirectoryEnabled": false,
  "isClaudeCodeForDesktopEnabled": false,
  "secureVmFeaturesEnabled": false,
  "disableAutoUpdates": false,
  "autoUpdaterEnforcementHours": 24
}
```

### Standard Enterprise

```json
{
  "isLocalDevMcpEnabled": false,
  "isDesktopExtensionEnabled": false,
  "isDesktopExtensionDirectoryEnabled": false,
  "isClaudeCodeForDesktopEnabled": true,
  "secureVmFeaturesEnabled": false,
  "disableAutoUpdates": false,
  "autoUpdaterEnforcementHours": 48
}
```

### Developer Teams

```json
{
  "isLocalDevMcpEnabled": true,
  "isDesktopExtensionEnabled": true,
  "isDesktopExtensionDirectoryEnabled": false,
  "isClaudeCodeForDesktopEnabled": true,
  "secureVmFeaturesEnabled": true,
  "disableAutoUpdates": false,
  "autoUpdaterEnforcementHours": 72
}
```

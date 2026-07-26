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

## Desktop managed settings (Code tab)

These keys are deployed through Claude Code managed settings (MDM or admin console), not through `claude_desktop_config.json`. The Desktop Code tab honors them. The standalone Claude Code CLI ignores Desktop-only keys such as `sshHostAllowlist`.

### `browserExternalPageTools`

**What it does:** When set to `"disabled"`, Claude cannot use tools to read or act on external pages in the Desktop Browser pane.

**Why it matters:** External pages can contain prompt-injection content that tricks Claude into exfiltrating secrets or performing unsafe actions.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `"disabled"` | Block Claude tool use on external sites. |
| Standard enterprise | `"disabled"` | Users may still navigate; Claude cannot act. |
| Developer teams | unset | Allow Browser tooling for web app testing. |

**What breaks if removed:** Claude can read and act on external sites in the Browser pane, increasing prompt-injection risk.

### `disableBrowserExternalNavigation`

**What it does:** When set to the JSON boolean `true`, neither users nor Claude can navigate to external sites in the Browser pane. Localhost previews still work. The string `"true"` is ignored.

**Why it matters:** Some orgs need a hard stop on any external browsing inside Desktop, even when Browser tools are disabled.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Eliminate external browsing surface. |
| Standard enterprise | `false` | Prefer `browserExternalPageTools: "disabled"` so developers can open docs. |
| Developer teams | unset / `false` | Keep external browsing for debugging. |

**What breaks if misconfigured:** Setting the string `"true"` does nothing. Removing the key re-enables external navigation.

### `disableMobileSimulatorTools`

**What it does:** When `true`, Claude cannot control or capture the iOS Simulator pane. Users can still interact with the simulator themselves.

**Why it matters:** Simulator control can expose app data, screenshots, and device state to the model.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `true` | Block model access to device state. |
| Standard enterprise | `true` | Enable only for approved mobile teams via exception. |
| Developer teams | `false` | Needed for iOS build and test workflows. |

**What breaks if removed:** Claude can drive the iOS Simulator and capture device content.

### `sshHostAllowlist`

**What it does:** Restricts Desktop SSH sessions to hosts whose resolved hostname matches one of the patterns. An empty array disables SSH sessions. Managed settings only.

**Why it matters:** Unrestricted SSH from Desktop can reach any host the endpoint can resolve, including production jump hosts.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Regulated | `[]` | Disable Desktop SSH entirely. |
| Standard enterprise | Approved host patterns only | Example: `["*.devboxes.example.com"]`. |
| Developer teams | unset | Allow ad-hoc SSH; prefer pairing with network controls. |

**What breaks if removed:** Users can open SSH sessions to any reachable host from Desktop. Pair with network or zero-trust controls for a hard boundary. This key does not restrict Bash `ssh` commands.

### Overlap with Claude Code

If you also deploy `claude-code/` managed settings, put Browser, Simulator, and SSH keys in that same managed file. Do not maintain a second conflicting copy only inside `claude_desktop_config.json` (Desktop ignores managed keys there).

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
  "autoUpdaterEnforcementHours": 24,
  "browserExternalPageTools": "disabled",
  "disableBrowserExternalNavigation": true,
  "disableMobileSimulatorTools": true,
  "sshHostAllowlist": []
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
  "autoUpdaterEnforcementHours": 48,
  "browserExternalPageTools": "disabled",
  "disableBrowserExternalNavigation": false,
  "disableMobileSimulatorTools": true,
  "sshHostAllowlist": ["*.devboxes.example.com"]
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
  "autoUpdaterEnforcementHours": 72,
  "disableMobileSimulatorTools": false
}
```

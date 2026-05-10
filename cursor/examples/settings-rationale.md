# Cursor Security Settings — Complete Rationale Guide

This document provides the definitive security reasoning behind every setting in the AI-Secure-Configs Cursor configuration. For each setting, it explains what it does, why it matters, the recommended value across three environment tiers, and the consequences of misconfiguration.

## Environment Tiers

| Tier | Description | Risk tolerance |
|------|-------------|----------------|
| **Regulated** | Healthcare, finance, government, defense — subject to compliance frameworks (HIPAA, SOC 2, FedRAMP, PCI-DSS) | Zero tolerance; all controls enforced |
| **Standard Enterprise** | Typical corporate engineering teams with IP protection requirements | Low tolerance; most controls enforced, some flexibility for productivity |
| **Developer** | Startups, open-source contributors, individual developers | Moderate tolerance; security-aware defaults with opt-out capability |

---

## 1. Workspace Trust

Workspace Trust is the first line of defense against malicious repositories. When a developer clones or opens an untrusted repository, workspace trust prevents automatic execution of tasks, scripts, extensions, and settings defined by that repository.

### 1.1 `security.workspace.trust.enabled`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Enables the Workspace Trust feature globally. When `true`, Cursor treats every newly opened folder as untrusted until the user explicitly grants trust. Untrusted workspaces disable task auto-run, debug configurations, certain extension features, and workspace-defined settings. |
| **Why it matters** | A cloned repository can contain `.vscode/tasks.json`, `.vscode/launch.json`, or `.vscode/settings.json` that execute arbitrary commands on open. Supply-chain attacks increasingly target developer environments through poisoned repos. Without workspace trust, opening a repo is equivalent to running its code. |
| **Misconfiguration risk** | If set to `false`, every opened folder is implicitly trusted. A developer who clones a malicious repo or opens a shared workspace can have arbitrary commands executed immediately — file exfiltration, reverse shells, or credential theft via task auto-run. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `true` (enforce via MDM) | Non-negotiable; enforce with `WorkspaceTrustEnabled` MDM policy so users cannot override |
| Standard Enterprise | `true` | Deploy via settings.json; educate developers on trust prompts |
| Developer | `true` | Default is already `true`; leave enabled |

### 1.2 `security.workspace.trust.startupPrompt`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls whether the trust prompt appears when Cursor starts and opens a folder. Values: `"always"`, `"once"`, `"never"`. |
| **Why it matters** | The startup prompt is the decision point where a user explicitly grants or denies trust. Setting it to `"always"` ensures every session begins with an explicit trust decision, preventing drift where a folder was trusted months ago under different conditions. |
| **Misconfiguration risk** | If set to `"never"`, users are never prompted and folders inherit whatever trust state was last set, or fall through to untrusted silently — leading to confusion and potential workarounds where users pre-trust everything. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `"always"` | Forces conscious trust decision every session |
| Standard Enterprise | `"always"` | Slight friction, but prevents stale trust |
| Developer | `"once"` | Acceptable — prompt once per workspace, then remember |

### 1.3 `security.workspace.trust.banner`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Shows a persistent banner in untrusted workspaces reminding the user that restricted mode is active. Values: `"always"`, `"untrustedRemote"`, `"never"`. |
| **Why it matters** | Visibility of trust state prevents developers from accidentally working in restricted mode (missing tooling) or missing that a workspace is untrusted (false sense of trust). The banner is a passive security indicator — like the padlock icon in a browser. |
| **Misconfiguration risk** | If set to `"never"`, users have no visual indication of trust state. They may not realize extensions are degraded in an untrusted workspace, or worse, assume a workspace is trusted when it is not. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `"always"` | Persistent visual reminder is required |
| Standard Enterprise | `"always"` | Minimal UX cost, high security signal |
| Developer | `"always"` | Recommended; no downside |

### 1.4 `security.workspace.trust.emptyWindow`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls whether an empty Cursor window (no folder opened) is trusted. When `false`, even a blank window runs in restricted mode. |
| **Why it matters** | Empty windows can still run terminal sessions and load extensions. Trusting them by default means any extension or terminal command runs with full permissions even before a folder is opened. An attacker who chains an extension exploit with an auto-start behavior could leverage a trusted empty window. |
| **Misconfiguration risk** | If set to `true`, any action taken in an empty window — installing extensions, running terminal commands, using AI features — runs with full trust. This creates a trust boundary gap. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | No implicit trust, ever |
| Standard Enterprise | `false` | Minimal workflow impact |
| Developer | `true` | Acceptable for convenience; low practical risk for individuals |

---

## 2. Terminal Security

### 2.1 `terminal.integrated.allowedLinkSchemes`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Defines which URL schemes are clickable in the integrated terminal. By default, many schemes are active. Restricting to `["https", "http", "file"]` prevents the terminal from creating clickable links for schemes like `javascript:`, `vscode:`, `cursor:`, `data:`, or custom protocol handlers. |
| **Why it matters** | Terminal output is often uncontrolled — it comes from build tools, test runners, log files, or server output. A malicious dependency or compromised CI log could inject a `vscode://` or `cursor://` deep link that, when clicked, triggers extension installs, settings changes, or workspace trust overrides. Protocol handler attacks are a known vector. |
| **Misconfiguration risk** | If this list includes `vscode:`, `cursor:`, or `data:`, clicking terminal output could trigger IDE actions without the user understanding the consequences — silently installing extensions, opening remote connections, or changing configuration. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `["https"]` | HTTP should redirect to HTTPS; no `file` links needed in regulated environments |
| Standard Enterprise | `["https", "http", "file"]` | Balanced — allows local file links |
| Developer | Default (all schemes) | Convenience over restriction |

### 2.2 `terminal.integrated.enableFileLinks`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls whether file paths in terminal output become clickable links that open in the editor. Values: `"on"`, `"off"`, `"notRemote"`. |
| **Why it matters** | In a compromised or untrusted environment, terminal output could contain crafted file paths designed to open sensitive files (like private keys or credentials) in the editor, where they might then be indexed, cached, or sent to AI context. Disabling this removes an attack surface where terminal output influences editor state. |
| **Misconfiguration risk** | If set to `"on"` in environments that handle sensitive files, a rogue process could output paths to credential files, causing the editor to open and potentially index them for AI features or recent-files lists. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `"off"` | No automatic file opening from terminal output |
| Standard Enterprise | `"off"` | Security benefit outweighs the convenience loss |
| Developer | `"on"` | Useful for clicking through stack traces; acceptable risk |

---

## 3. Port Forwarding

### 3.1 `remote.autoForwardPorts`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When using remote development (SSH, containers, WSL), Cursor detects services listening on ports and automatically forwards them to the local machine. |
| **Why it matters** | Automatic port forwarding can expose internal services to the developer's local network without awareness. In a shared or compromised remote environment, an attacker could start a service on a port, have it auto-forwarded, and the developer's local machine becomes an unintentional proxy. In cloud development environments, auto-forwarded ports may be publicly accessible depending on the hosting provider. |
| **Misconfiguration risk** | If `true`, any process on the remote machine that opens a port will be silently forwarded. This can expose databases, debug endpoints, admin panels, or attacker-controlled services to the developer's local network or even the public internet. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | All port forwarding must be explicit and auditable |
| Standard Enterprise | `false` | Developers should explicitly forward needed ports |
| Developer | `true` | Convenient for web development; understand the risk |

### 3.2 `remote.autoForwardPortsSource`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls how auto-forwarded ports are detected. `"process"` monitors running processes; `"output"` scans terminal output for port numbers. |
| **Why it matters** | Output-based detection is more aggressive and can be tricked by any text containing a port number. Process-based detection is more targeted but still automatic. If `autoForwardPorts` is enabled, `"process"` is the safer detection method. |
| **Misconfiguration risk** | Setting to `"output"` when auto-forward is enabled means terminal output like `Listening on port 8080` from a log file could trigger forwarding of port 8080, even if no local process is listening. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `"process"` (moot if autoForward is `false`) | Defense in depth |
| Standard Enterprise | `"process"` | Safer detection method |
| Developer | `"output"` | More convenient; catches more services |

---

## 4. Telemetry

### 4.1 `telemetry.telemetryLevel`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls what telemetry data Cursor and its extensions send. Values: `"off"`, `"crash"`, `"error"`, `"all"`. |
| **Why it matters** | Telemetry data can include file paths, extension usage, command history, error messages with code snippets, and workspace metadata. In regulated environments, this may constitute data exfiltration. Even in standard enterprises, telemetry to third-party extension vendors is a data classification concern. Disabling telemetry ensures no usage data leaves the organization's control. |
| **Misconfiguration risk** | If set to `"all"`, file paths, error messages (which may contain code), and usage patterns are transmitted. In healthcare or finance, this could violate data residency requirements. Extension-level telemetry may go to vendors with unknown data handling practices. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `"off"` | Required by most compliance frameworks |
| Standard Enterprise | `"off"` or `"crash"` | `"crash"` sends only crash dumps (useful for debugging); evaluate whether crash data is acceptable |
| Developer | `"error"` or `"all"` | Helps Cursor improve; acceptable for non-sensitive work |

---

## 5. Extension Controls

### 5.1 `extensions.autoUpdate`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, extensions update automatically to the latest version without user action. |
| **Why it matters** | Extensions are executable code running with broad IDE permissions. An auto-update can introduce a supply-chain compromise (a maintainer's account is hacked, or a malicious version is published). By disabling auto-update, teams can pin extension versions, review changelogs, and test updates in a staging environment before rollout. The 2024 VS Code Marketplace incidents demonstrated that compromised extensions can exfiltrate code and credentials. |
| **Misconfiguration risk** | If `true`, a compromised extension update is silently installed on every developer machine. The window between a malicious publish and detection could be hours or days — during which every auto-updating machine is compromised. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` (enforce via MDM `UpdateMode`) | All extensions go through an internal approval pipeline |
| Standard Enterprise | `false` | Update on a managed schedule; review release notes |
| Developer | `true` | Convenient; rely on Marketplace moderation |

### 5.2 `extensions.autoCheckUpdates`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls whether Cursor periodically checks the Marketplace for extension updates. Even if auto-update is off, this will show update badges. |
| **Why it matters** | Update checks are network calls to the Marketplace API that reveal which extensions are installed and their versions. This metadata can fingerprint the development environment. Disabling checks also prevents UI nudges that pressure developers into updating before IT has vetted new versions. |
| **Misconfiguration risk** | If `true` while `autoUpdate` is `false`, developers see update badges and may manually update to an unvetted version, bypassing the managed update workflow. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | No external calls; updates are pushed centrally |
| Standard Enterprise | `false` | Consistent with managed update strategy |
| Developer | `true` | Useful to know updates are available |

### 5.3 `extensions.ignoreRecommendations`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, suppresses extension recommendations from workspaces (`.vscode/extensions.json`), the Marketplace, and peers. |
| **Why it matters** | Repository-level `extensions.json` can recommend any extension by ID. A malicious repository can recommend a typosquatted or compromised extension. Marketplace recommendations can surface extensions based on popularity metrics that may be gamed. Suppressing recommendations ensures developers only install from an approved list. |
| **Misconfiguration risk** | If `false`, opening a cloned repository can trigger "Install Recommended Extensions" prompts. A developer who clicks "Install All" may install untrusted extensions from a malicious `extensions.json`. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `true` | Combined with `AllowedExtensions` MDM policy for allowlist enforcement |
| Standard Enterprise | `true` | Prevents social engineering via repo-level recommendations |
| Developer | `false` | Recommendations are useful for discovering tooling |

---

## 6. Git Safety

### 6.1 `git.autofetch`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Periodically runs `git fetch` in the background to check for remote changes. |
| **Why it matters** | Background `git fetch` is a network operation that authenticates to remote repositories. In environments with credential caching (SSH keys, PATs), this runs silently and continuously. If the remote URL is tampered with (e.g., a `.git/config` in a cloned repo points to an attacker's server), autofetch sends credentials to the wrong server. Additionally, in air-gapped or restricted networks, unexpected network calls violate network policy. |
| **Misconfiguration risk** | If `true` and a repository's remote URL is compromised or swapped (`.git/config` manipulation), credentials are silently sent to the attacker's server on every fetch interval. The developer sees no prompt or confirmation. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `false` | All git operations should be explicit and logged |
| Standard Enterprise | `false` | Developers manually fetch; prevents credential leak to tampered remotes |
| Developer | `true` | Convenient; low risk with trusted remotes |

### 6.2 `git.confirmSync`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Requires confirmation before the "Sync Changes" button pushes to and pulls from the remote. |
| **Why it matters** | Accidental sync can push unreviewed code, incomplete features, or sensitive files to a remote repository. In regulated environments, all pushes should go through a PR workflow. The confirmation dialog is a speed bump that prevents accidental data disclosure. |
| **Misconfiguration risk** | If `false`, a single click on "Sync" pushes whatever is committed — including accidentally committed credentials, `.env` files, or draft code — to the remote with no confirmation. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `true` | Mandatory; accidental pushes can be compliance violations |
| Standard Enterprise | `true` | Prevents accidental pushes of sensitive content |
| Developer | `true` or `false` | Personal preference; low risk for personal repos |

---

## 7. Network Security

### 7.1 `http.proxyStrictSSL`

| Attribute | Detail |
|-----------|--------|
| **What it does** | When `true`, all HTTPS connections through the configured proxy must have valid SSL certificates. Cursor will reject connections to servers with self-signed, expired, or mismatched certificates. |
| **Why it matters** | Disabling strict SSL enables man-in-the-middle attacks. An attacker on the network can intercept all HTTPS traffic between Cursor and external services (Marketplace, git remotes, AI endpoints, extension telemetry). This is especially critical because Cursor sends code context to AI endpoints — MITM on this traffic exposes source code. |
| **Misconfiguration risk** | If `false`, Cursor accepts any certificate, including those presented by MITM proxies, compromised CAs, or attacker-controlled servers. All extension downloads, git operations, AI requests, and telemetry become interceptable. This is the single most dangerous setting to misconfigure. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `true` | Non-negotiable; certificate errors must be investigated, not bypassed |
| Standard Enterprise | `true` | If a corporate proxy uses a custom CA, add the CA to the system trust store rather than disabling SSL validation |
| Developer | `true` | Always; there is no legitimate reason to disable this |

---

## 8. File Exclusions

### 8.1 `files.exclude`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Hides matching files from the Explorer pane, Quick Open, and file-based features. The recommended config excludes `.env`, `.env.*`, `secrets/`, `*.pem`, and `*.key`. |
| **Why it matters** | AI-powered features in Cursor index visible files for context. If credential files are visible in the explorer, they can be opened, read into AI context, and potentially included in prompts sent to AI endpoints. Excluding them removes them from the surface area of AI features, search results, and accidental browsing. This is defense-in-depth — not a substitute for `.gitignore`, but an additional layer. |
| **Misconfiguration risk** | If sensitive file patterns are not excluded, developers may accidentally open `.env` files, the AI may index private keys for context, and search results may surface credentials. Note: `files.exclude` only hides files from the UI — it does not prevent programmatic access via terminal or extensions. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | Exclude `.env`, `.env.*`, `secrets/`, `*.pem`, `*.key`, `*.pfx`, `*.p12`, `*.jks`, `*.keystore`, `*credentials*` | Comprehensive pattern list |
| Standard Enterprise | Exclude `.env`, `.env.*`, `secrets/`, `*.pem`, `*.key` | As provided in `settings.json` |
| Developer | Exclude `.env`, `.env.*` | Minimal; at least protect environment files |

### 8.2 `search.exclude`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Excludes matching files from Cursor's search results (Ctrl+Shift+F) and from AI context gathering during search-based operations. Extends `files.exclude` patterns to the search subsystem. |
| **Why it matters** | Search is a primary way AI features gather context. If `node_modules` is not excluded, search can pull in thousands of dependency files — increasing AI token usage, slowing operations, and potentially including vulnerable or malicious dependency code in AI context. Excluding secret files from search prevents credentials from appearing in search results that might be shared in screenshots or screen recordings. |
| **Misconfiguration risk** | If sensitive file patterns are not excluded from search, a search for a variable name might surface its value in a `.env` file. Searching for "password" might reveal actual passwords in config files. These search results can appear in AI context windows and are visible in screen shares. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | Same as `files.exclude` plus `**/node_modules/**`, `**/vendor/**`, `**/.git/**`, `**/dist/**`, `**/build/**` | Keep AI context clean and credential-free |
| Standard Enterprise | As provided in `settings.json` | Covers primary risks |
| Developer | At minimum exclude `**/node_modules/**` and `**/.env` | Performance and basic safety |

---

## 9. Permissions Configuration (`permissions.json`)

The `permissions.json` file (deployed to `~/.cursor/permissions.json`) controls which commands the Cursor AI Agent can auto-execute without user approval. This is the most operationally critical security control for AI-assisted development.

### 9.1 `terminalAllowlist`

| Attribute | Detail |
|-----------|--------|
| **What it does** | An array of command prefixes that the Agent can execute in the integrated terminal without prompting the user for approval. Commands not matching any prefix require explicit "Allow" clicks. |
| **Why it matters** | The Cursor Agent can generate and execute arbitrary shell commands. Without an allowlist, every command requires a click — which causes approval fatigue and leads to rubber-stamping. With a well-crafted allowlist, read-only and safe commands run instantly while dangerous commands (package installs, file deletions, network operations, sudo) always require review. The allowlist is a principal-of-least-privilege control for AI autonomy. |
| **Misconfiguration risk** | If the allowlist is too broad (e.g., includes `npm install`, `pip install`, `curl`, `wget`, `rm`, `sudo`), the Agent can install arbitrary packages (supply chain attack), download malicious payloads, delete files, or escalate privileges — all without user review. If the allowlist is empty, every command requires approval, creating friction that may cause developers to disable the feature entirely. |

**Recommended allowlists by tier:**

| Environment | Recommended Commands | Rationale |
|-------------|---------------------|-----------|
| Regulated (Strict) | `ls`, `cat`, `head`, `tail`, `grep`, `find`, `wc`, `pwd`, `git status`, `git diff`, `git log` | Read-only filesystem and git operations only. No echo (could write files via redirect). No build/test commands (could have side effects). |
| Standard Enterprise | All of Strict, plus: `echo`, `git branch`, `npm test`, `npm run lint`, `npm run build`, `npx tsc --noEmit`, `python -m pytest`, `go test ./...` | Adds common test and build commands. These have limited side effects and are part of normal development workflow. |
| Developer (Moderate) | All of Standard, plus: `tree`, `file`, `which`, `git stash list`, `npm run typecheck`, `npx prettier --check`, `npx eslint`, `python -m mypy`, `python -m flake8`, `go vet ./...`, `cargo test`, `cargo clippy`, `make test`, `make lint` | Adds linters, type checkers, and multi-language test runners. Still excludes installs, network commands, and destructive operations. |

**Commands that should NEVER be in the allowlist:**

| Command Pattern | Reason |
|-----------------|--------|
| `npm install`, `pip install`, `cargo add` | Installs arbitrary packages; supply chain risk |
| `curl`, `wget`, `fetch` | Downloads arbitrary content from the network |
| `rm`, `rm -rf` | Destructive file operations |
| `sudo`, `su` | Privilege escalation |
| `docker run`, `docker exec` | Container execution with potential host access |
| `ssh`, `scp`, `rsync` | Network access to remote systems |
| `chmod`, `chown` | Permission changes |
| `eval`, `exec`, `source` | Arbitrary code execution |
| `>`, `>>`, `tee` | File write operations (when used as standalone commands) |
| `kill`, `pkill` | Process termination |

### 9.2 `mcpAllowlist`

| Attribute | Detail |
|-----------|--------|
| **What it does** | An array of MCP (Model Context Protocol) tool identifiers that the Agent can invoke without user approval. MCP tools are external services that extend Agent capabilities — database queries, API calls, file system operations, cloud provider interactions. |
| **Why it matters** | MCP tools often have broad permissions: they can read databases, call APIs, modify cloud infrastructure, or interact with external services. Auto-approving MCP tools means the AI can take real-world actions (creating cloud resources, querying production databases, sending messages) without human review. The blast radius of a hallucinated or manipulated MCP call can be very large. |
| **Misconfiguration risk** | If MCP tools are added to the allowlist, a prompt injection or Agent hallucination could trigger database modifications, cloud resource creation, API calls to production services, or data exfiltration through external tool calls — all without user awareness or approval. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `[]` (empty) | All MCP tool calls require explicit approval; no exceptions |
| Standard Enterprise | `[]` (empty) | MCP tools should always require human-in-the-loop approval |
| Developer | `[]` or very specific read-only tools | Even for individual developers, MCP auto-approval is risky; the convenience gain is minimal compared to the risk |

---

## 10. MDM Policies

MDM (Mobile Device Management) policies are the highest-precedence controls. They are enforced at the OS level and cannot be overridden by users or workspace settings. These are deployed through Jamf, Intune, Kandji, or equivalent tools.

### 10.1 `AllowedTeamId`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Restricts Cursor login to accounts belonging to a specific team ID. Users not on this team cannot authenticate. |
| **Why it matters** | Prevents developers from using personal Cursor accounts on corporate machines. Personal accounts may not be covered by the organization's SSO, audit logging, or data protection agreements. This ensures all AI interactions, code context, and usage data are under the organization's Cursor Business/Enterprise plan with appropriate data handling terms. |
| **Misconfiguration risk** | If not set, developers can log in with personal accounts that have different privacy settings, potentially sending corporate code to Cursor servers under personal ToS rather than enterprise DPA. If set to the wrong team ID, all users are locked out. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | Set to organization's team ID | Mandatory; enforced via MDM |
| Standard Enterprise | Set to organization's team ID | Strongly recommended |
| Developer | Not applicable | N/A for personal use |

### 10.2 `AllowedExtensions`

| Attribute | Detail |
|-----------|--------|
| **What it does** | An allowlist of VS Code extension IDs that can be installed. Any extension not on this list is blocked. |
| **Why it matters** | Extensions run with full IDE permissions — they can read all files, execute terminal commands, make network requests, and access the clipboard. A malicious or compromised extension has the same access as the developer. Allowlisting ensures only vetted, approved extensions are installable. This is the enterprise equivalent of an app store curation policy. |
| **Misconfiguration risk** | If not set, any of the ~50,000+ Marketplace extensions can be installed, including known-malicious ones. If the list is too restrictive, developers lose productivity and may seek workarounds (using unsanctioned editors). |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | Curated list reviewed quarterly; typically 10-30 extensions | Each extension should undergo security review before approval |
| Standard Enterprise | Broader list of ~30-100 vetted extensions | Balance security and productivity; include major language support and linters |
| Developer | Not set (no restriction) | Personal choice |

### 10.3 `WorkspaceTrustEnabled`

| Attribute | Detail |
|-----------|--------|
| **What it does** | MDM-level enforcement of workspace trust. When set to `true` via MDM, the user cannot disable workspace trust in their settings. |
| **Why it matters** | The settings-level `security.workspace.trust.enabled` can be overridden by a user. The MDM policy cannot. This ensures workspace trust remains active even if a developer modifies their settings, installs an extension that changes settings, or follows instructions from a malicious README that says "disable workspace trust." |
| **Misconfiguration risk** | If not enforced via MDM, a user can set `security.workspace.trust.enabled: false` in their user settings, effectively disabling the entire trust framework across all workspaces. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `true` (MDM-enforced) | Non-negotiable |
| Standard Enterprise | `true` (MDM-enforced) | Strongly recommended |
| Developer | Not applicable | Use settings-level control |

### 10.4 `UpdateMode`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Controls how Cursor updates itself. Values: `"default"` (auto-update), `"start"` (check on startup), `"manual"` (user-initiated only). |
| **Why it matters** | Cursor updates include changes to the AI model integration, agent capabilities, and security features. In regulated environments, updates must be tested before deployment to ensure they don't introduce new data flows, change AI behavior, or break compliance controls. `"manual"` allows IT to control the update timeline. |
| **Misconfiguration risk** | If set to `"default"`, Cursor auto-updates, potentially introducing new features (like expanded agent capabilities) that haven't been security-reviewed. If set to `"manual"` without a patch management process, security fixes are delayed. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | `"manual"` | Updates tested and deployed by IT on a defined schedule |
| Standard Enterprise | `"manual"` or `"start"` | Balance timeliness with control |
| Developer | `"default"` | Stay current with latest features and security patches |

### 10.5 `NetworkDisableHttp2`

| Attribute | Detail |
|-----------|--------|
| **What it does** | Forces Cursor to use HTTP/1.1 instead of HTTP/2 for all network requests. |
| **Why it matters** | Some corporate proxies, firewalls, and DLP (Data Loss Prevention) tools cannot inspect HTTP/2 traffic due to its binary framing and multiplexing. If the organization's security infrastructure requires HTTP/1.1 for deep packet inspection, this setting ensures Cursor traffic is inspectable. Without it, DLP tools may be blind to data exfiltration via Cursor's AI endpoints. |
| **Misconfiguration risk** | If set to `true` unnecessarily, performance degrades due to lack of multiplexing and header compression. If set to `false` when the proxy requires HTTP/1.1, connections may fail or bypass security inspection. |

| Environment | Recommended Value | Notes |
|-------------|-------------------|-------|
| Regulated | Set based on proxy/DLP requirements | Test with your specific infrastructure |
| Standard Enterprise | `false` (unless proxy requires `true`) | Most modern proxies handle HTTP/2 |
| Developer | `false` | No reason to restrict |

---

## 11. Cursor Enterprise Features

These features are configured through the Cursor Admin Dashboard, not through settings files. They are documented here for completeness because they interact with the settings above.

### 11.1 Team Rules (Enforced vs. Optional)

| Attribute | Detail |
|-----------|--------|
| **What it does** | Team Rules are Cursor Rules (`.mdc` files) that are centrally managed in the admin dashboard and automatically applied to all team members' projects. **Enforced** rules cannot be overridden; **optional** rules can be toggled by users. |
| **Why it matters** | Enforced rules ensure security standards (like those in `rules/security.mdc`) are applied universally. Without enforced rules, each repository must include its own `.cursor/rules/` directory, and there's no guarantee developers haven't modified or deleted them. Team Rules provide centralized, tamper-resistant security policy for AI interactions. |
| **Misconfiguration risk** | If security rules are set to "optional," developers can disable them per-project. If no team rules are configured, security policy depends entirely on per-repo `.cursor/rules/` files, which can be modified by any contributor. |

| Environment | Recommended Approach |
|-------------|---------------------|
| Regulated | All security rules enforced; no optional rules for security-critical policies |
| Standard Enterprise | Core security rules enforced; coding style rules optional |
| Developer | Optional rules or per-project `.cursor/rules/` |

### 11.2 Audit Logs

| Attribute | Detail |
|-----------|--------|
| **What it does** | Records authentication events, settings changes, rule modifications, team membership changes, and administrative actions in the Cursor dashboard. |
| **Why it matters** | Audit logs provide forensic evidence for security incidents, compliance audits, and policy violation investigations. They answer questions like: "Who changed the terminal allowlist?", "When was a new extension approved?", "Which admin modified the team rules?" Without audit logs, there is no accountability for configuration changes. |
| **Misconfiguration risk** | If audit logging is not enabled or logs are not regularly reviewed, policy violations and unauthorized changes go undetected. If log retention is too short, evidence is lost before an investigation begins. |

| Environment | Recommended Approach |
|-------------|---------------------|
| Regulated | Enable with maximum retention; integrate with SIEM; review weekly |
| Standard Enterprise | Enable; review monthly; retain for 1 year minimum |
| Developer | Not applicable |

### 11.3 Admin API

| Attribute | Detail |
|-----------|--------|
| **What it does** | Provides programmatic access to team management, settings deployment, usage reporting, and policy enforcement. |
| **Why it matters** | The Admin API enables automation of security workflows: provisioning new team members with correct settings, auditing current configurations, enforcing compliance checks, and integrating with existing IT management tools. Manual dashboard management does not scale beyond ~50 developers. |
| **Misconfiguration risk** | API keys for the Admin API have broad permissions. If leaked, an attacker could modify team rules, change allowlists, add themselves to the team, or disable security controls. API keys must be stored in secrets management (not code repos) and rotated regularly. |

| Environment | Recommended Approach |
|-------------|---------------------|
| Regulated | Use for automation; store API keys in HSM/secrets manager; rotate quarterly; audit all API calls |
| Standard Enterprise | Use for provisioning and compliance checks; store keys securely |
| Developer | Not applicable |

### 11.4 Cloud Agent Security

| Attribute | Detail |
|-----------|--------|
| **What it does** | Cloud Agents run in Cursor's cloud infrastructure and can execute code, access the network, use the computer (browser/GUI), and receive follow-up instructions. Dashboard settings control these capabilities. |
| **Why it matters** | Cloud Agents operate autonomously with significant capabilities. Unlike local Agent mode where the developer can see every action in real time, Cloud Agents run in the background. This creates a unique threat model: prompt injection, unintended network access, secrets exposure, and unmonitored follow-up instructions from other team members. Each capability must be individually evaluated and restricted. |
| **Misconfiguration risk** | See the Cloud Agent Security section below for detailed per-setting analysis. The aggregate risk of misconfigured Cloud Agent settings is significant: secrets leaked to public repos, unrestricted network access enabling data exfiltration, and follow-up instructions allowing unauthorized command injection. |

| Environment | Recommended Approach |
|-------------|---------------------|
| Regulated | See detailed Cloud Agent configuration in `cloud-agent-security.json` — most features restricted or disabled |
| Standard Enterprise | Network allowlist; follow-ups restricted to service accounts; secrets enabled with public repo injection disabled |
| Developer | Evaluate each setting based on personal risk tolerance |

---

## 12. Combined Security Posture Matrix

The following matrix summarizes all settings across the three tiers for quick reference.

### Settings (`settings.json`)

| Setting | Regulated | Standard Enterprise | Developer |
|---------|-----------|--------------------:|-----------|
| `security.workspace.trust.enabled` | `true` (MDM) | `true` | `true` |
| `security.workspace.trust.startupPrompt` | `"always"` | `"always"` | `"once"` |
| `security.workspace.trust.banner` | `"always"` | `"always"` | `"always"` |
| `security.workspace.trust.emptyWindow` | `false` | `false` | `true` |
| `terminal.integrated.allowedLinkSchemes` | `["https"]` | `["https","http","file"]` | Default |
| `terminal.integrated.enableFileLinks` | `"off"` | `"off"` | `"on"` |
| `remote.autoForwardPorts` | `false` | `false` | `true` |
| `remote.autoForwardPortsSource` | `"process"` | `"process"` | `"output"` |
| `telemetry.telemetryLevel` | `"off"` | `"off"` | `"error"` |
| `extensions.autoUpdate` | `false` | `false` | `true` |
| `extensions.autoCheckUpdates` | `false` | `false` | `true` |
| `extensions.ignoreRecommendations` | `true` | `true` | `false` |
| `git.autofetch` | `false` | `false` | `true` |
| `git.confirmSync` | `true` | `true` | `true` |
| `http.proxyStrictSSL` | `true` | `true` | `true` |
| `files.exclude` | Comprehensive | Standard | Minimal |
| `search.exclude` | Comprehensive | Standard | Minimal |

### Permissions (`permissions.json`)

| Setting | Regulated | Standard Enterprise | Developer |
|---------|-----------|--------------------:|-----------|
| `terminalAllowlist` | Read-only (11 cmds) | + Build/test (22 cmds) | + Linters (37 cmds) |
| `mcpAllowlist` | `[]` | `[]` | `[]` |

### MDM Policies

| Policy | Regulated | Standard Enterprise | Developer |
|--------|-----------|--------------------:|-----------|
| `AllowedTeamId` | Set | Set | N/A |
| `AllowedExtensions` | Strict allowlist | Broad allowlist | Not set |
| `WorkspaceTrustEnabled` | `true` | `true` | N/A |
| `UpdateMode` | `"manual"` | `"manual"` | `"default"` |
| `NetworkDisableHttp2` | Per proxy needs | `false` | `false` |

### Cloud Agent Dashboard

| Setting | Regulated | Standard Enterprise | Developer |
|---------|-----------|--------------------:|-----------|
| Network access | `allowlist_only` | `default_plus_allowlist` | `allow_all` |
| Computer use | `disabled` | `disabled` | `enabled` |
| Follow-ups | `disabled` | `service_accounts_only` | `all_team_members` |
| Secrets injection | Disabled | Enabled (no public repos) | Enabled |
| Show file diffs | `true` | `true` | `true` |
| Show code snippets | `false` | `true` | `true` |

---

## Appendix A: Interaction Between Controls

Understanding how these controls layer is critical for a complete security posture:

```
MDM Policy (highest precedence)
  └─> Dashboard Admin Settings
       └─> User settings.json
            └─> Workspace settings.json (lowest precedence)
```

1. **MDM policies** override everything. If `WorkspaceTrustEnabled` is `true` via MDM, no settings file can disable it.
2. **Dashboard Admin Settings** (Team Rules, Cloud Agent config, allowlists) are managed centrally and override local files.
3. **User `settings.json`** (`~/.config/Cursor/User/settings.json`) applies globally to the user's Cursor instance.
4. **Workspace `settings.json`** (`.vscode/settings.json` in the repo) applies only to that workspace. This is the least trusted source since any repo contributor can modify it.

The `permissions.json` at `~/.cursor/permissions.json` is a user-level control, but the Team Admin Dashboard can enforce stricter allowlists that override it.

## Appendix B: Threat Model Summary

| Threat | Primary Control | Secondary Controls |
|--------|----------------|--------------------|
| Malicious repository (supply chain) | Workspace Trust | File exclusions, extension allowlist |
| Compromised extension | `AllowedExtensions` MDM policy | `extensions.autoUpdate: false`, `ignoreRecommendations: true` |
| AI Agent executing dangerous commands | `terminalAllowlist` in `permissions.json` | Team Rules (enforced), security.mdc |
| Credential exposure via AI context | `files.exclude` + `search.exclude` | `.cursor/rules/security.mdc` "Never Do" rules |
| Man-in-the-middle on AI traffic | `http.proxyStrictSSL: true` | `NetworkDisableHttp2` for DLP inspection |
| Data exfiltration via telemetry | `telemetry.telemetryLevel: "off"` | Network monitoring, DLP |
| Unauthorized Cloud Agent actions | Network allowlist, follow-up restrictions | Secrets injection controls, audit logs |
| Unmonitored configuration drift | Audit logs, Admin API | MDM enforcement, SIEM integration |
| Port scanning via auto-forward | `remote.autoForwardPorts: false` | Network segmentation |
| Protocol handler exploitation | `terminal.integrated.allowedLinkSchemes` | `enableFileLinks: "off"` |

## Appendix C: Compliance Mapping

| Compliance Framework | Key Cursor Controls |
|----------------------|---------------------|
| **SOC 2 (CC6.1 — Logical Access)** | `AllowedTeamId`, SSO/SAML, SCIM, audit logs |
| **SOC 2 (CC6.6 — System Boundaries)** | `terminalAllowlist`, `mcpAllowlist`, network allowlist |
| **SOC 2 (CC7.2 — Monitoring)** | Audit logs, Admin API integration with SIEM |
| **HIPAA (Access Control §164.312(a))** | Workspace trust, extension allowlist, `AllowedTeamId` |
| **HIPAA (Transmission Security §164.312(e))** | `http.proxyStrictSSL: true`, `telemetry.telemetryLevel: "off"` |
| **PCI-DSS (Req 7 — Restrict Access)** | `terminalAllowlist`, `AllowedExtensions`, Team Rules |
| **PCI-DSS (Req 10 — Track and Monitor)** | Audit logs, Cloud Agent activity monitoring |
| **FedRAMP (AC-6 — Least Privilege)** | `terminalAllowlist`, `mcpAllowlist`, `files.exclude` |
| **GDPR (Art. 32 — Security of Processing)** | `telemetry.telemetryLevel: "off"`, data residency via team plan |

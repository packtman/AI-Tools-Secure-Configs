# GitHub Copilot managed-settings.json: key rationale

This file maps each deployable key in `managed-settings-*.json` to what it does, why each tier sets it this way, and what breaks if it is misconfigured. Production JSON cannot contain comments. Keep this file next to the deployed JSON for audit review.

Vendor source (generally available 2026-08-06 for MCP allowlists, 2026-08-12 for Agent Plugins 1.0 governance):

- [Enterprise managed settings reference](https://docs.github.com/en/copilot/reference/enterprise-managed-settings-reference)
- [Configuring an MCP server allowlist](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-enterprise-allowlist)
- [Configuring enterprise-managed settings](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-agents/configure-enterprise-managed-settings)

MCP (Model Context Protocol) is a way for Copilot to call external tools through MCP servers. MDM (Mobile Device Management) is software such as Jamf or Intune that pushes settings to endpoints.

Do not put secrets, tokens, API keys, or Authorization headers in managed settings. The vendor `telemetry.headers` example uses a bearer token. Route collector auth through your secrets manager, not this file.

## Keys by tier

| Key | Baseline | Moderate | Strict | Reason for the difference |
|-----|----------|----------|--------|---------------------------|
| `permissions.disableBypassPermissionsMode` | `"disable"` | `"disable"` | `"disable"` | Bypass (YOLO / allow-all) skips every tool prompt. No tier should leave that gate open. |
| `enabledPlugins` | omitted | `{}` | `{}` | Baseline does not push plugins. Enterprise tiers start with an empty map. Add `PLUGIN@MARKETPLACE: true` only after review. |
| `extraKnownMarketplaces` | omitted | org GitHub repo | omitted | Moderate adds one approved catalog. Strict does not add any catalog. |
| `strictKnownMarketplaces` | omitted | same org GitHub repo | `[]` (lockdown) | Empty array blocks all plugin marketplaces. Moderate pins to the org catalog. Baseline keeps the vendor default marketplace. |
| `allowedMcpServers` | omitted (all allowed except deny) | `https://api.githubcopilot.com/*` | `[]` (built-in only) | Empty array blocks every non-built-in server. Omit the key to allow all except the denylist. |
| `deniedMcpServers` | filesystem MCP at `/` | filesystem MCP at `/` | filesystem MCP at `/` | Deny always wins. All tiers block a root-filesystem MCP. |
| `sandbox.enabled` | omitted | `true` | `true` | Copilot CLI sandbox is a minimum floor. Baseline leaves it to the user. |
| `sandbox.allowBypass` | omitted | `false` | `false` | Prevents the model from requesting unsandboxed commands. |
| `sandbox.sandboxMcpServers` | omitted | `true` | `true` | Local MCP processes started by Copilot CLI run inside the sandbox. |
| `sandbox.sandboxLspServers` | omitted | `true` | `true` | Language servers started by Copilot CLI run inside the sandbox. |
| `sandbox.gitAuth` | omitted | omitted | `false` | Strict blocks GitHub token injection for Git HTTPS inside the sandbox. |
| `sandbox.ghAuth` | omitted | omitted | `false` | Strict blocks GitHub token injection for GitHub CLI inside the sandbox. |
| `sandbox.allowDevToolAccess` | omitted | omitted | `false` | Strict blocks automatic access to caches and registries that often hold tokens. |
| `remoteControl.mode` | omitted | `requireSSO` | `disabled` | Strict blocks remote control of sessions on the device. Moderate requires SSO for listed orgs. |
| `permissions.model` | omitted | omitted | omitted | Model picker is not a security control for these tiers. |
| `telemetry` | omitted | omitted | omitted | OTEL export can carry Authorization headers. Configure collector auth in a secrets manager, not in this JSON. |

## Key-by-key rationale

### `permissions.disableBypassPermissionsMode`

**What it does:** Stops users from turning on bypass mode (also called YOLO or allow-all). In Copilot CLI this suppresses `--yolo`, `--allow-all`, `--allow-all-tools`, `--allow-all-paths`, `--allow-all-urls`, and the `/yolo` and `/allow-all` slash commands. In VS Code it turns off `chat.tools.global.autoApprove` and keeps it off. In the Copilot app it blocks Allow all under Tool Permissions.

**Why:** Bypass is the Copilot equivalent of Claude Code `--dangerously-skip-permissions`. Once it is on, the agent can run commands, read paths, and fetch URLs without a human prompt.

**What breaks if removed:** Developers regain a one-click skip of every approval. Pair this with Claude Code `disableBypassPermissionsMode` and Cursor empty `mcpAllowlist` so one tool cannot bypass the others.

### `enabledPlugins`

**What it does:** Auto-installs (`true`) or blocks (`false`) a plugin identified as `PLUGIN-NAME@MARKETPLACE-NAME`. Enterprise and team files combine additively.

**Why:** Agent Plugins 1.0 can bundle a skill and an MCP server in one package. Auto-installing an unreviewed plugin is the same as deploying unreviewed tools to every seat.

**What breaks if a plugin is set `true` without repo access:** The client tries to install it for every user and fails for anyone who cannot read the plugin host. Do not put private marketplace credentials in this file.

### `extraKnownMarketplaces` and `strictKnownMarketplaces`

**What they do:** `extraKnownMarketplaces` adds catalogs. `strictKnownMarketplaces` limits installs to listed catalogs. An empty `strictKnownMarketplaces` array is a complete lockdown.

**Why:** Public plugin marketplaces are an unreviewed supply chain. Moderate points both keys at one org-owned GitHub repo (`YOUR-ORG/YOUR-PLUGIN-MARKETPLACE`). Strict lists no catalogs.

**What breaks if Moderate is left on the placeholder repo:** Plugin discovery fails until you publish a real marketplace repository. Create that repo before Phase 2.

**Matcher note:** Do not treat marketplace `hostPattern` / `pathPattern` as a substitute for `strictKnownMarketplaces` unless your security team has reviewed the regex.

### `allowedMcpServers`

**What it does:** When present, only matching MCP servers can run. Built-in first-party Copilot servers (including the GitHub MCP server) stay allowed. Malformed JSON fails closed (treated as an empty allowlist). Unresolved variables such as `${TOKEN}` in a URL or command are blocked because the client cannot verify the server.

**Why:** This is the generally available replacement for the preview MCP private-registry allowlist. GitHub recommends setting the AI Controls registry policy to Allow all and using this file as the single source of truth.

**Matchers:** Use `serverUrl` for remote HTTP/SSE servers (wildcards allowed, URLs are canonicalized). Use `serverCommand` for local stdio servers (exact command and arguments, no wildcards). Do not use `serverName` as a security control. Users can rename servers.

**What breaks if Strict uses `[]`:** Third-party MCP servers stop, including Playwright and internal stdio servers. File an exception to add a `serverUrl` or `serverCommand` entry. Do not widen with `serverName`.

**Cloud agent gap:** Copilot cloud agent does not enforce MCP allowlists. Keep cloud agent disabled (Strict) or limited (Moderate) in `org-policy-*.json`.

### `deniedMcpServers`

**What it does:** Blocks matching servers even if they also appear on the allowlist. First-party Copilot servers cannot be denied.

**Why:** All three tiers deny `@modelcontextprotocol/server-filesystem` launched against `/`. That command would give the model read access to the entire disk.

**What breaks if the command args do not match exactly:** `serverCommand` has no wildcards. `npx -y @modelcontextprotocol/server-filesystem /home` is a different server and is not covered by the `/` deny. Add extra deny entries for other roots you care about (`/Users`, `/home`, `C:\\`).

### `sandbox`

**What it does:** Sets a minimum Copilot CLI sandbox. `enabled: true` forces the sandbox on. `allowBypass: false` stops unsandboxed command requests. `sandboxMcpServers` / `sandboxLspServers: true` put local MCP and language servers inside the sandbox. Strict also sets `gitAuth`, `ghAuth`, and `allowDevToolAccess` to `false`.

**Why:** Copilot CLI is a shell agent. This sandbox does not replace Claude Code or Cursor shell policy. Configure those tools separately.

**What breaks if Strict disables `allowDevToolAccess`:** Package restore, authenticated registries, and shared caches can fail until you grant explicit paths. Use the exception process, not a blanket `true`.

**Linux MDM:** Native MDM is not supported on Linux. Use the file-based path `/etc/github-copilot/managed-settings.json` owned by root, not a symlink, and not group- or world-writable.

### `remoteControl`

**What it does:** Controls whether another client can drive Copilot sessions hosted on this device. `disabled` blocks it. `requireSSO` allows it only from a client that is SSO-authorized for `githubDotComOrganizations`. This does not stop the user from remotely controlling sessions on other devices.

**Why:** A remote-controlled session is a prompt-injection path from a second machine.

**What breaks if the org login is wrong:** Every remote-control attempt fails, or a sibling org is trusted. Use the GitHub organization login, not a display name.

## Keys intentionally omitted

| Key | Why it is omitted |
|-----|-------------------|
| `permissions.model` | Auto model selection is a productivity default, not a threat control. |
| `telemetry` | Vendor examples put collector `Authorization` headers in JSON. That is a secret. If you need OTEL, inject headers from a secrets manager outside this repo. |
| `serverName` matchers | Documented as convenience only. Users can rename servers. |
| Registry-only MCP policy | Preview, name/ID matching, weaker than managed-settings allowlists. GitHub says do not combine it with this file. |

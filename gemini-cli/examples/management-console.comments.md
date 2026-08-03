# Gemini CLI Management Console: Setting Rationale

These notes map Google Management Console controls to the runtime `admin.*` fields the Gemini CLI receives remotely for Gemini Code Assist enterprise users.

**Do not** paste the `admin` object into `~/.gemini/settings.json` or system `settings.json`. Local files are a different control plane. Remote admin settings are immutable locally.

Console: https://goo.gle/manage-gemini-cli  
Upstream: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/admin/enterprise-controls.md

---

## Strict Mode / `admin.secureModeEnabled`

- **What:** Blocks YOLO mode and Always allow approval shortcuts.
- **Why (all tiers):** Prevents auto-approval of dangerous tool calls after prompt injection or mistaken trust.
- **What breaks if removed:** Users can re-enable YOLO and skip confirmations from local settings.
- **Values:** Baseline / Moderate / Strict: console Strict Mode enabled (`secureModeEnabled: true`).

## Extensions / `admin.extensions.enabled`

- **What:** Allows or blocks Gemini CLI extensions (including extension-bundled skills and tools).
- **Why:** Extensions can add arbitrary tools and network behavior outside the MCP allowlist story.
- **What breaks if misconfigured:** `false` blocks approved extension workflows; `true` without review expands the attack surface.
- **Values:** All tiers: disabled unless a documented exception exists.

## MCP Enabled / `admin.mcp.enabled`

- **What:** Master switch for Model Context Protocol (MCP) servers (external tool bridges the agent can call).
- **Why (Strict):** Disable MCP entirely for regulated endpoints.
- **Why (Moderate / Baseline):** Keep MCP available, then constrain with allowlist and/or required servers.
- **What breaks if removed:** Local MCP configs become usable again even when org policy intended a ban.
- **Values:** Strict `false`; Moderate / Baseline `true`.

## MCP Servers allowlist / `admin.mcp.config`

- **What:** Admin allowlist of remote MCP servers. Active allowlist ignores local servers not on the list. Matching names merge with admin `url` / `type` / `trust` / tool filters winning.
- **Why (Moderate):** Only audited remote HTTP/SSE servers. Clear local `command` / `args` / `env` / `cwd` so users cannot swap in a local binary.
- **Why (Strict):** Empty / unused because MCP is disabled.
- **Why (Baseline):** Empty allowlist means local MCP configs remain usable when MCP is enabled. Pair with endpoint system `mcp.allowed` if you need host-level enforcement without Code Assist enterprise.
- **What breaks if misconfigured:** Empty allowlist with MCP enabled is permissive. Over-broad `includeTools` exposes admin or destructive tools. `trust: true` skips per-tool approval.
- **Values:** Strict `{}`; Moderate explicit remote allowlist with `trust: false`; Baseline `{}`.

## Required MCP Servers / `admin.mcp.requiredConfig`

- **What:** Preview control that always injects named remote MCP servers after allowlist filtering. Overrides same-named local configs. Supports remote `sse` / `http` only (no local `command`).
- **Why (Moderate):** Force a mandatory compliance or inventory MCP without relying on each developer to configure it.
- **Why (Strict / Baseline):** Leave empty. Strict has MCP off. Baseline avoids forced org-wide MCP until reviewed.
- **What breaks if misconfigured:** A bad required URL breaks every session. `trust: true` (vendor default for required servers) removes approval prompts; this repo sets `trust: false`. Never put OAuth client secrets in repo templates.
- **Values:** Strict / Baseline `{}`; Moderate example remote compliance server only.

## Unmanaged Capabilities / `admin.skills.enabled`

- **What:** Console label Unmanaged Capabilities. Currently gates Agent Skills (on-demand skill packages from `~/.gemini/skills`, `.gemini/skills`, extensions, and built-ins).
- **Why (Strict / Moderate):** Disable until skills are reviewed. Skills grant directory access after consent and can ship scripts or procedural exfil guidance.
- **Why (Baseline):** Allow skills for productivity; still require user consent on activation and prefer org-reviewed skill repos.
- **What breaks if removed:** Users can install skills from git (`gemini skills install`) including untrusted repos with `--consent`.
- **Values:** Strict / Moderate `false`; Baseline `true`.

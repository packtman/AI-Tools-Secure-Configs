# Tabnine — Admin Security Policy

## 1. Identity & Access

- [ ] **SSO** — Configure SSO with your identity provider.
- [ ] **RBAC** — Assign Admin role only to administrators; use standard User role for developers. Use Team Lead role for limited delegation.
- [ ] **Installation Admin** — Reserve for core infrastructure team only.
- [ ] **License management** — Review active licenses monthly; reclaim unused seats.
- [ ] **Folder trust** — Verify folder trust defaults to `untrusted` (v0.24.0+ default); configure trusted folders explicitly.

## 2. Agent Security (v6.1+)

- [ ] **CLI sandboxing** — Ensure OS-level agent sandboxing is enabled (Seatbelt on macOS, containers on Linux/Windows).
- [ ] **Disable YOLO mode** — Set `security.disableYoloMode: true` in system settings to prevent users from bypassing approval.
- [ ] **Secure mode** — Set `secureModeEnabled: true` via remote admin settings.
- [ ] **Command permissions** — Default all commands to `require-confirmation` via Native Tools admin UI.
- [ ] **Auto-approve allowlist** — Only auto-approve safe read-only commands (`git status`, `npm test`).
- [ ] **Disabled commands** — Block destructive commands (`rm -rf`, `sudo`, `docker rm`, etc.).
- [ ] **Workspace scoping** — Verify workspace-scoped tool restrictions are active (blocks `~/.ssh`, `/etc/passwd`, etc.).
- [ ] **Agent Skills** — Enforce admin-approved Agent Skills via system settings (v0.25.0+).
- [ ] **Plan mode** — Set `approval_mode: plan` for read-only agent environments (plan without executing).

## 3. MCP Server Governance

- [ ] **MCP enabled/disabled** — Control `mcpEnabled` via remote admin settings.
- [ ] **MCP server allowlist** — Restrict which MCP servers agents can connect to.
- [ ] **Enterprise Context Engine** — Ensure only approved repositories are indexed for MCP context.
- [ ] **Coaching guidelines** — Define organizational coding standards via MCP for PR review enforcement.
- [ ] **Custom headers** — Use `%EMAIL%` and `%TEAM%` placeholders for authenticated MCP requests.

## 4. Model Configuration

- [ ] **Private endpoints** — Use private LLM endpoints (Amazon Bedrock, Azure OpenAI, GCP Vertex AI, or OpenAI-compatible).
- [ ] **Model selection** — Restrict available models to approved ones; centralized admin control applies automatically to CLI.
- [ ] **Model switching** — Verify admin model changes propagate to all CLI instances without local config changes.
- [ ] **Data residency** — Ensure model endpoints are in approved regions.
- [ ] **Training opt-out** — Verify code is not used for model training.

## 5. Admin Console Controls

- [ ] **Native Tools** — Configure Run/Apply/Create permissions per organization (Auto-approve / Ask first / Disable).
- [ ] **Cost Control** — Set agent cost limits and budget controls in Admin Console.
- [ ] **Extensions** — Manage CLI extensions; disable unauthorized extensions via admin settings (v0.25.0+).
- [ ] **Remote admin settings** — Verify settings propagate to IDE extensions within 15 minutes.
- [ ] **Modes** — Configure allowed modes in admin policies (v0.24.0+).

## 6. Network & Infrastructure

- [ ] **Private installation** — Deploy Tabnine in your private cloud / VPC / air-gapped environments.
- [ ] **Proxy configuration** — Route traffic through corporate proxy.
- [ ] **Firewall rules** — Allowlist Tabnine endpoints; block unauthorized traffic.
- [ ] **TLS enforcement** — Ensure all connections use TLS 1.2+.
- [ ] **SMTP** — Configure SMTP for user management emails (invitations, password resets).

## 7. Monitoring & Compliance

- [ ] **Admin dashboard** — Review usage analytics weekly; monitor agent session data.
- [ ] **Audit logs** — Enable and export audit logs.
- [ ] **Code attribution** — Track AI-generated code for compliance.
- [ ] **User-level agent data** — Review per-user agent activity and data exposure.
- [ ] **Incident response** — Document runbook for revoking access and investigating misuse.

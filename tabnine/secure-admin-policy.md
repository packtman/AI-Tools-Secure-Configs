# Tabnine — Admin Security Policy

## 1. Identity & Access

- [ ] **SSO** — Configure SSO with your identity provider.
- [ ] **RBAC** — Assign Admin role only to administrators; use standard User role for developers.
- [ ] **Installation Admin** — Reserve for core infrastructure team only.
- [ ] **License management** — Review active licenses monthly; reclaim unused seats.

## 2. Agent Security (v6.1+)

- [ ] **CLI sandboxing** — Ensure agent sandboxing is enabled (default in v6.1+).
- [ ] **Command permissions** — Default all commands to `require-confirmation`.
- [ ] **Auto-approve allowlist** — Only auto-approve safe read-only commands.
- [ ] **Disabled commands** — Block destructive commands (`rm -rf`, `sudo`, etc.).
- [ ] **Workspace scoping** — Verify workspace-scoped restrictions are active.

## 3. Model Configuration

- [ ] **Private endpoints** — Use private LLM endpoints for sensitive environments.
- [ ] **Model selection** — Restrict available models to approved ones.
- [ ] **Data residency** — Ensure model endpoints are in approved regions.
- [ ] **Training opt-out** — Verify code is not used for model training.

## 4. Network & Infrastructure

- [ ] **Private installation** — Deploy Tabnine in your private cloud for maximum control.
- [ ] **Proxy configuration** — Route traffic through corporate proxy.
- [ ] **Firewall rules** — Allowlist Tabnine endpoints; block unauthorized traffic.
- [ ] **TLS enforcement** — Ensure all connections use TLS 1.2+.
- [ ] **SMTP** — Configure SMTP for user management emails (invitations, password resets).

## 5. Monitoring & Compliance

- [ ] **Admin dashboard** — Review usage analytics weekly.
- [ ] **Audit logs** — Enable and export audit logs.
- [ ] **Code attribution** — Track AI-generated code for compliance.
- [ ] **Incident response** — Document runbook for revoking access and investigating misuse.

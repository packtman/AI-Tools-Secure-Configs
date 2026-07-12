# Windsurf (Codeium) — Admin Controls Reference

## Overview

Windsurf (by Codeium, now part of Cognition/Devin) provides centralized admin controls through the **Admin Portal**, available to organizations on the **Enterprise** plan. Admins manage identity, RBAC, feature toggles, MCP governance, and usage analytics from the portal. Enterprise also supports hybrid and self-hosted deployment modes for organizations with strict data residency requirements.

Windsurf is an AI-native IDE featuring the Cascade agent for autonomous code generation, multi-file edits, and agentic workflows, alongside Supercomplete for code completions.

---

## Admin Portal Access

| Interface | URL | Plans |
|-----------|-----|-------|
| Admin Portal | Windsurf web portal → Admin | Enterprise |
| API Access | Service keys with scoped permissions | Enterprise |
| SCIM API | Custom teams management via API | Enterprise |

### Roles

| Role | Capabilities |
|------|-------------|
| **Super Admin** | Full system access; modify any role or permission (admin role in "all users" group) |
| **Group Admin** | Manage roles and permissions within assigned groups only |
| **Admin** | Team management, feature settings, analytics |
| **User** | Use Windsurf within admin-defined policies |

---

## 1. Identity & Access Management

### SSO (SAML)

| Setting | Location | Notes |
|---------|----------|-------|
| Enable SSO | Admin Portal → SSO | SAML-based; supports Okta, Microsoft Entra ID (Azure AD), Google Workspace |
| SP-initiated SSO | Default | IdP-initiated SSO is NOT supported |
| Multiple IdP support | Via SAML configuration | Configure per organization requirement |

### SCIM Provisioning

| Setting | Location | Notes |
|---------|----------|-------|
| SCIM sync (users) | Admin Portal → SCIM | Auto-provision and deprovision users |
| SCIM sync (groups) | Admin Portal → SCIM | Map IdP groups to Windsurf teams |
| Supported IdPs | Microsoft Entra ID, Okta | SCIM configuration per provider |
| Service key permissions | Team Settings → Service Keys | SCIM requires Team User Read/Update/Delete |

### User Groups (Enterprise + SCIM)

| Capability | Description |
|------------|-------------|
| Group creation | Split users into multiple groups via SCIM integration |
| Role assignment per group | Assign different roles to different groups |
| Group-based feature access | Control feature availability per group |
| Hierarchical delegation | Group admins manage only their assigned groups |

---

## 2. Security & Governance

### Feature Toggles

| Setting | Location | Effect |
|---------|----------|--------|
| Auto-execution level | Admin Portal → Security | Set maximum level for terminal command auto-execution |
| Web search | Admin Portal → Features | Enable/disable web search capabilities |
| MCP servers | Admin Portal → Security | Manage via explicit whitelist |
| Deploys | Admin Portal → Features | Enable/disable infrastructure deployment features |
| Conversation sharing | Admin Portal → Features | Control whether users can share conversations |

### MCP Server Governance

| Setting | Location | Effect |
|---------|----------|--------|
| MCP whitelist | Admin Portal → Security | Approve specific MCP servers at admin level |
| Block unapproved MCP | Admin Portal → Security | Reject MCP servers not on whitelist |
| Read/write permissions | Admin Portal → Security | Enable read-only for analysts; restrict write to senior devs |
| Approval workflows | Admin Portal → Security | Require human confirmation for infrastructure-modifying commands |

### Code Security

| Setting | Location | Effect |
|---------|----------|--------|
| `.codeiumignore` | Repository level | Exclude files/directories from AI context |
| Secret scanning | Built-in | Detect and block secrets in AI suggestions |
| Attribution filtering | Admin Portal → Security | Filter AI completions with attribution concerns |

### Model Access Controls

| Setting | Location | Effect |
|---------|----------|--------|
| Model selection by team | Admin Portal → Models | Control which models are available per team/role |
| Provider restrictions | Admin Portal → Models | Limit to approved model providers |

---

## 3. Data Governance

### Privacy & Data

| Policy | Status | Notes |
|--------|--------|-------|
| No training on customer code | Enterprise | Contractual guarantee |
| Data retention control | Enterprise | Configurable retention policies |
| Data residency options | Enterprise | Cloud, Hybrid, or Self-Hosted deployment |

### Deployment Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| Cloud | AI processing on Codeium servers | Standard enterprise teams |
| Hybrid | Split processing between cloud and on-prem | Sensitive code with cloud convenience |
| Self-Hosted | All AI inference on customer infrastructure | CMMC, HIPAA, FedRAMP, air-gapped environments |

---

## 4. Monitoring & Audit

### Analytics Dashboard

| Metric | Description |
|--------|-------------|
| Usage per team | AI feature adoption by team |
| Per-user breakdown | Individual usage patterns |
| Credit consumption | Track spending against limits |
| Feature adoption | Which capabilities are being used |

### Audit Logging

| Capability | Description |
|------------|-------------|
| AI interaction logs | Record of AI-assisted actions |
| Admin action audit | Track all admin configuration changes |
| Export capability | API and dashboard export for SIEM integration |
| Compliance reporting | Reports for security reviews |

### Service Keys & API

| Capability | Description |
|------------|-------------|
| Scoped service keys | Generate keys with least-privilege permissions |
| API reporting | Programmatic access to usage data |
| Integration hooks | Connect to existing enterprise tooling |

---

## 5. Compliance

### Certifications

| Certification | Status |
|---------------|--------|
| SOC 2 Type II | ✓ |
| HIPAA | ✓ (Self-Hosted / Enterprise) |
| FedRAMP High | ✓ (Self-Hosted) |
| CMMC | ✓ (Self-Hosted) |

---

## 6. Recommended Admin Configuration

### For regulated environments (finance, healthcare, government)

- [ ] Deploy in Self-Hosted mode (all inference on customer infrastructure)
- [ ] Configure SSO with MFA enforcement
- [ ] Enable SCIM for automated provisioning/deprovisioning
- [ ] Set auto-execution level to minimum (require confirmation for all commands)
- [ ] Configure strict MCP whitelist — block all unapproved servers
- [ ] Set `.codeiumignore` rules for sensitive directories across all repos
- [ ] Enable attribution filtering
- [ ] Disable web search and deploy features
- [ ] Restrict conversation sharing
- [ ] Route audit logs to SIEM
- [ ] Assign minimal roles — read-only for analysts, restricted write for developers
- [ ] Review usage analytics and compliance reports monthly

### For standard enterprise teams

- [ ] Deploy in Cloud or Hybrid mode
- [ ] Configure SSO and SCIM
- [ ] Set reasonable auto-execution limits (confirm destructive commands)
- [ ] Configure MCP whitelist for approved integrations
- [ ] Enable web search
- [ ] Set up team-based model access
- [ ] Review analytics quarterly
- [ ] Configure `.codeiumignore` for secrets and sensitive config

### For developer-focused organizations

- [ ] Enable full feature set
- [ ] Configure SSO (optional enforcement)
- [ ] Set moderate auto-execution level
- [ ] Allow MCP broadly with denylist for risky servers
- [ ] Enable all AI features including deploys
- [ ] Monitor usage for cost optimization

---

## Cross-References

- **Windsurf IDE config:** [`../windsurf/`](../windsurf/) — Local configuration templates and security settings
- **RBAC documentation:** [Windsurf RBAC Docs](https://docs.windsurf.com/plugins/accounts/rbac-role-management)
- **SSO/SCIM setup:** [Windsurf SSO & SCIM Docs](https://docs.windsurf.com/plugins/accounts/sso-scim)

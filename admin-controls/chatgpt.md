# ChatGPT — Admin Controls Reference

## Overview

OpenAI provides centralized admin controls for ChatGPT through the **Workspace Admin Console** at `chatgpt.com/admin`, available to organizations on **ChatGPT Business** (formerly Team) and **ChatGPT Enterprise** plans. Enterprise additionally offers a **Global Admin Console** for multi-workspace management.

Admins manage identity, RBAC, feature toggles, usage limits, data retention, and compliance from the admin console. ChatGPT is a web/mobile application — there are no MDM device policies or local config files.

---

## Admin Console Access

| Interface | URL | Plans |
|-----------|-----|-------|
| Workspace Admin | `chatgpt.com/admin` | Business, Enterprise |
| Global Admin Console | `chatgpt.com/admin` (org-level) | Enterprise (multi-workspace) |

### Roles

| Role | Capabilities |
|------|-------------|
| **Owner** | Full access: billing, identity, workspace configuration, invite all roles |
| **Admin** | Manage users, groups, Codex access tokens, routine admin tasks |
| **Member** | Use ChatGPT and create GPTs; no admin privileges |
| **Analytics Viewer** | Member + access to workspace analytics |

### Seat Types

| Seat | Access |
|------|--------|
| ChatGPT | Full ChatGPT access (GPT-4o, o3, agents, canvas, etc.) |
| Codex | Access to Codex (code assistant) features |

Users can hold one or both seat types. Default seat type is configured in Identity & Access settings.

---

## 1. Identity & Access Management

### SSO (SAML)

| Setting | Location | Notes |
|---------|----------|-------|
| Enable SSO | Identity & Provisioning | SAML-based; shared with OpenAI API Platform |
| Enforce SSO | Identity & Provisioning | Disables password/social login for verified domain users |
| IdP integration | Identity & Provisioning | Supports Okta, Azure AD, Google Workspace, OneLogin |

### Domain Management

| Setting | Location | Notes |
|---------|----------|-------|
| Domain verification | Identity & Provisioning | DNS TXT record; shared with API Platform |
| Restrict external invites | Identity & Provisioning | Limit invites to verified domain emails only |

### SCIM Provisioning (Enterprise)

| Setting | Location | Notes |
|---------|----------|-------|
| Directory sync | Identity & Provisioning → SCIM | Auto-invite users based on IdP group membership |
| Group sync | Automatic with SCIM | IdP groups sync to ChatGPT groups for RBAC |
| Deprovisioning | Automatic with SCIM | Remove users when deactivated in IdP |

### IP Allowlisting (Enterprise)

| Setting | Location | Notes |
|---------|----------|-------|
| IP allowlist | Identity & Provisioning | Restrict access to approved IP ranges |

---

## 2. Permissions & RBAC

### Workspace Default Permissions

Location: `Settings and Permissions → Workspace` tab

These defaults apply to all users without a custom role:

| Permission Category | Controls |
|--------------------|----------|
| ChatGPT Agent | Enable/disable autonomous agent mode |
| Canvas | Enable/disable collaborative coding/writing canvas |
| Codex | Enable/disable Codex code assistant |
| Codex internet access | Allow Codex to access the internet |
| Custom GPTs — Create | Allow users to build custom GPTs |
| Custom GPTs — Use | Allow users to use shared GPTs |
| Memory | Allow ChatGPT to remember across conversations |
| Web search | Allow real-time web search |
| File uploads | Allow file attachment in conversations |
| Image generation | Allow DALL-E image generation |
| Voice mode | Allow Advanced Voice Mode |
| Apps & actions | Allow ChatGPT to use connected apps (email, calendar, etc.) |
| Data analysis | Allow code interpreter / data analysis |
| Record (audio) | Allow audio recording features |

### Custom Roles (Enterprise)

Location: `Settings and Permissions → Custom Roles` tab

| Action | Description |
|--------|-------------|
| Create role | Define a named role with specific permission overrides |
| Assign to groups | Apply role to one or more workspace groups |
| Permission inheritance | Users inherit the most permissive setting across all assigned roles |

### Usage Limits per Role (Enterprise)

| Setting | Options | Effect |
|---------|---------|--------|
| Usage limit level | None / Low / Standard / High / Custom | Weekly per-user credit cap |
| Enforcement mode | Admin Alert / Hard Cap | Alert-only or hard block at limit |
| Alert delivery | Weekly email digest to owners | Notify when users approach limits |

---

## 3. GPT Governance

### Custom GPT Controls

| Setting | Location | Effect |
|---------|----------|--------|
| GPT creation | Workspace defaults or RBAC | Allow/block users from creating GPTs |
| GPT sharing scope | Workspace settings | Internal only vs. public sharing |
| GPT publishing approval | Workspace settings | Require admin review before publishing |
| Third-party GPTs | Workspace settings | Allow/block GPT Store GPTs |

### App & Action Governance

| Setting | Location | Effect |
|---------|----------|--------|
| Connected apps | Workspace settings | Enable/disable app integrations (Google, Microsoft, etc.) |
| Action execution | Workspace settings | Allow ChatGPT to take actions via apps |
| Per-app control | Workspace settings | Granular enable/disable per integration |

---

## 4. Data Governance

### Data Training & Privacy

| Policy | Plan | Notes |
|--------|------|-------|
| No training on business data | Business+ | Contractual; conversations never used for training |
| End-to-end encryption | Enterprise | Data encrypted in transit (TLS 1.2+) and at rest (AES-256) |
| Enterprise Key Management | Enterprise | Customer-controlled encryption keys |

### Retention Policies (Enterprise)

| Setting | Location | Effect |
|---------|----------|--------|
| Conversation retention | Settings → Data & Compliance | Set retention window (days) or indefinite |
| Auto-deletion | Settings → Data & Compliance | Delete conversations after retention period |
| User self-deletion | Settings → Data & Compliance | Allow/block users from deleting their conversations |

### Compliance API (Enterprise)

| Capability | Description |
|------------|-------------|
| Conversation export | Bulk export conversation data for compliance review |
| Audit log export | Export admin action logs |
| DLP integration | Feed conversation content to DLP tools for policy enforcement |

### Data Residency (Enterprise)

| Region | Availability |
|--------|-------------|
| United States | Default |
| Europe (EU) | Available |
| United Kingdom | Available |
| Japan | Available |

---

## 5. Monitoring & Analytics

### Workspace Analytics

| Metric | Plan |
|--------|------|
| Active users | Business+ |
| Messages sent | Business+ |
| Feature adoption | Business+ |
| Per-user/team breakdown | Enterprise |
| Cost attribution | Enterprise |
| Model usage distribution | Enterprise |

### Audit Logs (Enterprise)

| Event Category | Examples |
|----------------|----------|
| Authentication | Login, SSO events, failed attempts |
| User management | Invite, deactivate, role change |
| Settings changes | Any admin configuration modification |
| GPT governance | GPT creation, publication, sharing changes |
| Compliance | Data export requests, retention policy changes |

### Compliance Certifications

| Certification | Status |
|---------------|--------|
| SOC 2 Type II | ✓ |
| ISO/IEC 27001:2022 | ✓ |
| ISO 27017 | ✓ |
| ISO 27018 | ✓ |
| ISO 27701 | ✓ |
| HIPAA (BAA available) | Enterprise |
| GDPR (DPA + SCCs) | ✓ |

---

## 6. Global Admin Console (Enterprise)

For organizations with multiple ChatGPT workspaces:

| Capability | Description |
|------------|-------------|
| Multi-workspace view | Manage settings across all workspaces |
| Centralized identity | Single SSO/SCIM configuration across workspaces |
| Usage rollup | Aggregate analytics across workspaces |
| Policy propagation | Apply consistent policies to multiple workspaces |
| Billing consolidation | Single invoice across workspaces |

---

## 7. Recommended Admin Configuration

### For regulated environments (finance, healthcare)

- [ ] Enforce SSO with MFA via IdP
- [ ] Enable SCIM for automated user lifecycle management
- [ ] Configure IP allowlisting for approved networks only
- [ ] Set retention policy to minimum required by compliance
- [ ] Enable Enterprise Key Management (EKM)
- [ ] Select appropriate data residency region
- [ ] Disable: web search, file uploads, connected apps, image generation (review per compliance needs)
- [ ] Create restrictive default role — disable most features
- [ ] Create specific roles per department with only needed features
- [ ] Set hard usage caps per role
- [ ] Block Custom GPT creation (or require admin approval)
- [ ] Block third-party GPTs from GPT Store
- [ ] Configure Compliance API export to your DLP/archival system
- [ ] Route audit logs to SIEM
- [ ] Request BAA for HIPAA if applicable

### For standard enterprise teams

- [ ] Enforce SSO for all users
- [ ] Enable SCIM with group sync
- [ ] Set conversation retention to 90 days (adjust per policy)
- [ ] Create default role with core features enabled
- [ ] Create elevated roles for power users (agents, Codex, apps)
- [ ] Set standard usage limits with admin alerts
- [ ] Allow internal Custom GPT sharing, block public
- [ ] Vet and enable specific connected apps only
- [ ] Review analytics monthly for adoption and anomalies
- [ ] Set up Compliance API for quarterly reviews

### For smaller teams (Business plan)

- [ ] Enable SSO (optional enforcement)
- [ ] Set default permissions — enable core features
- [ ] Verify training opt-out is active
- [ ] Limit connected apps to vetted integrations
- [ ] Review workspace analytics monthly
- [ ] Set GPT sharing to workspace-internal only

---

## 8. Key Differences: Business vs. Enterprise

| Capability | Business | Enterprise |
|------------|----------|------------|
| SSO (SAML) | ✗ | ✓ |
| SCIM provisioning | ✗ | ✓ |
| RBAC / Custom roles | ✗ | ✓ |
| Usage limits | ✗ | ✓ |
| IP allowlisting | ✗ | ✓ |
| Audit logs | ✗ | ✓ |
| Compliance API | ✗ | ✓ |
| Data residency | ✗ | ✓ |
| Enterprise Key Management | ✗ | ✓ |
| Global Admin Console | ✗ | ✓ |
| Usage caps (model) | Unlimited GPT-4o | Unlimited all models |
| Data training opt-out | ✓ | ✓ |
| Admin console | Basic | Full |

---

## Cross-References

- **OpenAI API Platform admin:** [`../openai-platform/`](../openai-platform/) — Org RBAC, API key policies, content filters
- **Shared SSO configuration:** SSO settings are shared between ChatGPT workspace and OpenAI API Platform organization

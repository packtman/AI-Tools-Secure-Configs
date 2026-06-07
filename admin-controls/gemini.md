# Gemini (Google Workspace) — Admin Controls Reference

## Overview

Google provides centralized admin controls for Gemini through the **Google Admin Console** (`admin.google.com`), available to organizations on **Google Workspace Business** and **Enterprise** editions. Admins manage Gemini feature access, data governance, and AI behavior through the Generative AI section of the Admin console.

Gemini in Google Workspace encompasses multiple surfaces: the standalone **Gemini app** (gemini.google.com), **Gemini in Workspace apps** (Gmail, Docs, Sheets, Slides, Meet, Chat, Drive), **NotebookLM**, **Gemini CLI**, and **Gemini Enterprise agents**. Each can be independently controlled at the user, group, or organizational unit (OU) level.

---

## Admin Console Access

| Interface | URL | Required Privilege |
|-----------|-----|-------------------|
| Google Admin Console | `admin.google.com` | Super Admin or Gemini Settings administrator |
| Generative AI section | Admin Console → Generative AI | Gemini Settings privilege |
| AI Control Center | Admin Console → Generative AI → AI control center | Super Admin (Enterprise Standard/Plus) |

### Admin Roles

| Role | Capabilities |
|------|-------------|
| **Super Admin** | Full access to all admin settings including AI Control Center |
| **Gemini Settings Admin** | Manage Gemini-specific feature access and policies |
| **Groups Admin** | Manage group membership for Gemini access control |
| **Custom Roles** | Granular privilege assignment via Admin SDK |

---

## 1. Feature Access Controls

### Gemini App (gemini.google.com)

| Setting | Location | Effect |
|---------|----------|--------|
| Service status | Generative AI → Gemini app | Turn on/off for all, specific OUs, or groups |
| Gemini Enterprise access | Generative AI → Gemini Enterprise | Enable Enterprise features (agents, advanced models) |
| Workspace data access | Generative AI → Gemini Enterprise | Allow Gemini to read Gmail, Drive, Calendar data |
| Edition-level control | Generative AI → Gemini Enterprise | Separate toggles for Business, Standard, Plus editions |

### Gemini in Workspace Apps

Location: `Generative AI → Gemini for Workspace → Feature access`

| Service | Controls |
|---------|----------|
| Gmail | Enable/disable Gemini compose, summarize, reply suggestions |
| Drive, Docs, Sheets, Slides | Enable/disable Gemini side panel, content generation |
| Meet | Enable/disable AI meeting notes, real-time captions |
| Chat | Enable/disable Gemini in Google Chat |
| Calendar | Enable/disable scheduling AI features |
| Forms, Drawings, Vids | Enable/disable AI-powered creation features |
| Google Workspace Studio | Enable/disable AI workflow builder |

Each service can be controlled per organizational unit or per group.

### Workspace Intelligence

Location: `Generative AI → Gemini for Workspace → Workspace Intelligence`

Controls which Workspace services can be actively searched to power generative AI:

| Setting | Effect |
|---------|--------|
| Gmail intelligence | Allow Gemini to reference email content |
| Drive intelligence | Allow Gemini to reference Drive files |
| Calendar intelligence | Allow Gemini to reference calendar events |
| Chat intelligence | Allow Gemini to reference Chat messages |
| Per-service toggle | Independent on/off for each data source |

### Additional AI Services

| Service | Location | Effect |
|---------|----------|--------|
| NotebookLM | Generative AI → NotebookLM | Enable/disable as additional service |
| NotebookLM Plus | Generative AI → NotebookLM | Enable premium features |
| Google Vids | Generative AI → Google Vids | Enable/disable video creation |
| Gemini in AppSheet | Generative AI → App Creation | Enable AI-assisted app creation |
| Gemini CLI | Generative AI → Gemini Enterprise | Included with Enterprise access |
| AI meeting notes | Generative AI → Meet | Allow Gemini to take meeting notes |
| Workspace MCP Server (Preview) | Generative AI → Integrations | Allow third-party AI apps to access Workspace data via MCP |

---

## 2. AI Control Center (Enterprise Standard/Plus)

Launched May 4, 2026, the AI Control Center provides a unified governance dashboard for all generative AI and agent activity.

**Location:** Admin Console → Generative AI → AI control center

### Modules

| Module | Function |
|--------|----------|
| Monitor and control AI access | View AI usage across all services; manage opt-in settings |
| Manage security for AI products | Granular authority over how Gemini and agents access Workspace data |
| Manage fundamental security | Surface existing protections (classification labels, DLP rules, trust domains) |
| Review privacy, abuse, and compliance | Data privacy, abuse prevention, and compliance standards |

### Monitored Services

The AI Control Center tracks usage across:

- Gmail, Drive, Docs, Sheets, Slides
- Meet, Calendar, Chat
- Gemini App (gemini.google.com)

### Agent Governance

| Setting | Location | Effect |
|---------|----------|--------|
| Agent access to Workspace data | AI Control Center → Manage security | Control how AI agents interact with organizational data |
| Classification labels | AI Control Center → Manage fundamental security | Label files to restrict AI access based on sensitivity |
| Trust rules | AI Control Center → Manage fundamental security | Prevent oversharing when using AI |
| Data protection rules | AI Control Center → Manage fundamental security | DLP enforcement for AI interactions |
| Trusted domains | AI Control Center → Manage fundamental security | Restrict external sharing in AI contexts |

### Third-Party AI App Controls

| Setting | Location | Effect |
|---------|----------|--------|
| Third-party AI app access | Security → API Controls | Control OAuth-based third-party AI app access |
| Workspace MCP Server access | Generative AI → Integrations | Govern third-party apps accessing Workspace via MCP |
| App allowlist/blocklist | Security → API Controls | Approve/block specific third-party AI applications |
| Context-Aware Access for AI | Security → Access → CAA | Conditional policies for AI service access |

> **Note:** Third-party apps connected via individual OAuth grants are managed through the existing API Controls section under Security, not the AI Control Center.

---

## 3. Identity & Access Management

Google Workspace provides identity management at the platform level (not Gemini-specific):

### Authentication

| Setting | Location | Effect |
|---------|----------|--------|
| SSO (SAML 2.0) | Admin Console → Security → SSO | Third-party IdP integration |
| 2-Step Verification | Admin Console → Security → 2SV | Enforce MFA for all users |
| Context-Aware Access | Admin Console → Security → CAA | Conditional access policies (IP, device, location) |

### User & Group Management

| Setting | Location | Effect |
|---------|----------|--------|
| Organizational Units | Admin Console → Directory → OUs | Hierarchical user grouping for policy |
| Groups | Admin Console → Directory → Groups | Flexible grouping for feature access |
| Auto-provisioning | Via Google Cloud Identity / SCIM | Sync from external IdP |
| License assignment | Admin Console → Billing → Licenses | Assign Gemini add-on licenses per user |

### Access Scoping for Gemini

| Approach | Use Case |
|----------|----------|
| By Organizational Unit | Department-wide enablement (Engineering, Marketing) |
| By Group | Cross-functional teams, pilot groups |
| By License | Only licensed users get Gemini features |

---

## 4. Data Governance

### Privacy Guarantees

| Policy | Status | Notes |
|--------|--------|-------|
| No training on customer data | ✓ (all Workspace editions) | Workspace data never used to train generative models |
| Data Processing Addendum | ✓ | Part of Workspace agreement |
| Processor commitment | ✓ | Google acts as data processor, not controller |

### Data Residency

| Setting | Location | Effect |
|---------|----------|--------|
| Data regions | Admin Console → Account → Data Regions | Control where Workspace data is stored |
| Supplemental data storage | Admin Console → Data Regions | Additional control for AI processing location |

### Retention & Deletion

| Setting | Location | Effect |
|---------|----------|--------|
| Gemini app conversation history | Admin Console → Generative AI | Set retention window or allow user control |
| User self-deletion | Admin Console → Generative AI | Allow users to delete their Gemini history |
| Vault retention rules | Admin Console → Vault | Apply legal hold and retention to Gemini data |

### Data Loss Prevention (DLP)

| Setting | Location | Effect |
|---------|----------|--------|
| DLP rules | Admin Console → Security → DLP | Scan and block sensitive content in Gemini |
| Content compliance | Admin Console → Compliance | Rules for content flowing through AI features |
| Information barriers | Via Workspace policies | Prevent cross-department data leakage via AI |

---

## 5. Security Controls

### Network & Access

| Setting | Location | Effect |
|---------|----------|--------|
| Context-Aware Access | Security → Access → Context-Aware | IP, device, OS, location-based access policies |
| Session management | Security → Session Control | Configure session duration and re-auth |
| API controls | Security → API Controls | Control third-party app access and OAuth scopes |
| Chrome Enterprise | Via Chrome management | Enforce browser policies for Gemini access |

### Device Management

| Setting | Location | Effect |
|---------|----------|--------|
| Mobile device management | Devices → Mobile | Enforce device compliance for mobile Gemini access |
| Chrome browser policies | Devices → Chrome → Settings | Control AI feature access in managed Chrome |
| Endpoint verification | Devices → Endpoint Verification | Verify device posture before granting access |

---

## 6. Monitoring & Audit

### Admin Reports

| Report | Location | Content |
|--------|----------|---------|
| Gemini usage report | Admin Console → Reporting → Gemini | Adoption metrics per app, per user |
| App usage per service | Reporting → Apps Usage | Gemini adoption within Gmail, Docs, etc. |
| User adoption | Reporting → User Reports | Per-user AI feature engagement |

### Audit Logs

| Log Type | Location | Content |
|----------|----------|---------|
| Admin audit | Security → Investigation → Admin log | All admin console changes |
| Gemini activity | Security → Investigation → Gemini | User interactions with Gemini features |
| Login audit | Security → Investigation → Login | Authentication events |
| OAuth token events | Security → Investigation → OAuth | Third-party app access grants |

### Security & Alert Center

| Setting | Location | Effect |
|---------|----------|--------|
| Custom alerts | Security → Alert Center | Alert on anomalous AI usage patterns |
| DLP incident alerts | Security → Alert Center | Notify on sensitive data exposure via AI |
| Investigation tool | Security → Investigation | Query across all log types |

### BigQuery Export

| Setting | Location | Effect |
|---------|----------|--------|
| Log export | Reporting → BigQuery Export | Stream all audit logs to BigQuery for analysis |
| SIEM integration | Via Chronicle or third-party | Export to Splunk, Sentinel, etc. |

---

## 7. Compliance

### Certifications

| Certification | Status |
|---------------|--------|
| SOC 2 Type II | ✓ |
| SOC 3 | ✓ |
| ISO/IEC 27001 | ✓ |
| ISO/IEC 27017 | ✓ |
| ISO/IEC 27018 | ✓ |
| ISO/IEC 27701 | ✓ |
| FedRAMP High | ✓ (Enterprise Plus) |
| HIPAA (BAA) | ✓ (Enterprise Plus) |
| GDPR | ✓ (DPA + SCCs) |

### Google Vault (Enterprise)

| Capability | Description |
|------------|-------------|
| Retention rules | Apply retention policies to Gemini conversation data |
| Legal hold | Preserve AI interactions for legal proceedings |
| Search & export | Search Gemini conversations for eDiscovery |
| Audit trail | Track Vault actions on AI data |

---

## 8. Supported Editions

| Feature | Business Starter | Business Standard | Business Plus | Enterprise Standard | Enterprise Plus |
|---------|-----------------|-------------------|---------------|--------------------|-----------------| 
| Gemini in Workspace apps | ✓ | ✓ | ✓ | ✓ | ✓ |
| Gemini app (core) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Workspace Intelligence | ✓ | ✓ | ✓ | ✓ | ✓ |
| Gemini Enterprise (agents) | Add-on | Add-on | Add-on | ✓ | ✓ |
| NotebookLM Plus | Add-on | Add-on | Add-on | ✓ | ✓ |
| AI Control Center | ✗ | ✗ | ✗ | ✓ | ✓ |
| Workspace MCP Server | ✗ | ✗ | ✗ | ✓ | ✓ |
| Advanced DLP | ✗ | ✗ | ✗ | ✓ | ✓ |
| Google Vault | ✗ | ✗ | ✗ | ✓ | ✓ |
| Context-Aware Access | ✗ | ✗ | ✗ | ✓ | ✓ |
| FedRAMP High | ✗ | ✗ | ✗ | ✗ | ✓ |
| HIPAA (BAA) | ✗ | ✗ | ✗ | ✗ | ✓ |

---

## 9. Recommended Admin Configuration

### For regulated environments (finance, healthcare, government)

- [ ] Enforce 2-Step Verification for all users
- [ ] Configure Context-Aware Access (restrict to managed devices, corporate IPs)
- [ ] Disable Gemini app for users not requiring it
- [ ] Disable Workspace Intelligence for services containing sensitive data
- [ ] Configure DLP rules to block PII/PHI in AI prompts and responses
- [ ] Set data residency to required region
- [ ] Configure Vault retention rules for all Gemini interactions
- [ ] Restrict Gemini Enterprise agents to specific OUs
- [ ] Block Workspace data access from Gemini app
- [ ] Enable audit log export to SIEM
- [ ] Set custom alerts for anomalous AI usage
- [ ] Request BAA for HIPAA coverage (Enterprise Plus)
- [ ] Review and approve any third-party integrations via API controls
- [ ] Disable NotebookLM unless specifically approved
- [ ] Configure AI Control Center — review all security modules
- [ ] Apply classification labels to sensitive files to restrict AI access
- [ ] Configure trust rules to prevent AI-mediated oversharing
- [ ] Block Workspace MCP Server access for external AI agents (unless vetted)

### For standard enterprise teams

- [ ] Enforce 2-Step Verification
- [ ] Enable Gemini in Workspace apps for all users
- [ ] Enable Gemini app for all licensed users
- [ ] Configure Workspace Intelligence — enable Drive and Calendar, evaluate Gmail
- [ ] Set DLP rules for most sensitive content categories
- [ ] Enable audit logging and set up monthly review
- [ ] Assign Gemini Enterprise licenses to power users / agent builders
- [ ] Configure Google Vault retention per data policy
- [ ] Allow Gemini Enterprise to access Workspace data (with appropriate DLP)
- [ ] Review Gemini usage reports quarterly
- [ ] Review AI Control Center dashboard monthly
- [ ] Apply classification labels to confidential documents
- [ ] Vet and approve third-party AI apps via API controls before Workspace MCP access

### For smaller business teams

- [ ] Enable Gemini features across Workspace apps (default on)
- [ ] Enable Gemini app for all users
- [ ] Enable Workspace Intelligence for productivity
- [ ] Review user-facing smart features settings
- [ ] Monitor adoption via Admin reports
- [ ] Disable any services not relevant to your business

---

## Cross-References

- **API-level Gemini controls:** [`../google-gemini/`](../google-gemini/) — Safety settings, VPC controls, IAM policies for Gemini API
- **Gemini CLI controls:** [`../gemini-cli/`](../gemini-cli/) — Tool restrictions, sandbox configuration
- **Admin security policy:** [`../google-gemini/secure-admin-policy.md`](../google-gemini/secure-admin-policy.md)

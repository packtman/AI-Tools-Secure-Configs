# Cross-Tool SSO Deployment Checklist

A unified checklist for deploying SSO across Claude, Cursor, ChatGPT, and Gemini for a consistent identity posture.

---

## Prerequisites

- [ ] **Identity Provider configured** — Okta, Azure AD (Entra ID), Google Workspace, or OneLogin
- [ ] **SAML 2.0 metadata available** — IdP metadata URL or XML file ready
- [ ] **Domain ownership verified** — DNS TXT records in place for all corporate domains
- [ ] **Test users identified** — 2–3 users per tool for validation before enforcement
- [ ] **Rollback plan documented** — Steps to disable enforcement if issues arise

---

## Claude (Team/Enterprise)

### Setup

- [ ] Navigate to `claude.ai` → Admin Settings → Security → SSO
- [ ] Upload SAML metadata or configure IdP connection manually
- [ ] Map IdP groups to Claude roles (Primary Owner, Admin, Member)
- [ ] Verify domain(s) via DNS TXT record
- [ ] Enable SSO (non-enforced) and test with pilot users
- [ ] Enable domain capture to auto-claim new users

### Enforcement

- [ ] After validation, enable "Enforce SSO"
- [ ] Confirm email/password login is disabled for verified domain users
- [ ] Verify SCIM provisioning syncs users correctly (Enterprise)
- [ ] Document IdP group → Claude role mapping

### Shared Config Note

> SSO settings are **independent** — Claude SSO is configured separately from other tools.

---

## Cursor (Enterprise)

### Setup

- [ ] Navigate to `cursor.com/settings` → Security & Identity → SSO
- [ ] Configure SAML connection with IdP metadata
- [ ] Test SSO login with pilot admin and member accounts
- [ ] Enable SCIM provisioning and sync initial user set
- [ ] Verify directory groups sync for spend limits and access control

### Enforcement

- [ ] Enable "Require SSO for all team members"
- [ ] Deploy `AllowedTeamId` via MDM to lock device logins to your team
- [ ] Confirm local login is disabled for all team members
- [ ] Verify new users provisioned via SCIM get correct roles

### Device Enforcement

- [ ] Deploy MDM policy: `AllowedTeamId` = your team ID(s)
- [ ] Verify users cannot log in to unauthorized teams on managed devices

---

## ChatGPT (Business / Enterprise)

### Setup

- [ ] Navigate to `chatgpt.com/admin` → Identity & Provisioning
- [ ] Verify domain via DNS TXT record
- [ ] Configure SAML SSO connection with IdP
- [ ] Test SSO login with pilot users
- [ ] Enable SCIM directory sync and map IdP groups to ChatGPT groups

### Enforcement

- [ ] Enable "Enforce SSO" — disables social login (Google/Microsoft/Apple) for verified domains
- [ ] Restrict invites to verified domains only
- [ ] Configure IP allowlist for additional network-level restriction
- [ ] Verify deprovisioned IdP users lose ChatGPT access

### Shared Config Note

> ChatGPT and OpenAI API Platform share a **single SSO connection** with your IdP. Domain verifications and SAML settings are shared between products. If you configure SSO for one, the other inherits the configuration.

---

## Gemini (Google Workspace)

### Setup

- [ ] Navigate to `admin.google.com` → Security → Authentication → SSO with third-party IdP
  - **OR** use Google as the IdP (Workspace native authentication)
- [ ] If using third-party IdP: configure SAML 2.0 profile
- [ ] If using Google as IdP: configure 2-Step Verification enforcement
- [ ] Assign Gemini licenses to appropriate users/OUs

### Enforcement

- [ ] Enforce 2-Step Verification for all users (Admin → Security → 2SV)
- [ ] Configure Context-Aware Access policies (IP, device, location restrictions)
- [ ] Set session control duration (re-auth frequency)
- [ ] Verify Gemini access respects OU-level service enablement

### Platform Note

> Gemini inherits Google Workspace's authentication. If you already have SSO/MFA configured for Workspace, Gemini is automatically covered. No separate Gemini-specific SSO exists.

---

## Post-Deployment Validation (All Tools)

### Positive Tests

- [ ] **IdP-authenticated user can log in** to each tool
- [ ] **Group membership** correctly maps to roles/permissions
- [ ] **New provisioned user** (via SCIM) appears in each tool
- [ ] **Deprovisioned user** (removed from IdP group) loses access

### Negative Tests

- [ ] **Password-only login blocked** on tools with SSO enforced
- [ ] **Unauthorized domain email** cannot join workspaces
- [ ] **IP outside allowlist** denied (where applicable)
- [ ] **Unmanaged device** blocked (where Context-Aware Access configured)

### Ongoing

- [ ] **Quarterly access reviews** — verify role assignments match current org structure
- [ ] **IdP group hygiene** — remove departed employees promptly
- [ ] **SSO certificate rotation** — schedule before expiry (typically annual)
- [ ] **Audit log monitoring** — alert on failed SSO attempts or role escalations

---

## Troubleshooting Common Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Users stuck in login loop | Mismatched SAML assertion attributes | Verify `NameID` format matches tool expectation |
| SCIM sync fails silently | Bearer token expired or wrong endpoint | Regenerate SCIM token in tool admin |
| Existing users locked out after enforcement | User email doesn't match verified domain | Add user's domain or create exception |
| MFA prompt appears on every login | Session duration too short | Increase session validity in IdP |
| ChatGPT SSO breaks API Platform | Shared SSO config changed | Coordinate changes — they share one connection |

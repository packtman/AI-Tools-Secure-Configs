# Claude API — Settings Rationale

Every organization-level security setting explained: **what it does**, **why it matters**, and **the recommended value** by environment.

---

## 1. SSO Enforcement (SAML/OIDC)

**What it does:** Requires all console users to authenticate through your corporate identity provider instead of email/password.

**Why it matters:** Without SSO, users create independent passwords that are:
- Not covered by your corporate MFA policy
- Not revoked when the user leaves the organization
- Susceptible to credential stuffing and phishing

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All enterprise | Enforce SSO | Single point of authentication tied to your IdP. Offboarding revokes access immediately. |

---

## 2. SCIM Provisioning

**What it does:** Automates user lifecycle — creates accounts when users join and deprovisions when they leave.

**Why it matters:** Manual user management is error-prone. A forgotten account after an employee departure is a dormant access vector. SCIM ensures your IdP is the source of truth.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Enterprise | Enable | Automates onboarding/offboarding. Eliminates zombie accounts. |
| Small teams | Optional | Manual management is feasible below ~50 users. |

---

## 3. Organization Admin Minimization (≤ 3)

**What it does:** Limits how many people have full administrative control over the organization.

**Why it matters:** Org Admins can create/delete workspaces, manage all members, create admin API keys, and access compliance data. Each admin is a potential point of compromise.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| All | ≤ 3 named individuals | Minimum viable admin count. Document who they are and why. Review quarterly. |

**Risk if over-provisioned:** More admins = more targets for phishing. An admin API key created by a compromised account can exfiltrate all organization data.

---

## 4. Workspace Separation

**What it does:** Creates isolated boundaries with separate API keys, member lists, and rate limits.

**Why it matters:** Without workspace separation, a compromised API key gives access to the entire organization's models and data. Workspaces contain the blast radius.

| Architecture | Purpose | Reasoning |
|--------------|---------|-----------|
| `{team}-prod` | Production workloads | Strict access; only service accounts and on-call engineers. |
| `{team}-staging` | Pre-production testing | Broader access; lower rate limits than prod. |
| `sandbox` | Experimentation | Open access; strict spend caps to prevent cost surprises. |

---

## 5. Role Assignment (Workspace Roles)

**What it does:** Controls what each member can do within a workspace.

| Role | Can call models | Can manage keys | Can manage members | Reasoning for default |
|------|----------------|-----------------|--------------------|-----------------------|
| User | Yes | No | No | **Default for all new members.** Minimum access to use the API. |
| Developer | Yes | Yes | No | For service owners who need to create/rotate keys. |
| Admin | Yes | Yes | Yes | For workspace leads who manage team membership. |

**Why least privilege matters:** A Developer who doesn't need to create API keys shouldn't have that permission. A compromised Developer account with key-creation rights can create new keys that survive password resets.

---

## 6. API Key Rotation (90/60 Day Schedule)

**What it does:** Forces periodic replacement of API keys.

**Why it matters:** Keys are bearer tokens — anyone who has the key has access. Over time, keys leak through logs, debugging sessions, screenshots, and configuration drift. Rotation limits the exposure window.

| Key type | Interval | Reasoning |
|----------|----------|-----------|
| Standard API (`sk-ant-api03-*`) | 90 days | Balances security with operational burden. Service owners can automate. |
| Admin API (`sk-ant-admin01-*`) | 60 days | Higher privilege = shorter rotation. Admin keys can do everything. |
| Compliance (`sk-ant-api01-*`) | 90 days | Used by security tooling; typically automated. |

**What happens without rotation:** A key leaked 6 months ago still works. You have no way to know it was compromised until it's used maliciously.

### API Key Expiration

**What it does:** Sets an `expires_at` timestamp when creating API keys and Admin API keys. Keys can also be created with no expiration (`expires_at: null`) if "Never" is selected.

**Why it matters:** Expiration converts key lifecycle from an honor-system rotation process into an enforced control. A forgotten key eventually stops working instead of remaining valid indefinitely.

| Environment | `api_key_expiration_required` | `allow_never_expiring_keys` | Reasoning |
|-------------|-------------------------------|-----------------------------|-----------|
| Baseline | `false` | `true` | Keeps low-friction startup workflows, but admins should still inventory long-lived keys. |
| Moderate | `true` | `false` | Enterprise keys should expire on schedule and use the `expires_at` field for alerting. |
| Strict | `true` | `false` | Regulated environments should not allow indefinite bearer tokens. |

**What breaks if too strict:** Services with manual secret rotation can fail when a key expires. Mitigate by alerting owners at least 14 days before expiration and testing rotation in staging.

---

## 7. Rate Limits & Spend Controls

**What it does:** Caps the number of API requests and the dollar amount per workspace per period.

**Why it matters:** Without limits:
- A bug in application code can make unlimited API calls, running up a massive bill
- A compromised API key can be used at full capacity for abuse
- One team's spike can degrade service for the whole organization

| Control | Purpose | Reasoning |
|---------|---------|-----------|
| `requests_per_minute` | Prevents runaway loops | A tight RPM cap stops bugs before they get expensive. |
| `tokens_per_minute` | Prevents token-heavy abuse | Large prompts consume more budget per request. |
| `monthly_budget_usd` | Hard cost boundary | CFO-friendly: maximum spend is guaranteed. |
| `alert_thresholds` (50/75/90%) | Early warning | Time to investigate before the cap is hit. |

### Model Group Rate Limits

**What it does:** The Rate Limits API can return entries with `group_type: "model_group"`, meaning the limit applies to a family of models listed in the response.

**Why it matters:** New models may share a rate-limit bucket. Admins should alert and capacity-plan by model group, not only by individual model name.

| Environment | Recommended handling |
|-------------|----------------------|
| Baseline | Review model-group limits during monthly spend checks. |
| Moderate | Track model-group limits per workspace and alert on saturation. |
| Strict | Require approval before adding models to production workloads if they share a constrained model group. |

---

## 7.1 MCP Tunnels

**What it does:** MCP tunnels expose internal MCP servers through Anthropic-assigned tunnel domains. The research-preview API uses the `mcp-tunnels-2026-06-22` beta header and WIF scope `workspace:manage_tunnels`. Older Admin API integrations used `mcp-tunnels-2026-05-19` and `org:manage_tunnels` during the migration window.

**Why it matters:** A tunnel bridges external Claude API infrastructure to an internal tool server. Tunnel tokens are credentials, and registered CA certificates define which internal gateway is trusted.

| Environment | `mcp_tunnels.enabled` | Token rotation | Certificate rotation | Reasoning |
|-------------|-----------------------|----------------|----------------------|-----------|
| Baseline | `false` | 30 days if approved | 90 days if approved | Research-preview tunnels require explicit opt-in even in flexible environments. |
| Moderate | `false` | 30 days if approved | 90 days if approved | Standard enterprise needs workspace owner approval, WIF scope review, and SIEM alerts first. |
| Strict | `false` | 14 days if approved | 60 days if approved | Regulated environments should avoid tunnel exposure unless a compensating control package is approved. |

**What breaks if enabled without review:** Internal tools can become reachable through a tunnel domain, tunnel tokens can be mishandled like static secrets, and certificate expiry can break MCP traffic unexpectedly.

---

## 7.2 Release Note Terms With No Org Policy Change

| Term | Triage |
|------|--------|
| `fast-mode-2026-02-01` | Fast mode is a premium model speed feature controlled by request headers and account access. Keep disabled unless an API gateway or workload owner explicitly approves premium usage. |
| `mcp_oauth` | Applies to Claude Managed Agents vault credentials. It is relevant only if Managed Agents are deployed, not to the base Claude API org-policy examples. |
| `LanguageModel` / `LanguageModelSession` | Swift SDK type names for Apple Foundation Models integration. No organization policy setting is required. |
| `model_context_window_exceeded` | Error/event naming for context-window handling. Monitor if useful, but no config template change is needed. |
| `policy_violation_investigation` | CMEK content preservation reason code. Security teams should recognize it in logs, but it is not a rollout config key. |

---

## 8. Compliance API & Activity Feed

**What it does:** Streams a feed of all organization events — API key creation, member changes, login events, configuration changes.

**Why it matters:** You cannot detect threats you cannot see. The Compliance API provides the audit trail needed for:
- **Incident response** — Who did what, when?
- **Regulatory compliance** — SOC 2, HIPAA, GDPR all require audit logs.
- **Anomaly detection** — Unusual key creation patterns, off-hours access, geographic anomalies.

| Environment | Recommended | Reasoning |
|-------------|-------------|-----------|
| Enterprise | Enable and stream to SIEM | Visibility is non-negotiable for compliance. |
| Small teams | Enable at minimum | Even without SIEM, the audit trail helps in incident response. |

---

## 9. Data Retention & Training Opt-Out

**What it does:** Controls whether Anthropic retains your prompts/responses and whether they're used for model training.

**Why it matters:** API data is NOT used for training by default (unlike the free consumer product). But you should verify this setting and document it for your compliance team.

| Setting | Recommended | Reasoning |
|---------|-------------|-----------|
| Training opt-out | Verify enabled (API default) | Your code and prompts must not train public models. |
| Prompt logging | Decide per use case | Log metadata only for compliance; full logs increase data exposure. |

---

## 10. Network Security (IP Allowlist, Proxy)

**What it does:** Restricts which IP addresses can make API calls.

**Why it matters:** A stolen API key used from an unknown IP address is a clear indicator of compromise. IP allowlisting ensures that even if a key leaks, it can only be used from your network.

| Control | Reasoning |
|---------|-----------|
| IP allowlist | Contains key theft to your network. Include VPN and CI/CD runner IPs. |
| Proxy routing | Gives your security team visibility into all API traffic. |
| TLS enforcement | Default; never override. All data in transit is encrypted. |

**Risk without allowlisting:** A leaked key can be used from anywhere in the world with no restrictions.

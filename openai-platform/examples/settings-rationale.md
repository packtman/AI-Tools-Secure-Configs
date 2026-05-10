# OpenAI Platform — Security Settings Rationale

A comprehensive explanation of every security-relevant setting on the OpenAI platform.
For each setting: what it does, why it matters, recommended values per environment, and failure modes when misconfigured.

---

## 1. Organization Roles

The organization level is the top of the OpenAI hierarchy. Every member belongs to the organization and is assigned exactly one organization-level role.

### Role Definitions

| Role | Capabilities | Risk level |
|------|-------------|------------|
| **Owner** | Full administrative control — billing, SSO, IP allowlists, audit logs, project creation, member management, Admin API key creation | Critical |
| **Reader** | View-only access to organization settings, members list, and billing overview | Low |

### Why Limit Owners to ≤ 3

| Factor | Explanation |
|--------|-------------|
| **Blast radius** | Every Owner can unilaterally change SSO settings, disable IP allowlists, create Admin API keys, or delete projects. More Owners means more vectors for accidental or malicious configuration changes. |
| **Accountability** | With many Owners it becomes impossible to attribute who changed a critical setting. Audit logs show the actor, but triage is faster when the set of possible actors is small. |
| **Social engineering** | Attackers target high-privilege accounts. Fewer Owners means a smaller target surface for phishing and credential-stuffing attacks. |
| **Compliance** | SOC 2, ISO 27001, and FedRAMP all require documented justification for administrative access and review of privileged accounts. A small, named set of Owners is easier to govern. |

### Recommended Values

| Environment | Max Owners | Rationale |
|-------------|-----------|-----------|
| Production org | 2–3 | Two for redundancy; three if teams span time zones |
| Sandbox / dev org | 1–2 | Lower-risk environment, fewer controls needed |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| > 5 Owners | Impossible to enforce change-management processes; any Owner can silently modify SSO, billing, or IP rules |
| 1 Owner | Single point of failure — if that person leaves or loses access, the organization is locked out |
| Using Owner role for day-to-day work | Accidental changes to org-wide settings; violates least-privilege |

---

## 2. Project-Level Roles

Projects are the primary isolation boundary for API keys, spending limits, rate limits, and member access.

### Role Definitions

| Role | Capabilities | Typical assignee |
|------|-------------|-----------------|
| **Owner** | Manage project members, create/revoke API keys, configure project settings, view usage | Tech lead, platform engineer |
| **Member** | Use the API within the project scope, view own usage | Application developer, data scientist |
| **Viewer** | View-only access to project resources and usage | Auditor, observer |

### Least-Privilege Principle

Default every new user to **Member**. Promote to Owner only when the person has an explicit operational need (key rotation, onboarding teammates). Document every Owner assignment with a ticket or approval record.

### Recommended Values

| Environment | Default role | Admin ratio |
|-------------|-------------|-------------|
| Production | Member | ≤ 2 Admins per project |
| Staging | Member | ≤ 3 Admins per project |
| Sandbox | Member | More relaxed, but still explicit assignment |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| Everyone is Admin | Any team member can create or revoke API keys, change rate limits, or remove other members — accidental key deletion causes outages |
| No Admin assigned | No one can rotate keys or onboard new members; operational bottleneck |
| Shared project across teams | One team's key leak or spending spike affects the other team's workloads |

---

## 3. Custom RBAC Roles

OpenAI supports custom roles with granular permission scopes beyond the preset Owner/Reader/Admin/Member roles.

### Available Permission Scopes

Custom roles can combine granular permissions for delegated administration. Note that some security-critical operations (IP allowlists, mTLS, OIDC) are restricted to organization Owners and cannot be delegated via custom roles.

| Permission scope | Controls | Use case |
|-----------------|----------|----------|
| `admin` | Subset of administrative operations | Delegated admin for specific functions |
| `billing` | View and manage billing | Finance team oversight |
| `projects` | Create and manage projects | Platform team managing project lifecycle |

### Why Custom Roles Matter

| Factor | Explanation |
|--------|-------------|
| **Separation of duties** | The person managing IP allowlists should not necessarily have billing access. Custom roles enforce this boundary. |
| **Audit clarity** | When a role is scoped to a single function, any action taken by that role is immediately attributable to a specific responsibility. |
| **Compliance** | Regulatory frameworks require demonstrable least-privilege. Custom roles provide the evidence. |
| **Operational safety** | Limiting what each person can change reduces the blast radius of compromised credentials. |

### Recommended Values

| Custom role | Permissions | Assign to |
|------------|------------|-----------|
| Project Manager | `projects`, `admin` | Platform engineering team |
| Audit Reviewer | Read-only audit logs | Compliance and security operations |
| Billing Viewer | Read-only `billing` | Finance team |

> **Note:** IP allowlist, mTLS, and OIDC management require the Owner role and cannot be assigned via custom roles.

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| Not creating custom roles | Forces over-use of the Owner role for delegated tasks |
| Overly broad custom roles | Defeats the purpose — equivalent to granting Owner |
| Not reviewing custom role assignments | Stale assignments accumulate; former team members retain access they no longer need |

---

## 4. API Key Types

### Key Type Comparison

| Key type | Prefix | Scope | Creates via | Rotation owner |
|----------|--------|-------|------------|----------------|
| **Admin API key** | `sk-admin-*` | Organization-wide | Dashboard (Owners only) | Organization Owner |
| **Project API key** | `sk-proj-*` | Single project | Dashboard or Admin API | Project Admin |
| **Service account key** | `sk-svcacct-*` | Single project | Dashboard or Admin API | Service owner / automation |

### When to Use Each

| Key type | Use when | Never use when |
|----------|----------|---------------|
| Admin API key | Automating user/project management, running IaC (Terraform) against the OpenAI Admin API | Serving inference traffic, embedding in application code |
| Project API key | Quick prototyping by a named developer, interactive use | CI/CD pipelines, shared services (use service accounts instead) |
| Service account key | Production inference, CI/CD pipelines, any automated system | Personal development (use project keys tied to your identity) |

### Rotation Schedule Rationale

| Key type | Interval | Why |
|----------|----------|-----|
| Admin API key | **60 days** | Highest privilege, highest risk. Shorter rotation limits the window of exposure if a key is compromised. Cannot be recovered if lost, so rotation also tests your recovery process. |
| Project API key | **90 days** | Moderate risk. Scoped to one project, so blast radius is contained. 90 days balances operational burden with security hygiene. |
| Service account key | **90 days** | Same risk profile as project keys. Automated rotation via secrets manager (Vault, AWS Secrets Manager) should make this painless. |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| Using Admin keys for inference | A leaked key grants full org control — attacker can create new projects, exfiltrate data, change SSO settings |
| Sharing one Project key across multiple services | When the key is rotated or revoked, all services break simultaneously; no way to attribute usage to a specific service |
| Never rotating keys | A compromised key remains valid indefinitely; attacker has persistent access |
| Storing keys in source code | Keys end up in git history, CI logs, and container images — extremely difficult to fully revoke exposure |

---

## 5. SSO / OIDC Enforcement

### What It Does

SSO/OIDC enforcement requires all organization members to authenticate through your corporate identity provider (Okta, Azure AD, Google Workspace, etc.) instead of using standalone OpenAI passwords.

### Why It Matters

| Factor | Explanation |
|--------|-------------|
| **Centralized identity** | User lifecycle management (onboarding, offboarding, role changes) happens in one place. Disabling an IdP account immediately revokes OpenAI access. |
| **MFA inheritance** | Your IdP's MFA policy (hardware keys, push notifications) applies to OpenAI access automatically. |
| **Password elimination** | No OpenAI-specific passwords means no OpenAI-specific password leaks. |
| **Session control** | IdP session policies (timeout, re-authentication) apply, giving you control over session duration. |
| **Compliance** | SOC 2 CC6.1 and ISO 27001 A.9.2 require centralized access management. SSO satisfies these controls. |

### Why Password-Only Is Dangerous

| Risk | Detail |
|------|--------|
| Credential stuffing | Users reuse passwords; breached credentials from other services grant OpenAI access |
| No centralized revocation | Offboarding requires manually removing the user from OpenAI — easy to forget |
| Weak MFA | OpenAI's built-in MFA is less configurable than enterprise IdP MFA (no hardware key enforcement) |
| Shadow accounts | Users can sign up with personal emails, creating unmanaged accounts |

### Recommended Values

| Environment | Setting |
|-------------|---------|
| All environments | SSO enforced, password login disabled |
| IdP provider | Okta, Azure AD, or Google Workspace with hardware-key MFA |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| SSO enabled but not enforced | Users can bypass SSO and log in with passwords |
| No IdP MFA policy | SSO without MFA is barely better than passwords |
| Not configuring SCIM provisioning | User deprovisioning is manual and error-prone |

---

## 6. IP Allowlisting

### What It Does

Restricts which source IP addresses can make API calls using your organization's keys. Requests from non-listed IPs are rejected with `403 Forbidden`.

### Why It Matters

| Factor | Explanation |
|--------|-------------|
| **Stolen key mitigation** | Even if an API key is leaked, it cannot be used from outside your network. This is the single most effective control against key theft. |
| **Blast radius reduction** | Limits where an attacker can operate, even if they compromise a developer workstation. |
| **Compliance** | PCI DSS 1.3 and SOC 2 CC6.6 require network-level access controls. |

### How to Scope

| IP source | Include? | Notes |
|-----------|----------|-------|
| Corporate office egress | Yes | Primary development and operations traffic |
| VPN egress | Yes | Remote developer access |
| CI/CD runner IPs | Yes | GitHub Actions, GitLab CI, Jenkins — use static IPs or NAT gateways |
| Cloud NAT gateways | Yes | Production services calling OpenAI from cloud environments |
| Developer home IPs | No | Dynamic, unmanaged — require VPN instead |
| `0.0.0.0/0` | Never | Disables the allowlist entirely |

### Recommended Values

| Environment | IP allowlist |
|-------------|-------------|
| Production | Cloud NAT gateway CIDRs + CI/CD runner IPs only |
| Staging | Same as production + VPN egress |
| Development | VPN egress + office egress |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| Allowlist not enabled | Stolen keys work from anywhere in the world |
| Overly broad CIDR (`/8` or `/16`) | Millions of IPs are permitted; effectively no restriction |
| Stale IPs after infra migration | Legitimate traffic blocked; production outage |
| Not including CI/CD IPs | Automated deployments and tests fail |
| Enabling enforcement without testing | Immediate lockout if the list is incomplete — test with `enforced: false` first |

---

## 7. Mutual TLS (mTLS)

### What It Does

Requires API clients to present a valid client certificate signed by a CA you upload to OpenAI. The server verifies the certificate before processing the request.

### When It's Worth the Complexity

| Scenario | Use mTLS? | Rationale |
|----------|-----------|-----------|
| High-value production inference | Yes | Defense-in-depth: even a stolen API key + allowed IP cannot succeed without the client certificate |
| Regulated industries (finance, healthcare) | Yes | Regulatory frameworks often require mutual authentication |
| Internal tooling / prototyping | No | Operational overhead outweighs the risk reduction |
| CI/CD pipelines | Maybe | Worth it if the pipeline runs in a high-trust environment where certificate distribution is easy |

### Why It Matters

| Factor | Explanation |
|--------|-------------|
| **Three-factor API auth** | API key (something you have) + IP allowlist (somewhere you are) + client certificate (something you prove) |
| **Certificate revocation** | Compromised clients can be revoked at the CA level without rotating API keys |
| **Non-repudiation** | Client certificates provide stronger identity binding than API keys alone |

### Recommended Values

| Environment | mTLS | Certificate rotation |
|-------------|------|---------------------|
| Production | Enabled | 1-year certificates, rotate 30 days before expiry |
| Staging | Optional | Same CA, shorter-lived certificates (90 days) |
| Development | Disabled | Use IP allowlisting instead |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| Expired client certificate | All API calls fail; production outage |
| CA certificate not rotated | When the CA expires, all client certificates become invalid simultaneously |
| Client key stored insecurely | Attacker with the key + cert can bypass mTLS — store private keys in HSM or secrets manager |
| mTLS enabled without monitoring | Certificate expiry goes unnoticed until it causes an outage |

---

## 8. Audit Logging

### What It Does

Records administrative and operational events across your organization. Events are available via the dashboard and can be exported to external systems.

### What Events Matter

| Event category | Examples | Why it matters |
|---------------|----------|---------------|
| **Authentication** | Login success/failure, SSO events, MFA challenges | Detect credential-stuffing attempts, identify compromised accounts |
| **API key lifecycle** | Key creation, rotation, deletion | Track who created keys and when — critical for incident response |
| **Member management** | User added/removed, role changed | Detect unauthorized privilege escalation |
| **Organization settings** | SSO config changed, IP allowlist modified, mTLS updated | Any change to security controls must be auditable |
| **Project management** | Project created/deleted, budget changed | Track structural changes that affect isolation boundaries |
| **API usage anomalies** | Unusual token volumes, new model access, off-hours usage | Early warning of key compromise or insider threat |

### Retention

| Consideration | Recommendation |
|--------------|----------------|
| Minimum retention | 90 days in OpenAI + forwarded to your SIEM |
| Compliance retention | 1 year (SOC 2), 7 years (financial regulations) — retain in your SIEM, not OpenAI |
| Cost vs. coverage | Longer retention increases storage cost but reduces risk of losing forensic evidence |

### SIEM Integration

| Integration step | Detail |
|-----------------|--------|
| Export method | OpenAI Audit Log API → your ingestion pipeline |
| Recommended SIEMs | Splunk, Datadog, Elastic, Sentinel, Chronicle |
| Alert rules | Failed login > 5 in 10 min, Admin key created, IP allowlist modified, Owner role granted |
| Dashboard | Visualize API key creation rate, role changes over time, login geography |

### Recommended Values

| Environment | Audit logging | Export to SIEM | Alert rules |
|-------------|--------------|----------------|-------------|
| Production | Enabled | Yes — real-time | Full set (auth, keys, settings, usage) |
| Staging | Enabled | Yes — batch (daily) | Subset (auth, key creation) |
| Development | Enabled | Optional | Minimal (Owner role grants only) |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| Audit logging disabled | No forensic evidence after a breach — cannot determine what was accessed or changed |
| Logs not exported | OpenAI's retention is limited; logs may age out before an incident is detected |
| No alert rules | Events are recorded but nobody notices — detection time increases from minutes to weeks |
| Over-logging (prompts/responses) | PII and sensitive data in logs creates a secondary data-breach surface |

---

## 9. Data Retention Settings

### What It Does

Controls how long OpenAI retains API request and response data. Configurable in Organization Settings → Data Controls.

### Privacy vs. Compliance Tradeoffs

| Setting | Privacy benefit | Compliance risk |
|---------|----------------|-----------------|
| **Zero-day retention** (delete immediately) | Maximum privacy — data never stored at rest on OpenAI servers | Cannot replay requests for debugging; no data available for abuse investigations |
| **30-day retention** (default) | Moderate privacy — data available for short-term debugging and abuse review | Sufficient for most compliance frameworks; may conflict with strict data-residency rules |
| **Extended retention** | Lowest privacy — data persists longer | Enables deeper usage analytics and abuse investigations; may conflict with GDPR minimization principle |

### Recommended Values

| Environment | Retention | Rationale |
|-------------|-----------|-----------|
| Production (regulated) | Zero-day or minimal | Minimize data exposure; rely on your own logging infrastructure |
| Production (standard) | 30 days | Balance between debugging capability and privacy |
| Staging / dev | 30 days | Useful for debugging and iteration |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| Retention too long in regulated environment | Violates data-minimization requirements (GDPR Art. 5(1)(c), CCPA) |
| Retention at zero with no local logging | Cannot investigate production issues or abuse |
| Not reviewing retention settings after policy changes | Organization privacy policy says "no data retained" but OpenAI setting is still at 30 days |
| Training data opt-out not confirmed | API data is not used for training by default, but failing to verify this assumption creates risk |

---

## 10. Content Moderation (Pre/Post Checking)

### What It Does

Calls the `/v1/moderations` endpoint to classify content against safety categories (hate, self-harm, sexual, violence, etc.). Can be applied to user inputs (pre-check) and model outputs (post-check).

### Why Both Matter

| Check | Purpose | What it catches |
|-------|---------|----------------|
| **Pre-check (input)** | Prevent harmful prompts from reaching the model | Prompt injection attacks, abusive user content, attempts to generate harmful outputs |
| **Post-check (output)** | Catch harmful content the model may generate despite safety training | Edge-case harmful outputs, hallucinated PII, content that violates your organization's policy |

### Why Pre-Check Alone Is Not Enough

A benign-looking input can produce harmful output through indirect prompt injection, multi-turn context accumulation, or model behavior changes after fine-tuning. Post-checking is the safety net.

### Why Post-Check Alone Is Not Enough

Blocking harmful outputs after generation still costs tokens and latency. Pre-checking rejects bad inputs early, saving resources and preventing the model from processing abusive content at all.

### Recommended Values

| Environment | Pre-check | Post-check | Threshold | Blocked categories |
|-------------|-----------|------------|-----------|-------------------|
| Production (consumer-facing) | Enabled | Enabled | 0.7 | All categories |
| Production (internal tools) | Enabled | Enabled | 0.8 | All categories |
| Staging | Enabled | Enabled | 0.5 (stricter for testing) | All categories |
| Red-team / adversarial testing | Disabled | Logging only | N/A | None blocked, all logged |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| No pre-check | Abusive inputs consume tokens and may produce harmful outputs |
| No post-check | Harmful model outputs reach end users |
| Threshold too low (0.3) | High false-positive rate; legitimate content blocked; user frustration |
| Threshold too high (0.95) | Harmful content slips through; moderation is effectively disabled |
| Categories not updated | New moderation categories added by OpenAI are not blocked |

---

## 11. PII Handling

### What It Does

Application-layer controls that scan inputs for personally identifiable information, block requests containing sensitive data, and redact PII before it reaches the API.

### Scan → Block → Redact Strategy

| Stage | Action | Purpose |
|-------|--------|---------|
| **Scan** | Detect PII patterns (SSN, credit card, passport, email, phone) in every request | Know what sensitive data is flowing to the API |
| **Block** | Reject requests containing high-sensitivity PII (SSN, credit card, bank account) | Prevent the most damaging data from ever leaving your environment |
| **Redact** | Replace detected PII with placeholder tokens before sending | Allow the request to proceed with sensitive data removed — preserves functionality |

### Why This Order Matters

Scanning first gives visibility. Blocking prevents the worst outcomes. Redacting handles the gray area where data is sensitive but the request is still valuable. Skipping any stage creates a gap.

### Recommended Values

| PII category | Action | Rationale |
|-------------|--------|-----------|
| SSN / national ID | Block | No legitimate reason to send to an LLM |
| Credit card number | Block | PCI DSS prohibits sending to third parties without controls |
| Bank account number | Block | Financial data exfiltration risk |
| Passport number | Block | Government ID — no LLM use case justifies the risk |
| Email address | Redact | Often needed for context but should not be stored by OpenAI |
| Phone number | Redact | Moderate sensitivity — redact unless required |
| Full name | Log + warn | Low sensitivity, but track for privacy compliance |
| IP address | Log + warn | May be needed for technical contexts |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| No PII scanning | Sensitive data sent to OpenAI without awareness; compliance violations |
| Block-only (no redact) | High rejection rate; developers bypass controls by removing PII manually (inconsistently) |
| Redact-only (no block) | High-sensitivity data (SSN, credit card) gets replaced but the pattern might be incomplete — false negatives |
| Not logging PII incidents | No visibility into how often sensitive data flows through; cannot prove compliance |

---

## 12. Project Budget Isolation

### What It Does

Sets per-project monthly spending limits. When a project reaches its limit, API requests return `429 Too Many Requests` until the next billing cycle or the limit is raised.

### Why Per-Project Limits Prevent Runaway Costs

| Factor | Explanation |
|--------|-------------|
| **Blast radius containment** | A bug in one service that generates infinite API calls only exhausts that project's budget, not the entire organization's |
| **Cost attribution** | Per-project spending makes it trivial to identify which team or service is driving costs |
| **Accountability** | Teams own their budgets; no tragedy-of-the-commons on a shared pool |
| **Early warning** | Budget alerts at 50%, 75%, 90% give teams time to investigate before hitting the hard limit |

### Recommended Values

| Environment | Budget | Alert thresholds | Rationale |
|-------------|--------|-------------------|-----------|
| Production | Based on historical usage + 20% buffer | 50%, 75%, 90% | Enough headroom for traffic spikes; alerts catch anomalies |
| Staging | 10–20% of production budget | 75%, 90% | Lower traffic; tighter limits acceptable |
| Sandbox / dev | $100–500/month | 90% only | Prevent experimentation from generating surprise bills |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| No per-project limits | A single runaway service can exhaust the entire org budget in hours |
| Limits too tight | Legitimate traffic gets throttled during peak usage; production outage |
| Limits too loose | No effective cost control; budget overruns discovered only at invoice time |
| No billing alerts | Team hits the hard limit with no warning; API calls suddenly fail |
| All teams share one project | Cannot attribute costs; one team's spike blocks another team's service |

---

## 13. Rate Limiting

### What It Does

Controls the maximum number of API requests per minute (RPM) and tokens per minute (TPM) at the project level.

### Why Per-Project Rate Limits Matter

| Factor | Explanation |
|--------|-------------|
| **Noisy-neighbor prevention** | Without per-project limits, one project's traffic spike degrades performance for all projects in the organization |
| **Abuse containment** | If a key is compromised, rate limits bound the attacker's throughput |
| **Predictable performance** | Each project gets a guaranteed allocation; capacity planning is meaningful |
| **Cost correlation** | Rate limits and budget limits work together — rate limits prevent cost spikes within a billing period |

### Recommended Values

| Environment | RPM | TPM | Rationale |
|-------------|-----|-----|-----------|
| Production (high-traffic) | 500–2,000 | 200,000–1,000,000 | Based on measured P99 traffic + headroom |
| Production (low-traffic) | 50–200 | 50,000–200,000 | Sufficient for internal tools and batch workloads |
| Staging | 100 | 50,000 | Enough for integration testing; prevents accidental load |
| Sandbox / dev | 20 | 10,000 | Tight limits prevent experimentation from consuming shared quota |

### What Goes Wrong

| Misconfiguration | Consequence |
|-----------------|-------------|
| No per-project rate limits | One project monopolizes the org's rate limit allocation; other projects get throttled |
| Limits too low for production | Legitimate traffic gets `429` responses; user-facing degradation |
| Limits too high | No effective protection against runaway costs or compromised keys |
| Not monitoring 429 rates | Rate limiting is working but nobody notices — silent service degradation |
| RPM set without TPM (or vice versa) | A few large requests can exhaust token budget while staying under RPM, or many small requests can exhaust RPM while staying under TPM |

---

## Summary Matrix

| Setting | Dev | Staging | Production | Regulated Production |
|---------|-----|---------|------------|---------------------|
| Org Owners | 1–2 | 2–3 | 2–3 | 2–3 + named justification |
| Project role default | Member | Member | Member | Member |
| Custom RBAC | Optional | Recommended | Required | Required |
| API key type | Project key | Service account | Service account | Service account |
| Key rotation | 90 days | 90 days | 90 days (proj) / 60 days (admin) | 60 days (all) |
| SSO/OIDC | Enforced | Enforced | Enforced | Enforced + hardware MFA |
| IP allowlist | VPN + office | VPN + office + CI/CD | NAT + CI/CD | NAT + CI/CD (minimal) |
| mTLS | Disabled | Optional | Recommended | Required |
| Audit logging | Enabled | Enabled + SIEM (batch) | Enabled + SIEM (real-time) | Enabled + SIEM + alerting |
| Data retention | 30 days | 30 days | 30 days or zero-day | Zero-day |
| Content moderation | Pre + post | Pre + post | Pre + post | Pre + post + logging |
| PII handling | Scan + warn | Scan + block critical | Scan + block + redact | Scan + block + redact + log |
| Project budget | $200/mo | $1,000/mo | Based on usage + 20% | Based on usage + 10% |
| Rate limits | 20 RPM | 100 RPM | Based on P99 traffic | Based on P99 + alerting |

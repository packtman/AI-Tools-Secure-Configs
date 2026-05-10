# Google Gemini — Enterprise Security Settings Rationale

Every setting below explains **what it controls**, **why it matters**, the **recommended value**, and the **risk of misconfiguration**. An admin reading this should understand the reasoning behind each recommendation, not just the value to set.

---

## 1. Safety Filter Categories

Safety filters are applied **per API request** using the `safety_settings` array. They are your primary defense against the model generating harmful content.

| Category | What it blocks | Recommended threshold | Why this threshold |
|----------|---------------|----------------------|-------------------|
| `HARM_CATEGORY_HARASSMENT` | Threats, bullying, intimidation, identity attacks | `BLOCK_MEDIUM_AND_ABOVE` | Blocks content with a reasonable probability of being harmful while allowing legitimate workplace discussions that may touch on conflict resolution or HR topics. |
| `HARM_CATEGORY_HATE_SPEECH` | Content promoting violence or discrimination based on protected attributes | `BLOCK_MEDIUM_AND_ABOVE` | Prevents generation of discriminatory content. Low-confidence false positives (blocked by `BLOCK_LOW_AND_ABOVE`) would interfere with DEI training materials or policy discussions. |
| `HARM_CATEGORY_SEXUALLY_EXPLICIT` | Sexual content, graphic descriptions | `BLOCK_MEDIUM_AND_ABOVE` | Enterprise environments have zero tolerance for explicit content. Medium threshold catches clear violations without blocking medical, educational, or HR-related content. |
| `HARM_CATEGORY_DANGEROUS_CONTENT` | Instructions for weapons, self-harm, illegal activities | `BLOCK_MEDIUM_AND_ABOVE` | Blocks genuinely dangerous instructions while permitting security research discussions, penetration testing guidance, and incident response content. |

### Threshold Comparison

| Threshold | Behavior | Enterprise use case |
|-----------|----------|-------------------|
| `BLOCK_NONE` | No filtering | **Never use in production.** Only for red-team testing in isolated environments. |
| `BLOCK_ONLY_HIGH` | Blocks only high-confidence harmful content | Too permissive — medium-confidence harmful content passes through. |
| `BLOCK_MEDIUM_AND_ABOVE` | Blocks medium and high confidence | **Enterprise default.** Best balance of safety and usability. |
| `BLOCK_LOW_AND_ABOVE` | Blocks low, medium, and high confidence | Regulated industries (healthcare, education for minors). Expect higher false-positive rates. |

### Misconfiguration Risk

Setting filters to `BLOCK_NONE` or `BLOCK_ONLY_HIGH` exposes the organization to generated harassment, hate speech, or dangerous instructions. This creates legal liability, HR violations, and reputational damage. Filters must be set **in application code on every request** — they are not server-side defaults.

---

## 2. Built-in Protections (Non-Configurable)

| Protection | What it does | Why it cannot be adjusted |
|-----------|-------------|--------------------------|
| Child Safety (CSAM) | Blocks generation and detection of child sexual abuse material | Legal obligation under federal law (18 U.S.C. § 2256). Google enforces this at the model layer with no override. |
| PII in training data | Google does not train on API request/response data for Gemini API | Contractual commitment under the Cloud Data Processing Addendum. Eliminates risk of proprietary data leaking into model weights. |
| Prompt injection defenses | Built-in detection of adversarial prompts attempting to override system instructions | Reduces (but does not eliminate) the risk of jailbreaks. Applications must still implement their own input validation. |

### Why this matters

These protections exist because certain safety guarantees must be unconditional. An administrator cannot accidentally weaken them, and an attacker cannot social-engineer their removal. However, **do not rely solely on built-in protections** — defense-in-depth requires application-layer checks as well.

---

## 3. Admin Settings (Project-Level)

Configure via the GCP Console or `gcloud` CLI per project.

| Setting | What it controls | Recommended value | Why | Misconfiguration risk |
|---------|-----------------|-------------------|-----|----------------------|
| `logging_enabled` | Whether Gemini prompts and responses are logged to Cloud Logging | `false` | Prompts frequently contain proprietary source code, architecture details, and internal documentation. Logging them creates a high-value target for attackers and may violate data handling policies. | If `true`, prompts containing trade secrets, customer data, or credentials are written to Cloud Logging, expanding the data breach surface. |
| `data_sharing_enabled` | Whether interaction data is shared with Google to improve models | `false` | Enterprise code and queries must not be used for model training. Even anonymized data can leak patterns. | If `true`, proprietary code patterns and business logic may influence future model outputs accessible to other customers. |
| `release_channel` | GA (stable) vs Preview (early features) | `GA` | Preview features have not completed Google's full security review and may have undiscovered vulnerabilities or behavioral regressions. | Using `Preview` in production means untested features may generate unexpected outputs or have undocumented data handling. |
| `code_customization_enabled` | Whether Gemini Code Assist uses organization-specific code for fine-tuning | `false` (until validated) | Code customization indexes your private repositories. Enable only after confirming the indexing pipeline meets your data classification requirements. | If enabled prematurely, code from restricted repositories may be indexed and surfaced to users without appropriate clearance. |

---

## 4. VPC Service Controls

VPC Service Controls create a security perimeter that prevents data exfiltration from GCP services.

### Why Gemini APIs Must Be in the Perimeter

Without VPC-SC, any authenticated identity with the correct IAM role can call Gemini APIs from **any network**, including personal devices, compromised CI/CD runners, or attacker-controlled infrastructure. The perimeter ensures Gemini traffic originates only from authorized networks and projects.

### Services to Include

| Service | API name | Why include |
|---------|----------|------------|
| Gemini for Google Cloud | `cloudaicompanion.googleapis.com` | Core Gemini chat and assist API. Without this, Gemini queries bypass the perimeter. |
| Gemini Code Assist | `gemini-code-assist.googleapis.com` | Code completion and generation. Handles source code — highest sensitivity. |
| Developer Connect | `developerconnect.googleapis.com` | Repository connections for code customization. If indexed code leaves the perimeter, the perimeter is meaningless. |
| Vertex AI | `aiplatform.googleapis.com` | Required if using Gemini models via Vertex AI endpoints. Vertex handles model invocations and training data. |

### Misconfiguration Risk

Omitting any of these services from the perimeter creates a bypass. For example, if `cloudaicompanion.googleapis.com` is restricted but `aiplatform.googleapis.com` is not, an attacker can call the same Gemini models through Vertex AI and exfiltrate data outside the perimeter.

---

## 5. IAM Roles — Least Privilege

| Role | What it grants | Who should have it | Why |
|------|---------------|-------------------|-----|
| `roles/cloudaicompanion.user` | Use Gemini features (chat, code assist, cloud assist) | Developer groups via Google Group | Permits interaction but not configuration. Developers can query Gemini but cannot change project-level settings, view audit logs, or manage other users. |
| `roles/cloudaicompanion.admin` | Manage Gemini settings, enable/disable features, view usage | Platform admins only (2–3 people) | Admin can toggle logging, data sharing, and code customization. Overly broad assignment means any user could disable safety controls. |
| `roles/aiplatform.user` | Use Vertex AI endpoints (if using Gemini via Vertex) | ML engineering group | Grants access to model endpoints. Should not be combined with `aiplatform.admin` which allows model deployment and deletion. |

### Conditional Access

Use IAM Conditions to restrict Gemini access to business hours, specific IP ranges, or device trust levels:

```
request.time.getHours('America/New_York') >= 8 && request.time.getHours('America/New_York') <= 20
```

This reduces the window for unauthorized use (e.g., compromised credentials used at 3 AM) and provides an additional detection signal.

### Misconfiguration Risk

Granting `cloudaicompanion.admin` to all developers allows any user to enable `data_sharing_enabled` or change the release channel to Preview. Granting `aiplatform.admin` allows model deletion or redeployment with weakened safety settings.

---

## 6. Organization Policies — Defense-in-Depth

Organization policies enforce constraints **above** IAM. Even an org admin with full IAM permissions cannot violate these policies without first modifying the org policy itself.

| Policy constraint | What it does | Recommended configuration | Why |
|-------------------|-------------|--------------------------|-----|
| `constraints/serviceuser.services` | Restricts which APIs can be enabled per project | Deny `cloudaicompanion.googleapis.com` in projects that should not use Gemini | Prevents shadow AI adoption. Teams cannot enable Gemini in sandbox projects without approval. |
| `constraints/gcp.resourceLocations` | Restricts where resources can be created | Allow only `in:us-locations` and/or `in:eu-locations` as required by data residency | Ensures Gemini processing occurs in jurisdictions that comply with GDPR, CCPA, or contractual obligations. |
| `constraints/iam.allowedPolicyMemberDomains` | Restricts which domains can be granted IAM roles | Allow only your Cloud Identity customer ID | Prevents granting Gemini access to external contractors, personal Gmail accounts, or partner organizations without explicit exception. |

### Misconfiguration Risk

Without `serviceuser.services` restrictions, any project owner can enable Gemini in their project, creating unmonitored AI usage. Without `resourceLocations`, Gemini may process data in regions that violate data residency requirements (e.g., EU personal data processed in `asia-southeast1`). Without `allowedPolicyMemberDomains`, an insider can grant `cloudaicompanion.user` to an external Gmail account.

---

## 7. Cloud Audit Logs

| Log type | What it captures | Why enable it |
|----------|-----------------|--------------|
| `ADMIN_READ` | Reads of IAM policies, project settings, Gemini configuration | Detects reconnaissance: an attacker checking who has Gemini access or what settings are configured. |
| `DATA_READ` | Gemini query requests (the prompt metadata, not necessarily full content) | Tracks who is using Gemini, how frequently, and from which IP. Essential for anomaly detection. |
| `DATA_WRITE` | Configuration changes, feature toggles, code customization updates | Captures when someone enables data sharing, changes safety thresholds, or modifies code customization. Critical for change management. |

### Services to Audit

| Service | Rationale |
|---------|-----------|
| `cloudaicompanion.googleapis.com` | All Gemini for Google Cloud interactions |
| `aiplatform.googleapis.com` | All Vertex AI Gemini model invocations |

### Recommended Configuration

Enable **all three log types** for both services. Route logs to a locked-down Cloud Logging bucket with a retention policy that meets your compliance requirements (typically 90–365 days). Export to SIEM for real-time alerting.

### Misconfiguration Risk

Without `DATA_WRITE` logs, an admin who disables safety features leaves no audit trail. Without `DATA_READ` logs, compromised credentials used to exfiltrate data via Gemini queries are invisible. Without `ADMIN_READ`, reconnaissance goes undetected.

---

## 8. Quotas and Budgets

| Control | What it does | Recommended value | Why |
|---------|-------------|-------------------|-----|
| `gemini_api_requests_per_minute` | Rate limit on API calls | 100 RPM per project (adjust by team size) | Prevents runaway automation from exhausting quotas and generating unexpected costs. A misconfigured CI pipeline calling Gemini in a loop can burn through budget in minutes. |
| `gemini_code_assist_requests_per_minute` | Rate limit on Code Assist calls | 60 RPM per project | Code Assist calls are heavier (longer prompts with full file context). Lower limit prevents IDE-triggered storms. |
| GCP Budget alerts | Spending threshold notifications | Set at 50%, 80%, 100% of monthly budget | Early warning allows investigation before cost overruns become critical. |
| Budget actions | Automated response when budget is exceeded | Disable billing at 120% of budget | Hard stop prevents unlimited spend from compromised credentials or automation bugs. |

### Misconfiguration Risk

Without quotas, a single compromised service account or a developer's infinite loop can generate thousands of API calls per minute. Without budget alerts, the organization discovers the overrun only on the monthly invoice. Without budget actions, spend is unbounded.

---

## 9. DLP Integration — Pre-Request Scanning

| Setting | What it does | Recommended configuration | Why |
|---------|-------------|--------------------------|-----|
| Cloud DLP inspection before API call | Scans prompt content for sensitive data types before sending to Gemini | Enable for all production workloads | Even with Google's contractual commitment not to train on API data, sending PII, PHI, or financial data to any external API creates compliance risk (GDPR Article 28, HIPAA BAA requirements). |
| InfoTypes to detect | Categories of sensitive data to scan for | `PHONE_NUMBER`, `EMAIL_ADDRESS`, `CREDIT_CARD_NUMBER`, `US_SOCIAL_SECURITY_NUMBER`, `PERSON_NAME`, custom InfoTypes for internal identifiers | Covers common regulated data categories. Custom InfoTypes catch organization-specific identifiers (employee IDs, internal account numbers). |
| DLP action on detection | What happens when sensitive data is found | Block the request and log the finding | Redacting and sending creates a degraded prompt that may produce meaningless output. Blocking forces the developer to sanitize manually, which is more reliable. |
| De-identification templates | Template for redacting sensitive data | Configure if choosing to redact instead of block | Allows the request to proceed with placeholders, then re-hydrates the response. Complex to implement correctly. |

### Misconfiguration Risk

Without DLP scanning, developers routinely paste customer data, database dumps, and log files containing PII directly into Gemini prompts. This creates regulatory violations and expands the data breach surface to include the Gemini API path.

---

## 10. Private Connectivity

| Connection type | When to use | Why |
|----------------|-------------|-----|
| Private Google Access | All enterprise workloads | Ensures Gemini API traffic stays on Google's backbone network rather than traversing the public internet. No additional cost. **Baseline requirement.** |
| Cloud VPN | Connecting on-premises IDEs to GCP Gemini APIs | Encrypts traffic between corporate network and GCP. Required when developers use on-premises workstations with Gemini Code Assist. |
| Cloud Interconnect | High-volume, latency-sensitive workloads | Dedicated physical connection to Google's network. Use when Gemini is integrated into production pipelines (e.g., real-time content moderation) where VPN latency or bandwidth is insufficient. |
| Private Service Connect | Accessing Gemini APIs via private endpoints | Creates a private endpoint in your VPC for Gemini APIs. Traffic never touches public IP space. Combine with VPC-SC for maximum isolation. |

### When Private Connectivity Is Required

- **Always:** Enable Private Google Access on all subnets using Gemini.
- **On-premises developers:** Cloud VPN or Interconnect.
- **Regulated industries:** Private Service Connect + VPC-SC. No public internet path to Gemini APIs.
- **Multi-cloud:** Cloud VPN to connect AWS/Azure workloads to GCP Gemini endpoints.

### Misconfiguration Risk

Without private connectivity, Gemini API traffic traverses the public internet. While TLS-encrypted, this exposes the traffic to network-level metadata collection, corporate firewall bypass (if users connect from personal networks), and potential TLS interception by compromised CAs.

---

## 11. Generation Config Parameters — Security Implications

| Parameter | What it controls | Recommended value | Security implication |
|-----------|-----------------|-------------------|---------------------|
| `temperature` | Randomness of output (0.0 = deterministic, 2.0 = maximum randomness) | `0.3`–`0.7` for code generation; `0.7`–`1.0` for creative tasks | **High temperature (>1.0) increases the probability of the model generating unsafe content that would normally have low probability.** Safety filters catch most issues, but edge cases become more frequent. High temperature also reduces output reproducibility, making security auditing harder. |
| `max_output_tokens` | Maximum length of generated response | `4096` for most use cases; lower for constrained outputs | Unlimited output tokens allow the model to generate extremely long responses, increasing cost and creating potential for verbose outputs that bury harmful content in otherwise benign text. |
| `top_p` | Nucleus sampling — cumulative probability cutoff | `0.95` | Values approaching `1.0` allow very low-probability tokens, which may include unsafe completions. `0.95` trims the long tail. |
| `top_k` | Number of top tokens considered at each step | `40` | Limits the vocabulary the model samples from. Lower values produce more predictable (auditable) output. Very high values (>100) approach unrestricted sampling. |
| `stop_sequences` | Tokens that trigger response termination | Set project-specific stop sequences | Prevents the model from generating past a natural boundary. Without stop sequences, the model may continue generating beyond the useful answer, potentially producing harmful trailing content. |

### Misconfiguration Risk

Setting `temperature: 2.0` with `top_p: 1.0` and `top_k: 0` (disabled) creates maximum randomness, dramatically increasing the frequency of safety filter edge cases and producing unreproducible outputs that cannot be audited. For code generation, high temperature produces syntactically valid but logically flawed code that may introduce security vulnerabilities.

---

## 12. Application-Layer Checks — Pre and Post Processing

Safety filters and model behavior are not sufficient alone. Application-layer checks provide defense-in-depth.

### Pre-Request Checks

| Check | What it does | Why it's needed | Recommended implementation |
|-------|-------------|----------------|---------------------------|
| PII scan | Detects personally identifiable information in the prompt | Prevents sending regulated data to the API, even if DLP integration is not available at the infrastructure layer | Use Cloud DLP API, Presidio, or regex-based scanner. Block or redact before the API call. |
| Profanity filter | Detects profanity and slurs in user input | Prevents the model from engaging with abusive input, which may produce harmful responses even with safety filters | Use a word list or ML-based classifier. Block the request and return a user-friendly error. |
| Input length limit | Caps the size of user input | Prevents prompt injection attacks that use extremely long inputs to overwhelm the model's context window and push system instructions out of scope | Set to `100000` characters for most use cases. Reject longer inputs with an error. |

### Post-Response Checks

| Check | What it does | Why it's needed | Recommended implementation |
|-------|-------------|----------------|---------------------------|
| Output validation | Validates the structure and content of the response | Catches cases where the model ignores safety filters (rare but possible, especially with adversarial prompts) | Parse the response against expected format. Flag responses that contain unexpected patterns. |
| PII redaction | Detects and redacts PII in the model's response | The model may hallucinate PII (generate realistic but fake social security numbers, phone numbers) or regurgitate PII from the prompt | Run the same PII scanner on the response. Redact before displaying to the user. |
| Content moderation | Secondary content classification on the response | Defense-in-depth — a second classifier catching what safety filters missed | Use a separate content moderation API (e.g., Perspective API, custom classifier). Log disagreements between safety filters and the secondary classifier for investigation. |

### Why Both Pre and Post Checks

Pre-request checks prevent sensitive data from leaving your network. Post-response checks prevent harmful content from reaching the user. Neither alone is sufficient:

- **Pre-only failure mode:** Safe input but harmful output (model generates dangerous content from a benign prompt).
- **Post-only failure mode:** Sensitive data is sent to the API (the damage is done even if the response is clean).
- **Both together:** Sensitive data never leaves, harmful content never arrives.

### Misconfiguration Risk

Without pre-request checks, developers routinely send production database queries, customer support tickets, and log files containing credentials directly to Gemini. Without post-response checks, hallucinated PII reaches end users (creating potential GDPR right-of-rectification issues), and rare safety filter bypasses go undetected.

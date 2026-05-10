# Amazon Q Developer — Settings Rationale

> A comprehensive rationale for every security-relevant Amazon Q Developer setting.
> For each control: what it does, why it matters, recommended values per environment, and what goes wrong when it is misconfigured.

---

## 1. IAM Identity Center vs Builder ID

Amazon Q Developer supports two authentication methods. This choice is the single most consequential security decision for your Q deployment.

### Comparison

| Aspect | Builder ID | IAM Identity Center |
|--------|-----------|-------------------|
| **Authentication** | Personal AWS account (email-based) | Federated through corporate IdP (Okta, Azure AD, Ping) |
| **MFA** | Optional, user-managed | Enforced by organizational policy |
| **License tier** | Free tier only | Free or Pro tier |
| **Encryption** | AWS-owned KMS keys only | AWS-owned or customer-managed KMS keys |
| **Admin control** | None — users self-register | Full lifecycle management (provisioning, deprovisioning, group policies) |
| **Audit** | Limited CloudTrail coverage | Full CloudTrail logging tied to corporate identity |
| **Data handling** | Code snippets may be used for service improvement | Pro tier: code is not used for service improvement |
| **SSO** | Not supported | Full SSO integration |
| **SCIM provisioning** | Not supported | Automatic user provisioning/deprovisioning from IdP |
| **Session management** | User-managed | Admin-controlled session duration and policies |

### Why Identity Center for Enterprise

| Reason | Detail |
|--------|--------|
| **Identity governance** | Builder IDs are personal accounts with no organizational oversight. An employee who leaves retains their Builder ID and any Q conversation history. Identity Center ties access to corporate identity — deprovisioning is immediate. |
| **Encryption control** | Customer-managed KMS keys are only available with Identity Center. Without them, you cannot meet compliance requirements for data encryption at rest (SOC 2, HIPAA, PCI DSS, FedRAMP). |
| **Audit trail** | Builder ID activity produces minimal CloudTrail events. Identity Center activity is fully logged and attributable to specific corporate users, satisfying audit requirements. |
| **MFA enforcement** | Builder IDs rely on the user to enable MFA. Identity Center enforces MFA through organizational policy — no user opt-out. |
| **Training opt-out** | Only Pro tier (Identity Center) guarantees that your code is not used for model improvement. Builder ID (Free tier) does not offer this guarantee. |
| **Compliance** | Regulated industries require that AI tools operate under enterprise identity management. Builder IDs do not satisfy SOX, HIPAA, or GDPR controller requirements because there is no organizational control over the account. |

**Misconfiguration risk:** Allowing developers to use Builder IDs alongside Identity Center creates shadow AI usage. Code processed through Builder IDs falls outside your DPA, encryption controls, and audit trail. Block Builder ID registration on corporate machines through endpoint policy or SCP.

---

## 2. AmazonQFullAccess vs AmazonQDeveloperAccess

AWS provides two managed IAM policies for Q Developer. Choosing between them is a least-privilege decision.

### Policy Comparison

| Capability | AmazonQDeveloperAccess | AmazonQFullAccess |
|-----------|----------------------|-------------------|
| Start/send chat conversations | Yes | Yes |
| Generate code completions | Yes | Yes |
| Run security scans | Yes | Yes |
| List code analysis findings | Yes | Yes |
| Create/delete Q profiles | **No** | Yes |
| Manage user assignments | **No** | Yes |
| Create/manage customizations | **No** | Yes |
| Manage encryption settings | **No** | Yes |
| Create/delete agents | **No** | Yes |
| Modify Q organizational settings | **No** | Yes |

### When to Use Each

| Policy | Assign To | Rationale |
|--------|----------|-----------|
| `AmazonQDeveloperAccess` | All developers, engineers, and regular users | Provides full use of Q features (chat, completions, scanning) without any administrative capability. This is the correct default for 95%+ of users. |
| `AmazonQFullAccess` | Q administrators only (typically 2–3 people per account) | Required for setting up Q, managing profiles, configuring encryption, and managing customizations. Should always require MFA. |

### Defense-in-Depth: Custom Policies

The managed policies are a starting point. For tighter control, create custom policies that:

| Restriction | Implementation | Rationale |
|------------|---------------|-----------|
| Region-lock all Q actions | `aws:RequestedRegion` condition | Prevents Q usage in unapproved regions where data residency is not guaranteed. |
| Require MFA for admin actions | `aws:MultiFactorAuthPresent` condition | Even if an admin's long-term credentials are compromised, the attacker cannot modify Q settings without MFA. |
| Deny customization management | Explicit deny on `codewhisperer:CreateCustomization` | Customizations ingest your codebase for fine-tuning. Restrict this to designated admin roles only. |
| Source IP restriction | `aws:SourceIp` condition | Limit Q admin actions to the corporate network or VPN. |

**Misconfiguration risk:** Assigning `AmazonQFullAccess` to all developers gives every engineer the ability to modify Q organizational settings, create customizations (which ingest codebase data), and change encryption keys. A single compromised developer account could reconfigure Q to use an attacker-controlled KMS key.

---

## 3. Service Control Policies (SCPs)

SCPs are the highest-authority guardrails in AWS Organizations. They override IAM policies and are the only way to enforce restrictions across all accounts in an OU.

### 3.1 Region Restriction

```json
{
  "Effect": "Deny",
  "Action": ["q:*", "codewhisperer:*"],
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": ["us-east-1", "us-west-2"]
    }
  }
}
```

| Aspect | Detail |
|--------|--------|
| **What it does** | Denies all Q Developer actions in any region other than the specified allowlist. |
| **Why it matters** | Amazon Q processes code and conversations on AWS infrastructure in the region where the service is invoked. Region restriction ensures data stays within jurisdictions where your organization has legal standing, DPAs, and compliance coverage. |
| **Recommended regions** | Limit to the fewest regions that meet your latency and availability requirements. Most organizations need only 1–2 regions. |
| **Misconfiguration risk** | Without region restriction, a developer can invoke Q in any region where the service is available. Data processed in an unapproved region may violate GDPR (if the region is outside the EU for EU data), data residency laws, or client contracts specifying data processing locations. |

### 3.2 Feature Restriction

```json
{
  "Effect": "Deny",
  "Action": [
    "codewhisperer:CreateCustomization",
    "codewhisperer:UpdateCustomization",
    "codewhisperer:DeleteCustomization"
  ],
  "Resource": "*"
}
```

| Aspect | Detail |
|--------|--------|
| **What it does** | Prevents customization management (fine-tuning Q on your codebase) in all accounts under the SCP. |
| **Why it matters** | Customizations upload portions of your codebase to AWS for model fine-tuning. This is a powerful feature but requires careful governance — the data ingested, the repositories indexed, and the resulting model must be controlled. An SCP ensures no rogue account can create unauthorized customizations. |
| **Recommended approach** | Deny customizations at the OU level. Create a dedicated "Q Admin" account with an SCP exception for customization management. |
| **Misconfiguration risk** | Without this SCP, any account with the right IAM permissions can create customizations. A developer in a sandbox account could inadvertently index a production repository, uploading proprietary code for fine-tuning without authorization. |

### 3.3 MFA Requirement for Admin Actions

```json
{
  "Effect": "Deny",
  "Action": [
    "q:CreateAssignment",
    "q:DeleteAssignment",
    "q:CreateProfile",
    "q:DeleteProfile",
    "q:UpdateProfile"
  ],
  "Resource": "*",
  "Condition": {
    "BoolIfExists": {
      "aws:MultiFactorAuthPresent": "false"
    }
  }
}
```

| Aspect | Detail |
|--------|--------|
| **What it does** | Denies Q administrative actions unless the caller has authenticated with MFA in the current session. |
| **Why it matters** | Q admin actions control who has access, what encryption is used, and how the service is configured. Requiring MFA ensures that even if long-term credentials are compromised, the attacker cannot modify Q settings. |
| **Misconfiguration risk** | Without MFA enforcement, a stolen access key pair is sufficient to reconfigure Q for the entire organization. |

### SCP Strategy Summary

| SCP | OU Scope | Purpose |
|-----|----------|---------|
| Region restriction | All OUs | Data residency and compliance |
| Customization deny | All OUs except Q Admin account | Prevent unauthorized codebase indexing |
| MFA for admin actions | All OUs | Protect configuration integrity |
| Feature deny (optional) | Specific OUs (e.g., finance, compliance) | Disable Q entirely in accounts that handle sensitive regulated data |

---

## 4. Customer-Managed KMS Keys

### Why Default AWS-Owned Keys Aren't Enough

| Requirement | AWS-Owned Keys | Customer-Managed Keys |
|------------|---------------|----------------------|
| **Key visibility** | You cannot see, audit, or manage the key | Full visibility in KMS console and CloudTrail |
| **Rotation control** | AWS rotates on its own schedule (not disclosed) | You control rotation frequency (annual automatic or on-demand manual) |
| **Access policy** | AWS controls who can use the key | You define the key policy — restrict to specific roles and services |
| **Cross-account protection** | No guarantee the key isn't shared | Key is unique to your account; you control grants |
| **Compliance evidence** | Cannot demonstrate key management to auditors | Full CloudTrail logs for every encrypt/decrypt operation; key policy is auditable |
| **Revocation** | You cannot revoke access to the key | Disable or delete the key to immediately render all Q data unreadable |
| **SOC 2 / HIPAA / PCI** | May not satisfy "customer-managed encryption" controls | Satisfies encryption-at-rest requirements with documented key management |
| **FedRAMP** | Does not satisfy FIPS 140-2 customer-managed key requirements | Customer-managed keys can use FIPS 140-2 validated HSMs |

### What Gets Encrypted

With customer-managed KMS keys, the following Amazon Q data is encrypted:

| Data Type | Description |
|-----------|-------------|
| Chat conversations | All Q chat interactions in the AWS console |
| Console error diagnostics | Data from "Diagnose this error" features |
| Customization data | Indexed code used for fine-tuning |
| Agent data | Data generated by Q agents in the IDE |

### Key Policy Recommendations

| Principle | Implementation |
|-----------|---------------|
| **Least privilege** | Grant `kms:Decrypt`, `kms:Encrypt`, `kms:GenerateDataKey` to the Q service principal only. |
| **Source account condition** | Add `aws:SourceAccount` condition to prevent confused deputy attacks. |
| **Separate admin role** | Key management actions (`kms:Create*`, `kms:Delete*`, `kms:Disable*`) should be restricted to a dedicated admin role, not the same role that uses Q. |
| **No cross-account sharing** | Do not add external account principals to the key policy. |

**Misconfiguration risk:** Using AWS-owned keys means you cannot revoke access to Q's encrypted data. If you need to terminate the Q relationship or respond to a data breach, you have no mechanism to render the data cryptographically inaccessible. With customer-managed keys, disabling the key immediately prevents all decryption.

---

## 5. Key Rotation

### Why Enable Automatic Rotation

| Aspect | Detail |
|--------|--------|
| **What it does** | AWS KMS automatically creates new key material annually. Old key material is retained for decryption of existing data; new encryptions use the new material. |
| **Why it matters** | Key rotation limits the blast radius of a key compromise. If key material is exposed, only data encrypted with that specific version is at risk — not all historical data. |
| **Compliance** | PCI DSS requires cryptographic key rotation at least annually. SOC 2 and HIPAA expect documented key rotation procedures. Automatic rotation satisfies these requirements with zero operational overhead. |
| **Operational impact** | None. AWS handles the rotation transparently. The key ARN does not change. No application changes are required. |

### Configuration

```bash
aws kms enable-key-rotation --key-id KEY_ID
```

### Verification

```bash
aws kms get-key-rotation-status --key-id KEY_ID
```

**Misconfiguration risk:** Without rotation, a single key version encrypts all Q data for the lifetime of the key. If that key material is ever compromised (through an AWS vulnerability, insider threat, or operational error), all historical Q data is exposed. With rotation enabled, exposure is limited to one year of data per key version.

---

## 6. VPC Endpoints

### When Needed

| Scenario | VPC Endpoint Required |
|----------|----------------------|
| Developers using Q in IDE from corporate network with internet access | No (traffic goes over public internet to AWS endpoints) |
| Q used in private subnets (no internet gateway) | **Yes** |
| Organization requires all AWS API traffic to stay on AWS backbone | **Yes** |
| Compliance requires no data traversal over public internet | **Yes** |
| Q used in isolated/air-gapped environments | **Yes** |

### Why VPC Endpoints Matter

| Benefit | Detail |
|---------|--------|
| **No internet exposure** | Traffic between your VPC and Q never leaves the AWS network. Eliminates the risk of traffic interception on the public internet. |
| **Security group control** | You can restrict which CIDR ranges, subnets, or security groups can reach the Q endpoint. This provides network-layer access control beyond IAM. |
| **Private DNS** | The VPC endpoint can override public DNS for Q service endpoints, ensuring that even DNS queries don't reveal Q usage patterns to external observers. |
| **Compliance** | Many compliance frameworks (FedRAMP, HIPAA, PCI DSS) require or strongly recommend that sensitive data processing occur over private network connections. |
| **DLP integration** | Traffic through VPC endpoints can be inspected by network DLP tools, providing an additional layer of data loss prevention. |

### Configuration Considerations

| Setting | Recommendation | Rationale |
|---------|---------------|-----------|
| **Endpoint policy** | Restrict to Q-specific actions only | Default endpoint policies allow all actions on all resources. Scope down to `q:*` and `codewhisperer:*` actions. |
| **Security groups** | Allow HTTPS (443) from developer subnets only | Prevent non-developer workloads from reaching Q. |
| **Private DNS** | Enable | Ensures all Q API calls from the VPC automatically route through the endpoint without application changes. |
| **Subnet placement** | Deploy in each AZ where developers operate | Endpoint availability must match developer subnet availability. |

**Misconfiguration risk:** Creating a VPC endpoint but not enabling private DNS means that Q API calls still resolve to public endpoints. Traffic goes over the internet despite having an endpoint in place. Always verify with a DNS lookup from within the VPC that the Q endpoint resolves to a private IP.

---

## 7. Security Scanning Features

Amazon Q Developer includes two security scanning capabilities that operate at different scopes.

### 7.1 Project Scan (On-Demand)

| Aspect | Detail |
|--------|--------|
| **What it does** | Scans an entire project or workspace for security vulnerabilities. Triggered manually or via CI/CD integration. |
| **Why to enable** | Catches vulnerabilities across the full codebase, not just the file you're editing. Identifies cross-file issues like insecure data flows, missing authorization checks, and hardcoded credentials. |
| **Coverage** | Supports Python, Java, JavaScript, TypeScript, C#, Go, Ruby, Kotlin, PHP, C, C++, Terraform, CloudFormation, and CDK. |
| **Recommended usage** | Run on every PR and on a scheduled basis (daily or weekly) for all repositories. |

### 7.2 Auto-Scan (Real-Time)

| Aspect | Detail |
|--------|--------|
| **What it does** | Continuously scans files as you edit them in the IDE. Provides inline security findings in real time. |
| **Why to enable** | Catches vulnerabilities at the earliest possible point — while the developer is writing the code. Fixing a vulnerability during development is orders of magnitude cheaper than finding it in production. |
| **Performance impact** | Minimal. Scans run asynchronously and only on changed files. |
| **Recommended usage** | Enable for all developers by default. |

### Why to Enable Both

| Scenario | Project Scan Only | Auto-Scan Only | Both Enabled |
|----------|:-----------------:|:--------------:|:------------:|
| Developer introduces SQL injection in new file | Caught at PR time | **Caught immediately** | **Caught immediately** |
| Existing vulnerability in untouched file | **Caught on schedule** | Not caught (file not edited) | **Caught on schedule** |
| Cross-file data flow vulnerability | **Caught at PR time** | May not be caught (single-file scope) | **Caught at PR time** |
| Hardcoded credential in config file | **Caught on schedule** | **Caught if file is opened** | **Caught by both** |

**Misconfiguration risk:** Disabling both scanning features means Q Developer provides no security value beyond code completions. You lose the built-in SAST capability that comes with the Pro license at no additional cost.

---

## 8. Code Review Capabilities

### Security Detector Coverage

Amazon Q code review includes security-focused detectors that go beyond generic linting:

| Detector Category | Examples | Impact if Disabled |
|-------------------|---------|-------------------|
| **Injection flaws** | SQL injection, command injection, LDAP injection, XPath injection | Undetected injection vulnerabilities are the #1 web application risk (OWASP Top 10). |
| **Authentication issues** | Hardcoded credentials, weak password handling, missing MFA checks | Compromised authentication leads directly to unauthorized access. |
| **Cryptographic weaknesses** | Weak algorithms (MD5, SHA1 for security), insufficient key lengths, insecure random number generation | Weak crypto can be broken by attackers, exposing encrypted data. |
| **Data exposure** | Sensitive data in logs, unencrypted data in transit, PII handling violations | Data exposure triggers breach notification requirements (GDPR 72-hour rule). |
| **Access control** | Overly permissive IAM policies, missing authorization checks, IDOR vulnerabilities | Broken access control is the most common security finding in real-world applications. |
| **Infrastructure** | Insecure Terraform/CloudFormation patterns, open security groups, unencrypted storage | Infrastructure misconfigurations are the leading cause of cloud breaches. |

### Recommended Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| Code review on PR | Enabled | Catches issues before they reach the main branch. |
| Security detectors | All enabled | No reason to disable individual detector categories. False positives are preferable to missed vulnerabilities. |
| Auto-fix suggestions | Enabled | Q can suggest fixes for detected issues, accelerating remediation. |

---

## 9. Workspace Context and Indexing

### What Workspace Indexing Does

When enabled, Amazon Q indexes your project files to provide more relevant completions and chat responses. This means Q reads and processes your source code to build a contextual understanding of your codebase.

### Data Handling Implications

| Aspect | Detail |
|--------|--------|
| **What is sent** | File contents from your workspace are sent to AWS for processing when you interact with Q (completions, chat, scanning). |
| **Where it's processed** | In the AWS region where your Q profile is configured. |
| **Retention** | For Pro tier (Identity Center): conversation data is retained for the session and not used for model training. For Free tier (Builder ID): content may be used for service improvement. |
| **Encryption in transit** | TLS 1.2+ for all data transmission. |
| **Encryption at rest** | AWS-owned keys (default) or customer-managed KMS keys (Pro tier). |

### What to Consider

| Consideration | Recommendation |
|--------------|---------------|
| **Sensitive repositories** | Evaluate whether repositories containing trade secrets, proprietary algorithms, or regulated data should have Q indexing enabled. Consider excluding specific directories via `.amazonq/ignore` patterns. |
| **Third-party code** | Code from clients or partners may be subject to NDAs or DPAs that restrict processing by AI tools. Verify contractual obligations before enabling Q on these repositories. |
| **Customizations** | If you create Q customizations, the indexed code is used for fine-tuning. This is a deeper level of data processing — ensure all indexed repositories are approved for this purpose. |
| **Data classification** | Align Q workspace access with your data classification policy. Public and internal-use code: generally safe. Confidential and restricted: requires explicit approval and customer-managed encryption. |

**Misconfiguration risk:** Enabling workspace indexing on a repository containing client data subject to a DPA that prohibits third-party AI processing creates a contractual breach. Always review data classification and contractual obligations before enabling Q on a repository.

---

## 10. IAM Conditions — Defense-in-Depth

IAM conditions add contextual restrictions to Q permissions. They work alongside SCPs to create multiple layers of protection.

### 10.1 MFA Requirement

```json
{
  "Condition": {
    "Bool": {
      "aws:MultiFactorAuthPresent": "true"
    }
  }
}
```

| Aspect | Detail |
|--------|--------|
| **What it does** | Requires multi-factor authentication for the API call to succeed. |
| **Why it matters** | Stolen long-term credentials (access keys leaked in a repo, phished passwords) cannot be used without the second factor. This is the most effective single control against credential theft. |
| **Apply to** | All `AmazonQFullAccess` policies. Optional but recommended for `AmazonQDeveloperAccess` as well. |
| **Misconfiguration risk** | Applying MFA conditions without ensuring your IdP supports MFA for programmatic access may lock out legitimate users. Test with a pilot group first. |

### 10.2 Region Restriction

```json
{
  "Condition": {
    "StringEquals": {
      "aws:RequestedRegion": ["us-east-1", "us-west-2"]
    }
  }
}
```

| Aspect | Detail |
|--------|--------|
| **What it does** | Limits Q API calls to specific AWS regions. |
| **Why it matters** | Data residency compliance. Even if Q is available in 10 regions, your organization may only have legal/compliance coverage for 2. Region conditions prevent accidental or intentional invocation in unapproved regions. |
| **Apply to** | All Q-related IAM policies. Also enforce at the SCP level for belt-and-suspenders protection. |
| **Misconfiguration risk** | Restricting to a single region with no fallback means a regional AWS outage takes down Q for the entire organization. Consider allowing a secondary region if availability is critical. |

### 10.3 Source IP Restriction

```json
{
  "Condition": {
    "IpAddress": {
      "aws:SourceIp": [
        "203.0.113.0/24",
        "198.51.100.0/24"
      ]
    }
  }
}
```

| Aspect | Detail |
|--------|--------|
| **What it does** | Restricts Q API calls to specified source IP ranges (typically corporate office and VPN egress IPs). |
| **Why it matters** | Even with valid credentials and MFA, an attacker operating from outside your network cannot use Q. This prevents credential abuse from non-corporate networks. |
| **Apply to** | Admin actions (`AmazonQFullAccess`) at minimum. Developer actions if your workforce operates exclusively from known IP ranges. |
| **Misconfiguration risk** | Overly strict IP restrictions break Q for remote developers not on VPN. If your workforce is distributed, use VPC endpoints instead of source IP restrictions for developer access. Reserve IP restrictions for admin actions only. |

### Layered Defense Matrix

| Layer | Control | Blocks |
|-------|---------|--------|
| **SCP** | Region restriction | Q usage in unapproved regions |
| **SCP** | MFA for admin | Credential theft for admin actions |
| **IAM Policy** | `AmazonQDeveloperAccess` | Privilege escalation to admin |
| **IAM Condition** | MFA required | Phished passwords without second factor |
| **IAM Condition** | Region restriction | Redundant region enforcement (defense-in-depth) |
| **IAM Condition** | Source IP | Access from non-corporate networks |
| **VPC Endpoint** | Private connectivity | Data traversal over public internet |
| **KMS** | Customer-managed key | Data exposure without key access |

---

## 11. CloudTrail Logging

### What Events to Track

CloudTrail captures API calls made to Amazon Q Developer. These events are essential for security monitoring, incident response, and compliance.

| Event Name | What It Indicates | Severity | Recommended Action |
|------------|-------------------|----------|-------------------|
| `CreateProfile` | A new Q profile was created | Medium | Verify authorized admin performed the action |
| `DeleteProfile` | A Q profile was deleted | High | Investigate — may indicate destructive action or account cleanup |
| `UpdateProfile` | Q profile settings were changed (encryption, features) | High | Verify change was approved. Check if encryption was downgraded. |
| `CreateAssignment` | A user was assigned Q access | Low | Normal provisioning. Flag if outside onboarding workflow. |
| `DeleteAssignment` | A user's Q access was revoked | Low | Normal deprovisioning. Correlate with offboarding ticket. |
| `CreateCustomization` | A codebase customization was initiated | High | Verify which repositories are being indexed. Ensure approval exists. |
| `DeleteCustomization` | A customization was removed | Medium | May indicate cleanup or unauthorized removal of security controls. |
| `StartConversation` | A Q chat session began | Low | Normal usage. High volume from a single user may indicate automation/abuse. |
| `SendMessage` | A message was sent to Q | Low | Normal usage. Monitor for unusual patterns. |
| `GenerateCompletions` | Q provided code completions | Low | Normal usage. Aggregate counts are useful for utilization reporting. |
| `ListCodeAnalysisFindings` | Security scan results were retrieved | Low | Normal usage. Absence of this event may indicate scanning is disabled. |

### CloudTrail Configuration

```bash
aws cloudtrail create-trail \
  --name amazon-q-audit \
  --s3-bucket-name my-cloudtrail-bucket \
  --is-multi-region-trail \
  --enable-log-file-validation
```

| Setting | Value | Rationale |
|---------|-------|-----------|
| `is-multi-region-trail` | `true` | Captures Q events regardless of which region the API call is made in. Essential when combined with SCP region restrictions to detect denied calls. |
| `enable-log-file-validation` | `true` | Ensures log files have not been tampered with. Required for forensic integrity and compliance evidence. |
| Log file encryption | Customer-managed KMS key | Protects audit trail with the same level of encryption as Q data itself. |

**Misconfiguration risk:** Without CloudTrail logging, you have no record of who used Q, what code was processed, or whether admin settings were changed. In the event of a data breach involving Q, you cannot determine scope or timeline without CloudTrail events.

---

## 12. CloudWatch Alarms

### What Thresholds Matter

CloudWatch alarms provide real-time alerting when Q usage patterns indicate security issues or operational problems.

| Alarm | Metric/Pattern | Threshold | Rationale |
|-------|---------------|-----------|-----------|
| **Admin action spike** | Count of `UpdateProfile`, `CreateAssignment`, `DeleteAssignment` events | > 10 per hour | Normal admin workflows produce a handful of events. A spike indicates automated or unauthorized changes. |
| **Customization creation** | `CreateCustomization` event | Any occurrence | Customizations index your codebase. Every creation should be an approved, deliberate act. Alert on any occurrence and verify. |
| **Encryption downgrade** | `UpdateProfile` where encryption config changes | Any occurrence | Someone may be switching from customer-managed to AWS-owned keys. This weakens your encryption posture. |
| **Denied API calls** | CloudTrail events with `errorCode: AccessDenied` for Q actions | > 5 per hour per user | A user repeatedly hitting permission boundaries may be attempting privilege escalation or probing for misconfigurations. |
| **Q usage from unapproved region** | CloudTrail events for Q actions in non-approved regions | Any occurrence | Indicates SCP bypass attempt or misconfigured IAM policy. |
| **Off-hours admin activity** | Q admin events outside business hours | Any occurrence | Admin changes at 3 AM warrant investigation unless tied to a change ticket. |
| **High-volume completions** | `GenerateCompletions` count per user | > 1,000 per hour | May indicate automated tooling using Q API, not a human developer. |

### Example CloudWatch Alarm

```json
{
  "AlarmName": "AmazonQ-UnauthorizedAdminAction",
  "MetricName": "Q-AdminActionCount",
  "Namespace": "Custom/AmazonQSecurity",
  "Statistic": "Sum",
  "Period": 3600,
  "EvaluationPeriods": 1,
  "Threshold": 10,
  "ComparisonOperator": "GreaterThanThreshold",
  "AlarmActions": ["arn:aws:sns:us-east-1:ACCOUNT_ID:security-alerts"],
  "TreatMissingData": "notBreaching"
}
```

**Misconfiguration risk:** Setting thresholds too high means real attacks go unnoticed. Setting them too low causes alert fatigue and alarms are ignored. Start with the thresholds above and tune based on your organization's baseline Q usage patterns over 2–4 weeks.

---

## 13. AWS Config Rules

### Compliance Monitoring

AWS Config rules continuously evaluate Q-related resource configurations against your security baseline.

| Rule | What It Checks | Why It Matters |
|------|---------------|----------------|
| **Q profile encryption** | Verifies that all Q profiles use customer-managed KMS keys | Detects encryption downgrades or new profiles created with AWS-owned keys |
| **KMS key rotation** | Verifies that KMS keys used by Q have automatic rotation enabled | Ensures compliance with key rotation requirements (PCI DSS, SOC 2) |
| **KMS key policy** | Verifies that Q's KMS key policy follows least privilege | Detects overly permissive key policies that could allow unauthorized decryption |
| **IAM policy compliance** | Verifies that no users have `AmazonQFullAccess` without MFA conditions | Catches privilege creep — admin access assigned without proper conditions |
| **SCP presence** | Verifies that Q-related SCPs are attached to all OUs | Detects SCP detachment, which would remove region or feature restrictions |
| **VPC endpoint configuration** | Verifies VPC endpoints exist for Q in required VPCs | Ensures private connectivity hasn't been accidentally removed |

### Custom Config Rule Example

```python
def evaluate_compliance(configuration_item, rule_parameters):
    """Check that Q profiles use customer-managed KMS keys."""
    if configuration_item["resourceType"] != "AWS::QDeveloper::Profile":
        return "NOT_APPLICABLE"

    encryption_config = configuration_item.get("configuration", {}).get(
        "encryptionConfig", {}
    )
    kms_key_arn = encryption_config.get("kmsKeyArn")

    if kms_key_arn and kms_key_arn.startswith("arn:aws:kms:"):
        return "COMPLIANT"
    return "NON_COMPLIANT"
```

### Remediation

| Non-Compliant Finding | Auto-Remediation | Manual Action |
|----------------------|-----------------|---------------|
| Q profile without customer-managed KMS | Not recommended (may disrupt service) | Update profile encryption configuration |
| KMS key without rotation | Enable via `aws kms enable-key-rotation` | Can be auto-remediated safely |
| Missing SCP | Re-attach via Organizations API | Investigate why it was detached |
| IAM user with full access, no MFA | Add MFA condition to policy | Review who assigned the policy |

**Misconfiguration risk:** AWS Config rules without remediation actions are informational only. Non-compliant resources stay non-compliant until someone manually fixes them. Set up auto-remediation for safe actions (key rotation) and SNS notifications for actions requiring judgment (encryption changes).

---

## 14. Data Residency

### Regional Processing Implications

| Aspect | Detail |
|--------|--------|
| **Where Q processes data** | In the AWS region where the Q profile is created and where API calls are made. |
| **What crosses regions** | If you invoke Q from `us-east-1` but your profile is in `us-west-2`, the request is processed in the region of invocation unless explicitly routed. |
| **EU considerations** | For GDPR compliance, European organizations should restrict Q to EU regions (`eu-west-1`, `eu-central-1`) via SCPs. Data processed in US regions may trigger GDPR Chapter V (international transfers) obligations. |
| **Data sovereignty** | Some countries (Germany, France, Australia) have data sovereignty requirements that mandate processing within national borders or approved jurisdictions. Verify Q availability in required regions. |
| **Cross-border teams** | If your developers span multiple continents, you may need multiple Q profiles in different regions. Balance latency against data residency requirements. |

### Configuration Strategy

| Organization Type | Region Strategy |
|-------------------|----------------|
| US-only company | Restrict to `us-east-1` and `us-west-2` |
| EU company (GDPR) | Restrict to EU regions only |
| Global enterprise | Region-specific Q profiles; SCPs enforced per OU by geography |
| Government / defense | Restrict to GovCloud regions if available |

**Misconfiguration risk:** A global company using a single US-based Q profile for all developers sends EU employee code to US infrastructure. If any of that code contains personal data (variable names referencing EU citizens, EU-specific business logic), this constitutes a cross-border data transfer under GDPR, requiring Standard Contractual Clauses or an adequacy decision.

---

## 15. Training Data Opt-Out

### How Data Handling Works by Tier

| Tier | Code used for training? | Chat used for training? | How to verify |
|------|:----------------------:|:----------------------:|---------------|
| **Free (Builder ID)** | May be used for service improvement | May be used for service improvement | Opt-out available in Q settings; verify via AWS documentation |
| **Pro (Identity Center)** | **No** — not used for model training | **No** — not used for model training | Covered by AWS Enterprise terms; verify in your DPA |

### Why This Matters

| Concern | Detail |
|---------|--------|
| **IP protection** | Code used for training could influence model outputs for other customers. While individual code snippets aren't reproduced verbatim, patterns and approaches could leak. |
| **Competitive risk** | If your proprietary algorithms influence model training, competitors using Q could receive suggestions that reflect your approaches. |
| **Contractual obligations** | Many enterprise contracts and client agreements prohibit using code for third-party model training. Using the Free tier may violate these obligations. |
| **Regulatory** | Healthcare (HIPAA), financial (GLBA), and government (ITAR, EAR) regulations may prohibit code from being used as training data for external AI models. |

### API-Level Data Handling

| API Interaction | Free Tier | Pro Tier |
|----------------|-----------|----------|
| Code completions | Content may be retained | Content not retained beyond session |
| Chat conversations | Content may be retained | Content not retained beyond session |
| Security scans | Findings retained for service improvement | Findings not retained |
| Customizations | N/A (Pro only) | Indexed code retained for customization only; deleted when customization is deleted |

### Verification Steps

1. **Confirm Pro tier enrollment** — Check IAM Identity Center for Q Developer Pro assignment.
2. **Review AWS DPA** — Ensure your Data Processing Addendum covers Q Developer specifically.
3. **Check account settings** — In the Q Developer console, verify the content sharing / service improvement setting is configured correctly.
4. **Audit CloudTrail** — Verify Q API calls are made with Identity Center credentials, not Builder IDs.

**Misconfiguration risk:** A developer using a Builder ID (Free tier) alongside the organization's Identity Center (Pro tier) setup sends code through the Free tier path, where it may be used for training. The organization believes all code is covered by Pro tier terms, but the Builder ID usage falls outside that coverage. Enforce Identity Center-only access through SCPs and endpoint policies.

---

## 16. Summary — Quick Reference

| Setting | Secure Default | Key Risk if Wrong |
|---------|---------------|-------------------|
| Authentication | IAM Identity Center (Pro tier) | Builder IDs: no admin control, no encryption choice, code may train models |
| IAM policy | `AmazonQDeveloperAccess` for users | `AmazonQFullAccess` everywhere: any compromised user can reconfigure Q |
| SCP — regions | Deny all except approved regions | Data processed in unapproved jurisdictions violating compliance |
| SCP — customizations | Deny except in admin account | Unauthorized codebase indexing for fine-tuning |
| KMS encryption | Customer-managed keys | AWS-owned keys: no visibility, no revocation, compliance gaps |
| Key rotation | Automatic, annual | Without rotation: total exposure if key material is compromised |
| VPC endpoints | Required for private subnets | Traffic over public internet despite private subnet design |
| Project scan | Enabled | Miss codebase-wide vulnerabilities |
| Auto-scan | Enabled | Vulnerabilities found late in the cycle instead of at write-time |
| Code review | All detectors enabled | Miss injection, auth, crypto, and access control flaws |
| MFA condition | Required for admin, recommended for all | Stolen credentials sufficient for full Q access |
| Region condition | Enforce in IAM and SCP | Accidental data processing in unapproved regions |
| Source IP condition | Admin actions at minimum | Admin actions from compromised external networks |
| CloudTrail | Multi-region, log validation | No audit trail for Q usage or configuration changes |
| CloudWatch alarms | Admin actions, encryption changes, denied calls | Attacks and misconfigurations go unnoticed |
| Config rules | Encryption, rotation, SCP presence | Configuration drift from security baseline |
| Data residency | Region-matched to compliance requirements | Cross-border data transfers violating GDPR or data sovereignty laws |
| Training opt-out | Pro tier (automatic) | Free tier code may be used for model training |

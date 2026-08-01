# Amazon Q Developer - Admin Security Policy

## 1. Identity & Access

- [ ] **IAM Identity Center** : Use Identity Center (not Builder IDs) for all Q Developer access.
- [ ] **Least privilege** : Prefer this repo's tiered `iam-policy-*.json` over broad `AmazonQFullAccess`.
- [ ] **MFA enforcement** : Require MFA for all Identity Center users; Strict also conditions Q chat on MFA.
- [ ] **SSO integration** : Connect Identity Center to your corporate IdP (Okta, Azure AD, etc.).
- [ ] **Session duration** : Set maximum session duration to 8 hours or less.

## 2. High-Autonomy Controls (PassRequest, Agents, Plugins)

- [ ] **`q:PassRequest`** : Deny on Moderate/Strict. This permission lets Amazon Q call AWS APIs with the caller's power.
- [ ] **Agent sessions** : Deny `qdeveloper:StartAgentSession` on Moderate/Strict unless an exception role is approved.
- [ ] **Code transform** : Deny `qdeveloper:TransformCode` outside controlled upgrade pipelines.
- [ ] **Plugins** : Deny `q:UsePlugin` on Moderate/Strict; deny `CreatePlugin` / OAuth app APIs for all developers.
- [ ] **CLI code generation** : Deny `q:GenerateCodeFromCommands` on Moderate/Strict if CLI-to-code autonomy is out of policy.
- [ ] **Exception path** : Document principal tag `q-autonomy-exception=approved` (see SCP) for time-boxed exceptions.

## 3. Encryption

- [ ] **Customer-managed KMS** : Enable customer-managed KMS keys for all Q data.
- [ ] **Key rotation** : Enable automatic key rotation on all KMS keys.
- [ ] **Key policy** : Restrict key usage to Q service principals and admin roles only.
- [ ] **Cross-account protection** : Ensure KMS keys are not shared across accounts.

## 4. Network Security

- [ ] **VPC endpoints** : Create VPC endpoints for Q if operating in private subnets.
- [ ] **Security groups** : Restrict VPC endpoint security groups to necessary CIDR ranges.
- [ ] **TLS enforcement** : All Q traffic uses TLS by default; never override.

## 5. Organizational Controls

- [ ] **SCPs** : Deploy `examples/iam-scp-restrict.json` (after replacing placeholders) to restrict Q by OU/account.
- [ ] **Region restriction** : Limit Q usage to approved AWS regions via SCPs.
- [ ] **Feature restriction** : Disable PassRequest, agents, transforms, and plugin admin not approved for your organization.
- [ ] **Customization control** : Restrict who can create and manage Q customizations.

## 6. Monitoring & Audit

- [ ] **CloudTrail** : Enable CloudTrail logging for all `q`, `qdeveloper`, and `codewhisperer` API calls.
- [ ] **Alerting** : Alert on Allow of `q:PassRequest`, any plugin/OAuth admin API, and customization mutations.
- [ ] **CloudWatch** : Set up alarms for unusual Q usage patterns.
- [ ] **AWS Config / Security Hub** : Monitor Q configuration compliance.

## 7. Data Governance

- [ ] **Code references** : Enable code reference tracking to identify AI-generated code.
- [ ] **Content controls** : Review and configure content filtering settings.
- [ ] **Data residency** : Ensure Q data stays within approved regions.
- [ ] **Training opt-out** : Verify Q Pro does not use your code for model training.

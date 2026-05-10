# Amazon Q Developer — Admin Security Policy

## 1. Identity & Access

- [ ] **IAM Identity Center** — Use Identity Center (not Builder IDs) for all Q Developer access.
- [ ] **Least privilege** — Default users to `AmazonQDeveloperAccess`; reserve `AmazonQFullAccess` for admins.
- [ ] **MFA enforcement** — Require MFA for all Identity Center users.
- [ ] **SSO integration** — Connect Identity Center to your corporate IdP (Okta, Azure AD, etc.).
- [ ] **Session duration** — Set maximum session duration to 8 hours or less.

## 2. Encryption

- [ ] **Customer-managed KMS** — Enable customer-managed KMS keys for all Q data.
- [ ] **Key rotation** — Enable automatic key rotation on all KMS keys.
- [ ] **Key policy** — Restrict key usage to Q service principals and admin roles only.
- [ ] **Cross-account protection** — Ensure KMS keys are not shared across accounts.

## 3. Network Security

- [ ] **VPC endpoints** — Create VPC endpoints for Q if operating in private subnets.
- [ ] **Security groups** — Restrict VPC endpoint security groups to necessary CIDR ranges.
- [ ] **TLS enforcement** — All Q traffic uses TLS by default; never override.

## 4. Organizational Controls

- [ ] **SCPs** — Deploy Service Control Policies to restrict Q by OU/account.
- [ ] **Region restriction** — Limit Q usage to approved AWS regions via SCPs.
- [ ] **Feature restriction** — Disable Q features not approved for your organization.
- [ ] **Customization control** — Restrict who can create and manage Q customizations.

## 5. Monitoring & Audit

- [ ] **CloudTrail** — Enable CloudTrail logging for all Q API calls.
- [ ] **CloudWatch** — Set up alarms for unusual Q usage patterns.
- [ ] **AWS Config** — Create Config rules to monitor Q configuration compliance.
- [ ] **Security Hub** — Integrate Q findings into AWS Security Hub.

## 6. Data Governance

- [ ] **Code references** — Enable code reference tracking to identify AI-generated code.
- [ ] **Content controls** — Review and configure content filtering settings.
- [ ] **Data residency** — Ensure Q data stays within approved regions.
- [ ] **Training opt-out** — Verify Q Pro does not use your code for model training.

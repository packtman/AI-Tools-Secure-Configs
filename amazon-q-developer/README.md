# Amazon Q Developer — Secure Admin Configuration

This directory contains security-hardened configurations for **Amazon Q Developer**, targeting AWS administrators who need to enforce IAM policies, encryption settings, and access controls.

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-admin-policy.md` | Admin security checklist |
| `examples/iam-policy-strict.json` | **Strict** — Read-only Q access, MFA required (regulated environments) |
| `examples/iam-policy-moderate.json` | **Moderate** — Standard developer access, region-locked (enterprise teams) |
| `examples/iam-policy-baseline.json` | **Baseline** — Broad developer access, essential guardrails (startups) |
| `examples/iam-policy-full-access.json` | Full admin IAM policy |
| `examples/iam-policy-developer.json` | Restricted developer IAM policy (reference, aligns with moderate tier) |
| `examples/iam-scp-restrict.json` | Service Control Policy to restrict Q features |
| `examples/encryption-config.md` | Customer-managed KMS encryption guide |
| `examples/settings-rationale.md` | Comprehensive rationale for every security setting |

## Key Security Concepts

### IAM Integration

Amazon Q Developer uses IAM for access control with two primary managed policies:

| Policy | Use case |
|--------|----------|
| `AmazonQFullAccess` | Full admin — manage Q settings, customizations, agents |
| `AmazonQDeveloperAccess` | Developer — use Q features without admin privileges |

### Access Tiers

| Feature tier | Authentication | Encryption |
|-------------|----------------|------------|
| Free tier (Builder ID) | AWS Builder ID | AWS-owned KMS keys |
| Pro tier (Identity Center) | IAM Identity Center | AWS-owned or customer-managed KMS |

**For enterprise use:** Always use IAM Identity Center (Pro tier) with customer-managed KMS keys.

### Service Control Policies (SCPs)

SCPs allow organization-wide restriction of Amazon Q features:
- Deny specific Q actions across all accounts in an OU
- Restrict which regions Q can be used in
- Limit access to specific Q capabilities (chat, agents, customizations)

### Customer-Managed Encryption

For IAM Identity Center users with Q Developer Pro:
- Chat in AWS console
- Diagnosing console errors
- Customizations
- Agents in the IDE

All can be encrypted with customer-managed KMS keys instead of the default AWS-owned keys.

## Deployment Checklist

1. Use IAM Identity Center (not Builder IDs) for all enterprise users.
2. Apply least-privilege IAM policies — default to `AmazonQDeveloperAccess`.
3. Deploy SCPs to restrict Q features by OU/account.
4. Enable customer-managed KMS encryption for all Q data.
5. Configure VPC endpoints if Q is used in private network environments.
6. Review AWS CloudTrail logs for Q-related API calls.
7. Set up AWS Config rules to monitor Q configuration compliance.

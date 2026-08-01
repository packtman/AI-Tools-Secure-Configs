# Amazon Q Developer - Secure Admin Configuration

This directory contains security-hardened configurations for **Amazon Q Developer**, targeting AWS administrators who need to enforce IAM policies, encryption settings, and access controls.

Amazon Q Developer is AWS's AI coding and cloud assistant (chat in the AWS console and IDE extensions for code suggestions, agents, and transformations).

## What Is Covered

| File | Purpose |
|------|---------|
| `secure-admin-policy.md` | Admin security checklist |
| `examples/iam-policy-strict.json` | **Strict** : Chat/suggestions only, MFA, denies PassRequest/agents/plugins |
| `examples/iam-policy-moderate.json` | **Moderate** : Chat/completions, denies PassRequest/agents/plugin admin |
| `examples/iam-policy-baseline.json` | **Baseline** : PassRequest and agents allowed in approved regions |
| `examples/iam-policy-full-access.json` | Full admin IAM policy |
| `examples/iam-policy-developer.json` | Restricted developer IAM policy (Moderate-aligned) |
| `examples/iam-scp-restrict.json` | Service Control Policy (SCP) for org-wide Q guardrails |
| `examples/encryption-config.md` | Customer-managed KMS encryption guide |
| `examples/settings-rationale.md` | Rationale for every security setting |

## 1. Rollout Plan

### Phased rollout

| Phase | Who | Exit criteria |
|-------|-----|---------------|
| Pilot | 5-10 Identity Center users in one account | Zero privilege-escalation via `q:PassRequest`; CloudTrail shows expected Allow/Deny; at least one rollback drill |
| Expanded pilot | One OU / 25-50 developers | Exception tag path for autonomy tested; support friction under 20% above baseline |
| Org-wide | All developer accounts via IAM Identity Center + SCP | SIEM alerts on denied PassRequest/agent/plugin admin; quarterly IAM review scheduled |

### Pre-rollout checklist

- [ ] IAM Identity Center (not Builder IDs) verified for the pilot account
- [ ] Secrets manager / KMS CMK path documented for Q Pro encryption
- [ ] CloudTrail trail includes `q`, `qdeveloper`, and `codewhisperer` events and SIEM ingest tested
- [ ] Rollback: detach custom policies and re-attach `AmazonQDeveloperAccess` documented

### What will break (Moderate)

| Blocked | Developer message |
|---------|-------------------|
| `q:PassRequest` (Q calling AWS APIs on the user's behalf) | "Amazon Q cannot change AWS resources for you. Use the AWS console or IaC with your own role, then ask Q for guidance only." |
| Agent sessions / code transform (`qdeveloper:StartAgentSession`, `qdeveloper:TransformCode`) | "Autonomous Q agents and transforms are disabled. Use chat + completions, or file an exception tagged `q-autonomy-exception=approved`." |
| Third-party plugins / OAuth app registration | "Only platform admins may register Q plugins. Request an approved plugin through the security exception process." |

### Rollback procedure

1. Detach `iam-policy-moderate.json` (or Strict/Baseline) from the pilot group/role.
2. Re-attach AWS managed `AmazonQDeveloperAccess` if temporary productivity restore is required.
3. For SCP rollback: detach `iam-scp-restrict.json` from the OU (keep region deny if data residency still required).
4. Notify pilots: "Amazon Q temporary policy rollback applied. Resume normal work; security will re-stage after review."

## 2. Config Files

Use the exact filenames above. Prefer customer-managed policies attached through IAM Identity Center permission sets. No API keys or account IDs belong in these files (replace `o-YOUR_ORG_ID` and region lists before deploy).

## 3. Tier Delta Table

| Setting / action | Baseline | Moderate | Strict | Reason for the difference |
|------------------|----------|----------|--------|---------------------------|
| `q:PassRequest` | Allow (approved regions) | Deny | Deny | PassRequest lets Q invoke any AWS API the identity can call. Moderate/Strict remove that privilege-escalation path. |
| `qdeveloper:StartAgentSession` | Allow | Deny | Deny | Agent sessions increase autonomous code/cloud changes. Allowed only where startup velocity outweighs risk. |
| `qdeveloper:TransformCode` | Allow | Deny | Deny | Bulk transforms can rewrite large trees. Keep off until change control exists. |
| `q:UsePlugin` | Allow | Deny | Deny | Plugins bridge third-party systems into chat. Moderate/Strict require admin-mediated integration. |
| Plugin/OAuth admin (`CreatePlugin`, `CreateOAuthAppConnection`, ...) | Deny | Deny | Deny | Only break-glass admin roles should register plugins. |
| Customizations (`codewhisperer:CreateCustomization`, ...) | Deny | Deny | Deny | Customizations ingest org codebases. Admin-only outside these developer policies. |
| Completions (`codewhisperer:GenerateCompletions`) | Allow | Allow | Deny (recommendations only) | Strict minimizes IDE code-generation surface while keeping chat usable. |
| MFA condition | No | No | Required | Regulated endpoints need step-up auth for every Q chat action. |
| Regions | 3 example regions | 2 example regions | 1 example region | Tighter residency as tier rises. |

## 4. Deployment Steps

Amazon Q Developer does **not** ship MDM managed-settings payloads like Claude Code or Cursor. Next-best controls: IAM Identity Center permission sets, Organizations SCPs, and endpoint controls that block Builder ID sign-in.

| OS / surface | Deploy path |
|--------------|-------------|
| AWS IAM / Identity Center | Attach the chosen `iam-policy-*.json` as a customer-managed policy on the developer permission set |
| AWS Organizations | Attach `iam-scp-restrict.json` to the target OU (replace `o-YOUR_ORG_ID`) |
| IDE extension (macOS/Windows/Linux) | Install Amazon Q / AWS Toolkit from approved software catalog; sign in with Identity Center only |
| Console chat | Same IAM policy governs console Q actions |

### Validation

```bash
# Confirm effective permissions for a pilot role (replace ARNs)
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::ACCOUNT_ID:role/QDeveloperPilot \
  --action-names q:SendMessage q:PassRequest qdeveloper:StartAgentSession q:CreatePlugin \
  --output table

# Expect: SendMessage allowed (per tier), PassRequest/StartAgentSession/CreatePlugin denied on Moderate/Strict
```

In the IDE: sign in with Identity Center, open chat, confirm completions work on Moderate/Baseline, and confirm an agent/transform request fails on Moderate/Strict.

### Audit logging (SIEM)

| Source | What to ship | Alert on |
|--------|--------------|----------|
| CloudTrail management events | `q:*`, `qdeveloper:*`, `codewhisperer:*` | `q:PassRequest` Allow outside exception roles; any `CreatePlugin` / `CreateCustomization`; bursts of `AccessDenied` after rollout |
| CloudWatch / Security Hub | Failed auth, unusual region attempts | Region denials from the SCP |

## 5. Workflow-Preservation Notes

| Blocked operation | Risk | Safe equivalent | Exception handling |
|-------------------|------|-----------------|--------------------|
| Q runs AWS APIs via `PassRequest` | Prompt injection or mistaken chat can mutate cloud resources with the user's power | Developer runs `aws` CLI / Terraform / console with least-privilege role; ask Q for the command text only | Tag principal `q-autonomy-exception=approved` and attach a scoped PassRequest allow policy reviewed by security |
| Start agent session / transform | Unattended multi-step code changes | Chat-guided edits reviewed in PRs; use approved upgrade pipelines for language transforms | Time-boxed permission set in a non-prod account |
| Use / register plugins | Data exfil to third-party plugin backends | Approved integrations via central plugin admin role | Security reviews plugin provider, then admin creates plugin once |
| Create customizations | Full codebase ingest for model customization | Use org-approved customization accounts only | Admin role with MFA + change ticket |

### Overlap with other tools

Amazon Q IDE agents and Claude Code / Cursor shell agents can all change local code. Do not assume denying Q agents covers local shell risk from those other tools. Keep Claude Code / Cursor shell policies in their own rollouts.

## Key Security Concepts

### IAM Integration

| Policy | Use case |
|--------|----------|
| `AmazonQFullAccess` | Full admin: manage Q settings, customizations, plugins |
| `AmazonQDeveloperAccess` | AWS managed developer policy (broader than this repo's Moderate) |
| `examples/iam-policy-*.json` | Hardened replacements with explicit PassRequest/agent/plugin posture |

### Access Tiers

| Feature tier | Authentication | Encryption |
|-------------|----------------|------------|
| Free tier (Builder ID) | AWS Builder ID | AWS-owned KMS keys |
| Pro tier (Identity Center) | IAM Identity Center | AWS-owned or customer-managed KMS |

**For enterprise use:** Always use IAM Identity Center (Pro tier) with customer-managed KMS keys.

## Deployment Checklist

1. Use IAM Identity Center (not Builder IDs) for all enterprise users.
2. Apply the tiered customer-managed policy that matches your risk tolerance.
3. Deploy SCPs to region-lock Q and deny high-autonomy actions by default.
4. Enable customer-managed KMS encryption for all Q data.
5. Configure VPC endpoints if Q is used in private network environments.
6. Review CloudTrail for `q:PassRequest`, plugin, and customization events.
7. Set up AWS Config / Security Hub rules for Q configuration compliance.

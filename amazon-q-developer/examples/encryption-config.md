# Amazon Q Developer — Customer-Managed KMS Encryption

## Overview

By default, Amazon Q Developer encrypts data with AWS-owned KMS keys. For enhanced security and compliance, configure customer-managed KMS keys.

## Prerequisites

- Amazon Q Developer Pro subscription (via IAM Identity Center)
- AWS KMS key in the same region as your Q Developer setup
- Appropriate KMS key policy

## KMS Key Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowQDeveloperAccess",
      "Effect": "Allow",
      "Principal": {
        "Service": "q.amazonaws.com"
      },
      "Action": [
        "kms:Decrypt",
        "kms:Encrypt",
        "kms:GenerateDataKey",
        "kms:CreateGrant",
        "kms:RetireGrant",
        "kms:DescribeKey"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "ACCOUNT_ID"
        }
      }
    },
    {
      "Sid": "AllowAdminManagement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT_ID:role/QDeveloperAdmin"
      },
      "Action": [
        "kms:Create*",
        "kms:Describe*",
        "kms:Enable*",
        "kms:List*",
        "kms:Put*",
        "kms:Update*",
        "kms:Revoke*",
        "kms:Disable*",
        "kms:Get*",
        "kms:Delete*",
        "kms:TagResource",
        "kms:UntagResource",
        "kms:ScheduleKeyDeletion",
        "kms:CancelKeyDeletion"
      ],
      "Resource": "*"
    }
  ]
}
```

## Setup Steps

1. **Create KMS key:**
```bash
aws kms create-key \
  --description "Amazon Q Developer encryption key" \
  --key-usage ENCRYPT_DECRYPT \
  --key-spec SYMMETRIC_DEFAULT \
  --tags TagKey=Purpose,TagValue=AmazonQDeveloper
```

2. **Enable automatic rotation:**
```bash
aws kms enable-key-rotation --key-id KEY_ID
```

3. **Apply key policy** (as shown above).

4. **Configure Q Developer** to use the key via the Amazon Q Developer Console:
   - Navigate to **Amazon Q Developer Console → Settings → Encryption**.
   - Select **Customer-managed key**.
   - Enter the KMS key ARN.

5. **Verify encryption:**
```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=Encrypt \
  --max-items 10
```

## Monitoring

- Enable CloudTrail logging for KMS operations.
- Set up CloudWatch alarms for KMS key usage anomalies.
- Monitor for `KMSKeyDisabled` and `KMSKeyDeleted` events.

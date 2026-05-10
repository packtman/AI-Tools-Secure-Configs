# Google Gemini — Organization Policy Constraints

## Restrict Gemini API Usage by Project

Apply organization policies to control which projects can use Gemini:

```bash
# Deny Gemini API in specific projects
gcloud resource-manager org-policies set-policy policy.yaml \
  --project=PROJECT_ID
```

`policy.yaml`:
```yaml
constraint: constraints/serviceuser.services
listPolicy:
  deniedValues:
    - cloudaicompanion.googleapis.com
    - gemini-code-assist.googleapis.com
```

## Restrict to Approved Regions

```bash
gcloud resource-manager org-policies set-policy region-policy.yaml \
  --organization=ORG_ID
```

`region-policy.yaml`:
```yaml
constraint: constraints/gcp.resourceLocations
listPolicy:
  allowedValues:
    - in:us-locations
    - in:eu-locations
```

## Restrict IAM Policy Members

Prevent external users from being granted Gemini access:

```bash
gcloud resource-manager org-policies set-policy domain-policy.yaml \
  --organization=ORG_ID
```

`domain-policy.yaml`:
```yaml
constraint: constraints/iam.allowedPolicyMemberDomains
listPolicy:
  allowedValues:
    - "C0XXXXXXX"
```

(Replace with your Cloud Identity / Google Workspace customer ID.)

## Audit Logging

Enable data access audit logs for Gemini:

```bash
gcloud projects set-iam-policy PROJECT_ID audit-policy.json
```

Include in `audit-policy.json`:
```json
{
  "auditConfigs": [
    {
      "service": "cloudaicompanion.googleapis.com",
      "auditLogConfigs": [
        { "logType": "ADMIN_READ" },
        { "logType": "DATA_READ" },
        { "logType": "DATA_WRITE" }
      ]
    },
    {
      "service": "aiplatform.googleapis.com",
      "auditLogConfigs": [
        { "logType": "ADMIN_READ" },
        { "logType": "DATA_READ" },
        { "logType": "DATA_WRITE" }
      ]
    }
  ]
}
```

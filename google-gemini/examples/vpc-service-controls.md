# Google Gemini — VPC Service Controls Configuration

## Overview

VPC Service Controls create a security perimeter around GCP resources to prevent data exfiltration. Adding Gemini APIs to a perimeter ensures that Gemini traffic is restricted to authorized networks.

## Services to Include

| Service | API name |
|---------|----------|
| Gemini for Google Cloud | `cloudaicompanion.googleapis.com` |
| Gemini Code Assist | `gemini-code-assist.googleapis.com` |
| Developer Connect (if used) | `developerconnect.googleapis.com` |
| Vertex AI (if using Gemini via Vertex) | `aiplatform.googleapis.com` |

## Setup via gcloud

### 1. Create access policy (if not exists)

```bash
gcloud access-context-manager policies create \
  --organization=ORG_ID \
  --title="Gemini Security Policy"
```

### 2. Create access level

```bash
gcloud access-context-manager levels create gemini-access \
  --policy=POLICY_ID \
  --title="Gemini Approved Networks" \
  --basic-level-spec=access-level.yaml
```

`access-level.yaml`:
```yaml
conditions:
  - ipSubnetworks:
      - "203.0.113.0/24"
      - "198.51.100.0/24"
    members:
      - "user:admin@example.com"
      - "serviceAccount:gemini-sa@project.iam.gserviceaccount.com"
```

### 3. Create service perimeter

```bash
gcloud access-context-manager perimeters create gemini-perimeter \
  --policy=POLICY_ID \
  --title="Gemini Perimeter" \
  --resources="projects/PROJECT_NUMBER" \
  --restricted-services="cloudaicompanion.googleapis.com,aiplatform.googleapis.com" \
  --access-levels="accessPolicies/POLICY_ID/accessLevels/gemini-access"
```

### 4. Verify the perimeter

```bash
gcloud access-context-manager perimeters describe gemini-perimeter \
  --policy=POLICY_ID
```

## VPC Network Configuration

### Private Google Access

Enable Private Google Access on subnets that need Gemini access:

```bash
gcloud compute networks subnets update SUBNET_NAME \
  --region=REGION \
  --enable-private-ip-google-access
```

### DNS configuration

Configure private DNS to route Gemini traffic through VPC:

```bash
gcloud dns managed-zones create gemini-private \
  --dns-name="googleapis.com" \
  --visibility="private" \
  --networks="NETWORK_NAME"

gcloud dns record-sets create "*.googleapis.com." \
  --zone="gemini-private" \
  --type="CNAME" \
  --rrdatas="restricted.googleapis.com."
```

## Monitoring

```bash
# Check perimeter violations
gcloud logging read 'resource.type="audited_resource" AND protoPayload.status.code=7' \
  --project=PROJECT_ID \
  --limit=50
```

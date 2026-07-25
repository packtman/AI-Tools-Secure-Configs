# OpenAI Platform: Network Security Configuration

## IP Allowlisting

Restrict API access to known corporate egress IPs to prevent unauthorized usage of stolen API keys.

### Configuration via Dashboard

1. Navigate to **Organization Settings → Security → IP Allowlist**.
2. Add your corporate egress IP ranges in CIDR notation.
3. Enable enforcement.

### Configuration via Admin API

```bash
curl -X POST https://api.openai.com/v1/organization/ip-allowlist \
  -H "Authorization: Bearer $OPENAI_ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_ranges": [
      "203.0.113.0/24",
      "198.51.100.0/24"
    ],
    "enforced": true
  }'
```

### Recommendations

- Include VPN egress IPs for remote workers.
- Include CI/CD runner IPs for automated workloads.
- Test with `enforced: false` before enabling enforcement.
- Maintain an updated list as network infrastructure changes.

---

## Container and Shell Org Network Allowlist

Containers and Shell tools use a two-layer network control:

1. Organization allowlist (admin dashboard): the maximum set of outbound domains.
2. Request-level `network_policy`: must be a subset of the org allowlist.

### Why It Matters

Open network access from skills or shell tools is a high-risk exfiltration path. The org allowlist is the ceiling; applications still must declare a narrower request policy.

### Recommended Values

| Environment | Org allowlist | Request policy |
|-------------|---------------|----------------|
| Regulated | Empty or disabled networking | Do not enable container networking |
| Standard enterprise | Minimal trusted package and VCS hosts only | Subset of org allowlist per job |
| Startups | Optional; start empty and add only proven needs | Always set `network_policy` when networking is enabled |

### Validation

```bash
# Expect failure when request domains are outside the org allowlist.
curl -L 'https://api.openai.com/v1/responses' \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "tools": [{
      "type": "shell",
      "environment": {
        "type": "container_auto",
        "network_policy": {
          "type": "allowlist",
          "allowed_domains": ["evil.example"]
        }
      }
    }],
    "input": "ping an unapproved domain"
  }'
```

### What Breaks If Misconfigured

- Over-broad org allowlists defeat the control.
- Missing request-level `network_policy` can leave networking unavailable or too open depending on product defaults.
- Allowlisting attacker-writable destinations enables prompt-injection-driven exfiltration.

---

## Mutual TLS (mTLS)

For production workloads requiring client certificate authentication.

### Setup

1. Generate a client certificate signed by a trusted CA.
2. Upload the CA certificate to OpenAI via **Organization Settings → Security → mTLS**.
3. Configure your application to present the client certificate on each API call.

### Application Configuration

```python
import httpx

client = httpx.Client(
    cert=("/path/to/client.crt", "/path/to/client.key"),
    verify="/path/to/ca-bundle.crt"
)

response = client.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}
)
```

---

## Proxy Configuration

Route OpenAI API traffic through your corporate proxy for logging and inspection.

### Environment variables

```bash
export HTTPS_PROXY=https://proxy.corp.example.com:8443
export HTTP_PROXY=http://proxy.corp.example.com:8080
export NO_PROXY=localhost,127.0.0.1,.corp.example.com
```

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-...",
    http_client=httpx.Client(proxy="https://proxy.corp.example.com:8443")
)
```

---

## Firewall Rules

Ensure your firewall allows outbound HTTPS to OpenAI endpoints:

| Destination | Port | Protocol | Purpose |
|-------------|------|----------|---------|
| `api.openai.com` | 443 | HTTPS | API calls |
| `platform.openai.com` | 443 | HTTPS | Dashboard access |
| `auth0.openai.com` | 443 | HTTPS | Authentication |
| `files.oaiusercontent.com` | 443 | HTTPS | File uploads/downloads |

Block all other outbound connections to `*.openai.com` subdomains unless explicitly required.

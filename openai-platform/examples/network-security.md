# OpenAI Platform — Network Security Configuration

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

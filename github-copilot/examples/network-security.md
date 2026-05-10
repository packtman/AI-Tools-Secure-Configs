# GitHub Copilot — Network Security Configuration

## Firewall Rules

### Required allowlist

Allow outbound HTTPS (port 443) to these endpoints:

| Hostname pattern | Purpose |
|-----------------|---------|
| `*.business.githubcopilot.com` | Copilot Business plan traffic |
| `*.enterprise.githubcopilot.com` | Copilot Enterprise plan traffic |
| `github.com` | Repository access |
| `api.github.com` | GitHub API |
| `copilot-proxy.githubusercontent.com` | Copilot suggestions |
| `default.exp-tas.com` | Experimentation service |
| `copilot-telemetry.githubusercontent.com` | Telemetry (optional) |

### Recommended blocklist

Block unauthorized Copilot plan usage on corporate networks:

| Hostname pattern | Reason |
|-----------------|--------|
| `*.individual.githubcopilot.com` | Block personal/free Copilot plans |

### Minimum client versions for network routing

| IDE | Extension/Version |
|-----|-------------------|
| VS Code | Copilot Chat ≥ 0.17 |
| JetBrains | Copilot ≥ 1.5.6.5692 |
| Visual Studio | ≥ 2022 17.11 |

---

## Proxy Configuration

### VS Code settings

```json
{
  "http.proxy": "https://proxy.corp.example.com:8443",
  "http.proxyStrictSSL": true,
  "http.proxyAuthorization": null,
  "github.copilot.advanced": {
    "debug.overrideProxyUrl": "https://proxy.corp.example.com:8443"
  }
}
```

### Environment variables

```bash
export HTTPS_PROXY=https://proxy.corp.example.com:8443
export HTTP_PROXY=http://proxy.corp.example.com:8080
export NO_PROXY=localhost,127.0.0.1,.corp.example.com
```

### Custom SSL certificates

If your proxy performs TLS inspection, install the corporate CA certificate:

```bash
# VS Code / Cursor
export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca-bundle.crt

# JetBrains
# Import via IDE: Settings → Tools → Server Certificates → Add
```

---

## Audit Logging

Monitor Copilot usage through GitHub's audit log:

```bash
# List Copilot-related events
gh api \
  -H "Accept: application/vnd.github+json" \
  "/orgs/ORGNAME/audit-log?phrase=action:copilot" \
  --paginate
```

Key events to monitor:
- `copilot.cfb_seat_assignment_created` — Seat assigned
- `copilot.cfb_seat_assignment_removed` — Seat removed
- `copilot.content_exclusion_changed` — Exclusion rules modified
